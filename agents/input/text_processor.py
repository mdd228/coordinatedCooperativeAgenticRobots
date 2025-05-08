import re
from typing import List
from core.agent import Agent
from core.state import WorkflowContext
from core.router import Router, MessageType

class TextProcessor(Agent):
    """Consolidated text processing agent that handles multiple processing steps"""
    
    def __init__(self, router: Router) -> None:
        super().__init__(router, "TextProcessor")
    
    def process(self, context: WorkflowContext) -> bool:
        try:
            # Convert to lowercase
            text: str = context.input_text.lower()
            
            # Remove punctuation
            text = re.sub(r'[^\w\s]', '', text)
            
            # Remove extra spaces
            text = ' '.join(text.split())
            
            # Split into words
            words: List[str] = text.split()
            
            # Trim each word
            words = [word.strip() for word in words]
            
            # Filter out empty words
            words = [word for word in words if word]
            
            # Update context
            context.words = words
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