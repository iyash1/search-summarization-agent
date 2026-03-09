
from data.constants import GPT_5_MINI
from data.models import AgentStateSentiment
from langchain_openai import ChatOpenAI

def analyze_sentiment_step(state: AgentStateSentiment) -> AgentStateSentiment:
    """Analyze the sentiment of the input text."""
    
    # Initialize the OpenAI model and define the prompt
    llm = ChatOpenAI(model = GPT_5_MINI)
    prompt = f"Please analyze the sentiment of the following text and return it as positive, negative, or neutral: {state['summary']}"
    
    # Get the sentiment directly from the model
    result = llm.invoke([prompt])
    
    # Update the state with our sentiment analysis
    return {
        "input_text": state["input_text"],  # Keep the original text
        "summary": state["summary"],  # Keep the existing summary
        "sentiment": result.content  # Add the sentiment analysis
    }