from agent_core import Agent

class ReturnHomeB(Agent):
    """Signals Robot B completion."""
    def run(self, ctx):
        ctx.setdefault('log_b', []).append("ReturnHomeB: Returning home") 