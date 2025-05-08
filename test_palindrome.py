import sys
from io import StringIO
from main import main

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

if __name__ == "__main__":
    test_palindrome() 