
from data.models import AgentStateTranslation
from data.constants import GPT_5_MINI
from langchain_openai import ChatOpenAI

def translate_step(state: AgentStateTranslation) -> AgentStateTranslation:
    """Translate text"""
    
    # Initialize the OpenAI model and define the prompt
    llm = ChatOpenAI(model = GPT_5_MINI)
    prompt = f"Please translate from english to spanish: {state['summary']}"
    
    # Get the summary directly from the model
    result = llm.invoke([prompt])
    
    # Update the state with our summary
    return {
        "input_text": state["input_text"],  # Keep the original text
        "summary": state["summary"],  # Add the summary
        "translated_summary": result.content
    }