from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import time

class WorkflowState(Enum):
    INITIALIZED = "initialized"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class WorkflowContext:
    """Enhanced context management for the workflow"""
    input_text: str
    words: List[str] = field(default_factory=list)
    palindromes: List[str] = field(default_factory=list)
    current_word: Optional[str] = None
    current_result: Optional[bool] = None
    state: WorkflowState = WorkflowState.INITIALIZED
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_error(self, error: str):
        """Add an error to the context and update state"""
        self.errors.append(error)
        self.state = WorkflowState.ERROR
        
    def complete(self):
        """Mark the workflow as completed"""
        self.end_time = time.time()
        self.state = WorkflowState.COMPLETED
        
    def start_processing(self):
        """Mark the workflow as processing"""
        self.state = WorkflowState.PROCESSING
        
    def is_valid(self) -> bool:
        """Validate the current state of the context"""
        if self.state == WorkflowState.ERROR:
            return False
        if not self.input_text and self.state != WorkflowState.INITIALIZED:
            return False
        return True
    
    def get_processing_time(self) -> float:
        """Get the total processing time"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time 