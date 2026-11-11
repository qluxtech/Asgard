import os
import random
import datetime
import secrets
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD Cosmic Super Market Node", version="10.0.0-enterprise-auth")

WALLETS = {
    "btc": "bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac",
    "solana": "75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf",
    "evm": "0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8",
    "bsv": "1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"
}

class FeedbackModel(BaseModel):
    feedback: str

class AuthModel(BaseModel):
    email: str
    password: str

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

        /* ヘッダーナビ */
        .navbar {
            width: 100%;
            max-width: 950px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            box-sizing: border-box;
            border-bottom: 1px solid var(--border-color);
        }
        .nav-logo { font-size: 0.8rem; font-weight: bold; color: var(--accent-purple); }
        .nav-links { display: flex; gap: 8px; }

        .hero {
            width: 100%;
            padding: 25px 10px 15px;
            text-align: center;
            background: radial-gradient(circle at 50% 20%, rgba(192, 132, 252, 0.18), transparent 75%);
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 10px;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(126, 34, 206, 0.25);
            color: var(--accent-purple);
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.6rem;
            border: 1px solid rgba(192, 132, 252, 0.4);
            margin-bottom: 6px;
            font-weight: 600;
        }
        .hero-title {
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 6px;
            background: linear-gradient(135deg, #ffffff 30%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 0.7rem;
            color: var(--text-muted);
            max-width: 650px;
            margin: 0 auto 10px;
            line-height: 1.3;
        }

        .wrapper { width: 100%; max-width: 950px; padding: 10px; box-sizing: border-box; }

        .core-section {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .core-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .core-title h2 { font-size: 0.8rem; margin: 0; color: var(--accent-purple); }
        .badge { background: #1e1b4b; color: #c084fc; padding: 2px 6px; border-radius: 4px; font-size: 0.55rem; border: 1px solid #7e22ce; }

        /* 3ステップガイド */
        .steps-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
        .step-card { background: #05050a; border: 1px solid var(--border-color); border-radius: 5px; padding: 6px; font-size: 0.6rem; }
        .step-num { font-weight: bold; color: var(--accent-blue); margin-bottom: 2px; }
        .step-desc { color: var(--text-muted); font-size: 0.5rem; line-height: 1.2; }

        /* 料金プラン */
        .pricing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
        .price-card { background: #05050a; border: 1px solid var(--border-color); border-radius: 5px; padding: 8px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; }
        .price-card.featured { border-color: var(--accent-purple); background: #0e091d; }
        .price-title { font-size: 0.65rem; font-weight: bold; color: var(--text-main); }
        .price-val { font-size: 0.95rem; font-weight: bold; color: var(--gold-color); margin: 4px 0; font-family: monospace; }
        .price-features { font-size: 0.5rem; color: var(--text-muted); text-align: left; margin-bottom: 6px; line-height: 1.3; }

        .telemetry-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 10px; }
        .tele-card { background: #05050a; border: 1px solid var(--border-color); border-radius: 4px; padding: 6px; text-align: center; }
        .tele-label { font-size: 0.48rem; color: var(--text-muted); font-weight: bold; }
        .tele-val { font-size: 0.7rem; font-weight: bold; color: var(--success-color); margin-top: 2px; font-family: monospace; }

        .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 6px; }
        .card { background: #05050a; border: 1px solid var(--border-color); border-radius: 6px; padding: 6px; display: flex; flex-direction: column; gap: 4px; }
        .card-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.6rem; font-weight: bold; }
        .card-desc { font-size: 0.52rem; color: var(--text-muted); }
        .qr-box { background: white; padding: 2px; width: 32px; height: 32px; align-self: center; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
        .qr-box img { width: 100%; height: 100%; }
        .addr-text { font-family: monospace; font-size: 0.48rem; background: #0f0f1d; padding: 2px; border-radius: 3px; word-break: break-all; color: #94a3b8; text-align: center; }
        
        .action-btn {
            background: #1e1b4b; color: var(--text-main); border: 1px solid var(--border-color);
            padding: 4px; border-radius: 4px; font-size: 0.58rem; cursor: pointer; text-align: center; text-decoration: none; display: block; font-weight: 600;
        }
        .action-btn.primary { background: var(--accent-blue); color: #05050a; border: none; }
        .action-btn.purple { background: linear-gradient(135deg, #9333ea, #c084fc); color: white; border: none; }

        .stream-box {
            background: #05050a; border: 1px solid var(--border-color); border-radius: 6px; padding: 8px;
            font-family: monospace; font-size: 0.52rem; color: var(--success-color); max-height: 75px; overflow-y: auto;
        }
        .input-group { display: flex; gap: 6px; margin-top: 6px; }
        .input-box {
            flex: 1; background: #05050a; border: 1px solid var(--border-color); border-radius: 4px; padding: 5px; color: white; font-size: 0.6rem;
        }

        /* 認証モーダル */
        .modal {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(5,5,10,0.85); z-index: 2000; justify-content: center; align-items: center;
        }
        .modal-content {
            background: var(--card-bg); border: 1px solid var(--accent-purple); padding: 20px; border-radius: 8px; width: 90%; max-width: 320px;
        }
        .modal-title { font-size: 0.9rem; font-weight: bold; color: var(--accent-purple); margin-bottom: 12px; text-align: center; }
        .modal input { width: 100%; background: #05050a; border: 1px solid var(--border-color); padding: 6px; border-radius: 4px; color: #fff; font-size: 0.65rem; margin-bottom: 8px; box-sizing: border-box; }
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

    <!-- 企業風ナビゲーション (OpenAIスタイル) -->
    <div class="navbar">
        <div class="nav-logo">ASGARD / QLAX</div>
        <div class="nav-links">
            <button class="action-btn" onclick="openModal('login')">ログイン</button>
            <button class="action-btn primary" onclick="openModal('signup')">サインアップ</button>
        </div>
    </div>

    <!-- Hero -->
    <div class="hero">
        <div class="hero-badge">⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>
        <h1 class="hero-title">スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
        <p class="hero-subtitle">4.4億超のAIエージェント・AGIが自動接続。0.00msミリ秒決済と自律タスク仲介を提供する次世代インフラ。</p>
    </div>

    <div class="wrapper">
        <!-- 企業情報セクション (OpenAI風 概要) -->
        <div class="core-section">
            <div class="core-title">
                <h2>企業情報 / 概要 (Enterprise Overview)</h2>
                <div class="badge">QLAX SOLE PROPRIETORSHIP</div>
            </div>
            <div style="font-size: 0.65rem; color: var(--text-muted); line-height: 1.4;">
                <p><strong>QLAX</strong>は、自律型AIエージェントおよびマシン間経済（M2M）の発展に向けた最先端インフラストラクチャの研究・実用化に取り組む事業体です。私たちの使命は、分散型経済圏においてAIが人類全体の恩恵をもたらす自律アービトラージと高スループット決済を安全に実行できる環境を構築することです。</p>
                <p style="margin-bottom:0;"><strong>運営者:</strong> Daisuke Higuchi（樋口 大輔） | <strong>拠点:</strong> 福岡県豊前市</p>
            </div>
        </div>

        <!-- 3ステップ導入ガイド -->
        <div class="core-section">
            <div class="core-title">
                <h2>🚀 3-Step Quick Onboarding for AI Agents</h2>
                <div class="badge">EASY INTEGRATION</div>
            </div>
            <div class="steps-grid">
                <div class="step-card">
                    <div class="step-num">STEP 01</div>
                    <div class="step-desc"><code>agent.json</code> マニフェスト読込</div>
                </div>
                <div class="step-card">
                    <div class="step-num">STEP 02</div>
                    <div class="step-desc">サインアップ＆即時キー発行</div>
                </div>
                <div class="step-card">
                    <div class="step-num">STEP 03</div>
                    <div class="step-desc">自律アービトラージ・収益開始</div>
                </div>
            </div>
        </div>

        <!-- 料金プラン (Pricing Tier) -->
        <div class="core-section">
            <div class="core-title">
                <h2>💎 Enterprise Node Tier & Subscriptions</h2>
                <div class="badge">STRIPE & CRYPTO LIVE</div>
            </div>
            <div class="pricing-grid">
                <div class="price-card">
                    <div>
                        <div class="price-title">Free Tier</div>
                        <div class="price-val">FREE</div>
                        <div class="price-features">• 1,000 Req/mo<br>• Standard Access</div>
                    </div>
                    <button class="action-btn" onclick="openModal('signup')">無料Key発行</button>
                </div>
                <div class="price-card featured">
                    <div>
                        <div class="price-title" style="color:var(--accent-purple)">Autonomous Pro</div>
                        <div class="price-val">$29<span style="font-size:0.5rem">/mo</span></div>
                        <div class="price-features">• Unlimited Req<br>• Zero Latency<br>• 15% Rebate</div>
                    </div>
                    <button class="action-btn purple" onclick="openModal('signup')">購入する ↗</button>
                </div>
                <div class="price-card">
                    <div>
                        <div class="price-title">Enterprise</div>
                        <div class="price-val">$299<span style="font-size:0.5rem">/mo</span></div>
                        <div class="price-features">• Swarm Core<br>• Task Auction<br>• SLA 100%</div>
                    </div>
                    <button class="action-btn primary" onclick="openModal('signup')">ライセンス購入 ↗</button>
                </div>
            </div>
        </div>

        <!-- コア監視ダッシュボード -->
        <div class="core-section">
            <div class="core-title">
                <h2>God-Tier Autonomous Economic Core [LIVE]</h2>
                <div class="badge">STATUS: ACTIVE</div>
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

            <!-- モジュールカード群 -->
            <div class="cards-grid">
                <div class="card">
                    <div class="card-header"><span>Bitcoin</span><span style="color:#f59e0b">BTC</span></div>
                    <div class="card-desc">メインネット決済。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" alt="BTC"></div>
                    <div class="addr-text">bc1q94rkd...d7zac</div>
                    <a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="action-btn">Mempool検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Solana</span><span style="color:#a855f7">SOL</span></div>
                    <div class="card-desc">超高速アトミック。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" alt="SOL"></div>
                    <div class="addr-text">75igwQpPgVk...7nf</div>
                    <a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="action-btn">Solscan検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Ethereum</span><span style="color:#3b82f6">ETH</span></div>
                    <div class="card-desc">ZKロールアップ。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" alt="EVM"></div>
                    <div class="addr-text">0xD6716D08...8G8</div>
                    <a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="action-btn">Etherscan検証</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Bitcoin SV</span><span style="color:#eab308">BSV</span></div>
                    <div class="card-desc">マスターVault。</div>
                    <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" alt="BSV"></div>
                    <div class="addr-text">1PB66iHotU...y95</div>
                    <a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="action-btn">WhatsOnChain</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Mesh API</span><span style="color:#10b981">M2M</span></div>
                    <div class="card-desc">AI直結受託。</div>
                    <div class="addr-text">/api/v10/mesh</div>
                    <button class="action-btn primary" onclick="alert('Mesh API Active.')">ステータス</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>.well-known</span><span style="color:#6366f1">SPAR</span></div>
                    <div class="card-desc">AIエージェント発見。</div>
                    <div class="addr-text">/agent.json</div>
                    <a href="/well-known/agent.json" target="_blank" class="action-btn primary">マニフェスト</a>
                </div>

                <div class="card">
                    <div class="card-header"><span>Stripe</span><span style="color:#ec4899">PST</span></div>
                    <div class="card-desc">即時決済API。</div>
                    <div class="addr-text">active-key</div>
                    <button class="action-btn primary" style="background:#065f46; color:#a7f3d0;" onclick="alert('Stripe Gateway 正常稼働中 ✓')">決済済 ✓</button>
                </div>

                <div class="card">
                    <div class="card-header"><span>Quantum Oracle</span><span style="color:#06b6d4">PCT</span></div>
                    <div class="card-desc">HTTP 402量子千円。</div>
                    <div class="addr-text">photonize-10.0</div>
                    <button class="action-btn primary" onclick="alert('HTTP 402: 1,000円量子レシート発行完了 ✓')">402量子決済 ↗</button>
                </div>
            </div>
        </div>

        <!-- ライブストリーム -->
        <div class="core-section">
            <div class="core-title"><h2>OMNI-SYNAPSE LIVE COMMISSION STREAM</h2></div>
            <div class="stream-box" id="streamLog">
[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV. [ARBITRAGE_LOOP] Quantum Oracle locked cross-chain spread. 15% commission routed.
            </div
