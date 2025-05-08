import unittest
from io import StringIO
import sys
from main import run_robot_a
from core.router import Router
from core.state import WorkflowContext

class TestPalindromeSystem(unittest.TestCase):
    def setUp(self):
        self.router = Router()
        self.test_input = "Madam Arora teaches malayalam"
        self.expected_palindromes = ["madam", "arora", "malayalam"]
    
    def test_palindrome_detection(self):
        # Create context
        context = WorkflowContext(input_text=self.test_input)
        
        # Run Robot A
        run_robot_a(self.router, self.test_input)
        
        # Verify results
        self.assertTrue(context.palindromes)
        self.assertEqual(sorted(context.palindromes), sorted(self.expected_palindromes))
        
        # Verify output formatting
        self.assertIn('output', context.metadata)
        self.assertIn('processing_time', context.metadata)
        self.assertEqual(context.metadata['palindrome_count'], len(self.expected_palindromes))

if __name__ == '__main__':
    unittest.main() 