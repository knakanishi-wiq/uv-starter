import random

from fastapi import FastAPI
from pydantic import BaseModel

from uv_starter.demo_module import add

app = FastAPI()


class RequestPayload(BaseModel):
    num_1: int
    num_2: int


@app.post("/")
async def root(request_payload: RequestPayload):
    sum = add(request_payload.num_1, request_payload.num_2)
    return {"message": f"the sum is {sum}"}
