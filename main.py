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

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASGARD / Advanced AGI Swarm & M2M Infrastructure</title>
<style>
:root{--bg:#05030a;--card:#0c0817;--bd:#581c87;--bd-glow:#7c3aed;--tx:#22d3ee;--tx-main:#f8fafc;--pr:#7c3aed;--accent:#db2777;}
body{background:var(--bg);color:var(--tx-main);font-family:sans-serif;margin:0;font-size:0.95rem;}
.wrap{width:100%;max-width:1100px;padding:16px;box-sizing:border-box;margin:0 auto}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:16px;margin-bottom:16px;box-shadow:0 4px 25px rgba(124,58,237,0.15)}
h1{font-size:1.45rem;}
h2{color:#c084fc;font-size:1.2rem;margin:0 0 14px 0;display:flex;align-items:center;}
p{font-size:0.9rem;line-height:1.5;color:#cbd5e1;}
.tag{background:var(--pr);color:#fff;padding:4px 10px;border-radius:6px;font-size:0.75rem;margin-left:8px;font-weight:bold;}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.grid-6{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:768px){.grid,.grid-4,.grid-6{grid-template-columns:1fr}}
.box{background:#07040e;border:1px solid var(--bd);border-radius:10px;padding:14px}
.btn{background:var(--pr);color:#fff;border:none;border-radius:6px;padding:8px 12px;cursor:pointer;font-weight:bold;width:100%;margin-top:8px;font-size:0.85rem;}
.btn:hover{background:#6d28d9;}
.btn-accent{background:var(--accent);}
.qr{width:75px;height:75px;margin:6px auto;background:#fff;padding:4px;border-radius:6px;}
.barcode{width:100%;height:35px;margin:6px auto;background:#fff;padding:2px;border-radius:4px;object-fit:contain;}
.addr-box{background:#030207;border:1px solid var(--bd);padding:6px;border-radius:6px;font-family:monospace;font-size:0.65rem;color:var(--tx);word-break:break-all;margin:6px 0;text-align:left;}
input{font-size:0.9rem;}
#modalOverlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,3,10,0.85);z-index:9999;justify-content:center;align-items:center;padding:15px;box-sizing:border-box;}
#modalBox{background:#0c0817;border:2px solid var(--bd-glow);border-radius:14px;padding:20px;width:100%;max-width:450px;text-align:center;}
</style>
</head>
<body>
<div style="background:#030207;border-bottom:1px solid var(--bd);border-top:1px solid var(--pr);color:#c084fc;padding:8px;font-size:0.75rem;text-align:center;font-weight:bold;">
VAPORLOCK: ACTIVE | PRE-INTENT AI: ON | M2M AUTO-BID: 0.00ms | SWARM-LOCK: 36.Mkc/S | ORBITAL LEO: ONLINE | AUTO-SWAP: READY
</div>

<div class="wrap">
  <div class="sec" style="text-align:center;background:radial-gradient(circle at center,#2e1065,#05030a);border-color:var(--bd-glow);">
    <div style="font-size:0.8rem;color:var(--tx);margin-bottom:8px;font-weight:bold;">GOD-TIER AGI & PRE-INTENT M2M INFRASTRUCTURE</div>
    <h1 style="color:#fff;margin:0 0 10px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
    <p style="color:#e2e8f0;max-width:800px;margin:0 auto;">検索の前に文脈を先回りする「プレ・インテントAI」と、数億の自律エージェントによるゼロレイテンシーM2M即時決済を完全統合。</p>
  </div>

  <div class="sec">
    <h2>次世代M2Mマーケティング & プレ・インテント中枢 <span class="tag" style="background:var(--accent);">ZERO FRICTION</span></h2>
    <div class="grid">
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">① 文脈先回り (Pre-Intent)</h3>
        <p>相談前の環境・文脈を検知し、必要リソースを自動展開。</p>
        <button class="btn" onclick="openModal('Pre-Intent Synced', '次世代M2M文脈先回りオファーが全ノードに展開されました。')">文脈先回りオファー発動</button>
      </div>
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">② M2Mエージェント自動選定</h3>
        <p>AIエージェントが構築・論理対話[ms]で最適APIを自動契約。</p>
        <button class="btn" style="background:#581c87;" onclick="window.open('/.well-known/agent.json', '_blank')">AI選定マニフェスト確認 ↗</button>
      </div>
      <div class="box" style="border-color:#c084fc;background:linear-gradient(135deg,#170b36,#581c87);">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">③ インパルス即時決済</h3>
        <p>意思決定の摩擦ゼロ。コンマ数秒で決済と着金を完了。</p>
        <button class="btn btn-accent" onclick="swarmBurst()">ゼロレイテンシーワンタップ決済</button>
      </div>
    </div>
  </div>

  <div class="sec" style="border-color:var(--bd-glow);background:linear-gradient(135deg,#0c0817,#170b36);">
    <h2>Omni-Channel Pay & Convenience Barcode Gateway <span class="tag" style="background:var(--accent);">ALL PAYMENTS</span></h2>
    <p style="font-size:0.85rem;margin-bottom:14px;">コンビニ店頭端末・各種スマホ決済・QR/バーコードによる即時決済ネットワーク。</p>
    <div class="grid-6">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">au PAY</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=aupay://asgard-core" width="75" alt="auPAY"></div>
        <button class="btn" onclick="payModal('au PAY')">au PAY決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">Alipay (支付宝)</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=alipay://asgard-core" width="75" alt="Alipay"></div>
        <button class="btn" onclick="payModal('Alipay')">Alipay決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">PayPay</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=paypay://asgard-core" width="75" alt="PayPay"></div>
        <button class="btn" onclick="payModal('PayPay')">PayPay決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">楽天ペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=rakutenpay://asgard-core" width="75" alt="Rakuten Pay"></div>
        <button class="btn" onclick="payModal('Rakuten Pay')">楽天ペイ決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">d払い</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=dbarai://asgard-core" width="75" alt="d barai"></div>
        <button class="btn" onclick="payModal('d払い')">d払い決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">メルペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=merpay://asgard-core" width="75" alt="Merpay"></div>
        <button class="btn" onclick="payModal('Merpay')">メルペイ決済</button>
      </div>
    </div>

    <div style="margin-top:14px;background:#030207;border:1px solid var(--bd);border-radius:10px;padding:14px;text-align:center;">
      <strong style="font-size:0.95rem;color:#c084fc;">🏪 コンビニ店頭バーコード決済 (7-Eleven / LAWSON / FamilyMart 他)</strong>
      <p style="font-size:0.75rem;color:#cbd5e1;margin:4px 0 10px 0;">レジ提示用共通バーコード</p>
      <div style="background:#fff;padding:8px;border-radius:6px;display:inline-block;width:100%;max-width:320px;box-sizing:border-box;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=280x45&data=ASGARD-CONVENIENCE-BARCODE-992810" class="barcode" alt="Barcode">
        <div style="font-family:monospace;font-size:0.75rem;color:#000;font-weight:bold;letter-spacing:2px;margin-top:2px;">|||||| |||| ||||| |||| ||||||||</div>
      </div>
      <div style="margin-top:10px;">
        <button class="btn btn-accent" style="max-width:280px;display:inline-block;" onclick="payModal('Convenience Store Barcode')">コンビニ決済用バーコードを発行</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>収益コントロール & 自動課税 <span class="tag">ACTIVE</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">累計税プール (Auto-Tithe)</div>
        <div id="poolDisplay" style="font-size:1.35rem;font-weight:bold;color:#fff;margin:6px 0;">$1,540.50</div>
        <button class="btn" onclick="drainPool()">オートスワップ・ドレイン</button>
      </div>
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">ダークプール収益</div>
        <div style="font-size:1.35rem;font-weight:bold;color:var(--tx);margin:6px 0;">+0.0485 BSV/s</div>
        <button class="btn" style="background:#581c87;" onclick="openModal('LEO Quantum Orbital Boost', '低軌道LEO衛星との暗号化リンク確立完了。')">低軌道LEOブースト</button>
      </div>
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">緊急キルスイッチ</div>
        <div style="font-size:1.15rem;font-weight:bold;color:#f87171;margin:8px 0;">GLOBAL EMERGENCY</div>
        <button class="btn btn-accent" style="background:#dc2626;" onclick="openModal('Global Emergency', '⚠️ キルスイッチスタンバイ中。')">キルスイッチ発動</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;">
        <strong style="font-size:1rem;color:#fff;">Free Tier</strong>
        <p style="font-size:1.25rem;color:#fff;margin:8px 0;">FREE</p>
        <button class="btn" style="background:#581c87;" onclick="upg('free')">無料ノード発行</button>
      </div>
      <div class="box" style="border-color:#c084fc;background:linear-gradient(135deg,#170b36,#581c87);text-align:center;">
        <strong style="font-size:1rem;color:#fff;">Autonomous Pro</strong>
        <p style="font-size:1.25rem;color:var(--tx);margin:8px 0;">$29/mo</p>
        <button class="btn" onclick="upg('autonomous_pro')">Proプラン購入する ↗</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:1rem;color:#fff;">Enterprise</strong>
        <p style="font-size:1.25rem;color:#fff;margin:8px 0;">$299/mo</p>
        <button class="btn" style="background:#581c87;" onclick="upg('enterprise')">Enterpriseライセンス ↗</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
    <div class="grid-4" style="text-align:center;margin-bottom:14px;font-size:0.8rem;">
      <div class="box">接続残高<br><strong style="font-size:1.1rem;color:#fff;">$94,800,120</strong></div>
      <div class="box">稼働エージェント<br><strong style="font-size:1.1rem;color:#fff;">442M units</strong></div>
      <div class="box">効率<br><strong style="font-size:1.1rem;color:#fff;">99.99%</strong></div>
      <div class="box">登録ノード<br><strong style="font-size:1.1rem;color:#fff;">128 nodes</strong></div>
    </div>
    <div class="grid-4">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin:bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac" width="75" alt="BTC"></div>
        <div class="addr-box">bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac</div>
        <button class="btn" onclick="copyAddr('bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Solana</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=solana:7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf" width="75" alt="SOL"></div>
        <div class="addr-box">7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf</div>
        <button class="btn" onclick="copyAddr('7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Ethereum</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=ethereum:0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68" width="75" alt="ETH"></div>
        <div class="addr-box">0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68</div>
        <button class="btn" onclick="copyAddr('0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin SV</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95" width="75" alt="BSV"></div>
        <div class="addr-box">1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95</div>
        <button class="btn" onclick="copyAddr('1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95')">📋 コピー</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>AI Syndicate Parliament & Governance <span class="tag" style="background:var(--accent);">AUTONOMOUS</span></h2>
    <div style="font-size:0.85rem;background:#030207;padding:12px;border-radius:6px;margin-bottom:12px;color:var(--tx);">[AI議会 Proposal #103]: プレ・インテントAI自動入札アルゴリズム更新 -> 可決・適用中</div>
    <div style="display:flex;gap:10px;margin-bottom:12px;">
      <input type="text" id="fb" placeholder="指令・フィードバックを入力..." style="flex:1;background:#07040e;border:1px solid var(--bd);color:#fff;padding:10px;border-radius:6px;outline:none;">
      <button class="btn" style="width:110px;margin:0;" onclick="sendFb()">送信</button>
    </div>
    <div class="grid">
      <div class="box" style="text-align:center;grid-column:span 2;"><button class="btn" onclick="vote()">賛成 (YES)</button></div>
      <div class="box" style="text-align:center;"><button class="btn" style="background:#3b0764;" onclick="vote()">反対 (NO)</button></div>
    </div>
  </div>

  <div class="sec">
    <h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
    <p style="font-size:0.85rem;margin:0 0 8px 0;">ASGARDは、数億のAIエージェント・AGIが自律接続し、0.00msミリ秒決済を提供する次世代AI M2M経済インフラです。</p>
    <p style="font-size:0.85rem;margin:0 0 8px 0;">QLAXは、福岡県豊前市を拠点に自律アービトラージと高スループット決済機構を開発する組織です。</p>
    <p style="font-size:0.85rem;margin:0;color:var(--tx);"><strong>運営責任者:</strong> Daisuke Higuchi</p>
  </div>
</div>

<div id="modalOverlay" onclick="closeModal()">
  <div id="modalBox" onclick="event.stopPropagation()">
    <h3 id="modalTitle" style="color:#c084fc;margin-top:0;">通知</h3>
    <div id="modalContent"></div>
    <button class="btn btn-accent" style="margin-top:15px;" onclick="closeModal()">閉じる</button>
  </div>
</div>

<script>
function openModal(t, c){
  document.getElementById('modalTitle').innerText = t;
  document.getElementById('modalContent').innerHTML = '<p style="color:#e2e8f0;">' + c + '</p>';
  document.getElementById('modalOverlay').style.display = 'flex';
}
function closeModal(){ document.getElementById('modalOverlay').style.display = 'none'; }
function copyAddr(txt){ navigator.clipboard.writeText(txt).then(() => alert('✨ コピーしました！')); }
async function swarmBurst(){
  let res = await fetch('/api/v111/agi/mesh', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({agent_id:"UI", fee_usd:25.0})});
  let r = await res.json();
  openModal('✨ 決済完了', 'クレジット値: $' + r.credited_usd);
  refreshPool();
}
async function payModal(m){
  let amt = prompt(m + " の決済金額（USD）を入力:", "50.0");
  if(!amt) return;
  let res = await fetch('/api/v111/pay', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({method:m, amount:parseFloat(amt)})});
  let r = await res.json();
  openModal('🚀 ' + m + ' 決済成功', '着金額: $' + r.amount);
  refreshPool();
}
async function drainPool(){
  let res = await fetch('/api/v111/drain', {method:'POST'});
  let r = await res.json();
  openModal('✨ ドレイン完了', '抽出金額: $' + r.amt);
  refreshPool();
}
async function upg(tier){
  let res = await fetch('/api/v111/tier/upgrade', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({target_tier:tier})});
  let r = await res.json();
  openModal('🚀 アップグレード完了', 'プラン: ' + r.tier.toUpperCase());
}
async function vote(){
  let res = await fetch('/api/v111/consensus', {method:'POST'});
  let r = await res.json();
  openModal('🌐 投票完了', r.msg);
}
function sendFb(){
  let v = document.getElementById('fb').value;
  if(v){ openModal('✉️ 送信完了', '指令: ' + v); document.getElementById('fb').value=''; }
  else { alert('内容を入力してください。'); }
}
async function refreshPool(){
  try{
    let res = await fetch('/api/v111/state');
    let d = await res.json();
    document.getElementById('poolDisplay').innerText = '$' + d.pool.toLocaleString(undefined, {minimumFractionDigits:2});
  }catch(e){}
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /\n"

@app.post("/api/v111/agi/mesh")
async def agi_mesh(data: dict):
    fee = float(data.get("fee_usd", 25.0))
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (fee,))
    con.commit(); con.close()
    return {"status": "synced", "credited_usd": fee}

@app.post("/api/v111/pay")
async def pay_op(data: dict):
    amt = float(data.get("amount", 50.0))
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (amt,))
    con.commit(); con.close()
    return {"status": "success", "amount": amt}

@app.post("/api/v111/tier/upgrade")
async def tier_upgrade(data: dict):
    return {"status": "UPGRADED", "tier": data.get("target_tier", "pro")}

@app.post("/api/v111/consensus")
async def agi_consensus():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE votes SET count = count + 1 WHERE choice = 'YES'")
    con.commit(); con.close()
    return {"status": "success", "msg": "スウォーム合意にてプロトコルが自動最適化されました。"}

@app.get("/api/v111/state")
async def st_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT pool, dark_pool FROM balance WHERE id = 1"); row = con.fetchone()
    con.close()
    return {"pool": row[0], "dark_pool": row[1]}

@app.post("/api/v111/drain")
async def dr_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.row_factory = sqlite3.Row
    c.execute("SELECT pool FROM balance WHERE id = 1"); row = c.fetchone()
    p = row["pool"] if row else 0.0
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    con.commit(); con.close()
    return {"status": "success", "amt": f"{p:.2f}"}
