#!/usr/bin/env python3
import requests
import json

def test_backend_fix():
    """Test the backend with both 'message' and 'question' keys"""
    
    base_url = "http://localhost:5000"
    
    test_cases = [
        {
            "data": {"message": "Create a lesson plan for science"},
            "description": "Using 'message' key"
        },
        {
            "data": {"question": "Create a quiz for math"},
            "description": "Using 'question' key"
        },
        {
            "data": {"text": "This should fail"},
            "description": "Using wrong key (should fail)"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['description']}")
        print(f"   Data: {test_case['data']}")
        
        try:
            response = requests.post(
                f"{base_url}/ask",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result.get('response', 'No response')[:100]}...")
            else:
                error = response.json()
                print(f"   ❌ Error: {error.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")

if __name__ == "__main__":
    print("🔧 Testing backend fix for message/question key mismatch...")
    test_backend_fix()