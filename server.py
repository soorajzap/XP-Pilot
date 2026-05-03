from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent_app
import uuid

app = FastAPI()


class AppState:
    def __init__(self):
        self.latest_session_id = None
        self.sessions = {}
        self.skills = {
            "total_fixes": 0,
            "xp": 0,
            "categories": {
                "SyntaxError": 0,
                "TypeError": 0,
                "NameError": 0,
                "LogicError": 0
            }
        }

state = AppState()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FixRequest(BaseModel):
    file_path: str
    code: str
    error: str

@app.get("/latest-session")
async def get_latest():
    return {"session_id": state.latest_session_id}

@app.get("/skills")
async def get_skills():
    return state.skills

@app.post("/trigger-fix")
async def trigger_fix(request: FixRequest, background_tasks: BackgroundTasks):
    session_id = str(uuid.uuid4())
    state.latest_session_id = session_id
    
    state.sessions[session_id] = {
        "status": "Processing",
        "original_code": request.code,
        "fixed_code": "",
        "error": request.error,
        "logs": ["Agent initialized...", "Analyzing error patterns..."]
    }
    
    background_tasks.add_task(run_agent_logic, session_id, request)
    return {"session_id": session_id}

async def run_agent_logic(session_id, request):
    initial_state = {
        "file_path": request.file_path,
        "code": request.code,
        "error": request.error,
        "attempts": 0,
        "is_fixed": False
    }
    
    result = agent_app.invoke(initial_state)
    
    if session_id in state.sessions:
        state.sessions[session_id].update({
            "fixed_code": result.get("code", ""),
            "status": "Ready for Review",
            "logs": state.sessions[session_id]["logs"] + ["Fix generated successfully."]
        })

        # Update Skill Tracking Logic
        state.skills["total_fixes"] += 1
        state.skills["xp"] += 15  
        
        # Parse error type for analytics
        error_name = request.error.split(':')[0]
        if error_name in state.skills["categories"]:
            state.skills["categories"][error_name] += 1
        else:
            state.skills["categories"]["LogicError"] += 1

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    return state.sessions.get(session_id)