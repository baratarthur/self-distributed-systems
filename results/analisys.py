import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURAÇÃO ---
FILE_PATH = 'results/results_round1.csv'

# --- 1. CARREGAMENTO E PREPARAÇÃO ---
print(f"Carregando dados de {FILE_PATH}...")
try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print("Erro: Arquivo não encontrado.")
    exit()

# Calcular tempo decorrido
start_time = df['timestamp'].min()
df['elapsed'] = df['timestamp'] - start_time

# Classificar Fases
def classificar_fase(segundos):
    if segundos < 25:
        return '1. Monolith'
    elif segundos < 50:
        return '2. Strong Dist.'
    else:
        return '3. Weak Dist.'

df['fase'] = df['elapsed'].apply(classificar_fase)

# --- 2. FILTRAGEM ---
# Usamos 'http_reqs' para contar requisições (métricas de contador)
df_reqs = df[df['metric_name'] == 'http_reqs'].copy()

# --- GRÁFICO 1: GET vs POST por Fase ---
# Agrupar dados
counts = df_reqs.groupby(['fase', 'method'])['metric_value'].count().unstack(fill_value=0)

plt.figure(figsize=(10, 6))
# Plotar barras agrupadas
counts.plot(kind='bar', stacked=False, color=['#3498db', '#e74c3c'], width=0.8)

plt.title('Total de Requests (GET vs POST) por Fase', fontsize=14)
plt.ylabel('Quantidade de Requests', fontsize=12)
plt.xlabel('Fase do Teste', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(title='Método HTTP')
plt.tight_layout()
plt.savefig('grafico_metodos_fase.png')
print("Gráfico 1 salvo: grafico_metodos_fase.png")

# --- GRÁFICO 2: Throughput (RPS) ao Longo do Tempo ---
# Agrupar por segundo (arredondando o tempo decorrido)
df_reqs['segundo_exato'] = df_reqs['elapsed'].astype(int)
throughput = df_reqs.groupby('segundo_exato')['metric_value'].count()

plt.figure(figsize=(14, 6))

# Plotar linha de RPS
plt.plot(throughput.index, throughput.values, color='#8e44ad', linewidth=2, label='RPS (Req/s)')
# Preencher área sob a curva para melhor visualização
plt.fill_between(throughput.index, throughput.values, color='#8e44ad', alpha=0.1)

# Marcar as fases no fundo
ymax = throughput.max() * 1.1
plt.ylim(0, ymax)
plt.axvspan(0, 25, color='gray', alpha=0.1, label='Monolith (0-25s)')
plt.axvspan(25, 50, color='green', alpha=0.1, label='Strong Dist. (25-50s)')
plt.axvspan(50, df['elapsed'].max(), color='orange', alpha=0.1, label='Weak Dist. (50s+)')

plt.title('Throughput (Requests por Segundo) durante o Teste', fontsize=14)
plt.ylabel('RPS', fontsize=12)
plt.xlabel('Tempo de Teste (s)', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('grafico_throughput.png')
print("Gráfico 2 salvo: grafico_throughput.png")

plt.show()