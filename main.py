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

app = FastAPI(title="ASGARD", version="98.0")

@app.get("/", response_class=HTMLResponse)
async def index():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>index.html not found</h1>"

@app.get("/docs", response_class=HTMLResponse)
async def docs_page():
    return "<html><body style='background:#05050a;color:#fff;font-family:sans-serif;padding:30px;font-size:1.3rem;'><h1>ASGARD API Docs</h1><a href='/' style='color:#38bdf8;'>← 戻る</a></body></html>"

@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>特定商取引法に基づく表記 / ASGARD</title>
<style>
body{background:#05050a;color:#f8fafc;font-family:sans-serif;margin:0;padding:24px;line-height:1.8;font-size:1.05rem;}
.container{max-width:900px;margin:0 auto;background:#0d0d1a;border:1px solid #2a2356;border-radius:14px;padding:30px;box-shadow:0 8px 30px rgba(0,0,0,0.6);}
h1{font-size:1.6rem;color:#c084fc;margin-bottom:20px;border-bottom:1px solid #2a2356;padding-bottom:12px;}
table{width:100%;border-collapse:collapse;margin-bottom:30px;}
th,td{padding:14px;border-bottom:1px solid #2a2356;text-align:left;vertical-align:top;}
th{width:32%;color:#94a3b8;font-size:1rem;}
td{color:#f8fafc;font-size:1.05rem;}
a{color:#38bdf8;text-decoration:none;}
.back{display:inline-block;margin-top:18px;background:#1e1b4b;color:#f8fafc;padding:12px 22px;border-radius:8px;border:1px solid #7e22ce;font-weight:bold;}
</style>
</head>
<body>
<div class="container">
<h1>特定商取引法に基づく表記</h1>
<table>
<tr><th>事業者名</th><td>QLAX</td></tr>
<tr><th>運営責任者</th><td>Daisuke Higuchi</td></tr>
<tr><th>所在地</th><td>〒828-0000 福岡県豊前市（詳細住所は請求があり次第遅滞なく開示します）</td></tr>
<tr><th>連絡先 / お問い合わせ</th><td>メールアドレスまたはプラットフォーム内サポート窓口よりご連絡ください。</td></tr>
<tr><th>販売価格</th><td>各プラン・サービスページに表示される金額（Autonomous Pro: $29/月, Enterprise: $299/月、その他API・ノード利用権に基づく）</td></tr>
<tr><th>商品代金以外の必要料金</th><td>ネットワーク手数料、決済手数料（ご利用の決済手段により異なります）</td></tr>
<tr><th>代金の支払い方法</th><td>クレジットカード（Stripe）、暗号資産（Bitcoin / BSV, Solana, Ethereum）、各種コード決済（au PAY, Alipay）</td></tr>
<tr><th>代金の支払い時期</th><td>各サービスお申し込み時、およびサブスクリプション毎月の更新時に即時決済されます。</td></tr>
<tr><th>サービス提供時期（引き渡し時期）</th><td>決済完了後、即時（リアルタイム / 0.00ms）にAPIエンドポイントおよびノード権限が解放・提供されます。</td></tr>
<tr><th>返品・キャンセルに関する特約</th><td>デジタルインフラストラクチャおよびAPIサービスの性質上、購入完了後の返品、換金、キャンセル、返金には応じられません。あらかじめご了承ください。</td></tr>
</table>
<a href="/" class="back">← メイン画面へ戻る</a>
</div>
</body>
</html>"""

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

@app.post("/api/v98/code-pay")
async def code_pay_endpoint(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE balance SET tax_pool = tax_pool + 45.0 WHERE id = 1")
    conn.commit()
    conn.close()
    return {"status": "success", "method": data.get("method"), "invoice_id": "inv_98", "amount_jpy": 4500}

@app.get("/api/v98/state")
async def get_system_state():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT choice, count FROM votes")
    votes = dict(c.fetchall())
    c.execute("SELECT tax_pool FROM balance WHERE id = 1")
    tax_pool = c.fetchone()[0]
    conn.close()
    return {"votes": votes, "tax_pool": tax_pool}

@app.post("/api/v98/drain")
async def post_drain():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT tax_pool FROM balance WHERE id = 1")
    pool = c.fetchone()[0]
    c.execute("UPDATE balance SET tax_pool = 0.0 WHERE id = 1")
    conn.commit()
    conn.close()
    return {"status": "success", "drained_amount": f"${pool:,.2f}"}

@app.post("/api/v98/feedback")
async def post_feedback(data: dict):
    return {"status": "success"}

@app.post("/api/v98/vote")
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
