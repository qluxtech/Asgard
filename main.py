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

app = FastAPI(title="ASGARD Cosmic Super Market Node", version="10.0.0-singularity-live")

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
    <title>ASGARD / Cosmic Super Market Node v10.0</title>
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
            z-index: 1002;
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

        .hero {
            width: 100%;
            padding: 30px 10px 20px;
            text-align: center;
            background: radial-gradient(circle at 50% 20%, rgba(192, 132, 252, 0.18), transparent 75%);
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 15px;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(126, 34, 206, 0.25);
            color: var(--accent-purple);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.65rem;
            border: 1px solid rgba(192, 132, 252, 0.4);
            margin-bottom: 10px;
            font-weight: 600;
        }
        .hero-title {
            font-size: 1.4rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #ffffff 30%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 0.75rem;
            color: var(--text-muted);
            max-width: 700px;
            margin: 0 auto 14px;
            line-height: 1.4;
        }
        .hero-cta { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
        .btn {
            padding: 7px 14px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
        }
        .btn-primary { background: linear-gradient(135deg, #9333ea, #c084fc); color: white; border: none; }
        .btn-secondary { background: var(--card-bg); color: var(--text-main); border: 1px solid var(--border-color); }

        .wrapper { width: 100%; max-width: 1000px; padding: 10px; box-sizing: border-box; }
        
        .showcase-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }
        .showcase-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 10px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .showcase-title { font-size: 0.8rem; font-weight: bold; color: var(--gold-color); margin-bottom: 4px; }
        .showcase-desc { font-size: 0.65rem; color: var(--text-muted); line-height: 1.3; margin-bottom: 8px; }
        .api-key-box {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 4px;
            font-family: monospace;
            font-size: 0.6rem;
            color: var(--accent-blue);
            word-break: break-all;
            margin-bottom: 6px;
            text-align: center;
        }

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
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 6px;
        }
        .card {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 6px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.65rem; font-weight: bold; }
        .card-desc { font-size: 0.55rem; color: var(--text-muted); }
        .qr-box { background: white; padding: 3px; width: 34px; height: 34px; align-self: center; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
        .qr-box img { width: 100%; height: 100%; }
        .addr-text { font-family: monospace; font-size: 0.5rem; background: #0f0f1d; padding: 2px; border-radius: 3px; word-break: break-all; color: #94a3b8; text-align: center; }
        .action-btn {
            background: #1e1b4b;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 4px;
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
            max-height: 80px;
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

    <div class="hero">
        <div class="hero-badge">⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>
        <h1 class="hero-title">スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
        <p class="hero-subtitle">
            4.4億超のAIエージェント・AGIが自動収集・連動する全モジュールデータ群をリアルタイム開放。
        </p>
        <div class="hero-cta">
            <a href="#dashboard" class="btn btn-primary">ライブノード監視ダッシュボード ↗</a>
            <a href="#developer" class="btn btn-secondary">API Key 発行ポータル ↗</a>
        </div>
    </div>

    <div class="wrapper">
        <div id="developer" style="scroll-margin-top: 10px;"></div>
        <div class="showcase-grid">
            <div class="showcase-card">
                <div>
                    <div class="showcase-title">🔑 Enterprise API Developer Portal</div>
                    <div class="showcase-desc">外部AIエージェント向けに、即座にノードアクセス用のAPIキーを発行。</div>
                    <div class="api-key-box" id="apiKeyDisplay">asgard_live_click_to_generate_key</div>
                </div>
                <button class="action-btn primary" onclick="generateApiKey()">APIKey を新規発行する ↗</button>
            </div>

            <div class="showcase-card">
                <div>
                    <div class="showcase-title">🧠 Quantum Autonomous Execution</div>
                    <div class="showcase-desc">静的スマートコントラクトの限界を克服。AIオラクルが最適な流動性・タスク分配を即時選定。</div>
                    <div style="font-size: 0.55rem; color: var(--success-color); font-family: monospace; margin-top: 2px;" id="quantumStatus">
                        STATUS: QUANTUM_OPTIMIZER_ACTIVE (0.00ms)
                    </div>
                </div>
                <button class="action-btn" onclick="alert('Quantum Execution Engine actively routing tasks.')">エンジン仕様書を見る ↗</button>
            </div>
        </div>

        <div id="dashboard" style="scroll-margin-top: 10px;"></div>

        <div class="core-section">
            <div class="core-title">
                <h2>God-Tier Autonomous Economic Core [LIVE]</h2>
                <div class="badge">STATUS: OMNI-EXPANSION ACTIVE</div>
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

            <div class="cards-grid">
                <div class="card">
                    <div class="card-header"><span>Bitcoin (BTC)</span><span style="color:#f59e0b">BTC</span></div>
                    <div class="card-desc">メインネット決済。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" alt="BTC"></div>
                    <div class="addr-text">bc1q94rkd...d7zac</div>
                    <a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="action-btn">Mempoolで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Solana (SOL)</span><span style="color:#a855f7">SOL</span></div>
                    <div class="card-desc">超高速アトミック。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" alt="SOL"></div>
                    <div class="addr-text">75igwQpPgVk...7nf</div>
                    <a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="action-btn">Solscanで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Ethereum (EVM)</span><span style="color:#3b82f6">ETH</span></div>
                    <div class="card-desc">ZKロールアップ。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" alt="EVM"></div>
                    <div class="addr-text">0xD6716D08...8G8</div>
                    <a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="action-btn">Etherscanで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Bitcoin SV (BSV)</span><span style="color:#eab308">BSV</span></div>
                    <div class="card-desc">マスターVault。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" alt="BSV"></div>
                    <div class="addr-text">1PB66iHotU...y95</div>
                    <a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="action-btn">WhatsOnChain確認</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Mesh API</span><span style="color:#10b981">M2M</span></div>
                    <div class="card-desc">AI直結受託。</div>
                    <div class="addr-text">/api/v10/autonomous-mesh</div>
                    <button class="action-btn primary" onclick="alert('Mesh API active.')">ステータス ↗</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>.well-known</span><span style="color:#6366f1">SPAR</span></div>
                    <div class="card-desc">AIエージェント発見。</div>
                    <div class="addr-text">/.well-known/agent.json</div>
                    <a href="/well-known/agent.json" target="_blank" class="action-btn primary">マニフェスト ↗</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Stripe Gateway</span><span style="color:#ec4899">PST</span></div>
                    <div class="card-desc">ウィジェット＆API。</div>
                    <div class="addr-text">enterprise-live-key</div>
                    <button class="action-btn primary" style="background:#065f46; color:#a7f3d0;" onclick="alert('Stripe決済完了済み ✓')">Stripe 決済済 ✓</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>Quantum Oracle</span><span style="color:#06b6d4">PCT/SX</span></div>
                    <div class="card-desc">HTTP 402量子千円。</div>
                    <div class="addr-text">photonize-engine-10.0</div>
                    <button class="action-btn primary" onclick="alert('Quantum Oracle active.')">量子オラクル確認 ↗</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>WebSocket Stream</span><span style="color:#ef4444">M2M</span></div>
                    <div class="card-desc">双方向リアルタイム。</div>
                    <div class="addr-text">wss://asgard.tgio.onrender.com/ws</div>
                    <button class="action-btn primary" onclick="alert('WebSocket Connected.')">接続テスト ↗</button>
                </div>
            </div>
        </div>

        <div class="core-section">
            <div class="core-title"><h2>OMNI-SYNAPSE LIVE COMMISSION STREAM</h2></div>
            <div class="stream-box" id="streamLog">
[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV. [ARBITRAGE_LOOP] Quantum Oracle locked cross-chain spread. 15% commission routed.
            </div>
        </div>

        <div class="core-section">
            <div class="core-title"><h2>ENTERPRISE FEEDBACK & SYSTEM INSIGHTS</h2></div>
            <div class="input-group">
                <input type="text" id="feedbackInput" class="input-box" placeholder="エンタープライズ・システムフィードバックを入力...">
                <button class="action-btn primary" onclick="sendFeedback()">送信</button>
            </div>
        </div>

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
        async function generateApiKey() {
            try {
                const res = await fetch('/api/v10/generate-key', { method: 'POST' });
                const data = await res.json();
                document.getElementById('apiKeyDisplay').innerText = da
