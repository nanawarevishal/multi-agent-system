import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

from app.core.graph import app_graph


class ContentRequest(BaseModel):
    topic: str


class ContentResponse(BaseModel):
    topic: str
    final_article: str
    revision_count: int


research_route = APIRouter(prefix="")


@research_route.post("/generate", response_model=ContentResponse)
async def create_generation_task(request: ContentRequest):
    """
    Receives a topic, runs the multi-agent graph, and returns the article.
    """
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    inputs = {"topic": request.topic}

    result = app_graph.invoke(inputs)

    final_article = (
        result.get("final_output") or result.get("draft") or "Generation failed."
    )

    return ContentResponse(
        topic=request.topic,
        final_article=final_article,
        revision_count=result.get("revision_count", 0),
    )
