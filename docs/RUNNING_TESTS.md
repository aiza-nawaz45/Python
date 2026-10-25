# Running the Tests (Task 4)

All commands are run from the repository root with the virtual environment active.

## Groups (suites)

| Marker | What it contains | Test cases |
|---|---|---|
| `smoke` | 9 quick, important tests (run first) | 9 |
| `stack` | Stack class tests | 63 |
| `prime` | is_prime tests | 20 |
| `queue` | CircularQueue tests | 60 |
| `data_driven` | tests that read CSV files in `test_data/` | 31 |
| `regression` | every test | 174 |

Groups are registered in `pytest.ini` and applied with `pytestmark` at the top of each test file
(module groups) and with `@pytest.mark.smoke` on selected tests.

## Execution order (pytest-order)

| Order index | Group |
|---|---|
| 1 - 9 | the 9 smoke tests, one index each |
| 20 | stack tests |
| 30 | prime tests |
| 40 | queue tests |
| 50 | data-driven (CSV) tests |

Tests with a lower index run first. Tests with the same index keep the order of the file.

## Commands

```bash
python -m pytest -n 0 -v                          # all tests, one process, in group order
python -m pytest -n 0 --collect-only -q           # only show the execution order
python -m pytest -m smoke -n 0 -v                 # smoke suite (9)
python -m pytest -m stack -v                      # stack suite (63)
python -m pytest -m prime -v                      # prime suite (20)
python -m pytest -m queue -v                      # queue suite (60)
python -m pytest -m data_driven -v                # CSV-driven suite (31)
python -m pytest -m "regression and not data_driven" -q   # 143 tests
python -m pytest -n 2 --dist loadscope -v         # parallel, 2 workers
python -m pytest -n auto --dist loadscope -q      # parallel, one worker per CPU core
```

## Parallel execution (pytest-xdist)

- `-n 2` starts 2 worker processes, `-n auto` starts one per CPU core, `-n 0` disables parallel runs.
- `--dist loadscope` gives all tests of one module to the same worker.
- The execution order above is guaranteed only with `-n 0`. In a parallel run each worker orders
  its own tests, so the global order can differ.
- Parallel runs are safe here because every test creates its own Stack / CircularQueue and the
  CSV files are only read.

## Data-driven tests

`tests/test_aiza_csv_driven.py` reads `test_data/*.csv`. To add a test case, add a row to the CSV
file. The test cases are described in `docs/test_cases.xlsx`.
