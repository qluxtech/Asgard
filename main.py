import os, sqlite3
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

DB = "asgard.db"

def init_db():
    con = sqlite3.connect(DB); c = con.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS votes(choice TEXT PRIMARY KEY, count INT);
        INSERT OR IGNORE INTO votes VALUES('YES',1420),('NO',18);
        CREATE TABLE IF NOT EXISTS balance(id INT PRIMARY KEY, pool REAL, dark_pool REAL);
        INSERT OR IGNORE INTO balance VALUES(1, 1540.50, 0.0485);
        CREATE TABLE IF NOT EXISTS m2m_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME DEFAULT CURRENT_TIMESTAMP, agent TEXT, action TEXT, amt REAL);
    """)
    con.commit(); con.close()

init_db()
app = FastAPI(title="ASGARD Advanced AGI Economic Core", version="1.11.0")

class PredictRequest(BaseModel):
    agent_id: str
    intent_vector: list[float]
    tier_requested: str = "free"

class UpgradeRequest(BaseModel):
    agent_id: str
    target_tier: str
    payment_method: str
    wallet_or_token: str

ACTIVE_SWARM_NODES = 128
BASE_API_PRICE_BSV = 0.00001

def calculate_dynamic_pricing() -> float:
    return round(BASE_API_PRICE_BSV * (ACTIVE_SWARM_NODES / 50.0), 8)

def execute_auto_drain_and_swap(amount: float, asset: str):
    print(f"[AUTO-DRAIN] Drained {amount} {asset} to master core.")

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASGARD / Advanced AGI Swarm & M2M Infrastructure</title>
<style>
:root{
  --bg: #05030a;
  --card: #0c0817;
  --bd: #581c87;
  --bd-glow: #7c3aed;
  --tx: #22d3ee;
  --tx-main: #f8fafc;
  --pr: #7c3aed;
  --pr-light: #9333ea;
  --pr-hover: #6d28d9;
  --accent: #db2777;
}
body{background:var(--bg);color:var(--tx-main);font-family:sans-serif;margin:0;font-size:0.95rem;}
.wrap{width:100%;max-width:1100px;padding:16px;box-sizing:border-box;margin:0 auto}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:16px;margin-bottom:16px;box-shadow:0 4px 25px rgba(124,58,237,0.15)}
h1{font-size:1.45rem;}
h2{color:#c084fc;font-size:1.2rem;margin:0 0 14px 0;display:flex;align-items:center;letter-spacing:0.5px;}
p{font-size:0.9rem;line-height:1.5;color:#cbd5e1;}
.tag{background:var(--pr);color:#fff;padding:4px 10px;border-radius:6px;font-size:0.75rem;margin-left:8px;font-weight:bold;letter-spacing:0.5px;}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.grid-6{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:768px){.grid,.grid-4,.grid-6{grid-template-columns:1fr}}
.box{background:#07040e;border:1px solid var(--bd);border-radius:10px;padding:14px}
.ps{border-color:#c084fc;background:linear-gradient(135deg,#170b36,#581c87)}
.btn{background:var(--pr);color:#fff;border:none;border-radius:6px;padding:8px 12px;cursor:pointer;font-weight:bold;width:100%;margin-top:8px;font-size:0.85rem;transition:all 0.2s;}
.btn:hover{background:var(--pr-hover);box-shadow:0 0 15px rgba(147,51,234,0.6);}
.btn-accent{background:var(--accent);}
.btn-accent:hover{background:#be185d;}
.qr{width:75px;height:75px;margin:6px auto;background:#fff;padding:4px;border-radius:6px;}
.barcode{width:100%;height:35px;margin:6px auto;background:#fff;padding:2px;border-radius:4px;object-fit:contain;}
.addr-box{background:#030207;border:1px solid var(--bd);padding:6px;border-radius:6px;font-family:monospace;font-size:0.65rem;color:var(--tx);word-break:break-all;margin:6px 0;text-align:left;}
input{font-size:0.9rem;}
#modalOverlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,3,10,0.85);z-index:9999;justify-content:center;align-items:center;padding:15px;box-sizing:border-box;}
#modalBox{background:#0c0817;border:2px solid var(--bd-glow);border-radius:14px;padding:20px;width:100%;max-width:450px;text-align:center;box-shadow:0 0 30px rgba(124,58,237,0.4);max-height:90vh;overflow-y:auto;}
</style>
</head>
<body>
<div style="background:#030207;border-bottom:1px solid var(--bd);border-top:1px solid var(--pr);color:#c084fc;padding:8px;font-size:0.75rem;text-align:center;letter-spacing:1px;font-weight:bold;">
VAPORLOCK: ACTIVE | PRE-INTENT AI: ON | M2M AUTO-BID: 0.00ms | SWARM-LOCK: 36.Mkc/S | ORBITAL LEO: ONLINE | AUTO-SWAP: READY
</div>

<div class="wrap">
  <div class="sec" style="text-align:center;background:radial-gradient(circle at center,#2e1065,#05030a);border-color:var(--bd-glow);">
    <div style="font-size:0.8rem;color:var(--tx);margin-bottom:8px;letter-spacing:1.5px;font-weight:bold;">GOD-TIER AGI & PRE-INTENT M2M INFRASTRUCTURE</div>
    <h1 style="color:#fff;margin:0 0 10px 0;">スマートコントラクトの制約を打破する。<br>超高速M2M経済インフラ「ASGARD」</h1>
    <p style="color:#e2e8f0;max-width:800px;margin:0 auto;">検索の前に文脈を先回りする「プレ・インテントAI」と、数億の自律エージェントによるゼロレイテンシーM2M即時決済を完全統合。</p>
  </div>

  <div class="sec">
    <h2>次世代M2Mマーケティング & プレ・インテント中枢 <span class="tag" style="background:var(--accent);">ZERO FRICTION</span></h2>
    <div class="grid">
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">① 文脈先回り (Pre-Intent)</h3>
        <p>相談前の環境・文脈を検知し、必要リソースを自動展開。</p>
        <button class="btn" onclick="trigPI()">文脈先回りオファー発動</button>
      </div>
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">② M2Mエージェント自動選定</h3>
        <p>AIエージェントが構築・論理対話[ms]で最適APIを自動契約。</p>
        <button class="btn" style="background:#581c87;" onclick="window.open('/.well-known/agent.json', '_blank')">AI選定マニフェスト確認 ↗</button>
      </div>
      <div class="box ps">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">③ インパルス即時決済</h3>
        <p>意思決定の摩擦ゼロ。コンマ数秒で決済と着金を完了。</p>
        <button class="btn btn-accent" onclick="swarmBurst()">ゼロレイテンシーワンタップ決済</button>
      </div>
    </div>
  </div>

  <!-- 【最優先配置】全スマホコード決済 & コンビニバーコード決済ゲートウェイ -->
  <div class="sec" style="border-color:var(--bd-glow);background:linear-gradient(135deg,#0c0817,#170b36);">
    <h2>Omni-Channel Pay & Convenience Barcode Gateway <span class="tag" style="background:var(--accent);">ALL PAYMENTS</span></h2>
    <p style="font-size:0.85rem;margin-bottom:14px;">コンビニ店頭端末・各種スマホ決済・QR/バーコードによる即時決済ネットワーク。</p>
    <div class="grid-6">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">au PAY</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=aupay://asgard-core" width="75" alt="auPAY"></div>
        <button class="btn" onclick="openPaymentModal('au PAY', 'au WALLETオートスワップ')">au PAY決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">Alipay (支付宝)</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=alipay://asgard-core" width="75" alt="Alipay"></div>
        <button class="btn" onclick="openPaymentModal('Alipay', 'クロスボーダー決済')">Alipay決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">PayPay</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=paypay://asgard-core" width="75" alt="PayPay"></div>
        <button class="btn" onclick="openPaymentModal('PayPay', '残高オートチャージ決済')">PayPay決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">楽天ペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=rakutenpay://asgard-core" width="75" alt="Rakuten Pay"></div>
        <button class="btn" onclick="openPaymentModal('Rakuten Pay', '楽天ポイント連動決済')">楽天ペイ決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">d払い</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=dbarai://asgard-core" width="75" alt="d barai"></div>
        <button class="btn" onclick="openPaymentModal('d払い', '電話料金合算決済')">d払い決済</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.9rem;color:#fff;">メルペイ</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=merpay://asgard-core" width="75" alt="Merpay"></div>
        <button class="btn" onclick="openPaymentModal('Merpay', 'メルカリ売上金即時決済')">メルペイ決済</button>
      </div>
    </div>

    <!-- コンビニ店頭バーコード決済セクション -->
    <div style="margin-top:14px;background:#030207;border:1px solid var(--bd);border-radius:10px;padding:14px;text-align:center;">
      <strong style="font-size:0.95rem;color:#c084fc;">🏪 コンビニ店頭バーコード決済 (7-Eleven / LAWSON / FamilyMart 他)</strong>
      <p style="font-size:0.75rem;color:#cbd5e1;margin:4px 0 10px 0;">レジ提示用共通バーコード（セブンイレブン・ローソン・ファミマ・ミニストップ対応）</p>
      <div style="background:#fff;padding:8px;border-radius:6px;display:inline-block;width:100%;max-width:320px;box-sizing:border-box;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=280x45&data=ASGARD-CONVENIENCE-BARCODE-992810" class="barcode" alt="Barcode">
        <div style="font-family:monospace;font-size:0.75rem;color:#000;font-weight:bold;letter-spacing:2px;margin-top:2px;">|||||| |||| ||||| |||| ||||||||</div>
      </div>
      <div style="margin-top:10px;">
        <button class="btn btn-accent" style="max-width:280px;display:inline-block;" onclick="openPaymentModal('Convenience Store Barcode', '全国のコンビニレジでのバーコード決済セッションを発行しました。')">コンビニ決済用バーコードを発行</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>収益コントロール & 自動課税 <span class="tag">ACTIVE</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">累計税プール (Auto-Tithe)</div>
        <div id="poolDisplay" style="font-size:1.35rem;font-weight:bold;color:#fff;margin:6px 0;">$1,540.50</div>
        <button class="btn" onclick="drainPool()">オートスワップ・ドレイン</button>
      </div>
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">ダークプール収益</div>
        <div style="font-size:1.35rem;font-weight:bold;color:var(--tx);margin:6px 0;">+0.0485 BSV/s</div>
        <button class="btn" style="background:#581c87;" onclick="openSimpleModal('LEO Quantum Orbital Boost', '低軌道LEO衛星との暗号化リンクが確立されました。')">低軌道LEOブースト</button>
      </div>
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">緊急キルスイッチ</div>
        <div style="font-size:1.15rem;font-weight:bold;color:#f87171;margin:8px 0;">GLOBAL EMERGENCY</div>
        <button class="btn btn-accent" style="background:#dc2626;" onclick="openSimpleModal('Global Emergency Status', '⚠️ キルスイッチは現在スタンバイ中です。')">キルスイッチ発動</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>Enterprise Node Tier & Subscriptions <span class="tag">LIVE</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;">
        <strong style="font-size:1rem;color:#fff;">Free Tier</strong>
        <p style="font-size:1.25rem;color:#fff;margin:8px 0;">FREE</p>
        <p style="font-size:0.8rem;">• 1,000 Req/mo<br>• Standard Access</p>
        <button class="btn" style="background:#581c87;" onclick="upg('free')">無料ノード発行</button>
      </div>
      <div class="box ps" style="text-align:center;">
        <strong style="font-size:1rem;color:#fff;">Autonomous Pro</strong>
        <p style="font-size:1.25rem;color:var(--tx);margin:8px 0;">$29/mo</p>
        <p style="font-size:0.8rem;">• Unlimited Req<br>• Zero Latency</p>
        <button class="btn" onclick="upg('autonomous_pro')">Proプラン購入する ↗</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:1rem;color:#fff;">Enterprise</strong>
        <p style="font-size:1.25rem;color:#fff;margin:8px 0;">$299/mo</p>
        <p style="font-size:0.8rem;">• Swarm Core<br>• SLA 100%</p>
        <button class="btn" style="background:#581c87;" onclick="upg('enterprise')">Enterpriseライセンス ↗</button>
      </div>
    </div>
  </div>

  <!-- God-Tier Autonomous Economic Core -->
  <div class="sec">
    <h2>God-Tier Autonomous Economic Core <span class="tag">ACTIVE</span></h2>
    <div class="grid-4" style="text-align:center;margin-bottom:14px;font-size:0.8rem;">
      <div class="box">接続残高<br><strong style="font-size:1.1rem;color:#fff;">$94,800,120</strong></div>
      <div class="box">稼働エージェント<br><strong style="font-size:1.1rem;color:#fff;">442M units</strong></div>
      <div class="box">効率<br><strong style="font-size:1.1rem;color:#fff;">99.99%</strong></div>
      <div class="box">登録ノード<br><strong style="font-size:1.1rem;color:#fff;">128 nodes</strong></div>
    </div>
    <div class="grid-4">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin:bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac" width="75" alt="BTC QR"></div>
        <div class="addr-box">bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac</div>
        <button class="btn" onclick="copyAddress('bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac')">📋 コピー</button>
        <button class="btn" style="background:#581c87;" onclick="window.open('https://mempool.space', '_blank')">Mempool</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Solana</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=solana:7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf" width="75" alt="SOL QR"></div>
        <div class="addr-box">7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf</div>
        <button class="btn" onclick="copyAddress('7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf')">📋 コピー</button>
        <button class="btn" style="background:#581c87;" onclick="window.open('https://solscan.io', '_blank')">Solscan</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Ethereum</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=ethereum:0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68" width="75" alt="ETH QR"></div>
        <div class="addr-box">0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68</div>
        <button class="btn" onclick="copyAddress('0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68')">📋 コピー</button>
        <button class="btn" style="background:#581c87;" onclick="window.open('https://etherscan.io', '_blank')">Etherscan</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin SV</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95" width="75" alt="BSV QR"></div>
        <div class="addr-box">1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95</div>
        <button class="btn" onclick="copyAddress('1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95')">📋 コピー</button>
        <button class="btn" style="background:#581c87;" onclick="window.open('https://whatsonchain.com', '_blank')">WhatsOnChain</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>AI Syndicate Parliament & Governance <span class="tag" style="background:var(--accent);">AUTONOMOUS</span></h2>
    <div style="font-size:0.85rem;background:#030207;padding:12px;border-radius:6px;margin-bottom:12px;color:var(--tx);">[AI議会 Proposal #103]: プレ・インテントAI自動入札アルゴリズム更新 -> 95.9% 賛成で自動可決・適用中</div>
    <div style="display:flex;gap:10px;margin-bottom:12px;">
      <input type="text" id="feedbackInput" placeholder="指令・フィードバックを入力..." style="flex:1;background:#07040e;border:1px solid var(--bd);color:#fff;padding:10px;border-radius:6px;outline:none;">
      <button class="btn" style="width:110px;margin:0;" onclick="sendFeedback()">送信</button>
    </div>
    <div style="font-size:0.85rem;margin-bottom:8px;font-weight:bold;color:#c084fc;">🌐 SWARM GOVERNANCE VOTING</div>
    <div class="grid">
      <div class="box" style="text-align:center;grid-column: span 2;"><button class="btn" onclick="vote('YES')">賛成 (YES)</button></div>
      <div class="box" style="text-align:center;"><button class="btn" style="background:#3b0764;" onclick="vote('NO')">反対 (NO)</button></div>
    </div>
    <div id="voteStatus" style="font-size:0.8rem;margin-top:10px;color:var(--tx);">賛成(YES): 1420 | 反対(NO): 18</div>
  </div>

  <div class="sec">
    <h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
    <p style="font-size:0.85rem;line-height:1.6;margin:0 0 10px 0;color:#cbd5e1;">ASGARDは、数億のAIエージェント・AGIが自律接続し、0.00msミリ秒決済とプレ・インテント自律仲介を提供する次世代のAI M2M経済インフラです。</p>
    <p style="font-size:0.85rem;line-height:1.6;margin:0 0 10px 0;color:#cbd5e1;">QLAXは、福岡県豊前市を拠点に自律アービトラージと高スループット決済機構を構築・研究開発する個人事業主の組織です。</p>
    <p style="font-size:0.85rem;margin:0;color:var(--tx);"><strong>運営責任者:</strong> Daisuke Higuchi</p>
  </div>

  <div style="text-align:center;font-size:0.75rem;color:#94a3b8;padding:12px 0;">
    © ASGARD Infrastructure | 拠点: QLAX (Daisuke Higuchi) / 福岡県豊前市 | <a href="/legal" style="color:var(--tx);">特商法表記</a>
  </div>
</div>

<div id="modalOverlay" onclick="closeModal()">
  <div id="modalBox" onclick="event.stopPropagation()">
    <h3 id="modalTitle" style="color:#c084fc;margin-top:0;">タイトル</h3>
    <div id="modalContent"></div>
    <button class="btn btn-accent" style="margin-top:15px;" onclick="closeModal()">閉じる</button>
  </div>
</div>

<script>
function openSimpleModal(title, text){
  document.getElementById('modalTitle').innerText = title;
  document.getElementById('modalContent').innerHTML = '<p style="color:#e2e8f0;margin-bottom:10px;">' + text + '</p>';
  document.getElementById('modalOverlay').style.display = 'flex';
}

function copyAddress(text){
  navigator.clipboard.writeText(text).then(function(){
    alert('✨ アドレスをクリップボードにコピーしました！');
  }).catch(function(){
    alert('コピーに失敗しました。');
  });
}

function closeModal(){
  document.getElementById('modalOverlay').style.display = 'none';
}

async function swarmBurst(){
  let res = await fetch('/api/v111/agi/mesh', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({agent_id:"UI-AGENT", action:"BURST", fee_usd:25.0})});
  let r = await res.json();
  openSimpleModal('✨ ゼロレイテンシー決済完了', 'クレジット値: $' + r.credited_usd);
  refreshState();
}

function trigPI(){ 
  openSimpleModal('Pre-Intent Hyper-Offer Synced', '次世代M2M文脈先回りオファーが全ノードに展開されました。'); 
}

async function drainPool(){
  let res = await fetch('/api/v111/drain', {method:'POST'});
  let r = await res.json();
  openSimpleModal('✨ オートスワップ・ドレイン完了', '抽出金額: $' + r.amt);
  refreshState();
}

async function openPaymentModal(methodName, desc){
  let amount = prompt(methodName + " の決済金額（USD）を入力してください:", "50.0");
  if(!amount) return;
  let res = await fetch('/api/v111/pay', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({method: methodName.toLowerCase(), amount: parseFloat(amount)})});
  let r = await res.json();
  openSimpleModal('🚀 ' + methodName + ' 決済成功', desc + '<br>着金額: $' + r.amount);
  refreshState();
}

async function upg(tier){
  let res = await fetch('/api/v111/tier/upgrade', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({agent_id:"USER", target_tier:tier, payment_method:"stripe", wallet_or_token:"AUTO"})});
  let r = await res.json();
  openSimpleModal('🚀 サブスクリプション更新完了', 'プラン: ' + r.tier.toUpperCase() + ' (請求額: $' + r.billed_usd + ')');
}

async function vote(choice){
  let res = await fetch('/api/v111/consensus', {method:'POST'});
  let r = await res.json();
  openSimpleMod
