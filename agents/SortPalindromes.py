from agent_core import Agent

class SortPalindromes(Agent):
    """Sorts the list of found palindromes."""
    def run(self, ctx):
        pals = ctx.get('palindromes', [])
        if pals:
            ctx['palindromes'] = sorted(set(pals))
            ctx.setdefault('log_a', []).append(f"SortPalindromes: Sorted palindromes {ctx['palindromes']}")
        else:
            ctx.setdefault('log_a', []).append("SortPalindromes: No palindromes to sort") 