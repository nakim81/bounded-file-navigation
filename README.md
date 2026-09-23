# Bounded File Navigation (experimental)

[한국어 README (README.ko.md)](README.ko.md)

An agent skill and a dependency-free Python CLI for finding relevant files without returning a repository dump to the model. **This is a discovery aid, not a token-savings or correctness claim.** Search results are capped; source reading is not. The agent must expand and verify relevant evidence before answering or editing.

## Quick Installation & Agent Usage

### 1. Universal Agent Skills CLI (`skills.sh` / Claude Code, Codex, Cursor, etc.)

```sh
# Inspect available skills in this repo
npx skills add nakim81/bounded-file-navigation --list

# Install globally
npx skills add nakim81/bounded-file-navigation -g -y

# Or install for a specific agent
npx skills add nakim81/bounded-file-navigation -g --agent claude-code -y
```

### 2. Hermes Agent CLI

```sh
hermes skills install https://raw.githubusercontent.com/nakim81/bounded-file-navigation/main/SKILL.md --name bounded-file-navigation --yes
```

### 3. Direct Run via Python (Zero dependencies, Python 3.9+)

```sh
git clone https://github.com/nakim81/bounded-file-navigation.git
cd bounded-file-navigation
python3 scripts/nav.py /path/to/repo 'manifest'
python3 scripts/nav.py /path/to/repo 'parse_manifest' --mode lines
```


## Core Metrics & Verification Targets

Token savings are invalid if grounding accuracy drops. We evaluate navigation against four sharp metrics:

| Metric | Target | Failure Condition | How to Measure |
|---|---|---|---|
| **Grounding Accuracy** | **100%** | Wrong file, hallucinated line, obsolete version | Citing file and exact line ranges must match the ground truth |
| **Omission Rate** | **0%** | Missed evidence due to early termination or TRUNCATED cutoff | Agent claimed absence when evidence was present past the query limit |
| **Total Prompt Tokens** | **≥ 50% Reduction** | Neutral or higher token cost due to repeated search loops | Total cumulative prompt tokens across all turns until answer/edit delivery |
| **Tool Turn Count** | **2 – 4 turns** | > 6 turns of wandering queries | Number of tool invocations spent in navigation/reading |

See [BENCHMARK.md](BENCHMARK.md) for the complete A/B evaluation protocol and [benchmarks/log.md](benchmarks/log.md) for empirical test logs.

## Evaluation before claiming savings

For each real task, write the question and a source-grounded answer key *before* comparing methods. Compare an unrestricted existing workflow with the bounded workflow on the same repository snapshot; randomize order across tasks where practical. Track (1) correct source/answer and missed evidence, (2) model-visible **actual token count** including skill instructions and follow-up tool calls, (3) wall time and number of calls. Include failures: hidden files, large files, duplicate names, relevant hits past the cap, and long lines. If correctness or evidence coverage drops, token reduction is not a success. Do not publish private repository paths or content in examples without permission.

This is a small baseline for iterative testing, not a graph index, a RAG system, or a substitute for ripgrep. Issues describing missed evidence with a reproducible **public or synthetic** fixture are welcome.

## License

MIT. See [LICENSE](LICENSE).
