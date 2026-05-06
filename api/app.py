from google import genai
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse

load_dotenv()

localdb = []

# Write a FastAPI app with one POST endpoint that calls the Anthropic API and streams the response
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
CHUNK_SIZE = 500
OVERLAP = 50
app = FastAPI()


@app.post('/')
def welcome():
    return {'message': "Hello, I Am ScaffDoc!"}


@app.get('/emi')
async def call_gemini():
    response = await client.aio.models.generate_content(
        model='gemini-2.5-flash',
        contents='What are the colors of the rainbow in one sentence'
    )
    return {'message': response.text}


@app.post('/stream')
async def stream_gemini():
    async def event_generator():
        stream = await client.aio.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents='What are the colors of the rainbow in one sentence'
        )

        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    return StreamingResponse(event_generator(), media_type='text/plain')


@app.post('/ingest')
async def ingest_text(text: str):
    chunks = [
        text[i:i + CHUNK_SIZE]
        for i in range(0, len(text), CHUNK_SIZE - OVERLAP)
    ]
    localdb.extend(chunks)
    return {'stored': len(chunks), 'total': len(localdb)}
