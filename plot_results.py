import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

RESULTS_FILE = "benchmark_results.csv"

def load_data(filename):
    if not os.path.exists(filename):
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        print("Certifique-se que 'benchmark_results.csv' está no mesmo diretório.")
        return None
        
    try:
        df = pd.read_csv(filename)
        df['mean_time_ms'] = df['mean_time_sec'] * 1000
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None

def plot_log_log(df):
    print("Gerando Gráfico 1 (Log-Log)...")
    data_random = df[df['case_type'] == 'random']
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data_random, x='size', y='mean_time_ms', hue='language', marker='o')
    
    plt.xscale('log')
    plt.yscale('log')
    
    plt.title('Gráfico 1: Tempo de Execução vs. Tamanho (Escala Log-Log)\nCaso Aleatório', fontsize=16)
    plt.xlabel('Tamanho da Entrada (N) - Escala Log', fontsize=12)
    plt.ylabel('Tempo Médio (ms) - Escala Log', fontsize=12)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(title='Linguagem')
    
    output_filename = 'grafico_1_log_log.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"-> Salvo como '{output_filename}'")

def plot_linear_comparison(df):
    print("Gerando Gráfico 2 (Linear - Custo da Abstração)...")
    data_random = df[df['case_type'] == 'random']
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data_random, x='size', y='mean_time_ms', hue='language', marker='o')
    
    plt.title('Gráfico 2: Custo da Abstração (Python vs. C++)\nCaso Aleatório - Escala Linear', fontsize=16)
    plt.xlabel('Tamanho da Entrada (N)', fontsize=12)
    plt.ylabel('Tempo Médio (ms)', fontsize=12)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(title='Linguagem')
    
    plt.ticklabel_format(style='plain', axis='y')
    
    output_filename = 'grafico_2_linear.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"-> Salvo como '{output_filename}'")

def plot_case_analysis(df):
    print("Gerando Gráfico 3 (Análise de Caso C++)...")
    
    data_cpp = df[df['language'] == 'c++']
    
    largest_n = data_cpp['size'].max()
    
    data_plot = data_cpp[data_cpp['size'] == largest_n]
    
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(data=data_plot, x='case_type', y='mean_time_ms', palette='viridis')
    
    plt.title(f'Gráfico 3: Análise de Caso (Não-Adaptativo) - C++\nN = {largest_n:,.0f}'.replace(',', '.'), fontsize=16)
    plt.xlabel('Tipo de Dados (Caso)', fontsize=12)
    plt.ylabel('Tempo Médio (ms)', fontsize=12)
    plt.grid(True, which="major", axis='y', ls="--", alpha=0.5)
    
    for p in barplot.patches:
        barplot.annotate(f'{p.get_height():.2f} ms', 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='center', 
                         xytext=(0, 9), 
                         textcoords='offset points')
    
    output_filename = 'grafico_3_case_analysis.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"-> Salvo como '{output_filename}'")


def main():
    sns.set_theme(style="whitegrid")
    
    df = load_data(RESULTS_FILE)
    
    if df is not None:
        plot_log_log(df)
        plot_linear_comparison(df)
        plot_case_analysis(df)
        print("\nTodos os gráficos foram gerados com sucesso!")

if __name__ == "__main__":
    try:
        import pandas
        import matplotlib
        import seaborn
    except ImportError as e:
        print(f"Erro: Dependência não encontrada: {e.name}")
        print("Por favor, instale as bibliotecas necessárias com:")
        print("pip install pandas matplotlib seaborn")
        exit(1)
        
    main()