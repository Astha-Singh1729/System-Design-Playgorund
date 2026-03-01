from sqids import Sqids 

sqids = Sqids(
    min_length=0,
    alphabet="5B8iG9l2Wp6b3r1t7k0h4nQzXvAdZfCoRuMsYwJgxeacDyjEKHIqLVNmOPTUFS"
)

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(num: int) -> str:
    """
    Converts a Database ID (e.g., 105) into a unique code (e.g., 'Tr8').
    """
    # Sqids expects a list of numbers, so we wrap 'num' in brackets
    return sqids.encode([num])

def decode(string: str) -> int:
    """
    Converts a code (e.g., 'Tr8') back into a Database ID (e.g., 105).
    """
    numbers = sqids.decode(string)
    # If decode fails or returns empty, return 0 or None
    if not numbers:
        return 0
    return numbers[0]
