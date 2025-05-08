from core.agent import Agent
from core.state import WorkflowContext, WorkflowState
from core.router import Router, MessageType

class OutputFormatter(Agent):
    """Enhanced output formatter agent"""
    
    def __init__(self, router: Router) -> None:
        super().__init__(router, "OutputFormatter")
    
    def process(self, context: WorkflowContext) -> bool:
        try:
            if not context.palindromes:
                context.metadata['output'] = "No palindromes found"
                return True
            
            # Sort palindromes
            sorted_palindromes: list[str] = sorted(context.palindromes)
            
            # Join with commas
            formatted_output: str = ", ".join(sorted_palindromes)
            
            # Capitalize first letter of each word
            formatted_output = " ".join(word.capitalize() for word in formatted_output.split())
            
            # Add processing time
            processing_time: float = context.get_processing_time()
            formatted_output = f"{formatted_output} (Processed in {processing_time:.2f} seconds)"
            
            # Store in metadata
            context.metadata['output'] = formatted_output
            context.metadata['processing_time'] = processing_time
            context.metadata['palindrome_count'] = len(context.palindromes)
            
            # Mark as completed
            context.complete()
            
            return True
        except Exception as e:
            context.add_error(f"Output formatting error: {str(e)}")
            return False
    
    def validate_output(self, context: WorkflowContext) -> bool:
        """Validate that output formatting was successful"""
        if context.state != WorkflowState.COMPLETED:
            return False
        if 'output' not in context.metadata:
            return False
        return True 