import sys
from io import StringIO
from main import main
import unittest
from core.router import Router
from core.state import WorkflowContext
from agents.input.text_processor import TextProcessor

def test_palindrome():
    # Test with a known palindrome sentence
    test_input = "Madam Arora teaches malayalam"
    print("Testing with input:", test_input)
    
    # Redirect stdin to provide test input
    sys.stdin = StringIO(test_input + "\n")
    
    # Run the main function
    main()
    
    # Restore stdin
    sys.stdin = sys.__stdin__

class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.router = Router()
        self.processor = TextProcessor(self.router)
        self.context = WorkflowContext()

    def test_special_characters(self):
        test_cases = [
            ("Hello?", ["hello"]),
            ("What's up?", ["whats", "up"]),
            ("Don't! Stop!", ["dont", "stop"]),
            ("Test-case", ["test-case"]),
            ("Multiple...spaces", ["multiple", "spaces"]),
            ("Question? Mark!", ["question", "mark"]),
            ("'Quoted' word", ["quoted", "word"]),
            ("Mixed-case!?", ["mixedcase"]),
            ("End with...", ["end", "with"]),
            ("Start with...text", ["start", "with", "text"])
        ]

        for input_text, expected_words in test_cases:
            with self.subTest(input_text=input_text):
                self.context.input_text = input_text
                success = self.processor.process(self.context)
                self.assertTrue(success, f"Processing failed for: {input_text}")
                self.assertEqual(
                    self.context.words,
                    expected_words,
                    f"Expected {expected_words} but got {self.context.words} for input: {input_text}"
                )

if __name__ == "__main__":
    test_palindrome()
    unittest.main() 