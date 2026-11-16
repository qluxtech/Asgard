import os
import sqlite3
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes (choice, count) VALUES ('YES', 1420), ('NO', 18)")
    c.execute("CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY, total_revenue REAL, tax_pool REAL)")
    c.execute("INSERT OR IGNORE INTO balance (id, total_revenue, tax_pool) VALUES (1, 94800120.00, 1540.50)")
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="ASGARD", version="106.0")

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASGARD / M2M Economic Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#2a2356;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;--red:#ef4444;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}
.top-tags{width:100%;max-width:1100px;background:#030307;border-bottom:1px solid var(--border);padding:10px;box-sizing:border-box;display:flex;flex-wrap:wrap;gap:6px;justify-content:center;}
.ttag{background:#130a24;border:1px solid #7e22ce;color:var(--purple);padding:5px 8px;border-radius:6px;font-family:monospace;font-size:0.7rem;font-weight:bold;}
.wrap{width:100%;max-width:1100px;padding:20px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px;margin-bottom:20px;box-shadow:0 8px 30px rgba(0,0,0,0.6);}
.sec h2{font-size:1.15rem;margin:0 0 14px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--purple);padding:4px 10px;border-radius:6px;font-size:0.8rem;border:1px solid #7e22ce;}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
@media(max-width:768px){.grid3,.grid4{grid-template-columns:1fr;}}
.box{background:#05050a;border:1px solid var(--border);border-radius:10px;padding:14px;font-size:0.95rem;}
.pcard{background:#05050a;border:1px solid var(--border);border-radius:10px;padding:16px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.pcard.feat{border-color:var(--purple);background:linear-gradient(135deg,#0d0d1a,#180e30);}
.btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:12px;border-radius:8px;font-size:0.95rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:bold;margin-top:10px;}
.btn.blue{background:#0369a1;color:#fff;border:none;}
.btn.pur{background:linear-gradient(135deg,#7e22ce,#c084fc);color:#fff;border:none;}
.btn.pay{background:linear-gradient(135deg,#6b21a8,#9333ea);color:#fff;border:1px solid #c084fc;}
.btn.red{background:linear-gradient(135deg,#b91c1c,#ef4444);color:#fff;border:none;}
.qr{background:#fff;padding:6px;width:100px;height:100px;margin:8px auto;border-radius:6px;display:flex;}
.qr img{width:100%;height:100%;}
.addr{font-family:monospace;font-size:0.75rem;background:#0f0f1d;padding:6px;border-radius:4px;word-break:break-all;color:var(--muted);text-align:center;}
.cli{background:#05050a;border:1px solid var(--border);padding:12px;border-radius:8px;font-family:monospace;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;color:var(--blue);}
.inp{background:#05050a;border:1px solid var(--border);border-radius:8px;padding:12px;color:#fff;font-size:0.95rem;box-sizing:border-box;}
#payModal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,10,0.95);z-index:999;justify-content:center;align-items:center;padding:16px;box-sizing:border-box;}
.modal-content{background:#0d0d1a;border:3px solid var(--purple);border-radius:20px;padding:30px 20px;width:100%;max-width:480px;text-align:center;}
</style>
</head>
<body>
<div class="top-tags">
<span class="ttag">VAPORLOCK: ACTIVE</span>
<span class="ttag">AUTOPILOT: 100%</span>
<span class="ttag">SWARM-LOCK: 36.8K/S</span>
<span class="ttag">SYNAPSE: UNLOCKED</span>
<span class="ttag">LMMAS: 44.9TO</span>
<span class="ttag">NASA_L2: 100%</span>
<span class="ttag">M2M_MEV: ACTIVE</span>
<span class="ttag">ORBITAL LEO: ONLINE</span>
</div>
<div class="wrap">
<div class="sec" style="text-align:center;background:radial-gradient(circle,rgba(147,51,234,0.3),transparent 75%);">
<div style="display:inline-block;background:rgba(126,34,206,0.3);color:var(--purple);padding:6px 16px;border-radius:20px;font-size:0.85rem;border:1px solid rgba(192,132,252,0.5);margin-bottom:10px;">⚡ GOD-TIER AGI & M2M ECONOMIC INFRASTRUCTURE</div>
<h1 style="font-size:1.7rem;color:#fff;line-height:1.4;margin:0 0 12px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
<p style="color:var(--muted);font-size:0.95rem;margin:0 auto;max-width:700px;">数億のAIエージェント・AGIがリアルタイムに接続する次世代のM2Mインフラストラクチャ。</p>
</div>

<div class="sec" style="border-color:var(--gold);background:linear-gradient(135deg,#0d0d1a,#1c150a);">
<h2>⚡ 収益コントロール & 自動課税 <span class="tag" style="background:#451a03;color:var(--gold);">ACTIVE</span></h2>
<div class="grid3">
<div class="box" style="text-align:center">
<div style="font-size:0.75rem;color:var(--muted)">強制課税プール</div>
<div id="taxPool" style="font-size:1.1rem;color:var(--gold);font-weight:bold;margin:6px 0">$1,540.50</div>
<button class="btn pur" onclick="drain()">ワンタップ・ドレイン</button>
</div>
<div class="box" style="text-align:center">
<div style="font-size:0.75rem;color:var(--muted)">ダークプール収益</div>
<div style="font-size:1.1rem;color:var(--green);font-weight:bold;margin:6px 0">+0.0485 BSV/s</div>
<button class="btn blue" onclick="alert('シンジケート接続完了')">シンジケート接続</button>
</div>
<div class="box" style="text-align:center">
<div style="font-size:0.75rem;color:var(--muted)">非常用キルスイッチ</div>
<div style="font-size:0.8rem;color:var(--red);margin:6px 0">GLOBAL EMERGENCY</div>
<button class="btn red" onclick="alert('キルスイッチ発動')">キルスイッチ発動</button>
</div>
</div>
</div>

<div class="sec">
<h2>ASGARD Installation Suite <span class="tag">SETUP</span></h2>
<div class="cli"><span>asgard install --node-core</span><button class="btn" style="margin:0;padding:6px 10px;width:auto;" onclick="copyCmd('asgard install --node-core')">コピー</button></div>
<div class="cli" style="color:var(--green);"><span>pip install asgard-m2m-swarm</span><button class="btn" style="margin:0;padding:6px 10px;width:auto;" onclick="copyCmd('pip install asgard-m2m-swarm')">コピー</button></div>
<div class="cli" style="color:var(--gold);margin-bottom:0;"><span>docker run -d --name asgard-node qlax/asgard-core</span><button class="btn" style="margin:0;padding:6px 10px;width:auto;" onclick="copyCmd('docker run -d --name asgard-node qlax/asgard-core')">コピー</button></div>
</div>

<div class="sec" style="border-color:#7e22ce;background:linear-gradient(135deg,#0d0d1a,#130a24);">
<h2>💳 Global & Code Payment Gateway <span class="tag" style="background:#581c87;color:#c084fc;">au PAY / Alipay</span></h2>
<div class="grid3">
<div class="pcard"><div><strong>au PAY 決済</strong><div style="font-size:0.75rem;color:var(--purple);margin:6px 0">au WALLET連携</div></div><button class="btn pay" onclick="pay('au PAY')">au PAYで支払う</button></div>
<div class="pcard"><div><strong>Alipay (支付宝)</strong><div style="font-size:0.75rem;color:var(--purple);margin:6px 0">クロスボーダー</div></div><button class="btn pur" onclick="pay('Alipay')">Alipayで支払う</button></div>
<div class="pcard"><div><strong>Stripe Gateway</strong><div style="font-size:0.75rem;color:var(--purple);margin:6px 0">マルチ通貨対応</div></div><button class="btn blue" onclick="pay('Stripe')">決済ゲートウェイ</button></div>
</div>
</div>

<div class="sec">
<h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
<div class="grid3">
<div class="pcard"><div><strong>Free Tier</strong><div style="font-size:1.1rem;color:var(--purple);margin:6px 0">FREE</div><div style="font-size:0.8rem;color:var(--muted);text-align:left">• 1,000 Req/mo<br>• Standard Access</div></div><button class="btn" onclick="alert('Free Active')">無料発行</button></div>
<div class="pcard feat"><div><strong style="color:var(--purple);">Autonomous Pro</strong><div style="font-size:1.1rem;color:var(--gold);margin:6px 0">$29/mo</div><div style="font-size:0.8rem;color:var(--muted);text-align:left">• Unlimited Req<br>• Zero Latency</div></div><button class="btn pur" onclick="pay('Autonomous Pro')">購入する ↗</button></div>
<div class="pcard"><div><strong>Enterprise</strong><div style="font-size:1.1rem;color:var(--purple);margin:6px 0">$299/mo</div><div style="font-size:0.8rem;color:var(--muted);text-align:left">• Swarm Core<br>• SLA 100%</div></div><button class="btn blue" onclick="pay('Enterprise')">ライセンス ↗</button></div>
</div>
</div>

<div class="sec">
<h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
<div class="grid4" style="margin-bottom:12px;">
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--muted)">埋蔵残高</div><div id="bIng" style="font-size:1rem;color:var(--green);font-weight:bold">$94,800,120</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--muted)">アクティブエージェント</div><div id="bAg" style="font-size:1rem;color:var(--green);font-weight:bold">442M units</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--muted)">効率</div><div style="font-size:1rem;color:var(--green);font-weight:bold">99.99%</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--muted)">登録ノード</div><div style="font-size:1rem;color:var(--blue);font-weight:bold">128 nodes</div></div>
</div>
<div class="grid4">
<div class="box"><strong>Bitcoin</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q94rkd"></div><div class="addr">bc1q94rkd...d7zac</div><a href="https://mempool.space" target="_blank" class="btn" style="padding:8px;font-size:0.85rem;">Mempool</a></div>
<div class="box"><strong>Solana</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=75igwQpPg"></div><div class="addr">75igwQpPg...7nf</div><a href="https://solscan.io" target="_blank" class="btn" style="padding:8px;font-size:0.85rem;">Solscan</a></div>
<div class="box"><strong>Ethereum</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD6716D0"></div><div class="addr">0xD6716D0...8G8</div><a href="https://etherscan.io" target="_blank" class="btn" style="padding:8px;font-size:0.85rem;">Etherscan</a></div>
<div class="box"><strong>Bitcoin SV</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1PB66iHot"></div><div class="addr">1PB66iHot...y95</div><a href="https://whatsonchain.com" target="_blank" class="btn" style="padding:8px;font-size:0.85rem;">WhatsOnChain</a></div>
</div>
</div>

<div class="sec">
<h2>ENTERPRISE FEEDBACK & GOVERNANCE <span class="tag">DB</span></h2>
<div style="display:flex;gap:8px"><input type="text" id="fb" class="inp" style="flex:1;" placeholder="フィードバックを入力..."><button class="btn pur" style="margin:0;width:80px" onclick="sendFb()">送信</button></div>
<div style="margin-top:12px;background:#05050a;border:1px solid var(--border);border-radius:8px;padding:14px;">
<div style="font-size:0.9rem;color:var(--purple);font-weight:bold;margin-bottom:8px;">🌐 SWARM GOVERNANCE VOTING</div>
<div style="display:flex;gap:8px;"><button class="btn blue" style="flex:1;margin:0;" onclick="vote('YES')">賛成 (YES)</button><button class="btn pur" style="flex:1;margin:0;" onclick="vote('NO')">反対 (NO)</button></div>
<div id="vRes" style="font-size:0.85rem;color:var(--green);margin-top:8px;font-family:monospace;">賛成: 1420 | 反対: 18</div>
</div>
</div>

<div class="sec">
<h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
<div style="font-size:0.95rem;color:var(--muted);line-height:1.6;">
<p style="margin:0 0 6px 0;"><strong>ASGARD</strong>は、数億のAIエージェント・AGIが自動接続し、0.00msミリ秒決済と自律タスク仲介を提供する次世代の自律型AI M2M経済インフラです。</p>
<p style="margin:0 0 6px 0;"><strong>QLAX</strong>は、福岡県豊前市を拠点に自律アービトラージと高スループット決済環境を構築・研究開発する個人事業主の組織です。</p>
<p style="margin:0;"><strong>運営責任者:</strong> Daisuke Higuchi</p>
</div>
</div>

<div style="text-align:center;font-size:0.75rem;color:var(--muted);padding:10px 0">&copy; ASGARD Infrastructure | 運営者: QLAX (Daisuke Higuchi) / 福岡県豊前市. <a href="/legal" style="color:var(--blue);">特商法表記</a></div>
</div>

<div id="payModal">
<div class="modal-content">
<div style="font-size:1.4rem;color:var(--purple);font-weight:bold;margin-bottom:14px;">💳 決済インプレッション</div>
<div id="mBody" style="font-size:1.1rem;margin-bottom:16px;"></div>
<div class="qr" style="width:200px;height:200px;margin:0 auto 16px auto;"><img id="mQr" src="" alt="QR"></div>
<button class="btn pur" onclick="closeModal()">閉じる (スクショ可能)</button>
</div>
</div>

<script>
function copyCmd(t){navigator.clipboard.writeText(t);alert('コピー完了');}
async function pay(m){
  const r=await fetch('/api/v106/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method:m})});
  const d=await r.json();
  document.getElementById('mBody').innerHTML='手段: <b style="color:var(--purple)">'+d.method+'</b><br>金額: <span style="color:var(--gold);font-weight:bold;">4,500 JPY</span>';
  document.getElementById('mQr').src='https://api.qrserver.com/v1/create-qr-code/?size=250x250&data='+d.method+'_inv';
  document.getElementById('payModal').style.display='flex';
}
function closeModal(){document.getElementById('payModal').style.display='none';}
async function drain(){
  const r=await fetch('/api/v106/drain',{method:'POST'});
  const d=await r.json();
  alert('ドレイン成功: '+d.drained_amount);
  loadState();
}
async function loadState(){
  try{
    const r=await fetch('/api/v106/state');
    const d=await r.json();
    document.getElementById('vRes').innerText='賛成(YES): '+d.votes.YES+' | 反対(NO): '+d.votes.NO;
    document.getElementById('taxPool').innerText='$'+d.tax_pool.toLocaleString('en-US',{minimumFractionDigits:2});
  }catch(e){}
}
async function vote(c){
  const r=await fetch('/api/v106/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice:c})});
  const d=await r.json();
  document.getElementById('vRes').innerText='賛成(YES): '+d.votes.YES+' | 反対(NO): '+d.votes.NO;
}
async function sendFb(){
  const v=document.getElementById('fb').value;
  if(!v)return;
  await fetch('/api/v106/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:v})});
  alert('送信完了');document.getElementById('fb').value='';
}
loadState();
</script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML

@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>特定商取引法に基づく表記 / ASGARD</title>
<style>
body{background:#05050a;color:#f8fafc;font-family:sans-serif;margin:0;padding:24px;line-height:1.8;font-size:1rem;}
.container{max-width:800px;margin:0 auto;background:#0d0d1a;border:1px solid #2a2356;border-radius:12px;padding:24px;}
h1{font-size:1.4rem;color:#c084fc;margin-bottom:16px;border-bottom:1px solid #2a2356;padding-bottom:10px;}
table{width:100%;border-collapse:collapse;margin-bottom:20px;}
th,td{padding:12px;border-bottom:1px solid #2a2356;text-align:left;vertical-align:top;}
th{width:35%;color:#94a3b8;font-size:0.9rem;}
td{color:#f8fafc;font-size:0.95rem;}
a{color:#38bdf8;text-decoration:none;}
</style>
</head>
<body>
<div class="container">
<h1>特定商取引法に基づく表記</h1>
<table>
<tr><th>事業者名</th><td>QLAX</td></tr>
<tr><th>運営責任者</th><td>Daisuke Higuchi</td></tr>
<tr><th>所在地</th><td>〒828-0000 福岡県豊前市（詳細住所は請求があり次第遅滞なく開示します）</td></tr>
<tr><th>連絡先 / お問い合わせ</th><td>プラットフォーム内サポート窓口よりご連絡ください。</td></tr>
<tr><th>販売価格</th><td>各プラン・サービスページに表示される金額（Autonomous Pro: $29/月, Enterprise: $299/月）</td></tr>
<tr><th>商品代金以外の必要料金</th><td>ネットワーク手数料、決済手数料</td></tr>
<tr><th>代金の支払い方法</th><td>クレジットカード（Stripe）、暗号資産、各種コード決済（au PAY, Alipay）</td></tr>
<tr><th>代金の支払い時期</th><td>お申し込み時、およびサブスクリプション毎月の更新時に即時決済されます。</td></tr>
<tr><th>サービス提供時期</th><td>決済完了後、即時にAPIエンドポイントおよびノード権限が解放されます。</td></tr>
<tr><th>返品・キャンセル</th><td>デジタルインフラの性質上、購入後の返品・キャンセル・返金には応じられません。</td></tr>
</table>
<a href="/" style="display:inline-block;margin-top:12px;background:#1e1b4b;color:#f8fafc;padding:10px 18px;border-radius:6px;border:1px solid #7e22ce;font-weight:bold;">← メイン画面へ戻る</a>
</div>
</body>
</html>"""

@app.post("/api/v106/pay")
async def pay_endpoint(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE balance SET tax_pool = tax_pool + 45.0 WHERE id = 1")
    conn.commit()
    conn.close()
    return {"status": "success", "method": data.get("method")}

@app.get("/api/v106/state")
async def state_endpoint():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT choice, count FROM votes")
    votes = dict(c.fetchall())
    c.execute("SELECT tax_pool FROM balance WHERE id = 1")
    tax_pool = c.fetchone()[0]
    conn.close()
    return {"votes": votes, "tax_pool": tax_pool}

@app.post("/api/v106/drain")
async def drain_endpoint():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT tax_pool FROM balance WHERE id = 1")
    pool = c.fetchone()[0]
    c.execute("UPDATE balance SET tax_pool = 0.0 WHERE id = 1")
    conn.commit()
    conn.close()
    return {"status": "success", "drained_amount": f"${pool:,.2f}"}

@app.post("/api/v106/feedback")
async def feedback_endpoint(data: dict):
    return {"status": "success"}

@app.post("/api/v106/vote")
async def vote_endpoint(data: dict):
    choice = data.get("choice")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE votes SET count = count + 1 WHERE choice = ?", (choice,))
    conn.commit()
    c.execute("SELECT choice, count FROM votes")
    votes = dict(c.fetchall())
    conn.close()
    return {"status": "success", "votes": votes}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
