# Multi-Agent Palindrome Detector

A demonstration of multi-agent cooperation in text processing and palindrome detection.

## Features
- Real-time text processing
- Special character handling
- Palindrome detection
- Agent activity logging
- Interactive web interface

## How to Use
1. Enter text in the input box
2. Click "Process Text"
3. Watch the agents work together
4. View the results and processing log

## Agent Team
- **TextProcessor:** Prepares and cleans the input text
- **SpecialCharHandler:** Manages special characters and punctuation
- **PalindromeDetector:** Identifies palindrome words
- **OutputFormatter:** Formats the results for display

## Technical Details
- Built with Python and Gradio
- Multi-agent architecture
- Real-time processing
- Interactive logging

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Deployment

This application is configured for deployment on Railway. To deploy:

1. Create a Railway account at https://railway.app/
2. Install the Railway CLI
3. Run `railway login`
4. Run `railway up`

## Architecture

- **Robota**: Main processing robot that handles text input and coordinates the workflow
- **Roboto**: Verification robot that checks individual words for palindrome properties

## License

MIT
