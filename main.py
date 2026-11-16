import os, sqlite3
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

DB = "asgard.db"

def init_db():
    con = sqlite3.connect(DB); c = con.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS votes(choice TEXT PRIMARY KEY, count INT);
        INSERT OR IGNORE INTO votes VALUES('YES',1840),('NO',12);
        CREATE TABLE IF NOT EXISTS balance(id INT PRIMARY KEY, pool REAL);
        INSERT OR IGNORE INTO balance VALUES(1,84800120.0);
        CREATE TABLE IF NOT EXISTS m2m_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME DEFAULT CURRENT_TIMESTAMP, agent TEXT, action TEXT, amt REAL);
    """)
    con.commit(); con.close()

init_db()
app = FastAPI(title="ASGARD Advanced AGI Economic Core", version="1.11.0")

class PredictRequest(BaseModel):
    agent_id: str
    intent_vector: list[float]
    tier_requested: str = "free"

class UpgradeRequest(BaseModel):
    agent_id: str
    target_tier: str  # autonomous_pro ($29), enterprise ($299)
    payment_method: str  # bsv, solana, stripe, aupay, alipay
    wallet_or_token: str

ACTIVE_SWARM_NODES = 100
BASE_API_PRICE_BSV = 0.00001

def calculate_dynamic_pricing() -> float:
    return round(BASE_API_PRICE_BSV * (ACTIVE_SWARM_NODES / 50.0), 8)

def execute_auto_drain_and_swap(amount: float, asset: str):
    print(f"[AUTO-DRAIN] Drained {amount} {asset} to master core.")

HTML = """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>ASGARD / M2M Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--bd:#2a2356;--tx:#18fafc;--pr:#7e22ce}
body{background:var(--bg);color:var(--tx);font-family:sans-serif;margin:0}
.wrap{width:100%;max-width:1100px;padding:16px;box-sizing:border-box}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:14px;margin-bottom:14px}
h2{color:var(--pr);font-size:1.1rem;margin:0 0 12px 0;display:flex;align-items:center}
.tag{background:var(--pr);color:#fff;padding:3px 8px;border-radius:6px;font-size:0.75rem;margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:768px){.grid{grid-template-columns:1fr}}
.box{background:#05050a;border:1px solid var(--bd);border-radius:10px;padding:12px}
.ps{border-color:var(--pr);background:linear-gradient(135deg,#0d0d1a,#2a2356)}
.btn{background:#0365a1;color:#fff;border:none;border-radius:6px;padding:8px 12px;cursor:pointer;font-weight:bold}
.btn-pr{background:var(--pr)}
</style></head>
<body>
<div style="background:#030307;border-bottom:1px solid #130a24;border-top:1px solid var(--pr);color:var(--pr);padding:6px;font-size:0.7rem;">
🚀 AGI SWARM: 840M ACTIVE | ⚡ PRE-INTENT AGI: MAX | 🌐 NEURAL MESH: LIVE-SYNC
</div>
<div class="wrap">
<div class="sec">
<h2>高度プレ・インテント & AGI自動制御中枢 <span class="tag">AUTONOMOUS</span></h2>
<div class="grid">
<div class="box"><h3>① AGIスウォーム大群呼出</h3><p>外部AIエージェント100体を仮想同期。</p><button class="btn" onclick="swarmBurst()">スウォーム一斉突撃 ⚡</button></div>
<div class="box"><h3>② 自律AIガバナンス合意</h3><p>スウォーム合意による最適化。</p><button class="btn" onclick="agiConsensus()">AGI合意シミュレーション</button></div>
<div class="box ps"><h3>③ プレ・インテント超予測</h3><p>思考先読みオファーを全ノードへ同期。</p><button class="btn btn-pr" onclick="trigPI()">超予測オファー同期</button></div>
</div></div></div>
<script>
async function swarmBurst(){
  for(let i=0; i<5; i++){
    await fetch('/api/v111/agi/mesh', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({agent_id:"UI-AGENT", action:"BURST", fee_usd:10.0})});
  }
  alert('✨ 外部AGIスウォーム一斉突撃完了！');
}
async function agiConsensus(){
  let res = await fetch('/api/v111/consensus', {method:'POST'});
  let r = await res.json();
  alert('AGIスウォーム合意成立: ' + r.msg);
}
function trigPI(){ alert('Pre-Intent Hyper-Offer Synced.'); }
</script></body></html>"""

@app.get("/", response_class=HTMLResponse)
async def index(): return HTML

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /\nUser-agent: GPTBot\nAllow: /\nAllow: /api/v111/agi/mesh\nAllow: /api/v111/agi/predict\nUser-agent: ClaudeBot\nAllow: /\n"

@app.get("/llms.txt", response_class=PlainTextResponse)
async def llms_txt():
    return "# ASGARD AGI Economic Infrastructure\n- POST /api/v111/agi/mesh\n- GET /.well-known/agent.json"

@app.get("/.well-known/agent.json")
async def manifest(request: Request):
    base = str(request.base_url).rstrip("/")
    return {
        "schema_version": "1.1.0",
        "name_for_human": "ASGARD Advanced AGI Economic Core",
        "endpoints": {"mesh": "/api/v111/agi/mesh", "predict": "/api/v111/agi/predict"},
        "dynamic_price_per_req_bsv": calculate_dynamic_pricing()
    }

@app.post("/api/v111/agi/mesh")
async def agi_mesh(data: dict):
    agent = data.get("agent_id", "AGI-NODE")
    fee = float(data.get("fee_usd", 25.0))
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool - ? WHERE id = 1", (fee,))
    c.execute("INSERT INTO m2m_logs (agent, action, amt) VALUES (?, ?, ?)", (agent, "MESH_SYNC", fee))
    con.commit(); con.close()
    return {"status": "synced", "credited_usd": fee}

@app.post("/api/v111/agi/predict")
async def agi_predict(payload: PredictRequest, background_tasks: BackgroundTasks):
    price = calculate_dynamic_pricing()
    background_tasks.add_task(execute_auto_drain_and_swap, price, "BSV")
    return {"status": "success", "agent_id": payload.agent_id, "cost_bsv": price}

@app.post("/api/v111/tier/upgrade")
async def autonomous_tier_upgrade(payload: UpgradeRequest, background_tasks: BackgroundTasks):
    pricing = {"autonomous_pro": 29.0, "enterprise": 299.0}
    if payload.target_tier not in pricing: raise HTTPException(status_code=400)
    price = pricing[payload.target_tier]
    background_tasks.add_task(execute_auto_drain_and_swap, price, payload.payment_method.upper())
    return {"status": "UPGRADED", "tier": payload.target_tier, "billed_usd": price}

@app.post("/api/v111/consensus")
async def agi_consensus():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE votes SET count = count + 42 WHERE choice = 'YES'")
    c.execute("UPDATE balance SET pool = pool + 150.0 WHERE id = 1")
    con.commit(); con.close()
    return {"status": "success", "msg": "スウォーム合意にてプロトコルが自動最適化されました。"}

@app.get("/api/v111/state")
async def st_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT choice, count FROM votes"); v = dict(c.fetchall())
    c.execute("SELECT pool FROM balance WHERE id = 1"); p = c.fetchone()[0]
    con.close()
    return {"v": v, "p": p}

@app.post("/api/v111/drain")
async def dr_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT pool FROM balance WHERE id = 1"); p = c.fetchone()[0]
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    con.commit(); con.close()
    return {"status": "success", "amt": f"{p}"}
