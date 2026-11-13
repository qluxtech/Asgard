import os, random, datetime, secrets, asyncio, sqlite3
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD", version="40.0")
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
    c.execute("CREATE TABLE IF NOT EXISTS qr_invoices (id TEXT PRIMARY KEY, provider TEXT, amount_jpy INTEGER, created_at TEXT)")
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

class QrPayReq(BaseModel):
    provider: str
    amount_jpy: int = 1000

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

HTML_LINES = [
    "<!DOCTYPE html>",
    "<html lang='ja'>",
    "<head>",
    "<meta charset='UTF-8'>",
    "<meta name='viewport' content='width=device-width,initial-scale=1.0'>",
    "<title>ASGARD / Omni-Payment & M2M Infrastructure</title>",
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
    ".qr{background:#fff;padding:2px;width:30px;height:30px;margin:4px auto;border-radius:3px;display:flex;}",
    ".qr img{width:100%;height:100%;}",
    ".addr{font-family:monospace;font-size:0.45rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:var(--muted);text-align:center;}",
    ".stream{background:#05050a;border:1px solid var(--border);border-radius:6px;padding:8px;font-family:monospace;font-size:0.5rem;color:var(--green);max-height:80px;overflow-y:auto;}",
    ".modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,10,0.88);z-index:2000;justify-content:center;align-items:center;}",
    ".modal-c{background:var(--card);border:1px solid var(--purple);padding:16px;border-radius:8px;width:90%;max-width:320px;text-align:center;}",
    ".modal-c input{width:100%;background:#05050a;border:1px solid var(--border);padding:6px;border-radius:4px;color:#fff;font-size:0.6rem;margin-bottom:8px;box-sizing:border-box;}",
    ".cli{background:#05050a;border:1px solid var(--border);padding:6px 8px;border-radius:4px;font-family:monospace;font-size:0.5rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}",
    ".inp{background:#05050a;border:1px solid var(--border);border-radius:4px;padding:5px;color:#fff;font-size:0.58rem;box-sizing:border-box;}",
    ".qbadge{display:inline-block;padding:1px 4px;border-radius:3px;font-size:0.45rem;font-weight:bold;float:right;}",
    "</style>",
    "</head>",
    "<body>",
    "<div class='bar'>",
    "<span class='bitem'>VAPORLOCK: ACTIVE</span>",
    "<span class='bitem g'>AUTOPILOT: 100%</span>",
    "<span class='bitem p'>OMNI_QR_GATEWAY: 16_SYSTEMS</span>",
    "<span class='bitem g'>DB: SQLITE_LIVE</span>",
    "<span class='bitem p'>AGENT_JSON: v2.0</span>",
    "</div>",
    "<div class='nav'>",
    "<div class='logo'>ASGARD / QLAX (v40.0)</div>",
    "<div style='display:flex;align-items:center;gap:4px;'>",
    "<a href='/docs' class='btn' style='margin:0;border-color:var(--blue);color:var(--blue);'>API Docs ↗</a>",
    "<button class='btn' style='margin:0;' onclick='openModal(\"login\")'>ログイン</button>",
    "<button class='btn blue' style='margin:0;' onclick='openModal(\"signup\")'>サインアップ</button>",
    "</div>",
    "</div>",
    "<div class='hero'>",
    "<div style='display:inline-block;background:rgba(126,34,206,0.25);color:var(--purple);padding:2px 8px;border-radius:20px;font-size:0.55rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;font-weight:600;'>⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div>",
    "<h1>スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1>",
    "<p>4.4億超のAIエージェント・AGIが自動接続。0.00msミリ秒決済と全主要コード決済・暗号資産ゲートウェイを統合。</p>",
    "</div>",
    "<div class='wrap'>",
    "",
    "<div class='sec'>",
    "<h2>ASGARD Installation Suite <span class='tag'>SETUP</span></h2>",
    "<div class='cli' style='color:var(--blue);'><span>asgard install --node-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd(\"asgard install --node-core\")'>コピー</button></div>",
    "<div class='cli' style='color:var(--green);'><span>pip install asgard-m2m-swarm</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd(\"pip install asgard-m2m-swarm\")'>コピー</button></div>",
    "<div class='cli' style='color:var(--gold);'><span>docker run -d --name asgard-node qlax/asgard-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd(\"docker run -d --name asgard-node qlax/asgard-core\")'>コピー</button></div>",
    "<div class='cli' style='color:var(--purple);margin-bottom:0;'><span>curl -s https://qlax.tech/.well-known/agent.json</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='copyCmd(\"curl -s https://qlax.tech/.well-known/agent.json\")'>コピー</button></div>",
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
    "<h2>Enterprise Node Tier & Subscriptions <span class='tag'>LIVE</span></h2>",
    "<div class='g3'>",
    "<div class='pcard'><div><strong>Free Tier</strong><div style='font-size:0.85rem;color:var(--gold);margin:3px 0'>FREE</div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• 1,000 Req/mo</div></div><button class='btn' onclick='openModal(\"signup\")'>無料発行</button></div>",
    "<div class='pcard feat'><div><strong style='color:var(--purple)'>Autonomous Pro</strong><div style='font-size:0.85rem;color:var(--gold);margin:3px 0'>$29<span style='font-size:0.45rem'>/mo</span></div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• Unlimited Req</div></div><button class='btn pur' onclick='openModal(\"signup\")'>購入する ↗</button></div>",
    "<div class='pcard'><div><strong>Enterprise</strong><div style='font-size:0.85rem;color:var(--gold);margin:3px 0'>$299<span style='font-size:0.45rem'>/mo</span></div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• Swarm Core</div></div><button class='btn blue' onclick='openModal(\"signup\")'>ライセンス ↗</button></div>",
    "</div>",
    "</div>",
    "",
    "<!-- 全コード決済・QR決済統合ゲートウェイ（限界拡張版 16ブランド対応） -->",
    "<div class='sec'>",
    "<h2>📱 Omni-QR & Universal Code Payment Gateway <span class='tag'>ALL CODE PAY</span></h2>",
    "<div style='display:flex;gap:6px;align-items:center;margin-bottom:8px;background:#05050a;padding:6px;border-radius:5px;border:1px solid var(--border);'>",
    "<span style='font-size:0.58rem;color:var(--muted);'>決済金額 (JPY):</span>",
    "<input type='number' id='qrAmountJpy' class='inp' style='width:100px;font-weight:bold;color:var(--gold);' value='1000' min='1'>",
    "<span style='font-size:0.5rem;color:var(--green);'>※下の各ブランドを選択して即時QRコード発行</span>",
    "</div>",
    "<div class='g4'>",
    "<div class='box'><div><strong>PayPay</strong><span class='qbadge' style='background:#ff0033;color:#fff;'>JP</span></div><div class='addr' style='margin-top:4px;'>ペイペイ決済</div><button class='btn' style='border-color:#ff0033;' onclick='openQrPay(\"PayPay\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>au PAY</strong><span class='qbadge' style='background:#eb5505;color:#fff;'>JP</span></div><div class='addr' style='margin-top:4px;'>KDDIコード決済</div><button class='btn' style='border-color:#eb5505;' onclick='openQrPay(\"au PAY\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>d払い</strong><span class='qbadge' style='background:#cc0033;color:#fff;'>JP</span></div><div class='addr' style='margin-top:4px;'>docomo決済</div><button class='btn' style='border-color:#cc0033;' onclick='openQrPay(\"d払い\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>楽天ペイ</strong><span class='qbadge' style='background:#bf0000;color:#fff;'>JP</span></div><div class='addr' style='margin-top:4px;'>Rakuten Pay</div><button class='btn' style='border-color:#bf0000;' onclick='openQrPay(\"楽天ペイ\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>メルペイ</strong><span class='qbadge' style='background:#4dc4ff;color:#000;'>JP</span></div><div class='addr' style='margin-top:4px;'>Merpayコード</div><button class='btn' style='border-color:#4dc4ff;' onclick='openQrPay(\"メルペイ\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>ファミペイ</strong><span class='qbadge' style='background:#009944;color:#fff;'>JP</span></div><div class='addr' style='margin-top:4px;'>FamiPay決済</div><button class='btn' style='border-color:#009944;' onclick='openQrPay(\"ファミペイ\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>Bank Pay</strong><span class='qbadge' style='background:#1d4ed8;color:#fff;'>BANK</span></div><div class='addr' style='margin-top:4px;'>銀行口座直結QR</div><button class='btn' style='border-color:#1d4ed8;' onclick='openQrPay(\"Bank Pay\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>Smart Code</strong><span class='qbadge' style='background:#059669;color:#fff;'>JCB</span></div><div class='addr' style='margin-top:4px;'>統一QRスキーム</div><button class='btn' style='border-color:#059669;' onclick='openQrPay(\"Smart Code\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>Alipay+</strong><span class='qbadge' style='background:#1677ff;color:#fff;'>CN/GL</span></div><div class='addr' style='margin-top:4px;'>アリペイ国際決済</div><button class='btn' style='border-color:#1677ff;' onclick='openQrPay(\"Alipay+\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>WeChat Pay</strong><span class='qbadge' style='background:#07c160;color:#fff;'>CN/GL</span></div><div class='addr' style='margin-top:4px;'>微信支付コード</div><button class='btn' style='border-color:#07c160;' onclick='openQrPay(\"WeChat Pay\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>UnionPay</strong><span class='qbadge' style='background:#00447c;color:#fff;'>銀聯</span></div><div class='addr' style='margin-top:4px;'>銀聯QRコード</div><button class='btn' style='border-color:#00447c;' onclick='openQrPay(\"UnionPay QR\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>PayPal QR</strong><span class='qbadge' style='background:#003087;color:#fff;'>US/GL</span></div><div class='addr' style='margin-top:4px;'>PayPalコード決済</div><button class='btn' style='border-color:#003087;' onclick='openQrPay(\"PayPal QR\")'>QR決済発行 ↗</button></div>",
    "<div class='box'><div><strong>Kakao Pay</strong><span class='qbadge' style='background:#fee500;color:#000;'>KR</span></div><div class='addr' style='margin-top:4px;'>カカオペイ決済</div><button class='btn' style='border-color:#fee500;' onclick='openQrPay(\"Kakao Pay\")'>QR
