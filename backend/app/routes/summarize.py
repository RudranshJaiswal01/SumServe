from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.groq_client import GroqClient, GroqSummarizationError
from app.utils.file_parser import extract_text_from_file, FileExtractionError
from app.core.logger import get_logger

logger = get_logger("summarize")

router = APIRouter()
groq = GroqClient()

@router.post("/summarize")
async def summarize(
    style: str = Form(...),
    text: str | None = Form(None),
    file: UploadFile | None = File(None),
):
    logger.info("Summarization request received")

    # ---- validation ----
    if (not text and not file):
        raise HTTPException(
            status_code=400,
            detail="Provide either text or file"
        )
    
    if (text and file):
        raise HTTPException(
            status_code=400,
            detail="Provide either text or file not both"
        )

    if style not in {"brief", "detailed", "bullet"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid summarization style"
        )

    # ---- extract text ----
    if file:
        try:
            text = extract_text_from_file(file)
        except FileExtractionError as e:
            raise HTTPException(status_code=415, detail=str(e))

    if not text or len(text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Content is too short"
        )

    if len(text) > 12_000:
        raise HTTPException(
            status_code=413,
            detail="Content exceeds maximum allowed length"
        )

    # ---- call LLM ----
    try:
        result = groq.summarize(text=text, style=style)
        summary = result["summary"]

        word_count = len(summary.split())

        return {
            "summary": summary,
            "word_count": word_count
        }
    
    except GroqSummarizationError as e:
        logger.error(f"Groq error: {e}")
        raise HTTPException(status_code=502, detail="Some error Occured with LLM Service")
