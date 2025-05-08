import threading
import time
from typing import List, Type, Dict, Any
from queue import Queue, Empty

class Agent:
    """Base class for all agents"""
    def __init__(self, router=None):
        self.router = router

    def run(self, ctx):
        """Override this method in your agent implementation"""
        pass

class Robot(threading.Thread):
    """Base class for robots that process agents in sequence"""
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.context = {
            'start_time': time.time(),
            'words': [],
            'palindromes': [],
            'total_words': 0,
            'current_word_index': 0,
            'done': False
        }
        self.daemon = True  # Make thread daemon so it exits when main thread exits

    def run(self):
        try:
            # Preprocessing: first 6 agents
            for i, agent_class in enumerate(self.pipeline[:6]):
                agent = agent_class(self.router)
                print(f"[Robot] Running agent: {agent_class.__name__}")
                agent.run(self.context)
                print(f"[Robot] Context after {agent_class.__name__}: {self.context}")
                # Insert CheckPhrasePalindrome after RemoveSpaces (assume RemoveSpaces is at index 3)
                if i == 3:
                    from agents.CheckPhrasePalindrome import CheckPhrasePalindrome
                    print(f"[Robot] Running agent: CheckPhrasePalindrome")
                    CheckPhrasePalindrome(self.router).run(self.context)
                    print(f"[Robot] Context after CheckPhrasePalindrome: {self.context}")

            total_words = len(self.context['words'])
            self.context['total_words'] = total_words
            # For each word, run the main pipeline (SendWord, ReceiveResult, HasMoreWords)
            for i in range(total_words):
                self.context['current_word_index'] = i
                for agent_class in self.pipeline[6:9]:  # SendWord, ReceiveResult, HasMoreWords
                    agent = agent_class(self.router)
                    print(f"[Robot] Running agent: {agent_class.__name__}")
                    agent.run(self.context)
                    print(f"[Robot] Context after {agent_class.__name__}: {self.context}")

            # Postprocessing: the rest
            for agent_class in self.pipeline[9:]:
                agent = agent_class(self.router)
                print(f"[Robot] Running agent: {agent_class.__name__}")
                agent.run(self.context)
                print(f"[Robot] Context after {agent_class.__name__}: {self.context}")
        except Exception as e:
            print(f"Error in robot execution: {str(e)}")
            self.context['error'] = str(e)
            self.context['done'] = True

class Router:
    """Handles communication between robots using thread-safe queues for each channel."""
    def __init__(self):
        self.channels = {}
        self.lock = threading.Lock()

    def publish(self, channel, message):
        with self.lock:
            if channel not in self.channels:
                self.channels[channel] = Queue()
            self.channels[channel].put(message)

    def subscribe(self, channel, timeout=1):
        with self.lock:
            if channel not in self.channels:
                self.channels[channel] = Queue()
        try:
            return self.channels[channel].get(timeout=timeout)
        except Empty:
            return None 