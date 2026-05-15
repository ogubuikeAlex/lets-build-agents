# The Problems and Limitations of LLMs

An LLM is like a highly sophisticated compression of human knowledge. It is brilliant at what it saw, completely blind to what came after.

---

## Core Limitations of LLMs

### 1. Knowledge Cutoff (Frozen in Time)

LLMs are trained on static datasets. Once training ends, the model's world stops. It has no awareness of:

- New product launches or startup announcements
- Live prices, scores, or market data
- Recent events, policies, or breaking news
- Emerging technologies or newly coined terms

**Example:**

```python
# Question 1: Known information — works perfectly
ask_gemini("What are the months of the year?")
# ✅ January, February, March... (trained knowledge)

# Question 2: Unknown/Future information
ask_gemini("When will Orra.xyz go live and collaborate with Rome Protocol?")
# 🥹 The model has no idea — it was never in the training data
```

Orra.xyz and Rome Protocol are crypto/web3 startups whose collaboration details post-date (or were never included in) the model's training corpus. 
The LLM cannot make up a reliable answer and if it tries, it **hallucinates**: fabricating plausible-sounding but entirely incorrect information.

---

### 2. No Long-Term Memory

Each API call to an LLM is stateless. The model doesn't remember your previous conversation unless you explicitly pass the history back in every request. It has no persistent memory of:

- Past user interactions
- Previous sessions
- Ongoing projects or preferences

---

### 3. Private / Domain-Specific Knowledge Gaps

LLMs are trained on publicly available internet data. They know nothing about:

- Your company's internal documents
- Proprietary databases or research
- Custom business logic or private APIs
- Confidential client records

Asking an LLM "What were our Q3 sales figures?" will yield nothing useful.
---

### 4. Hallucination

When an LLM lacks real knowledge but is prompted for a confident answer, it will often *invent* one. The output looks authoritative but is fabricated. This is a known failure mode called **hallucination**. This is especially dangerous in Legal or medical advice, financial data
or citation of papers or statistics

---

## The Natural Question: What If We Just Tell It?

If the model doesn't know something, what happens when we *provide* the information ourselves, right in the prompt?

This is a powerful idea. LLMs are exceptional at **reasoning over given context**. They can:
- Summarize it
- Answer questions about it
- Extract structured data from it
- Draw logical conclusions from it

They just can't *know* things they were never shown. But if we show them, in the prompt, at query time, we have solved the problem partially.

---

## Attempt 1: Hard-Coded Context Injection

The simplest possible approach: manually paste the relevant information into the prompt before asking the question. No database. No retrieval. Just string concatenation.

```python
hardcoded_context = """
[Source: Orra.xyz Official Announcement - May 2026]
Orra.xyz is a prediction amrket platform currently in closed beta.
The team has confirmed a public mainnet launch scheduled for Q4 2026.

Orra.xyz has officially announced a strategic collaboration with Rome Protocol,
a cross-chain interoperability layer. The partnership will enable Orra's 
users access solana blockchain via rome protocol evm infrastructure and also allow
orra's credentials to be verified across multiple blockchains via Rome Protocol's
messaging infrastructure. The integration is expected to go live alongside
the Orra mainnet launch in Q4 2026.
"""

# Inject the context directly into the prompt
prompt_with_context = f"""
Use the context below to answer the question accurately.
If the answer is not in the context, say "I don't know based on the provided information."

Context:
{hardcoded_context}

Question: {question}
"""

print("\n=== WITH HARD-CODED CONTEXT ===")
print(ask_gemini(prompt_with_context))
```

-------

## The Problem With Hard-Coded Context

This works — but it doesn't scale:

- ❌ We can't hard-code thousands of documents
- ❌ We can't predict which context is relevant for every possible question
- ❌ LLMs have a **context window limit** and we can't dump an entire knowledge base into a prompt
- ❌ Updating hard-coded context requires manual code changes
