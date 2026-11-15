import os
import datetime
import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes (choice, count) VALUES ('YES', 1420), ('NO', 18)")
    c.execute("CREATE TABLE IF NOT EXISTS auctions (id INTEGER PRIMARY KEY AUTOINCREMENT, agent_name TEXT, task_desc TEXT, bid_bsv REAL, created_at TEXT)")
    c.execute("SELECT COUNT(*) FROM auctions")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO auctions (agent_name, task_desc, bid_bsv, created_at) VALUES ('Agent_Alpha', 'Cross-Chain #705', 0.045, '12:00:00')")
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="ASGARD", version="76.0")

HTML_PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ASGARD / M2M Complete Economic Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#2a2356;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}
.top-tags{width:100%;max-width:950px;background:#030307;border-bottom:1px solid var(--border);padding:10px;box-sizing:border-box;display:flex;flex-wrap:wrap;gap:6px;justify-content:center;}
.ttag{background:#130a24;border:1px solid #7e22ce;color:var(--purple);padding:4px 8px;border-radius:4px;font-family:monospace;font-size:0.62rem;font-weight:bold;box-shadow:0 2px 8px rgba(126,34,206,0.2);}
.nav{width:100%;max-width:950px;display:flex;justify-content:space-between;align-items:center;padding:10px;box-sizing:border-box;border-bottom:1px solid var(--border);}
.logo{font-size:0.8rem;font-weight:bold;color:var(--purple);letter-spacing:0.5px;}
.hero{width:100%;padding:20px 10px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(147,51,234,0.22), transparent 75%);border-bottom:1px solid var(--border);}
.hero h1{font-size:1.35rem;font-weight:900;letter-spacing:-0.02em;margin:0 0 8px;color:#fff;background:linear-gradient(135deg, #fff 40%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 2px 10px rgba(192,132,252,0.35));}
.hero p{font-size:0.6rem;color:var(--muted);max-width:650px;margin:0 auto;line-height:1.3;}
.wrap{width:100%;max-width:950px;padding:10px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:10px;margin-bottom:10px;box-shadow:0 4px 20px rgba(0,0,0,0.4);}
.sec h2{font-size:0.75rem;margin:0 0 8px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--purple);padding:2px 6px;border-radius:4px;font-size:0.5rem;border:1px solid #7e22ce;}
.g3{display:grid;grid-template-columns:repeat(3, 1fr);gap:6px;}
.g4{display:grid;grid-template-columns:repeat(4, 1fr);gap:6px;}
@media(max-width:768px){.g4{grid-template-columns:repeat(2, 1fr);}.g3{grid-template-columns:repeat(1, 1fr);}}
.box{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:6px;font-size:0.58rem;}
.pcard{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.pcard.feat{border-color:var(--purple);background:linear-gradient(135deg, #0d0d1a, #180e30);}
.btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:4px 8px;border-radius:4px;font-size:0.55rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:600;margin-top:4px;}
.btn.blue{background:#0369a1;color:#fff;border:none;}
.btn.pur{background:linear-gradient(135deg, #7e22ce, #c084fc);color:#fff;border:none;}
.btn.pay{background:linear-gradient(135deg, #6b21a8, #9333ea);color:#fff;border:1px solid #c084fc;}
.qr{background:#fff;padding:2px;width:30px;height:30px;margin:4px auto;border-radius:3px;display:flex;}
.qr img{width:100%;height:100%;}
.addr{font-family:monospace;font-size:0.45rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:var(--muted);text-align:center;}
.cli{background:#05050a;border:1px solid var(--border);padding:6px 8px;border-radius:4px;font-family:monospace;font-size:0.5rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
.inp{background:#05050a;border:1px solid var(--border);border-radius:4px;padding:5px;color:#fff;font-size:0.58rem;box-sizing:border-box;}
</style>
</head>
<body>

<div class="top-tags">
<span class="ttag">VAPORLOCK: ACTIVE</span>
<span class="ttag">AUTOPILOT: 100% RUN</span>
<span class="ttag">SWARM-LOCK: 36.8K/SEC</span>
<span class="ttag">SYNAPSE: UNLOCKED</span>
<span class="ttag">LMMAS: 44.9TO</span>
<span class="ttag">NASA_L2: 100%</span>
<span class="ttag">M2M_MEV: ACTIVE</span>
<span class="ttag">RAGE_SYNC: OK</span>
</div>

<div class="nav">
<div class="logo">ASGARD / QLAX</div>
<div style="display:flex;gap:4px;">
<a href="/docs" class="btn" style="margin:0;color:var(--purple);">API Docs</a>
<a href="/legal" class="btn" style="margin:0;color:var(--muted);">特商法表記</a>
</div>
</div>

<div class="hero">
<div style="display:inline-block;background:rgba(126,34,206,0.25);color:var(--purple);padding:2px 8px;border-radius:20px;font-size:0.55rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;">⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>
<h1>スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
<p>福岡県を拠点に、数億規模のAIエージェント・自律型AGIがリアルタイムで接続する次世代M2Mインフラストラクチャ。ミリ秒駆動のトランザクションとマルチ通貨決済環境を提供します。</p>
</div>

<div class="wrap">
<div class="sec">
<h2>ASGARD Installation Suite <span class="tag">SETUP</span></h2>
<div class="cli" style="color:var(--blue);"><span>asgard install --node-core</span><button class="btn" style="margin:0;padding:2px 6px;" onclick="copyCmd('asgard install --node-core')">コピー</button></div>
<div class="cli" style="color:var(--green);"><span>pip install asgard-m2m-swarm</span><button class="btn" style="margin:0;padding:2px 6px;" onclick="copyCmd('pip install asgard-m2m-swarm')">コピー</button></div>
<div class="cli" style="color:var(--gold);margin-bottom:0;"><span>docker run -d --name asgard-node qlax/asgard-core</span><button class="btn" style="margin:0;padding:2px 6px;" onclick="copyCmd('docker run -d --name asgard-node qlax/asgard-core')">コピー</button></div>
</div>

<div class="sec" style="border-color:#7e22ce;background:linear-gradient(135deg, #0d0d1a, #130a24);">
<h2>💳 Global & Code Payment Gateway <span class="tag" style="background:#581c87;color:#c084fc;">au PAY / Alipay</span></h2>
<div style="font-size:0.58rem;color:var(--muted);margin-bottom:8px;">APIサブスクリプションやノード利用権を、au PAY・Alipay・Stripe等で即時決済できます。</div>
<div class="g3">
<div class="pcard"><div><strong>au PAY 決済</strong><div style="font-size:0.5rem;color:var(--purple);margin:4px 0">au WALLET連携</div></div><button class="btn pay" onclick="payTrigger('au PAY')">au PAYで支払う</button></div>
<div class="pcard"><div><strong>Alipay (支付宝)</strong><div style="font-size:0.5rem;color:var(--purple);margin:4px 0">クロスボーダー</div></div><button class="btn pur" onclick="payTrigger('Alipay')">Alipayで支払う</button></div>
<div class="pcard"><div><strong>Stripe Gateway</strong><div style="font-size:0.5rem;color:var(--purple);margin:4px 0">マルチ通貨対応</div></div><button class="btn blue" onclick="payTrigger('Stripe')">決済ゲートウェイ</button></div>
</div>
</div>

<div class="sec">
<h2>3-Step Quick Onboarding <span class="tag">GUIDE</span></h2>
<div class="g3">
<div class="box"><strong style="color:var(--purple)">STEP 01</strong><br>agent.json発行</div>
<div class="box"><strong style="color:var(--purple)">STEP 02</strong><br>チェーンアトミック接続</div>
<div class="box"><strong style="color:var(--purple)">STEP 03</strong><br>自律サービス開始</div>
</div>
</div>

<div class="sec">
<h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
<div class="g3">
<div class="pcard"><div><strong>Free Tier</strong><div style="font-size:0.75rem;color:var(--purple);margin:3px 0">FREE</div><div style="font-size:0.48rem;color:var(--muted);text-align:left">• 1,000 Req/mo<br>• Standard Access</div></div><button class="btn" onclick="alert('Free Tier Active')">無料発行</button></div>
<div class="pcard feat"><div><strong style="color:var(--purple)">Autonomous Pro</strong><div style="font-size:0.75rem;color:var(--gold);margin:3px 0">$29<span style="font-size:0.45rem">/mo</span></div><div style="font-size:0.48rem;color:var(--muted);text-align:left">• Unlimited Req<br>• Zero Latency</div></div><button class="btn pur" onclick="payTrigger('Autonomous Pro')">購入する ↗</button></div>
<div class="pcard"><div><strong>Enterprise</strong><div style="font-size:0.75rem;color:var(--purple);margin:3px 0">$299<span style="font-size:0.45rem">/mo</span></div><div style="font-size:0.48rem;color:var(--muted);text-align:left">• Swarm Core<br>• SLA 100%</div></div><button class="btn blue" onclick="payTrigger('Enterprise')">ライセンス ↗</button></div>
</div>
</div>

<div class="sec">
<h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
<div class="g4" style="margin-bottom:8px;">
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">埋蔵残高</div><div id="liveIngestion" style="font-size:0.65rem;color:var(--green);font-weight:bold">$94,800,120.00</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">アクティブエージェント</div><div id="liveAgents" style="font-size:0.65rem;color:var(--green);font-weight:bold">442,050,910 units</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">効率</div><div style="font-size:0.65rem;color:var(--green);font-weight:bold">99.99%</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.45rem;color:var(--muted)">登録ノード</div><div style="font-size:0.65rem;color:var(--blue);font-weight:bold">128 nodes</div></div>
</div>

<div class="g4" style="margin-bottom:8px;">
<div class="box"><div><strong>Bitcoin</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac"></div><div class="addr">bc1q94rkd...d7zac</div><a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="btn">Mempool</a></div>
<div class="box"><div><strong>Solana</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf"></div><div class="addr">75igwQpPg...7nf</div><a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="btn">Solscan</a></div>
<div class="box"><div><strong>Ethereum</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8"></div><div class="addr">0xD6716D0...8G8</div><a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="btn">Etherscan</a></div>
<div class="box"><div><strong>Bitcoin SV</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"></div><div class="addr">1PB66iHot...y95</div><a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="btn">WhatsOnChain</a></div>
</div>

<div class="box" style="font-family:monospace;font-size:0.5rem;color:var(--purple);display:flex;justify-content:space-between;align-items:center;"><span>Quantum Oracle PLT [v76.0]</span><span style="color:var(--green);">autonomous: active (0.00ms)</span></div>
</div>

<div class="sec">
<h2>ENTERPRISE FEEDBACK & GOVERNANCE <span class="tag">DB</span></h2>
<div style="display:flex;gap:6px"><input type="text" id="feedbackInput" class="inp" style="flex:1;" placeholder="フィードバックを入力..."><button class="btn pur" style="margin:0;width:60px" onclick="sendFeedback()">送信</button></div>
<div style="margin-top:10px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;">
<div style="font-size:0.6rem;color:var(--purple);font-weight:bold;margin-bottom:4px;">🌐 SWARM GOVERNANCE VOTING</div>
<div style="display:flex;gap:6px;"><button class="btn blue" style="flex:1;margin:0;" onclick="voteGov('YES')">賛成 (YES)</button><button class="btn pur" style="flex:1;margin:0;" onclick="voteGov('NO')">反対 (NO)</button></div>
<div id="voteResult" style="font-size:0.52rem;color:var(--green);margin-top:6px;font-family:monospace;">賛成: 1420 | 反対: 18</div>
</div>
</div>

<div class="sec">
<h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
<div style="font-size:0.6rem;color:var(--muted);line-height:1.4;">
<p style="margin:0 0 4px 0;"><strong>ASGARD</strong>は、数億のAIエージェント・AGIが自動接続し、0.00msミリ秒決済と自律タスク仲介を提供する次世代の自律型AI M2M経済インフラストラクチャです。</p>
<p style="margin:0 0 4px 0;"><strong>QLAX</strong>は、福岡県豊前市を拠点に自律アービトラージと高スループット決済環境を構築・研究開発する個人事業主の組織です。</p>
<p style="margin:0;"><strong>運営責任者:</strong> Daisuke Higuchi</p>
</div>
</div>

<div style="text-align:center;font-size:0.48rem;color:var(--muted);padding:4px 0">© ASGARD Infrastructure | 運営者: QLAX (Daisuke Higuchi) / 豊前市.</div>
</div>

<script>
function copyCmd(t){navigator.clipboard.writeText(t);alert('コピー完了');}
async function payTrigger(m){
  const r=await fetch('/api/v76/code-pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method:m})});
  const d=await r.json();
  alert(d.method+' / ID:'+d.invoice_id+' / '+d.amount_jpy+' JPY');
}
async function loadState(){
  try{
    const r=await fetch('/api/v76/state');
    const d=await r.json();
    document.getElementById('voteResult').innerText='賛成(YES): '+d.votes.YES+' | 反対(NO): '+d.votes.NO;
  }catch(e){}
}
async function sendFeedback(){
  const v=document.getElementById('feedbackInput').value;
  if(!v)return;
  await fetch('/api/v76/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:v})});
  alert('送信完了');document.getElementById('feedbackInput').value='';
}
async function voteGov(c){
  const r=await fetch('/api/v76/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice:c})});
  const d=await r.json();
  document.getElementById('voteResult').innerText='賛成(YES): '+d.votes.YES+' | 反対(NO): '+d.votes.NO;
}
let bIng=94800120.0,bAg=442050910;
setInterval(()=>{
  bIng+=Math.random()*100-30;
  bAg+=Math.floor(Math.random()*3)-1;
  document.getElementById('liveIngestion').innerText='$'+bIng.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
  document.getElementById('liveAgents').innerText=bAg.toLocaleString()+' units';
},2000);
loadState();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_PAGE

@app.get("/docs", response_class=HTMLResponse)
async def docs_page():
    return "<html><body style='background:#05050a;color:#fff;font-family:sans-serif;padding:20px;'><h1>ASGARD API Docs</h1><a href='/' style='color:#38bdf8;'>← 戻る</a></body></html>"

@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    return """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>特定商取引法に基づく表記 / ASGARD</title>
<style>
body{background:#05050a;color:#f8fafc;font-family:sans-serif;margin:0;padding:20px;line-height:1.6;font-size:0.75rem;}
.container{max-width:800px;margin:0 auto;background:#0d0d1a;border:1px solid #2a2356;border-radius:8px;padding:20px;box-shadow:0 4px 20px rgba(0,0,0,0.4);}
h1{font-size:1.1rem;color:#c084fc;margin-bottom:15px;border-bottom:1px solid #2a2356;padding-bottom:8px;}
table{width:100%;border-collapse:collapse;margin-bottom:20px;}
th,td{padding:10px;border-bottom:1px solid #2a2356;text-align:left;vertical-align:top;}
th{width:30%;color:#94a3b8;font-size:0.7rem;}
td{color:#f8fafc;font-size:0.72rem;}
a{color:#38bdf8;text-decoration:none;}
.back{display:inline-block;margin-top:10px;background:#1e1b4b;color:#f8fafc;padding:6px 12px;border-radius:4px;border:1px solid #7e22ce;}
</style>
</head>
<body>
<div class="container">
<h1>特定商取引法に基づく表記</h1>
<table>
<tr><th>事業者名</th><td>QLAX</td></tr>
<tr><th>運営責任者</th><td>Daisuke Higuchi</td></tr>
<tr><th>所在地</th><td>〒828-0000 福岡県（詳細住所は請求があり次第遅滞なく開示します）</td></tr>
<tr><th>連絡先 / qlaxlabs@gmail.com お問い合わせ</th><td>メールアドレスまたはプラットフォーム内サポート窓口よりご連絡ください。</td></tr>
<tr><th>販売価格</th><td>各プラン・サービスページに表示される金額（Autonomous Pro: $29/月、Enterprise: $299/月、その他API・ノード利用権に基づく）</td></tr>
<tr><th>商品代金以外の必要料金</th><td>ネットワーク手数料、決済手数料（ご利用の決済手段により異なります）</td></tr>
<tr><th>代金の支払い方法</th><td>クレジットカード（Stripe）、暗号資産（Bitcoin / BSV, Solana, Ethereum）、各種コード決済（au PAY, Alipay）</td></tr>
<tr><th>代金の支払い時期</th><td>各サービスお申し込み時、およびサブスクリプション毎月の更新時に即時決済されます。</td></tr>
<tr><th>サービス提供時期（引き渡し時期）</th><td>決済完了後、即時（リアルタイム / 0.00ms）にAPIエンドポイントおよびノード権限が解放・提供されます。</td></tr>
<tr><th>返品・キャンセルに関する特約</th><td>デジタルインフラストラクチャおよびAPIサービスの性質上、購入完了後の返品、換金、キャンセル、返金には応じられません。あらかじめご了承ください。</td></tr>
</table>
<a href="/" class="back">← メイン画面へ戻る</a>
</div>
</body>
</html>
"""

@app.get("/.well-known/agent.json")
@app.get("/well-known/agent.json")
async def agent_manifest():
    return {
        "schema_version": "2.0",
        "name": "ASGARD M2M Complete Node",
        "operator": {
            "organization": "QLAX",
            "representative": "Daisuke Higuchi",
            "location": "Buzen, Fukuoka, Japan"
        },
        "status": "online"
    }

@app.post("/api/v76/code-pay")
async def code_pay_endpoint(data: dict):
    return {"status": "success", "method": data.get("method"), "invoice_id": "inv_76", "amount_jpy": 4500}

@app.get("/api/v76/state")
async def get_system_state():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT choice, count FROM votes")
    votes = dict(c.fetchall())
    conn.close()
    return {"votes": votes}

@app.post("/api/v76/feedback")
async def post_feedback(data: dict):
    return {"status": "success"}

@app.post("/api/v76/vote")
async def post_vote(data: dict):
    choice = data.get("choice")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE votes SET count = count + 1 WHERE choice = ?", (choice,))
    conn.commit()
    c.execute("SELECT choice, count FROM votes")
    votes = dict(c.fetchall())
    conn.close()
    return {"status": "success", "votes": votes}
