# Bounded File Navigation: Benchmark Protocol & Evaluation

This document defines the sharp objective, measurement metrics, and evaluation workflow for the `bounded-file-navigation` skill.

---

## 1. Core Objective

> **Enable agents to locate 100% of required ground-truth evidence across large multi-project repositories using strict bounded queries and localized line-range reading, eliminating whole-file dumping into context while maintaining zero omission.**

---

## 2. Metrics & Targets

| Metric | Target | Failure Condition | How to Measure |
|---|---|---|---|
| **Grounding Accuracy** | **100%** | Wrong file, hallucinated line, obsolete version | Citing file and exact line ranges must match the ground truth |
| **Omission Rate** | **0%** | Missed evidence due to early termination or TRUNCATED cutoff | Agent claimed absence when evidence was present past the query limit |
| **Total Prompt Tokens** | **≥ 50% Reduction** | Neutral or higher token cost due to repeated search loops | Total cumulative prompt tokens across all turns until answer/edit delivery |
| **Tool Turn Count** | **2 – 4 turns** | > 6 turns of wandering queries | Number of tool invocations spent in navigation/reading |

---

## 3. Evaluation Protocol (A/B Comparison)

For every evaluated scenario:
1. **Define Task & Ground Truth:** Write down the question, target file, and exact line numbers before running.
2. **Run Method A (Unbounded Baseline):** Run unrestricted `search_files` + whole-file `read_file`. Record cumulative prompt tokens, tool turns, and final answer.
3. **Run Method B (Bounded Navigation):** Run `python3 scripts/nav.py <root> <query>` → inspect hits → bounded line reads. Record cumulative prompt tokens, tool turns, and final answer.
4. **Log Results:** Append the verified run row to `benchmarks/log.md`.
