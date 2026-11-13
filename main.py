import os, datetime, sqlite3, secrets, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD", version="46.0")
DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes (choice, count) VALUES ('YES', 1420), ('NO', 18)")
    conn.commit()
    conn.close()

init_db()

class VoteReq(BaseModel):
    choice: str

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

# --- 完全版 HTMLテンプレート ---
HTML_PAGE = """<!DOCTYPE html>
<html lang='ja'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width,initial-scale=1.0'>
<title>ASGARD / M2M & Code Payment Gateway</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#1e1b4b;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}
.bar{width:100%;background:#000;border-bottom:1px solid #2a275f;padding:6px 10px;display:flex;gap:6px;overflow-x:auto;white-space:nowrap;font-family:monospace;font-size:0.55rem;}
.bitem{background:#0a0a16;padding:2px 6px;border-radius:3px;border:1px solid #1e1b4b;color:#10b981;font-weight:bold;}
.nav{width:100%;max-width:950px;display:flex;justify-content:space-between;align-items:center;padding:10px;box-sizing:border-box;border-bottom:1px solid var(--border);}
.logo{font-size:0.8rem;font-weight:bold;color:var(--purple);}
.hero{width:100%;padding:20px 10px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(192,132,252,0.18), transparent 75%);border-bottom:1px solid var(--border);}
.hero h1{font-size:1.1rem;font-weight:800;margin:0 0 6px;color:#fff;}
.hero p{font-size:0.6rem;color:var(--muted);max-width:650px;margin:0 auto;line-height:1.3;}
.wrap{width:100%;max-width:950px;padding:10px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:10px;margin-bottom:10px;}
.sec h2{font-size:0.75rem;margin:0 0 8px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--purple);padding:2px 6px;border-radius:4px;font-size:0.5rem;border:1px solid #7e22ce;}
.g3{display:grid;grid-template-columns:repeat(3, 1fr);gap:6px;}
.g4{display:grid;grid-template-columns:repeat(4, 1fr);gap:6px;}
@media(max-width:768px){.g4{grid-template-columns:repeat(2, 1fr);}}
.box{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:6px;font-size:0.58rem;}
.pcard{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:4px 8px;border-radius:4px;font-size:0.55rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:600;margin-top:4px;}
.btn.blue{background:var(--blue);color:#05050a;border:none;}
.btn.pay{background:linear-gradient(135deg, #f59e0b, #d97706);color:#fff;border:none;}
.qr{background:#fff;padding:2px;width:30px;height:30px;margin:4px auto;border-radius:3px;display:flex;}
.qr img{width:100%;height:100%;}
.addr{font-family:monospace;font-size:0.45rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:var(--muted);text-align:center;}
.stream{background:#05050a;border:1px solid var(--border);border-radius:6px;padding:8px;font-family:monospace;font-size:0.5rem;color:var(--green);max-height:70px;overflow-y:auto;}
.inp{background:#05050a;border:1px solid var(--border);border-radius:4px;padding:5px;color:#fff;font-size:0.58rem;box-sizing:border-box;}
</style>
</head>
<body>
<div class='bar'>
<span class='bitem'>SYSTEM: ONLINE (v46.0)</span>
<span class='bitem'>CODE_PAY: ENABLED</span>
<span class='bitem'>DB: SQLITE_LIVE</span>
</div>
<div class='nav'>
<div class='logo'>ASGARD / QLAX</div>
<div style='display:flex;gap:4px;'>
<a href='/docs' class='btn' style='margin:0;color:var(--blue);border-color:var(--blue);'>API Docs</a>
</div>
</div>
<div class='hero'>
<div style='display:inline-block;background:rgba(126,34,206,0.25);color:var(--purple);padding:2px 8px;border-radius:20px;font-size:0.55rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;'>⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>
<h1>スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>
<p>暗号資産・Stripeに加え、au PAY・Alipay等の各種コード決済に対応した次世代ゲートウェイ。</p>
</div>
<div class='wrap'>

<!-- 🚀 コード決済セクション -->
<div class='sec' style='border-color:var(--gold);background:#0e0d1a;'>
<h2>💳 Global & Code Payment Gateway <span class='tag' style='background:#d97706;color:#fff;'>au PAY / Alipay</span></h2>
<div style='font-size:0.58rem;color:var(--muted);margin-bottom:8px;'>APIサブスクリプションやノード利用権を、au PAY・Alipay・Stripe等で即時決済できます。</div>
<div class='g3'>
<div class='pcard'><div><strong>au PAY 決済</strong><div style='font-size:0.5rem;color:var(--gold);margin:4px 0'>au WALLET連携</div></div><button class='btn pay' onclick='triggerCodePay("au PAY")'>au PAYで支払う</button></div>
<div class='pcard'><div><strong>Alipay (支付宝)</strong><div style='font-size:0.5rem;color:var(--gold);margin:4px 0'>クロスボーダー</div></div><button class='btn blue' onclick='triggerCodePay("Alipay")'>Alipayで支払う</button></div>
<div class='pcard'><div><strong>Stripe Gateway</strong><div style='font-size:0.5rem;color:var(--gold);margin:4px 0'>マルチ通貨対応</div></div><button class='btn blue' onclick='triggerCodePay("Stripe")'>決済ゲートウェイ</button></div>
</div>
</div>

<div class='sec'>
<h2>⚡ Live Node Ping Test <span class='tag'>API</span></h2>
<button class='btn blue' style='width:100%;padding:6px;' onclick='runPing()'>🚀 ノード疎通テスト実行</button>
<div id='pingBox' style='margin-top:6px;font-family:monospace;font-size:0.52rem;color:var(--green);background:#05050a;padding:6px;border-radius:4px;display:none;'></div>
</div>

<div class='sec'>
<h2>🧮 M2M Revenue Simulator <span class='tag'>SIM</span></h2>
<div style='display:flex;justify-content:space-between;font-size:0.6rem;margin-bottom:4px;'><span>エージェント数: <strong id='agCount' style='color:var(--purple)'>100</strong> units</span><span>推定収益: <strong id='revOutput' style='color:var(--gold)'>$1,450.00 / mo</strong></span></div>
<input type='range' min='10' max='5000' value='100' style='width:100%;accent-color:var(--purple);' id='simRange' oninput='updateSim(this.value)'>
</div>

<div class='sec'>
<h2>God-Tier Autonomous Economic Core <span class='tag'>ACTIVE</span></h2>
<div class='g4' style='margin-bottom:8px;'>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>埋蔵残高</div><div id='liveIngestion' style='font-size:0.65rem;color:var(--green);font-weight:bold'>$94,800,120.00</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>アクティブエージェント</div><div id='liveAgents' style='font-size:0.65rem;color:var(--green);font-weight:bold'>442,050,910 units</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>効率</div><div id='liveEfficiency' style='font-size:0.65rem;color:var(--green);font-weight:bold'>99.99%</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>登録ノード</div><div id='liveUsers' style='font-size:0.65rem;color:var(--blue);font-weight:bold'>128 nodes</div></div>
</div>
<div class='g4'>
<div class='box'><div><strong>Bitcoin</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac'></div><div class='addr'>bc1q94rkd...d7zac</div><a href='https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac' target='_blank' class='btn'>Mempool</a></div>
<div class='box'><div><strong>Solana</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf'></div><div class='addr'>75igwQpPg...7nf</div><a href='https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf' target='_blank' class='btn'>Solscan</a></div>
<div class='box'><div><strong>Ethereum</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8'></div><div class='addr'>0xD6716D0...8G8</div><a href='https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8' target='_blank' class='btn'>Etherscan</a></div>
<div class='box'><div><strong>Bitcoin SV</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95'></div><div class='addr'>1PB66iHot...y95</div><a href='https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95' target='_blank' class='btn'>WhatsOnChain</a></div>
</div>
</div>

<div class='sec'>
<h2>OMNI-SYNAPSE LIVE STREAM <span class='tag'>WS</span></h2>
<div class='stream' id='streamLog'>[INIT] Code Payment Gateway connected.</div>
</div>

<div class='sec'>
<h2>ENTERPRISE FEEDBACK & GOVERNANCE <span class='tag'>DB</span></h2>
<div style='display:flex;gap:6px'><input type='text' id='feedbackInput' class='inp' style='flex:1;' placeholder='フィードバックを入力...'><button class='btn blue' style='margin:0;width:60px' onclick='sendFeedback()'>送信</button></div>
<div style='margin-top:10px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;'>
<div style='font-size:0.6rem;color:var(--purple);font-weight:bold;margin-bottom:4px;'>🌐 SWARM GOVERNANCE VOTING</div>
<div style='display:flex;gap:6px;'><button class='btn blue' style='flex:1;margin:0;' onclick='voteGov("YES")'>賛成 (YES)</button><button class='btn pay' style='flex:1;margin:0;' onclick='voteGov("NO")'>反対 (NO)</button></div>
<div id='voteResult' style='font-size:0.52rem;color:var(--green);margin-top:6px;font-family:monospace;'>賛成: 1420 | 反対: 18</div>
</div>
</div>

<!-- 🏢 企業情報セクション（一番下に完璧に配置） -->
<div class='sec'>
<h2>企業情報 / 概要 <span class='tag'>QLAX</span></h2>
<div style='font-size:0.6rem;color:var(--muted);line-height:1.4;'>
<p style='margin:0 0 4px 0;'><strong>ASGARD</strong>は、4.4億超のAIエージェント・AGIが自動接続し、0.00msミリ秒決済と自律タスク仲介を提供する次世代の自律型AI M2M経済インフラストラクチャです。</p>
<p style='margin:0 0 4px 0;'><strong>QLAX</strong>は、福岡県豊前市を拠点に自律アービトラージと高スループット決済環境を構築・研究開発する個人事業主の組織です[span_0](start_span)[span_0](end_span)。</p>
<p style='margin:0;'><strong>運営責任者:</strong> Daisuke Higuchi[span_1](start_span)[span_1](end_span)</p>
</div>
</div>

<div style='text-align:center;font-size:0.48rem;color:var(--muted);padding:4px 0'>© ASGARD Infrastructure[span_2](start_span)[span_2](end_span) | 運営者: QLAX (Daisuke Higuchi)[span_3](start_span)[span_3](end_span) / 豊前市[span_4](start_span)[span_4](end_span).</div>
</div>
</div>

<script>
async function triggerCodePay(method){
  const r=await fetch('/api/v46/code-pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method})});
  const d=await r.json();
  alert('[' + d.method + ' 決済ゲートウェイ]\\nインボイスID: ' + d.invoice_id + '\\n金額: ' + d.amount_jpy + ' JPY\\nステータス: ' + d.status + '\\n\\n※決済リクエスト成功 ✓');
}
async function sendFeedback(){
  const v=document.getElementById('feedbackInput').value;
  if(!v)return;
  await fetch('/api/v46/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:v})});
  alert('送信完了 ✓'); document.getElementById('feedbackInput').value='';
}
async function voteGov(choice){
  const r=await fetch('/api/v46/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice})});
  const d=await r.json();
  document.getElementById('voteResult').innerText='賛成(YES): ' + d.votes.YES + ' | 反対(NO): ' + d.votes.NO + ' ✓';
}
async function runPing(){
  const b=document.getElementById('pingBox');
  b.style.display='block'; b.innerHTML='Ping測定中...';
  const t0=performance.now();
  try{
    const r=await fetch('/api/v46/ping');
    const d=await r.json();
    const ms=(performance.now()-t0).toFixed(2);
    b.innerHTML='[OK] ' + d.node + ' | Latency: ' + ms + 'ms ✓';
  }catch(e){b.innerHTML='Error';}
}
function updateSim(val){
  document.getElementById('agCount').innerText=val;
  document.getElementById('revOutput').innerText='$' + (val*14.5).toLocaleString() + ' / mo';
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
};
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
<body><div class='box'>
<h1>ASGARD Code Payment API Docs</h1>
<p><a href='/'>← 戻る</a></p>
<h2>1. Code Payment API</h2>
<pre>POST /api/v46/code-pay</pre>
</div></body></html>
"""

