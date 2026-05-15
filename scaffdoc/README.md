# ENTERPRISE HYBRID RAG SYSTEM

## Introduction: LLM As a Blackbox
A Large Language Model (LLM) is an AI trained on vast data to predict and generate text.

The "black box" nature of LLMs refers to our inability to fully comprehend how these systems, which contain billions of parameters and complex, non-linear neural networks, transform inputs into specific outputs. 

While we can understand the high-level architecture and training processes, the exact reasoning path, internal decision-making processes, and the precise combination of weights leading to a specific output are generally too complex for a human to interpret.

-------

## Project Set up

#### 1. Install uv
Run the command matching the operating system. For Windows, use PowerShell. 

* Linux / macOS (Bash):

`curl -LsSf https://astral.sh/uv/install.sh | sh`

* Windows (PowerShell):

`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

------------------------------
#### 2. Init Environment
Run these commands in the terminal (Bash or PowerShell) to create the folder and initialize the environment. 

```bash
# Create folder and files
mkdir rag-project && cd rag-project
touch .env main.py

# Initialize a new uv project
uv init

# Add Google's Generative AI SDK
uv add google-generativeai dotenv
```

#### 3. Create env and python Script 
💡 Note: Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey) 

In your .env file. Add this and replace `Add-Your-actual-API-Key` in the code with your actual API key 
```txt 
GEMINI_API_KEY=Add-Your-actual-API-Key
```
In `main.py` paste the code below.
```python
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Setup API Key
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

async def ask_gemini(prompt):
    response = await client.aio.models.generate_content(
        model='gemini-2.5-flash',
        contents=f'{prompt}'
    )
    return {'prompt': prompt, 'message': f"RESPONSE: {response.text}\n{'-'*20}"}
```

#### Ask Question

```markdown
# Question 1: Known information

ask_gemini("What are the months of the year?")

# Question 2: Unknown/Future information
# Note: "Orra.xyz" and its collab with "Rome Protocol" are specific crypto/web3 startups the model has no real-time data on.

ask_gemini("When will Orra.xyz go live and collaborate with Rome protocol?")
```
------------------------------
#### 4. Run the Script
Use uv run to execute the file. It will automatically handle the virtual environment.

`uv run main.py`



## The Problems and Limitation of an LLM - No Context

From the example above, we see that while an LLM works like a magic blackbox, it cannot help us when we need information it simply wasn't trained on.


Attempt to resolve the isssue by adding context: Hard coded context
Question: What if we are able to get relevant context an add that to a query
What, Why and How of a rag system
	- Honorable mention: Enterprise Rag system
	- Data cleaning and Prep is necessary
What are the components of our Naive Semantic RAG system
	- Show A diagram
	- Indexing and Storing Our DB + A Search engine
		Why we need to index and why we need a search db
		LanceDB -> Our 007 here
	- Retrieve and Format User Query
	- Send Formatted Context-Rich Query To LLM
Adding RAGAS
Turning this into a Hybrid System:
	- Show Diagram For How It Combines
	- Show how to add an API call
Did RAGAS Improve with Hybrid Approach
