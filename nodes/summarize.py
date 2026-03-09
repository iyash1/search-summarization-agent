
from data.constants import GPT_5_MINI
from data.models import AgentState
from langchain_openai import ChatOpenAI

def summarize_step(state: AgentState) -> AgentState:
    """Create a concise summary of the input text."""
    
    # Initialize the OpenAI model and define the prompt
    llm = ChatOpenAI(model = GPT_5_MINI)
    prompt = f"Please summarize the following text in one sentence that captures the main points: {state['input_text']}"
    
    # Get the summary directly from the model
    result = llm.invoke([prompt])
    
    # Update the state with our summary
    return {
        "input_text": state["input_text"],  # Keep the original text
        "summary": result.content  # Add the summary
    }