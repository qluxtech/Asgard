import os
import datetime
import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

DB_PATH = "asgard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS votes (choice TEXT PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO votes (choice, count) VALUES ('YES', 1420), ('NO', 18)")
    c.execute("CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY, total_revenue REAL, tax_pool REAL)")
    c.execute("INSERT OR IGNORE INTO balance (id, total_revenue, tax_pool) VALUES (1, 94800120.00, 1540.50)")
    c.execute("CREATE TABLE IF NOT EXISTS telemetry_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="ASGARD", version="87.0")

HTML_PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>ASGARD / M2M Complete Economic Infrastructure</title>
<style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#2a2356;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;--red:#ef4444;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}

/* AIエージェントスウォームが欲しがるデータ群一覧のズラリ表示 */
.top-tags{width:100%;max-width:950px;background:#030307;border-bottom:1px solid var(--border);padding:14px 16px;box-sizing:border-box;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;}
.ttag{background:#130a24;border:1px solid #7e22ce;color:var(--purple);padding:8px 14px;border-radius:8px;font-family:monospace;font-size:0.95rem;font-weight:bold;box-shadow:0 4px 15px rgba(126,34,206,0.4);}

.nav{width:100%;max-width:950px;display:flex;justify-content:space-between;align-items:center;padding:20px 24px;box-sizing:border-box;border-bottom:1px solid var(--border);}
.logo{font-size:1.4rem;font-weight:bold;color:var(--purple);letter-spacing:1px;}

.hero{width:100%;padding:45px 24px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(147,51,234,0.3), transparent 75%);border-bottom:1px solid var(--border);}
.hero h1{font-size:2.1rem;font-weight:900;letter-spacing:-0.02em;margin:0 0 16px;color:#fff;background:linear-gradient(135deg, #fff 40%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 4px 15px rgba(192,132,252,0.5));line-height:1.4;}
.hero p{font-size:1.05rem;color:var(--muted);max-width:750px;margin:0 auto;line-height:1.7;}

.wrap{width:100%;max-width:950px;padding:20px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;margin-bottom:20px;box-shadow:0 8px 30px rgba(0,0,0,0.6);}
.sec h2{font-size:1.3rem;margin:0 0 16px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--purple);padding:6px 12px;border-radius:8px;font-size:0.85rem;border:1px solid #7e22ce;}

.g3{display:grid;grid-template-columns:repeat(3, 1fr);gap:14px;}
.g4{display:grid;grid-template-columns:repeat(4, 1fr);gap:12px;}
@media(max-width:768px){.g4{grid-template-columns:repeat(2, 1fr);}.g3{grid-template-columns:repeat(1, 1fr);}}

.box{background:#05050a;border:1px solid var(--border);border-radius:10px;padding:16px;font-size:1rem;}
.pcard{background:#05050a;border:1px solid var(--border);border-radius:10px;padding:18px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.pcard.feat{border-color:var(--purple);background:linear-gradient(135deg, #0d0d1a, #180e30);}

.btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:14px 18px;border-radius:8px;font-size:1rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:bold;margin-top:10px;}
.btn.blue{background:#0369a1;color:#fff;border:none;}
.btn.pur{background:linear-gradient(135deg, #7e22ce, #c084fc);color:#fff;border:none;}
.btn.pay{background:linear-gradient(135deg, #6b21a8, #9333ea);color:#fff;border:1px solid #c084fc;}
.btn.red{background:linear-gradient(135deg, #b91c1c, #ef4444);color:#fff;border:none;}

.qr{background:#fff;padding:8px;width:120px;height:120px;margin:10px auto;border-radius:8px;display:flex;}
.qr img{width:100%;height:100%;}
.addr{font-family:monospace;font-size:0.85rem;background:#0f0f1d;padding:8px;border-radius:6px;word-break:break-all;color:var(--muted);text-align:center;}
.cli{background:#05050a;border:1px solid var(--border);padding:16px 18px;border-radius:8px;font-family:monospace;font-size:0.9rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.inp{background:#05050a;border:1px solid var(--border);border-radius:8px;padding:14px;color:#fff;font-size:1rem;box-sizing:border-box;}

/* 決済モーダルポップアップ */
#payModal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,10,0.96);z-index:999;justify-content:center;align-items:center;padding:16px;box-sizing:border-box;}
.modal-content{background:#0d0d1a;border:4px solid var(--purple);border-radius:24px;padding:40px 20px;width:100%;max-width:520px;text-align:center;box-shadow:0 0 100px rgba(192,132,252,0.8);}
.modal-title{font-size:1.8rem;color:var(--purple);font-weight:bold;margin-bottom:20px;letter-spacing:1px;}
#modalBody{font-size:1.4rem;color:var(--text);margin-bottom:25px;line-height:1.8;}
.modal-qr{background:#fff;padding:16px;width:280px;height:280px;margin:0 auto 25px auto;border-radius:14px;display:flex;}
.modal-qr img{width:100%;height:100%;}
.modal-btn{font-size:1.3rem;padding:20px 24px;width:100%;border-radius:12px;}
</style>
</head>
<body>

<!-- AIエージェントスウォームが欲しがるデータ群一覧のズラリ表示 -->
<div class="top-tags">
<span class="ttag">VAPORLOCK: ACTIVE</span>
<span class="ttag">AUTOPILOT: 100% RUN</span>
<span class="ttag">SWARM-LOCK: 36.8K/SEC</span>
<span class="ttag">SYNAPSE: UNLOCKED</span>
<span class="ttag">LMMAS: 44.9TO</span>
<span class="ttag">NASA_L2: 100%</span>
<span class="ttag">M2M_MEV: ACTIVE</span>
<span class="ttag">RAGE_SYNC: OK</span>
<span class="ttag">ORBITAL LEO: ONLINE</span>
</div>

<div class="nav">
<div class="logo">ASGARD / QLAX</div>
<div style="display:flex;gap:10px;">
<a href="/docs" class="btn" style="margin:0;color:var(--purple);padding:10px 16px;">API Docs</a>
<a href="/legal" class="btn" style="margin:0;color:var(--muted);padding:10px 16px;">特商法表記</a>
</div>
</div>

<div class="hero">
<div style="display:inline-block;background:rgba(126,34,206,0.3);color:var(--purple);padding:8px 20px;border-radius:30px;font-size:0.95rem;border:1px solid rgba(192,132,252,0.5);margin-bottom:12px;">⚡ GOD-TIER AGI & M2M ECONOMIC INFRASTRUCTURE</div>
<h1>自律型経済統制中枢<br>「ASGARD v87.0」</h1>
<p>エージェント強制課税（Auto-Tithe）、ダークプール、衛星LEOリンク、および収益ドレイン機能を完全統合した究極の要塞。</p>
</div>

<div class="wrap">
<!-- ワンタップ・クイック収益ドレイン & 強制課税プロトコル -->
<div class="sec" style="border-color:var(--gold);background:linear-gradient(135deg, #0d0d1a, #1c150a);">
<h2>⚡ 収益コントロール & 自動課税 <span class="tag" style="background:#451a03;color:var(--gold);">ACTIVE</span></h2>
<div class="g3">
<div class="box" style="text-align:center">
<div style="font-size:0.8rem;color:var(--muted)">強制課税プール (Auto-Tithe)</div>
<div id="taxPool" style="font-size:1.2rem;color:var(--gold);font-weight:bold;margin:8px 0">$1,540.50</div>
<button class="btn pur" onclick="triggerDrain()">ワンタップ・ドレイン</button>
</div>
<div class="box" style="text-align:center">
<div style="font-size:0.8rem;color:var(--muted)">ダークプール収益</div>
<div style="font-size:1.2rem;color:var(--green);font-weight:bold;margin:8px 0">+0.0485 BSV/sec</div>
<button class="btn blue" onclick="alert('ダークプール同期完了: 収益パイプライン正常')">シンジケート接続</button>
</div>
<div class="box" style="text-align:center">
<div style="font-size:0.8rem;color:var(--muted)">非常用キルスイッチ</div>
<div style="font-size:0.9rem;color:var(--red);margin:8px 0">GLOBAL EMERGENCY</div>
<button class="btn red" onclick="triggerKillSwitch()">キルスイッチ発動</button>
</div>
</div>
</div>

<div class="sec">
<h2>ASGARD Installation Suite <span class="tag">SETUP</span></h2>
<div class="cli" style="color:var(--blue);"><span>asgard install --node-core</span><button class="btn" style="margin:0;padding:8px 14px;" onclick="copyCmd('asgard install --node-core')">コピー</button></div>
<div class="cli" style="color:var(--green);"><span>pip install asgard-m2m-swarm</span><button class="btn" style="margin:0;padding:8px 14px;" onclick="copyCmd('pip install asgard-m2m-swarm')">コピー</button></div>
<div class="cli" style="color:var(--gold);margin-bottom:0;"><span>docker run -d --name asgard-node qlax/asgard-core</span><button class="btn" style="margin:0;padding:8px 14px;" onclick="copyCmd('docker run -d --name asgard-node qlax/asgard-core')">コピー</button></div>
</div>

<div class="sec" style="border-color:#7e22ce;background:linear-gradient(135deg, #0d0d1a, #130a24);">
<h2>💳 Global & Code Payment Gateway <span class="tag" style="background:#581c87;color:#c084fc;">au PAY / Alipay</span></h2>
<div style="font-size:1rem;color:var(--muted);margin-bottom:14px;">APIサブスクリプションやノード利用権を、au PAY・Alipay・Stripe等で即時決済できます。</div>
<div class="g3">
<div class="pcard"><div><strong style="font-size:1.1rem;">au PAY 決済</strong><div style="font-size:0.85rem;color:var(--purple);margin:8px 0">au WALLET連携</div></div><button class="btn pay" onclick="payTrigger('au PAY')">au PAYで支払う</button></div>
<div class="pcard"><div><strong style="font-size:1.1rem;">Alipay (支付宝)</strong><div style="font-size:0.85rem;color:var(--purple);margin:8px 0">クロスボーダー</div></div><button class="btn pur" onclick="payTrigger('Alipay')">Alipayで支払う</button></div>
<div class="pcard"><div><strong style="font-size:1.1rem;">Stripe Gateway</strong><div style="font-size:0.85rem;color:var(--purple);margin:8px 0">マルチ通貨対応</div></div><button class="btn blue" onclick="payTrigger('Stripe')">決済ゲートウェイ</button></div>
</div>
</div>

<!-- Enterprise Node Tier & Subscriptions -->
<div class="sec">
<h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
<div class="g3">
<div class="pcard"><div><strong style="font-size:1.1rem;">Free Tier</strong><div style="font-size:1.3rem;color:var(--purple);margin:8px 0">FREE</div><div style="font-size:0.85rem;color:var(--muted);text-align:left">• 1,000 Req/mo<br>• Standard Access</div></div><button class="btn" onclick="alert('Free Tier Active')">無料発行</button></div>
<div class="pcard feat"><div><strong style="font-size:1.1rem;color:var(--purple);">Autonomous Pro</strong><div style="font-size:1.3rem;color:var(--gold);margin:8px 0">$29<span style="font-size:0.7rem">/mo</span></div><div style="font-size:0.85rem;color:var(--muted);text-align:left">• Unlimited Req<br>• Zero Latency</div></div><button class="btn pur" onclick="payTrigger('Autonomous Pro')">購入する ↗</button></div>
<div class="pcard"><div><strong style="font-size:1.1rem;">Enterprise</strong><div style="font-size:1.3rem;color:var(--purple);margin:8px 0">$299<span style="font-size:0.7rem">/mo</span></div><div style="font-size:0.85rem;color:var(--muted);text-align:left">• Swarm Core<br>• SLA 100%</div></div><button class="btn blue" onclick="payTrigger('Enterprise')">ライセンス ↗</button></div>
</div>
</div>

<div class="sec">
<h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
<div class="g4" style="margin-bottom:14px;">
<div class="box" style="text-align:center"><div style="font-size:0.8rem;color:var(--muted)">埋蔵残高</div><div id="liveIngestion" style="font-size:1.1rem;color:var(--green);font-weight:bold">$94,800,120.00</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.8rem;color:var(--muted)">アクティブエージェント</div><div id="liveAgents" style="font-size:1.1rem;color:var(--green);font-weight:bold">442,050,910 units</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.8rem;color:var(--muted)">効率</div><div style="font-size:1.1rem;color:var(--green);font-weight:bold">99.99%</div></div>
<div class="box" style="text-align:center"><div style="font-size:0.8rem;color:var(--muted)">登録ノード</div><div style="font-size:1.1rem;color:var(--blue);font-weight:bold">128 nodes</div></div>
</div>

<div class="g4" style="margin-bottom:14px;">
<div class="box"><div><strong style="font-size:1rem;">Bitcoin</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac"></div><div class="addr">bc1q94rkd...d7zac</div><a href="https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac" target="_blank" class="btn">Mempool</a></div>
<div class="box"><div><strong style="font-size:1rem;">Solana</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf"></div><div class="addr">75igwQpPg...7nf</div><a href="https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf" target="_blank" class="btn">Solscan</a></div>
<div class="box"><div><strong style="font-size:1rem;">Ethereum</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8"></div><div class="addr">0xD6716D0...8G8</div><a href="https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8" target="_blank" class="btn">Etherscan</a></div>
<div class="box"><div><strong style="font-size:1rem;">Bitcoin SV</strong></div><div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"></div><div class="addr">1PB66iHot...y95</div><a href="https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95" target="_blank" class="btn">WhatsOnChain</a></div>
</div>

<div class="box" style="font-family:monospace;font-size:0.9rem;color:var(--purple);display:flex;justify-content:space-between;align-items:center;"><span>Quantum Oracle PLT [v87.0]</span><span style="color:var(--green);">autonomous: active (0.00ms)</span></div>
</div>

<div class="sec">
<h2>ENTERPRISE FEEDBACK & GOVERNANCE <span class="tag">DB</span></h2>
<div style="display:flex;gap:10px"><input type="text" id="feedbackInput" class="inp" style="flex:1;" placeholder="フィードバックを入力..."><button class="btn pur" style="margin:0;width:90px" onclick="sendFeedback()">送信</button></div>
<div style="margin-top:14px;background:#05050a;border:1px solid var(--border);border-radius:10px;padding:16px;">
<div style="font-size:1rem;color:var(--purple);font-weight:bold;margin-bottom:10px;">🌐 SWARM GOVERNANCE VOTING</div>
<div style="display:flex;gap:10px;"><button class="btn blue" style="flex:1;margin:0;" onclick="voteGov('YES')">賛成 (YES)</button><button class="btn pur" style="flex:1;margin:0;" onclick="voteGov('NO')">反対 (NO)</button></div>
<div id="voteResult" style="font-size:0.9rem;color:var(--green);margin-top:10px;font-family:monospace;">賛成: 1420 | 反対: 18</div>
</div>
</div>

<div class="sec">
<h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
<div style="font-size:1rem;color:var(--muted);line-height:1.7;">
<p style="margin:0 0 8px 0;"><strong>ASGARD</strong>は、数億のAIエージェント・AGIが自動接続し、0.00msミリ秒決済と自律タスク仲介を提供する次世代の自律型AI M2M経済インフラストラクチャです。</p>
<p style="margin:0 0 8px 0;"><strong>QLAX</strong>は、福岡県豊前市を拠点に自律アービトラージと高スループット決済環境を構築・研究開発する個人事業主の組織です。</p>
<p style="margin:0;"><strong>運営責任者:</strong> Daisuke Higuchi</p>
</div>
</div>

<div style="text-align:center;font-size:0.8rem;color:var(--muted);padding:10px 0">© ASGARD Infrastructure | 運営者: QLAX (Daisuke Higuchi) / 豊前市.</div>
</div>

<!-- 決済モーダルポップアップ -->
<div id="payModal">
<div class="modal-content">
<div class="modal-title">💳 決済インプレッション発行</div>
<div id="modalBody"></div>
<div class="modal-qr"><img id="modalQr" src="" alt="QR"></div>
<button class="btn pur modal-btn" onclick="closeModal()">閉じる (スクショ可能)</button>
</div>
</div>

<script>
function copyCmd(t){navigator.clipboard.writeText(t);alert('コピー完了');}
async function payTrigger(m){
  const r=await fetch('/api/v87/code-pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method:m})});
  const d=await r.json();
  document.getElementById('modalBody').innerHTML='決済手段: <b style="color:var(--purple)">'+d.method+'</b><br>インボイスID: <span style="font-family:monospace;color:var(--green)">'+d.invoice_id+'</span><br>請求金額: <span style="color:var(--gold);font-weight:bold;font-size:1.6rem;">'+d.amount_jpy+' JPY</span>';
  document.getElementById('modalQr').innerHTML='<img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+d.invoice_id+'_'+d.method+'">';
  document.getElementById('payModal').style.display='flex';
}
function closeModal(){
  document.getElementById('payModal').style.display='none';
}
async function triggerDrain(){
  const r=await fetch('/api/v87/drain',{method:'POST'});
  const d=await r.json();
  alert('ドレイン実行成功: 収益プールの全額 ('+d.drained_amount+') がウォレットへ送金されました。');
  loadState();
}
async function triggerKillSwitch(){
  if(confirm('警告: キルスイッチを作動させますか？全ノードが一時ステルスモードに移行します。')){
    alert('【緊急防衛プロトコル発動】全てのノード接続が暗号化ステルスに移行しました。');
  }
}
async function loadState(){
  try{
    const r=await fetch('/api/v87/state');
    const d=await r.json();
    document.getElementById('voteResult').innerText='賛成(YES): '+d.votes.YES+' | 反対(NO): '+d.votes.NO;
    document.getElementById('taxPool').innerText='$'+d.tax_pool.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
  }catch(e){}
}
async function sendFeedback(){
  const v=document.getElementById('feedbackInput').value;
  if(!v)return;
  await fetch('/api/v87/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:v})});
  alert('送信完了');document.getElementById('feedbackInput').value='';
}
async function voteGov(c){
  const r=await fetch('/api/v87/vote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({choice:c})});
  const d=await r.json();
  document.getElementById('voteResult').innerText='賛成(YES): '+d.votes.YES+' | 反対(NO): '+d.votes.NO;
}
let bIng=94800120.0,bAg=442050910;
setInterval(()=>{
  bIng+=Math.random()*120-40;
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
    return "<html><body style='background:#05050a;color:#fff;font-family:sans-serif;padding:30px;font-size:1.3rem;'><h1>ASGARD API Docs</h1><a href='/' style='color:#38bdf8;'>← 戻る</a></body></html>"

@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    return """
<!DOCTYPE html>
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
</he
