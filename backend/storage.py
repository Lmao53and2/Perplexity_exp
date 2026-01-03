from agno.db.sqlite import SqliteDb
import os

def load_session_storage():
    """Load session-specific SQLite storage."""
    storage_path = os.getenv("AGENT_STORAGE_PATH", "business_agent.db")
    return SqliteDb(db_file=storage_path)

def load_personality_storage():
    """Load storage for personality analysis data."""
    storage_path = os.getenv("PERSONALITY_STORAGE_PATH", "personality_data.db")
    return SqliteDb(db_file=storage_path)

def load_task_storage():
    """Load storage for extracted tasks."""
    storage_path = os.getenv("TASK_STORAGE_PATH", "task_data.db")
    return SqliteDb(db_file=storage_path)
