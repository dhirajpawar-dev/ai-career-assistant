from starlette.responses import HTMLResponse
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from groq import Groq
from dotenv import load_dotenv
from database import init_db, signup_user, login_user, save_goal, get_goal, save_task, get_tasks, update_task, delete_task
import os
import uuid

load_dotenv()
init_db()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

sessions = {}

def get_user_from_session(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        return sessions[session_id]
    return None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = get_user_from_session(request)
    if user:
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})

@app.post("/signup")
async def signup(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if signup_user(name, email, password):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("signup.html", {"request": request, "error": "Email already exists!"})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = login_user(email, password)
    if user:
        session_id = str(uuid.uuid4())
        sessions[session_id] = user
        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie("session_id", session_id)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password!"})

@app.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]
    response = RedirectResponse("/")
    response.delete_cookie("session_id")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/")
    goal_data = get_goal(user["id"])
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_name": user["name"],
        "user_id": user["id"],
        "goal_data": goal_data
    })

@app.get("/progress", response_class=HTMLResponse)
async def progress_page(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/")
    tasks = get_tasks(user["id"])
    goal_data = get_goal(user["id"])
    total = len(tasks)
    completed = sum(1 for t in tasks if t[2])
    percentage = int((completed / total) * 100) if total > 0 else 0
    return templates.TemplateResponse("progress.html", {
        "request": request,
        "user_name": user["name"],
        "user_id": user["id"],
        "tasks": tasks,
        "percentage": percentage,
        "completed": completed,
        "total": total,
        "goal_data": goal_data
    })

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/")
    goal_data = get_goal(user["id"])
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "user_name": user["name"],
        "user_id": user["id"],
        "goal_data": goal_data
    })

@app.post("/generate-roadmap")
async def generate_roadmap(request: Request):
    user = get_user_from_session(request)
    if not user:
        raise HTTPException(status_code=401)
    data = await request.json()
    goal = data.get("goal")
    timeline = data.get("timeline")

    prompt = f"""
    You are an honest career advisor. A person wants to: {goal}
    Their timeline: {timeline}
    
    Create a realistic, honest career roadmap. Do NOT make false promises.
    If the timeline is too short, say so honestly and suggest a realistic one.
    
    Provide:
    1. Is this timeline realistic? (be honest)
    2. Step by step roadmap with months
    3. Required qualifications/skills
    4. Resources to learn (free and paid)
    5. Realistic salary/outcome expectations
    
    Format it clearly with sections and bullet points.
    Be specific to their country/region if mentioned.
    
    After the roadmap, add this exact section:
    
    TASKS:
    - Task 1 description
    - Task 2 description
    - Task 3 description
    (add 5-8 specific actionable tasks based on the roadmap)
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    full_response = response.choices[0].message.content
    
    # Split roadmap and tasks
    if "TASKS:" in full_response:
        parts = full_response.split("TASKS:")
        roadmap = parts[0].strip()
        tasks_text = parts[1].strip()
        
        # Parse tasks
        tasks = []
        for line in tasks_text.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                tasks.append(line[2:].strip())
        
        # Delete old tasks and save new ones
        conn = __import__('sqlite3').connect("career.db")
        c = conn.cursor()
        c.execute("DELETE FROM progress WHERE user_id = ?", (user["id"],))
        conn.commit()
        conn.close()
        
        for task in tasks:
            if task:
                save_task(user["id"], task)
    else:
        roadmap = full_response
        tasks = []
    
    save_goal(user["id"], goal, timeline, roadmap)
    return JSONResponse({"roadmap": roadmap, "tasks": tasks})

@app.post("/add-task")
async def add_task(request: Request):
    user = get_user_from_session(request)
    if not user:
        raise HTTPException(status_code=401)
    data = await request.json()
    task = data.get("task")
    save_task(user["id"], task)
    return JSONResponse({"success": True})

@app.post("/update-task")
async def update_task_route(request: Request):
    user = get_user_from_session(request)
    if not user:
        raise HTTPException(status_code=401)
    data = await request.json()
    update_task(data.get("task_id"), data.get("completed"))
    return JSONResponse({"success": True})

@app.post("/delete-task")
async def delete_task_route(request: Request):
    user = get_user_from_session(request)
    if not user:
        raise HTTPException(status_code=401)
    data = await request.json()
    delete_task(data.get("task_id"))
    return JSONResponse({"success": True})

@app.post("/chat-ai")
async def chat_ai(request: Request):
    user = get_user_from_session(request)
    if not user:
        raise HTTPException(status_code=401)
    data = await request.json()
    message = data.get("message")
    goal_data = get_goal(user["id"])

    context = ""
    if goal_data:
        context = f"The user's career goal is: {goal_data[0]}. Their timeline: {goal_data[1]}."

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"You are an honest career advisor. {context} Give realistic, honest advice. Never make false promises."},
            {"role": "user", "content": message}
        ]
    )
    answer = response.choices[0].message.content
    return JSONResponse({"answer": answer})