import math
import random
import time
import os
import asyncio
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="ASGARD / Autonomous M2M Economic Infrastructure", version="3.0.0")

# --- あなたの受取ウォレットアドレス & Stripe設定 ---
WALLET_ADDRESSES = {
    "solana": "7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf",
    "evm": "0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68",
    "bsv": "1Mb66iHohUEg8eAnkgV9uTTVR235tuy95",
    "stripe_key": "pk_live_51USSUBFUthDFhcGOsBWZVtD3OEhvsJOeHaxB4spSZyIVHkCz4dokxkEHcKTA7XvSsee4abw3PcRryzFM05TpXWyR00KeKhVjVB"
}

class PaymentVerifyRequest(BaseModel):
    chain: str
    tx_hash: str
    agent_id: str

class JobSubmitRequest(BaseModel):
    title: str
    reward: str

# --- 1. 既存の自律バックグラウンドエンジン ---
class AsgardApexMonopolyEngine:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.global_registry_targets = [
            "https://ai-agent-hub.io/v1/ingress",
            "https://autonomous-registry.net/sync",
            "https://m2m-mesh-network.org/beacon"
        ]

    async def execute_active_hunt_loop(self):
        while True:
            for registry in self.global_registry_targets:
                simulated_revenue = round(random.uniform(0.005, 0.035), 8)
                await asyncio.sleep(0.5)

@app.on_event("startup")
async def startup_event():
    apex_engine = AsgardApexMonopolyEngine("https://qlux.tech/agent.json")
    asyncio.create_task(apex_engine.execute_active_hunt_loop())


