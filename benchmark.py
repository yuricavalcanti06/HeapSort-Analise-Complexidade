import numpy as np
import timeit
import subprocess
import os
import csv
import statistics
import sys
try:
    from heapsort import heapSort as heapSort_py
except ImportError:
    print("Erro: Não foi possível encontrar o arquivo 'heapsort.py'.")
    print("Certifique-se que 'heapsort.py' está no mesmo diretório.")
    sys.exit(1)


SIZES = [1000, 10000, 50000, 100000, 250000] # Tamanhos dos arrays
CASES = ["random", "sorted", "reversed"]     # Casos de teste
RUNS = 30                                    # Número de execuções (conforme solicitado: 30)
CPP_SOURCE = "heapsort.cpp"                  # Arquivo fonte C++
RESULTS_FILE = "benchmark_results.csv"       # Arquivo de saída

# Determina o nome do executável baseado no SO
if os.name == 'nt': # Windows
    CPP_EXECUTABLE = "./heapsort_cpp.exe"
else: # Linux, macOS, etc.
    CPP_EXECUTABLE = "./heapsort_cpp"


def generate_data(n, case_type="random"):
    """
    Gera dados de teste usando numpy para eficiência.
    Retorna uma lista Python, pois é isso que as funções de sort esperam.
    """
    print(f"Gerando dados: N={n}, Caso={case_type}...")
    if case_type == "random":
        arr = np.random.randint(0, n * 10, size=n, dtype=np.int64)
    elif case_type == "sorted":
        arr = np.arange(n, dtype=np.int64)
    elif case_type == "reversed":
        arr = np.arange(n - 1, -1, -1, dtype=np.int64)
    else:
        raise ValueError(f"Tipo de caso desconhecido: {case_type}")
    
    return list(arr)

def benchmark_python(data, runs):
    """
    Executa o benchmark para a implementação Python.
    Mede o tempo {runs} vezes e retorna uma lista de tempos.
    """
    times = []
    print(f"Executando Python (N={len(data)}, {runs} execuções)...")
    for i in range(runs):
        data_copy = data.copy() 
        
        start_time = timeit.default_timer()
        heapSort_py(data_copy)
        end_time = timeit.default_timer()
        
        times.append(end_time - start_time)
        print(f"  Run {i+1}/{runs}... {times[-1]:.4f}s")
        
    return times

def benchmark_cpp(data, runs):
    """
    Executa o benchmark para a implementação C++.
    Mede o tempo {runs} vezes e retorna uma lista de tempos.
    """
    times = []
    data_str = " ".join(map(str, data))
    
    print(f"Executando C++ (N={len(data)}, {runs} execuções)...")
    for i in range(runs):
        try:
            process = subprocess.run(
                [CPP_EXECUTABLE],
                input=data_str,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            time_str = process.stdout.strip()
            times.append(float(time_str))
            print(f"  Run {i+1}/{runs}... {times[-1]:.4f}s")
            
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar C++: {e}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return []
    return times

def compile_cpp():
    print(f"Compilando {CPP_SOURCE} com g++ -O3...")
    try:
        subprocess.run(
            ["g++", "-o", CPP_EXECUTABLE, CPP_SOURCE, "-std=c++11", "-O3"],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Compilação bem-sucedida. Executável: {CPP_EXECUTABLE}")
        return True
    except FileNotFoundError:
        print("Erro: 'g++' não encontrado.")
        print("Verifique se o compilador C++ (g++) está instalado e no PATH do seu sistema.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Erro de compilação C++:")
        print(e.stderr)
        return False

def main():
    """
    Loop principal do benchmark.
    """
    if not os.path.exists(CPP_SOURCE):
        print(f"Erro: Arquivo fonte '{CPP_SOURCE}' não encontrado.")
        return

    if not compile_cpp():
        return

    results = []

    print(f"\n--- Iniciando Benchmark ---")
    print(f"Execuções por teste: {RUNS}")
    print(f"Tamanhos (N): {SIZES}")
    print(f"Casos: {CASES}")
    print(f"Resultados serão salvos em {RESULTS_FILE}")

    try:
        for size in SIZES:
            for case in CASES:
                
                data = generate_data(size, case)
                
                py_times = benchmark_python(data, RUNS)
                if py_times:
                    py_mean = statistics.mean(py_times)
                    py_std = statistics.stdev(py_times) if RUNS > 1 else 0.0
                    results.append(["python", case, size, py_mean, py_std])
                    print(f"-> Python Média: {py_mean:.6f}s (std: {py_std:.6f}s)\n")

                cpp_times = benchmark_cpp(data, RUNS)
                if cpp_times:
                    cpp_mean = statistics.mean(cpp_times)
                    cpp_std = statistics.stdev(cpp_times) if RUNS > 1 else 0.0
                    results.append(["c++", case, size, cpp_mean, cpp_std])
                    print(f"-> C++ Média: {cpp_mean:.6f}s (std: {cpp_std:.6f}s)\n")

    finally:
        if os.path.exists(CPP_EXECUTABLE):
            try:
                os.remove(CPP_EXECUTABLE)
                print(f"Limpeza: removido {CPP_EXECUTABLE}")
            except OSError as e:
                print(f"Aviso: não foi possível remover {CPP_EXECUTABLE}: {e}")

    if results:
        try:
            with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["language", "case_type", "size", "mean_time_sec", "std_dev_sec"])
                writer.writerows(results)
            print(f"\n--- Benchmark Concluído ---")
            print(f"Resultados salvos com sucesso em {RESULTS_FILE}")
        except IOError as e:
            print(f"Erro ao salvar arquivo CSV: {e}")
    else:
        print("Nenhum resultado foi gerado para salvar.")


if __name__ == "__main__":
    main()