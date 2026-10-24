"""Unit tests for data_structures/stacks/stack.py (class Stack).

Author : Aiza Nawaz
Design : see docs/testing_notes.md
Run    : python -m pytest tests/test_aiza_stack.py -v

Techniques used (tagged in the comments):
    ECP  = Equivalence Class Partitioning
    BVA  = Boundary Value Analysis
    DT   = Decision Table
    ST   = State Transition
    EG   = Error Guessing
"""

import pytest

from data_structures.stacks.stack import (
    Stack,
    StackOverflowError,
    StackUnderflowError,
)


def make_stack(items=(), limit=10):
    """Helper: create a Stack with `limit` and push `items` in order."""
    stack = Stack(limit)
    for item in items:
        stack.push(item)
    return stack


# ---------------------------------------------------------------------------
# Stack.push  (10 tests)
# ---------------------------------------------------------------------------
def test_push_adds_item_on_top():  # ECP: valid push on partial stack
    stack = make_stack()
    stack.push(10)
    stack.push(20)
    assert stack.peek() == 20
    assert stack.size() == 2


@pytest.mark.parametrize(  # ECP: classes of data types
    "value",
    [7, "text", None, [1, 2]],
    ids=["int", "str", "none", "list"],
)
def test_push_accepts_different_types(value):
    stack = make_stack()
    stack.push(value)
    assert stack.peek() == value
    assert stack.size() == 1


def test_push_on_full_stack_raises_overflow():  # BVA: size == limit
    stack = make_stack([1, 2], limit=2)
    with pytest.raises(StackOverflowError):
        stack.push(3)


def test_push_into_last_free_slot_succeeds():  # BVA: size == limit - 1
    stack = make_stack([1, 2], limit=3)
    stack.push(3)
    assert stack.is_full()
    assert stack.size() == 3


def test_failed_push_does_not_change_stack():  # EG: failure must not corrupt state
    stack = make_stack([1, 2], limit=2)
    with pytest.raises(StackOverflowError):
        stack.push(3)
    assert str(stack) == "[1, 2]"
    assert stack.size() == 2


def test_push_allows_duplicate_values():  # EG: duplicates
    stack = make_stack()
    stack.push(5)
    stack.push(5)
    assert stack.size() == 2


def test_overflow_error_is_not_a_regular_exception():  # EG: design quirk
    # StackOverflowError derives from BaseException, so "except Exception"
    # will NOT catch it.
    assert issubclass(StackOverflowError, BaseException)
    assert not issubclass(StackOverflowError, Exception)


# NOTE: the list above contains 7 test functions; with the 4 parametrized
# type cases the push group runs 10 test cases.


# ---------------------------------------------------------------------------
# Stack.pop  (9 tests)
# ---------------------------------------------------------------------------
def test_pop_returns_last_pushed_item():  # ECP: valid pop
    stack = make_stack([1, 2, 3])
    assert stack.pop() == 3


def test_pop_decreases_size_by_one():  # ECP
    stack = make_stack([1, 2, 3])
    stack.pop()
    assert stack.size() == 2


def test_pop_on_empty_stack_raises_underflow():  # BVA: size == 0
    with pytest.raises(StackUnderflowError):
        Stack().pop()


def test_pop_after_last_item_removed_raises_underflow():  # BVA: size 1 -> 0
    stack = make_stack([1])
    assert stack.pop() == 1
    with pytest.raises(StackUnderflowError):
        stack.pop()


@pytest.mark.parametrize(  # BVA/ECP: sizes 1, 2 and many
    "items",
    [[1], [1, 2], [1, 2, 3, 4]],
    ids=["one_item", "two_items", "four_items"],
)
def test_pop_returns_items_in_reverse_order(items):
    stack = make_stack(items)
    popped = [stack.pop() for _ in items]
    assert popped == list(reversed(items))


def test_push_works_again_after_pop_from_full_stack():  # ST: full -> partial
    stack = make_stack([1, 2], limit=2)
    stack.pop()
    stack.push(9)
    assert stack.peek() == 9


def test_underflow_error_is_not_a_regular_exception():  # EG: design quirk
    assert issubclass(StackUnderflowError, BaseException)
    assert not issubclass(StackUnderflowError, Exception)


# ---------------------------------------------------------------------------
# Stack.peek  (6 tests)
# ---------------------------------------------------------------------------
def test_peek_returns_top_item():  # ECP
    assert make_stack([1, 2, 3]).peek() == 3


def test_peek_does_not_remove_item():  # EG: peek must be read-only
    stack = make_stack([1, 2, 3])
    stack.peek()
    assert stack.size() == 3


def test_peek_on_empty_stack_raises_underflow():  # BVA: size == 0
    with pytest.raises(StackUnderflowError):
        Stack().peek()


def test_peek_after_pop_returns_previous_item():  # ST
    stack = make_stack([1, 2, 3])
    stack.pop()
    assert stack.peek() == 2


def test_peek_on_single_element_stack():  # BVA: size == 1
    assert make_stack([42]).peek() == 42


def test_peek_on_full_stack():  # BVA: size == limit
    stack = make_stack([1, 2], limit=2)
    assert stack.peek() == 2


# ---------------------------------------------------------------------------
# Stack.is_empty  (6 tests)
# ---------------------------------------------------------------------------
def test_is_empty_true_for_new_stack():  # ECP: empty
    assert Stack().is_empty() is True


def test_is_empty_false_after_push():  # BVA: size 0 -> 1
    assert make_stack([1]).is_empty() is False


def test_is_empty_true_after_push_and_pop():  # ST: partial -> empty
    stack = make_stack([1])
    stack.pop()
    assert stack.is_empty() is True


def test_is_empty_false_for_full_stack():  # ECP: full
    assert make_stack([1, 2], limit=2).is_empty() is False


