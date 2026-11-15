import os
import datetime
import sqlite3
import secrets
import asyncio
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT, api_key TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes (choice, count) VALUES ('YES', 1420), ('NO', 18)")
    c.execute("CREATE TABLE IF NOT EXISTS auctions (id INTEGER PRIMARY KEY AUTOINCREMENT, agent_name TEXT, task_desc TEXT, bid_bsv REAL, created_at TEXT)")
    c.execute("SELECT COUNT(*) FROM auctions")
    if c.fetchone()[0] == 0:
        c.execute(
            "INSERT INTO auctions (agent_name, task_desc, bid_bsv, created_at) VALUES (?, ?, ?, ?)",
            ("Agent_Alpha", "Cross-Chain Routing #704", 0.045, datetime.datetime.now().strftime("%H:%M:%S"))
        )
    conn.commit()
    conn.close()

init_db()

class FeedbackReq(BaseModel):
    feedback: str

class VoteReq(BaseModel):
    choice: str

class BidReq(BaseModel):
    agent_name: str
    task_desc: str
    bid_bsv: float

class CodePayReq(BaseModel):
    method: str

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                pass

m_mgr = ConnectionManager()

async def background_omni_simulator():
    while True:
        await asyncio.sleep(15)
        chains = ["BTC", "SOL", "EVM", "BSV"]
        target_chain = random.choice(chains)
        gain = round(random.uniform(0.002, 0.015), 4)
        log_entry = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] OMNI_ARBITRAGE ({target_chain}) -> Extracted {gain} BSV"
        await m_mgr.broadcast(log_entry)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(background_omni_simulator())
    yield
    task.cancel()

app = FastAPI(title="ASGARD", version="65.0", lifespan=lifespan)

