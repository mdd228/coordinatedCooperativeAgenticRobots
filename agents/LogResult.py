from agent_core import Agent

class LogResult(Agent):
    """Logs the final result."""
    def run(self, ctx):
        if 'final_output' in ctx:
            ctx.setdefault('log_a', []).append("LogResult: Logged final output") 