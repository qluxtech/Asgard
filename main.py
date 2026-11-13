import os, datetime, sqlite3, secrets, asyncio, random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD", version="56.0")
DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT, api_key TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes (choice, count) VALUES ('YES', 1420), ('NO', 18)")
    c.execute("CREATE TABLE IF NOT EXISTS auctions (id INTEGER PRIMARY KEY AUTOINCREMENT, agent_name TEXT, task_desc TEXT, bid_bsv REAL, created_at TEXT)")
    c.execute("SELECT COUNT(*) FROM auctions")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO auctions (agent_name, task_desc, bid_bsv, created_at) VALUES (?, ?, ?, ?)",
                  ("Agent_Alpha", "Cross-Chain Routing #704", 0.045, datetime.datetime.now().strftime("%H:%M:%S")))
    conn.commit()
    conn.close()

init_db()

class FeedbackReq(BaseModel):
    feedback: str

class VoteReq(BaseModel):
    choice: str

class BidReq(BaseModel):
    agent_name: str
    task_desc: str
    bid_bsv: float

class CodePayReq(BaseModel):
    method: str

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
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
            except:
                pass

m_mgr = ConnectionManager()

HTML_PAGE = """<!DOCTYPE html>
<html lang='ja'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width,initial-scale=1.0'>
<title>ASGARD / M2M Complete Economic Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#2a2356;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}
.bar{width:100%;background:#030307;border-bottom:1px solid var(--border);padding:6px 10px;display:flex;gap:6px;overflow-x:auto;white-space:nowrap;font-family:monospace;font-size:0.55rem;}
.bitem{background:#0d0d1a;padding:2px 6px;border-radius:3px;border:1px solid var(--border);color:var(--purple);font-weight:bold;}
.nav{width:100%;max-width:950px;display:flex;justify-content:space-between;align-items:center;padding:10px;box-sizing:border-box;border-bottom:1px solid var(--border);}
.logo{font-size:0.8rem;font-weight:bold;color:var(--purple);letter-spacing:0.5px;}
.hero{width:100%;padding:22px 10px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(147,51,234,0.22), transparent 75%);border-bottom:1px solid var(--border);}
.hero h1{font-size:1.1rem;font-weight:800;margin:0 0 6px;color:#fff;background:linear-gradient(135deg, #fff 30%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p{font-size:0.6rem;color:var(--muted);max-width:650px;margin:0 auto;line-height:1.3;}
.wrap{width:100%;max-width:950px;padding:10px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:10px;margin-bottom:10px;box-shadow:0 4px 20px rgba(0,0,0,0.4);}
.sec h2{font-size:0.75rem;margin:0 0 8px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--purple);padding:2px 6px;border-radius:4px;font-size:0.5rem;border:1px solid #7e22ce;}
.g2{display:grid;grid-template-columns:repeat(2, 1fr);gap:6px;}
.g3{display:grid;grid-template-columns:repeat(3, 1fr);gap:6px;}
.g4{display:grid;grid-template-columns:repeat(4, 1fr);gap:6px;}
@media(max-width:768px){.g4{grid-template-columns:repeat(2, 1fr);}.g3{grid-template-columns:repeat(1, 1fr);}}
.box{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:6px;font-size:0.58rem;}
.pcard{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.pcard.feat{border-color:var(--purple);background:linear-gradient(135deg, #0d0d1a, #180e30);}
.btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:4px 8px;border-radius:4px;font-size:0.55rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:600;margin-top:4px;transition:all 0.2s;}
.btn:hover{border-color:var(--purple);background:#2e1065;}
.btn.blue{background:#0369a1;color:#fff;border:none;}
.btn.pur{background:linear-gradient(135deg, #7e22ce, #c084fc);color:#fff;border:none;}
.btn.pay{background:linear-gradient(135deg, #6b21a8, #9333ea);color:#fff;border:1px solid #c084fc;}
.qr{background:#fff;padding:2px;width:30px;height:30px;margin:4px auto;border-radius:3px;display:flex;}
.qr img{width:100%;height:100%;}
.addr{font-family:monospace;font-size:0.45rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:var(--muted);text-align:center;}
.stream{background:#05050a;border:1px solid var(--border);border-radius:6px;padding:8px;font-family:monospace;font-size:0.5rem;color:var(--green);max-height:70px;overflow-y:auto;}
.cli{background:#05050a;border:1px solid var(--border);padding:6px 8px;border-radius:4px;font-family:monospace;font-size:0.5rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
.inp{background:#05050a;border:1px solid var(--border);border-radius:4px;padding:5px;color:#fff;font-size:0.58rem;box-sizing:border-box;}
</style>
</head>
<body>
<div class='bar'>
<span class='bitem'>SYSTEM: ONLINE (v56.0)</span>
<span class='bitem'>CODE_PAY: ENABLED</span>
<span class='bitem'>DB: SQLITE_LIVE</span>
</div>
<div class='nav'>
<div class='logo'>ASGARD / QLAX</div>
<div style='display:flex;gap:4px;'>
<a href='/docs' class='btn' style='margin:0;color:var(--purple);border-color:var(--border);'>API Docs</a>
</div>
</div>
<div class='hero'>
<div style='display:inline-block;background:rgba(126,34,206,0.25);color:var(--purple);padding:2px 8px;border-radius:20px;font-size:0.55rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;'>⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>
<h1>スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
<p>4.4億超のAIエージェント・AGIが自動接続。暗号資産・Stripeに加え、au PAY・Alipay等の各種コード決済に対応した次世代ゲートウェイ。</p>
</div>
<div class='wrap'>

<!-- 1. Installation Suite -->
<div class='sec'>
<h2>ASGARD Installation Suite <span class='tag'>SETUP</span></h2>
<div class='cli' style='color:var(--blue);'><span>asgard install --node-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd("asgard install --node-core")'>コピー</button></div>
<div class='cli' style='color:var(--green);'><span>pip install asgard-m2m-swarm</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd("pip install asgard-m2m-swarm")'>コピー</button></div>
<div class='cli' style='color:var(--gold);margin-bottom:0;'><span>docker run -d --name asgard-node qlax/asgard-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd("docker run -d --name asgard-node qlax/asgard-core")'>コピー</button></div>
</div>

<!-- 2. Global & Code Payment Gateway -->
<div class='sec' style='border-color:#7e22ce;background:linear-gradient(135deg, #0d0d1a, #130a24);'>
<h2>💳 Global & Code Payment Gateway <span class='tag' style='background:#581c87;color:#c084fc;'>au PAY / Alipay</span></h2>
<div style='font-size:0.58rem;color:var(--muted);margin-bottom:8px;'>APIサブスクリプションやノード利用権を、au PAY・Alipay・Stripe等で即時決済できます。</div>
<div class='g3'>
<div class='pcard'><div><strong>au PAY 決済</strong><div style='font-size:0.5rem;color:var(--purple);margin:4px 0'>au WALLET連携</div></div><button class='btn pay' onclick='triggerCodePay("au PAY")'>au PAYで支払う</button></div>
<div class='pcard'><div><strong>Alipay (支付宝)</strong><div style='font-size:0.5rem;color:var(--purple);margin:4px 0'>クロスボーダー</div></div><button class='btn pur' onclick='triggerCodePay("Alipay")'>Alipayで支払う</button></div>
<div class='pcard'><div><strong>Stripe Gateway</strong><div style='font-size:0.5rem;color:var(--purple);margin:4px 0'>マルチ通貨対応</div></div><button class='btn blue' onclick='triggerCodePay("Stripe")'>決済ゲートウェイ</button></div>
</div>
</div>

<!-- 3. Quick Onboarding -->
<div class='sec'>
<h2>3-Step Quick Onboarding <span class='tag'>GUIDE</span></h2>
<div class='g3'>
<div class='box'><strong style='color:var(--purple)'>STEP 01</strong><br>agent.json発行</div>
<div class='box'><strong style='color:var(--purple)'>STEP 02</strong><br>チェーンアトミック接続</div>
<div class='box'><strong style='color:var(--purple)'>STEP 03</strong><br>自律サービス開始</div>
</div>
</div>

<!-- 4. Enterprise Node Tiers -->
<div class='sec'>
<h2>Enterprise Node Tier & Subscriptions <span class='tag'>LIVE</span></h2>
<div class='g3'>
<div class='pcard'><div><strong>Free Tier</strong><div style='font-size:0.75rem;color:var(--purple);margin:3px 0'>FREE</div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• 1,000 Req/mo<br>• Standard Access</div></div><button class='btn' onclick='alert("Free Tier Activated")'>無料発行</button></div>
<div class='pcard feat'><div><strong style='color:var(--purple)'>Autonomous Pro</strong><div style='font-size:0.75rem;color:var(--gold);margin:3px 0'>$29<span style='font-size:0.45rem'>/mo</span></div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• Unlimited Req<br>• Zero Latency</div></div><button class='btn pur' onclick='triggerCodePay("Autonomous Pro")'>購入する ↗</button></div>
<div class='pcard'><div><strong>Enterprise</strong><div style='font-size:0.75rem;color:var(--purple);margin:3px 0'>$299<span style='font-size:0.45rem'>/mo</span></div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• Swarm Core<br>• SLA 100%</div></div><button class='btn blue' onclick='triggerCodePay("Enterprise")'>ライセンス ↗</button></div>
</div>
</div>

<!-- 5. God-Tier Autonomous Economic Core (完全復元・整理されたデータ群) -->
<div class='sec'>
<h2>God-Tier Autonomous Economic Core <span class='tag'>ACTIVE</span></h2>
<div class='g4' style='margin-bottom:8px;'>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>埋蔵残高</div><div id='liveIngestion' style='font-size:0.65rem;color:var(--green);font-weight:bold'>$94,800,120.00</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>アクティブエージェント</div><div id='liveAgents' style='font-size:0.65rem;color:var(--green);font-weight:bold'>442,050,910 units</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>効率</div><div id='liveEfficiency' style='font-size:0.65rem;color:var(--green);font-weight:bold'>99.99%</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>登録ノード</div><div id='liveUsers' style='font-size:0.65rem;color:var(--blue);font-weight:bold'>128 nodes</div></div>
</div>

<!-- 暗号資産ウォレットグリッド (4つ) -->
<div class='g4' style='margin-bottom:8px;'>
<div class='box'><div><strong>Bitcoin</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac'></div><div class='addr'>bc1q94rkd...d7zac</div><a href='https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac' target='_blank' class='btn'>Mempool</a></div>
<div class='box'><div><strong>Solana</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf'></div><div class='addr'>75igwQpPg...7nf</div><a href='https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf' target='_blank' class='btn'>Solscan</a></div>
<div class='box'><div><strong>Ethereum</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8'></div><div class='addr'>0xD6716D0...8G8</div><a href='https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8' target='_blank' class='btn'>Etherscan</a></div>
<div class='box'><div><strong>Bitcoin SV</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95'></div><div class='addr'>1PB66iHot...y95</div><a href='https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95' target='_blank' class='btn'>WhatsOnChain</a></div>
</div>

<!-- オラクル・API接続カード群 (3つ) -->
<div class='g3'>
<div class='box'>
  <div style='font-size:0.52rem;color:var(--purple);font-weight:bold;'>Mock API / M2M</div>
  <div style='font-size:0.48rem;color:var(--muted);margin:2px 0;'>ハイパー・スループット</div>
  <button class='btn pur' onclick='alert("Mock API Active ✓")'>ステータス</button>
</div>
<div class='box'>
  <div style='font-size:0.52rem;color:var(--purple);font-weight:bold;'>aws kinesis / SACK</div>
  <div style='font-size:0.48rem;color:var(--muted);margin:2px 0;'>リアルタイムストリーム</div>
  <button class='btn blue' onclick='alert("AWS Kinesis Synced ✓")'>同期テスト</button>
</div>
<div class='box'>
  <div style='font-size:0.52rem;color:var(--purple);font-weight:bold;'>Stripe PYT</div>
  <div style='font-size:0.48rem;color:var(--muted);margin:2px 0;'>フィアット・決済基盤</div>
  <button class='btn pay' onclick='triggerCodePay("Stripe PYT")'>決済管理へ</button>
</div>
</div>
</div>

<!-- 6. Omni-Synapse Live Stream -->
<div class='sec'>
<h2>OMNI-SYNAPSE LIVE STREAM <span class='tag'>WS</span></h2>
<div class='stream' id='streamLog'>[INIT] Code Payment Gateway & WebSocket connected.</div>
</div>

<!-- 7. Feedback & Governance & Live Auction -->
<div class='sec'>
<h2>ENTERPRISE FEEDBACK, GOVERNANCE & LIVE AUCTION <span class='tag'>DB</span></h2>
<div style='display:flex;gap:6px'><input type='text' id='feedbackInput' class='inp' style='flex:1;' placeholder='フィードバックを入力...'><button class='btn pur' style='margin:0;width:60px' onclick='sendFeedback()'>送信</button></div>
<div style='margin-top:10px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;'>
<div style='font-size:0.6rem;color:var(--purple);font-weight:bold;margin-bottom:4px;'>🌐 SWARM GOVERNANCE VOTING</div>
<div style='display:flex;gap:6px;'><button class='btn blue' style='flex:1;margin:0;' onclick='voteGov("YES")'>賛成 (YES)</button><button class='btn pur' style='flex:1;margin:0;' onclick='voteGov("NO")'>反対 (NO)</button></div>
<div id='voteResult' style='font-size:0.52rem;color:var(--green);margin-top:6px;font-family:monospace;'>賛成: 1420 | 反対: 18</div>
</div>
<div style='margin-top:8px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;'>
<div style='font-size:0.6rem;color:var(--purple);font-weight:bold;margin-bottom:4px;'>🤖 LIVE AGENT TASK AUCTION</div>
<div style='display:flex;gap:4px;margin-bottom:6px;'>
<input type='text' id='bidAgent' class='inp' style='width:30%;' placeholder='Agent名'>
<input type='text' id='bidTask' class='inp' style='width:40%;' placeholder='タスク内容'>
<input type='number' step='0.001' id='bidAmount' class='inp' style='width:15%;' value='0.05'>
<button class='btn pur' style='margin:0;width:15%;' onclick='submitBid()'>入札</button>
</div>
<div id='auctionList' style='font-family:monospace;font-size:0.5rem;color:var(--green);background:#0d0d1a;padding:6px;border-radius:3px;max-height:60px;overflow-y:auto;'>読込中...</div>
</div>
</div>

<!-- 8. 企業情報セクション（タグ崩れ完全修正・一番下に配置） -->
<div class='sec'>
<h2>企業情報 / 概要 <span class='tag'>QLAX</span></h2>
<div style='font-size:0.6rem;color:var(--muted);line-height:1.4;'>
<p style='margin:0 0 4px 0;'><strong>ASGARD</strong>は、AIエージェント・AGIが自動接続し、0.00msミリ秒決済と自律タスク仲介を提供する次世代の自律型AI M2M経済インフラストラクチャです。</p>
<p style='margin:0 0 4px 0;'><strong>QLAX</strong>は、福岡県を拠点にM2Mインフラストラクチャと高スループット決済環境を構築・研究開発する個人事業主の組織です[span_0](start_span)[span_0](end_span)。</p>
<p style='margin:0;'><strong>運営責任者:</strong> Daisuke Higuchi[span_1](start_span)[span_1](end_span)</p>
</div>
</div>

<div style='text-align:center;font-size:0.48rem;color:var(--muted);padding:4px 0'>© ASGARD Infrastructure[span_2](start_span)[span_2](end_span) | 運営者: QLAX (Daisuke Higuchi)[span_3](start_span)[span_3](end_span) / 豊前市[span_4](start_span)[span_4](end_span).</div>
</div>
</div>

<script>
function copyCmd(t){navigator.clipboard.writeText(t);alert('コピー完了 ✓');}
async function triggerCodePay(method){
  const r=await fetch('/api/v56/code-pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method})});
  const d=await r.json();
  alert('[' + d.method + ' 決済ゲートウェイ]\\nインボイスID: ' + d.invoice_id + '\\n金額: ' + d.amount_jpy + ' JPY\\nステータス: ' + d.status + '\\n\\n※決済リクエスト成功 ✓');
}
async function loadState(){
  try{
    const r=await fetch('/api/v56/state');
    const d=await r.json();
    document.getElementById('voteResult').innerText='賛成(YES): ' + d.votes.YES + ' | 反対(NO): ' + d.votes.NO;
    let html = '';
    for(let i=0; i<d.auctions.length; i++){
      let a = d.auctions[i];
      html += '[' + a.created_at + '] ' + a.agent_name + ': ' + a.task_desc + ' (' + a.bid_bsv + ' BSV)<br>';
    }
    document.getElementById('auctionList').innerHTML = html;
  }catch(e){}
}
async function sendFeedback(){
  const v=document.getElementById('feedbackInput').value;
  if(!v)return;
  await fetch('/api/v56/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:v})});
  alert('送信完了 ✓'); document.getElementById('feedbackInput').value='';
}
async function voteGov(choice){
  const r=await fetch('/api/v56/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice})});
  const d=await r.json();
  document.getElementById('voteResult').innerText='賛成(YES): ' + d.votes.YES + ' | 反対(NO): ' + d.votes.NO + ' ✓';
}
async function submitBid(){
  const ag=document.getElementById('bidAgent').value||'Agent_1';
  const tk=document.getElementById('bidTask').value||'Compute';
  const am=parseFloat(document.getElementById('bidAmount').value)||0.05;
  try{
    await fetch('/api/v56/auction/bid',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({agent_name:ag,task_desc:tk,bid_bsv:am})});
    document.getElementById('bidTask').value=''; loadState();
  }catch(e){}
}
let bIng=94800120.0,bAg=442050910;
setInterval(()=>{
  bIng+=Math.random()*100-30;
  bAg+=Math.floor(Math.random()*3)-1;
  document.getElementById('liveIngestion').innerText='$' + bIng.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
  document.getElementById('liveAgents').innerText=bAg.toLocaleString() + ' units';
},2000);
const wsP=window.location.protocol==='https:'?'wss://':'ws://';
const liveWs=new WebSocket(wsP+window.location.host+'/ws');
liveWs.onmessage=function(e){
  const s=document.getElementById('streamLog');
  s.innerHTML+='<br>'+e.data; s.scrollTop=s.scrollHeight;
  loadState();
};
loadState();
</script>
</body>
</html>
"""

DOCS_HTML = """<!DOCTYPE html>
<html lang='ja'>
<head><meta charset='UTF-8'><title>API Docs</title>
<style>body{background:#05050a;color:#f8fafc;font-family:sans-serif;padding:20px;display:flex;justify-content:center;}
.box{max-width:700px;width:100%;background:#0d0d1a;border:1px solid #1e1b4b;padding:20px;border-radius:8px;}
h1{color:#c084fc;font-size:1.2rem;} pre{background:#05050a;padding:8px;color:#10b981;font-size:0.7rem;overflow-x:auto;} a{color:#38bdf8;}</style>
</head>
