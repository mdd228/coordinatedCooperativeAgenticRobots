import threading
from typing import Optional
from core.router import Router, MessageType, Message
from core.state import WorkflowContext
from agents.input.text_processor import TextProcessor
from agents.palindrome.detector import PalindromeDetector
from agents.output.formatter import OutputFormatter

def run_robot_a(router: Router, input_text: str) -> None:
    """Run Robot A (main processing robot)"""
    context = WorkflowContext(input_text=input_text)
    
    # Create agents
    text_processor = TextProcessor(router)
    palindrome_detector = PalindromeDetector(router)
    output_formatter = OutputFormatter(router)
    
    # Run pipeline
    if not text_processor.run(context):
        print(f"Text processing failed: {context.errors}")
        return
    
    if not palindrome_detector.run(context):
        print(f"Palindrome detection failed: {context.errors}")
        return
    
    if not output_formatter.run(context):
        print(f"Output formatting failed: {context.errors}")
        return
    
    # Print results
    print("\nResults:")
    print(f"Input text: {input_text}")
    print(f"Found palindromes: {context.palindromes}")
    print(f"Output: {context.metadata.get('output', 'No output')}")
    if context.errors:
        print("\nErrors encountered:")
        for error in context.errors:
            print(f"- {error}")

def run_robot_b(router: Router) -> None:
    """Run Robot B (verification robot)"""
    while True:
        # Receive word
        word: Optional[Message] = router.subscribe("word_channel")
        if word is None or word.content == "STOP":
            break
        
        # Check if palindrome
        is_palindrome = word.content == word.content[::-1]
        
        # Send result
        router.publish("result_channel", MessageType.RESULT, is_palindrome, "RobotB")

def main() -> None:
    # Create router
    router = Router()
    
    # Get input text
    input_text = input("Enter text to check for palindromes: ")
    
    # Create and start robots
    robot_a = threading.Thread(target=run_robot_a, args=(router, input_text))
    robot_b = threading.Thread(target=run_robot_b, args=(router,))
    
    robot_a.start()
    robot_b.start()
    
    # Wait for completion
    robot_a.join()
    router.publish("word_channel", MessageType.CONTROL, "STOP", "RobotA")
    robot_b.join()

if __name__ == "__main__":
    main() 