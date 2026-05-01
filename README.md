# AI Career Assistant 🤖

A full-stack AI-powered career planning web application that helps anyone plan and track their career journey — whether software engineering, government jobs, army, medicine, chartered accountancy, or any field in any country.

## Live Demo
🚀 [View Live App](https://ai-career-assistant-ld5b.onrender.com)

## Features
- 🔐 **User Authentication** — Secure signup and login with persistent sessions (stays logged in for 7 days)
- 🎯 **Universal Career Goal Setting** — Set any career goal in any field and get an AI-generated realistic roadmap
- 📋 **Auto-Generated Tasks** — AI automatically creates actionable tasks in your progress tracker from the roadmap
- ✅ **Progress Tracker** — Add tasks, mark them complete, track progress with a visual progress bar
- 🤖 **AI Progress Review** — Get honest AI feedback on your completed vs pending tasks with next steps
- 💬 **Career Chat with Memory** — Chat with AI that remembers your goal and saves full conversation history
- 🌍 **Universal** — Works for any career in any country — tech, government, army, medicine, finance, arts

## Tech Stack
- **Python** — Core programming language
- **FastAPI** — High-performance backend web framework
- **HTML/CSS** — Frontend UI with custom dark theme design
- **JavaScript** — Interactive frontend functionality (fetch API, DOM manipulation)
- **SQLite** — Database for users, goals, progress and chat history
- **Groq AI (LLaMA 3.3 70B)** — AI-powered career roadmap generation and chat
- **bcrypt** — Secure password hashing
- **itsdangerous** — Secure cookie-based session management
- **Jinja2** — Server-side HTML templating engine
- **Git & GitHub** — Version control and deployment

## Project Structure
ai-career-assistant/
├── static/
│   └── style.css          # Custom dark theme CSS (380+ lines)
├── templates/
│   ├── login.html         # Login page with show/hide password
│   ├── signup.html        # Signup page
│   ├── dashboard.html     # Career goal setting and roadmap display
│   ├── progress.html      # Progress tracker with AI review
│   └── chat.html          # AI career chat with history
├── main.py                # FastAPI backend — all routes and API calls
├── database.py            # SQLite database — all CRUD operations
└── requirements.txt       # Python dependencies

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Goals table
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal TEXT NOT NULL,
    timeline TEXT,
    roadmap TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Progress/Tasks table
CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Chat history table
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Architecture & Data Flow
User sets career goal + timeline
↓
FastAPI backend receives request
↓
Groq AI (LLaMA 3.3) generates realistic roadmap
↓
AI automatically extracts 5-8 actionable tasks
↓
Tasks saved to SQLite database
↓
User tracks progress → AI reviews and gives feedback
↓
All chat history saved and loaded on every session

## How the AI Works

**Roadmap Generation:**
- User inputs goal (e.g. "I want to become a software engineer") and timeline
- System sends structured prompt to Groq AI with honesty instructions
- AI generates roadmap AND a TASKS section with 5-8 specific actions
- Backend parses the TASKS section using regex and saves each task to database
- User sees roadmap + auto-populated progress tracker immediately

**AI Prompt Design:**
You are an honest career advisor. Do NOT make false promises.
If timeline is too short, say so honestly.
Provide: realistic assessment, step-by-step roadmap,
required qualifications, resources, salary expectations.
After roadmap add TASKS: section with 5-8 actionable items.

**Progress Review:**
- System fetches all tasks (completed + pending) from database
- Sends structured data to AI with completion statistics
- AI gives honest assessment, top 3 priorities, encouraging message
- Maximum 150 words — concise and actionable

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Login page |
| GET | `/signup` | Signup page |
| POST | `/login` | Authenticate user, set session cookie |
| POST | `/signup` | Create new user account |
| GET | `/dashboard` | Career goal and roadmap page |
| GET | `/progress` | Progress tracker page |
| GET | `/chat` | AI chat page with history |
| POST | `/generate-roadmap` | Generate AI roadmap + auto-create tasks |
| POST | `/add-task` | Add manual task |
| POST | `/update-task` | Mark task complete/incomplete |
| POST | `/delete-task` | Delete a task |
| POST | `/chat-ai` | Send message to AI, save history |
| POST | `/review-progress` | Get AI progress review |
| POST | `/clear-chat` | Clear chat history |
| GET | `/logout` | Clear session cookie |

## Security Features
- Passwords hashed with **bcrypt** (industry standard)
- Sessions stored as **signed cookies** using itsdangerous — cannot be tampered with
- API keys stored as **environment variables** — never in code
- `.env` and `career.db` excluded from GitHub via `.gitignore`
- Session expires after **7 days** automatically

## How to Run Locally
1. Clone the repository
git clone https://github.com/dhirajpawar-dev/ai-career-assistant.git
2. Install dependencies
pip install -r requirements.txt
3. Add your Groq API key in a `.env` file
GROQ_API_KEY=your_key_here
SECRET_KEY=any-random-string-here
4. Run the app
uvicorn main:app --reload
5. Open browser at `http://127.0.0.1:8000`

## Use Cases
- **Students** — Plan career path after graduation with realistic timelines
- **Career changers** — Get honest roadmap for switching fields
- **Job seekers** — Track preparation progress with AI accountability
- **Anyone** — Works for any career — tech, government, military, medicine, finance, arts

## Dataset Limitations & Honest Notes
- AI advice is generated by LLaMA 3.3 70B — always verify with official sources
- Career timelines are estimates — actual time may vary based on individual effort
- Salary figures mentioned are approximate market averages
- Government/military job advice may not reflect latest exam patterns

## Author
**Dhiraj Pawar**
- GitHub: [@dhirajpawar-dev](https://github.com/dhirajpawar-dev)
- Live App: [AI Career Assistant](https://ai-career-assistant-ld5b.onrender.com)