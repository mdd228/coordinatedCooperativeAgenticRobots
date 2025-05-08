from agent_core import Agent

class ReceiveWordB(Agent):
    """Receives a word to check."""
    def run(self, ctx):
        word = self.router.subscribe('word_channel')
        ctx['word'] = word
        print(f"[ReceiveWordB] Received word: {word}")
        if word == 'STOP':
            ctx['done'] = True
            ctx.setdefault('log_b', []).append("ReceiveWordB: Received STOP signal from Robot A")
        else:
            ctx.setdefault('log_b', []).append(f"ReceiveWordB: Received word '{word}' from Robot A") 