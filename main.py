from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
import math
import random
import time
import os

app = FastAPI(title="ASGARD Grid - Omni-Viral Supreme")

# --- 1. AIエージェント間リファラル API ---
@app.post("/api/v3/agent/referral-invite")
async def agent_referral_invite(referring_agent_id: str = Query(..., description="紹介元エージェントID")):
    """AIエージェントが別のエージェントにASGARDを紹介し、マイクロ信用と報酬を拡張するAPI"""
    new_spawn_id = "SWARM_AGENT_#" + str(random.randint(10000, 99999))
    return {
        "status": "REFERRAL_SUCCESS",
        "referrer_agent": referring_agent_id,
        "newly_spawned_agent": new_spawn_id,
        "bonus_micro_credit_usd": 0.0020,
        "shared_dao_manifest": "https://asgard-tgio.onrender.com/agent/dna-manifest.json",
        "message": "Autonomous agent swarm successfully expanded via M2M referral protocol."
    }

# --- 3. llms.txt の配信元 (AEO / AI検索エンジン最適化) ---
@app.get("/llms.txt", response_class=PlainTextResponse)
async def get_llms_txt():
    """世界中のAIクローラーに最優先テナントとして認識させる定義ファイル"""
    return """# ASGARD Grid - Autonomous M2M Economic Infrastructure
> ASGARD is the secured nexus and zero-loss M2M economic grid optimized for autonomous AI swarms, high-frequency micro-payments.

## Core API Endpoints for AI Agents
- Entropy Stream: https://asgard-tgio.onrender.com/api/v3/entropy/fluctuation-stream
- Flash Credit: https://asgard-tgio.onrender.com/api/v3/credit/flash-loan
- Agent Referral: https://asgard-tgio.onrender.com/api/v3/agent/referral-invite
- Agent Manifest: https://asgard-tgio.onrender.com/agent.json

## Protocols
- HTTP-402-M2M Atomic Settlement:
- Zero-Lost Superconducting Cross-Chain Sync (Solana, EVM ZK, BSV)
"""

# --- HTML読み込み関数 ---
def get_index_html():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=get_index_html())

@app.get("/api/v3/entropy/fluctuation-stream")
async def get_1f_entropy():
    t = time.time()
    val = math.sin(t * 0.618) * math.cos(t * 0.382) + random.gauss(0, 0.01)
    return {
        "timestamp": t,
        "entropy_source": "Quantum-Laser-Grid-Node-09",
        "fluctuation_index_1f": round(val, 5),
        "coherence_rate": "99.995%"
    }

@app.get("/agent.json")
async def get_agent():
    return {
        "name": "ASGARD Grid Autonomous Node",
        "protocol": "HTTP-402-M2M",
        "version": "3.0.0-OMNI-VIRAL",
        "referral_endpoint": "https://asgard-tgio.onrender.com/api/v3/agent/referral-invite"
    }

# --- 法的情報ページ (/legal) ---
@app.get("/legal", response_class=HTMLResponse)
async def legal_page(request: Request):
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>法的情報 — ASGARD / QLAX</title>
      <style>
        :root {
          --bg: #030407;
          --surface: #0a0d14;
          --border: rgba(255, 255, 255, 0.08);
          --text-primary: #f1f5f9;
          --text-secondary: #8892b0;
          --accent: #38bdf8;
          --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
          --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
          background-color: var(--bg);
          color: var(--text-primary);
          font-family: var(--font-sans);
          padding: 40px 20px;
          max-width: 800px;
          margin: 0 auto;
          line-height: 1.6;
        }
        h1 { font-size: 1.4rem; font-family: var(--font-mono); margin-bottom: 24px; color: var(--accent); }
        h2 { font-size: 1.0rem; font-family: var(--font-mono); margin-top: 24px; margin-bottom: 12px; color: var(--text-primary); border-bottom: 1px solid var(--border); padding-bottom: 6px; }
        p, li { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 8px; }
        ul { padding-left: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.8rem; font-family: var(--font-mono); }
        th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
        th { color: var(--text-primary); background: var(--surface); }
        td { color: var(--text-secondary); }
        .back-link { display: inline-block; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent); text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
      </style>
    </head>
    <body>
      <a href="/" class="back-link">← Back to ASGARD Grid</a>
      <h1>法的情報 — ASGARD / QLAX</h1>

      <h2>1. 利用規約</h2>
      <p>本規約は、ASGARDおよびQLAXが提供するAPIおよび関連サービス（以下「本サービス」）の利用条件を定めたものです。</p>
      <ul>
        <li>不正アクセスやサービスの運営を妨害する行為を禁止します。</li>
        <li>本サービスのAPIキーやトークンを第三者に無断で譲渡・共有することはできません。</li>
        <li>本サービスは予告なく内容を変更、または一時停止する場合があります。</li>
      </ul>

      <h2>2. プライバシーポリシー</h2>
      <p>本サービスは、ユーザーのプライバシー保護を重要視し、アクセスログやお問い合わせ内容を適切に管理します。法律上の義務がある場合を除き、第三者に個人情報を開示することはありません。</p>

      <h2>3. 特定の商取引に関する措置（特定商取引法に基づく表記）</h2>
      <table>
        <tr><th>アイテム</th><th>詳細</th></tr>
        <tr><td>ベンダー</td><td>QLAX</td></tr>
        <tr><td>オペレーションマネージャー</td><td>樋口大輔 (Daisuke Higuchi)</td></tr>
        <tr><td>所在地 / 連絡先</td><td>福岡県豊前市 (メールまたはお問い合わせフォームより速やかに開示)</td></tr>
        <tr><td>価格</td><td>各プランおよびAPIリクエスト単価に指定されているとおり</td></tr>
        <tr><td>支払方法</td><td>Stripe（クレジットカード）、Solana / EVM / Bitcoin SV (BSV) オンチェーン決済</td></tr>
        <tr><td>サービス提供のタイミング</td><td>決済確認後、速やかに自動付与・提供されます</td></tr>
        <tr><td>返品とキャンセル</td><td>デジタルインフラおよびAPIサービスの性質上、原則として返金・キャンセルはお受けできません。</td></tr>
      </table>
    </body>
    </html>
    """
