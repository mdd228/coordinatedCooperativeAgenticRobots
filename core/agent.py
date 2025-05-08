from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from .state import WorkflowContext
from .router import Router, MessageType
import time

class Agent(ABC):
    """Enhanced base class for all agents with better error handling and validation"""
    
    def __init__(self, router: Router, name: str):
        self.router = router
        self.name = name
        self.retry_count = 0
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds
    
    @abstractmethod
    def process(self, context: WorkflowContext) -> bool:
        """Process the current context. Return True if successful, False otherwise."""
        pass
    
    def validate_input(self, context: WorkflowContext) -> bool:
        """Validate input context. Override in subclasses if needed."""
        return context.is_valid()
    
    def validate_output(self, context: WorkflowContext) -> bool:
        """Validate output context. Override in subclasses if needed."""
        return context.is_valid()
    
    def run(self, context: WorkflowContext) -> bool:
        """Run the agent with retry logic and error handling"""
        if not self.validate_input(context):
            context.add_error(f"{self.name}: Invalid input context")
            return False
        
        while self.retry_count < self.max_retries:
            try:
                success = self.process(context)
                if success and self.validate_output(context):
                    return True
                
                self.retry_count += 1
                if self.retry_count < self.max_retries:
                    time.sleep(self.retry_delay)
            except Exception as e:
                context.add_error(f"{self.name}: {str(e)}")
                self.retry_count += 1
                if self.retry_count < self.max_retries:
                    time.sleep(self.retry_delay)
        
        return False
    
    def send_message(self, channel: str, message_type: MessageType, 
                    content: Any, requires_ack: bool = True) -> Optional[str]:
        """Send a message with acknowledgment"""
        return self.router.publish(channel, message_type, content, 
                                 self.name, requires_ack)
    
    def receive_message(self, channel: str, timeout: float = 1.0) -> Optional[Any]:
        """Receive a message with timeout"""
        message = self.router.subscribe(channel, timeout)
        return message.content if message else None 