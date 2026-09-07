from pathlib import Path

import pytest
import yaml

from examples.chapter06_enterprise_rag.qdrant_demo import (
    EvaluationCase,
    build_citations,
    build_documents,
    create_memory_qdrant,
    ingest_documents,
    recall_at_k,
    search_for_tenant,
    stable_chunk_id,
)


@pytest.fixture
def indexed_store():
    client, vector_store = create_memory_qdrant()
    ingest_documents(vector_store, build_documents())
    try:
        yield client, vector_store
    finally:
        client.close()


def test_stable_chunk_id_is_repeatable_and_tenant_specific():
    documents = build_documents()

    assert stable_chunk_id(documents[0]) == stable_chunk_id(documents[0])
    assert stable_chunk_id(documents[0]) != stable_chunk_id(documents[2])


def test_reingestion_upserts_same_point_ids(indexed_store):
    client, vector_store = indexed_store
    first_ids = ingest_documents(vector_store, build_documents())
    second_ids = ingest_documents(vector_store, build_documents())

    assert first_ids == second_ids
    assert client.count(collection_name="support_knowledge", exact=True).count == 4


def test_tenant_filter_prevents_cross_tenant_retrieval(indexed_store):
    _client, vector_store = indexed_store

    company_001 = search_for_tenant(
        vector_store,
        "已发货订单怎么处理？",
        tenant_id="company_001",
        k=2,
    )
    company_002 = search_for_tenant(
        vector_store,
        "已发货订单怎么处理？",
        tenant_id="company_002",
        k=2,
    )

    assert {doc.metadata["tenant_id"] for doc in company_001} == {"company_001"}
    assert {doc.metadata["tenant_id"] for doc in company_002} == {"company_002"}
    assert company_001[0].page_content != company_002[0].page_content


def test_citations_keep_stable_source_identity(indexed_store):
    _client, vector_store = indexed_store
    documents = search_for_tenant(
        vector_store,
        "已发货订单怎么处理？",
        tenant_id="company_001",
        k=1,
    )

    citation = build_citations(documents)[0]

    assert citation.chunk_id == documents[0].metadata["chunk_id"]
    assert citation.source == "refund-policy.md"
    assert citation.version == "2026-09"


def test_recall_at_k_uses_expected_sources(indexed_store):
    _client, vector_store = indexed_store
    cases = [
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
    ]

    assert recall_at_k(vector_store, cases, k=1) == 1.0
    assert recall_at_k(vector_store, [], k=1) == 0.0


def test_qdrant_compose_is_local_only_and_uses_named_volume():
    compose_path = (
        Path(__file__).resolve().parents[1] / "infra" / "qdrant" / "compose.yml"
    )
    compose = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
    service = compose["services"]["qdrant"]

    assert service["image"] == "qdrant/qdrant:v1.18.2"
    assert service["ports"] == [
        "127.0.0.1:6333:6333",
        "127.0.0.1:6334:6334",
    ]
    assert service["volumes"] == ["qdrant-data:/qdrant/storage"]
    assert "qdrant-data" in compose["volumes"]
