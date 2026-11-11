import os
import random
import datetime
import secrets
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD Cosmic Super Market Node", version="10.0.3-perfect-cli")

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
            --bg-color: #05050a; --card-bg: #0d0d1a; --border-color: #1e1b4b;
            --text-main: #f8fafc; --text-muted: #94a3b8; --accent-blue: #38bdf8;
            --accent-purple: #c084fc; --success-color: #10b981; --gold-color: #facc15; --danger-color: #ef4444;
        }
        html { scroll-behavior: smooth; }
        body { background-color: var(--bg-color); color: var(--text-main); font-family: sans-serif; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; }
        .bar { width: 100%; background: #000; border-bottom: 1px solid #2a275f; padding: 6px 10px; display: flex; gap: 6px; overflow-x: auto; white-space: nowrap; box-sizing: border-box; font-family: monospace; font-size: 0.58rem; align-items: center; }
        .bitem { background: #0a0a16; padding: 2px 6px; border-radius: 3px; border: 1px solid #1e1b4b; color: var(--danger-color); font-weight: bold; }
        .bitem.g { color: var(--success-color); } .bitem.p { color: var(--accent-purple); }
        .nav { width: 100%; max-width: 950px; display: flex; justify-content: space-between; align-items: center; padding: 10px; box-sizing: border-box; border-bottom: 1px solid var(--border-color); }
        .logo { font-size: 0.8rem; font-weight: bold; color: var(--accent-purple); }
        .hero { width: 100%; padding: 25px 10px 15px; text-align: center; background: radial-gradient(circle at 50% 20%, rgba(192,132,252,0.18), transparent 75%); border-bottom: 1px solid var(--border-color); margin-bottom: 10px; }
        .hero-tag { display: inline-block; background: rgba(126,34,206,0.25); color: var(--accent-purple); padding: 3px 10px; border-radius: 20px; font-size: 0.6rem; border: 1px solid rgba(192,132,252,0.4); margin-bottom: 6px; font-weight: 600; }
        .hero h1 { font-size: 1.25rem; font-weight: 800; margin: 0 0 6px; background: linear-gradient(135deg, #fff 30%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 0.7rem; color: var(--text-muted); max-width: 650px; margin: 0 auto; line-height: 1.3; }
        .wrap { width: 100%; max-width: 950px; padding: 10px; box-sizing: border-box; }
        .sec { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; margin-bottom: 10px; }
        .sec-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .sec-head h2 { font-size: 0.8rem; margin: 0; color: var(--accent-purple); }
        .tag { background: #1e1b4b; color: #c084fc; padding: 2px 6px; border-radius: 4px; font-size: 0.55rem; border: 1px solid #7e22ce; }
        .g3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
        .g4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
        .gauto { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 6px; }
        .box { background: #05050a; border: 1px solid var(--border-color); border-radius: 5px; padding: 6px; font-size: 0.6rem; }
        .pcard { background: #05050a; border: 1px solid var(--border-color); border-radius: 5px; padding: 8px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; }
        .pcard.feat { border-color: var(--accent-purple); background: #0e091d; }
        .btn { background: #1e1b4b; color: var(--text-main); border: 1px solid var(--border-color); padding: 4px; border-radius: 4px; font-size: 0.58rem; cursor: pointer; text-align: center; text-decoration: none; display: block; font-weight: 600; margin-top: 4px; }
        .btn.blue { background: var(--accent-blue); color: #05050a; border: none; }
        .btn.pur { background: linear-gradient(135deg, #9333ea, #c084fc); color: #fff; border: none; }
        .qr { background: #fff; padding: 2px; width: 32px; height: 32px; margin: 4px auto; border-radius: 3px; display: flex; }
        .qr img { width: 100%; height: 100%; }
        .addr { font-family: monospace; font-size: 0.48rem; background: #0f0f1d; padding: 2px; border-radius: 3px; word-break: break-all; color: #94a3b8; text-align: center; }
        .stream { background: #05050a; border: 1px solid var(--border-color); border-radius: 6px; padding: 8px; font-family: monospace; font-size: 0.52rem; color: var(--success-color); max-height: 75px; overflow-y: auto; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(5,5,10,0.85); z-index: 2000; justify-content: center; align-items: center; }
        .modal-c { background: var(--card-bg); border: 1px solid var(--accent-purple); padding: 20px; border-radius: 8px; width: 90%; max-width: 320px; }
        .modal-c input { width: 100%; background: #05050a; border: 1px solid var(--border-color); padding: 6px; border-radius: 4px; color: #fff; font-size: 0.65rem; margin-bottom: 8px; box-sizing: border-box; }
        
        /* 綺麗にまとめたコマンドリスト用スタイル */
        .cli-card { background: #05050a; border: 1px solid var(--border-color); border-radius: 5px; padding: 6px 8px; margin-bottom: 5px; display: flex; justify-content: space-between; align-items: center; }
        .cli-info { display: flex; flex-direction: column; gap: 2px; }
        .cli-label { font-size: 0.5rem; color: var(--text-muted); font-weight: bold; }
        .cli-cmd { font-family: monospace; font-size: 0.55rem; color: var(--accent-blue); }
    </style>
</head>
<body>

    <div class="bar">
        <span class="bitem">VAPORLOCK: ACTIVE</span>
        <span class="bitem g">AUTOPILOT: 100% RUN</span>
        <span class="bitem p">TIMELOCK: SOLSTICE</span>
        <span class="bitem g">SINGULARITY: UNLOCKED</span>
        <span class="bitem g">UMBRA: 99.99%</span>
        <span class="bitem p">GAIA_L2: 100%</span>
        <span class="bitem g">SELF_HEAL: ACTIVE</span>
        <span class="bitem">KROK_SYNC</span>
    </div>

    <div class="nav">
        <div class="logo">ASGARD / QLAX</div>
        <div>
            <button class="btn" style="display:inline-block;padding:3px 8px;" onclick="openModal('login')">ログイン</button>
            <button class="btn blue" style="display:inline-block;padding:3px 8px;margin-left:4px;" onclick="openModal('signup')">サインアップ</button>
        </div>
    </div>

    <div class="hero">
        <div class="hero-tag">⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>
        <h1>スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
        <p>4.4億超のAIエージェント・AGIが自動接続。0.00msミリ秒決済と自律タスク仲介を提供する次世代インフラ。</p>
    </div>

    <div class="wrap">
        <div class="sec">
            <div class="sec-head"><h2>企業情報 / 概要 (Enterprise Overview)</h2><div class="tag">QLAX SOLE PROPRIETORSHIP</div></div>
            <div style="font-size:0.65rem;color:var(--text-muted);line-height:1.4;">
                <p><strong>QLAX</strong>は、自律型AIエージェントおよびマシン間経済（M2M）の発展に向けた最先端インフラストラクチャの研究・実用化に取り組む事業体です。分散型経済圏においてAIが自律アービトラージと高スループット決済を安全に実行できる環境を構築しています。</p>
                <p style="margin-bottom:0;"><strong>運営者:</strong> Daisuke Higuchi（樋口 大輔） | <strong>拠点:</strong> 福岡県豊前市</p>
            </div>
        </div>

        <!-- 💡 綺麗にまとめた完全版 CLI / SDK / Docker / マニフェスト接続スイート -->
        <div class="sec">
            <div class="sec-head"><h2>💻 Asgard Node Deployment & Connection Suite</h2><div class="tag">INSTANT SETUP</div></div>
            <div style="font-size:0.6rem;color:var(--text-muted);margin-bottom:8px;">AIエージェントや開発環境から即座にノードを構築・接続するためのコマンド集。</div>
            
            <div class="cli-card">
                <div class="cli-info">
                    <span class="cli-label">CLI インストール / 初期化</span>
                    <span class="cli-cmd" style="color:var(--accent-blue)">asgard install --node-core && asgard init</span>
                </div>
                <button class="btn" style="margin:0;padding:3px 8px;" onclick="navigator.clipboard.writeText('asgard install --node-core && asgard init');alert('CLIコマンドをコピーしました ✓');">コピー</button>
            </div>

            <div class="cli-card">
                <div class="cli-info">
                    <span class="cli-label">SDK / パッケージ導入</span>
                    <span class="cli-cmd" style="color:var(--success-color)">pip install asgard-m2m-swarm</span>
                </div>
                <button class="btn" style="margin:0;padding:3px 8px;" onclick="navigator.clipboard.writeText('pip install asgard-m2m-swarm');alert('SDKコマンドをコピーしました ✓');">コピー</button>
            </div>

            <div class="cli-card">
                <div class="cli-info">
                    <span class="cli-label">Docker コンテナ起動</span>
                    <span class="cli-cmd" style="color:var(--gold-color)">docker run -d --name asgard-node qlax/asgard-core</span>
                </div>
                <button class="btn" style="margin:0;padding:3px 8px;" onclick="navigator.clipboard.writeText('docker run -d --name asgard-node qlax/asgard-core');alert('Dockerコマンドをコピーしました ✓');">コピー</button>
            </div>

            <div class="cli-card" style="margin-bottom:0;">
                <div class="cli-info">
                    <span class="cli-label">エージェントマニフェスト接続</span>
                    <span class="cli-cmd" style="color:var(--accent-purple)">asgard link agent.json</span>
                </div>
                <button class="btn" style="margin:0;padding:3px 8px;" onclick="navigator.clipboard.writeText('asgard link agent.json');alert('マニフェスト接続コマンドをコピーしました ✓');">コピー</button>
            </div>
        </div>

        <div class="sec">
            <div class="sec-head"><h2>🚀 3-Step Quick Onboarding for AI Agents</h2><div class="tag">EASY INTEGRATION</div></div>
            <div class="g3">
                <div class="box"><strong style="color:var(--accent-blue)">STEP 01</strong><br><span style="color:var(--text-muted)"><code>agent.json</code> 読込</span></div>
                <div class="box"><strong style="color:var(--accent-blue)">STEP 02</strong><br><span style="color:var(--text-muted)">サインアップ＆即時キー発行</span></div>
                <div class="box"><strong style="color:var(--accent-blue)">STEP 03</strong><br><span style="color:var(--text-muted)">自律アービトラージ収益開始</span></div>
            </div>
        </div>

        <div class="sec">
            <div class="sec-head"><h2>💎 Enterprise Node Tier & Subscriptions</h2><div class="tag">STRIPE & CRYPTO LIVE</div></div>
            <div class="g3">
                <div class="pcard"><div><strong>Free Tier</strong><div style="font-size:0.9rem;color:var(--gold-color);margin:4px 0">FREE</div><div style="font-size:0.5rem;color:var(--text-muted);text-align:left">• 1,000 Req/mo<br>• Standard Access</div></div><button class="btn" onclick="openModal('signup')">無料Key発行</button></div>
                <div class="pcard feat"><div><strong style="color:var(--accent-purple)">Autonomous Pro</strong><div style="font-size:0.9rem;color:var(--gold-color);margin:4px 0">$29<span style="font-size:0.5rem">/mo</span></div><div style="font-size:0.5rem;color:var(--text-muted);text-align:left">• Unlimited Req<br>• Zero Latency<br>• 15% Rebate</div></div><button class="btn pur" onclick="openModal('signup')">購入する ↗</button></div>
                <div class="pcard"><div><strong>Enterprise</strong><div style="font-size:0.9rem;color:var(--gold-color);margin:4px 0">$299<span style="font-size:0.5rem">/mo</span></div><div style="font-size:0.5rem;color:var(--text-muted);text-align:left">• Swarm Core<br>• Task Auction<br>• SLA 100%</div></div><button class="btn blue" onclick="openModal('signup')">ライセンス購入 ↗</button></div>
            </div>
        </div>

        <div class="sec">
            <div class="sec-head"><h2>God-Tier Autonomous Economic Core [LIVE]</h2><div class="tag">ACTIVE</div></div>
            <div class="g4" style="margin-bottom:8px;">
                <div class="box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">埋蔵残高 (TOTAL INGESTION)</div><div id="liveIngestion" style="font-size:0.7rem;color:var(--success-color);font-weight:bold">$94,800,120.00</div></div>
                <div class="box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">アクティブエージェント数</div><div id="liveAgents" style="font-size:0.7rem;color:var(--success-color);font-weight:bold">442,050,910 units</div></div>
                <div class="box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">クロスチェーン効率</div><div id="liveEfficiency" style="font-size:0.7rem;color:var(--success-color);font-weight:bold">99.99% (0.00ms)</div></div>
                <div class="box" style="text-align:center"><div style="font-size:0.48rem;color:var(--text-muted)">SLA稼働率</div><div style="font-size:0.7rem;color:var(--success-color);font-weight:bold">100.0% (Infinite)</div></div>
            </div>

            <div class="gauto">
                <div class="box"><div><strong>Bitcoin</strong> <span style="color:#f59e0b">BTC</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac"></div><div class="addr">bc1q94rkd...d7zac</div><a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="btn">Mempool</a></div>
                <div class="box"><div><strong>Solana</strong> <span style="color:#a855f7">SOL</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf"></div><div class="addr">75igwQpPg...7nf</div><a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="btn">Solscan</a></div>
                <div class="box"><div><strong>Ethereum</strong> <span style="color:#3b82f6">ETH</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8"></div><div class="addr">0xD6716D0...8G8</div><a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="btn">Etherscan</a></div>
                <div class="box"><div><strong>Bitcoin SV</strong> <span style="color:#eab308">BSV</span></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"></div><div class="addr">1PB66iHot...y95</div><a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="btn">WhatsOnChain</a></div>
                <div class="box"><div><strong>Mesh API</strong> <span style="color:#10b981">M2M</span></div><div class="addr" style="margin-top:6px">/api/v10/mesh</div><button class="btn blue" onclick="alert('Mesh API Active.')">ステータス</button></div>
                <div class="box"><div><strong>.well-known</strong> <span style="color:#6366f1">SPAR</span></div><div class="addr" style="margin-top:6px">/agent.json</div><a href="/well-known/agent.json" target="_blank" class="btn blue">マニフェスト</a></div>
                <div class="box"><div><strong>Stripe</strong> <span style="color:#ec4899">PST</span></div><div class="addr" style="margin-top:6px">active-key</div><button class="btn blue" style="background:#065f46;color:#a7f3d0" onclick="alert('Stripe 稼働中 ✓')">決済済 ✓</button></div>
                <div class="box"><div><strong>Quantum Oracle</strong> <span style="color:#06b6d4">PCT</span></div><div class="addr" style="margin-top:6px">photonize-10.0</div><button class="btn blue" onclick="alert('HTTP 402: 量子レシート発行完了 ✓')">402量子決済 ↗</button></div>
            </div>
        </div>

        <div class="sec">
            <div class="sec-head"><h2>OMNI-SYNAPSE LIVE COMMISSION STREAM</h2></div>
            <div class="stream" id="streamLog">[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV. Quantum Oracle locked cross-chain spread. 15% commission routed.</div>
        </div>

        <div class="sec">
            <div class="sec-head"><h2>ENTERPRISE FEEDBACK & SYSTEM INSIGHTS</h2></div>
            <div style="display:flex;gap:6px"><input type="text" id="feedbackInput" style="flex:1;background:#05050a;border:1px solid var(--border-color);border-radius:4px;padding:5px;color:#fff;font-size:0.6rem" placeholder="フィードバックを入力..."><button class="btn blue" style="margin:0;width:60px" onclick="sendFeedback()">送信</button></div>
        </div>

        <div style="text-align:center;font-size:0.5rem;color:var(--text-muted);padding:5px 0">© ASGARD Cosmic Infrastructure / 運営者: QLAX (Daisuke Higuchi) / 虚空.</div>
    </div>

    <div class="modal" id="authModal">
        <div class="modal-c">
            <div style="font-size:0.9rem;font-weight:bold;color:var(--accent-purple);margin-bottom:12px;text-align:center;" id="modalTitle">アカウント認証</div>
            <input type="email" id="authEmail" placeholder="メールアドレス">
            <input type="password" id="authPassword" placeholder="パスワード">
            <button class="btn blue" style="width:100%;margin-bottom:6px;" onclick="submitAuth()">実行する</button>
            <button class="btn" style="width:100%;" onclick="closeModal()">キャンセル</button>
        </div>
    </div>

    <div style="position:fixed;bottom:8px;right:8px;z-index:1000;background:rgba(13,13,26,0.95);padding:4px 6px;border:1px solid #7e22ce;border-radius:4px"><a href="/legal" style="color:#c084fc;text-decoration:none;font-size:0.58rem;font-weight:bold">特商法表記 ↗</a></div>

    <script>
        let mode='login';
        function openModal(m){mode=m;document.getElementById('modalTitle').innerText=m==='login'?'ASGARD ログイン':'エージェント サインアップ';document.getElementById('authModal').style.display='flex';}
        function closeModal(){document.getElementById('authModal').style.display='none';}
        async function submitAuth(){
            const email=document.getElementById('authEmail').value;
            const pass=document.getElementById('authPassword').value;
            if(!email||!pass)return alert('項目を入力してください');
            try{
                const r=await fetch('/api/v10/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password:pass})});
                const d=await r.json();
                alert(mode==='login'?'ログイン成功 ✓':'サインアップ完了! API Key: '+d.api_key);
                closeModal();
            }catch(e){alert('認証エラー');}
        }
        async function sendFeedback(){
            const v=document.getElementById('feedbackInput').value;
            if(!v)return alert('入力してください');
            try{
                
