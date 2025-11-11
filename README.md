# EDUASSIST:AI - POWERED TEACHER’S KNOWLEDGE HUB

Teaching requires constant access to learning materials, lesson plans, and student progress records.
Many teachers face challenges in organizing resources, preparing personalized lessons, and keeping up with new educational methods.
Traditional methods rely on manual preparation, which is time-consuming and often lacks personalization.
AI can help by creating a centralized platform where teachers can access lesson templates, track students, and get intelligent suggestions.
EduAssist is designed as a digital knowledge hub that empowers teachers with AI-driven tools for content creation, assessment, and resource management.


#WORKFLOW PATH

/Teacher_AI_Hub/
|
|-- train_models.py             # Script to train the AI models
|-- run_chatbot_app.py          # Script to launch the chatbot website
|
|-- /data/
|   |-- lesson_plan_training.json
|   |-- quiz_training.json
|   |-- lesson_plan_validation.json
|   |-- quiz_validation.json
|
|-- /app/                         # The chatbot application code
|   |-- __init__.py
|   |-- routes.py
|   |-- teacher_ai_module.py
|   |-- /templates/
|   |   |-- index.html
|   |-- /static/
|       |-- style.css
|
|-- /trained_models/              # This will be created automatically by the training script