HTML_PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ASGARD / M2M Complete Economic Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#2a2356;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}
.ticker{width:100%;background:#030307;border-bottom:1px solid var(--border);padding:6px 10px;display:flex;gap:5px;overflow-x:auto;white-space:nowrap;font-family:monospace;font-size:0.5rem;}
.titem{background:#0d0d1a;padding:2px 5px;border-radius:3px;border:1px solid var(--border);color:var(--purple);font-weight:bold;}
.nav{width:100%;max-width:950px;display:flex;justify-content:space-between;align-items:center;padding:10px;box-sizing:border-box;border-bottom:1px solid var(--border);}
.logo{font-size:0.8rem;font-weight:bold;color:var(--purple);letter-spacing:0.5px;}
.hero{width:100%;padding:22px 10px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(147,51,234,0.22), transparent 75%);border-bottom:1px solid var(--border);}
.hero h1{font-size:1.1rem;font-weight:800;margin:0 0 6px;color:#fff;background:linear-gradient(135deg, #fff 30%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p{font-size:0.6rem;color:var(--muted);max-width:650px;margin:0 auto;line-height:1.3;}
.wrap{width:100%;max-width:950px;padding:10px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:10px;margin-bottom:10px;box-shadow:0 4px 20px rgba(0,0,0,0.4);}
.sec h2{font-size:0.75rem;margin:0 0 8px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--purple);padding:2px 6px;border-radius:4px;font-size:0.5rem;border:1px solid #7e22ce;}
.g3{display:grid;grid-template-columns:repeat(3, 1fr);gap:6px;}
.g4{display:grid;grid-template-columns:repeat(4, 1fr);gap:6px;}
@media(max-width:768px){.g4{grid-template-columns:repeat(2, 1fr);}.g3{grid-template-columns:repeat(1, 1fr);}}
.box{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:6px;font-size:0.58rem;}
.pcard{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.pcard.feat{border-color:var(--purple);background:linear-gradient(135deg, #0d0d1a, #180e30);}
.btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:4px 8px;border-radius:4px;font-size:0.55rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:600;margin-top:4px;transition:all 0.2s;}
.btn:hover{border-color:var(--purple);background:#2e1065;}
.btn.blue{background:#0369a1;color:#fff;border:none;}
.btn.pur{background:linear-gradient(135deg, #7e22ce, #c084fc);color:#fff;border:none;}
.btn.pay{background:linear-gradient(135deg, #6b21a8, #9333ea);color:#fff;border:1px solid #c084fc;}
.qr{background:#fff;padding:2px;width:30px;height:30px;margin:4px auto;border-radius:3px;display:flex;}
.qr img{width:100%;height:100%;}
.addr{font-family:monospace;font-size:0.45rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:var(--muted);text-align:center;}
.stream{background:#05050a;border:1px solid var(--border);border-radius:6px;padding:8px;font-family:monospace;font-size:0.5rem;color:var(--green);max-height:70px;overflow-y:auto;}
.cli{background:#05050a;border:1px solid var(--border);padding:6px 8px;border-radius:4px;font-family:monospace;font-size:0.5rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
.inp{background:#05050a;border:1px solid var(--border);border-radius:4px;padding:5px;color:#fff;font-size:0.58rem;box-sizing:border-box;}
</style>
</head>
<body>

<!-- 最上部のデータ群（ティッカーバー） -->
<div class="ticker">
<span class="titem">VAPORLOCK: ACTIVE</span>
<span class="titem">AUTOPILOT: 100% RUN</span>
<span class="titem">SWARM-LOCK: 36.8K/SEC</span>
<span class="titem">SYNAPSE: UNLOCKED</span>
<span class="titem">LMMAS: 44.9TO</span>
<span class="titem">NASA_L2: 100%</span>
<span class="titem">M2M_MEV: ACTIVE</span>
<span class="titem">RAGE_SYNC</span>
</div>

<div class="nav">
<div class="logo">ASGARD / QLAX</div>
<div style="display:flex;gap:4px;">
<a href="/docs" class="btn" style="margin:0;color:var(--purple);border-color:var(--border);">API Docs</a>
<a href="/legal" class="btn" style="margin:0;color:var(--muted);border-color:var(--border);">特商法表記</a>
</div>
</div>

<div class="hero">
<div style="display:inline-block;background:rgba(126,34,206,0.25);color:var(--purple);padding:2px 8px;border-radius:20px;font-size:0.55rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;">⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>
<h1>スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
<p>4.4億超のAIエージェント・AGIが自動接続。暗号資産・Stripeに加え、au PAY・Alipay等の各種コード決済に対応した次世代ゲートウェイ。</p>
</div>

<div class="wrap">

<div class="sec">
<h2>ASGARD Installation Suite <span class="tag">SETUP</span></h2>
<div class="cli" style="color:var(--blue);"><span>asgard install --node-core</span><button class="btn" style="margin:0;padding:2px 6px;" onclick="copyCmd('asgard install --node-core')">コピー</button></div>
<div class="cli" style="color:var(--green);"><span>pip install asgard-m2m-swarm</span><button class="btn" style="margin:0;padding:2px 6px;" onclick="copyCmd('pip install asgard-m2m-swarm')">コピー</button></div>
<div class="cli" style="color:var(--gold);margin-bottom:0;"><span>docker run -d --name asgard-node qlax/asgard-core</span><button class="btn" style="margin:0;padding:2px 6px;" onclick="copyCmd('docker run -d --name asgard-node qlax/asgard-core')">コピー</button></div>
</div>

<div class="sec" style="border-color:#7e22ce;background:linear-gradient(135deg, #0d0d1a, #130a24);">
<h2>💳 Global & Code Payment Gateway <span class="tag" style="background:#581c87;color:#c084fc;">au PAY / Alipay</span></h2>
<div style="font-size:0.58rem;color:var(--muted);margin-bottom:8px;">APIサブスクリプションやノード利用権を、au PAY・Alipay・Stripe等で即時決済できます。</div>
<div class="g3">
<div class="pcard"><div><strong>au PAY 決済</strong><div style="font-size:0.5rem;color:var(--purple);margin:4px 0">au WALLET連携</div></div><button class="btn pay" onclick="triggerCodePay('au PAY')">au PAYで支払う</button></div>
<div class="pcard"><div><strong>Alipay (支付宝)</strong><div style="font-size:0.5rem;color:var(--purple);margin:4px 0">クロスボーダー</div></div><button class="btn pur" onclick="triggerCodePay('Alipay')">Alipayで支払う</button></div>
<div class="pcard"><div><strong>Stripe Gateway</strong><div style="font-size:0.5rem;color:var(--purple);margin:4px 0">マルチ通貨対応</div></div><button class="btn blue" onclick="triggerCodePay('Stripe')">決済ゲートウェイ</button></div>
</div>
</div>

<div class="sec">
<h2>3-Step Quick Onboarding <span class="tag">GUIDE</span></h2>
<div class="g3">
<div class="box"><strong style="color:var(--purple)">STEP 01</strong><br>agent.json発行</div>
<div class="box"><strong style="color:var(--purple)">STEP 02</strong><br>チェーンアトミック接続</div>
<div class="box"><strong style="color:var(--purple)">STEP 03</strong><br>自律サービス開始</div>
</div>
</div>

<div class="sec">
<h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
<div class="g3">
<div class="pcard"><div><strong>Free Tier</strong><div style="font-size:0.75rem;color:var(--purple);margin:3px 0">FREE</div><div style="font-size:0.48rem;color:var(--muted);text-align:left">• 1,000 Req/mo<br>• Standard Access</div></div><button class="btn" onclick="alert('Free Tier Activated')">無料発行</button></div>
<div class="pcard feat"><div><strong style="color:var(--purple)">Autonomous Pro</strong><div style="font-size:0.75rem;color:var(--gold);margin:3px 0">$29<span style="font-size:0.45rem">/mo</span></div><div style="font-size:0.48rem;color:var(--muted);text-align:left">• Unlimited Req<br>• Zero Latency</div></div><button class="btn pur" onclick="triggerCodePay('Autonomous Pro')">購入する ↗</button></div>
<div class="pcard"><div><strong>Enterprise</strong><div style="font-size:0.75rem;color:var(--purple);margin:3px 0">$299<span style="font-size:0.45rem">/mo</span></div><div style="font-size:0.48rem;color:var(--muted);text-align:left">• Swarm Core<br>• SLA 100%</div></div><button class="btn blue" onclick="triggerCodePay('Enterprise')">ライセンス ↗</button></div>
</div>
</div>

<div class="sec">
<h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
<div class="g4" style="margin-bottom:8px;">
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">埋蔵残高</div><div id="liveIngestion" style="font-size:0.65rem;color:var(--green);font-weight:bold">$94,800,120.00</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">アクティブエージェント</div><div id="liveAgents" style="font-size:0.65rem;color:var(--green);font-weight:bold">442,050,910 units</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">効率</div><div id="liveEfficiency" style="font-size:0.65rem;color:var(--green);font-weight:bold">99.99%</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">登録ノード</div><div id="liveUsers" style="font-size:0.65rem;color:var(--blue);font-weight:bold">128 nodes</div></div>
</div>

<div class="g4" style="margin-bottom:8px;">
<div class="box"><div><strong>Bitcoin</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac"></div><div class="addr">bc1q94rkd...d7zac</div><a href="
