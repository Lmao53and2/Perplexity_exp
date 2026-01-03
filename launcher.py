import uvicorn
import webbrowser
import threading
import time
from api import app

def open_browser():
    """Wait for server to start, then open the browser."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    # Start browser-opener thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run FastAPI server
    print("🚀 Starting Paramodus Desktop...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
