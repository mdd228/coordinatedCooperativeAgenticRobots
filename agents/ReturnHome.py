from agent_core import Agent

class ReturnHome(Agent):
    """Signals the robot to finish processing."""
    def run(self, ctx):
        ctx['done'] = True
        ctx.setdefault('log_a', []).append("ReturnHome: Robot is done and returning home") 