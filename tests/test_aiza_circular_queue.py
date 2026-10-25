"""Unit tests for data_structures/queues/circular_queue.py (class CircularQueue).

Author : Aiza Nawaz
Design : see docs/testing_notes.md
Run    : python -m pytest tests/test_aiza_circular_queue.py -v

Techniques used (tagged in the comments):
    ECP  = Equivalence Class Partitioning
    BVA  = Boundary Value Analysis
    DT   = Decision Table
    ST   = State Transition
    EG   = Error Guessing
"""

import pytest

from data_structures.queues.circular_queue import CircularQueue


# Groups and execution order (see pytest.ini and docs/RUNNING_TESTS.md)
pytestmark = [pytest.mark.regression, pytest.mark.queue, pytest.mark.order(40)]


def make_queue(items=(), capacity=5):
    """Helper: create a CircularQueue with `capacity` and enqueue `items` in order."""
    queue = CircularQueue(capacity)
    for item in items:
        queue.enqueue(item)
    return queue


# ---------------------------------------------------------------------------
# __init__  (8 test cases)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.order(7)
def test_new_queue_is_empty():  # ECP: valid capacity
    queue = CircularQueue(5)
    assert len(queue) == 0
    assert queue.is_empty()


def test_init_stores_capacity():  # ECP
    assert CircularQueue(5).n == 5


@pytest.mark.parametrize("capacity", [1, 5, 10], ids=["cap_1", "cap_5", "cap_10"])
def test_init_array_has_capacity_slots_filled_with_none(capacity):  # BVA: smallest valid
    assert CircularQueue(capacity).array == [None] * capacity


def test_init_front_rear_and_size_start_at_zero():  # ECP
    queue = CircularQueue(5)
    assert (queue.front, queue.rear, queue.size) == (0, 0, 0)


def test_init_with_zero_capacity_creates_empty_array():  # BVA: capacity 0
    assert CircularQueue(0).array == []


def test_init_with_negative_capacity_creates_empty_array():  # BVA/EG: capacity -1
    # No validation: [None] * -1 is an empty list, so no error is raised.
    assert CircularQueue(-1).array == []


# ---------------------------------------------------------------------------
# __len__  (8 test cases)
# ---------------------------------------------------------------------------
def test_len_of_new_queue_is_zero():  # BVA: size 0
    assert len(CircularQueue(5)) == 0


@pytest.mark.parametrize("count", [1, 3, 5], ids=["one", "three", "five_full"])
def test_len_equals_number_of_enqueues(count):  # ECP + BVA (5 == capacity)
    assert len(make_queue(range(count))) == count


def test_len_decreases_after_dequeue():  # ST
    queue = make_queue([1, 2, 3])
    queue.dequeue()
    assert len(queue) == 2


def test_len_unchanged_after_failed_enqueue():  # EG
    queue = make_queue([1, 2], capacity=2)
    with pytest.raises(Exception, match="QUEUE IS FULL"):
        queue.enqueue(3)
    assert len(queue) == 2


def test_len_unchanged_after_failed_dequeue():  # EG
    queue = CircularQueue(3)
    with pytest.raises(Exception, match="UNDERFLOW"):
        queue.dequeue()
    assert len(queue) == 0


def test_len_is_consistent_over_many_wrap_arounds():  # EG
    queue = CircularQueue(3)
    for i in range(10):
        queue.enqueue(i)
        assert len(queue) == 1
        queue.dequeue()
        assert len(queue) == 0


# ---------------------------------------------------------------------------
# is_empty  (7 test cases)
# ---------------------------------------------------------------------------
def test_is_empty_true_for_new_queue():  # ECP: empty
    assert CircularQueue(5).is_empty() is True


def test_is_empty_false_after_one_enqueue():  # BVA: size 0 -> 1
    assert make_queue(["A"]).is_empty() is False


def test_is_empty_true_after_enqueue_and_dequeue():  # ST: partial -> empty
    queue = make_queue(["A"])
    queue.dequeue()
    assert queue.is_empty() is True


def test_is_empty_false_for_full_queue():  # ECP: full
    assert make_queue([1, 2], capacity=2).is_empty() is False


def test_is_empty_true_for_zero_capacity_queue():  # BVA: capacity 0
    assert CircularQueue(0).is_empty() is True


