from collections import Counter
from poker.card import Card


def _sort_cards_desc(cards: list[Card]) -> list[Card]:
    return sorted(cards, key=lambda c: (c.rank, c.suit), reverse=True)


def _straight_high_and_order(ranks: list[int]) -> tuple[int, list[int]] | None:
    uniq = sorted(set(ranks), reverse=True)
    if len(uniq) != 5:
        return None

    # Wheel: A,2,3,4,5 => high = 5, order = 5,4,3,2,A
    if set(uniq) == {14, 5, 4, 3, 2}:
        return 5, [5, 4, 3, 2, 14]

    # Normal straight
    if uniq[0] - uniq[4] == 4 and all(uniq[i] - 1 == uniq[i + 1] for i in range(4)):
        return uniq[0], uniq[:] 
    return None


def rank5(cards: list[Card]) -> dict:
    if len(cards) != 5:
        raise ValueError("rank5 expects exactly 5 cards")

    ranks = [c.rank for c in cards]
    counts = Counter(ranks)
    count_values = sorted(counts.values(), reverse=True)

    is_flush = len({c.suit for c in cards}) == 1
    straight = _straight_high_and_order(ranks)

    if is_flush:
        chosen = _sort_cards_desc(cards)
        return {
            "category": "FLUSH",
            "chosen5": chosen,
            "tiebreak": tuple(c.rank for c in chosen),
        }

    if straight is not None:
        high, order = straight
        chosen = [next(c for c in cards if c.rank == r) for r in order]
        return {
            "category": "STRAIGHT",
            "chosen5": chosen,
            "tiebreak": (high,),
        }

    # THREE_OF_A_KIND: 3 + 1 + 1
    if count_values == [3, 1, 1]:
        trip_rank = max(r for r, cnt in counts.items() if cnt == 3)
        kickers = sorted((r for r, cnt in counts.items() if cnt == 1), reverse=True)
        return {
            "category": "THREE_OF_A_KIND",
            "chosen5": [c for c in cards if c.rank == trip_rank] + _sort_cards_desc([c for c in cards if c.rank in kickers]),
            "tiebreak": (trip_rank, *kickers),
        }

    # TWO_PAIR: 2 + 2 + 1
    if count_values == [2, 2, 1]:
        pair_ranks = sorted((r for r, cnt in counts.items() if cnt == 2), reverse=True)
        high_pair, low_pair = pair_ranks[0], pair_ranks[1]
        kicker_rank = next(r for r, cnt in counts.items() if cnt == 1)
        chosen = [c for c in cards if c.rank == high_pair] + \
                 [c for c in cards if c.rank == low_pair] + \
                 _sort_cards_desc([c for c in cards if c.rank == kicker_rank])
        return {
            "category": "TWO_PAIR",
            "chosen5": chosen,
            "tiebreak": (high_pair, low_pair, kicker_rank),
        }

    # ONE_PAIR: 2 + 1 + 1 + 1
    if count_values == [2, 1, 1, 1]:
        pair_rank = max(r for r, cnt in counts.items() if cnt == 2)
        kickers = sorted((r for r, cnt in counts.items() if cnt == 1), reverse=True)
        return {
            "category": "ONE_PAIR",
            "chosen5": [c for c in cards if c.rank == pair_rank] + _sort_cards_desc([c for c in cards if c.rank in kickers]),
            "tiebreak": (pair_rank, *kickers),
        }

    # HIGH_CARD
    chosen = _sort_cards_desc(cards)
    return {
        "category": "HIGH_CARD",
        "chosen5": chosen,
        "tiebreak": tuple(c.rank for c in chosen),
    }
