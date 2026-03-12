import pandas as pd
import matplotlib.pyplot as plt

def gerar_graficos(csv_path='load_test.csv'):
    # 1. Carregamento com tratamento aprimorado
    try:
        # low_memory=False evita avisos se o CSV do k6 for muito grande e tiver tipos mistos
        df = pd.read_csv(csv_path, low_memory=False)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_path}' não foi encontrado. Verifique o caminho.")
        return

    print("Processando e agregando os dados do k6...")

    # Converter timestamp e remover linhas inválidas de forma segura
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp', 'metric_name', 'metric_value'], inplace=True)

    # 2. Normalizar o tempo para "segundo de teste" (começando do 0)
    df['segundo_de_teste'] = (df['timestamp'] - df['timestamp'].min()).astype(int)

    # 3. Filtrar e agregar os dados
    df_reqs = df[df['metric_name'] == 'http_reqs']
    df_lat = df[df['metric_name'] == 'http_req_duration']

    # Usando os índices no agrupamento para um merge mais rápido e limpo depois
    reqs_por_segundo = df_reqs.groupby('segundo_de_teste')['metric_value'].sum().rename('requisicoes')
    lat_por_segundo = df_lat.groupby('segundo_de_teste')['metric_value'].mean().rename('latencia')

    # Calcular o Percentil 95 (P95) geral da latência para referência
    p95_latencia = df_lat['metric_value'].quantile(0.95) if not df_lat.empty else 0

    # Mesclar dados garantindo que todos os segundos estejam representados
    df_final = pd.merge(reqs_por_segundo, lat_por_segundo, left_index=True, right_index=True, how='outer').fillna(0)
    df_final.reset_index(inplace=True)

    x = df_final['segundo_de_teste']
    y_req = df_final['requisicoes']
    y_lat = df_final['latencia']

    # 4. Configurar a figura
    # O sharex=True alinha os dois gráficos horizontalmente
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # --- Primeiro Gráfico: Linha (RPS) ---
    ax1.plot(x, y_req, color='#1f77b4', linewidth=2, marker='o', markersize=4, label='RPS')
    ax1.set_title('Volume de Requisições por Segundo', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Requisições (RPS)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper right')

    # --- Segundo Gráfico: Pistão (Latência Média) ---
    # Correção: O gráfico de pistão real exige o uso do stem()
    markerlines, stemlines, baseline = ax2.stem(x, y_lat, basefmt=" ")
    
    # Estilizando o pistão
    plt.setp(stemlines, 'linewidth', 1.5, 'color', '#ff7f0e', alpha=0.8)
    plt.setp(markerlines, 'markersize', 5, 'color', '#d62728', 'marker', 's')
    
    # Adicionando a linha do P95 para enriquecer a análise
    if p95_latencia > 0:
        ax2.axhline(y=p95_latencia, color='purple', linestyle='--', alpha=0.7, label=f'P95 Geral: {p95_latencia:.2f}ms')
        ax2.legend(loc='upper right')

    ax2.set_title('Latência Média por Segundo', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Tempo de Teste (segundos)', fontsize=12)
    ax2.set_ylabel('Latência Média (ms)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)

    # Ajustar layout e exibir
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    gerar_graficos('load_test.csv')