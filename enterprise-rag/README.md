# Workshop 1: From LLM to RAG: Building a Context-Aware Agent

> **What you'll build:** A RAGAS-evaluated enterprise hybrid RAG system. It combines indexed vector database retrieval with real-time API calls to provide the LLM with comprehensive, accurate context.
<img width="750" height="600" alt="image" src="https://github.com/user-attachments/assets/f5f36ff1-7820-4424-9a00-0b8ef610d356" />

### Outline

**1. LLM as a black box: interact with the LLM**
- Initialise a project with `uv` and add dependencies
- Send a message the LLM knows — watch it answer confidently
- Send a message it has no way of knowing — watch it hallucinate or refuse
- Understand what you're actually talking to

**2. The problem: LLMs have no context**
- Why the model's knowledge is frozen at training time
- What "no memory" means for real applications
- The specific failure modes you just triggered

**3. First attempt: hard-coded context**
- Manually stuff relevant information into the prompt
- See it work — then see why it doesn't scale
- Arrive at the natural question: *what if we could automatically retrieve the right context?*

**4. What, why, and how of a RAG system**
- What RAG is and why it exists (enterprise angle included)
- Why data cleaning and preparation is non-negotiable before indexing anything
- Components of a naive semantic RAG system:
  - **Indexing** — chunking documents, embedding them, storing in LanceDB (our 007), building a full-text search index on top
  - **Retrieve and format** — embedding the user query, hybrid search (semantic + FTS), reranking results
  - **Send to LLM** — assembling a context-rich prompt and getting a grounded response
- Evaluating the system with **RAGAS** — faithfulness, answer relevancy, context precision, context recall

**5. Going hybrid: adding an external API**
- Why a static knowledge base isn't enough
- Diagram: how vector search and API retrieval combine
- Adding an API call to the retrieval pipeline
- How the system decides where to get context from (query routing strategies)
- Re-running RAGAS — did the hybrid approach actually improve things?

---

## Structure

```
lets-build-agents/
├── workshop-01-rag/
│   ├── docs/               # Knowledge base (markdown files to index)
│   ├── db/                 # LanceDB database (generated)
│   ├── src/
│   │   ├── indexing.py     # Chunking, embedding, storing
│   │   ├── retrieval.py    # Hybrid search and reranking
│   │   ├── api.py          # External API retrieval
│   │   └── agent.py        # Main pipeline
│   ├── eval/
│   │   └── ragas_eval.py   # RAGAS evaluation suite
│   ├── pyproject.toml
│   └── README.md
└── README.md               ← you are here
```

---

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) for project/dependency management
- A Google API key (for Gemini embeddings) — set as `GOOGLE_API_KEY` in a `.env` file

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/your-username/lets-build-agents.git
cd lets-build-agents/workshop-01-rag

# Create environment and install dependencies
uv sync

# Add your API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# Index your knowledge base
uv run python src/indexing.py

# Run the agent
uv run python src/agent.py
```

---

## Key Dependencies

| Package | Purpose |
|---|---|
| `lancedb` | Embedded vector database with hybrid search |
| `tiktoken` | Token-accurate text chunking |
| `ragas` | RAG evaluation framework |
| `python-dotenv` | Environment variable management |
| `google-generativeai` | Gemini embedding model |

---
