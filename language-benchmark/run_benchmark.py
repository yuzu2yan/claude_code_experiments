#!/usr/bin/env python3
import subprocess
import json
import os
import sys
import time
from datetime import datetime
import platform

def run_command(command, cwd=None):
    """コマンドを実行して出力を取得"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Exception running command: {command}")
        print(f"Exception: {e}")
        return None

def compile_cpp():
    """C++プログラムをコンパイル"""
    print("Compiling C++...")
    cmd = "g++ -O3 -std=c++17 src/cpp/benchmark.cpp -o src/cpp/benchmark"
    result = run_command(cmd)
    return result is not None

def compile_rust():
    """Rustプログラムをコンパイル"""
    print("Compiling Rust...")
    cmd = "cargo build --release"
    result = run_command(cmd, cwd="src/rust")
    return result is not None

def run_cpp_benchmark():
    """C++ベンチマークを実行"""
    print("\nRunning C++ benchmark...")
    output = run_command("./src/cpp/benchmark")
    if output:
        return parse_output(output)
    return None

def run_rust_benchmark():
    """Rustベンチマークを実行"""
    print("\nRunning Rust benchmark...")
    output = run_command("cargo run --release", cwd="src/rust")
    if output:
        return parse_output(output)
    return None

def run_python_benchmark():
    """Pythonベンチマークを実行"""
    print("\nRunning Python benchmark...")
    output = run_command("python3 src/python/benchmark.py")
    if output:
        return parse_output(output)
    return None

def parse_output(output):
    """ベンチマーク出力を解析"""
    results = {}
    lines = output.strip().split('\n')
    
    for line in lines:
        if ': ' in line and ' ms' in line:
            try:
                parts = line.split(': ')
                if len(parts) == 2:
                    test_name = parts[0].strip()
                    time_str = parts[1].replace(' ms', '').strip()
                    results[test_name] = float(time_str)
            except:
                pass
    
    return results

def print_results(all_results):
    """結果を表形式で表示"""
    if not all_results:
        print("No results to display")
        return
    
    # テスト名を取得
    test_names = set()
    for lang_results in all_results.values():
        if lang_results:
            test_names.update(lang_results.keys())
    
    test_names = sorted(list(test_names))
    
    # ヘッダーを表示
    print("\n" + "="*80)
    print("BENCHMARK RESULTS (time in milliseconds)")
    print("="*80)
    print(f"{'Test':<40} {'C++':<15} {'Rust':<15} {'Python':<15}")
    print("-"*80)
    
    # 各テストの結果を表示
    for test in test_names:
        cpp_time = all_results.get('cpp', {}).get(test, 'N/A')
        rust_time = all_results.get('rust', {}).get(test, 'N/A')
        python_time = all_results.get('python', {}).get(test, 'N/A')
        
        cpp_str = f"{cpp_time:.2f}" if isinstance(cpp_time, (int, float)) else cpp_time
        rust_str = f"{rust_time:.2f}" if isinstance(rust_time, (int, float)) else rust_time
        python_str = f"{python_time:.2f}" if isinstance(python_time, (int, float)) else python_time
        
        print(f"{test:<40} {cpp_str:<15} {rust_str:<15} {python_str:<15}")
    
    print("="*80)
    
    # 相対的なパフォーマンスを計算
    print("\nRELATIVE PERFORMANCE (compared to C++)")
    print("="*80)
    
    for test in test_names:
        cpp_time = all_results.get('cpp', {}).get(test)
        rust_time = all_results.get('rust', {}).get(test)
        python_time = all_results.get('python', {}).get(test)
        
        if isinstance(cpp_time, (int, float)) and cpp_time > 0:
            rust_ratio = rust_time / cpp_time if isinstance(rust_time, (int, float)) else 'N/A'
            python_ratio = python_time / cpp_time if isinstance(python_time, (int, float)) else 'N/A'
            
            rust_str = f"{rust_ratio:.2f}x" if isinstance(rust_ratio, (int, float)) else rust_ratio
            python_str = f"{python_ratio:.2f}x" if isinstance(python_ratio, (int, float)) else python_ratio
            
            print(f"{test:<40} C++: 1.00x     Rust: {rust_str:<10} Python: {python_str}")

def save_results(all_results):
    """結果をJSONファイルに保存"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/benchmark_{timestamp}.json"
    
    data = {
        "timestamp": timestamp,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        },
        "results": all_results
    }
    
    os.makedirs("results", exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nResults saved to: {filename}")

def main():
    print("Language Performance Benchmark")
    print("="*40)
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print("="*40)
    
    all_results = {}
    
    # C++をコンパイルして実行
    if compile_cpp():
        results = run_cpp_benchmark()
        if results:
            all_results['cpp'] = results
    else:
        print("Failed to compile C++")
    
    # Rustをコンパイルして実行
    if compile_rust():
        results = run_rust_benchmark()
        if results:
            all_results['rust'] = results
    else:
        print("Failed to compile Rust")
    
    # Pythonを実行
    results = run_python_benchmark()
    if results:
        all_results['python'] = results
    
    # 結果を表示
    print_results(all_results)
    
    # 結果を保存
    save_results(all_results)

if __name__ == "__main__":
    main()