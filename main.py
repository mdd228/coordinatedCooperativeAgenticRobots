import threading
from typing import Optional, List
from flask import Flask, request, jsonify, render_template_string
from core.router import Router, MessageType, Message
from core.state import WorkflowContext
from agents.input.text_processor import TextProcessor, SpecialCharHandler
from agents.palindrome.detector import PalindromeDetector
from agents.output.formatter import OutputFormatter
import os

app = Flask(__name__)
router = Router()

# Store processing logs
processing_logs: List[str] = []

def log_message(message: str) -> None:
    """Add a message to the processing logs"""
    processing_logs.append(message)
    print(message)  # Also print to console for debugging

def create_agent(agent_class, name: str) -> None:
    """Create and log agent creation"""
    log_message(f"[System] Creating new agent: {name}")
    return agent_class(router)

def run_robot_a(router: Router, input_text: str) -> dict:
    """Run Robot A (main processing robot)"""
    context = WorkflowContext(input_text=input_text)
    
    # Create agents with explicit logging
    log_message("[System] Initializing Robot A's agents...")
    text_processor = create_agent(TextProcessor, "TextProcessor")
    special_char_handler = create_agent(SpecialCharHandler, "SpecialCharHandler")
    palindrome_detector = create_agent(PalindromeDetector, "PalindromeDetector")
    output_formatter = create_agent(OutputFormatter, "OutputFormatter")
    
    # Run pipeline
    log_message("[System] Starting text processing pipeline...")
    if not text_processor.process(context):
        return {"error": f"Text processing failed: {context.errors}"}
    
    if not palindrome_detector.run(context):
        return {"error": f"Palindrome detection failed: {context.errors}"}
    
    if not output_formatter.run(context):
        return {"error": f"Output formatting failed: {context.errors}"}
    
    return {
        "input_text": input_text,
        "palindromes": context.palindromes,
        "output": context.metadata.get('output', 'No output'),
        "errors": context.errors,
        "logs": processing_logs
    }

def run_robot_b(router: Router) -> None:
    """Run Robot B (verification robot)"""
    log_message("[System] Initializing Robot B...")
    while True:
        # Receive word
        word: Optional[Message] = router.subscribe("word_channel")
        if word is None or word.content == "STOP":
            break
        
        # Check if palindrome
        is_palindrome = word.content == word.content[::-1]
        log_message(f"[RobotB] Checking word: {word.content} -> {'is' if is_palindrome else 'is not'} a palindrome")
        
        # Send result
        router.publish("result_channel", MessageType.RESULT, is_palindrome, "RobotB")

