from agent_core import Agent

class SplitWords(Agent):
    """Splits text into words."""
    def run(self, ctx):
        ctx['words'] = ctx['sentence'].split()
        ctx['total_words'] = len(ctx['words'])
        ctx.setdefault('log_a', []).append(f"SplitWords: Split into {ctx['total_words']} words") 