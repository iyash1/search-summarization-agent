"""
Calculator Tool Module
"""

import os
from datetime import date
from dotenv import load_dotenv
from data.models import CalculatorState
from data.constants import GPT_5_MINI

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# ------------------------------------
# Load environment variables
# ------------------------------------
load_dotenv()
IS_DEBUG = os.getenv("DEBUG", "False").lower() == "true"

llm = ChatOpenAI(model = GPT_5_MINI, temperature = 0, streaming = True)

# ---------------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------------
@tool
def calculate(num1: float, num2: float, operation: str) -> float:
    """
    Perform basic arithmetic operations on two numbers.

    Args:
        num1: First number
        num2: Second number
        operation: Operation to perform. One of:
            add, subtract, multiply, divide, mod, power

    Returns:
        Result of the arithmetic operation.
    """
    try:
        a = float(num1)
        b = float(num2)
    except (TypeError, ValueError) as exc:
        raise ValueError("Inputs must be numeric.") from exc

    op = operation.strip().lower()
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y,
        "mod": lambda x, y: x % y,
        "power": lambda x, y: x**y,
    }

    if op not in operations:
        raise ValueError("Unsupported operation. Use: add, subtract, multiply, divide, mod, power.")
    if op in {"divide", "mod"} and b == 0:
        raise ZeroDivisionError("Division/modulo by zero is not allowed.")

    return operations[op](a, b)

# List of tools for this step
tools_list = [calculate]

# ---------------------------------------------------------------------------
# Process an arithmetic expression using an LLM with tool-calling capability.
# The LLM acts as an intermediary that interprets natural language or
# structured expressions and determines the appropriate tool call arguments.
# ---------------------------------------------------------------------------
def calculator_agent(state: CalculatorState):
    # 1. Extracts the expression from the state
    expression = state["expression"]

    # 2. Binds the calculate tool to the LLM
    model_with_tools = llm.bind_tools([calculate])

    # 3. Invokes the LLM to interpret and determine which calculation to perform
    response = model_with_tools.invoke(
        [HumanMessage(content=expression)]
    )

    # 4. Executes the calculate tool if tool calls are present
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        result = calculate.invoke(tool_call["args"])
        return {
            "expression": expression,
            "result": str(result)
        }

    return {
        "expression": expression,
        "result": response.content
    }

# ------------------------------------------------------------
# Construct a LangGraph StateGraph for the calculator workflow.
# ------------------------------------------------------------
def build_graph():
    #  Initializes a StateGraph with CalculatorState schema
    graph = StateGraph(CalculatorState)

    # Adds the calculator_agent as a processing node
    graph.add_node("calculator", calculator_agent)

    # Configures the graph topology (entry point and edges)
    graph.set_entry_point("calculator")
    graph.add_edge("calculator", END)

    # Compiles and returns the executable graph
    return graph.compile()

# ------------------------------------------------------------
# This is the main entry point
# -------------------------------------------------------------
def calculator_tool(input_query: str):
    # Builds the computational graph
    app = build_graph()

    # Constructs initial state from the user query
    initial_state = {
        "expression": input_query,
        "result": ""
    }

    # Invokes the graph to process the calculation
    result = app.invoke(initial_state)

    print("\n==================== QUERY ====================")
    print(result["expression"])
    print("\n==================== OUTPUT ====================")
    print(result["result"])