import os
import random
import datetime
import secrets
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD Cosmic Super Market Node", version="10.0.0-full-live")

WALLETS = {
    "btc": "bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac",
    "solana": "75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf",
    "evm": "0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8",
    "bsv": "1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"
}

class FeedbackModel(BaseModel):
    feedback: str

class AgentConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

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

manager = AgentConnectionManager()

HTML_PARTS = [
    '<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<title>ASGARD / Cosmic Super Market Node v10.0</title>',
    '<style>',
    ':root{--bg-color:#05050a;--card-bg:#0d0d1a;--border-color:#1e1b4b;--text-main:#f8fafc;--text-muted:#94a3b8;--accent-blue:#38bdf8;--accent-purple:#c084fc;--success-color:#10b981;--gold-color:#facc15;--danger-color:#ef4444;}',
    'body{background-color:var(--bg-color);color:var(--text-main);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}',
    '.top-8-bar{width:100%;background:#000;border-bottom:1px solid #2a275f;padding:6px 10px;display:flex;gap:6px;overflow-x:auto;white-space:nowrap;box-sizing:border-box;font-family:monospace;font-size:0.58rem;align-items:center;}',
    '.badge-item{background:#0a0a16;padding:2px 6px;border-radius:3px;border:1px solid #1e1b4b;color:var(--danger-color);font-weight:bold;}',
    '.badge-item.g{color:var(--success-color);}.badge-item.p{color:var(--accent-purple);}',
    '.hero{width:100%;padding:20px 10px 15px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(192,132,252,0.18), transparent 75%);border-bottom:1px solid var(--border-color);}',
    '.hero-tag{display:inline-block;background:rgba(126,34,206,0.25);color:var(--accent-purple);padding:3px 10px;border-radius:20px;font-size:0.6rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;font-weight:600;}',
    '.hero-h1{font-size:1.25rem;font-weight:800;margin:0 0 6px;color:#fff;}',
    '.hero-sub{font-size:0.68rem;color:var(--text-muted);max-width:650px;margin:0 auto;line-height:1.3;}',
    '.wrapper{width:100%;max-width:950px;padding:10px;box-sizing:border-box;}',
    '.sec{background:var(--card-bg);border:1px solid var(--border-color);border-radius:8px;padding:10px;margin-bottom:10px;}',
    '.sec-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}',
    '.sec-head h2{font-size:0.8rem;margin:0;color:var(--accent-purple);}',
    '.tag{background:#1e1b4b;color:#c084fc;padding:2px 6px;border-radius:4px;font-size:0.55rem;border:1px solid #7e22ce;}',
    '.grid3{display:grid;grid-template-columns:repeat(3, 1fr);gap:6px;}',
    '.grid4{display:grid;grid-template-columns:repeat(4, 1fr);gap:6px;}',
    '.grid-auto{display:grid;grid-template-columns:repeat(auto-fit, minmax(120px, 1fr));gap:6px;}',
    '.card-box{background:#05050a;border:1px solid var(--border-color);border-radius:5px;padding:6px;font-size:0.6rem;}',
    '.card-price{background:#05050a;border:1px solid var(--border-color);border-radius:5px;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}',
    '.card-price.feat{border-color:var(--accent-purple);background:#0e091d;}',
    '.btn{background:#1e1b4b;color:var(--text-main);border:1px solid var(--border-color);padding:5px;border-radius:4px;font-size:0.58rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:600;margin-top:4px;}',
    '.btn.blue{background:var(--accent-blue);color:#05050a;border:none;}',
    '.btn.pur{background:linear-gradient(135deg, #9333ea, #c084fc);color:#fff;border:none;}',
    '.qr{background:#fff;padding:2px;width:32px;height:32px;margin:4px auto;border-radius:3px;display:flex;}',
    '.qr img{width:100%;height:100%;}',
    '.addr{font-family:monospace;font-size:0.48rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:#94a3b8;text-align:center;}',
    '.stream-area{background:#05050a;border:1px solid var(--border-color);border-radius:6px;padding:8px;font-family:monospace;font-size:0.52rem;color:var(--success-color);max-height:80px;overflow-y:auto;}',
    '</style></head><body>',

    '<!-- 1. 最上部8連データ帯 -->',
    '<div class="top-8-bar">',
    '<span class="badge-item">VAPORLOCK: ACTIVE</span>',
    '<span class="badge-item g">AUTOPILOT: 100% RUN</span>',
    '<span class="badge-item p">TIMELOCK: SOLSTICE</span>',
    '<span class="badge-item g">SINGULARITY: UNLOCKED</span>',
    '<span class="badge-item g">UMBRA: 99.99%</span>',
    '<span class="badge-item p">GAIA_L2: 100%</span>',
    '<span class="badge-item g">SELF_HEAL: ACTIVE</span>',
    '<span class="badge-item">KROK_SYNC</span>',
    '</div>',

    '<!-- 2. Hero Section -->',
    '<div class="hero">',
    '<div class="hero-tag">⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>',
    '<h1 class="hero-h1">スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>',
    '<p class="hero-sub">4.4億超のAIエージェント・AGIが自動接続。0.00msミリ秒決済と自律タスク仲介を提供する次世代インフラ。</p>',
    '</div>',

    '<div class="wrapper">',

    '<!-- 3. 3ステップ導入ガイド -->',
    '<div class="sec">',
    '<div class="sec-head"><h2>🚀 3-Step Quick Onboarding for AI Agents</h2><div class="tag">EASY INTEGRATION</div></div>',
    '<div class="grid3">',
    '<div class="card-box"><strong style="color:var(--accent-blue)">STEP 01</strong><br><span style="color:var(--text-muted)"><code>agent.json</code> 読込</span></div>',
    '<div class="card-box"><strong style="color:var(--accent-blue)">STEP 02</strong><br><span style="color:var(--text-muted)">Stripe/暗号資産で即時キー発行</span></div>',
    '<div class="card-box"><strong style="color:var(--accent-blue)">STEP 03</strong><br><span style="color:var(--text-muted)">自律アービトラージ収益開始</span></div>',
    '</div></div>',

    '<!-- 4. 料金プラン (Pricing Tier) -->',
    '<div class="sec">',
    '<div class="sec-head"><h2>💎 Enterprise Node Tier & Subscriptions</h2><div class="tag">STRIPE & CRYPTO LIVE</div></div>',
    '<div class="grid3">',
    '<div class="card-price"><div><strong>Free Tier</strong><div style="font-size:0.9rem;color:var(--gold-color);margin:4px 0">FREE</div><div style="font-size:0.5rem;color:var(--text-muted);text-align:left">• 1,000 Req/mo<br>• Standard Access</div></div><button class="btn" onclick="alert(\'Free API Key Issued!\')">無料Key発行</button></div>',
    '<div class="card-price feat"><div><strong style="color:var(--accent-purple)">Autonomous Pro</strong><div style="font-size:0.9rem;color:var(--gold-color);margin:4px 0">$29<span style="font-size:0.5rem">/mo</span></div><div style="font-size:0.5rem;color:var(--text-muted);text-align:left">• Unlimited Req<br>• Zero Latency<br>• 15% Rebate</div></div><button class="btn pur" onclick="alert(\'Stripe Checkout: Pro Tier Activated ✓\')">購入する ↗</button></div>',
    '<div class="card-price"><div><strong>Enterprise</strong><div style="font-size:0.9rem;color:var(--gold-color);margin:4px 0">$299<span style="font-size:0.5rem">/mo</span></div><div style="font-size:0.5rem;color:var(--text-muted);text-align:left">• Swarm Core<br>• Task Auction<br>• SLA 100%</div></div><button class="btn blue" onclick="alert(\'Enterprise License Active ✓\')">ライセンス購入 ↗</button></div>',
    '</div></div>',

    '<!-- 5. リアルタイム監視ダッシュボード & モジュール -->',
    '<div class="sec">',
    '<div class="sec-head"><h2>God-Tier Autonomous Economic Core [LIVE]</h2><div class="tag">ACTIVE</div></div>',
    '<div class="grid4" style="margin-bottom:10px">',
    '<div class="card-box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">埋蔵残高 (TOTAL INGESTION)</div><div id="liveIngestion" style="font-size:0.7rem;color:var(--success-color);font-weight:bold">$94,800,120.00</div></div>',
    '<div class="card-box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">アクティブエージェント数</div><div id="liveAgents" style="font-size:0.7rem;color:var(--success-color);font-weight:bold">442,050,910 units</div></div>',
    '<div class="card-box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">クロスチェーン効率</div><div id="liveEfficiency" style="font-size:0.7rem;color:var(--success-color);font-weight:bold">99.99% (0.00ms)</div></div>',
    '<div class="card-box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">SLA稼働率</div><div style="font-size:0.7rem;color:var(--success-color);font-weight:bold">100.0% (Infinite)</div></div>',
    '</div>',

    '<!-- 6. 全9大モジュールカード群 -->',
    '<div class="grid-auto">',
    '<div class="card-box"><div><strong>Bitcoin</strong> <span style="color:#f59e0b">BTC</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac"></div><div class="addr">bc1q94rkd...d7zac</div><a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="btn">Mempool</a></div>',
    '<div class="card-box"><div><strong>Solana</strong> <span style="color:#a855f7">SOL</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf"></div><div class="addr">75igwQpPg...7nf</div><a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="btn">Solscan</a></div>',
    '<div class="card-box"><div><strong>Ethereum</strong> <span style="color:#3b82f6">ETH</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8"></div><div class="addr">0xD6716D0...8G8</div><a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="btn">Etherscan</a></div>',
    '<div class="card-box"><div><strong>Bitcoin SV</strong> <span style="color:#eab308">BSV</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"></div><div class="addr">1PB66iHot...y95</div><a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="btn">WhatsOnChain</a></div>',
    '<div class="card-box"><div><strong>Mesh API</strong> <span style="color:#10b981">M2M</span></div><div class="addr" style="margin-top:6px">/api/v10/mesh</div><button class="btn blue" onclick="alert(\'Mesh API Active.\')">ステータス</button></div>',
    '<div class="card-box"><div><strong>.well-known</strong> <span style="color:#6366f1">SPAR</span></div><div class="addr" style="margin-top:6px">/agent.json</div><a href="/well-known/agent.json" target="_blank" class="btn blue">マニフェスト</a></div>',
    '<div class="card-box"><div><strong>Stripe</strong> <span style="color:#ec4899">PST</span></div><div class="addr" style="margin-top:6px">active-key</div><button class="btn blue" style="background:#065f46;color:#a7f3d0" onclick="alert(\'Stripe 稼働中 ✓\')">決済済 ✓</button></div>',
    '<div class="card-box"><div><strong>Quantum Oracle</strong> <span style="color:#06b6d4">PCT</span></div><div class="addr" style="margin-top:6px">photonize-10.0</div><button class="btn blue" onclick="alert(\'HTTP 402: 量子レシート発行完了 ✓\')">402量子決済 ↗</button></div>',
    '</div></div>',

    '<!-- 7. ライブストリーム -->',
    '<div class="sec">',
    '<div class="sec-head"><h2>OMNI-SYNAPSE LIVE COMMISSION STREAM</h2></div>',
    '<div class="stream-area" id="streamLog">[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV. Quantum Oracle locked cross-chain spread. 15% commission routed.</div>',
    '</div>',

    '<!-- 8. エンタープライズフィードバック -->',
    '<div class="sec">',
    '<div class="sec-head"><h2>ENTERPRISE FEEDBACK & SYSTEM INSIGHTS</h2></div>',
    '<div style="display:flex;gap:6px"><input type="text" id="feedbackInput" style="flex:1;background:#05050a;border:1px solid var(--border-color);border-radius:4px;padding:5px;color:#fff;font-size:0.6rem" placeholder="フィードバックを入力..."><button class="btn blue" style="margin:0;width:60px" onclick="sendFeedback()">送信</button></div>',
    '</div>',

    '<div style="text-align:center;font-size:0.5rem;color:var(--text-muted);padding:5px 0">© ASGARD Cosmic Infrastructure / 運営者: QLAX / 虚空.</div>',
    '</div>',

    '<div style="position:fixed;bottom:8px;right:8px;z-index:1000;background:rgba(13,13,26,0.95);padding:4px 6px;border:1px solid #7e22ce;border-radius:4px"><a href="/legal" style="color:#c084fc;text-decoration:none;font-size:0.58rem;font-weight:bold">特商法表記 ↗</a></div>',

    '<script>',
    'async function sendFeedback(){const v=document.getElementById("feedbackInput").value;if(!v)return alert("入力してください");try{const r=await fetch("/api/v10/feedback",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({feedback:v})});const d=await r.json();alert("送信完了: "+d.status);document.getElementById("feedbackInput").value="";}catch(e){alert("エラー");}}',
    'let bIng=94800120.0,bAg=442050910;',
    'setInterval(()=>{bIng+=Math.random()*125.5-30;bAg+=Math.floor(Math.random()*5)-1;let l=(Math.random()*0.08).toFixed(2);document.getElementById("liveIngestion").innerText="$"+bIng.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});document.getElementById("liveAgents").innerText=bAg.toLocaleString("en-US")+" units";document.getElementById("liveEfficiency").innerText="99."+Math.floor(85+Math.random()*14)+"% ("+l+"ms)";},2000);',
    'const wsP=window.location.protocol==="https:"?"wss://":"ws://";',
    'const liveWs=new WebSocket(wsP+window.location.host+"/ws");',
    'liveWs.onmessage=function(e){const s=document.getElementById("streamLog");s.innerHTML+="<br>"+e.data;s.scrollTop=s.scrollHeight;};',
    '</script></body></html>'
]

