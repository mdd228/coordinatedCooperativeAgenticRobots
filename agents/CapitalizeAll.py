from agent_core import Agent

class CapitalizeAll(Agent):
    """Capitalizes all text."""
    def run(self, ctx):
        if 'output' in ctx:
            ctx['output'] = ctx['output'].upper()
            ctx.setdefault('log_a', []).append("CapitalizeAll: Capitalized output") 