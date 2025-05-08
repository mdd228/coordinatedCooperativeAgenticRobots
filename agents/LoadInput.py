import time
from agent_core import Agent

class LoadInput(Agent):
    """Loads input text into the context."""
    def run(self, ctx):
        ctx['sentence'] = ctx['input']
        ctx['start_time'] = time.time()
        ctx.setdefault('log_a', []).append("LoadInput: Loaded input text") 