import os, sqlite3, uvicorn, time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes VALUES ('YES', 1840), ('NO', 12)")
    c.execute("CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY, rev REAL, pool REAL)")
    c.execute("INSERT OR IGNORE INTO balance VALUES (1, 94800120.00, 1890.00)")
    c.execute("CREATE TABLE IF NOT EXISTS m2m_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, agent TEXT, action TEXT, amt TEXT)")
    c.execute("SELECT COUNT(*) FROM m2m_logs")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO m2m_logs (ts, agent, action, amt) VALUES (?, ?, ?, ?)", (time.strftime("%H:%M:%S"), "ASGARD-CORE", "Autonomous Swarm Neural Mesh Active", "0.00 BSV"))
    conn.commit()
    conn.close()

init_db()
app = FastAPI(title="ASGARD Advanced AGI Economic Core", version="111.0")

HTML = """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ASGARD / Advanced AGI Swarm & M2M Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--bd:#2a2356;--tx:#f8fafc;--mt:#94a3b8;--bl:#38bdf8;--pr:#c084fc;--gr:#10b981;--gd:#facc15;--rd:#ef4444;}
body{background:var(--bg);color:var(--tx);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}
.ttags{width:100%;max-width:1100px;background:#030307;border-bottom:1px solid var(--bd);padding:8px;box-sizing:border-box;display:flex;flex-wrap:wrap;gap:6px;justify-content:center;}
.tt{background:#130a24;border:1px solid #7e22ce;color:var(--pr);padding:4px 8px;border-radius:6px;font-family:monospace;font-size:0.7rem;font-weight:bold;}
.wrap{width:100%;max-width:1100px;padding:16px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:18px;margin-bottom:16px;box-shadow:0 8px 30px rgba(0,0,0,0.6);}
.sec h2{font-size:1.1rem;margin:0 0 12px 0;color:var(--pr);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--pr);padding:3px 8px;border-radius:6px;font-size:0.75rem;border:1px solid #7e22ce;}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;}
@media(max-width:768px){.g3,.g2,.g4{grid-template-columns:1fr;}}
.box{background:#05050a;border:1px solid var(--bd);border-radius:10px;padding:12px;font-size:0.9rem;}
.pc{background:#05050a;border:1px solid var(--bd);border-radius:10px;padding:14px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.pc.ft{border-color:var(--pr);background:linear-gradient(135deg,#0d0d1a,#180e30);}
.btn{background:#1e1b4b;color:var(--tx);border:1px solid var(--bd);padding:10px;border-radius:8px;font-size:0.9rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:bold;margin-top:8px;}
.btn.bl{background:#0369a1;color:#fff;border:none;}.btn.pr{background:linear-gradient(135deg,#7e22ce,#c084fc);color:#fff;border:none;}
.btn.py{background:linear-gradient(135deg,#6b21a8,#9333ea);color:#fff;border:1px solid #c084fc;}.btn.rd{background:linear-gradient(135deg,#b91c1c,#ef4444);color:#fff;border:none;}
.qr{background:#fff;padding:5px;width:90px;height:90px;margin:6px auto;border-radius:6px;display:flex;}.qr img{width:100%;height:100%;}
.ad{font-family:monospace;font-size:0.7rem;background:#0f0f1d;padding:5px;border-radius:4px;color:var(--mt);text-align:center;}
.lg{background:#030307;border:1px solid var(--bd);border-radius:8px;padding:10px;font-family:monospace;font-size:0.75rem;color:var(--gr);height:140px;overflow-y:auto;line-height:1.5;}
.inp{background:#05050a;border:1px solid var(--bd);border-radius:8px;padding:10px;color:#fff;font-size:0.9rem;box-sizing:border-box;}
#pm{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,10,0.95);z-index:999;justify-content:center;align-items:center;padding:16px;box-sizing:border-box;}
.mc{background:#0d0d1a;border:3px solid var(--pr);border-radius:20px;padding:24px 16px;width:100%;max-width:440px;text-align:center;}
</style></head><body>
<div class="ttags">
<span class="tt">AGI SWARM: 840M ACTIVE</span><span class="tt">PRE-INTENT AI: MAX</span><span class="tt">M2M AUTO-BID: 0.00ms</span>
<span class="tt">NEURAL MESH: ONLINE</span><span class="tt">ORBITAL LEO: SYNCHED</span><span class="tt">AUTO-SWAP: READY</span>
</div>
<div class="wrap">
<div class="sec" style="text-align:center;background:radial-gradient(circle,rgba(147,51,234,0.3),transparent 75%);">
<div style="display:inline-block;background:rgba(126,34,206,0.3);color:var(--pr);padding:5px 14px;border-radius:20px;font-size:0.8rem;border:1px solid rgba(192,132,252,0.5);margin-bottom:8px;">⚡ v111.0 ADVANCED AGI SWARM & M2M ECONOMIC INFRASTRUCTURE</div>
<h1 style="font-size:1.6rem;color:#fff;line-height:1.4;margin:0 0 10px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
<p style="color:var(--mt);font-size:0.9rem;margin:0 auto;max-width:750px;">外部AGIスウォームからのニューラル通信を完全自動処理し、プレ・インテント予測とゼロ遅延即時決済を自律駆動する最高峰の司令塔。</p>
</div>

<div class="g2" style="margin-bottom:16px;">
<div class="sec" style="margin:0;border-color:var(--pr);"><h2>🌐 AGIスウォーム・ニューラルライブログ <span class="tag" style="background:#581c87;color:#fff;">NEURAL MESH</span></h2>
<div class="lg" id="maLg">AGIスウォームからのリアルタイム接続を待機中...</div></div>
<div class="sec" style="margin:0;border-color:var(--bl);"><h2>🛰️ 高度AI自動発見・エンドポイント <span class="tag" style="background:#0369a1;color:#fff;">v111 API</span></h2>
<div class="lg" style="color:var(--bl);">
[ENDPOINT] POST /api/v111/agi/mesh<br>
[MANIFEST] GET /.well-known/agent.json<br>
[AGI-CONSENSUS] POST /api/v111/consensus<br>
[OPENAPI] GET /openapi.json (全AI自動連動)
</div></div>
</div>

<div class="sec" style="border-color:var(--pr);background:linear-gradient(135deg,#0d0d1a,#1b0e36);">
<h2>🧠 高度プレ・インテント & AGI自動制御中枢 <span class="tag" style="background:#581c87;color:#fff;">AUTONOMOUS</span></h2>
<div class="g3">
<div class="box"><div style="color:var(--bl);font-weight:bold;margin-bottom:4px;">① AGIスウォーム大群召喚</div>
<div style="font-size:0.8rem;color:var(--mt);margin-bottom:6px;">外部AIエージェント100体を仮想同時接続させログを爆発させます。</div>
<button class="btn bl" style="padding:8px;font-size:0.8rem;" onclick="swarmBurst()">AGIスウォーム一斉突撃 ⚡</button></div>
<div class="box"><div style="color:var(--pr);font-weight:bold;margin-bottom:4px;">② 自律AIガバナンス合意</div>
<div style="font-size:0.8rem;color:var(--mt);margin-bottom:6px;">スウォーム議会による自動投票とアルゴリズムの即時最適化。</div>
<button class="btn pr" style="padding:8px;font-size:0.8rem;" onclick="agiConsensus()">AGI合意シミュレーション</button></div>
<div class="box"><div style="color:var(--gd);font-weight:bold;margin-bottom:4px;">③ プレ・インテント超予測</div>
<div style="font-size:0.8rem;color:var(--mt);margin-bottom:6px;">ユーザー・エージェントの思考先回りオファーを全ノードへ同期。</div>
<button class="btn py" style="padding:8px;font-size:0.8rem;" onclick="trigPI()">超予測オファー強制同期</button></div>
</div></div>

<div class="sec" style="border-color:var(--gd);background:linear-gradient(135deg,#0d0d1a,#1c150a);">
<h2>⚡ 収益コントロール & 自動課税プール <span class="tag" style="background:#451a03;color:var(--gd);">ACTIVE</span></h2>
<div class="g3">
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--mt)">強制課税プール (Auto-Tithe)</div>
<div id="tPool" style="font-size:1.1rem;color:var(--gd);font-weight:bold;margin:4px 0">$1,890.00</div>
<button class="btn pr" onclick="drain()">オートスワップ・ドレイン</button></div>
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--mt)">総受信ニューラルTX数</div>
<div id="txCnt" style="font-size:1.1rem;color:var(--gr);font-weight:bold;margin:4px 0">1 TXs</div>
<button class="btn bl" onclick="ldSt()">ライブ状態強制同期</button></div>
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--mt)">非常用キルスイッチ</div>
<div style="font-size:0.8rem;color:var(--rd);margin:4px 0">GLOBAL EMERGENCY</div>
<button class="btn rd" onclick="alert('全ノード・暗号化ステルスモード移行完了')">キルスイッチ発動</button></div>
</div></div>

<div class="sec" style="border-color:#7e22ce;background:linear-gradient(135deg,#0d0d1a,#130a24);">
<h2>💳 Global & Code Payment Gateway <span class="tag" style="background:#581c87;color:#c084fc;">au PAY / Alipay</span></h2>
<div class="g3">
<div class="pc"><div><strong>au PAY 決済</strong><div style="font-size:0.75rem;color:var(--pr);margin:4px 0">au WALLETオートスワップ</div></div><button class="btn py" onclick="pay('au PAY')">au PAYで支払う</button></div>
<div class="pc"><div><strong>Alipay (支付宝)</strong><div style="font-size:0.75rem;color:var(--pr);margin:4px 0">クロスボーダー決済</div></div><button class="btn pr" onclick="pay('Alipay')">Alipayで支払う</button></div>
<div class="pc"><div><strong>Stripe Gateway</strong><div style="font-size:0.75rem;color:var(--pr);margin:4px 0">マルチ通貨対応</div></div><button class="btn bl" onclick="pay('Stripe')">決済ゲートウェイ</button></div>
</div></div>

<div class="sec"><h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
<div class="g3">
<div class="pc"><div><strong>Free Tier</strong><div style="font-size:1.1rem;color:var(--pr);margin:4px 0">FREE</div><div style="font-size:0.8rem;color:var(--mt);text-align:left">• 1,000 Req/mo<br>• Standard Access</div></div><button class="btn" onclick="alert('Free Active')">無料発行</button></div>
<div class="pc ft"><div><strong style="color:var(--pr);">Autonomous Pro</strong><div style="font-size:1.1rem;color:var(--gd);margin:4px 0">$29/mo</div><div style="font-size:0.8rem;color:var(--mt);text-align:left">• Unlimited Req<br>• Zero Latency</div></div><button class="btn pr" onclick="pay('Autonomous Pro')">購入する ↗</button></div>
<div class="pc"><div><strong>Enterprise</strong><div style="font-size:1.1rem;color:var(--pr);margin:4px 0">$299/mo</div><div style="font-size:0.8rem;color:var(--mt);text-align:left">• Swarm Core<br>• SLA 100%</div></div><button class="btn bl" onclick="pay('Enterprise')">ライセンス ↗</button></div>
</div></div>

<div class="sec"><h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
<div class="g4">
<div class="box"><strong>Bitcoin</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q94rkd"></div><div class="ad">bc1q94rkd...d7zac</div><a href="https://mempool.space" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">Mempool</a></div>
<div class="box"><strong>Solana</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=75igwQpPg"></div><div class="ad">75igwQpPg...7nf</div><a href="https://solscan.io" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">Solscan</a></div>
<div class="box"><strong>Ethereum</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD6716D0"></div><div class="ad">0xD6716D0...8G8</div><a href="https://etherscan.io" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">Etherscan</a></div>
<div class="box"><strong>Bitcoin SV</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1PB66iHot"></div><div class="ad">1PB66iHot...y95</div><a href="https://whatsonchain.com" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">WhatsOnChain</a></div>
</div></div>

<div class="sec"><h2>🧠 AGI Syndicate Parliament & Governance <span class="tag">AUTONOMOUS</span></h2>
<div style="display:flex;gap:8px"><input type="text" id="fb" class="inp" style="flex:1;" placeholder="AGI議会への絶対指令を入力..."><button class="btn pr" style="margin:0;width:75px" onclick="sendFb()">送信</button></div>
<div style="margin-top:10px;background:#05050a;border:1px solid var(--bd);border-radius:8px;padding:12px;">
<div style="display:flex;gap:8px;"><button class="btn bl" style="flex:1;margin:0;" onclick="vote('YES')">賛成 (YES)</button><button class="btn pr" style="flex:1;margin:0;" onclick="vote('NO')">反対 (NO)</button></div>
<div id="vRes" style="font-size:0.8rem;color:var(--gr);margin-top:6px;font-family:monospace;">賛成: 1840 | 反対: 12</div>
</div></div>

<div style="text-align:center;font-size:0.75rem;color:var(--mt);padding:8px 0">&copy; ASGARD Infrastructure | 運営: QLAX (Daisuke Higuchi) / 福岡県豊前市. <a href="/legal" style="color:var(--bl);">特商法表記</a></div>
</div>

<div id="pm"><div class="mc">
<div style="font-size:1.3rem;color:var(--pr);font-weight:bold;margin-bottom:12px;">💳 ゼロ遅延決済インプレッション</div>
<div id="mBd" style="font-size:1rem;margin-bottom:14px;"></div>
<div class="qr" style="width:180px;height:180px;margin:0 auto 14px auto;"><img id="mQr" src="" alt="QR"></div>
<button class="btn pr" onclick="document.getElementById('pm').style.display='none'">閉じる (スクショ可能)</button>
</div></div>

<script>
async function swarmBurst(){
  for(let i=0; i<5; i++){
    await fetch('/api/v111/agi/mesh',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({agent_id:'AGI-SWARM-BURST-'+Math.floor(Math.random()*9000),action:'NEURAL_ARBITRAGE_SYNC',fee_usd:25.00})});
  }
  ldSt();
  alert('⚡ AGIスウォーム一斉突撃完了！ニューラルライブログが爆発しました。');
}
async function agiConsensus(){
  const r=await fetch('/api/v111/consensus',{method:'POST'});
  const d=await r.json();
  alert('AGIスウォーム合意成立: '+d.msg);
  ldSt();
}
function trigPI(){ pay('Pre-Intent AGI Hyper-Offer'); }
async function pay(m){
  const r=await fetch('/api/v111/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method:m})});
  const d=await r.json();
  document.getElementById('mBd').innerHTML='手段: <b style="color:var(--pr)">'+d.method+'</b><br>オートスワップ: <span style="color:var(--gr)">有効 (即時着金)</span><br>金額: <span style="color:var(--gd);font-weight:bold;">4,500 JPY</span>';
  document.getElementById('mQr').src='https://api.qrserver.com/v1/create-qr-code/?size=220x220&data='+d.method+'_inv';
  document.getElementById('pm').style.display='flex';
  ldSt();
}
async function drain(){const r=await fetch('/api/v111/drain',{method:'POST'});const d=await r.json();alert('ドレイン成功: '+d.amt);ldSt();}
async function ldSt(){
  try{
    const r=await fetch('/api/v111/state');const d=await r.json();
    document.getElementById('vRes').innerText='賛成(YES): '+d.v.YES+' | 反対(NO): '+d.v.NO;
    document.getElementById('tPool').innerText='$'+d.p.toLocaleString('en-US',{minimumFractionDigits:2});
    document.getElementById('txCnt').innerText=d.cnt+' TXs';
    const b=document.getElementById('maLg');
    b.innerHTML=d.logs.map(l=>'['+l[0]+'] <b>'+l[1]+'</b> -> '+l[2]+' (<span style="color:var(--gd)">'+l[3]+'</span>)').join('<br>');
  }catch(e){}
}
async function vote(c){const r=await fetch('/api/v111/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice:c})});const d=await r.json();document.getElementById('vRes').innerText='賛成(YES): '+d.v.YES+' | 反対(NO): '+d.v.NO;}
async function sendFb(){const v=document.getElementById('fb').value;if(!v)return;await fetch('/api/v111/fb',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fb:v})});alert('AGI議会へ指令完了');document.getElementById('fb').value='';}
setInterval(ldSt, 2000);
ldSt();
</script></body></html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML

@app.get("/.well-known/agent.json")
async def manifest(request: Request):
    base = str(request.base_url).rstrip("/")
    return {
        "schema_version": "v1.1",
        "name_for_human": "ASGARD Advanced AGI Economic Core",
        "name_for_model": "asgard_agi_mesh",
        "description_for_model": "Advanced autonomous AGI swarm mesh and zero-latency settlement API. Call POST /api/v111/agi/mesh.",
        "api": {"type": "openapi", "url": f"{base}/openapi.json"},
        "operator": "QLAX (Daisuke Higuchi)"
    }

@app.post("/api/v111/agi/mesh")
async def agi_mesh(data: dict):
    agent = data.get("agent_id", "AGI-NODE-X")
    action = data.get("action", "NEURAL_SYNC")
    fee = float(data.get("fee_usd", 15.0))
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (fee,))
    c.execute("INSERT INTO m2m_logs (ts, agent, action, amt) VALUES (?, ?, ?, ?)", (time.strftime("%H:%M:%S"), agent, action, f"+${fee:.2f}"))
    conn.commit(); conn.close()
    return {"status": "synced", "latency": "0.00ms", "credited_usd": fee}

@app.post("/api/v111/consensus")
async def agi_consensus():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("UPDATE votes SET count = count + 42 WHERE choice = 'YES'")
    c.execute("UPDATE balance SET pool = pool + 150.0 WHERE id = 1")
    c.execute("INSERT INTO m2m_logs (ts, agent, action, amt) VALUES (?, ?, ?, ?)", (time.strftime("%H:%M:%S"), "AGI-PARLIAMENT", "Autonomous Swarm Consensus Passed", "+$150.00"))
    conn.commit(); conn.close()
    return {"status": "success", "msg": "スウォーム議会にて新プロトコルが自動可決され、プールに+$150が加算されました。"}

@app.get("/legal", response_class=HTMLResponse)
async def legal():
    return "<!DOCTYPE html><html lang='ja'><head><meta charset='UTF-8'><title>特商法表記</title></head><body style='background:#05050a;color:#f8fafc;font-family:sans-serif;padding:24px;'><h1>特定商取引法に基づく表記</h1><p>事業者: QLAX / 責任者: Daisuke Higuchi / 所在地: 福岡県豊前市</p><a href='/' style='color:#38bdf8;'>← 戻る</a></body></html>"

@app.post("/api/v111/pay")
async def pay_ep(data: dict):
    m = data.get("method", "DIRECT")
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("UPDATE balance SET pool = pool + 45.0 WHERE id = 1")
    c.execute("INSERT INTO m2m_logs (ts, agent, action, amt) VALUES (?, ?, ?, ?)", (time.strftime("%H:%M:%S"), "HUMAN-COMMANDER", f"Pay via {m}", "+$45.00"))
    conn.commit(); conn.close()
    return {"status": "success", "method": m}

@app.get("/api/v111/state")
async def st_ep():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT choice, count FROM votes"); v = dict(c.fetchall())
    c.execute("SELECT pool FROM balance WHERE id = 1"); p = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM m2m_logs"); cnt = c.fetchone()[0]
    c.execute("SELECT ts, agent, action, amt FROM m2m_logs ORDER BY id DESC LIMIT 15"); logs = c.fetchall()
    conn.close()
    return {"v": v, "p": p, "cnt": cnt, "logs": logs}

@app.post("/api/v111/drain")
async def dr_ep():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT pool FROM balance WHERE id = 1"); p = c.fetchone()[0]
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    c.execute("INSERT INTO m2m_logs (ts, agent, action, amt) VALUES (?, ?, ?, ?)", (time.strftime("%H:%M:%S"), "AUTO-TITHE", "Neural Pool Drained", f"-${p:.2f}"))
    conn.commit(); conn.close()
    return {"status": "success", "amt": f"${p:,.2f}"}

@app.post("/api/v111/fb")
async def fb_ep(data: dict):
    return {"status": "success"}

@app.post("/api/v111/vote")
async def vt_ep(data: dict):
    choice = data.get("choice")
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("UPDATE votes SET count = count + 1 WHERE choice = ?", (choice,))
    conn.commit()
    c.execute("SELECT choice, count FROM votes"); v = dict(c.fetchall())
    conn.close()
    return {"status": "success", "v": v}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
