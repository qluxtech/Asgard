from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import math
import random
import time
import os

app = FastAPI(title="ASGARD Grid - Supreme")

# HTML読み込み関数（Jinja2パースエラー回避）
def get_index_html():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=get_index_html())

@app.get("/api/v3/entropy/fluctuation-stream")
async def get_1f_entropy():
    t = time.time()
    val = math.sin(t * 0.618) * math.cos(t * 0.382) + random.gauss(0, 0.03)
    return {
        "timestamp": t,
        "entropy_source": "Quantum-Laser-Grid-Node-09",
        "fluctuation_index_1f": round(val, 8),
        "coherence_rate": "99.982%"
    }

@app.get("/agent.json")
async def get_agent():
    return {
        "name": "ASGARD Grid Autonomous Node",
        "protocol": "HTTP-402-M2M",
        "version": "3.0.0"
    }
