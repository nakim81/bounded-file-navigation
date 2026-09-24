# Benchmark Logs

Record A/B navigation evaluations here.

## Run 1: 2026-09-24 (FastAPI Repository, 10 Ground-Truth Tasks)

- **Target Corpus:** `fastapi/fastapi` (48 Python files, core framework codebase)
- **Method A (Baseline):** Standard recursive unbounded `grep -rn`
- **Method B (Bounded Navigation):** `scripts/nav.py` (limit=12, rule-based narrowing on `TRUNCATED`)
- **Evaluation Mechanism:** Automated local runner (`benchmarks/run_benchmark.py`), 0 API tokens spent

### Summary
| Metric | Method A (Baseline) | Method B (Bounded Navigation) | Outcome |
|---|---|---|---|
| **Grounding Accuracy** | 10 / 10 (100%) | 10 / 10 (100%) | **Pass (100% matched)** |
| **Omission Rate** | 0% | 0% | **Pass (Zero missing targets)** |
| **Total Prompt Tokens** | 2,043 tokens | 748 tokens | **-63.4% Reduction** |
| **Average Tool Turns** | 1.0 turns | 1.1 turns | **Pass (Well within 2–4 budget)** |

### Task Details
| Task ID | Task Description | Target File:Line | Method A Tokens | Method B Tokens | Token Savings | Method B Turns | Accuracy |
|---|---|---|---|---|---|---|---|
| T01 | APIRouter class definition | `routing.py:2255` | 1,427 | 338 | +76.3% | 2 (Refined on Truncated) | Pass (100%) |
| T02 | Depends dependency injection class | `params.py:746` | 15 | 8 | +46.7% | 1 | Pass (100%) |
| T03 | HTTPException class definition | `exceptions.py:17` | 23 | 17 | +26.1% | 1 | Pass (100%) |
| T04 | FastAPI main application class | `applications.py:42` | 64 | 43 | +32.8% | 1 | Pass (100%) |
| T05 | OAuth2PasswordBearer security scheme | `security/oauth2.py:433` | 53 | 39 | +26.4% | 1 | Pass (100%) |
| T06 | UploadFile datastructure definition | `datastructures.py:21` | 23 | 16 | +30.4% | 1 | Pass (100%) |
| T07 | solve_dependencies execution helper | `dependencies/utils.py:586` | 187 | 115 | +38.5% | 1 | Pass (100%) |
| T08 | APIKeyBase security base class | `security/api_key.py:11` | 22 | 15 | +31.8% | 1 | Pass (100%) |
| T09 | AsyncExitStackMiddleware middleware | `middleware/asyncexitstack.py:8` | 148 | 104 | +29.7% | 1 | Pass (100%) |
| T10 | get_openapi schema generation function | `openapi/utils.py:585` | 81 | 53 | +34.6% | 1 | Pass (100%) |
