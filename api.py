from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from backend.agents import get_agent
from backend.pdf import process_pdf
from backend.paths import get_static_path

load_dotenv()

app = FastAPI()

# Resolve static path for bundling
static_path = str(get_static_path())

# Serve static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

class ChatRequest(BaseModel):
    message: str
    provider: str
    model: str
    api_key: Optional[str] = None
    pdf_text: Optional[str] = ""

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    return FileResponse(index_file)

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        env_key_map = {"Perplexity": "PERPLEXITY_API_KEY", "Groq": "GROQ_API_KEY", "OpenAI": "OPENAI_API_KEY"}
        api_key = request.api_key or os.getenv(env_key_map.get(request.provider, ""))
        
        if not api_key:
            raise HTTPException(status_code=400, detail=f"API Key for {request.provider} is missing.")

        agent = get_agent(request.provider, request.model, api_key, "main")
        prompt = f"PDF Context:\n{request.pdf_text}\n\nUser: {request.message}" if request.pdf_text else request.message
        response = agent.run(prompt)
        return {"role": "assistant", "content": response.content if hasattr(response, 'content') else str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-tasks")
async def extract_tasks(request: ChatRequest):
    try:
        env_key_map = {"Perplexity": "PERPLEXITY_API_KEY", "Groq": "GROQ_API_KEY", "OpenAI": "OPENAI_API_KEY"}
        api_key = request.api_key or os.getenv(env_key_map.get(request.provider, ""))
        if not api_key: return {"tasks": []}
        agent = get_agent(request.provider, request.model, api_key, "task")
        response = agent.run(f"Extract tasks from: {request.message}")
        content = response.content if hasattr(response, 'content') else str(response)
        tasks = [line.strip()[2:] for line in content.split('\n') if line.strip().startswith('- ')]
        return {"tasks": tasks}
    except Exception: return {"tasks": []}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = process_pdf(contents)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
