from fastapi import FastAPI
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import publish_message

app = FastAPI(title="Automated Multi-Platform Posting System", description="Publish one validated message to multiple configured platforms independently.", version="1.0.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/posting", response_model=PostingResponse, status_code=200)
async def create_post(request: PostingRequest):
    results = await publish_message(request.message)
    return PostingResponse(success=any(result.status == "success" for result in results), results=results)
