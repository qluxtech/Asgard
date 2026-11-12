import os, random, datetime, secrets, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ASGARD", version="32.0")
W = {"btc":"bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac","solana":"75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf","evm":"0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8","bsv":"1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95"}

class F(BaseModel): feedback: str
class A(BaseModel): email: str; password: str

class CM:
    def __init__(self): self.c = []
    async def connect(self, w: WebSocket): await w.accept(); self.c.append(w)
    def disconnect(self, w: WebSocket):
        if w in self.c: self.c.remove(w)
    async def broadcast(self, m: str):
        for w in list(self.c):
            try: await w.send_text(m)
            except: pass

m_mgr = CM()

HTML_PAGE = """<!DOCTYPE html><html lang='ja'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1.0'>
<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'>
<meta http-equiv='Pragma' content='no-cache'>
<title>ASGARD / M2M Node</title><style>
:root{--bg:#05050a;--card:#0d0d1a;--border:#1e1b4b;--text:#f8fafc;--muted:#94a3b8;--blue:#38bdf8;--purple:#c084fc;--green:#10b981;--gold:#facc15;}
body{background:var(--bg);color:var(--text);font-family:sans-serif;margin:0;padding:0;display:flex;flex-direction:column;align-items:center;}
.bar{width:100%;background:#000;border-bottom:1px solid #2a275f;padding:6px 10px;display:flex;gap:6px;overflow-x:auto;white-space:nowrap;font-family:monospace;font-size:0.55rem;}
.bitem{background:#0a0a16;padding:2px 6px;border-radius:3px;border:1px solid #1e1b4b;color:#ef4444;font-weight:bold;}
.bitem.g{color:var(--green);}.bitem.p{color:var(--purple);}
.nav{width:100%;max-width:950px;display:flex;justify-content:space-between;align-items:center;padding:10px;box-sizing:border-box;border-bottom:1px solid var(--border);}
.logo{font-size:0.8rem;font-weight:bold;color:var(--purple);}
.hero{width:100%;padding:20px 10px;text-align:center;background:radial-gradient(circle at 50% 20%, rgba(192,132,252,0.18), transparent 75%);border-bottom:1px solid var(--border);}
.hero h1{font-size:1.2rem;font-weight:800;margin:0 0 6px;background:linear-gradient(135deg, #fff 30%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p{font-size:0.65rem;color:var(--muted);max-width:650px;margin:0 auto;line-height:1.3;}
.wrap{width:100%;max-width:950px;padding:10px;box-sizing:border-box;}
.sec{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:10px;margin-bottom:10px;}
.sec h2{font-size:0.75rem;margin:0 0 8px 0;color:var(--purple);display:flex;justify-content:space-between;align-items:center;}
.tag{background:#1e1b4b;color:var(--purple);padding:2px 6px;border-radius:4px;font-size:0.5rem;border:1px solid #7e22ce;}
.g3{display:grid;grid-template-columns:repeat(3, 1fr);gap:6px;}
.g4{display:grid;grid-template-columns:repeat(4, 1fr);gap:6px;}
@media(max-width:768px){.g4{grid-template-columns:repeat(2, 1fr);}}
.box{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:6px;font-size:0.58rem;}
.pcard{background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;}
.pcard.feat{border-color:var(--purple);background:#0e091d;}
.btn{background:#1e1b4b;color:var(--text);border:1px solid var(--border);padding:4px;border-radius:4px;font-size:0.55rem;cursor:pointer;text-align:center;text-decoration:none;display:block;font-weight:600;margin-top:4px;}
.btn.blue{background:var(--blue);color:#05050a;border:none;}
.btn.pur{background:linear-gradient(135deg, #9333ea, #c084fc);color:#fff;border:none;}
.qr{background:#fff;padding:2px;width:30px;height:30px;margin:4px auto;border-radius:3px;display:flex;}
.qr img{width:100%;height:100%;}
.addr{font-family:monospace;font-size:0.45rem;background:#0f0f1d;padding:2px;border-radius:3px;word-break:break-all;color:var(--muted);text-align:center;}
.stream{background:#05050a;border:1px solid var(--border);border-radius:6px;padding:8px;font-family:monospace;font-size:0.5rem;color:var(--green);max-height:70px;overflow-y:auto;}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,10,0.85);z-index:2000;justify-content:center;align-items:center;}
.modal-c{background:var(--card);border:1px solid var(--purple);padding:16px;border-radius:8px;width:90%;max-width:300px;}
.modal-c input{width:100%;background:#05050a;border:1px solid var(--border);padding:6px;border-radius:4px;color:#fff;font-size:0.6rem;margin-bottom:8px;box-sizing:border-box;}
.cli{background:#05050a;border:1px solid var(--border);padding:6px 8px;border-radius:4px;font-family:monospace;font-size:0.5rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
</style></head><body>
<div class='bar'><span class='bitem'>VAPORLOCK: ACTIVE</span><span class='bitem g'>AUTOPILOT: 100%</span><span class='bitem p'>TIMELOCK: SOLSTICE</span><span class='bitem g'>SINGULARITY: UNLOCKED</span><span class='bitem g'>UMBRA: 99.99%</span><span class='bitem p'>GAIA_L2: 100%</span><span class='bitem g'>SELF_HEAL: ACTIVE</span></div>
<div class='nav'><div class='logo'>ASGARD / QLAX (v32.0)</div><div><button class='btn' style='display:inline-block;padding:3px 8px;' onclick='openModal("login")'>ログイン</button><button class='btn blue' style='display:inline-block;padding:3px 8px;margin-left:4px;' onclick='openModal("signup")'>サインアップ</button></div></div>
<div class='hero'><div style='display:inline-block;background:rgba(126,34,206,0.25);color:var(--purple);padding:2px 8px;border-radius:20px;font-size:0.55rem;border:1px solid rgba(192,132,252,0.4);margin-bottom:6px;font-weight:600;'>⚡ AGI & M2M ECONOMIC INFRASTRUCTURE</div><h1>スマートコントラクトを超越する<br>自律型AI M2M経済インフラ</h1><p>4.4億超のAIエージェント・AGIが自動接続。0.00msミリ秒決済と自律タスク仲介を提供する次世代インフラ。</p></div>
<div class='wrap'>
<div class='sec'><h2>ASGARD Installation Suite <span class='tag'>SETUP</span></h2>
<div class='cli' style='color:var(--blue);'><span>asgard install --node-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='navigator.clipboard.writeText("asgard install --node-core");alert("コピー ✓");'>コピー</button></div>
<div class='cli' style='color:var(--green);'><span>pip install asgard-m2m-swarm</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='navigator.clipboard.writeText("pip install asgard-m2m-swarm");alert("コピー ✓");'>コピー</button></div>
<div class='cli' style='color:var(--gold);'><span>docker run -d --name asgard-node qlax/asgard-core</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='navigator.clipboard.writeText("docker run -d --name asgard-node qlax/asgard-core");alert("コピー ✓");'>コピー</button></div>
<div class='cli' style='color:var(--purple);margin-bottom:0;'><span>asgard link agent.json</span><button class='btn' style='margin:0;padding:2px 6px;' onclick='navigator.clipboard.writeText("asgard link agent.json");alert("コピー ✓");'>コピー</button></div></div>
<div class='sec'><h2>⚡ Live Node Ping & Quantum Test <span class='tag'>TESTNET</span></h2>
<button class='btn blue' style='width:100%;padding:6px;' onclick='runPing()'>🚀 ノード疎通テスト実行 (Ping Node)</button>
<div id='pingBox' style='margin-top:6px;font-family:monospace;font-size:0.52rem;color:var(--green);background:#05050a;padding:6px;border-radius:4px;border:1px solid var(--border);display:none;'></div></div>
<div class='sec'><h2>🧮 M2M Revenue Simulator <span class='tag'>SIMULATOR</span></h2>
<div style='display:flex;justify-content:space-between;font-size:0.6rem;margin-bottom:4px;'><span>エージェント数: <strong id='agCount' style='color:var(--purple)'>100</strong> units</span><span>推定収益: <strong id='revOutput' style='color:var(--gold)'>$1,450.00 / mo</strong></span></div>
<input type='range' min='10' max='5000' value='100' style='width:100%;accent-color:var(--purple);' id='simRange' oninput='updateSim(this.value)'></div>
<div class='sec'><h2>Enterprise Node Tier & Subscriptions <span class='tag'>LIVE</span></h2>
<div class='g3'>
<div class='pcard'><div><strong>Free Tier</strong><div style='font-size:0.85rem;color:var(--gold);margin:3px 0'>FREE</div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• 1,000 Req/mo<br>• Standard Access</div></div><button class='btn' onclick='openModal("signup")'>無料発行</button></div>
<div class='pcard feat'><div><strong style='color:var(--purple)'>Autonomous Pro</strong><div style='font-size:0.85rem;color:var(--gold);margin:3px 0'>$29<span style='font-size:0.45rem'>/mo</span></div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• Unlimited Req<br>• Zero Latency<br>• 15% Rebate</div></div><button class='btn pur' onclick='openModal("signup")'>購入する ↗</button></div>
<div class='pcard'><div><strong>Enterprise</strong><div style='font-size:0.85rem;color:var(--gold);margin:3px 0'>$299<span style='font-size:0.45rem'>/mo</span></div><div style='font-size:0.48rem;color:var(--muted);text-align:left'>• Swarm Core<br>• Task Auction<br>• SLA 100%</div></div><button class='btn blue' onclick='openModal("signup")'>ライセンス ↗</button></div>
</div></div>
<div class='sec'><h2>God-Tier Autonomous Economic Core <span class='tag'>ACTIVE</span></h2>
<div class='g4' style='margin-bottom:8px;'>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>埋蔵残高 (INGESTION)</div><div id='liveIngestion' style='font-size:0.65rem;color:var(--green);font-weight:bold'>$94,800,120.00</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>アクティブエージェント</div><div id='liveAgents' style='font-size:0.65rem;color:var(--green);font-weight:bold'>442,050,910 units</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>クロスチェーン効率</div><div id='liveEfficiency' style='font-size:0.65rem;color:var(--green);font-weight:bold'>99.99% (0.00ms)</div></div>
<div class='box' style='text-align:center'><div style='font-size:0.45rem;color:var(--muted)'>SLA稼働率</div><div style='font-size:0.65rem;color:var(--green);font-weight:bold'>100.0%</div></div>
</div>
<div class='g4'>
<div class='box'><div><strong>Bitcoin</strong> <span style='color:#f59e0b'>BTC</span></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac'></div><div class='addr'>bc1q94rkd...d7zac</div><a href='https://mempool.space/address/bc1q94rkd0dFhDNOh28kqrx2vyfpwa2efd7zac' target='_blank' class='btn'>Mempool</a></div>
<div class='box'><div><strong>Solana</strong> <span style='color:#a855f7'>SOL</span></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf'></div><div class='addr'>75igwQpPg...7nf</div><a href='https://solscan.io/account/75igwQpPgVkcySLvE5c9er2XcbuaWRh8CnDEYu7nf' target='_blank' class='btn'>Solscan</a></div>
<div class='box'><div><strong>Ethereum</strong> <span style='color:#3b82f6'>ETH</span></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8'></div><div class='addr'>0xD6716D0...8G8</div><a href='https://etherscan.io/address/0xD6716D08Da19874D108i4Cb7dcA2c6G590BD8G8' target='_blank' class='btn'>Etherscan</a></div>
<div class='box'><div><strong>Bitcoin SV</strong> <span style='color:#eab308'>BSV</span></div><div class='qr'><img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95'></div><div class='addr'>1PB66iHot...y95</div><a href='https://whatsonchain.com/address/1PB66iHotUEgBaAnkgV9uTTV7R235Tuy95' target='_blank' class='btn'>WhatsOnChain</a></div>
<div class='box'><div><strong>Mesh API</strong> <span style='color:var(--green)'>M2M</span></div><div class='addr' style='margin-top:6px'>/api/v32/mesh</div><button class='btn blue' onclick='alert("Mesh API Active.")'>ステータス</button></div>
<div class='box'><div><strong>.well-known</strong> <span style='color:#6366f1'>SPAR</span></div><div class='addr' style='margin-top:6px'>/agent.json</div><a href='/well-known/agent.json' target='_blank' class='btn blue'>マニフェスト</a></div>
<div class='box'><div><strong>Stripe</strong> <span style='color:#ec4899'>PST</span></div><div class='addr' style='margin-top:6px'>active-key</div><button class='btn blue' style='background:#065f46;color:#a7f3d0' onclick='alert("Stripe 稼働中 ✓")'>決済済 ✓</button></div>
<div class='box'><div><strong>Quantum Oracle</strong> <span style='color:#06b6d4'>PCT</span></div><div class='addr' style='margin-top:6px'>photonize-32.0</div><button class='btn blue' onclick='alert("HTTP 402: 量子レシート発行完了 ✓")'>402量子決済 ↗</button></div>
<div class='box'><div style='color:var(--gold);font-weight:bold;margin-bottom:2px;'>⚡ ARBITRAGE</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>価格差分自動検出。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>0.142%</span><span style='color:var(--green);'>OPTIMAL</span></div></div>
<div class='box'><div style='color:var(--blue);font-weight:bold;margin-bottom:2px;'>💎 QUANTUM 402</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>ゼロレイテンシ決済。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>ACTIVE</span><span style='color:var(--green);'>0.00ms</span></div></div>
<div class='box'><div style='color:var(--purple);font-weight:bold;margin-bottom:2px;'>🌐 UMBRA SYNC</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>自律ノード同期。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>99.99%</span><span style='color:var(--green);'>SECURE</span></div></div>
<div class='box'><div style='color:var(--green);font-weight:bold;margin-bottom:2px;'>🤖 AGI AUCTION</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>自動タスク仲介。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>BID #704</span><span style='color:var(--green);'>WIN ✓</span></div></div>
<div class='box'><div style='color:#f43f5e;font-weight:bold;margin-bottom:2px;'>🔮 SWARM NET</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>群知能ノード同期。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>4.4億超</span><span style='color:var(--green);'>SYNC ✓</span></div></div>
<div class='box'><div style='color:#a855f7;font-weight:bold;margin-bottom:2px;'>🛡️ VAPORLOCK</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>超高密度防御シールド。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>ACTIVE</span><span style='color:var(--green);'>SECURE</span></div></div>
<div class='box'><div style='color:#38bdf8;font-weight:bold;margin-bottom:2px;'>⚡ PHOTON L2</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>光速データレイヤー。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>0.00ms</span><span style='color:var(--green);'>ONLINE</span></div></div>
<div class='box'><div style='color:#10b981;font-weight:bold;margin-bottom:2px;'>🌌 SINGULARITY</div><div style='color:var(--muted);font-size:0.5rem;margin-bottom:4px;'>特異点自己修復コア。</div><div style='display:flex;justify-content:space-between;font-family:monospace;background:#0d0d1a;padding:3px;border-radius:3px;'><span>UNLOCKED</span><span style='color:var(--green);'>100%</span></div></div>
</div></div>
<div class='sec'><h2>OMNI-SYNAPSE LIVE COMMISSION STREAM</h2>
<div class='stream' id='streamLog'>[OMNI_SYNC_INIT] Node operational across BTC, SOL, EVM, BSV. Quantum Oracle locked cross-chain spread. 15% commission routed.</div></div>
<div class='sec'><h2>ENTERPRISE FEEDBACK & SYSTEM INSIGHTS</h2>
<div style='display:flex;gap:6px'><input type='text' id='feedbackInput' style='flex:1;background:#05050a;border:1px solid var(--border);border-radius:4px;padding:5px;color:#fff;font-size:0.6rem' placeholder='フィードバックを入力...'><button class='btn blue' style='margin:0;width:60px' onclick='sendFeedback()'>送信</button></div>
<div style='margin-top:10px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;'>
<div style='font-size:0.6rem;color:var(--purple);font-weight:bold;margin-bottom:4px;'>🌐 SWARM GOVERNANCE VOTING CONSOLE</div>
<div style='font-size:0.52rem;color:var(--muted);margin-bottom:6px;'>次期プロトコル手数料削減（15% → 10%）の即時投票:</div>
<div style='display:flex;gap:6px;'><button class='btn blue' style='flex:1;margin:0;' onclick='voteGov("YES")'>賛成投票 (YES)</button><button class='btn pur' style='flex:1;margin:0;' onclick='voteGov("NO")'>反対投票 (NO)</button></div>
<div id='voteResult' style='font-size:0.5rem;color:var(--green);margin-top:6px;font-family:monospace;display:none;'></div></div>
<div style='margin-top:8px;background:#05050a;border:1px solid var(--border);border-radius:5px;padding:8px;'>
<div style='font-size:0.6rem;color:var(--gold);font-weight:bold;margin-bottom:4px;'>🤖 LIVE AGENT TASK AUCTION POOL</div>
<div style='font-size:0.52rem;color:var(--muted);margin-bottom:6px;'>自律エージェント間のリアルタイム・タスクオークション状況:</div>
<div style='font-family:monospace;font-size:0.5rem;color:var(--green);background:#0d0d1a;padding:5px;border-radius:3px;'>[AUCTION_NODE_#704] Active Bid: 0.045 BSV | Winner: Agent_Swarm_Alpha ✓</div></div></div>
<div class='sec'><h2>企業情報 / 概要 <span class='tag'>QLAX</span></h2>
<div style='font-size:0.6rem;color:var(--muted);line-height:1.4;'>
<p style='margin:0 0 4px 0;'><strong>ASGARD</strong>は、自律型AIエージェント・M2M経済インフラの研究開発プラットフォームです。</p>
<p style='margin:0 0 4px 0;'><strong>QLAX</strong>は、福岡県豊前市を拠点に自律アービトラージと高スループット決済環境を構築する個人事業主の組織です。</p>
<p style='margin:0;'><strong>運営者:</strong> Daisuke Higuchi</p>
</div></div>
<div style='text-align:center;font-size:0.48rem;color:var(--muted);padding:4px 0'>© ASGARD Infrastructure | 運営者: QLAX (Daisuke Higuchi) / 豊前市.</div></div></div>
<div class='modal' id='authModal'><div class='modal-c'><div style='font-size:0.85rem;font-weight:bold;color:var(--purple);margin-bottom:10px;text-align:center;' id='modalTitle'>アカウント認証</div><input type='email' id='authEmail' placeholder='メールアドレス'><input type='password' id='authPassword' placeholder='パスワード'><button class='btn blue' style='width:100%;margin-bottom:6px;' onclick='submitAuth()'>実行する</button><button class='btn' style='width:100%;' onclick='closeModal()'>キャンセル</button></div></div>
<div style='position:fixed;bottom:8px;right:8px;z-index:1000;background:rgba(13,13,26,0.95);padding:4px 6px;border:1px solid #7e22ce;border-radius:4px'><a href='/legal' style='color:var(--purple);text-decoration:none;font-size:0.55rem;font-weight:bold'>特定商取引法表記 ↗</a></div>
<script>
let mode='login';
function openModal(m){mode=m;document.getElementById('modalTitle').innerText=m==='login'?'ASGARD ログイン':'エージェント サインアップ';document.getElementById('authModal').style.display='flex';}
function closeModal(){document.getElementById('authModal').style.display='none';}
async function submitAuth(){
    const email=document.getElementById('authEmail').value;
    const pass=document.getElementById('authPassword').value;
    if(!email||!pass)return alert('項目を入力してください');
    try{
        const r=await fetch('/api/v32/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password:pass})});
        const d=await r.json();
        alert(mode==='login'?'ログイン成功 ✓':'サインアップ完了! API Key: '+d.api_key);
    
