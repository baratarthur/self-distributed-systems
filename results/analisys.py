import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- CONFIGURAÇÃO ESTÉTICA (Mantida para Artigo Científico) ---
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 12,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "lines.linewidth": 1.5
})

def processar_dados_k6_json(file_path):
    print("Carregando dados JSON (isso pode levar alguns instantes)...")
    
    # Lê o arquivo JSON onde cada linha é um objeto independente
    try:
        df_raw = pd.read_json(file_path, lines=True)
    except ValueError:
        print("Erro ao ler JSON. Verifique se o arquivo está no formato correto (NDJSON).")
        return pd.DataFrame()

    # O k6 gera muitos tipos de métricas (Point, Metric, etc). Queremos apenas os 'Point'
    df = df_raw[df_raw['type'] == 'Point'].copy()

    # O JSON do k6 aninha os valores dentro de 'data'. 
    # Estrutura típica: {'metric': 'http_req_duration', 'data': {'time': '...', 'value': 123, 'tags': {...}}}
    
    # Extração otimizada dos dados aninhados
    # Criamos colunas planas para facilitar a plotagem
    print("Processando e normalizando dados...")
    
    # Extraindo timestamp e valor
    df['timestamp'] = df['data'].apply(lambda x: x.get('time'))
    df['metric_value'] = df['data'].apply(lambda x: x.get('value'))
    
    # Extraindo a tag 'name' (fundamental para saber qual requisição é qual)
    # A estrutura é data -> tags -> name
    df['name'] = df['data'].apply(lambda x: x.get('tags', {}).get('name', 'Outros'))
    
    # Renomear coluna 'metric' para 'metric_name' para manter compatibilidade
    df.rename(columns={'metric': 'metric_name'}, inplace=True)

    # Converter timestamp para datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Limpeza: remover colunas originais pesadas
    df_clean = df[['timestamp', 'metric_name', 'metric_value', 'name']].copy()
    
    return df_clean

def gerar_grafico_latencia(df):
    print("Gerando gráfico de latência...")
    
    # Filtrar apenas a duração das requisições HTTP
    df_lat = df[df['metric_name'] == 'http_req_duration'].copy()
    
    if df_lat.empty:
        print("Aviso: Nenhuma métrica 'http_req_duration' encontrada.")
        return

    # Remover outliers extremos (acima de 99%) para limpar o gráfico
    q99 = df_lat['metric_value'].quantile(0.99)
    df_lat = df_lat[df_lat['metric_value'] < q99]

    # Reamostragem (Resample)
    df_lat.set_index('timestamp', inplace=True)
    
    # Agrupa por Nome da Requisição e calcula o P95 a cada 5 segundos
    df_resampled = df_lat.groupby('name')['metric_value'].resample('5s').quantile(0.95).reset_index()

    # Plot
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid") 
    
    sns.lineplot(
        data=df_resampled, 
        x='timestamp', 
        y='metric_value', 
        hue='name', 
        style='name', 
        markers=False, 
        dashes=True
    )

    plt.title("Latência de Requisição (P95)")
    plt.xlabel("Tempo de Execução")
    plt.ylabel("Latência (ms)")
    plt.legend(title="Operação")
    plt.tight_layout()
    
    plt.savefig('fig1_latencia_json.pdf', format='pdf', bbox_inches='tight')
    print("Gráfico de latência salvo (PDF).")

def gerar_grafico_leitura_escrita(df):
    print("Gerando gráfico de Leitura/Escrita...")
    
    # Usamos a métrica de duração para contar quantas requisições ocorreram
    df_reqs = df[df['metric_name'] == 'http_req_duration'].copy()
    
    if df_reqs.empty:
        return

    # Lógica de Categorização
    def categorizar(nome):
        nome = str(nome)
        if 'GetFeed' in nome:
            return 'Leitura (Read)'
        elif 'CreatePost' in nome or 'LikePost' in nome:
            return 'Escrita (Write)'
        return None # Ignora 'Outros' ou requisições sem tag

    df_reqs['tipo_operacao'] = df_reqs['name'].apply(categorizar)
    
    # Remover nulos (tags que não nos interessam)
    df_reqs = df_reqs.dropna(subset=['tipo_operacao'])
    
    # Contagem percentual
    contagem = df_reqs['tipo_operacao'].value_counts(normalize=True) * 100
    df_plot = contagem.reset_index()
    df_plot.columns = ['Operação', 'Porcentagem']
    
    # Plot
    plt.figure(figsize=(6, 6))
    sns.set_style("whitegrid")
    
    ax = sns.barplot(x='Operação', y='Porcentagem', data=df_plot, palette="Greys_d", edgecolor="black")
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points')

    plt.title("Proporção: Leitura vs. Escrita")
    plt.ylabel("Total de Requisições (%)")
    plt.ylim(0, 110)
    plt.tight_layout()
    
    plt.savefig('fig2_rw_json.pdf', format='pdf', bbox_inches='tight')
    print("Gráfico de distribuição salvo (PDF).")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <numero_do_round>")
        sys.exit(1)

    round_arg = sys.argv[1]
    ARQUIVO = f'results/results_round{round_arg}.json' # Nome do arquivo gerado pelo k6
    
    try:
        dados = processar_dados_k6_json(ARQUIVO)
        gerar_grafico_latencia(dados)
        gerar_grafico_leitura_escrita(dados)
        print("Processo concluído com sucesso.")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{ARQUIVO}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")