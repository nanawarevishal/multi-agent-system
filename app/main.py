import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.graph import app_graph
from app.api.v1.router import research_route


app = FastAPI(
    title="Multi-Agent Content Creator",
    description="Simplified API with logic inside main.py",
    version="1.0.0",
)

app.include_router(research_route)


@app.get("/")
def read_root():
    return {"status": "online"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
