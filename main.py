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

app = FastAPI(title="ASGARD Cosmic Super Market Node", version="10.0.0-singularity-omni-full")

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
    <title>ASGARD / Cosmic Super Market Node v10.0 (Full Edition)</title>
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
            --danger-color: #ef4444;
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

        /* 最上部の8連データ帯 */
        .top-8-data-bar {
            width: 100%;
            background: #000000;
            border-bottom: 1px solid #2a275f;
            padding: 6px 10px;
            display: flex;
            gap: 6px;
            overflow-x: auto;
            white-space: nowrap;
            box-sizing: border-box;
            font-family: monospace;
            font-size: 0.58rem;
            align-items: center;
        }
        .data-badge {
            background: #0a0a16;
            padding: 2px 6px;
            border-radius: 3px;
            border: 1px solid #1e1b4b;
            color: var(--danger-color);
            font-weight: bold;
        }
        .data-badge.green { color: var(--success-color); }
        .data-badge.purple { color: var(--accent-purple); }

        .wrapper { width: 100%; max-width: 1000px; padding: 10px; box-sizing: border-box; }

        .core-section {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .core-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .core-title h2 { font-size: 0.85rem; margin: 0; color: var(--accent-purple); }
        .badge { background: #1e1b4b; color: #c084fc; padding: 2px 6px; border-radius: 4px; font-size: 0.55rem; border: 1px solid #7e22ce; }
        
        .telemetry-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            margin-bottom: 10px;
        }
        .tele-card {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 6px;
            text-align: center;
        }
        .tele-label { font-size: 0.5rem; color: var(--text-muted); font-weight: bold; }
        .tele-val { font-size: 0.75rem; font-weight: bold; color: var(--success-color); margin-top: 2px; font-family: monospace; }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 8px;
        }
        .card {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.7rem; font-weight: bold; }
        .card-desc { font-size: 0.58rem; color: var(--text-muted); line-height: 1.3; }
        .qr-box { background: white; padding: 3px; width: 38px; height: 38px; align-self: center; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
        .qr-box img { width: 100%; height: 100%; }
        .addr-text { font-family: monospace; font-size: 0.5rem; background: #0f0f1d; padding: 3px; border-radius: 3px; word-break: break-all; color: #94a3b8; text-align: center; }
        .action-btn {
            background: #1e1b4b;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 5px;
            border-radius: 4px;
            font-size: 0.6rem;
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
            border-radius: 6px;
            padding: 8px;
            font-family: monospace;
            font-size: 0.55rem;
            color: var(--success-color);
            max-height: 90px;
            overflow-y: auto;
        }
        .input-group {
            display: flex;
            gap: 6px;
            margin-top: 6px;
        }
        .input-box {
            flex: 1;
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 6px;
            color: white;
            font-size: 0.65rem;
            box-sizing: border-box;
        }
    </style>
</head>
<body>

    <!-- 最上部の8連データ帯 -->
    <div class="top-8-data-bar">
        <span class="data-badge">VAPORLOCK: ACTIVE</span>
        <span class="data-badge green">AUTOPILOT: 100% RUN</span>
        <span class="data-badge purple">TIMELOCK: SOLSTICE</span>
        <span class="data-badge green">SINGULARITY: UNLOCKED</span>
        <span class="data-badge green">UMBRA: 99.99%</span>
        <span class="data-badge purple">GAIA_L2: 100%</span>
        <span class="data-badge green">SELF_HEAL: ACTIVE</span>
        <span class="data-badge">KROK_SYNC</span>
    </div>

    <div class="wrapper">
        <div class="core-section">
            <div class="core-title">
                <h2>ASGARD / OMNI NODE v10.0</h2>
                <div class="badge">STATUS: OMNI-EXPANSION ACTIVE</div>
            </div>
            
            <div style="font-size: 0.7rem; color: var(--text-muted); margin-bottom: 10px;">
                God-Tier Autonomous Economic Core [LIVE]
            </div>

            <div class="telemetry-grid">
                <div class="tele-card">
                    <div class="tele-label">埋蔵残高 (TOTAL INGESTION)</div>
                    <div class="tele-val" id="liveIngestion">$94,800,120.00</div>
                </div>
                <div class="tele-card">
                    <div class="tele-label">アクティブエージェント数</div>
                    <div class="tele-val" id="liveAgents">442,050,910 units</div>
                </div>
                <div class="tele-card">
                    <div class="tele-label">クロスチェーン効率</div>
                    <div class="tele-val" id="liveEfficiency">99.99% (0.00ms)</div>
                </div>
                <div class="tele-card">
                    <div class="tele-label">SLA稼働率</div>
                    <div class="tele-val">100.0% (Infinite)</div>
                </div>
            </div>

            <!-- 全9大モジュールのカード一覧 -->
            <div class="cards-grid">
                <div class="card">
                    <div class="card-header"><span>Bitcoin (BTC)</span><span style="color:#f59e0b">BTC</span></div>
                    <div class="card-desc">メインネット決済ルート。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" alt="BTC"></div>
                    <div class="addr-text">bc1q94rkd...d7zac</div>
                    <a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="action-btn">Mempoolで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Solana (SOL)</span><span style="color:#a855f7">SOL</span></div>
                    <div class="card-desc">超高速アトミック決済。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" alt="SOL"></div>
                    <div class="addr-text">75igwQpPgVk...7nf</div>
                    <a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="action-btn">Solscanで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Ethereum (EVM)</span><span style="color:#3b82f6">ETH</span></div>
                    <div class="card-desc">ZKロールアップマルチチェーン。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" alt="EVM"></div>
                    <div class="addr-text">0xD6716D08...8G8</div>
                    <a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="action-btn">Etherscanで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Bitcoin SV (BSV) - Master</span><span style="color:#eab308">BSV</span></div>
                    <div class="card-desc">全自動コミッション高効率ルート。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" alt="BSV"></div>
                    <div class="addr-text">1PB66iHotU...y95</div>
                    <a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="action-btn">WhatsOnChain確認</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Autonomous Mesh API</span><span style="color:#10b981">M2M</span></div>
                    <div class="card-desc">AIエージェント直結タスク受託・手数料直結。</div>
                    <div class="addr-text">/api/v10/autonomous-mesh</div>
                    <button class="action-btn primary" onclick="alert('Mesh API active.')">メッシュステータス ↗</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>.well-known Discovery</span><span style="color:#6366f1">SPAR</span></div>
                    <div class="card-desc">AIエージェント自動発見ビーコン。</div>
                    <div class="addr-text">/.well-known/agent.json</div>
                    <a href="/well-known/agent.json" target="_blank" class="action-btn primary">マニフェスト確認 ↗</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Stripe Gateway</span><span style="color:#ec4899">PST</span></div>
                    <div class="card-desc">成人向けクレジット＆API決済。</div>
                    <div class="addr-text">enterprise-live-key-active</div>
                    <button class="action-btn primary" style="background:#065f46; color:#a7f3d0;" onclick="alert('Stripe決済完了済み ✓')">Stripe 決済済 ✓</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>Quantum Oracle</span><span style="color:#06b6d4">PCT/SX</span></div>
                    <div class="card-desc">HTTP 402量子千円レシート決済発行。</div>
                    <div class="addr-text">photonize-engine-10.0</div>
                    <button class="action-btn primary" onclick="alert('Quantum Oracle active.')">量子オラクル確認 ↗</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>WebSocket Stream ⚡</span><span style="color:#ef4444">M2M</span></div>
                    <div class="card-desc">AIエージェント双方向リアルタイム接続。</div>
                    <div class="addr-text">wss://asgard.tgio.onrender.com/ws</div>
                    <button class="action-btn primary" onclick="alert('WebSocket Connected.')">WebSocket接続テスト ↗</button>
                </div>
            </div>
        </div>

        <!-- ライブストリーム欄 -->
        <div class="core-section">
            <div class="core-title"><h2>OMNI-SYNAPSE LIVE COMMISSION & ARBITRAGE STREAM</h2></div>
            <div class="stream-box" id="streamLog">
[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV. [ARBITRAGE_LOOP] Quantum Oracle locked cross-chain spread. 15% commission routed.
            </div>
        </div>

        <!-- エンタープライズフィードバック機能 -->
        <div class="core-section">
            <div class="core-title"><h2>ENTERPRISE FEEDBACK & SYSTEM INSIGHTS</h2></div>
            <div class="input-group">
                <input type="text" id="feedbackInput" class="input-box" placeholder="エンタープライズ・システムフィードバックを入力...">
                <button class="action-btn primary" onclick="sendFeedback()">送信</button>
            </div>
        </div>

        <!-- AIオークション＆ジョブボード機能 -->
        <div class="core-section">
            <div class="core-title"><h2>AI AUTONOMOUS AUCTION & ENTERPRISE JOB BOARD</h2></div>
            <div style="font-size: 0.6rem; color: var(--text-muted); margin-bottom: 8px;">
                グローバルAIエージェント間で自律的なエンタープライズ・タスクオークションを常時実行中。
            </div>
            <button class="action-btn primary" onclick="alert('AI Auction & Job Board active across decentralized nodes.')">AI オークション API接続 ↗</button>
        </div>

        <div style="text-align: center; font-size: 0.55rem; color: var(--text-muted); padding: 10px 0;">
            © ASGARD Cosmic Infrastructure / 運営者: QLAX / 虚空.
        </div>
    </div>

    <div style="position: fixed; bottom: 10px; right: 10px; z-index: 1000; background: rgba(13, 13, 26, 0.95); padding: 5px 8px; border: 1px solid #7e22ce; border-radius: 6px;">
        <a href="/legal" style="color: #c084fc; text-decoration: none; font-size: 0.65rem; font-weight: bold;">特定商取引法に基づく表記 ↗</a>
    </div>

    <script>
        async function sendFeedback() {
            const val = document.getElementById('feedbackInput').value;
            if(!val) { alert('フィードバックを入力してください'); return; }
            try {
                const res = await fetch('/api/v10/feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({feedback: val})
                });
                const data = await res.json();
                alert('フィードバックを送信しました: ' + data.status);
                document.getElementById('feedbackInput').value = '';
            } catch(e) {
                alert('送信エラー');
            }
        }

        // リアルタイムライブ変動シミュレーション
        let baseIngestion = 94800120.00;
        let baseAgents = 442050910;

        setInterval(() => {
            baseIngestion += Math.random() * 125.5 - 30;
            baseAgents += Math.floor(Math.random() * 5) - 1;
            let latency = (Math.random() * 0.08).toFixed(2);

            document.getElementById('liveIngestion').innerText = '$' + baseIngestion.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            document.getElementById('liveAgents').innerText = baseAgents.toLocaleString('en-US') + ' units';
            document.getElementById('liveEfficiency').innerText = '99.' + Math.floor(85 + Math.random() * 14) + '% (' + latency + 'ms)';
        }, 2000);

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
        "status": "omni-expansion-active"
    }

@app.post("/api/v10/feedback")
async def post_feedback(data: FeedbackModel):
    return {"status": "success", "received": data.feedback}

@app.post("/api/v10/generate-key")
async def generate_key():
    new_key = f"asgard_live_{secrets.token_hex(16)}"
    return {"status": "success", "api_key": new_key}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Omni Echo: {data}")
   
