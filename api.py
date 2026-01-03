from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv

from backend.agents import get_agent
from backend.pdf import process_pdf

load_dotenv()

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str
    provider: str
    model: str
    api_key: Optional[str] = None
    pdf_text: Optional[str] = ""

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Determine which API key to use
        env_key_map = {
            "Perplexity": "PERPLEXITY_API_KEY",
            "Groq": "GROQ_API_KEY",
            "OpenAI": "OPENAI_API_KEY"
        }
        api_key = request.api_key or os.getenv(env_key_map.get(request.provider, ""))
        
        if not api_key:
            raise HTTPException(status_code=400, detail=f"API Key for {request.provider} is missing.")

        agent = get_agent(request.provider, request.model, api_key, "main")
        
        prompt = request.message
        if request.pdf_text:
            prompt = f"PDF Context:\n{request.pdf_text}\n\nUser: {request.message}"
            
        response = agent.run(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        return {"role": "assistant", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-tasks")
async def extract_tasks(request: ChatRequest):
    try:
        env_key_map = {"Perplexity": "PERPLEXITY_API_KEY", "Groq": "GROQ_API_KEY", "OpenAI": "OPENAI_API_KEY"}
        api_key = request.api_key or os.getenv(env_key_map.get(request.provider, ""))
        
        if not api_key:
            return {"tasks": []}

        agent = get_agent(request.provider, request.model, api_key, "task")
        response = agent.run(f"Extract tasks from: {request.message}")
        content = response.content if hasattr(response, 'content') else str(response)
        
        tasks = []
        for line in content.split('\n'):
            if line.strip().startswith('- '):
                tasks.append(line.strip()[2:])
        
        return {"tasks": tasks}
    except Exception:
        return {"tasks": []}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = process_pdf(contents)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
