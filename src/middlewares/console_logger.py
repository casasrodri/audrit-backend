import json

from fastapi import Request


async def console_log(request: Request, call_next):
    body = await request.body()
    if body:
        try:
            print("  >> BODY:", json.loads(body))
        except (UnicodeDecodeError, json.JSONDecodeError):
            print("  >> BODY: Encoded data")

    response = await call_next(request)
    return response
