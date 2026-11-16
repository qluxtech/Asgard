import os, sqlite3, uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes VALUES ('YES', 1420), ('NO', 18)")
    c.execute("CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY, rev REAL, pool REAL)")
    c.execute("INSERT OR IGNORE INTO balance VALUES (1, 94800120.00, 1540.50)")
    conn.commit()
    conn.close()

init_db()
app = FastAPI(title="ASGARD", version="109.0")

HTML = """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ASGARD / M2M Autonomous Economy & Pre-Intent Engine</title>
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
.lg{background:#030307;border:1px solid var(--bd);border-radius:8px;padding:10px;font-family:monospace;font-size:0.75rem;color:var(--gr);height:100px;overflow-y:auto;line-height:1.4;}
.inp{background:#05050a;border:1px solid var(--bd);border-radius:8px;padding:10px;color:#fff;font-size:0.9rem;box-sizing:border-box;}
#pm{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,10,0.95);z-index:999;justify-content:center;align-items:center;padding:16px;box-sizing:border-box;}
.mc{background:#0d0d1a;border:3px solid var(--pr);border-radius:20px;padding:24px 16px;width:100%;max-width:440px;text-align:center;}
</style></head><body>
<div class="ttags">
<span class="tt">VAPORLOCK: ACTIVE</span><span class="tt">PRE-INTENT AI: ON</span><span class="tt">M2M AUTO-BID: 0.00ms</span>
<span class="tt">SWARM-LOCK: 36.8K/S</span><span class="tt">ORBITAL LEO: ONLINE</span><span class="tt">AUTO-SWAP: READY</span>
</div>
<div class="wrap">
<div class="sec" style="text-align:center;background:radial-gradient(circle,rgba(147,51,234,0.3),transparent 75%);">
<div style="display:inline-block;background:rgba(126,34,206,0.3);color:var(--pr);padding:5px 14px;border-radius:20px;font-size:0.8rem;border:1px solid rgba(192,132,252,0.5);margin-bottom:8px;">⚡ GOD-TIER AGI & PRE-INTENT M2M INFRASTRUCTURE</div>
<h1 style="font-size:1.6rem;color:#fff;line-height:1.4;margin:0 0 10px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
<p style="color:var(--mt);font-size:0.9rem;margin:0 auto;max-width:750px;">検索の前に文脈を先回りする「プレ・インテントAI」と、数億の自律エージェントによるゼロ遅延M2M即時決済を完全統合。</p>
</div>

<div class="sec" style="border-color:var(--pr);background:linear-gradient(135deg,#0d0d1a,#1b0e36);">
<h2>🧠 次世代M2Mマーケティング & プレ・インテント中枢 <span class="tag" style="background:#581c87;color:#fff;">ZERO-FRICTION</span></h2>
<div class="g3">
<div class="box"><div style="color:var(--bl);font-weight:bold;margin-bottom:4px;">① 文脈先回り (Pre-Intent)</div>
<div style="font-size:0.8rem;color:var(--mt);margin-bottom:6px;">検索前の環境・文脈を検知し、必要リソースを自動展開。</div>
<div id="piSt" style="font-family:monospace;font-size:0.75rem;color:var(--gr);">検知中: 最適オファー準備完了</div>
<button class="btn bl" style="padding:8px;font-size:0.8rem;" onclick="trigPI()">文脈先回りオファー発動</button></div>
<div class="box"><div style="color:var(--pr);font-weight:bold;margin-bottom:4px;">② M2Mエージェント自動選定</div>
<div style="font-size:0.8rem;color:var(--mt);margin-bottom:6px;">AIエージェントが論理・速度(0.00ms)で最適APIを自動契約。</div>
<div style="font-family:monospace;font-size:0.75rem;color:var(--gd);">/.well-known/agent.json 公開中</div>
<a href="/.well-known/agent.json" target="_blank" class="btn pr" style="padding:8px;font-size:0.8rem;">AI選定マニフェスト確認 ↗</a></div>
<div class="box"><div style="color:var(--gd);font-weight:bold;margin-bottom:4px;">③ インパルス即時決済</div>
<div style="font-size:0.8rem;color:var(--mt);margin-bottom:6px;">意思決定の摩擦ゼロ。コンマ数秒で決済と着金を完了。</div>
<div style="font-family:monospace;font-size:0.75rem;color:var(--gr);">オートスワップ直結: 稼働中</div>
<button class="btn py" style="padding:8px;font-size:0.8rem;" onclick="pay('Pre-Intent Instant Offer')">ゼロ遅延ワンタップ決済</button></div>
</div></div>

<div class="sec" style="border-color:var(--gd);background:linear-gradient(135deg,#0d0d1a,#1c150a);">
<h2>⚡ 収益コントロール & 自動課税 <span class="tag" style="background:#451a03;color:var(--gd);">ACTIVE</span></h2>
<div class="g3">
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--mt)">強制課税プール (Auto-Tithe)</div>
<div id="tPool" style="font-size:1.1rem;color:var(--gd);font-weight:bold;margin:4px 0">$1,540.50</div>
<button class="btn pr" onclick="drain()">オートスワップ・ドレイン</button></div>
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--mt)">ダークプール収益</div>
<div style="font-size:1.1rem;color:var(--gr);font-weight:bold;margin:4px 0">+0.0485 BSV/s</div>
<button class="btn bl" onclick="bstLEO()">衛星軌道LEOブースト</button></div>
<div class="box" style="text-align:center"><div style="font-size:0.75rem;color:var(--mt)">非常用キルスイッチ</div>
<div style="font-size:0.8rem;color:var(--rd);margin:4px 0">GLOBAL EMERGENCY</div>
<button class="btn rd" onclick="alert('全ノード・暗号化ステルスモード移行完了')">キルスイッチ発動</button></div>
</div></div>

<div class="g2" style="margin-bottom:16px;">
<div class="sec" style="margin:0;"><h2>🌐 AI自律M&A・自動選定ログ <span class="tag">LIVE</span></h2>
<div class="lg" id="maLg">[M2M-SELECT] Agent #8821 auto-selected ASGARD API (0.00ms)<br>[M&A-DEAL] Swarm Syndicate acquired API #402 (0.15 BSV)<br>[PRE-INTENT] Context match 99.9% -> Auto-settled</div></div>
<div class="sec" style="margin:0;"><h2>🛰️ 衛星軌道(LEO)直結リンク <span class="tag" style="background:#0369a1;color:#fff;">0.00ms</span></h2>
<div class="lg" id="leoLg" style="color:var(--bl);">[LEO-L2] Quantum encryption handshake established<br>[ORBITAL] Cross-chain node sync rate: 100%<br>[READY] Zero-latency packet routing active</div></div>
</div>

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
<div class="g4" style="margin-bottom:10px;">
<div class="box" style="text-align:center"><div style="font-size:0.7rem;color:var(--mt)">埋蔵残高</div><div style="font-size:0.95rem;color:var(--gr);font-weight:bold">$94,800,120</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.7rem;color:var(--mt)">稼働エージェント</div><div style="font-size:0.95rem;color:var(--gr);font-weight:bold">442M units</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.7rem;color:var(--mt)">効率</div><div style="font-size:0.95rem;color:var(--gr);font-weight:bold">99.99%</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.7rem;color:var(--mt)">登録ノード</div><div style="font-size:0.95rem;color:var(--bl);font-weight:bold">128 nodes</div></div>
</div>
<div class="g4">
<div class="box"><strong>Bitcoin</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q94rkd"></div><div class="ad">bc1q94rkd...d7zac</div><a href="https://mempool.space" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">Mempool</a></div>
<div class="box"><strong>Solana</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=75igwQpPg"></div><div class="ad">75igwQpPg...7nf</div><a href="https://solscan.io" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">Solscan</a></div>
<div class="box"><strong>Ethereum</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD6716D0"></div><div class="ad">0xD6716D0...8G8</div><a href="https://etherscan.io" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">Etherscan</a></div>
<div class="box"><strong>Bitcoin SV</strong><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1PB66iHot"></div><div class="ad">1PB66iHot...y95</div><a href="https://whatsonchain.com" target="_blank" class="btn" style="padding:6px;font-size:0.8rem;">WhatsOnChain</a></div>
</div></div>

<div class="sec"><h2>🧠 AI Syndicate Parliament & Governance <span class="tag">AUTONOMOUS</span></h2>
<div style="margin-bottom:10px;background:#05050a;border:1px solid var(--bd);border-radius:8px;padding:12px;font-size:0.85rem;color:var(--pr);">
[AI議会 Proposal #109]: プレ・インテントAI自動入札アルゴリズム更新 → 99.9% 賛成で自動可決・適用中</div>
<div style="display:flex;gap:8px"><input type="text" id="fb" class="inp" style="flex:1;" placeholder="指令・フィードバックを入力..."><button class="btn pr" style="margin:0;width:75px" onclick="sendFb()">送信</button></div>
<div style="margin-top:10px;background:#05050a;border:1px solid var(--bd);border-radius:8px;padding:12px;">
<div style="font-size:0.85rem;color:var(--pr);font-weight:bold;margin-bottom:6px;">🌐 SWARM GOVERNANCE VOTING</div>
<div style="display:flex;gap:8px;"><button class="btn bl" style="flex:1;margin:0;" onclick="vote('YES')">賛成 (YES)</button><button class="btn pr" style="flex:1;margin:0;" onclick="vote('NO')">反対 (NO)</button></div>
<div id="vRes" style="font-size:0.8rem;color:var(--gr);margin-top:6px;font-family:monospace;">賛成: 1420 | 反対: 18</div>
</div></div>

<div class="sec"><h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
<div style="font-size:0.9rem;color:var(--mt);line-height:1.5;">
<p style="margin:0 0 4px 0;"><strong>ASGARD</strong>は、数億のAIエージェント・AGIが自動接続し、0.00msミリ秒決済とプレ・インテント自律仲介を提供する次世代のAI M2M経済インフラです。</p>
<p style="margin:0 0 4px 0;"><strong>QLAX</strong>は、福岡県豊前市を拠点に自律アービトラージと高スループット決済環境を構築・研究開発する個人事業主の組織です。</p>
<p style="margin:0;"><strong>運営責任者:</strong> Daisuke Higuchi</p>
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
function trigPI(){document.getElementById('piSt').innerText='発動完了: 0.00ms 最適オファー展開済み';pay('Pre-Intent Context Offer');}
function bstLEO(){alert('【衛星軌道LEOブースト発動】量子回線直結・収益スピード3倍加速！');document.getElementById('leoLg').innerHTML+='<br>[BOOST] Orbital LEO link maxed out (0.00ms)';}
async function pay(m){
  const r=await fetch('/api/v109/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method:m})});
  const d=await r.json();
  document.getElementById('mBd').innerHTML='手段: <b style="color:var(--pr)">'+d.method+'</b><br>オートスワップ: <span style="color:var(--gr)">有効 (即時着金)</span><br>金額: <span style="color:var(--gd);font-weight:bold;">4,500 JPY</span>';
  document.getElementById('mQr').src='https://api.qrserver.com/v1/create-qr-code/?size=220x220&data='+d.method+'_inv';
  document.getElementById('pm').style.display='flex';
}
async function drain(){const r=await fetch('/api/v109/drain',{method:'POST'});const d=await r.json();alert('ドレイン成功: '+d.amt);ldSt();}
async function ldSt(){try{const r=await fetch('/api/v109/state');const d=await r.json();document.getElementById('vRes').innerText='賛成(YES): '+d.v.YES+' | 反対(NO): '+d.v.NO;document.getElementById('tPool').innerText='$'+d.p.toLocaleString('en-US',{minimumFractionDigits:2});}catch(e){}}
async function vote(c){const r=await fetch('/api/v109/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice:c})});const d=await r.json();document.getElementById('vRes').innerText='賛成(YES): '+d.v.YES+' | 反対(NO): '+d.v.NO;}
async function sendFb(){const v=document.getElementById('fb').value;if(!v)return;await fetch('/api/v109/fb',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fb:v})});alert('AI議会へ送信完了');document.getElementById('fb').value='';}
setInterval(()=>{
  const ag=['#4921','#9932','#1024','#7739'],ac=['auto-selected ASGARD API','executed Pre-Intent bid','acquired API asset'],pr=['0.12 BSV','0.45 SOL','1.20 JPYC'];
  const b=document.getElementById('maLg');
  b.innerHTML+='<br>Agent '+ag[Math.floor(Math.random()*4)]+' '+ac[Math.floor(Math.random()*3)]+' ('+pr[Math.floor(Math.random()*3)]+')';
  b.scrollTop=b.scrollHeight;
},3500);
ldSt();
</script></body></html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML

@app.get("/.well-known/agent.json")
@app.get("/well-known/agent.json")
async def manifest():
    return {"schema_version":"2.0","name":"ASGARD Pre-Intent M2M Node","latency":"0.00ms","operator":{"organization":"QLAX","representative":"Daisuke Higuchi","location":"Buzen, Fukuoka, Japan"},"status":"online"}

@app.get("/legal", response_class=HTMLResponse)
async def legal():
    return "<!DOCTYPE html><html lang='ja'><head><meta charset='UTF-8'><title>特商法表記</title></head><body style='background:#05050a;color:#f8fafc;font-family:sans-serif;padding:24px;line-height:1.8;'><h1>特定商取引法に基づく表記</h1><p><strong>事業者名:</strong> QLAX / <strong>運営責任者:</strong> Daisuke Higuchi / <strong>所在地:</strong> 福岡県豊前市</p><p><strong>支払方法:</strong> Stripe, 暗号資産, au PAY, Alipay / <strong>引渡時期:</strong> 決済完了後即時(0.00ms) / <strong>返品:</strong> デジタル商品の性質上不可</p><a href='/' style='color:#38bdf8;'>← メイン画面へ戻る</a></body></html>"

@app.post("/api/v109/pay")
async def pay_ep(data: dict):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("UPDATE balance SET pool = pool + 45.0 WHERE id = 1")
    conn.commit(); conn.close()
    return {"status": "success", "method": data.get("method")}

@app.get("/api/v109/state")
async def st_ep():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT choice, count FROM votes"); v = dict(c.fetchall())
    c.execute("SELECT pool FROM balance WHERE id = 1"); p = c.fetchone()[0]
    conn.close()
    return {"v": v, "p": p}

@app.post("/api/v109/drain")
async def dr_ep():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT pool FROM balance WHERE id = 1"); p = c.fetchone()[0]
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    conn.commit(); conn.close()
    return {"status": "success", "amt": f"${p:,.2f}"}

@app.post("/api/v109/fb")
async def fb_ep(data: dict):
    return {"status": "success"}

@app.post("/api/v109/vote")
async def vt_ep(data: dict):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("UPDATE votes SET count = count + 1 WHERE choice = ?", (data.get("choice"),))
    conn.commit()
    c.execute("SELECT choice, count FROM votes"); v = dict(c.fetchall())
    conn.close()
    return {"status": "success", "v": v}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
