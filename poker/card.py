from __future__ import annotations
from dataclasses import dataclass


_RANK_MAP = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "T": 10,
    "J": 11, "Q": 12, "K": 13, "A": 14,
}
_VALID_SUITS = {"S", "H", "D", "C"}  


@dataclass(frozen=True, order=False)
class Card:
    rank: int  
    suit: str  
    @staticmethod
    def from_str(token: str) -> "Card":
        if not token or not token.strip():
            raise ValueError("Empty card token")

        t = token.strip().upper()

        # Last char is suit, the rest is rank
        if len(t) < 2:
            raise ValueError(f"Invalid card token: {token}")

        suit = t[-1]
        rank_part = t[:-1]

        if suit not in _VALID_SUITS:
            raise ValueError(f"Invalid suit: {suit}")

        # Accept "10" and also "T"
        rank = _RANK_MAP.get(rank_part)
        if rank is None:
            raise ValueError(f"Invalid rank: {rank_part}")

        return Card(rank=rank, suit=suit)

    # Important: no suit-based ordering. Only rank matters for comparison.
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank < other.rank
