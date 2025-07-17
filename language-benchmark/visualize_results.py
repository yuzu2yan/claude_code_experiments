#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def load_latest_results():
    """最新の結果ファイルを読み込む"""
    result_files = glob.glob("results/benchmark_*.json")
    if not result_files:
        print("No result files found in results/ directory")
        return None
    
    latest_file = max(result_files)
    with open(latest_file, 'r') as f:
        return json.load(f)

def create_bar_chart(data):
    """言語別の実行時間を棒グラフで表示"""
    results = data['results']
    
    # テスト名と言語を取得
    test_names = set()
    for lang_results in results.values():
        test_names.update(lang_results.keys())
    test_names = sorted(list(test_names))
    
    languages = ['cpp', 'rust', 'python']
    language_labels = ['C++', 'Rust', 'Python']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    # 各テストごとにサブプロットを作成
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Language Performance Comparison', fontsize=16)
    axes = axes.flatten()
    
    for idx, test in enumerate(test_names):
        if idx >= len(axes):
            break
            
        ax = axes[idx]
        times = []
        
        for lang in languages:
            time = results.get(lang, {}).get(test, 0)
            times.append(time if isinstance(time, (int, float)) else 0)
        
        bars = ax.bar(language_labels, times, color=colors)
        ax.set_title(test, fontsize=12)
        ax.set_ylabel('Time (ms)')
        ax.set_yscale('log')  # 対数スケールで表示
        
        # 値をバーの上に表示
        for bar, time in zip(bars, times):
            if time > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                       f'{time:.1f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('results/performance_comparison.png', dpi=300, bbox_inches='tight')
    print("Chart saved to: results/performance_comparison.png")
    plt.show()

def create_relative_performance_chart(data):
    """C++を基準とした相対パフォーマンスチャート"""
    results = data['results']
    
    test_names = set()
    for lang_results in results.values():
        test_names.update(lang_results.keys())
    test_names = sorted(list(test_names))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(test_names))
    width = 0.25
    
    cpp_baseline = [1.0] * len(test_names)
    rust_ratios = []
    python_ratios = []
    
    for test in test_names:
        cpp_time = results.get('cpp', {}).get(test, 1)
        rust_time = results.get('rust', {}).get(test, cpp_time)
        python_time = results.get('python', {}).get(test, cpp_time)
        
        if isinstance(cpp_time, (int, float)) and cpp_time > 0:
            rust_ratio = rust_time / cpp_time if isinstance(rust_time, (int, float)) else 1
            python_ratio = python_time / cpp_time if isinstance(python_time, (int, float)) else 1
        else:
            rust_ratio = 1
            python_ratio = 1
        
        rust_ratios.append(rust_ratio)
        python_ratios.append(python_ratio)
    
    bars1 = ax.bar(x - width, cpp_baseline, width, label='C++ (baseline)', color='#1f77b4')
    bars2 = ax.bar(x, rust_ratios, width, label='Rust', color='#ff7f0e')
    bars3 = ax.bar(x + width, python_ratios, width, label='Python', color='#2ca02c')
    
    ax.set_ylabel('Relative Performance (lower is better)')
    ax.set_title('Performance Relative to C++')
    ax.set_xticks(x)
    ax.set_xticklabels([t.replace(' (', '\n(') for t in test_names], rotation=0, ha='center')
    ax.legend()
    ax.set_yscale('log')
    
    # 値を表示
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   f'{height:.1f}x', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('results/relative_performance.png', dpi=300, bbox_inches='tight')
    print("Chart saved to: results/relative_performance.png")
    plt.show()

def print_summary(data):
    """結果のサマリーを表示"""
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)
    print(f"Timestamp: {data['timestamp']}")
    print(f"Platform: {data['platform']['system']} {data['platform']['release']}")
    print(f"Python: {data['platform']['python_version']}")
    print("="*60)

def main():
    print("Loading benchmark results...")
    data = load_latest_results()
    
    if not data:
        print("Please run ./run_benchmark.py first to generate results")
        return
    
    print_summary(data)
    
    print("\nGenerating visualizations...")
    create_bar_chart(data)
    create_relative_performance_chart(data)
    
    print("\nVisualization complete!")

if __name__ == "__main__":
    main()