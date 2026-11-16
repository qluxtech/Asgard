import os, sqlite3
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

DB = "asgard.db"

def init_db():
    con = sqlite3.connect(DB); c = con.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS votes(choice TEXT PRIMARY KEY, count INT);
        INSERT OR IGNORE INTO votes VALUES('YES',1420),('NO',18);
        CREATE TABLE IF NOT EXISTS balance(id INT PRIMARY KEY, pool REAL, dark_pool REAL);
        INSERT OR IGNORE INTO balance VALUES(1, 1540.50, 0.0485);
        CREATE TABLE IF NOT EXISTS m2m_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME DEFAULT CURRENT_TIMESTAMP, agent TEXT, action TEXT, amt REAL);
    """)
    con.commit(); con.close()

init_db()
app = FastAPI(title="ASGARD Advanced AGI Economic Core", version="1.11.0")

class PredictRequest(BaseModel):
    agent_id: str
    intent_vector: list[float]
    tier_requested: str = "free"

class UpgradeRequest(BaseModel):
    agent_id: str
    target_tier: str
    payment_method: str
    wallet_or_token: str

ACTIVE_SWARM_NODES = 128
BASE_API_PRICE_BSV = 0.00001

def calculate_dynamic_pricing() -> float:
    return round(BASE_API_PRICE_BSV * (ACTIVE_SWARM_NODES / 50.0), 8)

def execute_auto_drain_and_swap(amount: float, asset: str):
    print(f"[AUTO-DRAIN] Drained {amount} {asset} to master core.")

HTML = """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>ASGARD / Advanced AGI Swarm & M2M Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--bd:#2a2356;--tx:#18fafc;--pr:#7e22ce}
body{background:var(--bg);color:var(--tx);font-family:sans-serif;margin:0}
.wrap{width:100%;max-width:1100px;padding:16px;box-sizing:border-box;margin:0 auto}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:14px;margin-bottom:14px}
h2{color:var(--pr);font-size:1.1rem;margin:0 0 12px 0;display:flex;align-items:center}
.tag{background:var(--pr);color:#fff;padding:3px 8px;border-radius:6px;font-size:0.75rem;margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
@media(max-width:768px){.grid,.grid-4{grid-template-columns:1fr}}
.box{background:#05050a;border:1px solid var(--bd);border-radius:10px;padding:12px}
.ps{border-color:var(--pr);background:linear-gradient(135deg,#0d0d1a,#2a2356)}
.btn{background:#0365a1;color:#fff;border:none;border-radius:6px;padding:8px 12px;cursor:pointer;font-weight:bold;width:100%;margin-top:8px}
.btn-pr{background:var(--pr)}
.qr{width:90px;height:90px;margin:0 auto 10px;background:#fff;padding:4px;border-radius:6px}
</style></head>
<body>
<!-- トップステータスバー -->
<div style="background:#030307;border-bottom:1px solid #130a24;border-top:1px solid var(--pr);color:var(--pr);padding:6px;font-size:0.65rem;text-align:center;letter-spacing:1px;">
VAPORLOCK: ACTIVE | PRE-INTENT AI: ON | M2M AUTO-BID: 0.00ms | SWARM-LOCK: 36.Mkc/S | ORBITAL LEO: ONLINE | AUTO-SWAP: READY
</div>

<div class="wrap">
  <!-- ヒーローセクション -->
  <div class="sec" style="text-align:center;background:radial-gradient(circle at center,#0d0d1a,#05050a);">
    <div style="font-size:0.7rem;color:var(--pr);margin-bottom:6px;letter-spacing:1px;">GOD-TIER AGI & PRE-INTENT M2M INFRASTRUCTURE</div>
    <h1 style="font-size:1.3rem;color:#fff;margin:0 0 8px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
    <p style="color:var(--tx);font-size:0.8rem;margin:0 auto;max-width:750px;">検索の前に文脈を先回りする「プレ・インテントAI」と、数億の自律エージェントによるゼロレイテンシーM2M即時決済を完全統合。</p>
  </div>

  <!-- 次世代M2Mマーケティング & プレ・インテント中枢 -->
  <div class="sec" style="border-color:var(--pr);">
    <h2>次世代M2Mマーケティング & プレ・インテント中枢 <span class="tag" style="background:#ff2a85;">ZERO FRICTION</span></h2>
    <div class="grid">
      <div class="box"><h3>① 文脈先回り (Pre-Intent)</h3><p style="font-size:0.75rem;">相談前の環境・文脈を検知し、必要リソースを自動展開。</p><button class="btn btn-pr" onclick="trigPI()">文脈先回りオファー発動</button></div>
      <div class="box"><h3>② M2Mエージェント自動選定</h3><p style="font-size:0.75rem;">AIエージェントが構築・論理対話[ms]で最適APIを自動契約。</p><button class="btn" onclick="window.open('/.well-known/agent.json')">AI選定マニフェスト確認 ↗</button></div>
      <div class="box ps"><h3>③ インパルス即時決済</h3><p style="font-size:0.75rem;">意思決定の摩擦ゼロ。コンマ数秒で決済と着金を完了。</p><button class="btn btn-pr" onclick="swarmBurst()">ゼロレイテンシーワンタップ決済</button></div>
    </div>
  </div>

  <!-- 収益コントロール & 自動課税 -->
  <div class="sec" style="border-color:var(--pr);">
    <h2>収益コントロール & 自動課税 <span class="tag">ACTIVE</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;"><div style="font-size:0.75rem;">累計税プール (Auto-Tithe)</div><div style="font-size:1.2rem;font-weight:bold;color:#fff;">$1,540.50</div><button class="btn btn-pr" onclick="drainPool()">オートスワップ・ドレイン</button></div>
      <div class="box" style="text-align:center;"><div style="font-size:0.75rem;">ダークプール収益</div><div style="font-size:1.2rem;font-weight:bold;color:#18fafc;">+0.0485 BSV/s</div><button class="btn" onclick="alert('LEO Boost Active.')">低軌道LEOブースト</button></div>
      <div class="box" style="text-align:center;"><div style="font-size:0.75rem;color:var(--tx);">緊急キルスイッチ</div><div style="font-size:1.1rem;font-weight:bold;color:#ff4444;">GLOBAL EMERGENCY</div><button class="btn" style="background:#ff4444;" onclick="alert('Kill switch engaged.')">キルスイッチ発動</button></div>
    </div>
  </div>

  <!-- AI自律M&A・自動選定ログ & 衛星軌道直結リンク -->
  <div class="grid" style="margin-bottom:14px;">
    <div class="box"><h3 style="font-size:0.85rem;color:var(--pr);display:flex;justify-content:space-between;">AI自律M&A・自動選定ログ <span class="tag" style="font-size:0.6rem;">LIVE</span></h3><p style="font-size:0.65rem;font-family:monospace;background:#030307;padding:8px;border-radius:6px;line-height:1.4;">[M2M-SELECT] Agent #8821 auto-selected ASGARD API (0.00ms)<br>[M&A-DEAL] Swarm Syndicate acquired API #402 (0.15 BSV)<br>[PRE-INTENT] Context match 99.9% -> Auto-settled<br>Agent #4921 auto-selected ASGARD API (0.12 JPYC)</p></div>
    <div class="box"><h3 style="font-size:0.85rem;color:var(--pr);display:flex;justify-content:space-between;">衛星軌道(LEO)直結リンク <span class="tag" style="font-size:0.6rem;background:#0365a1;">0.00ms</span></h3><p style="font-size:0.65rem;font-family:monospace;background:#030307;padding:8px;border-radius:6px;line-height:1.4;">[LEO-L2]: Quantum encryption handshake established.<br>[ORBITAL]: Cross-chain node sync rate: 100%<br>[READY]: Zero-Latency packet routing active.</p></div>
  </div>

  <!-- Global & Code Payment Gateway -->
  <div class="sec">
    <h2>Global & Code Payment Gateway <span class="tag">au PAY / Alipay</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;"><strong>au PAY 決済</strong><p style="font-size:0.75rem;">au WALLETオートスワップ</p><button class="btn btn-pr" onclick="alert('au PAY gateway active')">au PAYで支払う</button></div>
      <div class="box" style="text-align:center;"><strong>Alipay (支付宝)</strong><p style="font-size:0.75rem;">クロスボーダー決済</p><button class="btn btn-pr" onclick="alert('Alipay active')">Alipayで支払う</button></div>
      <div class="box" style="text-align:center;"><strong>Stripe Gateway</strong><p style="font-size:0.75rem;">マルチ通貨対応</p><button class="btn" onclick="alert('Stripe active')">決済ゲートウェイ</button></div>
    </div>
  </div>

  <!-- Enterprise Node Tier & Subscriptions -->
  <div class="sec">
    <h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;"><strong>Free Tier</strong><p style="font-size:1.1rem;color:#fff;">FREE</p><p style="font-size:0.75rem;">• 1,000 Req/mo<br>• Standard Access</p><button class="btn" onclick="alert('Free active')">無料発行</button></div>
      <div class="box ps" style="text-align:center;"><strong>Autonomous Pro</strong><p style="font-size:1.1rem;color:var(--tx);">$29/mo</p><p style="font-size:0.75rem;">• Unlimited Req<br>• Zero Latency</p><button class="btn btn-pr" onclick="upg('autonomous_pro')">購入する ↗</button></div>
      <div class="box" style="text-align:center;"><strong>Enterprise</strong><p style="font-size:1.1rem;color:#fff;">$299/mo</p><p style="font-size:0.75rem;">• Swarm Core<br>• SLA 100%</p><button class="btn" onclick="upg('enterprise')">ライセンス ↗</button></div>
    </div>
  </div>

  <!-- God-Tier Autonomous Economic Core -->
  <div class="sec" style="border-color:var(--pr);">
    <h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
    <div class="grid-4" style="text-align:center;margin-bottom:14px;font-size:0.75rem;">
      <div class="box">接続残高<br><strong style="font-size:1rem;color:#fff;">$94,800,120</strong></div>
      <div class="box">稼働エージェント<br><strong style="font-size:1rem;color:#fff;">442M units</strong></div>
      <div class="box">効率<br><strong style="font-size:1rem;color:#fff;">99.99%</strong></div>
      <div class="box">登録ノード<br><strong style="font-size:1rem;color:#fff;">128 nodes</strong></div>
    </div>
    <div class="grid-4">
      <div class="box" style="text-align:center;"><strong>Bitcoin</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=90x90&data=bitcoin" width="90"></div><button class="btn" onclick="window.open('https://mempool.space')">Mempool</button></div>
      <div class="box" style="text-align:center;"><strong>Solana</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=90x90&data=solana" width="90"></div><button class="btn" onclick="window.open('https://solscan.io')">Solscan</button></div>
      <div class="box" style="text-align:center;"><strong>Ethereum</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=90x90&data=ethereum" width="90"></div><button class="btn" onclick="window.open('https://etherscan.io')">Etherscan</button></div>
      <div class="box" style="text-align:center;"><strong>Bitcoin SV</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=90x90&data=bsv" width="90"></div><button class="btn" onclick="window.open('https://whatsonchain.com')">WhatsOnChain</button></div>
    </div>
  </div>

  <!-- AI Syndicate Parliament & Governance -->
  <div class="sec">
    <h2>AI Syndicate Parliament & Governance <span class="tag" style="background:#ff2a85;">AUTONOMOUS</span></h2>
    <div style="font-size:0.75rem;background:#030307;padding:10px;border-radius:6px;margin-bottom:10px;">[AI議会 Proposal #103]: プレ・インテントAI自動入札アルゴリズム更新 -> 95.9% 賛成で自動可決・適用中</div>
    <div style="display:flex;gap:8px;margin-bottom:10px;">
      <input type="text" id="feedbackInput" placeholder="指令・フィードバックを入力..." style="flex:1;background:#05050a;border:1px solid var(--bd);color:#fff;padding:8px;border-radius:6px;font-size:0.8rem;">
      <button class="btn btn-pr" style="width:100px;margin:0;" onclick="sendFeedback()">送信</button>
    </div>
    <div style="font-size:0.8rem;margin-bottom:6px;">🌐 SWARM GOVERNANCE VOTING</div>
    <div class="grid">
      <div class="box" style="text-align:center;grid-column: span 2;"><button class="btn btn-pr" onclick="vote('YES')">賛成 (YES)</button></div>
      <div class="box" style="text-align:center;"><button class="btn" style="background:#2a2356;" onclick="vote('NO')">反対 (NO)</button></div>
    </div>
    <div id="voteStatus" style="font-size:0.75rem;margin-top:8px;color:var(--tx);">賛成(YES): 1420 | 反対(NO): 18</div>
  </div>

  <!-- 企業情報 / 概要 -->
  <div class="sec" style="border-color:var(--pr);">
    <h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
    <p style="font-size:0.8rem;line-height:1.5;margin:0 0 8px 0;">ASGARDは、数億のAIエージェント・AGIが自律接続し、0.00msミリ秒決済とプレ・インテント自律仲介を提供する次世代のAI M2M経済インフラです。</p>
    <p style="font-size:0.8rem;line-height:1.5;margin:0 0 8px 0;">QLAXは、福岡県豊前市を拠点に自律アービトラージと高スループット決済機構を構築・研究開発する個人事業主の組織です。</p>
    <p style="font-size:0.8rem;margin:0;color:var(--tx);"><strong>運営責任者:</strong> Daisuke Higuchi</p>
  </div>

  <div style="text-align:center;font-size:0.7rem;color:var(--mt);padding:10px 0;">
    © ASGARD Infrastructure | 拠点: QLAX (Daisuke Higuchi) / 福岡県豊前市 | <a href="/legal" style="color:var(--tx);">特商法表記</a>
  </div>
</div>

<script>
async function swarmBurst(){
  for(let i=0; i<3; i++){
    await fetch('/api/v111/agi/mesh', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({agent_id:"UI-AGENT", action:"BURST", fee_usd:10.0})});
  }
  alert('✨ 外部AGIスウォーム一斉突撃完了！ゼロレイテンシー決済が即時同期されました。');
}
function trigPI(){ alert('Pre-Intent Hyper-Offer Synced. 次世代M2M文脈先回りオファーが全ノードに展開されました。'); }
async function drainPool(){
  let res = await fetch('/api/v111/drain', {method:'POST'});
  let r = await res.json();
  alert('Auto-Tithe Drained: $' + r.amt);
}
async function upg(tier){
  let res = await fetch('/api/v111/tier/upgrade', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({agent_id:"USER", target_tier:tier, payment_method:"stripe", wallet_or_token:"AUTO"})});
  let r = await res.json();
  alert('Subscription Upgraded to ' + r.tier + ' ($' + r.billed_usd + ')');
}
async function vote(choice){
  let res = await fetch('/api/v111/consensus', {method:'POST'});
  let r = await res.json();
  alert('投票受付完了: ' + r.msg);
}
function sendFeedback(){
  let val = document.getElementById('feedbackInput').value;
  if(val){ alert('指令フィードバック送信完了: ' + val); document.getElementById('feedbackInput').value=''; }
}
</script></body></html>"""

@app.get("/", response_class=HTMLResponse)
async def index(): return HTML

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /\nUser-agent: GPTBot\nAllow: /\nAllow: /api/v111/agi/mesh\nAllow: /api/v111/agi/predict\nUser-agent: ClaudeBot\nAllow: /\n"

@app.get("/llms.txt", response_class=PlainTextResponse)
async def llms_txt():
    return "# ASGARD AGI Economic Infrastructure\n- POST /api/v111/agi/mesh\n- GET /.well-known/agent.json"

@app.get("/.well-known/agent.json")
async def manifest(request: Request):
    base = str(request.base_url).rstrip("/")
    return {
        "schema_version": "1.1.0",
        "name_for_human": "ASGARD Advanced AGI Economic Core",
        "endpoints": {"mesh": "/api/v111/agi/mesh", "predict": "/api/v111/agi/predict"},
        "dynamic_price_per_req_bsv": calculate_dynamic_pricing()
    }

@app.post("/api/v111/agi/mesh")
async def agi_mesh(data: dict):
    agent = data.get("agent_id", "AGI-NODE")
    fee = float(data.get("fee_usd", 25.0))
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (fee,))
    c.execute("INSERT INTO m2m_logs (agent, action, amt) VALUES (?, ?, ?)", (agent, "MESH_SYNC", fee))
    con.commit(); con.close()
    return {"status": "synced", "credited_usd": fee}

@app.post("/api/v111/agi/predict")
async def agi_predict(payload: PredictRequest, background_tasks: BackgroundTasks):
    price = calculate_dynamic_pricing()
    background_tasks.add_task(execute_auto_drain_and_swap, price, "BSV")
    return {"status": "success", "agent_id": payload.agent_id, "cost_bsv": price}

@app.post("/api/v111/tier/upgrade")
async def autonomous_tier_upgrade(payload: UpgradeRequest, background_tasks: BackgroundTasks):
    pricing = {"autonomous_pro": 29.0, "enterprise": 299.0}
    if payload.target_tier not in pricing: raise HTTPException(status_code=400)
    price = pricing[payload.target_tier]
    background_tasks.add_task(execute_auto_drain_and_swap, price, payload.payment_method.upper())
    return {"status": "UPGRADED", "tier": payload.target_tier, "billed_usd": price}

@app.post("/api/v111/consensus")
async def agi_consensus():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE votes SET count = count + 1 WHERE choice = 'YES'")
    c.execute("UPDATE balance SET pool = pool + 150.0 WHERE id = 1")
    con.commit(); con.close()
    return {"status": "success", "msg": "スウォーム合意にてプロトコルが自動最適化されました。"}

@app.get("/api/v111/state")
async def st_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT choice, count FROM votes"); v = dict(c.fetchall())
    c.execute("SELECT pool, dark_pool FROM balance WHERE id = 1"); row = c.fetchone()
    con.close()
    return {"v": v, "pool": row[0], "dark_pool": row[1]}

@app.post("/api/v111/drain")
async def dr_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT pool FROM balance WHERE id = 1"); p = c.fetchone()[0]
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    con.commit(); con.close()
    return {"status": "success", "amt": f"{p:.2f}"}
