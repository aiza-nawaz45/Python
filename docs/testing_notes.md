# Test Design Notes - Assignment 3 (Unit Test Automation)

**Project:** TheAlgorithms/Python (fork: aiza-nawaz45/Python)
**Tester:** Aiza Nawaz (24L-6803)
**Framework:** pytest 9.1.1, Python 3.13

Run all tests of this document with:

```
python -m pytest tests/test_aiza_stack.py tests/test_aiza_prime_check.py -v
```

Techniques: **ECP** (equivalence class partitioning), **BVA** (boundary value analysis),
**DT** (decision table), **ST** (state transition), **EG** (error guessing).

---

## Module 1: `data_structures/stacks/stack.py` (class `Stack`)

The class stores items in a list, has a capacity `limit` (default 10) and raises
`StackOverflowError` (push on a full stack) or `StackUnderflowError` (pop/peek on an empty stack).

### 1.1 Input domain of the constructor `Stack(limit)`

| Partition | Example | Expected behaviour | Test |
|---|---|---|---|
| Default | `Stack()` | limit = 10 | `test_default_limit_is_ten` |
| Positive limit | `Stack(3)` | limit stored as 3 | `test_custom_limit_is_stored` |
| Zero limit (BVA) | `Stack(0)` | empty and full at the same time; first push overflows | `test_is_empty_true_for_zero_limit_stack`, `test_is_full_true_for_zero_limit_stack` |
| Negative limit (BVA/EG) | `Stack(-1)` | `is_full()` is False (size 0 != -1) | `test_is_full_false_for_negative_limit_stack` |

### 1.2 Boundaries of the stack size (relative to `limit` and 0)

| Boundary | Operation | Expected | Test |
|---|---|---|---|
| size = 0 | pop / peek | StackUnderflowError | `test_pop_on_empty_stack_raises_underflow`, `test_peek_on_empty_stack_raises_underflow` |
| size = 1 | pop / peek | returns the item; pop then makes it empty | `test_pop_after_last_item_removed_raises_underflow`, `test_peek_on_single_element_stack` |
| size = limit - 1 | push | accepted, stack becomes full | `test_push_into_last_free_slot_succeeds` |
| size = limit | push | StackOverflowError | `test_push_on_full_stack_raises_overflow` |

### 1.3 Equivalence classes for pushed data

Valid classes: integers, strings, `None`, lists. All are accepted because the stack is generic.
Test: `test_push_accepts_different_types`.

### 1.4 Decision table (stack state x operation)

| State | Operation | Outcome |
|---|---|---|
| Empty | pop | StackUnderflowError |
| Empty | peek | StackUnderflowError |
| Partial | push | item added |
| Full | push | StackOverflowError |

Test: `test_decision_table_stack_operations` (4 rows).

### 1.5 State transition

`Empty --push--> Partial --push--> Full --pop--> Partial --pop--> Empty`

At every state the tests check `str()`, `is_empty()` and `is_full()`.
Test: `test_state_transition_empty_partial_full_back_to_empty`.

### 1.6 Error guessing

- A failed push must not change the stack (`test_failed_push_does_not_change_stack`).
- `peek()` must not remove the item (`test_peek_does_not_remove_item`).
- Duplicate values are allowed (`test_push_allows_duplicate_values`).
- `"10" in stack` is False when the stack holds the integer 10.
- The two error classes derive from `BaseException`, not `Exception`.

### 1.7 Observations (possible design issues, not logged as bugs)

1. `StackOverflowError` and `StackUnderflowError` inherit from `BaseException`, so a normal
   `except Exception:` block will not catch them.
2. The constructor does not validate `limit`. With `Stack(-1)`, `push()` raises
   `StackOverflowError` but `is_full()` returns `False`, which is inconsistent.

### 1.8 Test count

| Group | Test cases |
|---|---|
| push | 10 |
| pop | 9 |
| peek | 6 |
| is_empty | 6 |
| is_full | 8 |
| size | 8 |
| `__contains__` | 6 |
| Class level (constructor, `__bool__`, LIFO, state transition, decision table) | 10 |
| **Total** | **63** |

---

## Module 2: `maths/prime_check.py` (function `is_prime`)

`is_prime(number)` accepts only integers `>= 0`, otherwise raises
`ValueError("is_prime() only accepts positive integers")`.

### 2.1 Equivalence classes

| Class | Examples | Expected | Test |
|---|---|---|---|
| Negative integers (invalid) | -1, -19 | ValueError | `test_negative_numbers_raise_value_error` |
| Non-integers (invalid) | 16.1, 5.0, "7", None | ValueError | `test_non_integer_types_raise_value_error` |
| 0 and 1 | 0, 1 | False | `test_is_prime_returns_expected_value` |
| Special-cased primes | 2, 3 | True | same |
| Even numbers > 2 | 4 | False | same |
| Multiples of 3 > 3 | 9 | False | same |
| Composite with smallest factor >= 5 | 25, 49 | False | same |
| Primes of the form 6k +/- 1 | 97, 7919 | True | same |

### 2.2 Boundary values

| Boundary | Values | Reason |
|---|---|---|
| Invalid / valid | -1 | 0 | last invalid and first valid value |
| Not prime / prime | 1 | 2 | smallest prime |
| Special-cased branch | 3 | 4 | end of `1 < n < 4`, first composite |
| Loop divisor `i` | 25 | 5 * 5, found with `n % i` |
| Loop divisor `i + 2` | 49 | 7 * 7, found with `n % (i + 2)` |

### 2.3 Error guessing

- `5.0` is mathematically a whole number but is rejected because it is a `float`.
- `True` and `False` (subclass of `int`) are treated as 1 and 0 and return `False`.
- The error message must explain the problem (`only accepts positive integers`).
- The return type must be `bool`.

### 2.4 Test count

| Group | Test cases |
|---|---|
| Function level: return values for valid input | 10 |
| Module level: validation and contract | 10 |
| **Total** | **20** |

---

## Module 3

To be added (class-based module from `data_structures`).
