from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_core import rag_answer, ensure_index_built


app = FastAPI(title="Simple RAG API")

# Allow local React dev server by default
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


class AskResponse(BaseModel):
    answer: str


@app.on_event("startup")
def _startup():
    ensure_index_built()


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    ans = rag_answer(req.question, top_k=req.top_k)
    return AskResponse(answer=ans)


