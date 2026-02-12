from poker.card import Card
from poker.evaluator import best_of_7


def test_best_of_7_picks_best_five_from_seven():
    cards7 = [
        Card.from_str("AS"),
        Card.from_str("AH"),
        Card.from_str("KD"),
        Card.from_str("9C"),
        Card.from_str("5H"),
        Card.from_str("2D"),
        Card.from_str("3S"),
    ]

    result = best_of_7(cards7)

    assert result["category"] == "ONE_PAIR"
    assert [c.rank for c in result["chosen5"]] == [14, 14, 13, 9, 5]
    assert result["tiebreak"] == (14, 13, 9, 5)


def test_best_of_7_board_plays_is_possible():
    cards7 = [
        Card.from_str("AS"),
        Card.from_str("KD"),
        Card.from_str("QC"),
        Card.from_str("JH"),
        Card.from_str("10S"),
        Card.from_str("2D"),
        Card.from_str("3S"),
    ]

    result = best_of_7(cards7)

    assert result["category"] == "STRAIGHT"
    assert [c.rank for c in result["chosen5"]] == [14, 13, 12, 11, 10]
    assert result["tiebreak"] == (14,)


def test_best_of_7_supports_wheel_straight_a2345():
    cards7 = [
        Card.from_str("AS"),
        Card.from_str("2D"),
        Card.from_str("3C"),
        Card.from_str("4H"),
        Card.from_str("5S"),
        Card.from_str("KD"),
        Card.from_str("QC"),
    ]

    result = best_of_7(cards7)

    assert result["category"] == "STRAIGHT"
    assert [c.rank for c in result["chosen5"]] == [5, 4, 3, 2, 14]
    assert result["tiebreak"] == (5,)


def test_best_of_7_prefers_flush_over_straight_when_both_available():
    cards7 = [
        Card.from_str("AS"),
        Card.from_str("KS"),
        Card.from_str("QS"),
        Card.from_str("JS"),
        Card.from_str("9S"),
        Card.from_str("10D"),
        Card.from_str("2C"),
    ]

    result = best_of_7(cards7)

    assert result["category"] == "FLUSH"
    assert [c.rank for c in result["chosen5"]] == [14, 13, 12, 11, 9]
    assert result["tiebreak"] == (14, 13, 12, 11, 9)
