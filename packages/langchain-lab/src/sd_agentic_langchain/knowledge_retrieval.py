"""Knowledge retrieval (RAG): LangChain vector store retrieve then LCEL generate."""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from pydantic import BaseModel

from sd_agentic_shared.corpus import RAG_CHUNKS
from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import RAG_REPLY_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

K = 3


class RetrievedChunk(BaseModel):
    id: str
    title: str
    text: str
    score: float


class RagResult(BaseModel):
    query: str
    retrieved: list[RetrievedChunk]
    reply: str


def _store() -> InMemoryVectorStore:
    docs = [
        Document(
            page_content=f"{chunk.title}. {chunk.text}",
            metadata={"id": chunk.id, "title": chunk.title, "text": chunk.text},
        )
        for chunk in RAG_CHUNKS
    ]
    return InMemoryVectorStore.from_documents(docs, OpenAIEmbeddings())


def _generate_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RAG_REPLY_SYSTEM),
            ("human", "Retrieved chunks:\n{chunks}\n\nEmail:\n{email}"),
        ]
    )
    return prompt | ChatOpenAI(model=openai_model()) | StrOutputParser()


@observe(name="pattern.knowledge_retrieval")
def run(email: str | None = None) -> RagResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:langchain", "pattern:knowledge_retrieval"],
        metadata={"pattern": "knowledge_retrieval", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        config = {"callbacks": [handler]}
        pairs = _store().similarity_search_with_score(ticket, k=K)
        retrieved = [
            RetrievedChunk(
                id=str(doc.metadata.get("id") or ""),
                title=str(doc.metadata.get("title") or ""),
                text=str(doc.metadata.get("text") or doc.page_content),
                score=round(float(score), 4),
            )
            for doc, score in pairs
        ]
        blob = "\n\n".join(
            f"[{item.id}] {item.title}: {item.text}" for item in retrieved
        ) or "(none)"
        reply = _generate_chain().invoke(
            {"chunks": blob, "email": ticket},
            config=config,
        )
        return RagResult(query=ticket, retrieved=retrieved, reply=reply)


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
