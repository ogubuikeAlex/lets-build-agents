# Evaluating with RAGAS
 
We would be moving with eyes closed if we build this RAG system and not actually measure its effectiveness. 

**RAGAS** (Retrieval-Augmented Generation Assessment) is an evaluation framework that gives us metrics for both retrieval quality and generation quality.
The best part is it dows not need human-labelled answers for every test case.
 
Key RAGAS metrics:
 
| Metric | What it measures |
|---|---|
| **Faithfulness** | Does the answer stay true to the retrieved context? (Hallucination detector) |
| **Answer Relevancy** | Is the answer actually relevant to the question asked? |
| **Context Precision** | Are the retrieved chunks actually useful for answering? |
| **Context Recall** | Did we retrieve all the information needed to answer? |
 
We run RAGAS over a test set of questions to get a baseline score for our naive system.
 
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
 
results = evaluate(
    dataset=test_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
print(results)
```
 
These scores are our benchmark.
 
---
 
