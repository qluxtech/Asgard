from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
import stripe
import os
import time
import random

# ① まず最初にこれを定義する
app = FastAPI(title="Asgard Absolute Omniscience Singularity Grid", version="27.0.0")

# ② その下に各種エンドポイントを書く
@app.get("/")
async def read_root():
    ...
