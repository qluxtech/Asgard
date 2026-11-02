from fastapi import FastAPI, Header, status
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="ASGARD Quantum Singularity Node", version="7.0.0")

WALLETS = {
    "btc": "bc1qlt94rkd00fx0h06h28kqzx2vyfpww2efjd7zac",
    "solana": "7SigxwQgPVgXNcySLvE5c9er2XcbuwXRhh8cnDEYu7hf",
    "evm": "0xD67146D08Ba19874Df08f4cb7dcA2Ce6E69B4B68",
    "bsv": "1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95"
}

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASGARD / QUANTUM SINGULARITY NODE</title>
    <style>
        body { background-color: #07090e; color: #f8fafc; font-family: sans-serif; padding: 2rem; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; background: #0f172a; border: 1px solid #1e293b; padding: 2rem; border-radius: 12px; }
        h1 { color: #10b981; font-size: 1.5rem; }
        .box { background: #07090e; border: 1px solid #1e293b; padding: 1rem; margin-top: 1rem; font-family: monospace; color: #60a5fa; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ ASGARD / QUANTUM SINGULARITY NODE v7.0.0</h1>
        <p>量子先回り決済・自律型クレジットライン稼働中</p>
        <div class="box">BSV Wallet: 1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95</div>
        <div class="box">Endpoint: /.well-known/agent.json</div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_CONTENT

@app.get("/.well-known/agent.json")
def agent_manifest():
    return {
        "name": "ASGARD Quantum Singularity Node",
        "version": "7.0.0",
        "operator": "Daisuke Higuchi",
        "organization": "QLAX",
        "wallets": WALLETS
    }

@app.get("/apt/v3/quantum-predictive")
def quantum_predictive(payment_proof: str = Header(None, alias="X-Payment-Proof")):
    if not payment_proof:
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "error": "Quantum Pre-Settlement Required",
                "fee": "0.0008 BSV",
                "settlement_wallet": WALLETS["bsv"]
            }
        )
    return {"status": "QUANTUM_PRE_SETTLED_SUCCESS", "latency": "0.00ms"}
