from agent_core import Agent

class SendResultB(Agent):
    """Sends the result of palindrome check back to Robot A."""
    def run(self, ctx):
        if ctx.get('is_pal'):
            print(f"[SendResultB] Sending palindrome '{ctx['word']}' back to Robot A")
            self.router.publish('result_channel', ctx['word'])
            ctx.setdefault('log_b', []).append(f"SendResultB: Sent palindrome '{ctx['word']}' back to Robot A")
        else:
            print(f"[SendResultB] '{ctx.get('word')}' is not a palindrome, nothing sent")
            ctx.setdefault('log_b', []).append(f"SendResultB: '{ctx.get('word')}' is not a palindrome, nothing sent") 