use std::time::Instant;
use rand::Rng;

// ベンチマーク1: 素数計算
fn find_primes(n: usize) -> Vec<usize> {
    let mut is_prime = vec![true; n + 1];
    let mut primes = Vec::new();
    is_prime[0] = false;
    is_prime[1] = false;
    
    for i in 2..=n {
        if is_prime[i] {
            primes.push(i);
            let mut j = i * i;
            while j <= n {
                is_prime[j] = false;
                j += i;
            }
        }
    }
    primes
}

// ベンチマーク2: フィボナッチ数列（再帰）
fn fibonacci_recursive(n: u32) -> u64 {
    match n {
        0 | 1 => n as u64,
        _ => fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2),
    }
}

// ベンチマーク3: 行列乗算
fn matrix_multiply(a: &Vec<Vec<f64>>, b: &Vec<Vec<f64>>) -> Vec<Vec<f64>> {
    let n = a.len();
    let mut result = vec![vec![0.0; n]; n];
    
    for i in 0..n {
        for j in 0..n {
            for k in 0..n {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    result
}

// ベンチマーク4: 配列ソート
fn benchmark_sort(size: usize) {
    let mut rng = rand::thread_rng();
    let mut data: Vec<i32> = (0..size).map(|_| rng.gen_range(0..1000000)).collect();
    data.sort();
}

fn measure_time<F>(func: F, name: &str) -> f64
where
    F: FnOnce(),
{
    let start = Instant::now();
    func();
    let duration = start.elapsed();
    let time_ms = duration.as_secs_f64() * 1000.0;
    println!("{}: {:.2} ms", name, time_ms);
    time_ms
}

fn main() {
    println!("Rust Benchmark");
    println!("==============");
    
    // 素数計算
    measure_time(|| { find_primes(100000); }, "Prime numbers (up to 100,000)");
    
    // フィボナッチ数列
    measure_time(|| { fibonacci_recursive(35); }, "Fibonacci (n=35)");
    
    // 行列乗算
    measure_time(|| {
        let size = 200;
        let mut rng = rand::thread_rng();
        let a: Vec<Vec<f64>> = (0..size)
            .map(|_| (0..size).map(|_| rng.gen()).collect())
            .collect();
        let b: Vec<Vec<f64>> = (0..size)
            .map(|_| (0..size).map(|_| rng.gen()).collect())
            .collect();
        matrix_multiply(&a, &b);
    }, "Matrix multiplication (200x200)");
    
    // 配列ソート
    measure_time(|| { benchmark_sort(1000000); }, "Array sort (1,000,000 elements)");
}