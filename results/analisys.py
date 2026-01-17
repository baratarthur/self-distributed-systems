import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração estética
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)

# Lista para armazenar os dados de todos os rounds
all_data = []

# --- 1. COLETA DE DADOS ---
for round_num in range(1, 4):
    FILE_PATH = f'results/30u/results_round{round_num}.csv'
    
    print(f"Lendo {FILE_PATH}...")
    try:
        # Carregar (simulação para o exemplo funcionar, use pd.read_csv no real)
        df = pd.read_csv(FILE_PATH)
        
        # --- Simulação de dados (Remova isso no seu código real) ---
        # df = pd.DataFrame({
        #     'timestamp': range(100),
        #     'metric_name': ['http_reqs'] * 100,
        #     'method': ['GET'] * 50 + ['POST'] * 50,
        #     'metric_value': [1] * 100
        # })
        # -----------------------------------------------------------

    except FileNotFoundError:
        print(f"Aviso: {FILE_PATH} não encontrado.")
        continue

    # Processamento de Tempo e Fase
    start_time = df['timestamp'].min()
    df['elapsed'] = df['timestamp'] - start_time

    def classificar_fase(segundos):
        if segundos < 25: return '1. Monolith'
        elif segundos < 50: return '2. Strong Dist.'
        else: return '3. Weak Dist.'

    df['fase'] = df['elapsed'].apply(classificar_fase)
    
    # Filtrar apenas requisições
    df_reqs = df[df['metric_name'] == 'http_reqs'].copy()
    
    # ADICIONAR COLUNA IDENTIFICADORA DO ROUND (Crucial para o gráfico único)
    # Ex: "Cenário 1 (3 comps)", "Cenário 2 (4 comps)"
    label_cenario = f'Round {round_num}\n({round_num + 2} Comps)'
    df_reqs['cenario'] = label_cenario
    
    # Adicionar à lista geral
    all_data.append(df_reqs)

# --- 2. CONSOLIDAÇÃO ---
if not all_data:
    print("Nenhum dado carregado.")
    exit()

# Cria um único DataFrame com tudo (Round 1, 2 e 3 empilhados)
df_final = pd.concat(all_data)

# Agrupar para contar as requisições
# Precisamos agrupar por Cenario, Fase e Metodo
df_counts = df_final.groupby(['cenario', 'fase', 'method'])['metric_value'].count().reset_index(name='count')

# --- 3. PLOTAGEM ÚNICA (FACETGRID) ---
# kind='bar': Cria barras
# x='fase': Eixo X
# y='count': Altura da barra
# hue='cenario': As CORES diferenciarão os Rounds (comparação direta)
# col='method': Cria dois subplots lado a lado (um para GET, um para POST)

g = sns.catplot(
    data=df_counts, 
    kind="bar",
    x="fase", 
    y="count", 
    hue="cenario",      # Onde a comparação acontece
    col="method",       # Separa GET e POST
    palette="viridis",  # Paleta de cores profissional
    height=5,           # Altura de cada subplot
    aspect=1,           # Largura relativa
    edgecolor="black",  # Borda nas barras
    alpha=0.9           # Transparência leve
)

# --- 4. AJUSTES FINAIS ---
g.set_axis_labels("Test Phase", "Total Requests")
g.set_titles("{col_name} Requests") # Títulos dos subplots (GET Requests / POST Requests)

# Ajuste da legenda (título)
g._legend.set_title("Configuration")

# Melhorar a visualização dos números (opcional: adicionar labels nas barras)
for ax in g.axes.flat:
    ax.grid(True, axis='y', linestyle='--', alpha=0.5, zorder=0)
    
    # Opcional: Escrever o valor em cima da barra
    for container in ax.containers:
        ax.bar_label(container, padding=3, fmt='%d', fontsize=9)

plt.subplots_adjust(top=0.85) # Espaço para o título geral
g.figure.suptitle('Performance Comparison: Evolution of Remote Components', fontsize=16, fontweight='bold')

plt.savefig('results/30u/comparison_all_rounds.pdf', bbox_inches='tight')
print("Gráfico comparativo salvo!")

