from typing import Dict, Any, Optional
from queue import Queue, Empty
import threading
import time
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    WORD = "word"
    RESULT = "result"
    CONTROL = "control"
    ERROR = "error"

@dataclass
class Message:
    """Structured message with metadata"""
    type: MessageType
    content: Any
    sender: str
    timestamp: float = time.time()
    message_id: str = ""
    requires_ack: bool = True
    ack_received: bool = False

class Router:
    """Enhanced router with message validation and acknowledgment"""
    def __init__(self):
        self.channels: Dict[str, Queue] = {}
        self.ack_channels: Dict[str, Queue] = {}
        self.lock = threading.Lock()
        self.message_counter = 0
        
    def _get_next_message_id(self) -> str:
        """Generate unique message ID"""
        with self.lock:
            self.message_counter += 1
            return f"msg_{self.message_counter}"
    
    def publish(self, channel: str, message_type: MessageType, content: Any, 
                sender: str, requires_ack: bool = True) -> str:
        """Publish a message to a channel with acknowledgment"""
        with self.lock:
            if channel not in self.channels:
                self.channels[channel] = Queue()
                self.ack_channels[channel] = Queue()
            
            message = Message(
                type=message_type,
                content=content,
                sender=sender,
                message_id=self._get_next_message_id(),
                requires_ack=requires_ack
            )
            
            self.channels[channel].put(message)
            return message.message_id
    
    def subscribe(self, channel: str, timeout: float = 1.0) -> Optional[Message]:
        """Subscribe to a channel with timeout"""
        with self.lock:
            if channel not in self.channels:
                self.channels[channel] = Queue()
                self.ack_channels[channel] = Queue()
        
        try:
            message = self.channels[channel].get(timeout=timeout)
            if message.requires_ack:
                self._send_ack(channel, message.message_id)
            return message
        except Empty:
            return None
    
    def _send_ack(self, channel: str, message_id: str):
        """Send acknowledgment for a message"""
        self.ack_channels[channel].put(message_id)
    
    def wait_for_ack(self, channel: str, message_id: str, timeout: float = 1.0) -> bool:
        """Wait for acknowledgment of a message"""
        try:
            ack = self.ack_channels[channel].get(timeout=timeout)
            return ack == message_id
        except Empty:
            return False
    
    def clear_channel(self, channel: str):
        """Clear all messages from a channel"""
        with self.lock:
            if channel in self.channels:
                while not self.channels[channel].empty():
                    try:
                        self.channels[channel].get_nowait()
                    except Empty:
                        break 