def test_is_empty_true_for_zero_limit_stack():  # BVA: limit == 0
    assert Stack(0).is_empty() is True


def test_is_empty_still_true_after_failed_pop():  # EG
    stack = Stack()
    with pytest.raises(StackUnderflowError):
        stack.pop()
    assert stack.is_empty() is True


# ---------------------------------------------------------------------------
# Stack.is_full  (8 tests)
# ---------------------------------------------------------------------------
def test_is_full_false_for_new_default_stack():  # ECP
    assert Stack().is_full() is False


def test_is_full_false_for_empty_stack_with_limit_one():  # BVA: limit == 1
    assert Stack(1).is_full() is False


def test_is_full_true_for_limit_one_after_one_push():  # BVA
    assert make_stack([1], limit=1).is_full() is True


def test_is_full_false_one_below_limit():  # BVA: limit - 1
    assert make_stack([1, 2], limit=3).is_full() is False


def test_is_full_true_exactly_at_limit():  # BVA: == limit
    assert make_stack([1, 2, 3], limit=3).is_full() is True


def test_is_full_true_for_zero_limit_stack():  # BVA: limit == 0
    assert Stack(0).is_full() is True


def test_is_full_false_after_pop_from_full_stack():  # ST: full -> partial
    stack = make_stack([1, 2], limit=2)
    stack.pop()
    assert stack.is_full() is False


def test_is_full_false_for_negative_limit_stack():  # BVA/EG: limit == -1
    # size (0) never equals a negative limit, so is_full() is False even though
    # push() would raise StackOverflowError. See docs/testing_notes.md.
    assert Stack(-1).is_full() is False


# ---------------------------------------------------------------------------
# Stack.size  (8 tests)
# ---------------------------------------------------------------------------
def test_size_zero_for_new_stack():  # BVA
    assert Stack().size() == 0


@pytest.mark.parametrize("count", [1, 3, 5, 10])  # ECP + BVA (10 == default limit)
def test_size_equals_number_of_pushes(count):
    assert make_stack(range(count)).size() == count


def test_size_decreases_after_pop():  # ST
    stack = make_stack([1, 2, 3])
    stack.pop()
    assert stack.size() == 2


def test_size_unchanged_after_peek():  # EG
    stack = make_stack([1, 2, 3])
    stack.peek()
    assert stack.size() == 3


def test_size_unchanged_after_failed_push():  # EG
    stack = make_stack([1, 2], limit=2)
    with pytest.raises(StackOverflowError):
        stack.push(3)
    assert stack.size() == 2


# ---------------------------------------------------------------------------
# Stack.__contains__  (6 tests)
# ---------------------------------------------------------------------------
def test_contains_present_item():  # ECP: present
    assert 10 in make_stack([10, 20])


def test_contains_absent_item():  # ECP: absent
    assert 30 not in make_stack([10, 20])


def test_contains_on_empty_stack():  # BVA: size == 0
    assert 1 not in Stack()


def test_contains_false_after_item_is_popped():  # ST
    stack = make_stack([10, 20])
    stack.pop()
    assert 20 not in stack


def test_contains_is_type_sensitive_for_strings():  # EG: "10" is not 10
    assert "10" not in make_stack([10])


def test_contains_duplicate_remains_after_one_pop():  # EG
    stack = make_stack([5, 5])
    stack.pop()
    assert 5 in stack


# ---------------------------------------------------------------------------
# Class level: the Stack class as a whole  (10 tests)
# ---------------------------------------------------------------------------
def test_default_limit_is_ten():  # BVA: constructor default
    stack = Stack()
    assert stack.limit == 10
    for i in range(10):
        stack.push(i)
    with pytest.raises(StackOverflowError):
        stack.push(10)


def test_custom_limit_is_stored():  # ECP: constructor argument
    assert Stack(3).limit == 3


@pytest.mark.parametrize(  # ECP: __bool__ for empty / non-empty
    "items, expected",
    [([], False), ([1], True)],
    ids=["empty", "non_empty"],
)
def test_bool_of_stack(items, expected):
    assert bool(make_stack(items)) is expected


def test_lifo_full_cycle():  # ECP: Last-In-First-Out
    stack = make_stack([1, 2, 3, 4, 5])
    assert [stack.pop() for _ in range(5)] == [5, 4, 3, 2, 1]
    assert stack.is_empty()


def test_state_transition_empty_partial_full_back_to_empty():  # ST
    stack = Stack(2)
    assert str(stack) == "[]"
    assert stack.is_empty()

    stack.push("a")  # empty -> partial
    assert str(stack) == "['a']"
    assert not stack.is_empty() and not stack.is_full()

    stack.push("b")  # partial -> full
    assert str(stack) == "['a', 'b']"
    assert stack.is_full()

    assert stack.pop() == "b"  # full -> partial
    assert not stack.is_full()

    assert stack.pop() == "a"  # partial -> empty
    assert stack.is_empty()


@pytest.mark.parametrize(  # DT: stack state x operation -> outcome
    "state, operation, expected",
    [
        ("empty", "pop", StackUnderflowError),
        ("empty", "peek", StackUnderflowError),
        ("full", "push", StackOverflowError),
        ("partial", "push", None),
    ],
    ids=["empty-pop", "empty-peek", "full-push", "partial-push"],
)
def test_decision_table_stack_operations(state, operation, expected):
    items = {"empty": [], "partial": [1, 2], "full": [1, 2, 3]}[state]
    stack = make_stack(items, limit=3)
    action = getattr(stack, operation)
    args = (99,) if operation == "push" else ()

    if expected is None:
        action(*args)
        assert 99 in stack
    else:
        with pytest.raises(expected):
            action(*args)
