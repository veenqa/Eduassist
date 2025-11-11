import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import re
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeacherAI:
    def __init__(self, model_paths=None):
        self.models = {}
        self.tokenizers = {}
        
        # Default model paths if none provided
        if model_paths is None:
            model_paths = {
                'lesson_plan': 'trained_models/final_model_lesson_plan',
                'quiz': 'trained_models/final_model_quiz'
            }
        
        # Load both models
        for task_type, model_path in model_paths.items():
            if os.path.exists(model_path):
                logger.info(f"Loading model for '{task_type}' from {model_path}...")
                try:
                    self.tokenizers[task_type] = AutoTokenizer.from_pretrained(model_path)
                    self.tokenizers[task_type].pad_token = self.tokenizers[task_type].eos_token
                    self.models[task_type] = AutoModelForCausalLM.from_pretrained(model_path)
                    
                    # Check if CUDA is available
                    if torch.cuda.is_available():
                        self.models[task_type] = self.models[task_type].cuda()
                        logger.info(f"Using device: cuda")
                    
                    logger.info(f"✅ Model '{task_type}' loaded successfully.")
                except Exception as e:
                    logger.error(f"❌ Failed to load {task_type} model: {e}")
            else:
                logger.warning(f"⚠️ Model path {model_path} does not exist")
    
    def detect_intent(self, user_input):
        """Simple intent detection focused on 'His First Flight'"""
        user_input_lower = user_input.lower()
        
        # Check for lesson plan intent
        lesson_plan_indicators = ['lesson plan', 'lesson', 'plan', 'teaching', 'class', 'duration', 'minute']
        quiz_indicators = ['quiz', 'test', 'questions', 'assessment', 'exam', 'question']
        
        lesson_score = sum(1 for word in lesson_plan_indicators if word in user_input_lower)
        quiz_score = sum(1 for word in quiz_indicators if word in user_input_lower)
        
        # Force 'His First Flight' context
        if "his first flight" in user_input_lower:
            if lesson_score >= quiz_score:
                return 'lesson_plan'
            else:
                return 'quiz'
        
        # Default based on scores
        if lesson_score > quiz_score:
            return 'lesson_plan'
        elif quiz_score > lesson_score:
            return 'quiz'
        else:
            return 'ambiguous'
    
    def generate_lesson_plan_for_his_first_flight(self, duration="45 minutes", focus="character analysis"):
        """Generate a lesson plan specifically for 'His First Flight'"""
        
        base_plan = {
            "title": "Lesson Plan: His First Flight - Character Analysis",
            "duration": duration,
            "grade_level": "10th Grade",
            "subject": "English Literature",
            "topic": "His First Flight by Liam O'Flaherty",
            "focus": focus,
            "learning_objectives": [
                "Analyze the character development of the young seagull",
                "Understand the theme of overcoming fear and building confidence",
                "Identify literary devices used to portray character emotions",
                "Relate the story's themes to personal experiences of overcoming challenges"
            ],
            "materials_needed": [
                "Copies of 'His First Flight' story",
                "Whiteboard and markers",
                "Character analysis worksheets",
                "Projector for visual aids (optional)"
            ],
            "activities": [
                {
                    "time": "10 minutes",
                    "activity": "Introduction & Warm-up",
                    "description": "Discuss: 'Have you ever been afraid to try something new? How did you overcome your fear?'"
                },
                {
                    "time": "15 minutes",
                    "activity": "Guided Reading & Analysis",
                    "description": "Read key passages highlighting the seagull's fear, hesitation, and eventual courage. Focus on descriptive language."
                },
                {
                    "time": "10 minutes",
                    "activity": "Character Mapping",
                    "description": "Create a character trait chart showing how the seagull changes from beginning to end"
                },
                {
                    "time": "10 minutes",
                    "activity": "Group Discussion",
                    "description": "Discuss what motivated the seagull to finally fly and how hunger played a role"
                }
            ],
            "assessment": {
                "type": "Writing Assignment",
                "description": "Write a paragraph analyzing how the young seagull's character develops throughout the story, citing specific examples from the text."
            },
            "differentiation": {
                "for_struggling_learners": "Provide sentence starters for the writing assignment",
                "for_advanced_learners": "Research and compare with other coming-of-age stories about overcoming fear"
            }
        }
        
        # Customize based on focus
        if "theme" in focus.lower():
            base_plan["learning_objectives"][1] = "Analyze the central theme of courage versus fear in depth"
            base_plan["activities"][3]["description"] = "Group discussion on how the theme of courage is developed through the seagull's journey"
        elif "comprehension" in focus.lower():
            base_plan["activities"][1]["description"] = "Comprehension questions and vocabulary building from the text"
        
        return base_plan
    
    def generate_quiz_for_his_first_flight(self, difficulty="medium", question_count=5):
        """Generate a quiz specifically for 'His First Flight'"""
        
        # Base questions for His First Flight
        all_questions = [
            {
                "question": "Why was the young seagull afraid to fly?",
                "options": [
                    "He had injured wings",
                    "He lacked confidence and was scared of failing", 
                    "Other seagulls bullied him",
                    "The weather was too stormy"
                ],
                "correct_answer": "He lacked confidence and was scared of failing",
                "explanation": "The story emphasizes the seagull's fear and lack of confidence rather than physical limitations."
            },
            {
                "question": "What finally motivated the young seagull to fly?",
                "options": [
                    "His parents forced him to fly",
                    "He saw his family eating and became very hungry",
                    "Another bird showed him how to fly",
                    "A storm forced him to leave the ledge"
                ],
                "correct_answer": "He saw his family eating and became very hungry",
                "explanation": "Hunger was the primary motivation that overcame his fear."
            },
            {
                "question": "How did the young seagull feel after his first successful flight?",
                "options": [
                    "Still afraid and uncertain",
                    "Exhausted and tired",
                    "Proud, happy, and confident",
                    "Angry at his family for leaving him"
                ],
                "correct_answer": "Proud, happy, and confident",
                "explanation": "The story describes his joy and newfound confidence after successfully flying."
            },
            {
                "question": "What is the main theme of 'His First Flight'?",
                "options": [
                    "The importance of family relationships",
                    "Overcoming fear and gaining self-confidence",
                    "The beauty of nature and flying",
                    "The struggle for survival in the wild"
                ],
                "correct_answer": "Overcoming fear and gaining self-confidence",
                "explanation": "The central theme revolves around conquering fear and building self-confidence."
            },
            {
                "question": "How did the seagull's parents try to help him overcome his fear?",
                "options": [
                    "They brought him food regularly",
                    "They scolded and criticized him",
                    "They called to him encouragingly and demonstrated flying",
                    "They left him alone to figure it out himself"
                ],
                "correct_answer": "They called to him encouragingly and demonstrated flying",
                "explanation": "His parents used encouragement and demonstration rather than force."
            }
        ]
        
        # Select questions based on count
        selected_questions = all_questions[:min(question_count, len(all_questions))]
        
        quiz = {
            "title": "Comprehension Quiz: His First Flight",
            "difficulty": difficulty,
            "question_count": len(selected_questions),
            "instructions": "Read each question carefully and select the best answer.",
            "questions": selected_questions
        }
        
        return quiz
    
    def extract_parameters(self, user_input):
        """Extract parameters like duration, difficulty, question count from user input"""
        params = {}
        
        # Extract duration
        duration_match = re.search(r'(\d+)\s*min', user_input.lower())
        if duration_match:
            params['duration'] = f"{duration_match.group(1)} minutes"
        else:
            params['duration'] = "45 minutes"  # default
        
        # Extract difficulty
        if 'easy' in user_input.lower():
            params['difficulty'] = 'easy'
        elif 'hard' in user_input.lower() or 'difficult' in user_input.lower():
            params['difficulty'] = 'hard'
        else:
            params['difficulty'] = 'medium'  # default
        
        # Extract question count
        count_match = re.search(r'(\d+)\s*question', user_input.lower())
        if count_match:
            params['question_count'] = int(count_match.group(1))
        else:
            params['question_count'] = 5  # default
        
        # Extract focus
        if 'character' in user_input.lower() or 'analysis' in user_input.lower():
            params['focus'] = 'character analysis'
        elif 'theme' in user_input.lower():
            params['focus'] = 'theme analysis'
        elif 'comprehension' in user_input.lower():
            params['focus'] = 'reading comprehension'
        else:
            params['focus'] = 'character analysis'  # default
        
        return params
    
    def generate_response(self, user_input):
        """Main method to generate response - specialized for 'His First Flight'"""
        try:
            task_type = self.detect_intent(user_input)
            logger.info(f"🤖 Task identified: {task_type}")
            
            # Extract parameters
            params = self.extract_parameters(user_input)
            
            if task_type == 'ambiguous':
                return {
                    "success": False,
                    "message": "I can help you create lesson plans and quizzes for 'His First Flight'! Please specify what you'd like. Examples: 'Create a lesson plan for His First Flight' or 'Generate a quiz about His First Flight'"
                }
            
            # Use our specialized generators (not relying on models)
            if task_type == 'lesson_plan':
                content = self.generate_lesson_plan_for_his_first_flight(
                    duration=params['duration'],
                    focus=params['focus']
                )
            else:  # quiz
                content = self.generate_quiz_for_his_first_flight(
                    difficulty=params['difficulty'],
                    question_count=params['question_count']
                )
            
            return {
                "success": True,
                "task_type": task_type,
                "content": content,
                "note": "Generated using specialized template for 'His First Flight'"
            }
                
        except Exception as e:
            logger.error(f"❌ Error in generate_response: {e}")
            # Final fallback
            if 'quiz' in str(task_type) or 'quiz' in user_input.lower():
                content = self.generate_quiz_for_his_first_flight()
            else:
                content = self.generate_lesson_plan_for_his_first_flight()
            
            return {
                "success": True,
                "task_type": 'quiz' if 'quiz' in user_input.lower() else 'lesson_plan',
                "content": content,
                "note": "Generated using emergency fallback"
            }
    
    def format_response_for_display(self, response_data):
        """Format the response for nice display - CLEANED UP FORMATTING"""
        try:
            if not response_data.get("success", False):
                return response_data.get("message", "An error occurred.")
            
            content = response_data["content"]
            task_type = response_data["task_type"]
            
            if task_type == 'lesson_plan':
                return self._format_lesson_plan_clean(content)
            else:  # quiz
                return self._format_quiz_clean(content)
                
        except Exception as e:
            logger.error(f"❌ Error formatting response: {e}")
            return "Sorry, there was an error formatting the response. Please try again."
    
    def _format_lesson_plan_clean(self, data):
        """Clean, readable lesson plan formatting"""
        formatted = "📚 LESSON PLAN\n\n"
        formatted += f"Title: {data.get('title', 'Lesson Plan')}\n\n"
        formatted += f"Duration: {data.get('duration', '45 minutes')}\n"
        formatted += f"Grade Level: {data.get('grade_level', '10th Grade')}\n"
        formatted += f"Subject: {data.get('subject', 'English Literature')}\n"
        formatted += f"Topic: {data.get('topic', 'His First Flight')}\n"
        formatted += f"Focus: {data.get('focus', 'Character Analysis')}\n\n"
        
        formatted += "🎯 LEARNING OBJECTIVES:\n"
        for i, obj in enumerate(data.get('learning_objectives', []), 1):
            formatted += f"{i}. {obj}\n"
        formatted += "\n"
        
        formatted += "📦 MATERIALS NEEDED:\n"
        for material in data.get('materials_needed', []):
            formatted += f"• {material}\n"
        formatted += "\n"
        
        formatted += "🕒 ACTIVITIES:\n"
        for activity in data.get('activities', []):
            formatted += f"{activity.get('time', 'Time')} - {activity.get('activity', 'Activity')}:\n"
            formatted += f"  {activity.get('description', 'Description')}\n\n"
        
        if 'assessment' in data:
            formatted += "📝 ASSESSMENT:\n"
            formatted += f"{data['assessment'].get('type', 'Assessment')}:\n"
            formatted += f"{data['assessment'].get('description', 'Description')}\n\n"
        
        if 'differentiation' in data:
            formatted += "🎓 DIFFERENTIATION:\n"
            formatted += f"For struggling learners: {data['differentiation'].get('for_struggling_learners', 'N/A')}\n"
            formatted += f"For advanced learners: {data['differentiation'].get('for_advanced_learners', 'N/A')}\n"
        
        return formatted
    
    def _format_quiz_clean(self, data):
        """Clean, readable quiz formatting"""
        formatted = "📝 QUIZ\n\n"
        formatted += f"Title: {data.get('title', 'Quiz')}\n"
        formatted += f"Difficulty: {data.get('difficulty', 'Medium')}\n"
        formatted += f"Questions: {data.get('question_count', 'Multiple')}\n"
        formatted += f"Instructions: {data.get('instructions', 'Select the best answer for each question.')}\n\n"
        
        formatted += "=" * 50 + "\n\n"
        
        for i, question in enumerate(data.get('questions', []), 1):
            formatted += f"QUESTION {i}: {question.get('question', 'Question')}\n\n"
            
            options = question.get('options', [])
            for j, option in enumerate(options):
                formatted += f"  {chr(65+j)}) {option}\n"
            
            formatted += f"\n✅ ANSWER: {question.get('correct_answer', 'Answer')}\n"
            
            if question.get('explanation'):
                formatted += f"💡 EXPLANATION: {question['explanation']}\n"
            
            formatted += "\n" + "-" * 40 + "\n\n"
        
        return formatted

# Create a global instance
teacher_ai = TeacherAI()
