from fastapi import APIRouter, UploadFile, File, HTTPException
from retrieval.pdf_processor import processor
from openai import OpenAI
import database
from config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/upload")
async def upload_pdf(user_id: str, file: UploadFile = File(...)):
    client = OpenAI(api_key=settings.openai_api_key)
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed.")
    
    content = await file.read()
    text = processor.extract_text(content)
    chunks = processor.chunk_text(text)
    
    for i, chunk in enumerate(chunks):
        # Generate embedding
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding
        
        # Store in DB
        await database.store_chunk(
            title=f"{file.filename} (Chunk {i})",
            content=chunk,
            embedding=embedding,
            user_id=user_id
        )
    
    return {"message": f"Successfully indexed {len(chunks)} chunks from {file.filename}."}
