from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    topic: str
    research_notes: str
    draft: str
    final_output: str
    revision_count: int
    human_feedback: str
