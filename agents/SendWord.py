from agent_core import Agent

class SendWord(Agent):
    """Sends one word at a time to be checked for palindrome. Sends STOP when done."""
    def run(self, ctx):
        idx = ctx.get('current_word_index', 0)
        words = ctx.get('words', [])
        if idx < len(words):
            word = words[idx]
            ctx['current_word'] = word
            print(f"[SendWord] Sending word '{word}' at index {idx}")
            self.router.publish('word_channel', word)
            ctx.setdefault('log_a', []).append(f"SendWord: Sent '{word}' to Robot B (index {idx})")
        else:
            self.router.publish('word_channel', 'STOP')
            ctx.setdefault('log_a', []).append("SendWord: No more words to send, sent STOP to Robot B") 