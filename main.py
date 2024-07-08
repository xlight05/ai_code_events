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
    yield f"event: libraries\ndata: {"[\"ballerina/io\",\"ballerinax/googleapis.sheets\"]"}\n\n"
    yield f"event: functions\ndata: {'[{"name":"ballerinax/googleapis.sheets","clients":[{"name":"Client","functions":[{"name":"createSpreadsheet"},{"name":"openSpreadsheetById"},{"name":"appendValue"}]}]},{"name":"ballerina/io","functions":[{"name":"fileReadCsv"}]}]'}\n\n"
    yield f"event: message_start\ndata: {""}\n\n"
    with open("first.txt", 'r') as file:
        while True:
            char = file.read(5)
            if not char:
                break
            data = {"delta":{"type":"text_delta","text":char}}
            yield f"event: content_delta\ndata: {json.dumps(data)}\n\n"
    yield f"event: message_stop\ndata: {""}\n\n"
   
    yield f"event: compile_started\ndata: {""}\n\n"
    yield f"event: diagnostics\ndata: {"[\"ERROR [balSource17696242700046434752.bal:(30:40,30:56)] incompatible types: expected \'(string[][]|map<anydata>[])\', found \'(int|string|decimal)[][]\'\"]"}\n\n"
    
    yield f"event: message_start\ndata: {""}\n\n"

    with open("second.txt", 'r') as file:
        while True:
            char = file.read(5)
            if not char:
                break
            data = {"delta":{"type":"text_delta","text":char}}
            yield f"event: content_delta\ndata: {json.dumps(data)}\n\n"

    yield f"event: message_stop\ndata: {""}\n\n"
    yield f"event: resp_stop\ndata: {""}\n\n"


@app.get("/code")
async def root():
    return StreamingResponse(code_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
