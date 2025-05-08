from agent_core import Agent

class ReceiveResult(Agent):
    """Receives palindrome check result for the current word."""
    def run(self, ctx):
        idx = ctx.get('current_word_index', 0)
        total = ctx.get('total_words', 0)
        if idx < total:
            result = self.router.subscribe('result_channel')
            print(f"[ReceiveResult] Got result '{result}' from Robot B (index {idx})")
            ctx.setdefault('log_a', []).append(f"ReceiveResult: Got result '{result}' from Robot B (index {idx})")
            if result:
                ctx.setdefault('palindromes', []).append(result)
                ctx.setdefault('log_a', []).append(f"ReceiveResult: Received palindrome '{result}' from Robot B")
            # Index increment removed; handled by main Robot loop
        else:
            ctx.setdefault('log_a', []).append("ReceiveResult: No more results to receive") 