from poker.card import Card
from poker.evaluator import determine_winners


def test_determine_winners_single_winner():
    board = [
        Card.from_str("AS"),
        Card.from_str("KD"),
        Card.from_str("9C"),
        Card.from_str("5H"),
        Card.from_str("2D"),
    ]

    p0 = [Card.from_str("AH"), Card.from_str("3S")]

    p1 = [Card.from_str("QH"), Card.from_str("JS")]

    out = determine_winners(board, [p0, p1])

    assert out["winners"] == [0]
    assert out["results"][0]["category"] == "ONE_PAIR"
    assert out["results"][1]["category"] == "HIGH_CARD"


def test_determine_winners_split_board_plays():
    board = [
        Card.from_str("5C"),
        Card.from_str("6D"),
        Card.from_str("7H"),
        Card.from_str("8S"),
        Card.from_str("9D"),
    ]

    p0 = [Card.from_str("AS"), Card.from_str("AH")]
    p1 = [Card.from_str("KC"), Card.from_str("QD")]

    out = determine_winners(board, [p0, p1])

    assert out["winners"] == [0, 1]
    assert out["results"][0]["category"] == "STRAIGHT"
    assert out["results"][1]["category"] == "STRAIGHT"
    assert [c.rank for c in out["results"][0]["chosen5"]] == [9, 8, 7, 6, 5]
