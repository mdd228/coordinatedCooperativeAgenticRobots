def is_palindrome(word: str) -> bool:
    """Check if a word is a palindrome."""
    # Remove spaces and convert to lowercase
    word = word.lower().replace(" ", "")
    return word == word[::-1]

def find_palindromes(text: str) -> list[str]:
    """Find all palindromes in the given text."""
    # Split into words and clean them
    words = text.lower().split()
    words = [word.strip('.,!?') for word in words]
    
    # Find palindromes
    palindromes = [word for word in words if is_palindrome(word)]
    return sorted(palindromes)

def format_output(palindromes: list[str], processing_time: float) -> str:
    """Format the output with palindromes and processing time."""
    if not palindromes:
        return "No palindromes found"
    
    # Capitalize first letter of each word
    formatted = ", ".join(word.capitalize() for word in palindromes)
    return f"{formatted} (Processed in {processing_time:.2f} seconds)"

def main():
    import time
    
    # Get input
    text = input("Enter text to check for palindromes: ")
    
    # Process
    start_time = time.time()
    palindromes = find_palindromes(text)
    processing_time = time.time() - start_time
    
    # Format and display results
    result = format_output(palindromes, processing_time)
    
    print("\nResults:")
    print(f"Input text: {text}")
    print(f"Found palindromes: {palindromes}")
    print(f"Output: {result}")

if __name__ == "__main__":
    main() 