# ----------------------------------------
# analyze trhoughput
# ----------------------------------------

sns.set_theme(style="white", context="paper", font_scale=1.1)

throughput_data = []

# --- 1. PROCESSAMENTO GARANTINDO ORDEM ---
# Iterar explicitamente na ordem 1, 2, 3
for round_num in [1, 2, 3]: 
    FILE_PATH = f'results/30u/results_round{round_num}.csv'
    
    print(f"Processando {FILE_PATH}...")
    try:
        df = pd.read_csv(FILE_PATH)
        
        # --- CORREÇÃO CRÍTICA 1: ORDENAÇÃO ---
        # Garante que o tempo comece do menor para o maior. 
        # Sem isso, o gráfico de linha e o fill_between "quebram" ou invertem.
        df['timestamp'] = pd.to_numeric(df['timestamp']) # Garante que é número
        df = df.sort_values(by='timestamp', ascending=True)
        
        # Calcular tempo decorrido
        start_time = df['timestamp'].iloc[0] # Pega o primeiro após ordenar
        df['elapsed'] = df['timestamp'] - start_time
        
        # Agrupar por segundo
        df_reqs = df[df['metric_name'] == 'http_reqs'].copy()
        df_reqs['segundo_exato'] = df_reqs['elapsed'].astype(int)
        
        # Contagem (RPS)
        df_rps = df_reqs.groupby('segundo_exato')['metric_value'].count().reset_index(name='rps')
        
        # Metadados
        df_rps['round'] = round_num
        df_rps['titulo'] = f"Round {round_num}: {round_num + 2} Remote Components"
        
        throughput_data.append(df_rps)

    except FileNotFoundError:
        print(f"Erro: {FILE_PATH} não encontrado.")
        continue

if not throughput_data:
    print("Nenhum dado encontrado.")
    exit()

# --- 2. PLOTAGEM ---
# nrows=3 garante Round 1 em cima, Round 2 no meio, Round 3 embaixo
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 10), sharex=True, sharey=True)

# Se quiser inverter a ordem visual (Round 3 no topo), descomente a linha abaixo:
# throughput_data.reverse() 

colors = ['#8e44ad', '#2980b9', '#2c3e50'] 

for i, df in enumerate(throughput_data):
    # Se houver menos rounds que subplots, evita erro de índice
    if i >= len(axes): break
    
    ax = axes[i]
    color = colors[i]
    
    # Plotagem
    ax.plot(df['segundo_exato'], df['rps'], color=color, linewidth=1.5)
    ax.fill_between(df['segundo_exato'], df['rps'], color=color, alpha=0.1)
    
    # Fases (Fundo Colorido)
    ax.axvspan(0, 25, color='gray', alpha=0.1, lw=0)      # Monolito
    ax.axvspan(25, 50, color='#27ae60', alpha=0.1, lw=0)  # Dist. Forte
    # Vai até o fim dos dados desse round específico
    max_time = df['segundo_exato'].max()
    ax.axvspan(50, max_time if max_time > 50 else 51, color='#e67e22', alpha=0.1, lw=0) # Dist. Fraca

    # Títulos e Labels
    ax.set_title(df['titulo'].iloc[0], loc='left', fontsize=11, fontweight='bold')
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_ylabel('RPS')
    
    # Adicionar labels das fases apenas no PRIMEIRO gráfico (topo)
    if i == 0:
        ylim = ax.get_ylim()
        # Ajuste a altura (0.9) conforme necessário
        ax.text(12.5, ylim[1]*0.85, "Monolith", ha='center', fontsize=9, color='dimgray')
        ax.text(37.5, ylim[1]*0.85, "Strong Dist.", ha='center', fontsize=9, color='darkgreen')
        ax.text(60, ylim[1]*0.85, "Weak Dist.", ha='center', fontsize=9, color='#d35400')

axes[-1].set_xlabel('Test Time (seconds)')
plt.tight_layout()
plt.savefig('results/30u/throughput_comparison_fixed.pdf', bbox_inches='tight')
print("Gráfico corrigido salvo.")