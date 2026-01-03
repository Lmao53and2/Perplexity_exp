# Paramodus Anime.js Version

A high-performance, multi-agent AI productivity assistant built with **Agno v2.0**, **FastAPI**, and **Anime.js**.

## Refactored Architecture

The Streamlit frontend has been completely replaced with a custom web interface:
- **Backend**: FastAPI (`api.py`) serves as the REST API and static file host.
- **Frontend**: A custom HTML/JS interface located in `static/`.
- **Animations**: `anime.js` handles smooth UI transitions and message entry effects.
- **Core Logic**: Remains in the `backend/` package, fully decoupled from any specific UI framework.

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure your API keys in a `.env` file.
4. Start the server: `python api.py`.
5. Open your browser at `http://localhost:8000`.
