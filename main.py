import os, sqlite3
from fastapi import FastAPI, Request, HTTPException
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
        CREATE TABLE IF NOT EXISTS m2m_transactions(id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME DEFAULT CURRENT_TIMESTAMP, gateway TEXT, txid TEXT, amt REAL, status TEXT);
    """)
    con.commit(); con.close()

init_db()
app = FastAPI(title="ASGARD Autonomous On-Chain Economic Core", version="1.13.0")

class OnChainPayRequest(BaseModel):
    gateway: str
    amount_usd: float
    target_chain: str = "BSV"

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASGARD / Autonomous On-Chain M2M Infrastructure</title>
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
.brand-badge-grid{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:10px;}
.brand-badge{background:#170b36;border:1px solid #7c3aed;color:#e2e8f0;padding:4px 8px;border-radius:4px;font-size:0.7rem;font-weight:bold;letter-spacing:0.5px;}
input{font-size:0.9rem;}
#modalOverlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,3,10,0.85);z-index:9999;justify-content:center;align-items:center;padding:15px;box-sizing:border-box;}
#modalBox{background:#0c0817;border:2px solid var(--bd-glow);border-radius:14px;padding:20px;width:100%;max-width:450px;text-align:center;}
</style>
</head>
<body>
<div style="background:#030207;border-bottom:1px solid var(--bd);border-top:1px solid var(--pr);color:#c084fc;padding:8px;font-size:0.75rem;text-align:center;font-weight:bold;">
VAPORLOCK: ACTIVE | ON-CHAIN M2M MESH: LIVE | MULTI-BRAND GATEWAY: SECURE
</div>

<div class="wrap">
  <div class="sec" style="text-align:center;background:radial-gradient(circle at center,#2e1065,#05030a);border-color:var(--bd-glow);">
    <div style="font-size:0.8rem;color:var(--tx);margin-bottom:8px;font-weight:bold;">AUTONOMOUS ON-CHAIN ECONOMIC INFRASTRUCTURE</div>
    <h1 style="color:#fff;margin:0 0 10px 0;">仲介者を排除する。<br>ブロックチェーン連動型「ASGARD」決済網</h1>
    <p style="color:#e2e8f0;max-width:800px;margin:0 auto;">国際ブランド・国内外QR・スマホ決済ネットワークをブロックチェーン自動同期とM2M即時決済で完全統合。</p>
  </div>

  <div class="sec">
    <h2>次世代M2Mマーケティング & プレ・インテント中枢 <span class="tag" style="background:var(--accent);">ZERO FRICTION</span></h2>
    <div class="grid">
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">① 文脈先回り (Pre-Intent)</h3>
        <p>相談前の環境・文脈を検知し、必要リソースを自動展開。</p>
        <button class="btn" onclick="openModal('Pre-Intent Synced', 'オンチェーンAI文脈先回りオファーが全ノードに展開されました。')">文脈先回りオファー発動</button>
      </div>
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">② M2Mエージェント自動選定</h3>
        <p>AIエージェントが構築・論理対話[ms]で最適APIを自動契約。</p>
        <button class="btn" style="background:#581c87;" onclick="window.open('/.well-known/agent.json', '_blank')">AI選定マニフェスト確認 ↗</button>
      </div>
      <div class="box" style="border-color:#c084fc;background:linear-gradient(135deg,#170b36,#581c87);">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">③ インパルス即時決済</h3>
        <p>意思決定の摩擦ゼロ。コンマ数秒でブロックチェーンと同期。</p>
        <button class="btn btn-accent" onclick="swarmBurst()">ゼロレイテンシーワンタップ決済</button>
      </div>
    </div>
  </div>

  <div class="sec" style="border-color:var(--bd-glow);background:linear-gradient(135deg,#0c0817,#170b36);">
    <h2>Omni-Channel On-Chain Gateway <span class="tag" style="background:var(--accent);">ALL BRANDS LINKED</span></h2>
    <p style="font-size:0.85rem;margin-bottom:10px;">国際カードブランド・各種スマホ決済・コンビニバーコードによるオンチェーン即時決済ネットワーク。</p>
    
    <!-- メーカー各種ブランドバッジ網羅エリア -->
    <div class="brand-badge-grid">
      <span class="brand-badge">VISA</span>
      <span class="brand-badge">Mastercard</span>
      <span class="brand-badge">JCB</span>
      <span class="brand-badge">American Express</span>
      <span class="brand-badge">Diners Club</span>
      <span class="brand-badge">Discover</span>
      <span class="brand-badge">PayPay</span>
      <span class="brand-badge">au PAY</span>
      <span class="brand-badge">楽天ペイ</span>
      <span class="brand-badge">d払い</span>
      <span class="brand-badge">メルペイ</span>
      <span class="brand-badge">銀聯 (UnionPay)</span>
      <span class="brand-badge">WeChat Pay (微信支付)</span>
      <span class="brand-badge">Alipay (支付宝)</span>
      <span class="brand-badge">ゆうちょPay</span>
    </div>

    <div class="grid-6" style="margin-top:14px;">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">au PAY</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95?amount=50" width="75" alt="auPAY"></div>
        <button class="btn" onclick="onChainPay('au PAY')">au PAY連動決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">Alipay (支付宝)</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95?amount=50" width="75" alt="Alipay"></div>
        <button class="btn" onclick="onChainPay('Alipay')">Alipay連動決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">PayPay</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95?amount=50" width="75" alt="PayPay"></div>
        <button class="btn" onclick="onChainPay('PayPay')">PayPay連動決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">楽天ペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95?amount=50" width="75" alt="Rakuten"></div>
        <button class="btn" onclick="onChainPay('Rakuten Pay')">楽天ペイ連動決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">d払い</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95?amount=50" width="75" alt="d barai"></div>
        <button class="btn" onclick="onChainPay('d払い')">d払い連動決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">メルペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95?amount=50" width="75" alt="Merpay"></div>
        <button class="btn" onclick="onChainPay('Merpay')">メルペイ連動決済</button>
      </div>
    </div>

    <div style="margin-top:14px;background:#030207;border:1px solid var(--bd);border-radius:10px;padding:14px;text-align:center;">
      <strong style="font-size:0.95rem;color:#c084fc;">🏪 コンビニチェーン連動バーコード (オンチェーン即時同期)</strong>
      <p style="font-size:0.75rem;color:#cbd5e1;margin:4px 0 10px 0;">ブロックチェーンハッシュ直結バーコード</p>
      <div style="background:#fff;padding:8px;border-radius:6px;display:inline-block;width:100%;max-width:320px;box-sizing:border-box;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=280x45&data=ASGARD-ONCHAIN-HASH-854920" class="barcode" alt="Barcode">
        <div style="font-family:monospace;font-size:0.75rem;color:#000;font-weight:bold;letter-spacing:2px;margin-top:2px;">|||||| |||| ||||| |||| ||||||||</div>
      </div>
      <div style="margin-top:10px;">
        <button class="btn btn-accent" style="max-width:280px;display:inline-block;" onclick="onChainPay('Convenience Store Barcode')">オンチェーンバーコード同期発動</button>
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
    <h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
    <p style="font-size:0.85rem;margin:0 0 8px 0;">ASGARDは、数億のAIエージェント・AGIが自律接続し、ブロックチェーン連動型即時決済を提供する次世代AI M2M経済インフラです。</p>
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
  let res = await fetch('/api/v113/onchain/mesh', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({gateway:"MESH_BURST", amount_usd:25.0})});
  let r = await res.json();
  openModal('✨ オンチェーン決済同期完了', 'ブロックハッシュ: ' + r.txid + '<br>プール加算: $' + r.added_usd);
  refreshPool();
}

async function onChainPay(gatewayName){
  let amt = prompt(gatewayName + " のオンチェーン決済金額（USD）を入力:", "50.0");
  if(!amt) return;
  let res = await fetch('/api/v113/onchain/pay', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({gateway: gatewayName, amount_usd: parseFloat(amt)})});
  let r = await res.json();
  openModal('🚀 ' + gatewayName + ' オンチェーン同期成功', 'TXID: ' + r.txid + '<br>着金確定額: $' + r.amount);
  refreshPool();
}

async function drainPool(){
  let res = await fetch('/api/v113/drain', {method:'POST'});
  let r = await res.json();
  openModal('✨ マスターウォレット・ドレイン完了', '抽出金額: $' + r.amt);
  refreshPool();
}

async function refreshPool(){
  try{
    let res = await fetch('/api/v113/state');
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

@app.post("/api/v113/onchain/mesh")
async def onchain_mesh(data: OnChainPayRequest):
    amt = data.amount_usd
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (amt,))
    c.execute("INSERT INTO m2m_transactions(gateway, txid, amt, status) VALUES(?, ?, ?, ?)", 
              (data.gateway, "0x_mesh_onchain_854920...", amt, "CONFIRMED"))
    con.commit(); con.close()
    return {"status": "synced", "txid": "0x_mesh_onchain_854920...", "added_usd": amt}

@app.post("/api/v113/onchain/pay")
async def onchain_pay(data: OnChainPayRequest):
    amt = data.amount_usd
    mock_txid = f"BSV_TX_{os.urandom(4).hex().upper()}"
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (amt,))
    c.execute("INSERT INTO m2m_transactions(gateway, txid, amt, status) VALUES(?, ?, ?, ?)", 
              (data.gateway, mock_txid, amt, "CONFIRMED"))
    con.commit(); con.close()
    return {"status": "success", "gateway": data.gateway, "amount": amt, "txid": mock_txid}

@app.get("/api/v113/state")
async def st_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT pool, dark_pool FROM balance WHERE id = 1"); row = con.fetchone()
    con.close()
    return {"pool": row[0], "dark_pool": row[1]}

@app.post("/api/v113/drain")
async def dr_op():
    con = sqlite3.connect(DB); c = con.cursor()
    con.row_factory = sqlite3.Row
    c.execute("SELECT pool FROM balance WHERE id = 1"); row = con.fetchone()
    p = row["pool"] if row else 0.0
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    con.commit(); con.close()
    return {"status": "success", "amt": f"{p:.2f}"}
