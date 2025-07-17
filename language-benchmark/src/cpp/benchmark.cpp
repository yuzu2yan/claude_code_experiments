#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>
#include <algorithm>
#include <numeric>

// ベンチマーク1: 素数計算
std::vector<int> find_primes(int n) {
    std::vector<bool> is_prime(n + 1, true);
    std::vector<int> primes;
    is_prime[0] = is_prime[1] = false;
    
    for (int i = 2; i <= n; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
            for (long long j = (long long)i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }
    return primes;
}

// ベンチマーク2: フィボナッチ数列（再帰）
long long fibonacci_recursive(int n) {
    if (n <= 1) return n;
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2);
}

// ベンチマーク3: 行列乗算
std::vector<std::vector<double>> matrix_multiply(
    const std::vector<std::vector<double>>& a,
    const std::vector<std::vector<double>>& b) {
    int n = a.size();
    std::vector<std::vector<double>> result(n, std::vector<double>(n, 0.0));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    return result;
}

// ベンチマーク4: 配列ソート
void benchmark_sort(int size) {
    std::vector<int> data(size);
    for (int i = 0; i < size; i++) {
        data[i] = rand() % 1000000;
    }
    std::sort(data.begin(), data.end());
}

template<typename Func>
double measure_time(Func func, const std::string& name) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    double time_ms = duration.count() / 1000.0;
    
    std::cout << name << ": " << time_ms << " ms" << std::endl;
    return time_ms;
}

int main() {
    std::cout << "C++ Benchmark" << std::endl;
    std::cout << "=============" << std::endl;
    
    // 素数計算
    measure_time([]() { find_primes(100000); }, "Prime numbers (up to 100,000)");
    
    // フィボナッチ数列
    measure_time([]() { fibonacci_recursive(35); }, "Fibonacci (n=35)");
    
    // 行列乗算
    measure_time([]() {
        int size = 200;
        std::vector<std::vector<double>> a(size, std::vector<double>(size));
        std::vector<std::vector<double>> b(size, std::vector<double>(size));
        
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                a[i][j] = rand() / (double)RAND_MAX;
                b[i][j] = rand() / (double)RAND_MAX;
            }
        }
        matrix_multiply(a, b);
    }, "Matrix multiplication (200x200)");
    
    // 配列ソート
    measure_time([]() { benchmark_sort(1000000); }, "Array sort (1,000,000 elements)");
    
    return 0;
}