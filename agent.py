import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI # Changed to Gemini
from tools import run_python_file

# 1. Load the environment variables FIRST
load_dotenv()

class AgentState(TypedDict):
    file_path: str
    code: str
    error: str
    attempts: int
    is_fixed: bool

# 2. Initialize Gemini (This will now find your GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def fixer_node(state: AgentState):
    print(f"\n--- ATTEMPT {state['attempts'] + 1}: FIXING CODE ---")
    
    prompt = f"""
    You are an expert Python developer. Fix the bug in this code.
    Return ONLY the raw python code. Do not include markdown formatting like ```python.
    
    Error: {state['error']}
    Current Code:
    {state['code']}
    """
    response = llm.invoke(prompt)
    
    # Cleaning the response to ensure it's just pure code
    clean_code = response.content.strip().replace("```python", "").replace("```", "")
    
    return {
        "code": clean_code,
        "attempts": state['attempts'] + 1
    }

def verifier_node(state: AgentState):
    # Save the agent's attempt to the file
    with open(state['file_path'], 'w') as f:
        f.write(state['code'])
    
    # Run the file using our tool
    success, output = run_python_file(state['file_path'])
    
    if success:
        print("✅ Code Passed!")
    else:
        print(f"❌ Still Broken: {output.strip()}")
        
    return {
        "is_fixed": success,
        "error": output if not success else ""
    }

# --- Graph Construction ---
workflow = StateGraph(AgentState)
workflow.add_node("fix_code", fixer_node)
workflow.add_node("verify_code", verifier_node)

workflow.set_entry_point("fix_code")
workflow.add_edge("fix_code", "verify_code")

def router(state: AgentState):
    if state["is_fixed"] or state["attempts"] >= 3:
        return END
    return "fix_code"

workflow.add_conditional_edges("verify_code", router)
agent_app = workflow.compile()