def test_is_empty_still_true_after_failed_dequeue():  # EG
    queue = CircularQueue(3)
    with pytest.raises(Exception, match="UNDERFLOW"):
        queue.dequeue()
    assert queue.is_empty() is True


def test_is_empty_false_when_partially_dequeued():  # ECP: partial
    queue = make_queue(["A", "B"])
    queue.dequeue()
    assert queue.is_empty() is False


# ---------------------------------------------------------------------------
# first  (8 test cases)
# ---------------------------------------------------------------------------
def test_first_returns_false_for_empty_queue():  # BVA: size 0 (current behaviour)
    assert CircularQueue(5).first() is False


def test_first_returns_item_after_one_enqueue():  # BVA: size 1
    assert make_queue(["A"]).first() == "A"


def test_first_returns_oldest_item_not_newest():  # ECP: FIFO
    assert make_queue(["A", "B", "C"]).first() == "A"


def test_first_does_not_remove_item():  # EG: read-only
    queue = make_queue(["A", "B"])
    queue.first()
    assert len(queue) == 2


def test_first_returns_next_item_after_dequeue():  # ST
    queue = make_queue(["A", "B"])
    queue.dequeue()
    assert queue.first() == "B"


def test_first_is_correct_after_wrap_around():  # EG: front index moves
    queue = make_queue(["A", "B", "C"], capacity=3)
    queue.dequeue()
    queue.enqueue("D")
    assert queue.first() == "B"


def test_first_cannot_tell_stored_false_from_empty_queue():  # EG: design quirk
    # first() returns False for an empty queue, so a queue whose first item is
    # the value False gives the same answer.
    queue = make_queue([False])
    assert queue.first() is False
    assert not queue.is_empty()


def test_first_returns_false_again_after_queue_is_emptied():  # ST
    queue = make_queue(["A"])
    queue.dequeue()
    assert queue.first() is False


# ---------------------------------------------------------------------------
# enqueue  (10 test cases)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.order(8)
def test_enqueue_returns_the_same_queue_for_chaining():  # ECP
    queue = CircularQueue(5)
    assert queue.enqueue("A") is queue
    queue.enqueue("B").enqueue("C")
    assert len(queue) == 3


def test_enqueue_stores_items_in_order():  # ECP
    queue = make_queue(["A", "B"])
    assert queue.array == ["A", "B", None, None, None]


@pytest.mark.parametrize(  # ECP: classes of data types
    "value",
    [7, "text", None],
    ids=["int", "str", "none"],
)
def test_enqueue_accepts_different_types(value):
    queue = make_queue([value])
    assert len(queue) == 1
    assert queue.first() == value


def test_enqueue_on_full_queue_raises_exception():  # BVA: size == capacity
    queue = make_queue([1, 2], capacity=2)
    with pytest.raises(Exception, match="QUEUE IS FULL"):
        queue.enqueue(3)


def test_enqueue_into_last_free_slot_succeeds():  # BVA: size == capacity - 1
    queue = make_queue([1, 2], capacity=3)
    queue.enqueue(3)
    assert len(queue) == 3


def test_failed_enqueue_does_not_change_array():  # EG
    queue = make_queue(["A", "B"], capacity=2)
    with pytest.raises(Exception, match="QUEUE IS FULL"):
        queue.enqueue("C")
    assert queue.array == ["A", "B"]


def test_enqueue_reuses_freed_slot_after_wrap_around():  # ST/EG
    queue = make_queue(["A", "B", "C"], capacity=3)
    queue.dequeue()
    queue.enqueue("D")
    assert queue.array == ["D", "B", "C"]


def test_enqueue_on_zero_capacity_queue_raises_exception():  # BVA: capacity 0
    with pytest.raises(Exception, match="QUEUE IS FULL"):
        CircularQueue(0).enqueue("A")


# ---------------------------------------------------------------------------
# dequeue  (10 test cases)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.order(9)
def test_dequeue_returns_oldest_item():  # ECP: FIFO
    queue = make_queue(["A", "B"])
    assert queue.dequeue() == "A"


def test_dequeue_clears_the_freed_slot():  # EG
    queue = make_queue(["A"])
    queue.dequeue()
    assert queue.array == [None] * 5


