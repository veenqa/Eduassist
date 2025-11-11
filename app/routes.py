from flask import render_template, request, jsonify
import logging
from app import app
from app.teacher_ai_module import teacher_ai

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        
        # Accept both 'message' and 'question' keys
        user_input = ""
        if data:
            user_input = data.get('message', '').strip() or data.get('question', '').strip()
        
        logger.info(f"User input: '{user_input}'")
        
        if not user_input:
            return jsonify({"error": "Please enter a message."}), 400
        
        # Generate response
        response_data = teacher_ai.generate_response(user_input)
        
        if not response_data.get("success", False):
            error_msg = response_data.get("message", "Unknown error occurred")
            return jsonify({"error": error_msg}), 400
        
        # Format the response for display
        formatted_response = teacher_ai.format_response_for_display(response_data)
        
        # Add note if it's a fallback response
        final_response = formatted_response
        if response_data.get("note"):
            final_response = f"📝 {response_data['note']}\n\n{formatted_response}"
        
        logger.info("✅ Successfully generated response")
        return jsonify({"response": final_response})
        
    except Exception as e:
        logger.error(f"Error in /ask route: {e}")
        return jsonify({"error": "An internal server error occurred. Please try again."}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "EDUASSIST for 'His First Flight' is running"})