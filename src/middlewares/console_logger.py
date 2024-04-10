from fastapi import FastAPI, Request
import json


def console_logger_midd(app: FastAPI):

    @app.middleware("http")
    async def console_log(request: Request, call_next):
        body = await request.body()
        if body:
            print("  >> BODY:", json.loads(body))

        response = await call_next(request)
        return response