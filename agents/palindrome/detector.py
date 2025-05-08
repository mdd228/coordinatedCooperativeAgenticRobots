from core.agent import Agent
from core.state import WorkflowContext, WorkflowState
from core.router import MessageType

class PalindromeDetector(Agent):
    """Enhanced palindrome detection agent"""
    
    def __init__(self, router):
        super().__init__(router, "PalindromeDetector")
    
    def is_palindrome(self, word: str) -> bool:
        """Check if a word is a palindrome"""
        # Remove any remaining spaces and convert to lowercase
        word = word.lower().replace(" ", "")
        return word == word[::-1]
    
    def process(self, context: WorkflowContext) -> bool:
        try:
            if not context.words:
                context.add_error("No words to process")
                return False
            
            # Process each word
            for word in context.words:
                context.current_word = word
                if self.is_palindrome(word):
                    context.palindromes.append(word)
                
                # Send word to other robot for verification
                message_id = self.send_message(
                    "word_channel",
                    MessageType.WORD,
                    word
                )
                
                # Wait for acknowledgment
                if message_id and not self.router.wait_for_ack("word_channel", message_id):
                    context.add_error(f"Failed to get acknowledgment for word: {word}")
                    continue
                
                # Wait for result
                result = self.receive_message("result_channel")
                if result is None:
                    context.add_error(f"No result received for word: {word}")
                    continue
                
                # Verify result matches our calculation
                if result != self.is_palindrome(word):
                    context.add_error(f"Result mismatch for word: {word}")
            
            return True
        except Exception as e:
            context.add_error(f"Palindrome detection error: {str(e)}")
            return False
    
    def validate_output(self, context: WorkflowContext) -> bool:
        """Validate that palindrome detection was successful"""
        if context.state == WorkflowState.ERROR:
            return False
        return True 