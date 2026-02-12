from collections import Counter
from poker.card import Card


def _sort_cards_desc(cards: list[Card]) -> list[Card]:
    return sorted(cards, key=lambda c: (c.rank, c.suit), reverse=True)


def rank5(cards: list[Card]) -> dict:
    if len(cards) != 5:
        raise ValueError("rank5 expects exactly 5 cards")

    counts = Counter(c.rank for c in cards)
    count_values = sorted(counts.values(), reverse=True)

    # ONE_PAIR: 2 + 1 + 1 + 1
    if count_values == [2, 1, 1, 1]:
        pair_rank = max(r for r, cnt in counts.items() if cnt == 2)
        kickers = sorted((r for r, cnt in counts.items() if cnt == 1), reverse=True)

        pair_cards = [c for c in cards if c.rank == pair_rank]
        kicker_cards = _sort_cards_desc([c for c in cards if c.rank in kickers])

        chosen = pair_cards + kicker_cards
        return {
            "category": "ONE_PAIR",
            "chosen5": chosen,
            "tiebreak": (pair_rank, *kickers),
        }

    # HIGH_CARD fallback
    chosen = _sort_cards_desc(cards)
    ranks = tuple(c.rank for c in chosen)
    return {
        "category": "HIGH_CARD",
        "chosen5": chosen,
        "tiebreak": ranks,
    }
