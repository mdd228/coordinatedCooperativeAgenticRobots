from agent_core import Agent

class DuplicateOutput(Agent):
    """Duplicates the output."""
    def run(self, ctx):
        if 'output' in ctx:
            ctx['output'] = ctx['output'] + ' ' + ctx['output']
            ctx.setdefault('log_a', []).append("DuplicateOutput: Duplicated output") 