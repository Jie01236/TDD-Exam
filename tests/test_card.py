import pytest
from poker.card import Card


def test_parse_ace_of_spades():
    c = Card.from_str("AS")
    assert c.rank == 14
    assert c.suit == "S"


def test_parse_ten_of_hearts_accepts_10_and_case_insensitive():
    c = Card.from_str("10h")
    assert c.rank == 10
    assert c.suit == "H"


def test_parse_face_cards():
    assert Card.from_str("JD").rank == 11
    assert Card.from_str("QH").rank == 12
    assert Card.from_str("KC").rank == 13
    assert Card.from_str("AS").rank == 14


def test_invalid_card_raises():
    with pytest.raises(ValueError):
        Card.from_str("1S")
    with pytest.raises(ValueError):
        Card.from_str("VS")
    with pytest.raises(ValueError):
        Card.from_str("10P")
    with pytest.raises(ValueError):
        Card.from_str("")


def test_sorting_is_by_rank_only_suit_does_not_break_ties():
    a_spades = Card.from_str("AS")
    a_hearts = Card.from_str("AH")
    k_spades = Card.from_str("KS")

    sorted_cards = sorted([k_spades, a_hearts, a_spades], reverse=True)
    assert sorted_cards[0].rank == 14
    assert sorted_cards[1].rank == 14
    assert sorted_cards[2].rank == 13
