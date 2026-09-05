"""A deterministic offline Document -> Retriever -> answer RAG pipeline."""

from __future__ import annotations

import math

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter


class LocalKeywordEmbeddings(Embeddings):
    """Small teaching embedding; not a production semantic model."""

    FEATURES = (
        ("未发货", "还没发货"),
        ("已发货", "已经发货"),
        ("退款", "退货"),
        ("运费",),
        ("发票",),
    )

    @classmethod
    def _embed(cls, text: str) -> list[float]:
        vector = [
            float(sum(text.count(keyword) for keyword in synonyms))
            for synonyms in cls.FEATURES
        ]
        if not any(vector):
            vector.append(1.0)
        else:
            vector.append(0.0)

        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Convert document chunks to vectors of one stable dimension."""

        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        """Convert one query with the same vocabulary and dimensions."""

        return self._embed(text)


def load_documents() -> list[Document]:
    """Create source Documents as a loader would do."""

    return [
        Document(
            page_content=(
                "退款规则。未发货订单可以直接申请取消。"
                "已发货订单不能直接取消，应在签收后申请退货。"
            ),
            metadata={"source": "refund-policy.md", "section": "退款"},
        ),
        Document(
            page_content=(
                "运费规则。商品存在质量问题时，退货运费由商家承担。"
                "个人原因退货时，运费通常由用户承担。"
            ),
            metadata={"source": "shipping-policy.md", "section": "运费"},
        ),
        Document(
            page_content="发票规则。订单完成后可以在订单详情页申请电子发票。",
            metadata={"source": "invoice-policy.md", "section": "发票"},
        ),
    ]


def split_documents(documents: list[Document]) -> list[Document]:
    """Split source documents while retaining source metadata."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=32,
        chunk_overlap=6,
        add_start_index=True,
        separators=["\n\n", "\n", "。", "，", " ", ""],
    )
    return splitter.split_documents(documents)


def build_vector_store(chunks: list[Document]) -> InMemoryVectorStore:
    """Embed and index chunks in a process-local vector store."""

    store = InMemoryVectorStore(embedding=LocalKeywordEmbeddings())
    store.add_documents(chunks)
    return store


def build_retriever(chunks: list[Document], k: int = 2):
    """Expose search behind LangChain's query -> Documents interface."""

    return build_vector_store(chunks).as_retriever(search_kwargs={"k": k})


def format_documents(documents: list[Document]) -> str:
    """Turn retrieved Documents into bounded prompt context."""

    blocks = []
    for index, document in enumerate(documents, start=1):
        source = document.metadata["source"]
        blocks.append(f"[{index}] source={source}\n{document.page_content}")
    return "\n\n".join(blocks)


def build_rag_prompt() -> ChatPromptTemplate:
    """Define a grounded-answer contract for the generation step."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "只根据给定资料回答。资料不足时明确说不知道，并引用资料编号。",
            ),
            ("human", "资料：\n{context}\n\n问题：{question}"),
        ]
    )


def retrieve(question: str, k: int = 2) -> list[Document]:
    """Run the online retrieval half of the example."""

    chunks = split_documents(load_documents())
    retriever = build_retriever(chunks, k=k)
    return retriever.invoke(question)


def create_prompt_messages(question: str, documents: list[Document]):
    """Produce the final messages that a real chat model would receive."""

    context = format_documents(documents)
    return build_rag_prompt().invoke(
        {"context": context, "question": question}
    ).to_messages()


def generate_offline_answer(documents: list[Document]) -> str:
    """Stand in for generation while preserving an observable citation."""

    for index, document in enumerate(documents, start=1):
        if "已发货订单不能直接取消" in document.page_content:
            return f"已发货订单不能直接取消，应在签收后申请退货。[{index}]"
    return "现有资料不足，无法回答。"


def run_offline_rag(question: str) -> tuple[str, list[Document]]:
    """Execute retrieve -> format -> offline generation."""

    documents = retrieve(question)
    create_prompt_messages(question, documents)
    return generate_offline_answer(documents), documents


def main() -> None:
    question = "订单已经发货，还能直接取消吗？"
    answer, documents = run_offline_rag(question)

    print(f"问题：{question}")
    print("检索结果：")
    for document in documents:
        print(f"- {document.metadata['source']}: {document.page_content}")
    print(f"回答：{answer}")


if __name__ == "__main__":
    main()
