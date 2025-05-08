from agent_core import Agent
import time

class SendWord(Agent):
    """Sends a word to be checked for palindrome"""
    def run(self, ctx):
        if ctx['words']:
            w = ctx['words'].pop(0)
            ctx['current_word'] = w
            self.router.publish('word_channel', w)
            ctx.setdefault('log_a', []).append(f"SendWord: Sent '{w}' to Robot B")
            print(f"RobotA: Sending word '{w}' to RobotB")

class ReceiveResult(Agent):
    """Receives palindrome check result"""
    def run(self, ctx):
        result = self.router.subscribe('result_channel')
        if result:  # Only append if it's a palindrome
            ctx.setdefault('palindromes', []).append(result)
            ctx.setdefault('log_a', []).append(f"ReceiveResult: Received palindrome '{result}' from Robot B")
            print(f"RobotA: Received palindrome '{result}' from RobotB")

class HasMoreWords(Agent):
    """Checks if there are more words to process"""
    def run(self, ctx):
        if not ctx['words']:
            ctx['done'] = True
            ctx.setdefault('log_a', []).append("HasMoreWords: No more words to process")
            print("RobotA: No more words to process")

class SortPalindromes(Agent):
    """Sorts found palindromes"""
    def run(self, ctx):
        if 'palindromes' in ctx:
            ctx['palindromes'].sort()
            ctx.setdefault('log_a', []).append(f"SortPalindromes: Sorted {len(ctx['palindromes'])} palindromes")
            print(f"RobotA: Sorted {len(ctx['palindromes'])} palindromes")

class JoinWithComma(Agent):
    """Joins palindromes with commas"""
    def run(self, ctx):
        if 'palindromes' in ctx:
            ctx['output'] = ','.join(ctx['palindromes'])
            ctx.setdefault('log_a', []).append(f"JoinWithComma: Joined palindromes: {ctx['output']}")
            print(f"RobotA: Joined palindromes: {ctx['output']}")

class DuplicateOutput(Agent):
    """Duplicates the output for emphasis"""
    def run(self, ctx):
        if 'output' in ctx:
            ctx['output'] = ctx['output'] + ctx['output']
            ctx.setdefault('log_a', []).append("DuplicateOutput: Duplicated output for emphasis")
            print("RobotA: Duplicated output for emphasis")

class CapitalizeAll(Agent):
    """Capitalizes all text"""
    def run(self, ctx):
        if 'output' in ctx:
            ctx['output'] = ctx['output'].upper()
            ctx.setdefault('log_a', []).append("CapitalizeAll: Capitalized output")
            print("RobotA: Capitalized output")

class FormatFinal(Agent):
    """Formats the final output"""
    def run(self, ctx):
        if 'output' in ctx:
            elapsed_time = time.time() - ctx['start_time']
            ctx['final_output'] = f"Palindromes: {ctx['output']}\nProcessed {ctx['total_words']} words in {elapsed_time:.2f} seconds"
            ctx.setdefault('log_a', []).append("FormatFinal: Formatted final output")

class LogResult(Agent):
    """Logs the final result"""
    def run(self, ctx):
        if 'final_output' in ctx:
            ctx.setdefault('log_a', []).append("LogResult: Logged final output")
            print("\n" + "="*50)
            print(ctx['final_output'])
            print("="*50 + "\n")

# Robot B specific agents
class ReceiveWordB(Agent):
    """Receives a word to check"""
    def run(self, ctx):
        ctx['word'] = self.router.subscribe('word_channel')
        ctx.setdefault('log_b', []).append(f"ReceiveWordB: Received word '{ctx['word']}' from Robot A")
        print(f"RobotB: Received word '{ctx['word']}' from RobotA")

class ReverseText(Agent):
    """Reverses text for palindrome check"""
    def run(self, ctx):
        ctx['reversed_word'] = ctx['word'][::-1]
        ctx.setdefault('log_b', []).append(f"ReverseText: Reversed '{ctx['word']}' to '{ctx['reversed_word']}'")
        print(f"RobotB: Reversed '{ctx['word']}' to '{ctx['reversed_word']}'")

class CompareOriginal(Agent):
    """Compares original and reversed text"""
    def run(self, ctx):
        ctx['is_pal'] = (ctx['word'] == ctx['reversed_word'])
        ctx.setdefault('log_b', []).append(f"CompareOriginal: {'Found' if ctx['is_pal'] else 'Not a'} palindrome")
        print(f"RobotB: {'Found' if ctx['is_pal'] else 'Not a'} palindrome")

class SendResultB(Agent):
    """Sends palindrome check result"""
    def run(self, ctx):
        res = ctx['word'] if ctx['is_pal'] else ''
        if res:
            self.router.publish('result_channel', res)
            ctx.setdefault('log_b', []).append(f"SendResultB: Sent palindrome '{res}' back to Robot A")
            print(f"RobotB: Sending palindrome '{res}' back to RobotA")

class LogCheck(Agent):
    """Logs the check result"""
    def run(self, ctx):
        ctx.setdefault('log_b', []).append(f"LogCheck: Completed check for '{ctx.get('word', '')}'")
        print(f"RobotB: Completed check for '{ctx['word']}'") 