def test_dequeue_decreases_size_by_one():  # ECP
    queue = make_queue(["A", "B", "C"])
    queue.dequeue()
    assert queue.size == 2


def test_dequeue_on_empty_queue_raises_exception():  # BVA: size 0
    with pytest.raises(Exception, match="UNDERFLOW"):
        CircularQueue(5).dequeue()


def test_dequeue_after_last_item_removed_raises_exception():  # BVA: size 1 -> 0
    queue = make_queue(["A"])
    assert queue.dequeue() == "A"
    with pytest.raises(Exception, match="UNDERFLOW"):
        queue.dequeue()


@pytest.mark.parametrize(  # BVA/ECP: sizes 1, 2 and 4
    "items",
    [["A"], ["A", "B"], ["A", "B", "C", "D"]],
    ids=["one_item", "two_items", "four_items"],
)
def test_dequeue_returns_items_in_insertion_order(items):
    queue = make_queue(items)
    assert [queue.dequeue() for _ in items] == items


def test_dequeue_order_is_correct_after_wrap_around():  # EG
    queue = make_queue(["A", "B", "C"], capacity=3)
    assert queue.dequeue() == "A"
    queue.enqueue("D")
    assert [queue.dequeue() for _ in range(3)] == ["B", "C", "D"]


def test_failed_dequeue_does_not_change_state():  # EG
    queue = CircularQueue(3)
    with pytest.raises(Exception, match="UNDERFLOW"):
        queue.dequeue()
    assert (queue.front, queue.rear, queue.size) == (0, 0, 0)


# ---------------------------------------------------------------------------
# Class level: the CircularQueue class as a whole  (9 test cases)
# ---------------------------------------------------------------------------
def test_fifo_full_cycle():  # ECP: First-In-First-Out
    queue = make_queue(["A", "B", "C", "D", "E"])
    assert [queue.dequeue() for _ in range(5)] == ["A", "B", "C", "D", "E"]
    assert queue.is_empty()


def test_state_transition_empty_partial_full_back_to_empty():  # ST
    queue = CircularQueue(2)
    assert queue.is_empty()

    queue.enqueue("a")  # empty -> partial
    assert len(queue) == 1
    assert queue.first() == "a"

    queue.enqueue("b")  # partial -> full
    assert len(queue) == 2
    with pytest.raises(Exception, match="QUEUE IS FULL"):
        queue.enqueue("c")

    assert queue.dequeue() == "a"  # full -> partial
    assert len(queue) == 1

    assert queue.dequeue() == "b"  # partial -> empty
    assert queue.is_empty()


@pytest.mark.parametrize(  # DT: queue state x operation -> outcome
    "state, operation, message",
    [
        ("empty", "dequeue", "UNDERFLOW"),
        ("full", "enqueue", "QUEUE IS FULL"),
        ("partial", "enqueue", None),
        ("partial", "dequeue", None),
    ],
    ids=["empty-dequeue", "full-enqueue", "partial-enqueue", "partial-dequeue"],
)
def test_decision_table_queue_operations(state, operation, message):
    items = {"empty": [], "partial": [1, 2], "full": [1, 2, 3]}[state]
    queue = make_queue(items, capacity=3)
    action = getattr(queue, operation)
    args = (99,) if operation == "enqueue" else ()

    if message is None:
        action(*args)
    else:
        with pytest.raises(Exception, match=message):
            action(*args)


def test_indices_wrap_around_after_many_cycles():  # EG: modulo arithmetic
    queue = CircularQueue(3)
    for i in range(10):
        queue.enqueue(i)
        queue.dequeue()
    assert queue.size == 0
    assert queue.front == queue.rear == 1  # 10 operations modulo 3


def test_queue_with_capacity_one_works_repeatedly():  # BVA: capacity 1
    queue = CircularQueue(1)
    queue.enqueue("A")
    with pytest.raises(Exception, match="QUEUE IS FULL"):
        queue.enqueue("B")
    assert queue.dequeue() == "A"
    queue.enqueue("B")
    assert queue.first() == "B"


def test_errors_are_plain_exception_objects():  # EG: design quirk
    # The queue raises the generic Exception class, not a custom error class.
    with pytest.raises(Exception) as info:
        CircularQueue(1).dequeue()
    assert type(info.value) is Exception
    assert str(info.value) == "UNDERFLOW"
