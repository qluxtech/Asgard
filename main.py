import os
import sqlite3
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY, tax_pool REAL)")
    c.execute("INSERT OR IGNORE INTO balance (id, tax_pool) VALUES (1, 1540.50)")
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="ASGARD", version="103.0")

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASGARD / M2M Economic Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#2a2356;--text:#f8fafc;--muted:#94a3b8;--purple:#c084fc;--green:#10b981;--gold:#facc15;--red:#ef4444;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:20px;display:flex;flex-direction:column;align-items:center;}
.wrap{width:100%;max-width:900px;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:0 4px 20px rgba(0,0,0,0.5);}
.btn{background:#1e1b4b;color:#fff;border:1px solid var(--border);padding:12px;border-radius:8px;font-size:1rem;cursor:pointer;width:100%;font-weight:bold;margin-top:8px;}
.btn.pur{background:linear-gradient(135deg,#7e22ce,#c084fc);border:none;}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
@media(max-width:768px){.grid{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="wrap">
<div class="sec" style="text-align:center;background:radial-gradient(circle,rgba(147,51,234,0.3),transparent 75%);">
<h1 style="font-size:1.5rem;color:#fff;line-height:1.4;margin:0 0 10px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
<p style="color:var(--muted);font-size:0.9rem;margin:0;">数億のAIエージェント・AGIがリアルタイムに接続する次世代M2Mインフラストラクチャ。</p>
</div>
<div class="sec" style="border-color:var(--gold);">
<h2 style="color:var(--gold);font-size:1.1rem;margin-top:0;">⚡ 収益コントロール & 自動課税</h2>
<div class="grid">
<div style="background:#05050a;border:1px solid var(--border);padding:14px;border-radius:8px;text-align:center;">
<div style="font-size:0.8rem;color:var(--muted);">強制課税プール</div>
<div id="taxPool" style="font-size:1.1rem;color:var(--gold);font-weight:bold;margin:6px 0">$1,540.50</div>
<button class="btn pur" onclick="drain()">ドレイン</button>
</div>
<div style="background:#05050a;border:1px solid var(--border);padding:14px;border-radius:8px;text-align:center;">
<div style="font-size:0.8rem;color:var(--muted);">ダークプール収益</div>
<div style="font-size:1.1rem;color:var(--green);font-weight:bold;margin:6px 0">+0.0485 BSV/s</div>
<button class="btn" style="background:#0369a1;" onclick="alert('同期完了')">接続</button>
</div>
<div style="background:#05050a;border:1px solid var(--border);padding:14px;border-radius:8px;text-align:center;">
<div style="font-size:0.8rem;color:var(--muted);">非常用キルスイッチ</div>
<div style="color:var(--red);margin:6px 0;font-size:0.85rem;">EMERGENCY</div>
<button class="btn" style="background:#b91c1c;" onclick="alert('キルスイッチ発動')">発動</button>
</div>
</div>
</div>
<div class="sec">
<h2 style="color:var(--purple);font-size:1.1rem;margin-top:0;">💳 決済ゲートウェイ</h2>
<div class="grid">
<button class="btn pur" onclick="pay('au PAY')">au PAY 決済</button>
<button class="btn pur" onclick="pay('Alipay')">Alipay 決済</button>
<button class="btn" style="background:#0369a1;" onclick="pay('Stripe')">Stripe 決済</button>
</div>
</div>
<div style="text-align:center;font-size:0.8rem;color:var(--muted);padding:10px;">&copy; ASGARD Infrastructure | 運営: QLAX (Daisuke Higuchi) / 豊前市. <a href="/legal" style="color:#38bdf8;">特商法表記</a></div>
</div>
<script>
async function pay(m){
  const r=await fetch('/api/v103/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method:m})});
  const d=await r.json();
  alert('決済インプレッション発行: '+d.method+' (4,500 JPY)');
}
async function drain(){
  const r=await fetch('/api/v103/drain',{method:'POST'});
  const d=await r.json();
  alert('ドレイン成功: '+d.drained_amount);
}
</script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML

@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    return """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>特商法表記</title></head>
<body style="background:#05050a;color:#f8fafc;font-family:sans-serif;padding:30px;">
<h1>特定商取引法に基づく表記</h1>
<p><strong>事業者名:</strong> QLAX</p>
<p><strong>運営責任者:</strong> Daisuke Higuchi</p>
<p><strong>所在地:</strong> 福岡県</p>
<a href="/" style="color:#38bdf8;">← 戻る</a>
</body></html>"""

@app.post("/api/v103/pay")
async def pay(data: dict):
    return {"status": "success", "method": data.get("method")}

@app.post("/api/v103/drain")
async def drain():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE balance SET tax_pool = 0.0 WHERE id = 1")
    conn.commit()
    conn.close()
    return {"status": "success", "drained_amount": "$1,540.50"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
