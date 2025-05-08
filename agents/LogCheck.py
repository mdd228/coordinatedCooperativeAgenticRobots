from agent_core import Agent

class LogCheck(Agent):
    """Logs the check result."""
    def run(self, ctx):
        ctx.setdefault('log_b', []).append(f"LogCheck: Completed check for '{ctx.get('word', '')}'") 