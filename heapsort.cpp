#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    
    while (true) {
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
            
            i = largest;
        } else {
            break;
        }
    }
}

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
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

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