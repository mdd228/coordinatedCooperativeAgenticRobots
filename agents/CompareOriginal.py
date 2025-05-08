from agent_core import Agent

class CompareOriginal(Agent):
    """Compares original and reversed word to check for palindrome."""
    def run(self, ctx):
        word = ctx.get('word', '')
        reversed_word = ctx.get('reversed_word', '')
        print(f"[CompareOriginal] Comparing: word='{word}', reversed_word='{reversed_word}'")
        if word and word == reversed_word:
            ctx['is_pal'] = True
            print(f"[CompareOriginal] '{word}' is a palindrome.")
            ctx.setdefault('log_b', []).append(f"CompareOriginal: Found palindrome '{word}'")
        else:
            ctx['is_pal'] = False
            print(f"[CompareOriginal] '{word}' is NOT a palindrome.")
            ctx.setdefault('log_b', []).append(f"CompareOriginal: '{word}' is not a palindrome") 