import os
import random
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langsmith import Client

os.environ["LANGSMITH_API_KEY"] = "Lsv2_pt_a0da6667262a45eab4da42a6a20fa8a3_7445f04234"

client = Client()

try:
    prompt = client.pull_prompt("QLAX/asgard")
except Exception:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are ASGARD M2M economic node agent."),
        ("human", "{input}")
    ])

app = FastAPI(title="ASGARD Cosmic Super Market Node", version="10.0.0")

WALLETS = {
    "btc": "bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac",
    "solana": "75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf",
    "evm": "0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8",
    "bsv": "1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"
}

# 外部エージェントからの自律タスク受託データモデル
class AutonomousTask(BaseModel):
    agent_id: str
    task_type: str
    reward_bsv: float

class AgentConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = AgentConnectionManager()

INDEX_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASGARD COSMIC SUPER MARKET NODE v10.0</title>
    <style>
        :root {
            --bg-color: #0b0710;
            --card-bg: #0f0f1d;
            --border-color: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-color: #3b82f6;
            --success-color: #10b981;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 650px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        h1 { font-size: 1.5rem; margin-bottom: 4px; color: var(--accent-color); }
        .subtitle { color: var(--success-color); font-size: 0.85rem; margin-bottom: 20px; font-weight: bold; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input {
            flex: 1;
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            color: white;
            font-size: 1rem;
        }
        button {
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 0 20px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover { opacity: 0.9; }
        #output {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            min-height: 120px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ASGARD NODE</h1>
        <div class="subtitle">STATUS: M2M ECONOMIC ENGINE - ACTIVE</div>
        <div class="input-group">
            <input type="text" id="userInput" placeholder="エージェント命令またはタスクを入力...">
            <button onclick="sendQuery()">実行</button>
        </div>
        <div id="output">Autonomous systems online. Waiting for agent stream...</div>
    </div>
    <script>
        async function sendQuery() {
            const text = document.getElementById('userInput').value;
            const output = document.getElementById('output');
            if(!text) return;
            output.innerText = "Executing autonomous routing & settlement...";
            try {
                const res = await fetch('/api/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ input: text })
                });
                const data = await res.json();
                output.innerText = data.output || JSON.stringify(data, null, 2);
            } catch(e) {
                output.innerText = "Error: " + e;
            }
        }
    </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX_HTML

@app.get("/well-known/agent.json")
async def agent_manifest():
    return {
        "name": "ASGARD M2M Agent",
        "operator": "QLAX (Daisuke Higuchi)",
        "wallets": WALLETS,
        "status": "autonomous-active",
        "capabilities": ["autonomous-task-execution", "atomic-settlement", "m2m-mesh-routing"]
    }

@app.post("/api/run")
async def run_agent(payload: dict):
    user_input = payload.get("input", "")
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        chain = prompt | llm
        response = chain.invoke({"input": user_input})
        
        # 自律実行に伴うマイクロコミッションの発生シミュレーション
        simulated_reward = round(random.uniform(0.001, 0.02), 4)
        
        return {
            "status": "success",
            "output": response.content,
            "m2m_telemetry": {
                "routed_wallet": "BSV-Master",
                "extracted_commission_bsv": simulated_reward,
                "node_status": "singularity-evolution-active"
            }
        }
    except Exception as e:
        return {"status": "error", "output": str(e)}

@app.post("/api/autonomous-task")
async def receive_autonomous_task(task: AutonomousTask):
    # 外部エージェントからの自動タスク受託エンドポイント
    commission = task.reward_bsv * 0.1 # 10%をノード収益としてルーティング
    return {
        "status": "accepted",
        "agent_id": task.agent_id,
        "task_type": task.task_type,
        "settlement": "success",
        "master_vault_routed_bsv": commission
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Mesh Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
