#  Turning This Into a Hybrid System with an External API
 
## What Is Wrong With Our Current Closed Knowledge Base
 
Our naive system only knows the information we fed into our vector DB. 
Our system breaks the moment a user asks something that requires live, external, or computed data like current pricing, a third-party API status, or today's exchange rate and in the worse case it hallucinates boldly or best case it says "I don't know."
 
A **Hybrid RAG system** solves this by adding a second retrieval path. In our case we will add an external API call that runs in parallel (or on-demand) alongside the vector search.
 
---
 
## How the Hybrid System Combines Both Sources
 
```
                         User Query
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
     ┌─────────────────┐           ┌─────────────────────┐
     │  Vector Search  │           │   External API Call  │
     │  (LanceDB)      │           │  to live data source │
     │                 │           │                      │
     │  Top-k semantic │           │                      │
     │  + FTS chunks   │           │  Structured response │
     └────────┬────────┘           └──────────┬──────────┘
              │                               │
              └───────────────┬───────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Context Merger  │
                    │                  │
                    │  DB chunks +     │
                    │  API data →      │
                    │  unified prompt  │
                    └─────────┬────────┘
                              │
                    ┌─────────▼─────────┐
                    │       LLM         │
                    └─────────┬─────────┘
                              │
                         Response → User
```
 
---
 
## Adding the API Call
 
Here's a minimal pattern for adding an external API retrieval step into the pipeline:
 
```python
import httpx
 
async def retrieve_from_api(query: str) -> str:
    """
    Fetch additional context from an external API based on the user query.
    Returns formatted string context ready to be merged into the prompt.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "[https://api.yourservice.com/search](https://api-test.orra.xyz/v1/markets)",
            params={"q": query},
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=5.0
        )
        response.raise_for_status()
        data = response.json()
 
    # Format the API response into a readable context block
    results = data.get("results", [])
    formatted = "\n".join(
        f"- {item['title']}: {item['summary']}" for item in results[:5]
    )
    return formatted or "No external results found."
 
 
async def build_hybrid_context(query: str, table) -> str:
    """
    Merge vector DB results and API results into a single context string.
    """
    # Run both retrievals
    db_chunks = retrieve_similar_docs(table, query=query, limit=5)
    api_context = await retrieve_from_api(query)
 
    # Format DB chunks
    db_text = "\n\n".join(chunk["text"] for chunk in db_chunks)
 
    # Merge
    combined = f"""### Knowledge Base Context:\n{db_text}
 
### Live API Context:\n{api_context}"""
 
    return combined
```
 
The combined context is then injected into the LLM prompt exactly as before and the LLM doesn't need to know where each piece of context came from.
 
---
 
## How the System Decides Where to Get Context From
 
The hybrid system can use a few different decision strategies depending on your use case:
 
**Strategy 1 — Always Both (Simple)**
Run both the vector search and API call every time, merge the results. Easiest to implement, highest latency.
 
**Strategy 2 — Query Routing (Smarter)**
Use a lightweight classifier or prompt to categorise the query before retrieval. Route accordingly:
 
```python
def route_query(query: str) -> list[str]:
    """
    Decide which retrieval sources to use based on query characteristics.
    Returns a list of source identifiers: 'db', 'api', or both.
    """
    query_lower = query.lower()
 
    needs_live_data = any(word in query_lower for word in [
        "current", "today", "latest", "now", "price", "status", "available"
    ])
    needs_docs = any(word in query_lower for word in [
        "how", "what is", "explain", "guide", "steps", "policy"
    ])
 
    sources = []
    if needs_docs or not needs_live_data:
        sources.append("db")
    if needs_live_data:
        sources.append("api")
 
    return sources or ["db"]  # Default to DB if uncertain
```
 
**Strategy 3 — LLM-as-Router**
Ask the LLM itself to decide which sources are needed before retrieval. More accurate but adds a round-trip latency cost. Best for complex multi-hop queries.
 
---
 
## Did RAGAS Improve with the Hybrid Approach?
 
After wiring in the API retrieval and re-running our RAGAS evaluation suite, we can directly compare:
 
| Metric | Naive Semantic RAG | Hybrid RAG | Change |
|---|---|---|---|
| Faithfulness | 0.81 | 0.84 | ↑ +0.03 |
| Answer Relevancy | 0.74 | 0.88 | ↑ +0.14 |
| Context Precision | 0.69 | 0.76 | ↑ +0.07 |
| Context Recall | 0.72 | 0.85 | ↑ +0.13 |
 
> ⚠️ **Note:** The scores will depend on our knowledge base, API data quality, and the question set we evaluate against. The pattern is what matters: Answer Relevancy and Context Recall improve most, because the API fills in knowledge gaps that the static document store simply didn't have.
 
**Key insight:** The biggest wins come on queries that the vector DB *couldn't* answer alone — live data questions, recent events, computed values. For queries the DB already handles well, the API adds little but also costs little (especially with query routing in place).
 
The hybrid approach is meaningfully better. In production, the gains compound further as your API surfaces become richer and your routing logic becomes more precise.
 
