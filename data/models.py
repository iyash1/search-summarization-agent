from typing import TypedDict
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    input_text: str
    summary: str

class AgentStateTranslation(TypedDict):
    input_text: str
    summary: str
    translated_summary: str

class AgentStateSentiment(TypedDict):
    input_text: str
    summary: str
    sentiment: str

class AgentSearchState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]