from poker.card import Card
from poker.evaluator import holdem_best


def test_holdem_best_uses_board_and_hole_to_form_best_hand():
    board = [
        Card.from_str("AS"),
        Card.from_str("KD"),
        Card.from_str("9C"),
        Card.from_str("5H"),
        Card.from_str("2D"),
    ]
    hole = [Card.from_str("AH"), Card.from_str("3S")]

    result = holdem_best(board, hole)

    assert result["category"] == "ONE_PAIR"
    assert [c.rank for c in result["chosen5"]] == [14, 14, 13, 9, 5]
    assert result["tiebreak"] == (14, 13, 9, 5)
