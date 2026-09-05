import pytest
from langchain_core.documents import Document

from examples.chapter05_rag_basics.rag_demo import (
    LocalKeywordEmbeddings,
    create_prompt_messages,
    format_documents,
    load_documents,
    retrieve,
    run_offline_rag,
    split_documents,
)


def test_document_loader_keeps_content_and_source_metadata():
    documents = load_documents()

    assert all(isinstance(document, Document) for document in documents)
    assert documents[0].metadata["source"] == "refund-policy.md"


def test_splitter_creates_chunks_and_inherits_metadata():
    documents = load_documents()
    chunks = split_documents(documents)

    assert len(chunks) > len(documents)
    assert all(len(chunk.page_content) <= 32 for chunk in chunks)
    assert all("source" in chunk.metadata for chunk in chunks)
    assert all("start_index" in chunk.metadata for chunk in chunks)


def test_embedding_uses_same_normalized_dimension_for_docs_and_query():
    embeddings = LocalKeywordEmbeddings()

    document_vector = embeddings.embed_documents(["已发货订单退款"])[0]
    query_vector = embeddings.embed_query("已发货怎么退款")

    assert len(document_vector) == len(query_vector) == 6
    assert sum(value * value for value in query_vector) == pytest.approx(1.0)


def test_retriever_returns_relevant_documents_without_scores():
    results = retrieve("已发货订单怎么退款？", k=2)

    assert len(results) == 2
    assert all(isinstance(document, Document) for document in results)
    assert any("已发货订单不能直接取消" in doc.page_content for doc in results)


def test_context_formatter_keeps_source_labels():
    documents = retrieve("已发货订单怎么退款？", k=1)

    context = format_documents(documents)

    assert "[1] source=refund-policy.md" in context
    assert documents[0].page_content in context


def test_prompt_receives_context_and_question_as_human_message():
    question = "已发货订单怎么退款？"
    documents = retrieve(question, k=1)

    messages = create_prompt_messages(question, documents)

    assert "只根据给定资料回答" in messages[0].content
    assert question in messages[1].content
    assert documents[0].page_content in messages[1].content


def test_complete_offline_rag_returns_grounded_answer_and_sources():
    answer, documents = run_offline_rag("订单已经发货，还能直接取消吗？")

    assert "不能直接取消" in answer
    assert "[1]" in answer
    assert documents[0].metadata["source"] == "refund-policy.md"
