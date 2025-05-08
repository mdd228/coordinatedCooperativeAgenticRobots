from agent_core import Agent

class CheckPhrasePalindrome(Agent):
    """Checks if the fully normalized sentence is a palindrome."""
    def run(self, ctx):
        original = ctx.get('sentence', '')
        # Normalize: remove spaces and punctuation, lowercase
        import string
        normalized = original.replace(' ', '').lower().translate(str.maketrans('', '', string.punctuation))
        if normalized and normalized == normalized[::-1] and len(normalized) > 1:
            ctx.setdefault('palindromes', []).append(f"[PHRASE] {original.strip()}")
            ctx.setdefault('log_a', []).append(f"CheckPhrasePalindrome: Found phrase palindrome '{original.strip()}'")
        else:
            ctx.setdefault('log_a', []).append(f"CheckPhrasePalindrome: '{original.strip()}' is not a phrase palindrome") 