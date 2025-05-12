from flask import Flask, send_from_directory, request, jsonify
from core.router import Router, MessageType, Message
from core.state import WorkflowContext
from agents.input.text_processor import TextProcessor, SpecialCharHandler
from agents.palindrome.detector import PalindromeDetector
from agents.output.formatter import OutputFormatter
import os

app = Flask(__name__, static_folder='static')
router = Router()

# Store processing logs
processing_logs = []

def log_message(message: str) -> None:
    """Add a message to the processing logs"""
    processing_logs.append(message)
    print(message)  # Also print to console for debugging

def create_agent(agent_class, name: str) -> None:
    """Create and log agent creation"""
    log_message(f"[System] Creating new agent: {name}")
    return agent_class(router)

def process_text(input_text: str) -> Dict[str, Any]:
    """Process text through the agent pipeline"""
    global processing_logs
    processing_logs = []  # Clear previous logs
    
    log_message(f"[System] Processing input: {input_text}")
    
    # Create and run Robot A
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

def format_output(result: Dict[str, Any]) -> str:
    """Format the result for display"""
    if "error" in result:
        return f"Error: {result['error']}"
    
    output = f"Input: {result['input_text']}\n\n"
    output += f"Palindromes found: {', '.join(result['palindromes']) if result['palindromes'] else 'None'}\n\n"
    output += f"Output: {result['output']}\n\n"
    output += "Processing Log:\n"
    output += "\n".join(result['logs'])
    
    return output

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

@app.route("/api/process", methods=["POST"])
def api_process():
    data = request.get_json()
    input_text = data.get("input_text", "")
    result = process_text(input_text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860) 