from agent_core import Agent
import string

class RemovePunct(Agent):
    """Removes punctuation from text."""
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].translate(str.maketrans('', '', string.punctuation))
        ctx.setdefault('log_a', []).append("RemovePunct: Removed punctuation") 