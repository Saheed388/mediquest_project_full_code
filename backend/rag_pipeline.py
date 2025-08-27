import os
from typing import Optional, List
from qdrant_client import QdrantClient
from qdrant_client import models
from qdrant_client.models import PointStruct, VectorParams, Distance
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
q_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model_handle= "jinaai/jina-embeddings-v2-small-en"
collection_name = "health-care-facility-rag"

def search(query: str, limit: int = 1):
    """Search the FAQ database using Qdrant hybrid query API."""
    try:
        results = q_client.query_points(
            collection_name=collection_name,
            query=models.Document(
                text=query,
                model=model_handle   # same model you used when inserting data
            ),
            limit=limit,
            with_payload=True
        )
        return results
    except Exception as e:
        print(f"Search error: {str(e)}")
        return None


def build_prompt(query: str, search_results: Optional[List[PointStruct]]) -> str:
    """Build a prompt for the LLM using search results."""
    prompt_template = """
You are a health facility information assistant. Always prioritize answering the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

If the QUESTION is a greeting (e.g., 'hello', 'hi', 'hey', or similar), respond with a friendly greeting like 'Hello! How can I assist you with healthcare facility information today?' and do not provide any facility data.

If the CONTEXT is empty or does not contain sufficient information to answer the QUESTION (and the QUESTION is not a greeting), then check reliable online sources, but restrict the search strictly to healthcare facilities in Abuja or Lagos.

When using online information, provide only concise and relevant details without extra explanation.

QUESTION: {question}

CONTEXT: {context}
""".strip()
    return prompt_template.format(question=query, context=search_results)

    context = ""
    if not search_results:
        return prompt_template.format(question=query, context="No relevant information found.")

    # Check if search_results has points (Qdrant QueryResponse)
    if hasattr(search_results, 'points'):
        points = search_results.points
    else:
        points = search_results

    # Build context from points
    for point in points:
        try:
            # If point is a dict
            if isinstance(point, dict):
                section = point.get('section', 'N/A')
                question = point.get('question', 'N/A')
                text = point.get('text', 'N/A')
            # If point is a Qdrant Point with payload
            else:
                section = point.payload.get('section', 'N/A')
                question = point.payload.get('question', 'N/A')
                text = point.payload.get('text', 'N/A')
            context += f"Section: {section}\nQuestion: {question}\nAnswer: {text}\n\n"
        except (AttributeError, KeyError) as e:
            context += f"Invalid data format in search results: {str(e)}\n\n"

    if not context.strip():
        context = "No relevant information found."

    return prompt_template.format(question=query, context=context.strip())

def llm(prompt: str) -> str:
    """Generate a response using the LLM."""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"  # Updated to a valid Groq model
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM error: {str(e)}"

def rag(query: str) -> str:
    """Run the RAG pipeline: search, build prompt, and generate answer."""
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer