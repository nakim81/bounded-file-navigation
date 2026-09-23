# Bounded File Navigation (experimental)

An agent skill and a dependency-free Python CLI for finding relevant files without returning a repository dump to the model. **This is a discovery aid, not a token-savings or correctness claim.** Search results are capped; source reading is not. The agent must expand and verify relevant evidence before answering or editing.

## Try it

Python 3.9+; no installation or network access required.

```sh
python3 scripts/nav.py /path/to/repo 'manifest'                  # matching text-file paths
python3 scripts/nav.py /path/to/repo 'parse_manifest' --mode lines
python3 scripts/nav.py /path/to/repo/src 'parse_manifest' --mode lines --limit 25
```

Use the `SKILL.md` in an agent's skills directory (or reference it from your project's instructions). Replace `/path/to/repo` with your own directory. The script only reads files, skips common build/dependency/cache and hidden directories, scans selected text extensions, and omits files larger than 1 MB from content search. A `TRUNCATED` result means the search did **not** examine the whole tree; narrow and retry. `NO MATCH` is not proof of absence. Results are not relevance-ranked.

## Evaluation before claiming savings

For each real task, write the question and a source-grounded answer key *before* comparing methods. Compare an unrestricted existing workflow with the bounded workflow on the same repository snapshot; randomize order across tasks where practical. Track (1) correct source/answer and missed evidence, (2) model-visible **actual token count** including skill instructions and follow-up tool calls, (3) wall time and number of calls. Include failures: hidden files, large files, duplicate names, relevant hits past the cap, and long lines. If correctness or evidence coverage drops, token reduction is not a success. Do not publish private repository paths or content in examples without permission.

This is a small baseline for iterative testing, not a graph index, a RAG system, or a substitute for ripgrep. Issues describing missed evidence with a reproducible **public or synthetic** fixture are welcome.

## License

MIT. See [LICENSE](LICENSE).
