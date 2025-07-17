import time
import random
import numpy as np

# ベンチマーク1: 素数計算
def find_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    return primes

# ベンチマーク2: フィボナッチ数列（再帰）
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# ベンチマーク3: 行列乗算
def matrix_multiply(a, b):
    n = len(a)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    
    return result

# ベンチマーク4: 配列ソート
def benchmark_sort(size):
    data = [random.randint(0, 999999) for _ in range(size)]
    data.sort()

def measure_time(func, name):
    start = time.time()
    func()
    end = time.time()
    time_ms = (end - start) * 1000
    print(f"{name}: {time_ms:.2f} ms")
    return time_ms

def main():
    print("Python Benchmark")
    print("================")
    
    # 素数計算
    measure_time(lambda: find_primes(100000), "Prime numbers (up to 100,000)")
    
    # フィボナッチ数列
    measure_time(lambda: fibonacci_recursive(35), "Fibonacci (n=35)")
    
    # 行列乗算
    def matrix_test():
        size = 200
        a = [[random.random() for _ in range(size)] for _ in range(size)]
        b = [[random.random() for _ in range(size)] for _ in range(size)]
        matrix_multiply(a, b)
    
    measure_time(matrix_test, "Matrix multiplication (200x200)")
    
    # 配列ソート
    measure_time(lambda: benchmark_sort(1000000), "Array sort (1,000,000 elements)")

if __name__ == "__main__":
    main()