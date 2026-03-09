from data.models import AgentStateSentiment

# LangGraph imports (Updated based on recent versions)
from langgraph.graph import StateGraph

from nodes.summarize import summarize_step
from nodes.sentiment import analyze_sentiment_step

# --------------------------------
# Workflow to summarize and analyze sentiment
# --------------------------------
def workflow_summarize_and_analyze_sentiment(input_text: str):
    # Let's define a stategraph with the "AgentState" we defined earlier
    workflow = StateGraph(AgentStateSentiment)

    # Let's add a node, which is the summarize function we defined before
    workflow.add_node("summarize", summarize_step)

    # Let's define Edges, which define how data flows between nodes
    workflow.add_edge("summarize", "sentiment") 
    workflow.add_node("sentiment", analyze_sentiment_step)
    workflow.set_entry_point("summarize")

    # Let's compile the graph
    graph = workflow.compile() 

    # Set up the initial state with the input text
    initial_state = {
            "input_text": input_text,
            "summary": "",
            "sentiment": ""}

    # Run the graph
    result = graph.invoke(initial_state)

    # Get the summary and sentiment from the result
    summary = result["summary"]
    sentiment = result["sentiment"]

    # Print the results with clear labels and spacing
    print(f"=== Generated Summary ===")
    print(summary)

    print("\n=== Sentiment Analysis ===")
    print(sentiment)

