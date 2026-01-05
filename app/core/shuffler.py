import secrets
from typing import List, TypeVar

T = TypeVar('T')

class Shuffler:
    @staticmethod
    def shuffle(deck: List[T]) -> List[T]:
        """
        Cryptographically secure shuffle using the secrets module (Fisher-Yates).
        Returns a new list to avoid mutating the original.
        """
        # Create a copy to preserve original
        shuffled_deck = deck[:]
        # SystemRandom uses os.urandom(), which is cryptographically secure
        secrets.SystemRandom().shuffle(shuffled_deck)
        return shuffled_deck

    @staticmethod
    def pick_card(deck: List[T]) -> T:
        """Picks a single random card securely."""
        return secrets.choice(deck)
