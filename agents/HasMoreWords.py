from agent_core import Agent

class HasMoreWords(Agent):
    """Checks if there are more words to process and signals completion."""
    def run(self, ctx):
        idx = ctx.get('current_word_index', 0)
        total = ctx.get('total_words', 0)
        if idx >= total:
            print(f"[HasMoreWords] No more words to process (index {idx}, total {total})")
            ctx['done'] = True
            ctx.setdefault('log_a', []).append(f"HasMoreWords: No more words to process (index {idx}, total {total})")
        else:
            print(f"[HasMoreWords] More words to process (index {idx}, total {total})")
            ctx.setdefault('log_a', []).append(f"HasMoreWords: More words to process (index {idx}, total {total})") 