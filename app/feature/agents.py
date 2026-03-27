from langchain_openai import ChatOpenAI
from app.core.state import AgentState
from app.utils.tools import mock_search_tool


llm = ChatOpenAI(model="gpt-4o", temperature=0.5)


def researcher_agent(state: AgentState):
    print("--- RESEARCHER AGENT ---")
    topic = state["topic"]
    search_results = mock_search_tool(topic)

    prompt = (
        f"You are a research assistant. Compile detailed bullet points on '{topic}'.\n"
        f"Focus on finding concrete examples, dates, and names.\n"
        f"Data: {search_results}"
    )
    notes = llm.invoke(prompt).content
    return {"research_notes": notes}


def writer_agent(state: AgentState):
    print("--- WRITER AGENT ---")
    notes = state["research_notes"]
    feedback = state.get("human_feedback", "")
    current_draft = state.get("draft", "")

    if feedback and current_draft:

        prompt = (
            f"You are a meticulous writer. You received feedback on your previous draft.\n"
            f"1. Analyze the feedback.\n"
            f"2. Rewrite the draft to address the specific points raised.\n"
            f"3. Do not ignore the feedback.\n\n"
            f"Previous Draft:\n{current_draft}\n\n"
            f"Editor Feedback:\n{feedback}\n\n"
            f"Revised Draft:"
        )
    else:
        prompt = (
            f"You are a technical writer. Write a comprehensive blog post based on these notes.\n"
            f"Include specific historical examples and dates where possible.\n"
            f"Notes:\n{notes}"
        )

    draft = llm.invoke(prompt).content
    return {"draft": draft, "revision_count": state.get("revision_count", 0) + 1}


def editor_agent(state: AgentState):
    print("--- EDITOR AGENT ---")
    draft = state["draft"]

    prompt = (
        f"You are a pragmatic editor. Your goal is to finalize articles efficiently.\n"
        f"Review the draft below.\n"
        f"- If the draft is coherent, factually sounds, and answers the prompt, reply with 'APPROVED'.\n"
        f"- Only request revisions (starting with 'REVISE') if there are major factual errors or missing key points.\n"
        f"- Do not nitpick minor details.\n\n"
        f"Draft:\n{draft}"
    )

    critique = llm.invoke(prompt).content

    if "APPROVED" in critique:
        return {"final_output": draft}
    else:
        return {"human_feedback": critique}
