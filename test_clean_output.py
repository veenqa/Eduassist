#!/usr/bin/env python3
from app.teacher_ai_module import teacher_ai

def test_clean_output():
    print("🧪 Testing Clean Output Formatting...")
    
    test_queries = [
        "Create a quiz about His First Flight",
        "Generate a 5-question quiz for His First Flight",
        "Create a lesson plan for His First Flight",
        "Make a 45-minute lesson plan focusing on character analysis"
    ]
    
    for query in test_queries:
        print(f"\n" + "="*70)
        print(f"👤 User: {query}")
        print("="*70)
        
        response = teacher_ai.generate_response(query)
        
        if response.get("success"):
            formatted = teacher_ai.format_response_for_display(response)
            print(f"🤖 Assistant Response:")
            print(formatted)
            print("\n" + "="*70)
        else:
            print(f"❌ Error: {response.get('message')}")
    
    print("\n✅ Clean output testing complete!")

if __name__ == "__main__":
    test_clean_output()