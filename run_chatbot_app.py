#!/usr/bin/env python3
import os
import sys
from app import app

def main():
    print("--- Initializing AI Assistant for the Web App ---")
    
    # Import and initialize the AI
    from app.teacher_ai_module import teacher_ai
    
    print("---------------------------------------------")
    print("🚀 Starting the Teacher AI Hub Chatbot Application...")
    print("🌍 Open your web browser and navigate to http://localhost:5000")
    print("---------------------------------------------")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()