
# Fixed Harbor Task: dynamo/log-report

This repository contains a corrected version of the `dynamo/log-report` Terminal-Bench 2 (Harbor) task. The original task had several authoring defects across its format, environment, verifier, and instructions. This README documents what was broken, how it was fixed, and the evidence that the fix works.

## Task Summary

Parse an Apache-style access log into a small JSON summary report containing total request count, unique IP count, and the most frequently requested path.

## Defects Found

1. **`task.toml`** — `artifacts` was a string (`"/app/out.json"`) instead of a TOML array, and pointed to the wrong file. The actual output is `/app/report.json`.
2. **`environment/Dockerfile`** — base image was `python:latest` (unpinned, floating tag), which breaks reproducibility.
3. **`environment/Dockerfile`** — the reference solution (`solution_hint.py`) was leaked directly into the agent's image, letting any agent read the answer key instead of solving the task.
4. **`tests/test_outputs.py`** — the verifier only checked that the output file existed and was non-empty. It never validated any actual value, so a no-op or garbage-writing agent could pass.
5. **`tests/test.sh`** — wrote `reward.txt` to the wrong path (`/app/reward.txt` instead of `/logs/verifier/reward.txt`) and never generated `ctrf.json`.
6. **`instruction.md`** — vague prose with no output path, no schema, and no numbered success criteria, making it inconsistent with the verifier.

## Fixes Applied

- `task.toml`: `artifacts = ["/app/report.json"]`
- `environment/Dockerfile`: base image pinned by `@sha256` digest; `solution_hint.py` removed from build context entirely
- `tests/test_outputs.py`: independently recomputes expected `total_requests`, `unique_ips`, and `top_path` from `access.log` and asserts them against the report
- `tests/test.sh`: writes `reward.txt` and `ctrf.json` to `/logs/verifier/`, runs plain `pytest` with no verify-time installs
- `instruction.md`: rewritten with the exact output path and four numbered, unambiguous success criteria, matching the verifier 1:1

## Verification Evidence

### Oracle run (expected: reward 1)


```
<img width="2222" height="988" alt="image" src="https://github.com/user-attachments/assets/e38a5e6f-cbab-4c0a-be33-b33a5dc09116" />

### Oracle run (expected: reward 0)
<img width="2266" height="934" alt="image" src="https://github.com/user-attachments/assets/11c70dd7-5fa7-4fa3-a75a-f8ad82ad0b5a" />



<img width="2282" height="574" alt="image" src="https://github.com/user-attachments/assets/ce8ac203-07dc-4031-b067-f164fdd9622d" />

<img width="2334" height="1074" alt="image" src="https://github.com/user-attachments/assets/192b19fd-47f7-4e85-a49c-940020bb8e67" />
