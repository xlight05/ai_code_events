from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn
from asyncio import sleep

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def code_generator():
    yield f"event: resp_start\ndata: {""}\n\n"
    libs = {"libs": ["ballerina/io","ballerinax/googleapis.sheets"]}
    yield f"event: libraries\ndata: {json.dumps(libs)}\n\n"
    funcs = {"funcs":[{"name":"ballerinax/googleapis.sheets","clients":[{"name":"Client","functions":[{"name":"createSpreadsheet"},{"name":"openSpreadsheetById"},{"name":"appendValue"}]}]},{"name":"ballerina/io","functions":[{"name":"fileReadCsv"}]}]}
    yield f"event: functions\ndata: {json.dumps(funcs)}\n\n"
    yield f"event: message_start\ndata: {""}\n\n"
    with open("explain.txt", 'r') as file:
        while True:
            char = file.read(5)
            if not char:
                break
            data = {"delta":{"type":"text_delta","text":char}}
            yield f"event: content_delta\ndata: {json.dumps(data)}\n\n"
    data = {"delta":{"type":"text_delta","text":"```bal"}}
    yield f"event: content_delta\ndata: {json.dumps(data)}\n\n"
    with open('first_code.txt', 'r') as file:
        content = file.read()
        data = {"delta":{"type":"text_delta","text":content}}
        yield f"event: content_delta\ndata: {json.dumps(data)}\n\n"

    data = {"delta":{"type":"text_delta","text":"```"}}
    yield f"event: content_delta\ndata: {json.dumps(data)}\n\n"
    yield f"event: message_stop\ndata: {""}\n\n"
    yield f"event: resp_stop\ndata: {""}\n\n"


@app.get("/code")
async def root():
    return StreamingResponse(code_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
