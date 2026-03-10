import os
from datetime import date
from dotenv import load_dotenv
from data.models import CalculatorState
from data.constants import GPT_5_MINI

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode 
from typing import TypedDict, Annotated, Sequence, List, Tuple, Optional, Any, Union, Literal,  Tuple


# ------------------------------------
# Load environment variables
# ------------------------------------
load_dotenv()
IS_DEBUG = os.getenv("DEBUG", "False").lower() == "true"

llm = ChatOpenAI(model = GPT_5_MINI, temperature = 0, streaming = True)

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

tools_list = [calculate]

def calculator_agent(state: CalculatorState):
    expression = state["expression"]
    model_with_tools = llm.bind_tools([calculate])

    response = model_with_tools.invoke(
        [HumanMessage(content=expression)]
    )

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

def build_graph():
    graph = StateGraph(CalculatorState)
    graph.add_node("calculator", calculator_agent)
    graph.set_entry_point("calculator")
    graph.add_edge("calculator", END)
    return graph.compile()

def calculator_tool(input_query: str):
    app = build_graph()

    initial_state = {
        "expression": input_query,
        "result": ""
    }

    result = app.invoke(initial_state)
    print("\n==================== QUERY ====================")
    print(result["expression"])
    print("\n==================== OUTPUT ====================")
    print(result["result"])