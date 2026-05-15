# What, Why and How Of A Retrieval-Augmented Generation (RAG) System

## What is RAG
Retrieval-Augmented Generation is an architecture where we give an LLM access to external knowledge it wasn't trained on. Our aim with this is to give it the ability to correctly answer questions beyond what it has memorized.

With RAG we can trun our previous hard-coded context approach into a dynamic, scalable system.

`FUN FACT: This is the foundation of most AI applications you use.`

## Components of A Semantic RAG System
 
Our starting point is a **Naive Semantic RAG** system. 

**Let not your heart be distressed,** "Naive" here doesn't mean bad, it means straightforward: embed everything, search by vector similarity, hand the result to the LLM. 

The flow for this:
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
[LLM] ──────► Grounded Answer
```

To implement this we would modularize it into three stages:
 
```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                             │
│                                                                 │
│  ┌──────────────┐    ┌─────────────────┐    ┌───────────────┐  │
│  │   INDEXING   │    │ RETRIEVE+FORMAT │    │  LLM + SEND   │  │
│  │              │    │                 │    │               │  │
│  │ .md files    │    │  User query     │    │  Context-rich │  │
│  │     ↓        │───▶│      ↓          │───▶│  prompt sent  │  │
│  │  Chunk text  │    │ Embed + search  │    │  to LLM       │  │
│  │     ↓        │    │      ↓          │    │      ↓        │  │
│  │  Embed +     │    │ Top-k chunks    │    │  Response     │  │
│  │  store in DB │    │  formatted      │    │  → User       │  │
│  └──────────────┘    └─────────────────┘    └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```
