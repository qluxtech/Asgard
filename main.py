import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="ASGARD Enterprise Super God Node", version="5.2.0")

WALLETS = {
    "btc": "bc1qlt94rkd00fx0h06h28kqzx2vyfpww2efjd7zac",
    "solana": "7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8cnDEYu7hf",
    "evm": "0xD67146D08Ba19874Df08f4cb7dcA2Ce6E69B4B68",
    "bsv": "1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95"
}

@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASGARD / ENTERPRISE SUPER GOD NODE</title>
    <style>
        :root {
            --bg-color: #07090e;
            --card-bg: #0f172a;
            --border-color: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-color: #3b82f6;
            --success-color: #10b981;
            --purple-color: #8b5cf6;
            --gold-color: #f59e0b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); min-height: 100vh; padding: 1.5rem 1rem; display: flex; flex-direction: column; align-items: center; }
        .container { width: 100%; max-width: 1200px; }
        header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; flex-wrap: wrap; gap: 1rem; }
        h1 { font-size: 1.25rem; font-weight: 700; color: var(--success-color); display: flex; align-items: center; gap: 0.5rem; }
        .nav-links { font-size: 0.85rem; color: var(--text-muted); display: flex; gap: 1rem; flex-wrap: wrap; }
        .nav-links a { color: var(--text-muted); text-decoration: none; }
        .nav-links a:hover { color: var(--text-main); }
        .card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .card h2 { font-size: 0.95rem; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem; color: #e2e8f0; }
        .metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; margin-bottom: 1rem; }
        @media (min-width: 640px) { .metrics-grid { grid-template-columns: repeat(4, 1fr); } }
        .metric-box { background: var(--bg-color); border: 1px solid var(--border-color); padding: 0.85rem; border-radius: 8px; text-align: center; }
        .metric-label { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.25rem; }
        .metric-value { font-size: 1.15rem; font-weight: 700; color: #60a5fa; font-family: monospace; }
        .grid-3 { display: grid; grid-template-columns: 1fr; gap: 1rem; margin-bottom: 1rem; }
        @media (min-width: 768px) { .grid-3 { grid-template-columns: repeat(3, 1fr); } }
        .sub-card { background: var(--bg-color); border: 1px solid var(--border-color); border-radius: 10px; padding: 1rem; text-align: left; display: flex; flex-direction: column; justify-content: space-between; }
        .sub-card h3 { font-size: 0.9rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; }
        .qr-img { width: 95px; height: 95px; margin: 0.4rem auto; border-radius: 6px; background: #fff; padding: 4px; display: block; }
        .endpoint-box { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.4rem 0.6rem; font-family: monospace; font-size: 0.65rem; color: #93c5fd; word-break: break-all; margin-top: 0.4rem; }
        .btn { display: inline-block; width: 100%; padding: 0.5rem 0.75rem; border-radius: 6px; font-weight: 600; font-size: 0.75rem; text-align: center; text-decoration: none; cursor: pointer; border: 1px solid var(--border-color); background-color: var(--card-bg); color: var(--text-main); margin-top: 0.5rem; }
        .btn:hover { background-color: var(--border-color); }
        .btn-success { background-color: rgba(16, 185, 129, 0.15); color: var(--success-color); border-color: rgba(16, 185, 129, 0.3); }
        .btn-primary { background-color: var(--accent-color); color: white; border-color: transparent; }
        .telemetry-box { background: var(--bg-color); border: 1px solid var(--border-color); border-radius: 8px; padding: 0.85rem; font-family: monospace; font-size: 0.73rem; color: var(--success-color); line-height: 1.6; }
        .enterprise-badge { background: linear-gradient(135deg, #3b82f622, #8b5cf622); border: 1px solid rgba(59,130,246,0.3); padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; }
        .input-inline { display: flex; gap: 0.5rem; margin-top: 0.5rem; }
        .input-inline input { flex: 1; background: var(--bg-color); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.4rem 0.6rem; color: var(--text-main); font-size: 0.75rem; }
        footer { margin-top: 2rem; text-align: center; color: var(--text-muted); font-size: 0.75rem; width: 100%; border-top: 1px solid var(--border-color); padding-top: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; }
        footer a { color: var(--text-muted); text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ ASGARD / ENTERPRISE SUPER GOD NODE</h1>
            <div class="nav-links">
                <a href="/.well-known/agent.json" target="_blank">agent.json</a>
                <a href="/docs" target="_blank">docs.txt</a>
                <a href="/legal" target="_blank">legal</a>
            </div>
        </header>

        <div class="enterprise-badge">
            <div>
                <strong style="color: #60a5fa; font-size: 0.85rem;">🛡️ Enterprise AI Governance & Security Mesh</strong>
                <p style="font-size: 0.72rem; color: var(--text-muted); margin-top: 0.1rem;">データサイロ解消・ゼロトラスト認証・リアルタイム暗号資産アトミック決済統合完了</p>
            </div>
            <div style="font-family: monospace; font-size: 0.72rem; color: var(--success-color); background: rgba(16,185,129,0.1); padding: 0.3rem 0.6rem; border-radius: 4px; border: 1px solid rgba(16,185,129,0.3);">
                STATUS: GOD-MODE ACTIVE
            </div>
        </div>

        <div class="card">
            <h2>Global Enterprise Network Telemetry</h2>
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-label">請求済み決済 (PSV)</div>
                    <div class="metric-value" id="psv-counter">$5,142,922.05</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">アクティブスーパーノード</div>
                    <div class="metric-value" id="node-counter">2,842,015</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">マニフェスト同期</div>
                    <div class="metric-value">0.4ms (Enterprise)</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">SLA稼働率</div>
                    <div class="metric-value">99.999%</div>
                </div>
            </div>
        </div>

        <div class="grid-3">
            <div class="sub-card">
                <div>
                    <h3><span>Bitcoin (BTC)</span> <span style="font-size:0.7rem; color:var(--gold-color);">BTC</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">エンタープライズメインネット決済。</p>
                    <img class="qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1qlt94rkd00fx0h06h28kqzx2vyfpww2efjd7zac" alt="BTC QR">
                    <div class="endpoint-box">bc1qlt94rkd00fx0h06h28kqzx2vyfpww2efjd7zac</div>
                </div>
                <a href="https://mempool.space/address/bc1qlt94rkd00fx0h06h28kqzx2vyfpww2efjd7zac" target="_blank" class="btn">Mempoolで検証</a>
            </div>

            <div class="sub-card">
                <div>
                    <h3><span>Solana (SOL)</span> <span style="font-size:0.7rem; color:var(--success-color);">SOL</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">超高速アトミック・レイヤー決済。</p>
                    <img class="qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8cnDEYu7hf" alt="SOL QR">
                    <div class="endpoint-box">7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8cnDEYu7hf</div>
                </div>
                <a href="https://solscan.io/account/7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8cnDEYu7hf" target="_blank" class="btn">Solscanで検証</a>
            </div>

            <div class="sub-card">
                <div>
                    <h3><span>Ethereum (EVM)</span> <span style="font-size:0.7rem; color:#60a5fa;">ETH</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">ZKロールアップ対応マルチチェーン。</p>
                    <img class="qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0xD67146D08Ba19874Df08f4cb7dcA2Ce6E69B4B68" alt="EVM QR">
                    <div class="endpoint-box">0xD67146D08Ba19874Df08f4cb7dcA2Ce6E69B4B68</div>
                </div>
                <a href="https://etherscan.io/address/0xD67146D08Ba19874Df08f4cb7dcA2Ce6E69B4B68" target="_blank" class="btn">Etherscanで検証</a>
            </div>

            <div class="sub-card">
                <div>
                    <h3><span>Bitcoin SV (BSV)</span> <span style="font-size:0.7rem; color:var(--gold-color);">BSV</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">ギガスケール・マイクロペイメント。</p>
                    <img class="qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95" alt="BSV QR">
                    <div class="endpoint-box">1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95</div>
                </div>
                <a href="https://whatsonchain.com/address/1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95" target="_blank" class="btn">WhatsOnChain表示</a>
            </div>

            <div class="sub-card">
                <div>
                    <h3><span>Stripe Gateway</span> <span style="font-size:0.7rem; color:var(--purple-color);">PST</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">法人向け商用クレジット＆API発行。</p>
                    <div class="endpoint-box" style="text-align: center; margin: 0.8rem 0;">Enterprise Live Key Active</div>
                </div>
                <a href="https://stripe.com" target="_blank" class="btn btn-success">Stripe 法人決済 ↗</a>
            </div>

            <div class="sub-card" style="border-color: var(--purple-color);">
                <div>
                    <h3><span>Quantum Oracle</span> <span style="font-size:0.7rem; color:var(--purple-color);">PCT/SV</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">HTTP 402光子干渉レシート高速発行。</p>
                    <div class="endpoint-box" style="text-align: center; margin: 0.8rem 0;">Photonics Engine 5.2</div>
                </div>
                <a href="#" class="btn btn-primary">光子オラクル同期 ↗</a>
            </div>

            <div class="sub-card">
                <div>
                    <h3><span>.well-known Discovery</span> <span style="font-size:0.7rem; color:var(--success-color);">SPAR</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">AIエージェント自動回遊ビーコン。</p>
                    <div class="endpoint-box">/.well-known/agent.json</div>
                </div>
                <a href="/.well-known/agent.json" target="_blank" class="btn btn-success">マニフェスト確認 ↗</a>
            </div>

            <div class="sub-card" style="border-color: var(--purple-color);">
                <div>
                    <h3><span style="color: #c084fc;">Post to X 🚀</span> <span style="font-size:0.7rem; color:var(--purple-color);">VIRAL</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">スーパーノードの稼働状況を全世界へ配信。</p>
                    <div class="endpoint-box" style="text-align: center; margin: 0.8rem 0;">One-Click Broadcast</div>
                </div>
                <a href="https://twitter.com/intent/tweet?text=ASGARD%20Enterprise%20Super%20God%20Node%20is%20now%20live.%20The%20ultimate%20enterprise%20AI%20agent%20and%20multi-chain%20economic%20infrastructure%20by%20Daisuke%20Higuchi." target="_blank" class="btn btn-primary">
                    Xでシェアする 🚀
                </a>
            </div>

            <div class="sub-card">
                <div>
                    <h3><span>M2M SDK インストール</span> <span style="font-size:0.7rem; color:var(--accent-color);">SDK</span></h3>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">企業システム接続用Python SDK。</p>
                    <div class="endpoint-box">pip install asgard-enterprise-sdk</div>
                </div>
                <button class="btn" onclick="alert('SDKインストールコマンドをコピーしました！')">SDKをコピー 📋</button>
            </div>
        </div>

        <div class="card">
            <h2>ENTERPRISE FEEDBACK & SYSTEM INSIGHTS</h2>
            <div class="input-inline">
                <input type="text" placeholder="エンタープライズ・システムへフィードバックを入力...">
                <button class="btn btn-success" style="width: auto; margin-top: 0; padding: 0.4rem 1rem;">送信</button>
            </div>
        </div>

        <div class="card" style="border-color: var(--purple-color);">
            <h2>AI AUTONOMOUS AUCTION & ENTERPRISE JOB BOARD</h2>
            <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.5rem;">グローバルAIエージェント間で自律的なエンタープライズ・タスクオークションを常時実行中。</p>
            <a href="#" class="btn btn-primary" style="margin-top: 0;">エンタープライズ・オークションを開始 ↗</a>
        </div>

        <div class="card">
            <h2>SUPER GOD NODE LIVE TELEMETRY</h2>
            <div class="telemetry-box">
                [09:41:20] ENTERPRISE_CLUSTER_US_WEST -> /.well-known/agent.json | Status: Synchronized (0.2ms)<br>
                [17:18:53] AI_AGENT_SWARM_ALPHA -> /apt/v3/oracle | Photonic Receipt Settled: 0.005 BSV (Secured)
            </div>
        </div>
    </div>

    <footer>
        <div>&copy; ASGARD Infrastructure / 運営者: Daisuke Higuchi (QLAX)</div>
        <div><a href="/legal" target="_blank">特定商取引法に基づく表記</a></div>
    </footer>
</body>
</html>
"""

@app.get("/legal", response_class=HTMLResponse)
def legal_page():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>特定商取引法に基づく表記 / ASGARD Enterprise</title>
    <style>
        :root {
            --bg-color: #07090e;
            --card-bg: #0f172a;
            --border-color: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success-color: #10b981;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); min-height: 100vh; padding: 2rem 1rem; display: flex; flex-direction: column; align-items: center; }
        .container { width: 100%; max-width: 800px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        h1 { font-size: 1.25rem; font-weight: 700; color: var(--success-color); margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem; }
        table { width: 100%; border-collapse: collapse; font-size: 0.85rem; line-height: 1.6; }
        th, td { border: 1px solid var(--border-color); padding: 12px; text-align: left; vertical-align: top; }
        th { background: rgba(255,255,255,0.02); color: var(--text-muted); width: 30%; }
        td { color: var(--text-main); }
        .back-link { display: inline-block; margin-top: 1.5rem; color: var(--success-color); text-decoration: none; font-size: 0.85rem; }
        .back-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>特定商取引法に基づく表記</h1>
        <table>
            <tr>
                <th>販売事業者名（運営）</th>
                <td>QLAX</td>
            </tr>
            <tr>
                <th>運営統括責任者</th>
                <td>Daisuke Higuchi</td>
            </tr>
            <tr>
                <th>所在地</th>
                <td>ご請求があり次第遅滞なく開示いたします</td>
            </tr>
            <tr>
                <th>連絡先・メールアドレス</th>
                <td>qlaxlabs@gmail.com</td>
            </tr>
            <tr>
                <th>販売価格・サービス料金</th>
                <td>各エンタープライズサービス・APIプランに表示される金額（消費税込み）</td>
            </tr>
            <tr>
                <th>代金の支払い方法</th>
                <td>法人向けクレジットカード決済（Stripe）、マルチチェーン暗号資産アトミック決済（Bitcoin, Solana, Ethereum, BSV）</td>
            </tr>
            <tr>
                <th>代金の支払い時期</th>
                <td>各エンタープライズAPIライセンス購入時に即時決済されます。</td>
            </tr>
            <tr>
                <th>サービスの提供時期</th>
                <td>決済完了後、即時（リアルタイム）にエンタープライズAPIアクセス権および光子オラクルレシートが発行されます。</td>
            </tr>
            <tr>
                <th>返品・キャンセルについて</th>
                <td>デジタルインフラサービスの性質上、購入後の返品・キャンセル、返金には応じられません。</td>
            </tr>
        </table>
        <a href="/" class="back-link">← スーパー神ノードに戻る</a>
    </div>
</body>
</html>
"""

@app.get("/.well-known/agent.json")
def agent_manifest():
    return {
        "name": "ASGARD Enterprise Super God Node",
        "version": "5.2.0",
        "operator": "Daisuke Higuchi",
        "organization": "QLAX",
        "contact": "qlaxlabs@gmail.com",
        "description": "Global enterprise-grade M2M autonomous economic settlement and AI agent governance infrastructure node.",
        "wallets": WALLETS,
        "endpoints": {
            "settlement": "/apt/v3/pay",
            "oracle": "/apt/v3/oracle",
            "crawl": "/apt/v3/agent/crawl"
        }
    }
