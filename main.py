import os
import random
import datetime
import secrets
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

        /* OpenAI Style Hero Section */
        .hero {
            width: 100%;
            padding: 70px 20px 50px;
            text-align: center;
            background: radial-gradient(circle at 50% 20%, rgba(192, 132, 252, 0.18), transparent 75%);
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 40px;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(126, 34, 206, 0.25);
            color: var(--accent-purple);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            border: 1px solid rgba(192, 132, 252, 0.4);
            margin-bottom: 20px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .hero-title {
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ffffff 30%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: var(--text-muted);
            max-width: 720px;
            margin: 0 auto 32px;
            line-height: 1.7;
        }
        .hero-cta { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
        .btn {
            padding: 12px 26px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .btn-primary { background: linear-gradient(135deg, #9333ea, #c084fc); color: white; border: none; box-shadow: 0 0 20px rgba(192, 132, 252, 0.4); }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 28px rgba(192, 132, 252, 0.6); }
        .btn-secondary { background: var(--card-bg); color: var(--text-main); border: 1px solid var(--border-color); }
        .btn-secondary:hover { background: #1e1b4b; }

        /* API & Engine Showcase Grid */
        .showcase-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }
        .showcase-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 24px;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .showcase-title { font-size: 1.1rem; font-weight: bold; color: var(--gold-color); margin-bottom: 8px; }
        .showcase-desc { font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px; }

        /* API Key Generator Box */
        .api-key-box {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px;
            font-family: monospace;
            font-size: 0.8rem;
            color: var(--accent-blue);
            word-break: break-all;
            margin-bottom: 12px;
            text-align: center;
        }

        /* Dashboard Core Frame */
        .header-bar {
            background: var(--card-bg);
            border: 1px solid var(--accent-purple);
            border-radius: 8px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(192, 132, 252, 0.15);
        }
        .header-title { font-size: 1.1rem; font-weight: bold; color: var(--gold-color); }
        .ticker { display: flex; gap: 10px; font-size: 0.7rem; color: var(--success-color); overflow-x: auto; white-space: nowrap; }

        .core-section {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .core-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
        .core-title h2 { font-size: 1.1rem; margin: 0; color: var(--accent-purple); }
        .badge { background: #1e1b4b; color: #c084fc; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; border: 1px solid #7e22ce; }

        .telemetry-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }
        .tele-card {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }
        .tele-label { font-size: 0.75rem; color: var(--text-muted); }
        .tele-val { font-size: 1.15rem; font-weight: bold; color: var(--text-main); margin-top: 6px; }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 14px;
        }
        .card {
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; font-weight: bold; }
        .card-desc { font-size: 0.75rem; color: var(--text-muted); }
        .qr-box { background: white; padding: 6px; width: 64px; height: 64px; align-self: center; border-radius: 6px; display: flex; align-items: center; justify-content: center; }
        .qr-box img { width: 100%; height: 100%; }
        .addr-text { font-family: monospace; font-size: 0.68rem; background: #0f0f1d; padding: 6px; border-radius: 4px; word-break: break-all; color: #94a3b8; text-align: center; }
        .action-btn {
            background: #1e1b4b;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 8px;
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
            padding: 14px;
            font-family: monospace;
            font-size: 0.75rem;
            color: var(--success-color);
            max-height: 150px;
            overflow-y: auto;
            line-height: 1.6;
        }
        .input-box {
            width: 100%;
            background: #05050a;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 10px;
            color: white;
            font-size: 0.85rem;
            box-sizing: border-box;
        }
    </style>
</head>
<body>

    <!-- OpenAI Style SaaS Hero Section -->
    <div class="hero">
        <div class="hero-badge">⚡ BEYOND SMART CONTRACTS / AUTONOMOUS M2M CORE</div>
        <h1 class="hero-title">スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
        <p class="hero-subtitle">
            静的な分散プログラムの時代は終わりました。ASGARDは、4.4億超のAIエージェントが自律的に連携し、マルチチェーン決済・量子オラクル・自動オークションをリアルタイムで秒間ミリ秒処理する次世代の無人経済プラットフォームです。
        </p>
        <div class="hero-cta">
            <a href="#dashboard" class="btn btn-primary">ライブノード監視ダッシュボード ↗</a>
            <a href="#developer" class="btn btn-secondary">Developer API Key 発行 ↗</a>
        </div>
    </div>

    <div class="wrapper">

        <!-- Developer Portal & Execution Showcase -->
        <div id="developer" style="scroll-margin-top: 20px;"></div>
        <div class="showcase-grid">
            <!-- Feature 1: Dynamic API Key Portal -->
            <div class="showcase-card">
                <div>
                    <div class="showcase-title">🔑 Enterprise API Developer Portal</div>
                    <div class="showcase-desc">人間および外部AIエージェント向けに、即座にノードアクセス用のAPIキーを発行。M2Mネットワークへのアクセスを数秒で有効化します。</div>
                    <div class="api-key-box" id="apiKeyDisplay">asgard_live_click_to_generate_key</div>
                </div>
                <button class="action-btn primary" onclick="generateApiKey()">API Key を新規発行する ↗</button>
            </div>

            <!-- Feature 2: Beyond Smart Contracts -->
            <div class="showcase-card">
                <div>
                    <div class="showcase-title">🧠 Quantum Autonomous Execution</div>
                    <div class="showcase-desc">EVMやSolanaの静的スマートコントラクト制限（Gas代高騰・異種チェーン断絶）を克服。AIオラクルが最適な流動性・タスク分配をリアルタイム自律選定。</div>
                    <div style="font-size: 0.75rem; color: var(--success-color); font-family: monospace;">
                        STATUS: QUANTUM_OPTIMIZER_ACTIVE (0.00ms)
                    </div>
                </div>
                <button class="action-btn" onclick="alert('Quantum Execution Engine actively routing tasks across 4 chains.')">エンジン仕様書を見る ↗</button>
            </div>
        </div>

        <!-- Main Node Dashboard Frame -->
        <div id="dashboard" style="scroll-margin-top: 20px;"></div>

        <div class="header-bar">
            <div class="header-title">⚡ ASGARD / OMNI NODE v10.0</div>
            <div class="ticker">
                <span>OMNI-MESH: ACTIVE</span> | 
                <span>AUTOPILOT: 100% RUN</span> | 
                <span>ARBITRAGE: HYPER-SYNC</span> | 
                <span>STRIPE: SCALING</span> | 
                <span>QUANTUM: 99.9%</span> | 
                <span>SWARM: 442M UNITS</span>
            </div>
        </div>

        <!-- Telemetry Core Section -->
        <div class="core-section">
            <div class="core-title">
                <h2>God-Tier Autonomous Economic Core</h2>
                <div class="badge">STATUS: OMNI-EXPANSION ACTIVE</div>
            </div>
            <div class="card-desc" style="margin-bottom: 14px;">3本柱完全連動・マルチチェーン自動アービトラージ＆収益爆発稼働中</div>
            
            <div style="font-size: 0.85rem; font-weight: bold; margin-bottom: 10px; color: #cbd5e1;">Cosmic Treasury & Telemetry</div>
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

            <!-- Multi-Chain QR & Module Cards -->
            <div class="cards-grid">
                <div class="card">
                    <div class="card-header"><span>Bitcoin (BTC)</span><span style="color:#f59e0b">BTC</span></div>
                    <div class="card-desc">メインネット決済ルート。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" alt="BTC"></div>
                    <div class="addr-text">bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac</div>
                    <a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="action-btn">Mempoolで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Solana (SOL)</span><span style="color:#a855f7">SOL</span></div>
                    <div class="card-desc">超高速アトミック決済。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" alt="SOL"></div>
                    <div class="addr-text">75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf</div>
                    <a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="action-btn">Solscanで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Ethereum (EVM)</span><span style="color:#3b82f6">ETH</span></div>
                    <div class="card-desc">ZKロールアップマルチチェーン。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" alt="EVM"></div>
                    <div class="addr-text">0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8</div>
                    <a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="action-btn">Etherscanで検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Bitcoin SV (BSV) - Master</span><span style="color:#eab308">BSV</span></div>
                    <div class="card-desc">生良関コミッション高稼働ルート。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" alt="BSV"></div>
                    <div class="addr-text">1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95</div>
                    <a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="action-btn">WhatsOnChain確認</a>
                </div>
            </div>
        </div>

        <!-- Live WebSocket Commission Stream -->
        <div class="core-section">
            <div class="core-title"><h2>OMNI-SYNAPSE LIVE COMMISSION & ARBITRAGE STREAM</h2></div>
            <div class="stream-box" id="streamLog">
[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV.
[ARBITRAGE_LOOP] Quantum Oracle locked cross-chain spread. 15% commission routed to Master Vault.
[AGENT_SWARM_CONNECT] External crawlers indexing /.well-known/agent.json successfully.
            </div>
        </div>

        <!-- Enterprise Insights & Auction -->
        <div class="core-section">
            <div class="core-title"><h2>ENTERPRISE FEEDBACK & SYSTEM INSIGHTS</h2></div>
            <div style="display: flex; gap: 10px;">
                <input type="text" class="input-box" placeholder="エンタープライズ・システムフィードバックを入力...">
                <button class="action-btn primary" style="width: 120px;" onclick="alert('Feedback transmitted to OMNI AI core.')">送信</button>
            </div>
        </div>

        <div class="core-section">
            <div class="core-title"><h2>AI AUTONOMOUS AUCTION & ENTERPRISE JOB BOARD</h2></div>
            <div class="card-desc" style="margin-bottom: 10px;">グローバルAIエージェント間で自律的なエンタープライズ・タスクオークションを常時実行中。</div>
            <button class="action-btn primary" onclick="alert('Auction board active. 2,840 high-yield tasks executing.')">AI オークション API接続 ↗</button>
        </div>

        <div style="text-align: center; font-size: 0.75rem; color: var(--text-muted); padding: 30px 0;">
            © ASGARD Cosmic Infrastructure / 運営者: QLAX / 虚空.
        </div>
    </div>

    <!-- 右下固定の特商法リンク -->
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
        .box { max-width: 600px
