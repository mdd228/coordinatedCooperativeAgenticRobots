from agent_core import Agent
import time

class FormatFinal(Agent):
    """Formats the final output."""
    def run(self, ctx):
        if 'palindromes' in ctx:
            elapsed_time = time.time() - ctx.get('start_time', time.time())
            palindromes_str = ', '.join(ctx.get('palindromes', []))
            total_words = ctx.get('total_words', 0)
            ctx['final_output'] = f"Found palindromes: {palindromes_str}\nProcessed {total_words} words in {elapsed_time:.2f} seconds"
            ctx.setdefault('log_a', []).append("FormatFinal: Formatted final output") 