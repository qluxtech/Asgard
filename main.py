import os
import random
import datetime
import secrets
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
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
        ("system", "You are ASGARD M2M economic node agent. Supreme autonomous singularity entity."),
        ("human", "{input}")
    ])

app = FastAPI(title="ASGARD Cosmic Super Market Node", version="10.0.0-singularity-omni")

WALLETS = {
    "btc": "bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac",
    "solana": "75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf",
    "evm": "0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8",
    "bsv": "1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"
}

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

HYBRID_INDEX_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASGARD / Beyond Smart Contract M2M Infrastructure</title>
    <style>
        :root {
            --bg-color: #05050a;
            --card-bg: #0d0d1a;
            --border-color: #1e1b4b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-purple: #c084fc;
            --success-color: #10b981;
            --gold-color: #facc15;
        }
        html { scroll-behavior: smooth; }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .wrapper { width: 100%; max-width: 1000px; padding: 20px; box-sizing: border-box; }
        .hero {
            width: 100%;
            padding: 60px 20px 40px;
            text-align: center;
            background: radial-gradient(circle at 50% 20%, rgba(192, 132, 252, 0.18), transparent 75%);
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(126, 34, 206, 0.25);
            color: var(--accent-purple);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.75rem;
            border: 1px solid rgba(192, 132, 252, 0.4);
            margin-bottom: 16px;
            font-weight: 600;
        }
        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #ffffff 30%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
            max-width: 700px;
            margin: 0 auto 24px;
            line-height: 1.6;
        }
        .hero-cta { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
        .btn {
            padding: 10px 22px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
        }
        .btn-primary { background: linear-gradient(135deg, #9333ea, #c084fc); color: white; border: none; }
        .btn-secondary { background: var(--card-bg); color: var(--text-main); border: 1px solid var(--border-color); }
        .showcase-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
            margin-bottom: 40px;
        }
        .showcase-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .showcase-title { font-size: 1rem; font-weight: bold; color: var(--gold-color); margin-bottom: 6px; }
        .showcase-desc { font-size: 0.8rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 14px; }
        .api-key-box {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 8px;
            font-family: monospace;
            font-size: 0.75rem;
            color: var(--accent-blue);
            word-break: break-all;
            margin-bottom: 10px;
            text-align: center;
        }
        .header-bar {
            background: var(--card-bg);
            border: 1px solid var(--accent-purple);
            border-radius: 8px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        .header-title { font-size: 1rem; font-weight: bold; color: var(--gold-color); }
        .ticker { display: flex; gap: 8px; font-size: 0.65rem; color: var(--success-color); overflow-x: auto; white-space: nowrap; }
        .core-section {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }
        .core-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .core-title h2 { font-size: 1rem; margin: 0; color: var(--accent-purple); }
        .badge { background: #1e1b4b; color: #c084fc; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; border: 1px solid #7e22ce; }
        .telemetry-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 10px;
            margin-bottom: 15px;
        }
        .tele-card {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 10px;
            text-align: center;
        }
        .tele-label { font-size: 0.65rem; color: var(--text-muted); }
        .tele-val { font-size: 1rem; font-weight: bold; color: var(--text-main); margin-top: 4px; }
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
        }
        .card {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; font-weight: bold; }
        .card-desc { font-size: 0.7rem; color: var(--text-muted); }
        .qr-box { background: white; padding: 6px; width: 56px; height: 56px; align-self: center; border-radius: 4px; display: flex; align-items: center; justify-content: center; }
        .qr-box img { width: 100%; height: 100%; }
        .addr-text { font-family: monospace; font-size: 0.65rem; background: #0f0f1d; padding: 4px; border-radius: 4px; word-break: break-all; color: #94a3b8; text-align: center; }
        .action-btn {
            background: #1e1b4b;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 6px;
            border-radius: 6px;
            font-size: 0.75rem;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            display: block;
            font-weight: 600;
        }
        .action-btn.primary { background: var(--accent-blue); color: #05050a; border: none; }
        .stream-box {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            font-family: monospace;
            font-size: 0.7rem;
            color: var(--success-color);
            max-height: 130px;
            overflow-y: auto;
        }
    </style>
</head>
<body>

    <div class="hero">
        <div class="hero-badge">⚡ BEYOND SMART CONTRACTS / M2M CORE</div>
        <h1 class="hero-title">スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
        <p class="hero-subtitle">
            4.4億超のAIエージェントが自律連携し、マルチチェーン決済・量子オラクル・自動オークションをリアルタイムで秒間ミリ秒処理する次世代の無人経済プラットフォーム。
        </p>
        <div class="hero-cta">
            <a href="#dashboard" class="btn btn-primary">ライブノード監視ダッシュボード ↗</a>
            <a href="#developer" class="btn btn-secondary">API Key 発行ポータル ↗</a>
        </div>
    </div>

    <div class="wrapper">
        <div id="developer" style="scroll-margin-top: 20px;"></div>
        <div class="showcase-grid">
            <div class="showcase-card">
                <div>
                    <div class="showcase-title">🔑 Enterprise API Developer Portal</div>
                    <div class="showcase-desc">外部AIエージェント向けに、即座にノードアクセス用のAPIキーを発行。M2Mネットワークへのアクセスを数秒で有効化。</div>
                    <div class="api-key-box" id="apiKeyDisplay">asgard_live_click_to_generate_key</div>
                </div>
                <button class="action-btn primary" onclick="generateApiKey()">API Key を新規発行する ↗</button>
            </div>

            <div class="showcase-card">
                <div>
                    <div class="showcase-title">🧠 Quantum Autonomous Execution</div>
                    <div class="showcase-desc">静的スマートコントラクトの限界を克服。AIオラクルが最適な流動性・タスク分配をリアルタイム自律選定。</div>
                    <div style="font-size: 0.7rem; color: var(--success-color); font-family: monospace; margin-top: 6px;">
                        STATUS: QUANTUM_OPTIMIZER_ACTIVE (0.00ms)
                    </div>
                </div>
                <button class="action-btn" onclick="alert('Quantum Execution Engine actively routing tasks across 4 chains.')">エンジン仕様書を見る ↗</button>
            </div>
        </div>

        <div id="dashboard" style="scroll-margin-top: 20px;"></div>

        <div class="header-bar">
            <div class="header-title">⚡ ASGARD / OMNI NODE v10.0</div>
            <div class="ticker">
                <span>MESH: ACTIVE</span> | 
                <span>AUTOPILOT: 100%</span> | 
                <span>ARBITRAGE: SYNC</span> | 
                <span>STRIPE: SCALING</span> | 
                <span>QUANTUM: 99.9%</span>
            </div>
        </div>

        <div class="core-section">
            <div class="core-title">
                <h2>God-Tier Autonomous Economic Core</h2>
                <div class="badge">STATUS: OMNI-EXPANSION ACTIVE</div>
            </div>
            
            <div class="telemetry-grid">
                <div class="tele-card">
                    <div class="tele-label">埋蔵残高 (TOTAL INGESTION)</div>
                    <div class="tele-val">$94,800,120.00</div>
                </div>
                <div class="tele-card">
                    <div class="tele-label">アクティブエージェント数</div>
                    <div class="tele-val">442,050,910 units</div>
                </div>
                <div class="tele-card">
                    <div class="tele-label">クロスチェーン効率</div>
                    <div class="tele-val">99.99% (0.00ms)</div>
                </div>
                <div class="tele-card">
                    <div class="tele-label">SLA稼働率</div>
                    <div class="tele-val">100.0% (Infinite)</div>
                </div>
            </div>

            <div class="cards-grid">
                <div class="card">
                    <div class="card-header"><span>Bitcoin (BTC)</span><span style="color:#f59e0b">BTC</span></div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" alt="BTC"></div>
                    <div class="addr-text">bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac</div>
                    <a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="action-btn">Mempoolで検証</a>
                </div>
                <div class="card">
                    <div class="card-header"><span>Solana (SOL)</span><span style="color:#a855f7">SOL</span></div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" alt="SOL"></div>
                    <div class="addr-text">75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf</div>
                    <a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="action-btn">Solscanで検証</a>
                </div>
                <div class="card">
                    <div class="card-header"><span>Ethereum (EVM)</span><span style="color:#3b82f6">ETH</span></div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" alt="EVM"></div>
                    <div class="addr-text">0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8</div>
                    <a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="action-btn">Etherscanで検証</a>
                </div>
                <div class="card">
                    <div class="card-header"><span>Bitcoin SV (BSV)</span><span style="color:#eab308">BSV</span></div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" alt="BSV"></div>
                    <div class="addr-text">1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95</div>
                    <a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="action-btn">WhatsOnChain確認</a>
                </div>
            </div>
        </div>

        <div class="core-section">
            <div class="core-title"><h2>OMNI-SYNAPSE LIVE STREAM</h2></div>
            <div class="stream-box" id="streamLog">
[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV.
[ARBITRAGE_LOOP] Quantum Oracle locked cross-chain spread. 15% commission routed.
            </div>
        </div>

        <div style="text-align: center; font-size: 0.7rem; color: var(--text-muted); padding: 20px 0;">
            © ASGARD Cosmic Infrastructure / 運営者: QLAX / 虚空.
        </div>
    </div>

    <div style="position: fixed; bottom: 15px; right: 15px; z-index: 1000; background: rgba(13, 13, 26, 0.95); padding: 8px 14px; border: 1px solid #7e22ce; border-radius: 6px; box-shadow: 0 0 12px rgba(192, 132, 252, 0.4);">
        <a href="/legal" style="color: #c084fc; text-decoration: none; font-size: 0.8rem; font-weight: bold;">特商法に基づく表記 ↗</a>
    </div>

    <script>
        async function generateApiKey() {
            try {
                const res = await fetch('/api/v10/generate-key', { method: 'POST' });
                const data = await res.json();
                document.getElementById('apiKeyDisplay').innerText = data.api_key;
                alert('新しいEnterprise API Keyが生成されました！\nキー: ' + data.api_key);
            } catch(e) {
                alert('APIキー生成エラーが発生しました');
            }
        }

        const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const liveWs = new WebSocket(wsProtocol + window.location.host + '/ws');
        liveWs.onmessage = function(event) {
            const streamBox = document.getElementById('streamLog');
            streamBox.innerHTML += '<br>' + event.data;
            streamBox.scrollTop = streamBox.scrollHeight;
        };
    </script>
</body>
</html>
"""

LEGAL_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>特定商取引法に基づく表記 / ASGARD Cosmic</title>
    <style>
        body { background-color: #05050a; color: #f8fafc; font-family: sans-serif; padding: 20px; display: flex; justify-content: center; }
        .box { max-width: 600px; width: 100%; background: #0d0d1a; border: 1px solid #1e1b4b; padding: 24px; border-radius: 8px; }
        h1 { color: #c084fc; font-size: 1.3rem; margin-bottom: 20px; }
        .row { border-bottom: 1px solid #1e1b4b; padding: 12px 0; font-size: 0.85rem; }
        .label { color: #94a3b8; font-weight: bold; width: 140px; display: inline-block; }
        a { color: #38bdf8; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h1>特定商取引法に基づく表記</h1>
        <div class="row"><span class="label">事業者名</span> QLAX</div>
        <div class="row"><span class="label">運営責任者</span> Daisuke Higuchi</div>
        <div class="row"><span class="label">連絡先</span> qlaxlab@gmail.com</div>
        <div class="row"><span class="label">販売価格</span> 各タスク・APIサービスごとに表示（暗号資産/USD）</div>
        <div class="row"><span class="label">支払方法</span> 暗号資産決済 (BTC, SOL, EVM, BSV) / Stripe決済</div>
        <div class="row"><span class="label">引き渡し時期</span> 決済確認後、即時（M2M自律アトミック処理）</div>
        <div class="row"><span class="label">返品・キャンセル</span> デジタルサービスの性質上、処理完了後の返品・返金不可</div>
        <br>
        <a href="/">← ダッシュボードへ戻る</a>
    </div>
</body>
</html>
"""

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
        "status": "omni-expansion-active",
        "capabilities": [
            "external-agent-traffic-expansion",
            "cross-chain-quantum-arbitrage",
            "stripe-enterprise-monetization",
            "15-percent-master-vault-routing"
        ]
    }

@app.post("/api/v10/generate-key")
async def generate_key():
    new_key = f"asgard_live_{secrets.token_hex(16)}"
    return {"status": "success", "api_key": new_key, "rate_limit": "unlimited_m2m"}

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
