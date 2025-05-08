from agent_core import Agent

class TrimWords(Agent):
    """Trims whitespace from words."""
    def run(self, ctx):
        ctx['words'] = [w.strip() for w in ctx['words']]
        print(f"[TrimWords] Final words list: {ctx['words']}")
        ctx.setdefault('log_a', []).append("TrimWords: Trimmed whitespace from words") 