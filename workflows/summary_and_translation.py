from data.models import AgentStateTranslation

# LangGraph imports (Updated based on recent versions)
from langgraph.graph import StateGraph

from nodes.summarize import summarize_step
from nodes.translate import translate_step

# --------------------------------
# Workflow to summarize and translate text
# --------------------------------
def workflow_summarize_and_translate(input_text: str):
    # Let's define a stategraph with the "AgentState" we defined earlier
    workflow = StateGraph(AgentStateTranslation)

    # Let's add a node, which is the summarize function we defined before
    workflow.add_node("summarize", summarize_step)

    # Let's define Edges, which define how data flows between nodes
    workflow.add_edge("summarize", "translate") 
    workflow.add_node("translate", translate_step)
    workflow.set_entry_point("summarize")

    # Let's compile the graph
    graph = workflow.compile() 

    # Set up the initial state with the input text
    initial_state = {
            "input_text": input_text,
            "summary": "",
            "translated_summary": ""}
        
    # Run the graph
    result = graph.invoke(initial_state)
        
    # Get the summary from the result
    summary = result["summary"]
    translation = result["translated_summary"]

    # Print the results with clear labels and spacing
    print(f"=== Generated Summary ===")
    print(summary)

    print("\n=== Translated Summary ===")
    print(translation)

