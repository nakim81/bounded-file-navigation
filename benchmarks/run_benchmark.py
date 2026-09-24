#!/usr/bin/env python3
"""
Automated Local 0-Token Benchmark Runner for Bounded File Navigation.
Evaluates Method A (Unbounded baseline: raw recursive grep) vs.
Method B (Bounded navigation: scripts/nav.py with rule-based refinement on TRUNCATED).
Zero external dependencies, zero LLM API costs.
"""

import os
import sys
import subprocess
import time
from typing import Dict, Any, List

TARGET_REPO = "/tmp/fastapi-bench/fastapi"

BENCHMARK_TASKS = [
    {
        "id": "T01",
        "name": "APIRouter class definition",
        "initial_query": "APIRouter",
        "refined_query": "class APIRouter",
        "mode": "lines",
        "target_file": "routing.py",
        "target_line": 2255,
        "category": "cold_discovery"
    },
    {
        "id": "T02",
        "name": "Depends dependency injection class",
        "initial_query": "class Depends",
        "refined_query": None,
        "mode": "lines",
        "target_file": "params.py",
        "target_line": 746,
        "category": "cold_discovery"
    },
    {
        "id": "T03",
        "name": "HTTPException class definition",
        "initial_query": "class HTTPException",
        "refined_query": None,
        "mode": "lines",
        "target_file": "exceptions.py",
        "target_line": 17,
        "category": "cold_discovery"
    },
    {
        "id": "T04",
        "name": "FastAPI main application class",
        "initial_query": "class FastAPI",
        "refined_query": None,
        "mode": "lines",
        "target_file": "applications.py",
        "target_line": 42,
        "category": "warm_rediscovery"
    },
    {
        "id": "T05",
        "name": "OAuth2PasswordBearer security scheme",
        "initial_query": "OAuth2PasswordBearer",
        "refined_query": "class OAuth2PasswordBearer",
        "mode": "lines",
        "target_file": "security/oauth2.py",
        "target_line": 433,
        "category": "cold_discovery"
    },
    {
        "id": "T06",
        "name": "UploadFile datastructure definition",
        "initial_query": "class UploadFile",
        "refined_query": None,
        "mode": "lines",
        "target_file": "datastructures.py",
        "target_line": 21,
        "category": "cold_discovery"
    },
    {
        "id": "T07",
        "name": "solve_dependencies execution helper",
        "initial_query": "solve_dependencies",
        "refined_query": "def solve_dependencies",
        "mode": "lines",
        "target_file": "dependencies/utils.py",
        "target_line": 586,
        "category": "cold_discovery"
    },
    {
        "id": "T08",
        "name": "APIKeyBase security base class",
        "initial_query": "class APIKeyBase",
        "refined_query": None,
        "mode": "lines",
        "target_file": "security/api_key.py",
        "target_line": 11,
        "category": "cold_discovery"
    },
    {
        "id": "T09",
        "name": "AsyncExitStackMiddleware middleware",
        "initial_query": "AsyncExitStackMiddleware",
        "refined_query": "class AsyncExitStackMiddleware",
        "mode": "lines",
        "target_file": "middleware/asyncexitstack.py",
        "target_line": 8,
        "category": "cold_discovery"
    },
    {
        "id": "T10",
        "name": "get_openapi schema generation function",
        "initial_query": "def get_openapi",
        "refined_query": None,
        "mode": "lines",
        "target_file": "openapi/utils.py",
        "target_line": 585,
        "category": "warm_rediscovery"
    }
]

def run_method_a_unbounded(task: Dict[str, Any], root: str) -> Dict[str, Any]:
    """Simulates Method A: standard recursive unbounded grep."""
    query = task["initial_query"]
    cmd = ["grep", "-rn", query, root]
    start = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.perf_counter() - start
    
    output = proc.stdout
    target_match = False
    for line in output.splitlines():
        if task["target_file"] in line and f":{task['target_line']}:" in line:
            target_match = True
            break
            
    chars = len(output)
    est_tokens = max(1, round(chars / 3.8))
    
    return {
        "turns": 1,
        "chars": chars,
        "est_tokens": est_tokens,
        "hit": target_match,
        "duration_ms": round(duration * 1000, 2)
    }

