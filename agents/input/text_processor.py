import re
from typing import List
from core.agent import Agent
from core.state import WorkflowContext
from core.router import Router, MessageType

class SpecialCharHandler(Agent):
    """Agent specifically for handling special characters"""
    
    def __init__(self, router: Router) -> None:
        super().__init__(router, "SpecialCharHandler")
    
    def process(self, context: WorkflowContext) -> bool:
        try:
            text: str = context.input_text
            original_text = text
            
            # Handle special characters - explicitly list characters to keep
            # This ensures consistent behavior across regex implementations
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\' -')
            processed_text = ''.join(c for c in text if c in allowed_chars)
            
            # Log what was removed
            removed_chars = set(original_text) - set(processed_text)
            if removed_chars:
                print(f"[SpecialCharHandler] Removed special characters: {removed_chars}")
                context.metadata['removed_chars'] = list(removed_chars)
            
            context.input_text = processed_text
            return True
        except Exception as e:
            context.add_error(f"Special character handling error: {str(e)}")
            return False

class TextProcessor(Agent):
    """Consolidated text processing agent that handles multiple processing steps"""
    
    def __init__(self, router: Router) -> None:
        super().__init__(router, "TextProcessor")
        self.special_char_handler = SpecialCharHandler(router)
    
    def process(self, context: WorkflowContext) -> bool:
        try:
            # Convert to lowercase
            text: str = context.input_text.lower()
            print(f"[TextProcessor] Converting to lowercase: {text}")
            
            # Handle special characters using dedicated agent
            context.input_text = text
            if not self.special_char_handler.process(context):
                return False
            text = context.input_text
            
            # Log removed characters if any
            if 'removed_chars' in context.metadata:
                print(f"[TextProcessor] Special characters were removed: {context.metadata['removed_chars']}")
            
            # Remove extra spaces
            text = ' '.join(text.split())
            print(f"[TextProcessor] Removed extra spaces: {text}")
            
            # Split into words
            words: List[str] = text.split()
            
            # Trim each word and handle special cases
            processed_words = []
            for word in words:
                original_word = word
                word = word.strip()
                # Remove leading/trailing punctuation
                word = word.strip("'\".,!?;:")
                if word != original_word:
                    print(f"[TextProcessor] Cleaned word: '{original_word}' -> '{word}'")
                if word:
                    processed_words.append(word)
            
            # Update context
            context.words = processed_words
            context.start_processing()
            
            return True
        except Exception as e:
            context.add_error(f"Text processing error: {str(e)}")
            return False
    
    def validate_output(self, context: WorkflowContext) -> bool:
        """Validate that words were properly processed"""
        if not context.words:
            context.add_error("No words found after processing")
            return False
        return True 