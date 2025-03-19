# token_tracker.py
class TokenTracker:
    _total_tokens = 0  # Class-level token counter

    @classmethod
    def add_tokens(cls, tokens: int):
        """Add tokens to the global counter."""
        cls._total_tokens += tokens

    @classmethod
    def get_total_tokens(cls) -> int:
        """Get the total tokens used so far."""
        return cls._total_tokens