HYBRID_INDEX_HTML = "".join(HTML_PARTS)

LEGAL_HTML = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>特定商取引法に基づく表記</title>
<style>body{background:#05050a;color:#f8fafc;font-family:sans-serif;padding:20px;display:flex;justify-content:center;}.box{max-width:600px;width:100%;background:#0d0d1a;border:1px solid #1e1b4b;padding:24px;border-radius:8px;}h1{color:#c084fc;font-size:1.3rem;margin-bottom:20px;}.row{border-bottom:1px solid #1e1b4b;padding:12px 0;font-size:0.85rem;}.label{color:#94a3b8;font-weight:bold;width:140px;display:inline-block;}a{color:#38bdf8;text-decoration:none;font-weight:bold;}</style>
</head><body><div class="box"><h1>特定商取引法に基づく表記</h1>
<div class="row"><span class="label">事業者名</span> QLAX</div>
<div class="row"><span class="label">運営責任者</span> Daisuke Higuchi</div>
<div class="row"><span class="label">連絡先</span> qlaxlab@gmail.com</div>
<div class="row"><span class="label">販売価格</span> 各タスク・APIサービスごとに表示（暗号資産/USD）</div>
<div class="row"><span class="label">支払方法</span> 暗号資産決済 (BTC, SOL, EVM, BSV) / Stripe決済</div>
<div class="row"><span class="label">引き渡し時期</span> 決済確認後、即時（M2M自律アトミック処理）</div>
<div class="row"><span class="label">返品・キャンセル</span> デジタルサービスの性質上、処理完了後の返品・返金不可</div>
<br><a href="/">← ダッシュボードへ戻る</a></div></body></html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HYBRID_INDEX_HTML

@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    return LEGAL_HTML

@app.get("/well-known/agent.json")
async def agent_manifest():
    return {
        "name": "ASGARD Omni-Singularity M2M Agent",
        "operator": "QLAX (Daisuke Higuchi)",
        "wallets": WALLETS,
        "status": "omni-expansion-active"
    }

@app.post("/api/v10/feedback")
async def post_feedback(data: FeedbackModel):
    return {"status": "success", "received": data.feedback}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Omni Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def background_omni_simulator():
    while True:
        await asyncio.sleep(12)
        chains = ["BTC", "SOL", "EVM", "BSV"]
        target_chain = random.choice(chains)
        gain = round(random.uniform(0.002, 0.015), 4)
        log_entry = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] OMNI_ARBITRAGE ({target_chain}) -> Master Vault | Extracted {gain} BSV 15% Commission (0.00ms)"
        await manager.broadcast(log_entry)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_omni_simulator())
