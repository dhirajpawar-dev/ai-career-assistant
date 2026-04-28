# AI Career Assistant 🤖

A full-stack AI-powered career planning web application that helps anyone plan and track their career journey — whether software engineering, government jobs, army, medicine, or any field.

## Live Demo
🚀 [View Live App](https://ai-career-assistant-ld5b.onrender.com)

## Features
- 🔐 **User Authentication** — Secure signup and login system
- 🎯 **Career Goal Setting** — Set any career goal and get an AI-generated roadmap
- 📋 **Progress Tracker** — Add tasks, mark them complete, track progress with a visual bar
- 💬 **AI Career Chat** — Chat with AI that remembers your goal and gives honest advice
- 🌍 **Universal** — Works for any career in any country — tech, government, army, medicine, finance

## Tech Stack
- **Python** — Core programming language
- **FastAPI** — High-performance backend web framework
- **HTML/CSS** — Frontend UI with custom dark theme design
- **JavaScript** — Interactive frontend functionality
- **SQLite** — Database for users, goals and progress tracking
- **Groq AI (LLaMA 3.3)** — AI-powered career roadmap and chat
- **bcrypt** — Secure password hashing
- **Jinja2** — HTML templating engine
- **Git & GitHub** — Version control

## Project Structure
ai-career-assistant/
├── static/
│   └── style.css        # Custom dark theme CSS
├── templates/
│   ├── login.html       # Login page
│   ├── signup.html      # Signup page
│   ├── dashboard.html   # Career goal and roadmap
│   ├── progress.html    # Progress tracker
│   └── chat.html        # AI career chat
├── main.py              # FastAPI backend and routes
├── database.py          # SQLite database functions
└── requirements.txt     # Python dependencies

## How to Run Locally
1. Clone the repository
git clone https://github.com/dhirajpawar-dev/ai-career-assistant.git
2. Install dependencies
pip install -r requirements.txt
3. Add your Groq API key in a `.env` file
GROQ_API_KEY=your_key_here
4. Run the app
uvicorn main:app --reload
5. Open browser at `http://127.0.0.1:8000`

## How It Works
1. User signs up and logs in
2. Sets a career goal — any field, any country
3. AI generates a realistic, honest roadmap with timeline
4. User tracks progress by adding and completing tasks
5. User chats with AI for personalized career advice
6. AI remembers the user's goal across all sessions

## Author
**Dhiraj Pawar**
- GitHub: [@dhirajpawar-dev](https://github.com/dhirajpawar-dev)
