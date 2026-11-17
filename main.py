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

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASGARD / Advanced AGI Swarm & M2M Infrastructure</title>
<style>
:root{
  --bg: #05030a;
  --card: #0c0817;
  --bd: #581c87;
  --bd-glow: #7c3aed;
  --tx: #22d3ee;
  --tx-main: #f8fafc;
  --pr: #7c3aed;
  --pr-hover: #6d28d9;
  --accent: #db2777;
}
body{background:var(--bg);color:var(--tx-main);font-family:sans-serif;margin:0;font-size:0.95rem;}
.wrap{width:100%;max-width:1100px;padding:16px;box-sizing:border-box;margin:0 auto}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:16px;margin-bottom:16px;box-shadow:0 4px 25px rgba(124,58,237,0.15)}
h1{font-size:1.45rem;}
h2{color:#c084fc;font-size:1.2rem;margin:0 0 14px 0;display:flex;align-items:center;letter-spacing:0.5px;}
p{font-size:0.9rem;line-height:1.5;color:#cbd5e1;}
.tag{background:var(--pr);color:#fff;padding:4px 10px;border-radius:6px;font-size:0.75rem;margin-left:8px;font-weight:bold;}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.grid-6{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:768px){.grid,.grid-4,.grid-6{grid-template-columns:1fr}}
.box{background:#07040e;border:1px solid var(--bd);border-radius:10px;padding:14px}
.btn{background:var(--pr);color:#fff;border:none;border-radius:6px;padding:8px 12px;cursor:pointer;font-weight:bold;width:100%;margin-top:8px;font-size:0.85rem;transition:all 0.2s;}
.btn:hover{background:var(--pr-hover);box-shadow:0 0 15px rgba(147,51,234,0.6);}
.btn-accent{background:var(--accent);}
.btn-accent:hover{background:#be185d;}
.qr{width:75px;height:75px;margin:6px auto;background:#fff;padding:4px;border-radius:6px;}
.barcode{width:100%;height:35px;margin:6px auto;background:#fff;padding:2px;border-radius:4px;object-fit:contain;}
.addr-box{background:#030207;border:1px solid var(--bd);padding:6px;border-radius:6px;font-family:monospace;font-size:0.65rem;color:var(--tx);word-break:break-all;margin:6px 0;text-align:left;}
input{font-size:0.9rem;}
#modalOverlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,3,10,0.85);z-index:9999;justify-content:center;align-items:center;padding:15px;box-sizing:border-box;}
#modalBox{background:#0c0817;border:2px solid var(--bd-glow);border-radius:14px;padding:20px;width:100%;max-width:450px;text-align:center;box-shadow:0 0 30px rgba(124,58,237,0.4);max-height:90vh;overflow-y:auto;}
</style>
</head>
<body>
<div style="background:#030207;border-bottom:1px solid var(--bd);border-top:1px solid var(--pr);color:#c084fc;padding:8px;font-size:0.75rem;text-align:center;letter-spacing:1px;font-weight:bold;">
VAPORLOCK: ACTIVE | PRE-INTENT AI: ON | M2M AUTO-BID: 0.00ms | SWARM-LOCK: 36.Mkc/S | ORBITAL LEO: ONLINE | AUTO-SWAP: READY
</div>

<div class="wrap">
  <div class="sec" style="text-align:center;background:radial-gradient(circle at center,#2e1065,#05030a);border-color:var(--bd-glow);">
    <div style="font-size:0.8rem;color:var(--tx);margin-bottom:8px;letter-spacing:1.5px;font-weight:bold;">GOD-TIER AGI & PRE-INTENT M2M INFRASTRUCTURE</div>
    <h1 style="color:#fff;margin:0 0 10px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
  </div>

  <!-- 【全スマホ決済 & コンビニバーコード決済完全網羅】 -->
  <div class="sec" style="border-color:var(--bd-glow);background:linear-gradient(135deg,#0c0817,#170b36);">
    <h2>Omni-Channel Pay & Convenience Barcode Gateway <span class="tag" style="background:var(--accent);">ALL PAYMENTS</span></h2>
    <p style="font-size:0.85rem;margin-bottom:14px;">コンビニ店頭端末・各種スマホ決済・QR/バーコードによる即時決済ネットワーク。</p>
    <div class="grid-6">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">au PAY</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=aupay://asgard-core" width="75" alt="auPAY"></div>
        <button class="btn" onclick="openPaymentModal('au PAY', 'au WALLETオートスワップ')">au PAY決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">Alipay (支付宝)</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=alipay://asgard-core" width="75" alt="Alipay"></div>
        <button class="btn" onclick="openPaymentModal('Alipay', 'クロスボーダー決済')">Alipay決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">PayPay</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=paypay://asgard-core" width="75" alt="PayPay"></div>
        <button class="btn" onclick="openPaymentModal('PayPay', '残高オートチャージ決済')">PayPay決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">楽天ペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=rakutenpay://asgard-core" width="75" alt="Rakuten Pay"></div>
        <button class="btn" onclick="openPaymentModal('Rakuten Pay', '楽天ポイント連動決済')">楽天ペイ決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">d払い</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=dbarai://asgard-core" width="75" alt="d barai"></div>
        <button class="btn" onclick="openPaymentModal('d払い', '電話料金合算決済')">d払い決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">メルペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=merpay://asgard-core" width="75" alt="Merpay"></div>
        <button class="btn" onclick="openPaymentModal('Merpay', 'メルカリ売上金即時決済')">メルペイ決済</button>
      </div>
    </div>

    <!-- コンビニ店頭バーコード決済セクション -->
    <div style="margin-top:14px;background:#030207;border:1px solid var(--bd);border-radius:10px;padding:14px;text-align:center;">
      <strong style="font-size:0.95rem;color:#c084fc;">🏪 コンビニ店頭バーコード決済 (7-Eleven / LAWSON / FamilyMart 他)</strong>
      <p style="font-size:0.75rem;color:#cbd5e1;margin:4px 0 10px 0;">レジ提示用共通バーコード（セブンイレブン・ローソン・ファミマ・ミニストップ対応）</p>
      <div style="background:#fff;padding:8px;border-radius:6px;display:inline-block;width:100%;max-width:320px;box-sizing:border-box;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=280x45&data=ASGARD-CONVENIENCE-BARCODE-992810" class="barcode" alt="Barcode">
        <div style="font-family:monospace;font-size:0.75rem;color:#000;font-weight:bold;letter-spacing:2px;margin-top:2px;">|||||| |||| ||||| |||| ||||||||</div>
      </div>
      <div style="margin-top:10px;">
        <button class="btn btn-accent" style="max-width:280px;display:inline-block;" onclick="openPaymentModal('Convenience Store Barcode', '全国のコンビニレジでのバーコード決済セッションを発行しました。')">コンビニ決済用バーコードを発行</button>
      </div>
    </div>
  </div>

  <!-- God-Tier Autonomous Economic Core (仮想通貨ウォレット) -->
  <div class="sec">
    <h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
    <div class="grid-4">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin:bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac" width="75" alt="BTC"></div>
        <div class="addr-box">bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac</div>
        <button class="btn" onclick="copyAddress('bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Solana</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=solana:7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf" width="75" alt="SOL"></div>
        <div class="addr-box">7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf</div>
        <button class="btn" onclick="copyAddress('7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Ethereum</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=ethereum:0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68" width="75" alt="ETH"></div>
        <div class="addr-box">0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68</div>
        <button class="btn" onclick="copyAddress('0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin SV</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95" width="75" alt="BSV"></div>
        <div class="addr-box">1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95</div>
        <button class="btn" onclick="copyAddress('1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95')">📋 コピー</button>
      </div>
    </div>
  </div>

  <div style="text-align:center;font-size:0.75rem;color:#94a3b8;padding:12px 0;">
    © ASGARD Infrastructure | 拠点: QLAX (Daisuke Higuchi) / 福岡県豊前市
  </div>
</div>

<div id="modalOverlay" onclick="closeModal()">
  <div id="modalBox" onclick="event.stopPropagation()">
    <h3 id="modalTitle" style="color:#c084fc;margin-top:0;">タイトル</h3>
    <div id="modalContent"></div>
    <button class="btn btn-accent" style="margin-top:15px;" onclick="closeModal()">閉じる</button>
  </div>
</div>

<script>
function openSimpleModal(title, text){
  document.getElementById('modalTitle').innerText = title;
  document.getElementById('modalContent').innerHTML = '<p style="color:#e2e8f0;margin-bottom:10px;">' + text + '</p>';
  document.getElementById('modalOverlay').style.display = 'flex';
}
function copyAddress(text){
  navigator.clipboard.writeText(text).then(function(){ alert('✨ アドレスをコピーしました！'); });
}
function closeModal(){
  document.getElementById('modalOverlay').style.display = 'none';
}
async function openPaymentModal(methodName, desc){
  let amount = prompt(methodName + " の決済金額（USD）を入力してください:", "50.0");
  if(!amount) return;
  let res = await fetch('/api/v111/pay', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({method: methodName.toLowerCase(), amount: parseFloat(amount)})});
  let r = await res.json();
  openSimpleModal('🚀 ' + methodName + ' 決済成功', desc + '<br>着金額: $' + r.amount);
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

@app.post("/api/v111/pay")
async def pay_op(data: dict):
    method = data.get("method", "direct")
    amt = float(data.get("amount", 50.0))
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (amt,))
    con.commit(); con.close()
    return {"status": "success", "method": method, "amount": amt}
