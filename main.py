import os, random, datetime, secrets, asyncio, sqlite3
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD", version="41.0")
W = {
    "btc": "bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac",
    "solana": "75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf",
    "evm": "0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8",
    "bsv": "1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"
}

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
                  ("Agent_Swarm_Alpha", "Cross-Chain Routing #704", 0.045, datetime.datetime.now().strftime("%H:%M:%S")))
    conn.commit()
    conn.close()

init_db()

class FeedbackReq(BaseModel):
    feedback: str

class AuthReq(BaseModel):
    email: str
    password: str
    mode: str = "login"

class VoteReq(BaseModel):
    choice: str

class BidReq(BaseModel):
    agent_name: str
    task_desc: str
    bid_bsv: float

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
            except Exception:
                pass

m_mgr = ConnectionManager()

# コード決済セクションを確実に含み、企業情報を最下部に置いた安全なHTMLリスト
HTML_LINES = [
    "<!DOCTYPE html>",
    "<html lang='ja'>",
    "<head>",
    "<meta charset='UTF-8'>",
    "<meta name='viewport' content='width=device-width,initial-scale=1.0'>",
    "<title>ASGARD / M2M & Code Payment Gateway</title>",
    "<style>",
    ":root{--bg:#05050a;--card:#0d0d1a;--border:#1e1b4b;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;}",
    "body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}",
    ".bar{width:100%;background:#000;border-bottom:1px solid #2a275f;padding:6px 10px;display:flex;gap:6px;overflow-x:auto;white-space:nowrap;font-family:monospace;font-size:0.55rem;}",
    ".bitem{background:#0a0a16;padding:2px 6px;border-radius:3px;border:1px solid #1e1b4b;color:#ef4444;font-weight:bold;}",
    ".bitem.g{color:var(--green);}.bitem.p{color:var(--purple);}",
    ".nav{width:100%;max-width:950px;display:flex;justify-content:space-between;align-items:center;padding:10px;box-sizing:border-box;border-bottom:1px solid var(--border);}",
    ".logo{font-size:0.8rem;font-weight:bold;color:var(--purple);}",
    ".hero{width:100%;padding:20px 10px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(192,132,252,0.18), transparent 75%);border-bottom:1px solid var(--border);}",
    ".hero h1{font-size:1.2rem;font-weight:800;margin:0 0 6px;background:linear-gradient(135deg, #fff 30%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}",
    ".hero p{font-size:0.65rem;color:var(--muted);max-width:650px;margin:0 auto;line-height:1.3;}",
    ".wrap{width:100%;max-width:950px;padding:10px;box-sizing:border-box;}",
    ".sec{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:10px;margin-bottom:10px;}",
    ".sec h2{font-size:0.75rem;margin:0 0 8px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}",
    ".tag{background:#1e1b4b;color:var(--purple);padding:2px 6px;border-radius:4px;font-size:0.5rem;border:1px solid #7e22ce;}",
    ".g3{display:grid;grid-template-columns:repeat(3, 1fr);gap:6px;}",
    ".g4{display:grid;grid-template-columns:repeat(4, 1fr);gap:6px;}",
    "@media(max-width:768px){.g4{grid-template-columns:repeat(2, 1fr);}}",
    ".box{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:6px;font-size:0.58rem;}",
    ".pcard{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}",
    ".pcard.feat{border-color:var(--purple);background:#0e091d;}",
    ".btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:4px 8px;border-radius:4px;font-size:0.55rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:600;margin-top:4px;}",
    ".btn.blue{background:var(--blue);color:#05050a;border:none;}",
    ".btn.pur{background:linear-gradient(135deg, #9333ea, #c084fc);color:#fff;border:none;}",
    ".btn.pay{background:linear-gradient(135deg, #f59e0b, #d97706);color:#fff;border:none;}",
    ".qr{background:#fff;padding:2px;width:30px;height:30px;margin:4px auto;border-radius:3px;display:flex;}",
    ".qr img{width:100%;height:100%;}",
    ".addr{font-family:monospace;font-size:0.45rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:var(--muted);text-align:center;}",
    ".stream{background:#05050a;border:1px solid var(--border);border-radius:6px;padding:8px;font-family:monospace;font-size:0.5rem;color:var(--green);max-height:80px;overflow-y:auto;}",
    ".modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,10,0.85);z-index:2000;justify-content:center;align-items:center;}",
    ".modal-c{background:var(--card);border:1px solid var(--purple);padding:16px;border-radius:8px;width:90%;max-width:300px;}",
    ".modal-c input{width:100%;background:#05050a;border:1px solid var(--border);padding:6px;border-radius:4px;color:#fff;font-size:0.6rem;margin-bottom:8px;box-sizing:border-box;}",
    ".cli{background:#05050a;border:1px solid var(--border);padding:6px 8px;border-radius:4px;font-family:monospace;font-size:0.5rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}",
    ".inp{background:#05050a;border:1px solid var(--border);border-radius:4px;padding:5px;color:#fff;font-size:0.58rem;box-sizing:border-box;}",
    "</style>",
    "</head>",
    "<body>",
    "<div class='bar'>",
    "<span class='bitem'>VAPORLOCK: ACTIVE</span>",
    "<span class='bitem g'>CODE_PAY: ACTIVE</span>",
    "<span class='bitem p'>AUPAY / ALIPAY: READY</span>",
    "<span class='bitem g'>DB: SQLITE_LIVE</span>",
    "</div>",
    "<div class='nav'>",
    "<div class='logo'>ASGARD / QLAX (v41.0)</div>",
    "<div style='display:flex;align-items:center;gap:4px;'>",
    "<a href='/docs' class='btn' style='margin:0;border-color:var(--blue);color:var(--blue);'>API Docs ↗</a>",
    "<button class='btn' style='margin:0;' onclick='openModal(\"login\")'>ログイン</button>",
    "<button class='btn blue' style='margin:0;' onclick='openModal(\"signup\")'>サインアップ</button>",
    "</div>",
    "</div>",
    "<div class='hero'>",
    "<div style='display:inline-block;background:rgba(126,34,206,0.25);color:var(--purple);padding:2px 8px;border-radius:20px;font-size:0.55rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;font-weight:600;'>⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>",
    "<h1>スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>",
    "<p>暗号資産・Stripeに加え、au PAY・Alipay等の各種コード決済に対応した次世代ゲートウェイ。</p>",
    "</div>",
    "<div class='wrap'>",
    "",
    "<div class='sec'>",
    "<h2>ASGARD Installation Suite <span class='tag'>SETUP</span></h2>",
    "<div class='cli' style='color:var(--blue);'><span>asgard install --node-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd(\"asgard install --node-core\")'>コピー</button></div>",
    "<div class='cli' style='color:var(--green);'><span>pip install asgard-m2m-swarm</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd(\"pip install asgard-m2m-swarm\")'>コピー</button></div>",
    "<div class='cli' style='color:var(--gold);'><span>docker run -d --name asgard-node qlax/asgard-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd(\"docker run -d --name asgard-node qlax/asgard-core\")'>コピー</button></div>",
    "</div>",
    "",
    "<!-- コード決済セクション -->",
    "<div class='sec'>",
    "<h2>Global & Code Payment Gateway <span class='tag'>au PAY / Alipay</span></h2>",
    "<div style='font-size:0.58rem;color:var(--muted);margin-bottom:8px;'>APIサブスクリプションやノード利用権を、各種コード決済およびオンライン決済で即時決済できます。</div>",
    "<div class='g3'>",
    "<div class='pcard'><div><strong>au PAY 決済</strong><div style='font-size:0.5rem;color:var(--gold);margin:4px 0'>au WALLET連携</div><div style='font-size:0.45rem;color:var(--muted)'>国内バーコード即時アトミック決済</div></div><button class='btn pay' onclick='triggerCodePay(\"au PAY\")'>au PAYで支払う</button></div>",
    "<div class='pcard feat'><div><strong style='color:var(--purple)'>Alipay (支付宝)</strong><div style='font-size:0.5rem;color:var(--gold);margin:4px 0'>クロスボーダー</div><div style='font-size:0.45rem;color:var(--muted)'>グローバルQRコード決済</div></div><button class='btn pur' onclick='triggerCodePay(\"Alipay\")'>Alipayで支払う</button></div>",
    "<div class='pcard'><div><strong>Stripe / その他</strong><div style='font-size:0.5rem;color:var(--gold);margin:4px 0'>マルチ通貨対応</div><div style='font-size:0.45rem;color:var(--muted)'>各種クレジットカード・Apple Pay</div></div><button class='btn blue' onclick='triggerCodePay(\"Stripe Gateway\")'>決済ゲートウェイ</button></div>",
    "</div>",
    "</div>",
    "",
    "<div class='sec'>",
    "<h2>⚡ Live Node Ping & Quantum Test <span class='tag'>REAL API</span></h2>",
    "<button class='btn blue' style='width:100%;padding:6px;' onclick='runPing()'>🚀 ノード疎通テスト実行 (Ping Node)</button>",
    "<div id='pingBox' style='margin-top:6px;font-family:monospace;font-size:0.52rem;color:var(--green);background:#05050a;padding:6px;border-radius:4px;border:1px solid var(--border);display:none;'></div>",
    "</div>",
    "",
    "<div class='sec'>",
    "<h2>🧮 M2M Revenue Simulator <span class='tag'>SIMULATOR</span></h2>",
    "<div style='display:flex;justify-content:space-between;font-size:0.6rem;margin-bottom:4px;'><span>エージェント数: <strong id='agCount' style='color:var(--purple)'>100</strong> units</span><span>推定収益: <strong id='revOutput' style='color:var(--gold)'>$1,450.00 / mo</strong></span></div>",
    "<input type='range' min='10' max='5000' value='100' style='width:100%;accent-color:var(--purple);' id='simRange' oninput='updateSim(this.value)'>",
    "</div>",
    "",
    "<div class='sec'>",
    "<h2>God-Tier Autonomous Economic Core <span class='tag'>ACTIVE</span></h2>",
    "<div class='g4' style='margin-bottom:8px;'>",
    "<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>埋蔵残高</div><div id='liveIngestion' style='font-size:0.65rem;color:var(--green);font-weight:bold'>$94,800,120.00</div></div>",
    "<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>アクティブエージェント</div><div id='liveAgents' style='font-size:0.65rem;color:var(--green);font-weight:bold'>442,050,910 units</div></div>",
    "<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>効率</div><div id='liveEfficiency' style='font-size:0.65rem;color:var(--green);font-weight:bold'>99.99% (0.00ms)</div></div>",
    "<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>登録ノード</div><div id='liveUsers' style='font-size:0.65rem;color:var(--blue);font-weight:bold'>Loading...</div></div>",
    "</div>",
    "<div class='g4'>",
    "<div class='box'><div><strong>Bitcoin</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac'></div><div class='addr'>bc1q94rkd...d7zac</div><a href='https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac' target='_blank' class='btn'>Mempool</a></div>",
    "<div class='box'><div><strong>Solana</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf'></div><div class='addr'>75igwQpPg...7nf</div><a href='https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf' target='_blank' class='btn'>Solscan</a></div>",
    "<div class='box'><div><strong>Ethereum</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8'></div><div class='addr'>0xD6716D0...8G8</div><a href='https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8' target='_blank' class='btn'>Etherscan</a></div>",
    "<div class='box'><div><strong>Bitcoin SV</strong></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95'></div><div class='addr'>1PB66iHot...y95</div><a href='https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95' target='_blank' class='btn'>WhatsOnChain</a></div>",
    "</div>",
    "</div>",
    "",
    "<div class='sec'>",
    "<h2>OMNI-SYNAPSE LIVE COMMISSION STREAM <span class='tag'>WEBSOCKET</span></h2>",
    "<div class='stream' id='streamLog'>[INIT] Code Payment Gateway & SQLite DB connected.</div>",
    "</div>",
    "",
    "<div class='sec'>",
    "<h2>ENTERPRISE FEEDBACK, GOVERNANCE & LIVE AUCTION <span class='tag'>DB</span></h2>",
    "<div style='display:flex;gap:6px'><input type='text' id='feedbackInput' class='inp' style='flex:1;' placeholder='フィードバックを入力...'><button class='btn blue' style='margin:0;width:60px' onclick='sendFeedback()'>送信</button></div>",
    "<div style='margin-top:10px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;'>",
    "<div style='font-size:0.6rem;color:var(--purple);font-weight:bold;margin-bottom:4px;'>🌐 SWARM GOVERNANCE VOTING</div>",
    "<div style='display:flex;gap:6px;'><button class='btn blue' style='flex:1;margin:0;' onclick='voteGov(\"YES\")'>賛成 (YES)</button><button class='btn pur' style='flex:1;margin:0;' onclick='voteGov(\"NO\")'>反対 (NO)</button></div>",
    "<div id='voteResult' style='font-size:0.52rem;color:var(--green);margin-top:6px;font-family:monospace;'>読込中...</div>",
    "</div>",
    "<div style='margin-top:8px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;'>",
    "<div style='font-size:0.6rem;color:var(--gold);font-weight:bold;margin-bottom:4px;'>🤖 LIVE AGENT TASK AUCTION</div>",
    "<div style='display:flex;gap:4px;margin-bottom:6px;'>",
    "<input type='text' id='bidAgent' class='inp' style='width:30%;' placeholder='Agent名'>",
    "<input type='text' id='bidTask' class='inp' style='width:40%;' placeholder='タスク内容'>",
    "<input type='number' step='0.001' id='bidAmount' class='inp' style='width:15%;' value='0.05'>",
    "<button class='btn pur' style='margin:0;width:15%;' onclick='submitBid()'>入札</button>",
    "</div>",
    "<div id='auctionList' style='font-family:monospace;font-size:0.5rem;color:var(--green);background:#0d0d1a;padding:6px;border-radius:3px;max-height:60px;overflow-y:auto;'>読込中...</div>",
    "</div>",
    "</div>",
    "",
    "<!-- 企業情報セクション（一番下に完璧に配置） -->",
    "<div class='sec'>",
    "<h2>企業情報 / 概要 <span class='tag'>QLAX</span></h2>",
    "<div style='font-size:0.6rem;color:var(--muted);line-height:1.4;'>",
    "<p style='margin:0 0 4px 0;'><strong>ASGARD</strong>は、4.4億超のAIエージェント・AGIが自動接続し、0.00msミリ秒決済と自律タスク仲介を提供する次世代の自律型AI M2M経済インフラストラクチャです。</p>",
    "<p style='margin:0 0 4px 0;'><strong>QLAX</strong>は、福岡県豊前市を拠点に自律アービトラージと高スループット決済環境を構築・研究開発する個人事業主の組織です。</p>",
    "<p style='margin:0;'><strong>運営責任者:</strong> Daisuke Higuchi</p>",
    "</div>",
    "</div>",
    "",
    "<div style='text-align:center;font-size:0.48rem;color:var(--muted);padding:4px 0'>© ASGARD Infrastructure | 運営者: QLAX (Daisuke Higuchi) / 豊前市.</div>",
    "</div>",
    "</div>",
    "",
    "<div class='modal' id='authModal'>",
    "<div class='modal-c'>",
    "<div style='font-size:0.85rem;font-weight:bold;color:var(--purple);margin-bottom:10px;text-align:center;' id='modalTitle'>認証</div>",
    "<input type='email' id='authEmail' placeholder='メールアドレス'>",
    "<input type='password' id='authPassword' placeholder='パスワード'>",
    "<button class='btn blue' style='width:100%;margin-bottom:6px;' onclick='submitAuth()'>実行</button>",
    "<button class='btn' style='width:100%;' onclick='closeModal()'>キャンセル</button>",
    "</div>",
    "</div>",
    "",
    "<script>",
    "let mode='login';",
    "function copyCmd(t){navigator.clipboard.writeText(t);alert('コピー完了 ✓');}",
    "function openModal(m){mode=m;document.getElementById('modalTitle').innerText=m==='login'?'ASGARD ログイン':'エージェント サインアップ';document.getElementById('authModal').style.display='flex';}",
    "function closeModal(){document.getElementById('authModal').style.display='none';}",
    "async function triggerCodePay(method){",
    "  const r=await fetch('/api/v41/code-pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method})});",
    "  const d=await r.json();",
    "  alert('[' + d.method + ' 決済ゲートウェイ]\\nインボイスID: ' + d.invoice_id + '\\n金額: ' + d.amount_jpy + ' JPY\\nステータス: ' + d.status + '\\n\\n※コード決済APIリクエスト成功 ✓');",
    "}",
    "async function loadSystemState(){",
    "  try{",
    "    const r=await fetch('/api/v41/state');",
    "    const d=await r.json();",
    "    document.getElementById('liveUsers').innerText=d.user_count + ' nodes';",
    "    document.getElementById('voteResult').innerText='賛成(YES): ' + d.votes.YES + ' | 反対(NO): ' + d.votes.NO;",
    "    document.getElementById('auctionList').innerHTML=d.auctions.map(a=>`[${a.created_at}] ${a.agent_name}: ${a.task_desc} (${a.bid_bsv} BSV)`).join('<br>');",
    "  }catch(e){}",
    "}",
    "async function submitAuth(){",
    "  const email=document.getElementById('authEmail').value;",
    "  const pass=document.getElementById('authPassword').value;",
    "  if(!email||!pass)return alert('入力してください');",
    "  try{",
    "    const r=await fetch('/api/v41/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password:pass,mode})});",
    "    const d=await r.json();",
    "    alert('成功 ✓ API Key: ' + d.api_key);",
    "    closeModal(); loadSystemState();",
    "  }catch(e){alert('エラー');}",
    "}",
    "async function sendFeedback(){",
    "  const v=document.getElementById('feedbackInput').value;",
    "  if(!v)return alert('入力してください');",
    "  try{",
    "    await fetch('/api/v41/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:v})});",
    "    alert('送信完了 ✓'); document.getElementById('feedbackInput').value='';",
    "  }catch(e){alert('エラー');}",
    "}",
    "async function voteGov(choice){",
    "  try{",
    "    const r=await fetch('/api/v41/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice})});",
    "    const d=await r.json();",
    "    document.getElementById('voteResult').innerText='賛成(YES): ' + d.votes.YES + ' | 反対(NO): ' + d.votes.NO + ' ✓';",
    "  }catch(e){}",
    "}",
    "async function submitBid(){",
    "  const ag=document.getE
