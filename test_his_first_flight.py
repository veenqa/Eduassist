#!/usr/bin/env python3
from app.teacher_ai_module import teacher_ai

def test_his_first_flight():
    print("🧪 Testing EDUASSIST for 'His First Flight'...")
    
    test_queries = [
        "Create a 45-minute lesson plan for 'His First Flight' focusing on character analysis",
        "Generate a 5-question, medium-difficulty quiz for 'His First Flight'",
        "Make me a lesson plan for His First Flight",
        "Create a quiz about His First Flight",
        "I need a lesson plan for character analysis in His First Flight"
    ]
    
    for query in test_queries:
        print(f"\n" + "="*70)
        print(f"👤 User: {query}")
        
        response = teacher_ai.generate_response(query)
        
        if response.get("success"):
            formatted = teacher_ai.format_response_for_display(response)
            print(f"🤖 Assistant:")
            print(formatted)
        else:
            print(f"❌ Error: {response.get('message')}")
    
    print("\n" + "="*70)
    print("✅ Testing complete! Your EDUASSIST is ready for 'His First Flight'!")

if __name__ == "__main__":
    test_his_first_flight()