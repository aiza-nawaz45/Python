"""Task 3: data-driven tests. Test data is read from external CSV files.

Author : Aiza Nawaz
Data   : test_data/prime_data.csv, stack_state_data.csv,
         stack_overflow_data.csv, queue_data.csv
Sheet  : docs/test_cases.xlsx (test case descriptions TC-CSV-01 .. TC-CSV-04)
Run    : python -m pytest tests/test_aiza_csv_driven.py -v

To add a test case, add a new row to the CSV file. No Python change is needed.
"""

import csv
from pathlib import Path

import pytest

from data_structures.queues.circular_queue import CircularQueue
from data_structures.stacks.stack import (
    Stack,
    StackOverflowError,
    StackUnderflowError,
)
from maths.prime_check import is_prime

# Groups and execution order (see pytest.ini and docs/RUNNING_TESTS.md)
pytestmark = [pytest.mark.regression, pytest.mark.data_driven, pytest.mark.order(50)]


DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"


def read_csv(file_name):
    """Return the rows of a CSV file in test_data/ as a list of dictionaries."""
    with open(DATA_DIR / file_name, newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def split_items(text):
    """Turn "1 2 3" into ["1", "2", "3"]; an empty cell gives []."""
    return text.split()


# ---------------------------------------------------------------------------
# TC-CSV-01: is_prime  (test_data/prime_data.csv)
# ---------------------------------------------------------------------------
def prime_rows():
    return [
        pytest.param(int(row["number"]), row["expected"], id=row["tc_id"])
        for row in read_csv("prime_data.csv")
    ]


@pytest.mark.parametrize("number, expected", prime_rows())
def test_is_prime_from_csv(number, expected):
    if expected == "ValueError":
        with pytest.raises(ValueError):
            is_prime(number)
    else:
        assert is_prime(number) is (expected == "True")


# ---------------------------------------------------------------------------
# TC-CSV-02: Stack state after pushes  (test_data/stack_state_data.csv)
# ---------------------------------------------------------------------------
def stack_state_rows():
    return [
        pytest.param(
            int(row["limit"]),
            [int(item) for item in split_items(row["items"])],
            int(row["expected_size"]),
            row["expected_top"],
            row["expected_full"] == "True",
            id=row["tc_id"],
        )
        for row in read_csv("stack_state_data.csv")
    ]


@pytest.mark.parametrize(
    "limit, items, expected_size, expected_top, expected_full", stack_state_rows()
)
def test_stack_state_from_csv(limit, items, expected_size, expected_top, expected_full):
    stack = Stack(limit)
    for item in items:
        stack.push(item)

    assert stack.size() == expected_size
    assert stack.is_full() is expected_full

    if expected_top == "UNDERFLOW":
        with pytest.raises(StackUnderflowError):
            stack.peek()
    else:
        assert stack.peek() == int(expected_top)


# ---------------------------------------------------------------------------
# TC-CSV-03: Stack overflow rule  (test_data/stack_overflow_data.csv)
# ---------------------------------------------------------------------------
def stack_overflow_rows():
    return [
        pytest.param(
            int(row["limit"]),
            [int(item) for item in split_items(row["items"])],
            int(row["extra_item"]),
            row["expected"],
            id=row["tc_id"],
        )
        for row in read_csv("stack_overflow_data.csv")
    ]


@pytest.mark.parametrize("limit, items, extra_item, expected", stack_overflow_rows())
def test_stack_overflow_rule_from_csv(limit, items, extra_item, expected):
    stack = Stack(limit)
    for item in items:
        stack.push(item)

    if expected == "StackOverflowError":
        with pytest.raises(StackOverflowError):
            stack.push(extra_item)
    else:
        stack.push(extra_item)
        assert stack.peek() == extra_item
        assert stack.size() == len(items) + 1


# ---------------------------------------------------------------------------
# TC-CSV-04: CircularQueue enqueue/dequeue scenarios  (test_data/queue_data.csv)
# ---------------------------------------------------------------------------
def queue_rows():
    return [
        pytest.param(
            int(row["capacity"]),
            split_items(row["items"]),
            int(row["dequeues"]),
            split_items(row["later_items"]),
            int(row["expected_len"]),
            row["expected_first"],
            id=row["tc_id"],
        )
        for row in read_csv("queue_data.csv")
    ]


@pytest.mark.parametrize(
    "capacity, items, dequeues, later_items, expected_len, expected_first",
    queue_rows(),
)
def test_circular_queue_scenario_from_csv(
    capacity, items, dequeues, later_items, expected_len, expected_first
):
    queue = CircularQueue(capacity)
    for item in items:
        queue.enqueue(item)
    for _ in range(dequeues):
        queue.dequeue()
    for item in later_items:
        queue.enqueue(item)

    assert len(queue) == expected_len
    # first() returns the boolean False for an empty queue.
    assert queue.first() == (False if expected_first == "False" else expected_first)
