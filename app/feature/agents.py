from langchain_openai import ChatOpenAI
from app.core.state import AgentState
from app.utils.tools import mock_search_tool

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


def researcher_agent(state: AgentState):
    print("--- RESEARCHER AGENT ---")
    topic = state["topic"]

    search_results = mock_search_tool(topic)

    prompt = f"You are a researcher. Compile bullet points on '{topic}' using this data: {search_results}"
    notes = llm.invoke(prompt).content

    return {"research_notes": notes}


def writer_agent(state: AgentState):
    print("--- WRITER AGENT ---")
    notes = state["research_notes"]

    prompt = f"You are a technical writer. Write a short blog post (100 words) based on these notes:\n{notes}"
    draft = llm.invoke(prompt).content

    return {"draft": draft, "revision_count": state.get("revision_count", 0) + 1}


def editor_agent(state: AgentState):
    print("--- EDITOR AGENT ---")
    draft = state["draft"]

    prompt = f"You are a strict editor. Critique this draft. If it's good, say 'APPROVED'. If it needs work, say 'REVISE'. Draft:\n{draft}"
    critique = llm.invoke(prompt).content

    if "APPROVED" in critique:
        return {"final_output": draft}
    else:
        return {"draft": "", "human_feedback": critique}
