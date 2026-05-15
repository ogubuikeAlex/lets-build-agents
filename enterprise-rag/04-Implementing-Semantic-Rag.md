# Implementing RAG System

### Stage 1: Build The Search Engine
 
#### **Why do we need to index?**
 
Unfortunately, LLMs have a fixed context window and it would be wild to feed it our entire knowledge base on every request.

And even if we could do that, it would be slow and expensive. 

Indexing solves this by pre-processing our documents into a structure that makes it fast to find only the *relevant* pieces at query time.

-----
 
#### **Why do we need a vector database?**
 
Traditional keyword search (like grep or SQL `LIKE`) can only match exact words. A user asking *"how do I reset my credentials?"* won't find a document that says *"steps to recover account access"*,  even though they mean the same thing. 

Vector databases store **semantic embeddings**.

A Semantic embedding is a numeric representations of *meaning*. Similar meanings cluster together in vector space, so semantic search finds conceptually relevant content regardless of the exact words used.
 
```LanceDB is our 007 here.```

[LanceDB](https://lancedb.com/) is an embedded, serverless vector database that runs alongside our application with no separate server to manage. 
For today's demonstration, we use lancedb because it supports both full text search and also vector search.

Here's what lancedb does for us:
- Stores our document chunks and their vector embeddings in a single table
- Gives us best of both worlds: supports **full-text search (FTS)** alongside vector search
- Provides a Python-native API that fits cleanly into our pipeline

#### Some Info To Keep In Mind
> **Full-text search** ia a keyword-based search that finds documents containing the exact words (or stems of words) in our query.
> 
> **Vector search** is a similarity-based search that finds documents whose meaning is closest to our query, regardless of the exact words we sent it.
> 
> **Chunking** is when we split a large document into smaller pieces so each piece fits within a model's token limit and retrieves with more precision.
> 
> **Embedding model** is a model that converts text into a fixed-length list of numbers (a vector) that captures its semantic meaning.


Here's the indexing flow from our code:
 
```python
# 1. Define the schema — LanceDB knows which field to embed automatically
class Document(LanceModel):
    id: str
    text: str = model.SourceField()          # Raw text, gets embedded
    vector: Vector(model.ndims()) = model.VectorField()  # The embedding
 
# 2. Create the table and a full-text search index on top
table = db.create_table(table_name, schema=Document, mode='overwrite')
table.create_fts_index('text', replace=True)
 
# 3. Chunk documents and add them
for md_file in knowledge_base.glob('*.md'):
    for index, chunk in enumerate(chunk_text(text, max_tokens=8192)):
        docs.append({'id': f'{md_file.stem}_{index}', 'text': chunk})
 
table.add(docs)
```
`model.ndims()` returns the number of dimensions in the vectors that the embedding model produces. Gemini's gemini-embedding-001 outputs 3072-dimensional vectors, so Vector(model.ndims()) is just a clean way of writing Vector(3072) without hardcoding it.

**Note:** Smaller, focused chunks retrieve more precisely. For example, a 200-word chunk about a single topic scores much higher than a 5,000-word document where the relevant part is buried on page 3.
 
---
 
### Stage 2: Retrieve and Format the User Query
 
When a user asks a question, we:
 
1. **Embed the query** using the same embedding model used at index time (Gemini `gemini-embedding-001`). This is importan because if we don't use the same model the vector spaces won't match.
2. **Search the database** for the most semantically similar chunks.
3. **Format the results** into a structured context block.
   
From our code:
 
```python
def retrieve_similar_docs(table, query, query_type='hybrid', limit=100, reranker_weight=0.7):
    reranker = LinearCombinationReranker(weight=reranker_weight)
 
    results = (
        table.search(query=query, query_type='hybrid')
        .rerank(reranker=reranker)
        .limit(limit)
        .to_list()
    )
    return results
```
 
`query_type='hybrid'` means we run **both** semantic vector search and keyword full-text search simultaneously. 

The `LinearCombinationReranker` then merges the two ranked lists into one, weighted by `reranker_weight` (0.7 = 70% semantic, 30% keyword). This already gives us a leg up over pure vector search.
 
---
 
### Stage 3: Send the Context-Rich Query to the LLM
 
The retrieved chunks are assembled into a prompt that gives the LLM everything it needs:
 
```
System: You are a helpful assistant. Answer only using the context provided below.
 
Context:
[Chunk 1 text]
[Chunk 2 text]
...
 
User Question: When will orra go to main net
```
 
