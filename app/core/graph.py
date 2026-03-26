from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.feature.agents import researcher_agent, writer_agent, editor_agent


def check_quality(state: AgentState):

    if state.get("final_output"):
        return "end"

    if state.get("revision_count", 0) >= 3:
        return "end"

    return "revise"


workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("editor", editor_agent)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "editor")

workflow.add_conditional_edges(
    "editor",
    check_quality,
    {"end": END, "revise": "writer"},
)

app_graph = workflow.compile()
