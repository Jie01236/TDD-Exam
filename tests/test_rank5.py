import pytest
from poker.card import Card
from poker.evaluator import rank5


# =====================================================
# HIGH CARD
# =====================================================

def test_rank5_high_card_basic():
    cards = [
        Card.from_str("AS"),
        Card.from_str("KD"),
        Card.from_str("9C"),
        Card.from_str("5H"),
        Card.from_str("2D"),
    ]

    result = rank5(cards)

    assert result["category"] == "HIGH_CARD"
    assert [c.rank for c in result["chosen5"]] == [14, 13, 9, 5, 2]
    assert result["tiebreak"] == (14, 13, 9, 5, 2)


# =====================================================
# ONE PAIR
# =====================================================

def test_rank5_one_pair_basic():
    cards = [
        Card.from_str("AS"),
        Card.from_str("AH"),
        Card.from_str("KD"),
        Card.from_str("9C"),
        Card.from_str("2D"),
    ]

    result = rank5(cards)

    assert result["category"] == "ONE_PAIR"
    assert [c.rank for c in result["chosen5"]] == [14, 14, 13, 9, 2]
    assert result["tiebreak"] == (14, 13, 9, 2)


def test_rank5_one_pair_tie_break():
    cards1 = [
        Card.from_str("AS"),
        Card.from_str("AH"),
        Card.from_str("KD"),
        Card.from_str("9C"),
        Card.from_str("2D"),
    ]
    cards2 = [
        Card.from_str("KS"),
        Card.from_str("KH"),
        Card.from_str("QD"),
        Card.from_str("JC"),
        Card.from_str("2H"),
    ]

    r1 = rank5(cards1)
    r2 = rank5(cards2)

    assert r1["tiebreak"] > r2["tiebreak"]  # AA > KK


# =====================================================
# TWO PAIR
# =====================================================

def test_rank5_two_pair_basic():
    cards = [
        Card.from_str("KS"),
        Card.from_str("KH"),
        Card.from_str("7D"),
        Card.from_str("7C"),
        Card.from_str("AS"),
    ]

    result = rank5(cards)

    assert result["category"] == "TWO_PAIR"
    assert [c.rank for c in result["chosen5"]] == [13, 13, 7, 7, 14]
    assert result["tiebreak"] == (13, 7, 14)


# =====================================================
# THREE OF A KIND
# =====================================================

def test_rank5_three_of_a_kind():
    cards = [
        Card.from_str("9S"),
        Card.from_str("9H"),
        Card.from_str("9D"),
        Card.from_str("KS"),
        Card.from_str("2C"),
    ]

    result = rank5(cards)

    assert result["category"] == "THREE_OF_A_KIND"
    assert [c.rank for c in result["chosen5"]] == [9, 9, 9, 13, 2]
    assert result["tiebreak"] == (9, 13, 2)


# =====================================================
# STRAIGHT
# =====================================================

def test_rank5_straight_ace_high():
    cards = [
        Card.from_str("10S"),
        Card.from_str("JD"),
        Card.from_str("QC"),
        Card.from_str("KH"),
        Card.from_str("AS"),
    ]

    result = rank5(cards)

    assert result["category"] == "STRAIGHT"
    assert [c.rank for c in result["chosen5"]] == [14, 13, 12, 11, 10]
    assert result["tiebreak"] == (14,)


def test_rank5_straight_wheel_ace_low():
    cards = [
        Card.from_str("AS"),
        Card.from_str("2D"),
        Card.from_str("3C"),
        Card.from_str("4H"),
        Card.from_str("5S"),
    ]

    result = rank5(cards)

    assert result["category"] == "STRAIGHT"
    assert [c.rank for c in result["chosen5"]] == [5, 4, 3, 2, 14]
    assert result["tiebreak"] == (5,)


# =====================================================
# FLUSH
# =====================================================

def test_rank5_flush():
    cards = [
        Card.from_str("AS"),
        Card.from_str("QS"),
        Card.from_str("9S"),
        Card.from_str("5S"),
        Card.from_str("2S"),
    ]

    result = rank5(cards)

    assert result["category"] == "FLUSH"
    assert [c.rank for c in result["chosen5"]] == [14, 12, 9, 5, 2]
    assert result["tiebreak"] == (14, 12, 9, 5, 2)


# =====================================================
# FULL HOUSE
# =====================================================

def test_rank5_full_house():
    cards = [
        Card.from_str("KS"),
        Card.from_str("KH"),
        Card.from_str("KD"),
        Card.from_str("2C"),
        Card.from_str("2D"),
    ]

    result = rank5(cards)

    assert result["category"] == "FULL_HOUSE"
    assert [c.rank for c in result["chosen5"]] == [13, 13, 13, 2, 2]
    assert result["tiebreak"] == (13, 2)


# =====================================================
# FOUR OF A KIND
# =====================================================

def test_rank5_four_of_a_kind():
    cards = [
        Card.from_str("7S"),
        Card.from_str("7H"),
        Card.from_str("7D"),
        Card.from_str("7C"),
        Card.from_str("AS"),
    ]

    result = rank5(cards)

    assert result["category"] == "FOUR_OF_A_KIND"
    assert [c.rank for c in result["chosen5"]] == [7, 7, 7, 7, 14]
    assert result["tiebreak"] == (7, 14)


# =====================================================
# STRAIGHT FLUSH
# =====================================================

def test_rank5_straight_flush():
    cards = [
        Card.from_str("9S"),
        Card.from_str("10S"),
        Card.from_str("JS"),
        Card.from_str("QS"),
        Card.from_str("KS"),
    ]

    result = rank5(cards)

    assert result["category"] == "STRAIGHT_FLUSH"
    assert [c.rank for c in result["chosen5"]] == [13, 12, 11, 10, 9]
    assert result["tiebreak"] == (13,)
