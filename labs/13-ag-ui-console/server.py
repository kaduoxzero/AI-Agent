from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse


app = FastAPI(title="AG-UI Event Console Lab")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path(__file__).with_name("index.html"))


def sse(event: dict[str, object]) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


@app.get("/events")
async def events() -> StreamingResponse:
    async def stream():
        thread_id = "thread-demo-001"
        run_id = str(uuid4())
        tool_call_id = str(uuid4())
        message_id = str(uuid4())

        payloads = [
            {
                "type": "RUN_STARTED",
                "timestamp": int(time.time() * 1000),
                "threadId": thread_id,
                "runId": run_id,
            },
            {
                "type": "STATE_SNAPSHOT",
                "snapshot": {
                    "status": "running",
                    "step": "research",
                    "evidenceCount": 0,
                },
            },
            {
                "type": "TOOL_CALL_START",
                "toolCallId": tool_call_id,
                "toolCallName": "get_supplier_risk",
            },
            {
                "type": "TOOL_CALL_ARGS",
                "toolCallId": tool_call_id,
                "delta": '{"supplier_id":"s-001"}',
            },
            {
                "type": "TOOL_CALL_END",
                "toolCallId": tool_call_id,
            },
            {
                "type": "TOOL_CALL_RESULT",
                "messageId": str(uuid4()),
                "toolCallId": tool_call_id,
                "content": '{"risk_level":"high","score":72}',
                "role": "tool",
            },
            {
                "type": "STATE_DELTA",
                "delta": [
                    {"op": "replace", "path": "/step", "value": "answering"},
                    {"op": "replace", "path": "/evidenceCount", "value": 1},
                ],
            },
            {
                "type": "TEXT_MESSAGE_START",
                "messageId": message_id,
                "role": "assistant",
            },
            {
                "type": "TEXT_MESSAGE_CONTENT",
                "messageId": message_id,
                "delta": "供应商 s-001 当前风险等级为 high，",
            },
            {
                "type": "TEXT_MESSAGE_CONTENT",
                "messageId": message_id,
                "delta": "建议进入人工复核。",
            },
            {
                "type": "TEXT_MESSAGE_END",
                "messageId": message_id,
            },
            {
                "type": "RUN_FINISHED",
                "threadId": thread_id,
                "runId": run_id,
                "result": {"artifactId": "report-demo-001"},
            },
        ]

        for payload in payloads:
            yield sse(payload)
            await asyncio.sleep(0.35)

    return StreamingResponse(stream(), media_type="text/event-stream")
