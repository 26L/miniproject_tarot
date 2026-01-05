from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_llm_model():
    """
    Returns the configured LLM model instance.
    Uses Google Gemini via LangChain.
    """
    if not settings.GOOGLE_API_KEY:
        print("Warning: GOOGLE_API_KEY is not set. AI features will fail.")
        return None

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7,
        streaming=True
    )
    return llm
