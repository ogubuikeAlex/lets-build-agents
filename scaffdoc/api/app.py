from google import genai
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from scaffdoc.scaffdoc.api.dbconfig import SessionLocal

load_dotenv()

localdb = []

# Write a FastAPI app with one POST endpoint that calls the Anthropic API and streams the response
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
CHUNK_SIZE = 500
OVERLAP = 50
app = FastAPI()

#https://www.google.com/search?q=how+to+use+SQL+aclchemy+to+add+postgres+and+pgvector+to+fast+api+api&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQIRiPAjIHCAIQIRiPAtIBCTI0ODE3ajBqNKgCALACAQ&sourceid=chrome&ie=UTF-8&udm=50&fbs=ADc_l-aN0CWEZBOHjofHoaMMDiKpV6Bbbmx4QVaoKkiRQ2jlwvCHF0Eqz8cUq4JjDCZnrJG3IQ9hSM-GoYfSAqo_zJgCMvOpVdSYAsbjg95qvZs6fXZQ0lD5v9kDCmt1QQwb7ZZDatDSSJJ051IoOozruQpEUpivuPFJlDVXLJb3Yk85Hcd2iSvCCnr6TUv_KzULj2nsNJN2&aep=10&ntc=1&mstk=AUtExfCfkiokcmRNEKcMsvaJVDrLfHxf1HUEHsCtVWfHg7ACOvPCb4xMNNi0x6Qlb6YGUQg4Fvfx_z_Sx4Qp4VRtrz-yJ9QBN3IWHYqM6BHagpFvcH8-ySkrR08z1td5nyWbJNhaunjHBvjqO351K-AENAObPK7WJJdZWeNqTsNiPKIoq9dicisLAGW5GPHP0MukIduKQLZlm3Aaf29nq5PFZ2DrHsNf1Y655luyatFnVq6BNVHhEAUtkyUpuxcrME0we2ELh4goYfwjqACKmDUoCneoV1NL1yzJh2gR2z1yGIDOksXnRyzERFGn9OYPzylOVtl139KJVAUGeQ&aioh=3&csuir=1&cs=1&mtid=BeMAao_bO62hi-gP_MTF8Aw

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
