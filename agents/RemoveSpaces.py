from agent_core import Agent

class RemoveSpaces(Agent):
    """Removes extra spaces from text."""
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].replace('  ', ' ')
        ctx.setdefault('log_a', []).append("RemoveSpaces: Removed extra spaces") 