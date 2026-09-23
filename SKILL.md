---
name: bounded-file-navigation
description: "Use when finding project files without flooding context."
version: 0.1.0
author: Noah Kim (nakim81), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [search, files, context, coding]
    related_skills: []
---

# Bounded file navigation

Locate evidence while keeping tool output small. The output cap is a *discovery budget*, never a cap on evidence needed to answer. This skill does not index content or replace source inspection.

## When to use

Use for multi-file project exploration, repeated file lookup, or large repositories. For an already-known file, open it directly.

## Procedure

1. Start at the known project root. Read its local agent instructions; identify the smallest likely subtree and search terms. Do not search your whole home directory by default.
2. Use `terminal(command="python3 scripts/nav.py ROOT QUERY --mode paths")` (from this repository), or an equivalent bounded `search_files` call, to locate candidates. The script prints up to 12 paths by default; it skips common dependency/build/cache directories. Search terms are literal and case-insensitive.
3. If the answer requires content, use `--mode lines` for short matching excerpts. A truncated result means **not exhaustive**. Narrow the subtree or vary the query; use `--limit` (maximum 50) only when needed. `--mode lines` can omit long lines and large files. A zero-hit result is not proof of absence.
4. Open the relevant source with `read_file` at the cited path and line range. Expand beyond a snippet to cover definitions, adjacent conditions, references, and counterexamples. For a correctness or safety decision, inspect all relevant branches even if that exceeds the discovery budget.
5. Before editing or claiming absence, check current file state and repository status. If the query could have missed generated/ignored/hidden files, use a targeted direct check or an appropriate project manifest. Report uncertainty when coverage is incomplete.

## Pitfalls

- Filesystem walking may be slower than `rg` on large repositories; this script is a dependency-free baseline, not a performance claim.
- Results use sorted directory order, not relevance ranking. The first 12 hits can hide the right file. Re-query and narrow before trusting results.
- Only ordinary text extensions are searched; skipped directories are not evidence of absence.
- Do not send private paths or project content to a public benchmark or issue report without permission.

## Verification

For each navigation task, record whether the correct source and answer were found; compare tool-output tokens, calls, and time against an unrestricted baseline. Savings count only when answer accuracy and evidence coverage hold. See `README.md` for the evaluation protocol.