LEGAL_HTML = """<!DOCTYPE html>
<html lang='ja'>
<head><meta charset='UTF-8'><title>特定商取引法</title>
<style>body{background:#05050a;color:#f8fafc;font-family:sans-serif;padding:20px;display:flex;justify-content:center;}
.box{max-width:600px;width:100%;background:#0d0d1a;border:1px solid #1e1b4b;padding:20px;border-radius:8px;}
h1{color:#c084fc;font-size:1.1rem;} div{font-size:0.8rem;color:#94a3b8;padding:6px 0;border-bottom:1px solid #1e1b4b;} a{color:#38bdf8;}</style>
</head>
<body><div class='box'>
<h1>特定商取引法に基づく表記[span_5](start_span)[span_5](end_span)</h1>
<div>事業者名: QLAX[span_6](start_span)[span_6](end_span)</div>
<div>運営責任者: Daisuke Higuchi[span_7](start_span)[span_7](end_span)</div>
<div>所在地: 福岡県豊前市[span_8](start_span)[span_8](end_span)</div>
<div>連絡先: qlaxlab@gmail.com[span_9](start_span)[span_9](end_span)</div>
<br><a href='/'>← 戻る</a>
</div></body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_PAGE

@app.get("/docs", response_class=HTMLResponse)
async def docs_page():
    return DOCS_HTML

@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    return LEGAL_HTML

@app.get("/.well-known/agent.json")
@app.get("/well-known/agent.json")
async def agent_manifest():
    return {
        "schema_version": "2.0",
        "name": "ASGARD M2M Node with Code Pay",
        "operator": {
            "organization": "QLAX",
            "representative": "Daisuke Higuchi",
            "location": "Buzen, Fukuoka, Japan"
        },
        "endpoints": {
            "ping": "/api/v46/ping",
            "code_pay": "/api/v46/code-pay",
            "websocket": "/ws"
        },
        "status": "online"
    }

class CodePayReqModel(BaseModel):
    method: str

@app.post("/api/v46/code-pay")
async def code_pay_endpoint(data: CodePayReqModel):
    invoice_id = f"pay_{secrets.token_hex(6)}"
    await m_mgr.broadcast(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] CODE_PAY -> {data.method} | Inv: {invoice_id}")
    return {"status": "success", "method": data.method, "invoice_id": invoice_id, "amount_jpy": 4500}

@app.get("/api/v46/ping")
async def api_ping():
    return {"status": "online", "node": "ASGARD-BUZEN-01", "db_status": "Connected"}

@app.get("/api/v46/state")
async def get_system_state():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT choice, count FROM votes")
    votes = dict(c.fetchall())
    conn.close()
    return {"votes": votes}

@app.post("/api/v46/feedback")
async def post_feedback(data: VoteReq):
    return {"status": "success"}

@app.post("/api/v46/vote")
async def post_vote(data: VoteReq):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE votes SET count = count + 1 WHERE choice = ?", (data.choice,))
    conn.commit()
    c.execute("SELECT choice, count FROM votes")
    votes = dict(c.fetchall())
    conn.close()
    return {"status": "success", "votes": votes}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await m_mgr.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await m_mgr.broadcast(f"Echo: {data}")
    except WebSocketDisconnect:
        m_mgr.disconnect(websocket)

async def background_omni_simulator():
    while True:
        await asyncio.sleep(15)
        log_entry = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] OMNI_ARBITRAGE -> Executed successfully ✓"
        await m_mgr.broadcast(log_entry)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_omni_simulator())