def run_method_b_bounded(task: Dict[str, Any], root: str, script_path: str) -> Dict[str, Any]:
    """
    Simulates Method B: bounded navigation tool with rule-based refinement.
    Turn 1: bounded search.
    If TRUNCATED and target not found, Turn 2: refined query (or narrowed path).
    """
    total_chars = 0
    turns = 0
    target_match = False
    start = time.perf_counter()
    
    # Turn 1
    cmd1 = [sys.executable, script_path, root, task["initial_query"], "--mode", task["mode"], "--limit", "12"]
    proc1 = subprocess.run(cmd1, capture_output=True, text=True)
    turns += 1
    total_chars += len(proc1.stdout)
    
    for line in proc1.stdout.splitlines():
        if task["target_file"] in line and f":{task['target_line']}:" in line:
            target_match = True
            break
            
    # Check if truncated and needs refinement
    if not target_match and "TRUNCATED:" in proc1.stdout and task["refined_query"]:
        # Turn 2: Refined query
        cmd2 = [sys.executable, script_path, root, task["refined_query"], "--mode", task["mode"], "--limit", "12"]
        proc2 = subprocess.run(cmd2, capture_output=True, text=True)
        turns += 1
        total_chars += len(proc2.stdout)
        
        for line in proc2.stdout.splitlines():
            if task["target_file"] in line and f":{task['target_line']}:" in line:
                target_match = True
                break
                
    duration = time.perf_counter() - start
    est_tokens = max(1, round(total_chars / 3.8))
    
    return {
        "turns": turns,
        "chars": total_chars,
        "est_tokens": est_tokens,
        "hit": target_match,
        "duration_ms": round(duration * 1000, 2)
    }

def main():
    if not os.path.exists(TARGET_REPO):
        print(f"Error: Target repo not found at {TARGET_REPO}")
        print("Run: git clone --depth 1 https://github.com/fastapi/fastapi.git /tmp/fastapi-bench")
        sys.exit(1)
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    nav_script = os.path.join(project_root, "scripts", "nav.py")
    
    print("=" * 80)
    print(f"Running Bounded File Navigation Benchmark on FastAPI ({len(BENCHMARK_TASKS)} tasks)")
    print("=" * 80)
    
    total_a_tokens = 0
    total_b_tokens = 0
    a_hits = 0
    b_hits = 0
    total_b_turns = 0
    
    results = []
    
    for task in BENCHMARK_TASKS:
        res_a = run_method_a_unbounded(task, TARGET_REPO)
        res_b = run_method_b_bounded(task, TARGET_REPO, nav_script)
        
        total_a_tokens += res_a["est_tokens"]
        total_b_tokens += res_b["est_tokens"]
        if res_a["hit"]:
            a_hits += 1
        if res_b["hit"]:
            b_hits += 1
        total_b_turns += res_b["turns"]
        
        savings = (1 - (res_b["est_tokens"] / res_a["est_tokens"])) * 100 if res_a["est_tokens"] > 0 else 0
        
        results.append({
            "id": task["id"],
            "name": task["name"],
            "a_tokens": res_a["est_tokens"],
            "b_tokens": res_b["est_tokens"],
            "savings": savings,
            "b_turns": res_b["turns"],
            "a_hit": res_a["hit"],
            "b_hit": res_b["hit"]
        })
        
        print(f"[{task['id']}] {task['name'][:32]:32} | "
              f"Base: {res_a['est_tokens']:4} tok | Bounded: {res_b['est_tokens']:4} tok "
              f"({savings:+6.1f}%) | Turns: {res_b['turns']} | Hit: {'✓' if res_b['hit'] else '✗'}")

    overall_savings = (1 - (total_b_tokens / total_a_tokens)) * 100 if total_a_tokens > 0 else 0
    avg_turns = total_b_turns / len(BENCHMARK_TASKS)
    
    print("=" * 80)
    print("BENCHMARK SUMMARY RESULTS:")
    print(f"- Total Tasks:               {len(BENCHMARK_TASKS)}")
    print(f"- Grounding Accuracy:        Method A: {a_hits}/{len(BENCHMARK_TASKS)} ({a_hits/len(BENCHMARK_TASKS)*100:.0f}%) | "
          f"Method B: {b_hits}/{len(BENCHMARK_TASKS)} ({b_hits/len(BENCHMARK_TASKS)*100:.0f}%)")
    print(f"- Total Prompt Tokens:       Method A: {total_a_tokens:,} tok | Method B: {total_b_tokens:,} tok")
    print(f"- Net Token Reduction:       {overall_savings:.1f}%")
    print(f"- Average Tool Turns:        {avg_turns:.1f} turns / task")
    print("=" * 80)

if __name__ == "__main__":
    main()
