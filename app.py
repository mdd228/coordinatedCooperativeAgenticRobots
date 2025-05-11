import gradio as gr
from flask import Flask, request, jsonify
from core.router import Router, MessageType, Message
from core.state import WorkflowContext
from agents.input.text_processor import TextProcessor, SpecialCharHandler
from agents.palindrome.detector import PalindromeDetector
from agents.output.formatter import OutputFormatter
import threading
from typing import List, Dict, Any
import os

# Initialize Flask app
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

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="Multi-Agent Palindrome Detector") as interface:
        gr.Markdown("""
        # Multi-Agent Palindrome Detector
        Watch our intelligent agents work together to find palindromes in your text
        """)
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="Enter text to check for palindromes",
                    placeholder="Type your text here...",
                    lines=5
                )
                process_btn = gr.Button("Process Text")
            
            with gr.Column():
                output = gr.Textbox(
                    label="Results",
                    lines=10,
                    interactive=False
                )
        
        process_btn.click(
            fn=process_text,
            inputs=input_text,
            outputs=output,
            postprocess=format_output
        )
        
        gr.Markdown("""
        ## Our Agent Team:
        - **TextProcessor:** Prepares and cleans the input text
        - **SpecialCharHandler:** Manages special characters and punctuation
        - **PalindromeDetector:** Identifies palindrome words
        - **OutputFormatter:** Formats the results for display
        """)
    
    return interface

# Create and launch the interface
interface = create_interface()
interface.launch(server_name="0.0.0.0", server_port=7860) 