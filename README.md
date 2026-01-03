# Paramodus Decoupled

A high-performance, multi-agent AI productivity assistant built with **Agno v2.0**. This version has been refactored to separate the core agentic backend from the Streamlit frontend.

## Architecture

- **`backend/`**: Contains the core logic.
    - `agents.py`: Agent factory and model management.
    - `storage.py`: SQLite database persistence logic.
    - `pdf.py`: Isolated PDF context processing.
- **`app.py`**: The Streamlit frontend, now simplified to handle UI and session state while delegating AI logic to the `backend` package.

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure your API keys in a `.env` file (see `.env.example`).
4. Run the app: `streamlit run app.py`.
