from poker.card import Card


def _sort_cards_desc(cards: list[Card]) -> list[Card]:
    
    return sorted(cards, key=lambda c: (c.rank, c.suit), reverse=True)


def rank5(cards: list[Card]) -> dict:
    if len(cards) != 5:
        raise ValueError("rank5 expects exactly 5 cards")

    chosen = _sort_cards_desc(cards)
    ranks = tuple(c.rank for c in chosen)

    return {
        "category": "HIGH_CARD",
        "chosen5": chosen,
        "tiebreak": ranks,
    }
