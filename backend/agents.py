from agno.agent import Agent
from agno.models.perplexity import Perplexity
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from .storage import load_session_storage, load_personality_storage, load_task_storage

def get_model(provider_name, model_name, api_key):
    """Model factory to return appropriate Agno model instance."""
    if provider_name == "Perplexity":
        return Perplexity(id=model_name, api_key=api_key)
    elif provider_name == "Groq":
        return Groq(id=model_name, api_key=api_key)
    return OpenAIChat(id=model_name, api_key=api_key)

def get_agent(provider_name, model_name, api_key, agent_role):
    """Agent factory to return configured Agno agents based on roles."""
    model = get_model(provider_name, model_name, api_key)
    
    if agent_role == "personality":
        return Agent(
            model=model,
            db=load_personality_storage(),
            instructions="Analyze the user's personality based on the chat. Be concise. Use Markdown.",
            markdown=True
        )
    elif agent_role == "task":
        return Agent(
            model=model,
            db=load_task_storage(),
            instructions="Extract actionable tasks from the conversation. Return only a markdown list starting with '- '.",
            markdown=True
        )
    else:
        return Agent(
            model=model,
            db=load_session_storage(),
            instructions="You are Paramodus, a helpful AI assistant. Answer accurately. Use LaTeX for math: $inline$ and $$block$$.",
            markdown=True
        )
