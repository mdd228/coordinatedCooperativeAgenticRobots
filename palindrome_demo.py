from agent_core import Agent, Robot, Router
import time
import string
from agents.CheckPhrasePalindrome import CheckPhrasePalindrome

# Text Processing Agents
class LoadInput(Agent):
    def run(self, ctx):
        ctx['sentence'] = ctx['input']
        ctx['start_time'] = time.time()
        print(f"RobotA: Loaded input text: {ctx['input']}")

class ToLower(Agent):
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].lower()

class RemovePunct(Agent):
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].translate(str.maketrans('', '', string.punctuation))

class RemoveSpaces(Agent):
    def run(self, ctx):
        ctx['sentence'] = ctx['sentence'].replace('  ', ' ')

class SplitWords(Agent):
    def run(self, ctx):
        ctx['words'] = ctx['sentence'].split()
        ctx['total_words'] = len(ctx['words'])
        ctx['words_to_process'] = ctx['words'].copy()  # Create a queue of words to process
        print(f"RobotA: Split into {ctx['total_words']} words")

# Robot A Agents
class SendWord(Agent):
    def run(self, ctx):
        if ctx['words_to_process']:
            word = ctx['words_to_process'].pop(0)  # Take the next word from queue
            self.router.publish('word_channel', word)
            print(f"RobotA: Sending word '{word}' to RobotB")
        else:
            self.router.publish('word_channel', '')  # Signal end of words
            ctx['done'] = True
            print("RobotA: No more words to process")

class ReceiveResult(Agent):
    def run(self, ctx):
        result = self.router.subscribe('result_channel')
        if result:
            ctx.setdefault('palindromes', []).append(result)
            print(f"RobotA: Received palindrome '{result}' from RobotB")

class FormatOutput(Agent):
    def run(self, ctx):
        if 'palindromes' in ctx:
            palindromes = sorted(set(ctx['palindromes']))  # Remove duplicates and sort
            elapsed_time = time.time() - ctx['start_time']
            output = f"\n{'='*50}\n"
            output += f"Found {len(palindromes)} palindromes: {', '.join(palindromes)}\n"
            output += f"Processed {ctx['total_words']} words in {elapsed_time:.2f} seconds\n"
            output += f"{'='*50}\n"
            print(output)

# Robot B Agents
class ReceiveWordB(Agent):
    def run(self, ctx):
        word = self.router.subscribe('word_channel')
        if not word:  # Empty string signals end
            ctx['done'] = True
            return
        ctx['word'] = word
        print(f"RobotB: Received word '{word}' from RobotA")

class CheckPalindrome(Agent):
    def run(self, ctx):
        if 'word' in ctx:
            word = ctx['word']
            is_palindrome = word == word[::-1]
            if is_palindrome:
                self.router.publish('result_channel', word)
                print(f"RobotB: Found palindrome '{word}'")
            else:
                print(f"RobotB: '{word}' is not a palindrome")

# Robot Definitions
class RobotA(Robot):
    def run(self):
        # Initialize and process text
        for agent in [LoadInput, ToLower, RemovePunct, RemoveSpaces, CheckPhrasePalindrome, SplitWords]:
            agent(self.router).run(self.context)
        
        # Process words and collect results
        while not self.context.get('done', False):
            SendWord(self.router).run(self.context)
            ReceiveResult(self.router).run(self.context)
            time.sleep(0.1)
        
        # Format final output
        FormatOutput(self.router).run(self.context)
        print("RobotA: Task completed")

class RobotB(Robot):
    def run(self):
        while True:
            ReceiveWordB(self.router).run(self.context)
            if self.context.get('done', False):
                break
            CheckPalindrome(self.router).run(self.context)
            time.sleep(0.1)
        print("RobotB: Task completed")

if __name__ == '__main__':
    router = Router()
    robot_a = RobotA(router)
    robot_b = RobotB(router)
    
    # Set input text
    robot_a.context['input'] = "Madam Arora teaches malayalam"
    
    print("\nStarting Palindrome Finder...\n")
    
    # Start robots
    robot_b.start()  # Start B first to ensure it's ready to receive
    time.sleep(0.1)
    robot_a.start()
    
    # Wait for completion
    robot_a.join()
    robot_b.join() 