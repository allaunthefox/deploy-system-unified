#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500004
# Script Type: Benchmark Aggregation
# Description: Runs benchmarks N times and calculates statistics
# Output: JSON and Markdown with Mean, Median, Min, Max, StdDev
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""benchmark_aggregator.py - Run benchmarks $N$ times and calculate statistics.

Calculates Mean, Median, Min, Max, and Standard Deviation.
Outputs results in JSON and Markdown.
"""

import argparse
import json
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def run_benchmark(command: List[str], cwd: Optional[Path] = None) -> Dict[str, Any]:
    """Runs a single iteration of the benchmark."""
    start_time = time.perf_counter()
    try:
        # Run the command and capture output
        result = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=False
        )
        end_time = time.perf_counter()
        
        # Try to parse the output as JSON if it looks like JSON
        output_json = None
        try:
            output_json = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass

        return {
            "duration": end_time - start_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "json_data": output_json
        }
    except Exception as e:
        return {
            "error": str(e),
            "duration": 0,
            "return_code": -1
        }


def calculate_stats(data: List[float]) -> Dict[str, float]:
    """Calculates statistical metrics for a list of data points."""
    if not data:
        return {}
    
    return {
        "count": len(data),
        "min": min(data),
        "max": max(data),
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "stdev": statistics.stdev(data) if len(data) > 1 else 0.0
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark Aggregator")
    parser.add_argument("command", help="Command to benchmark (as a single string)", nargs="+")
    parser.add_argument("--iterations", "-n", type=int, default=5, help="Number of iterations")
    parser.add_argument("--warmup", "-w", type=int, default=1, help="Number of warmup iterations")
    parser.add_argument("--output-dir", "-o", default="/var/lib/deploy-system/evidence/benchmark/baselines", help="Output directory")
    parser.add_argument("--name", help="Name for this benchmark run", default="benchmark")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_name = f"{args.name}_{timestamp}"
    
    print(f"[*] Starting benchmark aggregation for: {' '.join(args.command)}")
    print(f"[*] Warmup: {args.warmup} iterations")
    print(f"[*] Benchmark: {args.iterations} iterations")
    
    # Warmup
    for i in range(args.warmup):
        print(f"  [Warmup {i+1}/{args.warmup}] Running...", end="\r")
        run_benchmark(args.command)
    print("\n  [Warmup] Complete")
    
    # Actual Benchmark
    results = []
    durations = []
    
    for i in range(args.iterations):
        print(f"  [Run {i+1}/{args.iterations}] Running...", end="\r")
        res = run_benchmark(args.command)
        results.append(res)
        if res.get("return_code") == 0:
            durations.append(res["duration"])
    print("\n  [Runs] Complete")
    
    # Aggregate custom metrics if the script outputs JSON
    custom_metrics: Dict[str, List[float]] = {}
    for res in results:
        if res.get("json_data") and isinstance(res["json_data"], dict):
            for key, value in res["json_data"].items():
                if isinstance(value, (int, float)):
                    if key not in custom_metrics:
                        custom_metrics[key] = []
                    custom_metrics[key].append(float(value))

    stats_data = {
        "run_name": args.name,
        "timestamp": timestamp,
        "command": args.command,
        "iterations": args.iterations,
        "warmup": args.warmup,
        "execution_time_stats": calculate_stats(durations),
        "custom_metrics_stats": {k: calculate_stats(v) for k, v in custom_metrics.items()}
    }

    # Save JSON results
    json_file = output_dir / f"{run_name}.json"
    json_file.write_text(json.dumps(stats_data, indent=2))
    
    # Generate Markdown Summary
    md_file = output_dir / f"{run_name}.md"
    md_content = [
        f"# Benchmark results for: {args.name}",
        f"- **Timestamp**: {timestamp}",
        f"- **Command**: `{' '.join(args.command)}`",
        f"- **Iterations**: {args.iterations} (Warmup: {args.warmup})",
        "",
        "## Execution Time Statistics (seconds)",
        "| Metric | Value |",
        "| :--- | :--- |",
        f"| Mean | {stats_data['execution_time_stats'].get('mean', 0):.4f} |",
        f"| Median | {stats_data['execution_time_stats'].get('median', 0):.4f} |",
        f"| Min | {stats_data['execution_time_stats'].get('min', 0):.4f} |",
        f"| Max | {stats_data['execution_time_stats'].get('max', 0):.4f} |",
        f"| StdDev | {stats_data['execution_time_stats'].get('stdev', 0):.4f} |",
        ""
    ]
    
    if custom_metrics:
        md_content.append("## Custom Metric Statistics")
        for key, stats in stats_data["custom_metrics_stats"].items():
            md_content.extend([
                f"### {key}",
                "| Metric | Value |",
                "| :--- | :--- |",
                f"| Mean | {stats.get('mean', 0):.4f} |",
                f"| Median | {stats.get('median', 0):.4f} |",
                f"| Min | {stats.get('min', 0):.4f} |",
                f"| Max | {stats.get('max', 0):.4f} |",
                f"| StdDev | {stats.get('stdev', 0):.4f} |",
                ""
            ])

    md_file.write_text("\n".join(md_content))
    
    print(f"[*] Results saved to {output_dir}")
    print(f"[*] Summary: {md_file}")


if __name__ == "__main__":
    main()
