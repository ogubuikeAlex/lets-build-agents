# What, Why and How Of A Retrieval-Augmented Generation (RAG) System

## What is RAG
**RAG** solves the scalability problem by automating the context injection step:

1. **Index** your knowledge base (documents, databases, websites) into a vector store
2. **Retrieve** only the most relevant chunks for a given query (using semantic search)
3. **Augment** the LLM prompt with those retrieved chunks
4. **Generate** a grounded, accurate response

```
User Query
    │
    ▼
[Retriever] ──── searches ────► [Vector Database / Knowledge Base]
    │                                        │
    │◄──────── relevant chunks ──────────────┘
    │
    ▼
[Prompt = Query + Retrieved Context]
    │
    ▼
[LLM] ──────► Grounded Answer ✅
```

RAG turns the hard-coded context approach into a dynamic, scalable system — the **foundation of most production AI applications today**.

---

*Next: Implementing a basic RAG pipeline with embeddings and a vector store.*
