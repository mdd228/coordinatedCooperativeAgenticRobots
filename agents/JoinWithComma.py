from agent_core import Agent

class JoinWithComma(Agent):
    """Joins palindromes with a comma for output."""
    def run(self, ctx):
        pals = ctx.get('palindromes', [])
        if pals:
            ctx['output'] = ', '.join(pals)
            ctx.setdefault('log_a', []).append(f"JoinWithComma: Joined palindromes into '{ctx['output']}'")
        else:
            ctx['output'] = ''
            ctx.setdefault('log_a', []).append("JoinWithComma: No palindromes to join") 