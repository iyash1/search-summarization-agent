
from data.models import AgentState

# LangGraph imports (Updated based on recent versions)
from langgraph.graph import StateGraph, END


from nodes.summarize import summarize_step
# ------------------------------------
# Workflow to summarize text
# ------------------------------------
def workflow_summarize(input_text: str):
    # Let's define a stategraph with the "AgentState" we defined earlier
    workflow = StateGraph(AgentState)

    # Let's add a node, which is the summarize function we defined before
    workflow.add_node("summarize", summarize_step)

    # Let's define Edges, which define how data flows between nodes
    workflow.add_edge("summarize", END) 
    workflow.set_entry_point("summarize")
    workflow.compile()

    # Let's compile the graph
    graph = workflow.compile() 

    # Set up the initial state with the input text
    initial_state = {
            "input_text": input_text,
            "summary": ""}
        
    # Run the graph
    result = graph.invoke(initial_state)
        
    # Get the summary from the result
    summary = result["summary"]
        
    # Print the result
    print(summary)
