from agent_core import Agent

class LoadInput(Agent):
    """Loads input text into the context"""
    def run(self, ctx):
        ctx['sentence'] = ctx['input']
        ctx.setdefault('log_a', []).append("LoadInput: Loaded input text")

class ToLower(Agent):
    """Converts text to lowercase"""
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].lower()
        ctx.setdefault('log_a', []).append("ToLower: Converted to lowercase")

class RemovePunct(Agent):
    """Removes punctuation from text"""
    def run(self, ctx):
        import string
        ctx['sentence'] = ctx['sentence'].translate(str.maketrans('', '', string.punctuation))
        ctx.setdefault('log_a', []).append("RemovePunct: Removed punctuation")

class RemoveSpaces(Agent):
    """Removes extra spaces from text"""
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].replace('  ', ' ')
        ctx.setdefault('log_a', []).append("RemoveSpaces: Removed extra spaces")

class SplitWords(Agent):
    """Splits text into words"""
    def run(self, ctx):
        ctx['words'] = ctx['sentence'].split()
        ctx['total_words'] = len(ctx['words'])
        ctx.setdefault('log_a', []).append(f"SplitWords: Split into {ctx['total_words']} words")

class TrimWords(Agent):
    """Trims whitespace from words"""
    def run(self, ctx):
        ctx['words'] = [w.strip() for w in ctx['words']]
        ctx.setdefault('log_a', []).append("TrimWords: Trimmed whitespace from words") 