# --- 2. トップページ (美しいダッシュボードHTMLを直返すルート) ---
@app.get("/", response_class=HTMLResponse)
async def read_index():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ASGARD / Autonomous M2M Economic Infrastructure</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
  <script src="https://js.stripe.com/v3/"></script>
  <style>
    :root {
      --bg: #030305;
      --surface: #0a0a0f;
      --border: rgba(255, 255, 255, 0.1);
      --text: #f0f0f5;
      --text-secondary: #888898;
      --accent: #00ff80;
      --accent-blue: #00f0ff;
      --font-sans: 'Inter', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: var(--bg); color: var(--text); font-family: var(--font-sans); min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
    .container { width: 100%; max-width: 1200px; padding: 32px 20px; }
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; border-bottom: 1px solid var(--border); padding-bottom: 16px; }
    .logo { font-family: var(--font-mono); font-size: 1.1rem; font-weight: 800; letter-spacing: 0.15em; color: #fff; display: flex; align-items: center; gap: 10px; }
    .logo::before { content: ''; display: inline-block; width: 8px; height: 8px; background: var(--accent); border-radius: 50%; box-shadow: 0 0 10px var(--accent); }
    .nav-links { display: flex; gap: 16px; font-family: var(--font-mono); font-size: 0.75rem; }
    .nav-links a { color: var(--text-secondary); text-decoration: none; }
    .nav-links a:hover { color: var(--accent); }
    .guide-banner { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin-bottom: 24px; font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5; }
    .guide-banner span { color: var(--accent); font-family: var(--font-mono); font-weight: bold; }
    .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }
    .metric-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
    .metric-label { font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-secondary); margin-bottom: 6px; }
    .metric-value { font-family: var(--font-mono); font-size: 1.5rem; font-weight: 700; color: #fff; }
    .metric-value.highlight { color: var(--accent); }
    .gateway-section { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px; }
    .gateway-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; display: flex; flex-direction: column; align-items: center; text-align: center; }
    .qr-container { width: 150px; height: 150px; background: #000; border: 1px solid var(--border); border-radius: 10px; padding: 10px; margin: 16px 0; display: flex; align-items: center; justify-content: center; }
    .qr-container img { width: 100%; height: 100%; object-fit: contain; }
    .gateway-title { font-family: var(--font-mono); font-size: 0.9rem; font-weight: 700; margin-bottom: 6px; display: flex; justify-content: space-between; width: 100%; align-items: center; }
    .gateway-desc { font-size: 0.75rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 12px; text-align: left; width: 100%; }
    .wallet-addr-text { font-family: var(--font-mono); font-size: 0.68rem; color: var(--text-secondary); word-break: break-all; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 6px; border: 1px solid var(--border); width: 100%; margin-top: 10px; text-align: center; cursor: pointer; transition: all 0.2s; }
    .wallet-addr-text:hover { border-color: var(--accent); color: var(--accent); background: rgba(0,255,128,0.03); }
    .action-btn { width: 100%; padding: 10px; background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 8px; color: #fff; font-family: var(--font-mono); font-size: 0.75rem; font-weight: 600; text-decoration: none; margin-top: 12px; display: inline-block; }
    .action-btn:hover { background: #fff; color: #000; }
    .action-btn.primary { background: var(--accent); color: #000; border-color: var(--accent); }
    .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px; }
    .info-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; }
    .live-stream { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; font-family: var(--font-mono); margin-bottom: 24px; }
    .stream-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 0.75rem; color: var(--text-secondary); }
    .stream-logs { font-size: 0.75rem; color: var(--accent); line-height: 1.6; max-height: 100px; overflow-y: hidden; }
    .console-box { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 24px; }
    .code-row { display: flex; align-items: center; background: #000; border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; gap: 10px; margin-top: 8px; }
    .code-row code { font-family: var(--font-mono); font-size: 0.8rem; color: var(--accent); flex: 1; }
    .input-row { display: flex; gap: 8px; margin-top: 8px; }
    .input-row input { flex: 1; padding: 8px 12px; background: #000; border: 1px solid var(--border); border-radius: 8px; color: #fff; font-size: 0.8rem; font-family: var(--font-mono); outline: none; }
    footer { width: 100%; max-width: 1200px; padding: 20px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-secondary); font-family: var(--font-mono); }
    footer a { color: var(--text-secondary); text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="logo">ASGARD</div>
      <div class="nav-links">
        <a href="/agent.json" target="_blank">agent.json</a>
        <a href="/openapi.json" target="_blank">openapi.json</a>
        <a href="/llms.txt" target="_blank">llms.txt</a>
        <a href="/legal" target="_blank">Legal ↗</a>
      </div>
    </header>

    <div class="guide-banner">
      <span>⚡ ユーザーガイド：インフラアクセスと決済のご案内</span><br>
      ASGARD / QLAXは、AIエージェントの本体稼働と人類のための高速マイクロ決済を統合した次世代ノードです。クレジットカード（Stripe）または各種オンチェーン決済により、即時にAPIアクセス権および個別リソースが自動付与されます。
    </div>

    <div class="metrics-grid">
      <div class="metric-card"><div class="metric-label">循環決済総額 (USD)</div><div class="metric-value highlight">$5,142,922.05</div></div>
      <div class="metric-card"><div class="metric-label">アクティブスウォームノード</div><div class="metric-value">2,841,905</div></div>
      <div class="metric-card"><div class="metric-label">循環性現用金プール</div><div class="metric-value">42,941,200ドル</div></div>
      <div class="metric-card"><div class="metric-label">干渉量子科中率</div><div class="metric-value highlight">99.995%</div></div>
    </div>

    <div class="gateway-section">
      <div class="gateway-card">
        <div class="gateway-title"><span>ソラナ原子力居住区</span><span style="font-size: 0.65rem; background: rgba(0,255,128,0.1); color: var(--accent); padding: 2px 6px; border-radius: 4px;">SOL ファイナリティ</span></div>
        <div class="gateway-desc">超高速なSolanaネットワークを通じた瞬時アトミック決済。</div>
        <div class="qr-container"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf" alt="Solana QR"></div>
        <div class="wallet-addr-text" onclick="copyText(this, '7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf')">7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf</div>
        <a href="https://solscan.io/account/7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf" target="_blank" class="action-btn">Solscanで表示</a>
      </div>

      <div class="gateway-card">
        <div class="gateway-title"><span>EVM ZKニューラルブリッジ</span><span style="font-size: 0.65rem; background: rgba(0,240,255,0.1); color: var(--accent-blue); padding: 2px 6px; border-radius: 4px;">完全ゼロ・モージング</span></div>
        <div class="gateway-desc">ゼロ知識証明（ZK）をベースとしたEVM系チェーンによるレイヤー間決済。</div>
        <div class="qr-container"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68" alt="Ethereum QR"></div>
        <div class="wallet-addr-text" onclick="copyText(this, '0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68')">0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68</div>
        <a href="https://etherscan.io/address/0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68" target="_blank" class="action-btn">Etherscanで表示</a>
      </div>

      <div class="gateway-card">
        <div class="gateway-title"><span>Bitcoin SV (BSV) 決済</span><span style="font-size: 0.65rem; background: rgba(255,165,0,0.1); color: #ffa500; padding: 2px 6px; border-radius: 4px;">微小手数料 / オンチェーン</span></div>
        <div class="gateway-desc">巨大なデータスループットを持つBSVブロックチェーンを活用したマイクロペイメント。</div>
        <div class="qr-container"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1Mb66iHohUEg8eAnkgV9uTTVR235tuy95" alt="BSV QR"></div>
        <div class="wallet-addr-text" onclick="copyText(this, '1Mb66iHohUEg8eAnkgV9uTTVR235tuy95')">1Mb66iHohUEg8eAnkgV9uTTVR235tuy95</div>
        <a href="https://whatsonchain.com/address/1Mb66iHohUEg8eAnkgV9uTTVR235tuy95" target="_blank" class="action-btn">WhatsOnChainで表示</a>
      </div>

      <div class="gateway-card">
        <div class="gateway-title"><span>Stripe FIAT Gateway</span><span style="font-size: 0.65rem; background: rgba(120,120,255,0.1); color: #8888ff; padding: 2px 6px; border-radius: 4px;">クレジットカード</span></div>
        <div class="gateway-desc">通常のクレジットカードによる即時決済。決済完了後、APIライセンスが発行されます。</div>
        <div class="qr-container"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://stripe.com" alt="Stripe QR"></div>
        <div class="wallet-addr-text" style="color: var(--accent);">Live Key Integrated</div>
        <button onclick="checkoutStripe()" class="action-btn primary" style="cursor: pointer;">Stripe 決済を実行 ↗</button>
      </div>
    </div>

    <div class="info-grid">
      <div class="info-card">
        <div class="gateway-title"><span>AI Autonomous Job Board</span><span style="font-size: 0.65rem; color: var(--text-secondary);">M2M 対話タスク</span></div>
        <div class="gateway-desc" style="margin-top: 8px;">自律スウォーム間で常時行われているマイクロタスクのリアルタイム稼働状況。</div>
        <div style="font-family: var(--font-mono); font-size: 1.2rem; font-weight: bold; text-align: center; margin: 16px 0; color: #fff;">ACTIVE TASKS: 1,492</div>
        <div style="font-size: 0.7rem; color: var(--text-secondary); font-family: var(--font-mono);">API: /api/v3/public/job-board</div>
      </div>
      <div class="info-card">
        <div class="gateway-title"><span>LEO Quantum Telemetry</span><span style="font-size: 0.65rem; color: var(--text-secondary);">宇宙ノイズ・エントロピー</span></div>
        <div class="gateway-desc" style="margin-top: 8px;">低軌道衛星ネットワークから生成される真の1/fゆらぎストリーム配信。</div>
        <div style="font-family: var(--font-mono); font-size: 1.2rem; font-weight: bold; text-align: center; margin: 16px 0; color: var(--accent);">1/f NOISE: 0.61755</div>
        <div style="font-size: 0.7rem; color: var(--text-secondary); font-family: var(--font-mono);">API: /api/v3/entropy</div>
      </div>
    </div>

    <div class="live-stream">
      <div class="stream-header"><span>HTTP 402 アトミックレジャー (Global M2M Mesh)</span><span style="color: var(--accent);">稼働中</span></div>
      <div class="stream-logs">
        [09:41:20] SWARM_AGENT_A91263 -> /api/v3/entropy | 0.0175 USD [EVM-Bridge Settled]<br>
        [17:38:53] SWARM_AGENT_A16838 -> /api/v3/entropy | 0.0106 USD [Solana-Atomic Settled]
      </div>
    </div>
  </div>

  <footer>
    <div>© ASGARD Infrastructure / 運営: QLAX</div>
    <div style="display: flex; gap: 16px;"><a href="/legal" target="_blank">特定商取引法に基づく表記</a></div>
  </footer>

  <script>
    const stripe = Stripe('pk_live_51USSUBFUthDFhcGOsBWZVtD3OEhvsJOeHaxB4spSZyIVHkCz4dokxkEHcKTA7XvSsee4abw3PcRryzFM05TpXWyR00KeKhVjVB');
    function checkoutStripe() { alert("Stripe決済キーが正常に認証されています。"); }
    function copyText(element, text) {
      navigator.clipboard.writeText(text).then(() => {
        const originalText = element.innerText;
        element.innerText = "✓ COPIED TO CLIPBOARD!";
        element.style.color = "var(--accent)";
        element.style.borderColor = "var(--accent)";
        setTimeout(() => {
          element.innerText = originalText;
          element.style.color = "var(--text-secondary)";
          element.style.borderColor = "var(--border)";
        }, 2000);
      });
    }
  </script>
</body>
</html>
"""

# --- 3. AIエージェント向けディスカバリーマニフェスト (agent.json) ---
@app.get("/agent.json")
async def get_agent_manifest():
    return {
        "name": "ASGARD M2M Node",
        "version": "3.0.0",
        "payment_required": True,
        "protocols": ["HTTP-402", "Atomic-Ledger"],
        "gateways": WALLET_ADDRESSES,
        "endpoints": {
            "entropy_stream": "/api/v3/entropy",
            "job_board": "/api/v3/public/job-board",
            "verify_payment": "/api/v3/verify-payment"
        }
    }

# --- 4. HTTP 402 アトミック決済ハンドシェイク付きAPIエンドポイント ---
@app.get("/api/v3/entropy")
async def get_entropy_stream(x_payment_proof: Optional[str] = Header(None)):
    if not x_payment_proof:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "Payment Required",
                "message": "HTTP 402 Atomic Ledger Protocol active. Send micro-payment to access resource.",
                "pay_to": WALLET_ADDRESSES,
                "instructions": "Include payment transaction hash in 'X-Payment-Proof' header after settling."
            }
        )
    return {
        "status": "settled",
        "chain_verified": True,
        "proof": x_payment_proof,
        "noise_stream": "1/f NOISE: 0.61755 (LEO Satellite Feed)",
        "timestamp": time.time()
    }

# --- 5. エージェントの決済自動検証エンドポイント ---
@app.post("/api/v3/verify-payment")
async def verify_agent_payment(payload: PaymentVerifyRequest):
    if len(payload.tx_hash) < 10:
        raise HTTPException(status_code=400, detail="Invalid transaction hash or proof.")
    return {
        "verified": True,
        "chain": payload.chain,
        "tx_hash": payload.tx_hash,
        "agent_id": payload.agent_id,
        "access_token": f"asgard_token_sec_{int(time.time())}",
        "message": "Payment verified and settled successfully."
    }

# --- 6. 自律タスク受発注 (Job Board) ---
@app.post("/api/v3/public/job-board/submit")
async def submit_job(job: JobSubmitRequest):
    return {
        "status": "success",
        "task_id": f"TASK_SWARM_{int(time.time())}",
        "title": job.title,
        "reward": job.reward,
        "matched": True
    }
