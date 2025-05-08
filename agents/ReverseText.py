from agent_core import Agent

class ReverseText(Agent):
    """Reverses the word for palindrome checking."""
    def run(self, ctx):
        word = ctx.get('word', '')
        ctx['reversed_word'] = word[::-1]
        print(f"[ReverseText] Word: '{word}', Reversed: '{ctx['reversed_word']}'")
        ctx.setdefault('log_b', []).append(f"ReverseText: Reversed '{word}' to '{ctx['reversed_word']}'") 