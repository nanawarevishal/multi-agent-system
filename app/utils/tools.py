def mock_search_tool(query: str) -> str:
    """Simulates a search engine API call."""
    database = {
        "ai agents": "AI agents are autonomous systems that perceive their environment and take actions. Key frameworks include LangGraph and AutoGen.",
        "python": "Python is a high-level programming language known for readability. It is widely used in AI and Web Dev.",
    }

    for key, value in database.items():
        if key in query.lower():
            return value
    return "No specific facts found. Use general knowledge."
