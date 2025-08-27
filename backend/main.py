from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import rag
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Dict

# Load environment variables
load_dotenv()

app = FastAPI(title="Health FAQ RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://saheedmediquest.vercel.app",  # Frontend URL
        "http://localhost:5173",  # Vite dev server for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# In-memory store to track query attempts
attempt_counter: Dict[str, int] = {}

@app.get("/")
async def root():
    return {"message": "Health FAQ RAG API is running."}

@app.post("/search")
async def search_endpoint(request: QueryRequest):
    try:
        # Get the current attempt count for this query
        query_key = request.query
        attempt_counter[query_key] = attempt_counter.get(query_key, 0) + 1
        attempt = attempt_counter[query_key]

        # Call the rag function
        answer = rag(request.query)

        # Reset attempt counter on successful response
        attempt_counter.pop(query_key, None)
        return {"query": request.query, "answer": answer}

    except Exception as e:
        # Check for timeout-related errors (adjust based on rag's exception type)
        if "timeout" in str(e).lower():  # Replace with specific exception if known
            if attempt in (1, 2):
                return {
                    "error": "💡 Hmm, the request timed out. Don’t worry, just try again and we’ll get it sorted 👍"
                }
            elif attempt == 3:
                attempt_counter.pop(query_key, None)  # Reset after third attempt
                return {
                    "error": "💡 Opps, the request timed out. Don’t worry, just try again and we’ll get it sorted 👍"
                }
            else:
                # Handle subsequent attempts
                attempt_counter.pop(query_key, None)
                raise HTTPException(status_code=429, detail="Too many timeout attempts. Please try again later.")
        else:
            # Handle non-timeout errors
            attempt_counter.pop(query_key, None)
            raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")

# For local development, run Uvicorn with dynamic port
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Use Render's PORT or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)