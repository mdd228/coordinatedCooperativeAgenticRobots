from agent_core import Agent

class ToLower(Agent):
    """Converts text to lowercase."""
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].lower()
        ctx.setdefault('log_a', []).append("ToLower: Converted to lowercase") 