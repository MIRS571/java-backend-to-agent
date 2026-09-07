"""Offline Qdrant example with stable IDs, tenant filters, and evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid5

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

from examples.chapter05_rag_basics.rag_demo import LocalKeywordEmbeddings

COLLECTION_NAME = "support_knowledge"
VECTOR_SIZE = 6
CHUNK_NAMESPACE = UUID("7a1f4268-c727-4c40-bddb-cb39c0112c19")


@dataclass(frozen=True)
class EvaluationCase:
    """One retrieval question with an expected source document."""

    question: str
    tenant_id: str
    expected_source: str


@dataclass(frozen=True)
class Citation:
    """Application-facing source data kept outside generated prose."""

    chunk_id: str
    source: str
    version: str


def stable_chunk_id(document: Document) -> str:
    """Derive one repeatable UUID from a chunk's logical identity."""

    metadata = document.metadata
    identity = "|".join(
        [
            str(metadata["tenant_id"]),
            str(metadata["source"]),
            str(metadata["version"]),
            str(metadata["start_index"]),
        ]
    )
    return str(uuid5(CHUNK_NAMESPACE, identity))


def build_documents() -> list[Document]:
    """Create chunks for two tenants that intentionally discuss similar topics."""

    return [
        Document(
            page_content="已发货订单不能直接取消，应在签收后申请退货。",
            metadata={
                "tenant_id": "company_001",
                "source": "refund-policy.md",
                "version": "2026-09",
                "start_index": 0,
            },
        ),
        Document(
            page_content="质量问题退货的运费由商家承担。",
            metadata={
                "tenant_id": "company_001",
                "source": "shipping-policy.md",
                "version": "2026-09",
                "start_index": 0,
            },
        ),
        Document(
            page_content="已发货订单可以联系客服尝试拦截。",
            metadata={
                "tenant_id": "company_002",
                "source": "refund-policy.md",
                "version": "2026-08",
                "start_index": 0,
            },
        ),
        Document(
            page_content="质量问题退货的运费需要用户先行垫付。",
            metadata={
                "tenant_id": "company_002",
                "source": "shipping-policy.md",
                "version": "2026-08",
                "start_index": 0,
            },
        ),
    ]


def create_memory_qdrant() -> tuple[QdrantClient, QdrantVectorStore]:
    """Create an embedded Qdrant collection for deterministic tests."""

    client = QdrantClient(location=":memory:")
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )

    store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=LocalKeywordEmbeddings(),
    )
    return client, store


def ingest_documents(
    vector_store: QdrantVectorStore,
    documents: list[Document],
) -> list[str]:
    """Upsert chunks with deterministic IDs and citation metadata."""

    indexed_documents: list[Document] = []
    ids: list[str] = []
    for document in documents:
        chunk_id = stable_chunk_id(document)
        ids.append(chunk_id)
        indexed_documents.append(
            Document(
                id=chunk_id,
                page_content=document.page_content,
                metadata={**document.metadata, "chunk_id": chunk_id},
            )
        )

    vector_store.add_documents(documents=indexed_documents, ids=ids)
    return ids


def tenant_filter(tenant_id: str) -> models.Filter:
    """Build a mandatory filter for LangChain's nested metadata payload."""

    return models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.tenant_id",
                match=models.MatchValue(value=tenant_id),
            )
        ]
    )


def search_for_tenant(
    vector_store: QdrantVectorStore,
    question: str,
    tenant_id: str,
    k: int = 2,
) -> list[Document]:
    """Search with tenant isolation enforced inside Qdrant."""

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": k,
            "filter": tenant_filter(tenant_id),
        }
    )
    return retriever.invoke(question)


def build_citations(documents: list[Document]) -> list[Citation]:
    """Map retrieved metadata to stable application-facing citations."""

    return [
        Citation(
            chunk_id=str(document.metadata["chunk_id"]),
            source=str(document.metadata["source"]),
            version=str(document.metadata["version"]),
        )
        for document in documents
    ]


def recall_at_k(
    vector_store: QdrantVectorStore,
    cases: list[EvaluationCase],
    k: int,
) -> float:
    """Measure how often the expected source appears in the top-k results."""

    hits = 0
    for case in cases:
        results = search_for_tenant(
            vector_store=vector_store,
            question=case.question,
            tenant_id=case.tenant_id,
            k=k,
        )
        if any(
            document.metadata["source"] == case.expected_source
            for document in results
        ):
            hits += 1
    return hits / len(cases) if cases else 0.0


def main() -> None:
    client, vector_store = create_memory_qdrant()
    try:
        ids = ingest_documents(vector_store, build_documents())
        results = search_for_tenant(
            vector_store,
            question="已发货订单能直接取消吗？",
            tenant_id="company_001",
            k=1,
        )
        citations = build_citations(results)
        score = recall_at_k(
            vector_store,
            cases=[
                EvaluationCase(
                    question="已发货订单怎么处理？",
                    tenant_id="company_001",
                    expected_source="refund-policy.md",
                ),
                EvaluationCase(
                    question="质量问题退货运费谁承担？",
                    tenant_id="company_001",
                    expected_source="shipping-policy.md",
                ),
            ],
            k=1,
        )

        print(f"写入 point 数量：{len(ids)}")
        print(f"租户检索结果：{results[0].page_content}")
        print(f"引用：{citations[0]}")
        print(f"Recall@1：{score:.2%}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
