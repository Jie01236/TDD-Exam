from __future__ import annotations

from collections import Counter
from itertools import combinations
from poker.card import Card


# -----------------------------
# Global category ordering (PDF)
# -----------------------------
CATEGORY_STRENGTH: dict[str, int] = {
    "HIGH_CARD": 0,
    "ONE_PAIR": 1,
    "TWO_PAIR": 2,
    "THREE_OF_A_KIND": 3,
    "STRAIGHT": 4,
    "FLUSH": 5,
    "FULL_HOUSE": 6,
    "FOUR_OF_A_KIND": 7,
    "STRAIGHT_FLUSH": 8,
}


def _hand_key(result: dict) -> tuple[int, tuple]:
    return (CATEGORY_STRENGTH[result["category"]], result["tiebreak"])


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

    # STRAIGHT_FLUSH (highest): flush + straight
    if is_flush and straight is not None:
        high, order = straight
        chosen = [next(c for c in cards if c.rank == r) for r in order]
        return {
            "category": "STRAIGHT_FLUSH",
            "chosen5": chosen,
            "tiebreak": (high,),
        }

    # FOUR_OF_A_KIND
    if count_values == [4, 1]:
        quad_rank = max(r for r, cnt in counts.items() if cnt == 4)
        kicker_rank = max(r for r, cnt in counts.items() if cnt == 1)
        chosen = [c for c in cards if c.rank == quad_rank] + _sort_cards_desc([c for c in cards if c.rank == kicker_rank])
        return {
            "category": "FOUR_OF_A_KIND",
            "chosen5": chosen,
            "tiebreak": (quad_rank, kicker_rank),
        }

    # FULL_HOUSE: 3 + 2
    if count_values == [3, 2]:
        trip_rank = max(r for r, cnt in counts.items() if cnt == 3)
        pair_rank = max(r for r, cnt in counts.items() if cnt == 2)
        chosen = [c for c in cards if c.rank == trip_rank] + [c for c in cards if c.rank == pair_rank]
        return {
            "category": "FULL_HOUSE",
            "chosen5": chosen,
            "tiebreak": (trip_rank, pair_rank),
        }

    # FLUSH
    if is_flush:
        chosen = _sort_cards_desc(cards)
        return {
            "category": "FLUSH",
            "chosen5": chosen,
            "tiebreak": tuple(c.rank for c in chosen),
        }

    # STRAIGHT
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
        chosen = [c for c in cards if c.rank == trip_rank] + _sort_cards_desc([c for c in cards if c.rank in kickers])
        return {
            "category": "THREE_OF_A_KIND",
            "chosen5": chosen,
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
        chosen = [c for c in cards if c.rank == pair_rank] + _sort_cards_desc([c for c in cards if c.rank in kickers])
        return {
            "category": "ONE_PAIR",
            "chosen5": chosen,
            "tiebreak": (pair_rank, *kickers),
        }

    # HIGH_CARD
    chosen = _sort_cards_desc(cards)
    return {
        "category": "HIGH_CARD",
        "chosen5": chosen,
        "tiebreak": tuple(c.rank for c in chosen),
    }

def best_of_7(cards7: list[Card]) -> dict:
    """
    Choose the best 5-card hand out of 7 cards.
    Returns the winning 5-card evaluation dict (category/chosen5/tiebreak).
    """
    if len(cards7) != 7:
        raise ValueError("best_of_7 expects exactly 7 cards")

    best: dict | None = None
    best_key: tuple[int, tuple] | None = None

    for combo in combinations(cards7, 5):
        r = rank5(list(combo))
        k = _hand_key(r)
        if best is None or k > best_key:
            best = r
            best_key = k

    return best  


def holdem_best(board5: list[Card], hole2: list[Card]) -> dict:
    """
    Texas Hold'em: best 5-card hand out of board5 + hole2.
    Allows 0/1/2 hole cards to be used naturally.
    """
    if len(board5) != 5:
        raise ValueError("holdem_best expects exactly 5 board cards")
    if len(hole2) != 2:
        raise ValueError("holdem_best expects exactly 2 hole cards")
    return best_of_7(board5 + hole2)