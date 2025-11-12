#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

/**
 * @brief Restaura a propriedade do Max-Heap na subárvore com raiz em 'i'.
 * @param arr O vetor (representando o heap).
 * @param n O tamanho do heap.
 * @param i O índice da raiz da subárvore.
 */
void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n && arr[l] > arr[largest]) {
        largest = l;
    }

    if (r < n && arr[r] > arr[largest]) {
        largest = r;
    }

    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        
        heapify(arr, n, largest);
    }
}

/**
 * @brief Função principal para ordenar um vetor usando Heap Sort.
 * @param arr O vetor a ser ordenado.
 */
void heapSort(std::vector<int>& arr) {
    int n = arr.size();

    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }

    for (int i = n - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);

        heapify(arr, i, 0);
    }
}

int main() {
    
    std::vector<int> arr;
    int num;
    while (std::cin >> num) {
        arr.push_back(num);
    }

    auto start = std::chrono::high_resolution_clock::now();

    heapSort(arr);

    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed = end - start;

    std::cout << elapsed.count() << std::endl;

    return 0;
}