@app.route('/check', methods=['POST'])
def check_palindrome():
    global processing_logs
    processing_logs = []  # Clear previous logs
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    input_text = data['text']
    log_message(f"[System] Processing input: {input_text}")
    
    # Create and start robots
    robot_a = threading.Thread(target=run_robot_a, args=(router, input_text))
    robot_b = threading.Thread(target=run_robot_b, args=(router,))
    
    robot_a.start()
    robot_b.start()
    
    # Wait for completion
    robot_a.join()
    router.publish("word_channel", MessageType.CONTROL, "STOP", "RobotA")
    robot_b.join()
    
    result = run_robot_a(router, input_text)
    return jsonify(result)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Multi-Agent Palindrome Detector</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    max-width: 1000px; 
                    margin: 0 auto; 
                    padding: 20px;
                    background-color: #f8f9fa;
                    color: #333;
                }
                .container {
                    background-color: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                .header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .header h1 {
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .header p {
                    color: #666;
                    font-size: 1.1em;
                }
                .input-section {
                    margin-bottom: 30px;
                }
                textarea { 
                    width: 100%; 
                    height: 120px; 
                    margin: 10px 0;
                    padding: 15px;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    font-size: 1.1em;
                    resize: vertical;
                }
                textarea:focus {
                    outline: none;
                    border-color: #007bff;
                    box-shadow: 0 0 0 3px rgba(0,123,255,0.25);
                }
                button { 
                    padding: 12px 24px; 
                    background: #007bff; 
                    color: white; 
                    border: none; 
                    cursor: pointer;
                    border-radius: 6px;
                    font-size: 1.1em;
                    transition: all 0.3s ease;
                }
                button:hover {
                    background: #0056b3;
                    transform: translateY(-1px);
                }
                button:disabled {
                    background: #ccc;
                    cursor: not-allowed;
                }
                .results-section {
                    margin-top: 30px;
                }
                #result { 
                    margin-top: 20px;
                    padding: 20px;
                    border-radius: 8px;
                }
                .error { 
                    color: #dc3545;
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                }
                .success { 
                    color: #28a745;
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                }
                .log-container {
                    margin-top: 30px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    max-height: 400px;
                    overflow-y: auto;
                }
                .log-container h3 {
                    color: #2c3e50;
                    margin-top: 0;
                }
                .log-entry {
                    margin: 8px 0;
                    padding: 8px;
                    border-bottom: 1px solid #e9ecef;
                    font-family: 'Consolas', monospace;
                }
                .agent-log {
                    color: #0056b3;
                    font-weight: bold;
                }
                .system-log {
                    color: #28a745;
                    font-weight: bold;
                }
                .robot-log {
                    color: #6f42c1;
                    font-weight: bold;
                }
                .agent-info {
                    background-color: #e9ecef;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .agent-info h3 {
                    color: #2c3e50;
                    margin-top: 0;
                }
                .agent-info ul {
                    list-style-type: none;
                    padding-left: 0;
                }
                .agent-info li {
                    margin: 5px 0;
                    padding: 5px 0;
                    border-bottom: 1px solid #dee2e6;
                }
                .loading {
                    display: none;
                    text-align: center;
                    margin: 20px 0;
                }
                .loading-spinner {
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #007bff;
                    border-radius: 50%;
                    width: 30px;
                    height: 30px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Multi-Agent Palindrome Detector</h1>
                    <p>Watch our intelligent agents work together to find palindromes in your text</p>
                </div>

                <div class="agent-info">
                    <h3>Our Agent Team:</h3>
                    <ul>
                        <li><strong>TextProcessor:</strong> Prepares and cleans the input text</li>
                        <li><strong>SpecialCharHandler:</strong> Manages special characters and punctuation</li>
                        <li><strong>PalindromeDetector:</strong> Identifies palindrome words</li>
                        <li><strong>OutputFormatter:</strong> Formats the results for display</li>
                    </ul>
                </div>

                <div class="input-section">
                    <textarea id="input" placeholder="Enter text to check for palindromes..."></textarea>
                    <button onclick="checkPalindrome()">Process Text</button>
                </div>
                
                <div class="loading" id="loading">
                    <div class="loading-spinner"></div>
                    <p>Agents are processing your text...</p>
                </div>

                <div id="result"></div>
                
                <div class="log-container">
                    <h3>Agent Activity Log:</h3>
                    <div id="logs"></div>
                </div>
            </div>
            
            <script>
                function formatLogEntry(log) {
                    if (log.includes('[System]')) {
                        return `<div class="log-entry"><span class="system-log">${log}</span></div>`;
                    } else if (log.includes('[Robot')) {
                        return `<div class="log-entry"><span class="robot-log">${log}</span></div>`;
                    } else {
                        return `<div class="log-entry"><span class="agent-log">${log}</span></div>`;
                    }
                }

                async function checkPalindrome() {
                    const button = document.querySelector('button');
                    const result = document.getElementById('result');
                    const logs = document.getElementById('logs');
                    const loading = document.getElementById('loading');
                    
                    try {
                        button.disabled = true;
                        result.innerHTML = '';
                        logs.innerHTML = '<div class="log-entry"><span class="system-log">Initializing agents...</span></div>';
                        loading.style.display = 'block';
                        
                        const text = document.getElementById('input').value;
                        const response = await fetch('/check', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ text })
                        });
                        
                        const data = await response.json();
                        
                        // Display logs with different styling based on log type
                        logs.innerHTML = data.logs.map(formatLogEntry).join('');
                        
                        if (data.error) {
                            result.innerHTML = `<div class="error">${data.error}</div>`;
                        } else {
                            result.innerHTML = `
                                <div class="success">
                                    <h3>Results:</h3>
                                    <p><strong>Input:</strong> ${data.input_text}</p>
                                    <p><strong>Palindromes found:</strong> ${data.palindromes.join(', ') || 'None'}</p>
                                    <p><strong>Output:</strong> ${data.output}</p>
                                </div>
                            `;
                        }
                    } catch (error) {
                        result.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                    } finally {
                        button.disabled = false;
                        loading.style.display = 'none';
                    }
                }
            </script>
        </body>
    </html>
    ''')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 