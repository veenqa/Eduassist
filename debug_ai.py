#!/usr/bin/env python3
import sys
import os
import logging

# Add the app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def test_ai_directly():
    print("🧪 Testing AI module directly...")
    
    try:
        from teacher_ai_module import teacher_ai
        
        test_queries = [
            "Generate a 5-question, medium-difficulty quiz for 'His First Flight'",
            "Create a lesson plan",
            "test"
        ]
        
        for query in test_queries:
            print(f"\n" + "="*60)
            print(f"Testing: '{query}'")
            
            response = teacher_ai.generate_response(query)
            print(f"Response: {response}")
            
            if response.get("success"):
                formatted = teacher_ai.format_response_for_display(response)
                print(f"Formatted: {formatted}")
            else:
                print(f"ERROR: {response.get('message')}")
                
    except Exception as e:
        print(f"❌ Failed to test AI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_directly()