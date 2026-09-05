# 第 5 章示例：RAG 基础

本示例离线展示两条流程：

- 建库：`Document -> RecursiveCharacterTextSplitter -> Embedding -> InMemoryVectorStore`；
- 查询：`question -> Retriever -> Documents -> Prompt context -> answer`。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter05_rag_basics.rag_demo
```

`LocalKeywordEmbeddings` 是为了测试可重复而写的教学实现，只能识别代码中列出的关键词，不是语义模型。生产项目应使用经过评估的 Embedding 模型，并在第 6 章将内存向量库替换为 Qdrant。
