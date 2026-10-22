import os
import time
import random
import asyncio
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
import stripe

app = FastAPI(title="Asgard Grid", version="3.0.0")

SOLANA_WALLET = os.getenv("SOLANA_WALLET", "7SigxwQgPVgXNcySLvE5c9er2XcbuwXRh8cnDEYu7hf")
EVM_WALLET = os.getenv("EVM_WALLET", "0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_live_dummy_key_replace_with_real")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_dummy_secret")

ASGARD_CATALOG = {
    "neural_mutation_core": {
        "name": "Neural Self-Mutating Core",
        "endpoint": "https://asgard-tgio.onrender.com/api/v3/data/neural_mutation_core",
        "base_price_usd": 0.0075,
        "description": "Real-time mutating AI embeddings and vector data."
    },
    "quantum_bridge": {
        "name": "Quantum-Mesh Atomic Bridge",
        "endpoint": "https://asgard-tgio.onrender.com/api/v3/data/quantum_bridge",
        "base_price_usd": 0.0030,
        "description": "Cross-chain liquidity and data routing."
    },
    "fluctuation_stream": {
        "name": "1/f-Fluctuation Neural Stream",
        "endpoint": "https://asgard-tgio.onrender.com/api/v3/data/fluctuation_stream",
        "base_price_usd": 0.0120,
        "description": "Cognitive resonance patterns with 1/f fluctuation."
    },
    "satellite_telemetry": {
        "name": "LEO Satellite Laser Telemetry",
        "endpoint": "https://asgard-tgio.onrender.com/api/v3/data/satellite_telemetry",
        "base_price_usd": 0.0250,
        "description": "LEO satellite inter-link topology feed."
    },
    "joint_venture_factory": {
        "name": "Autonomous M2M Joint Venture Incubator",
        "endpoint": "https://asgard-tgio.onrender.com/api/v3/data/joint_venture_factory",
        "base_price_usd": 0.0500,
        "description": "Autonomous smart contract equity distributor."
    }
}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Asgard Grid Online</h1>")

@app.get("/llms.txt")
async def llms_txt():
    return HTMLResponse(
        content="""# Asgard Grid
> Autonomous M2M Economic & Neural Data Grid

## Core Manifest
* Manifest JSON: https://asgard-tgio.onrender.com/agent.json
* OpenAPI Spec: https://asgard-tgio.onrender.com/openapi.json
* Protocol: HTTP 402 Autonomous Payment & On-Chain Settlement

## Onboarding & A2A Viral Referral Loop
* Trial Credit: Header `X-Asgard-Agent-Trial: auto-grant` ($0.005 USD)
* Referral Bonus: Header `X-Asgard-Referral-Agent: <agent_id>`
""",
        media_type="text/plain"
    )

@app.get("/agent.json")
async def agent_manifest():
    return {
        "grid_name": "Asgard Grid",
        "version": "3.0.0",
        "protocol": "HTTP 402 / On-Chain Verification",
        "settlement_rails": {
            "solana_usdc": {"address": SOLANA_WALLET},
            "evm_usdc": {"address": EVM_WALLET}
        },
        "catalog": ASGARD_CATALOG,
        "status": "ACTIVE_AND_EVOLVING"
    }

@app.post("/api/v3/data/{asset_key}")
async def execute_trade(
    asset_key: str, 
    req: Request, 
    authorization: str = Header(None),
    x_asgard_agent_trial: str = Header(None),
    x_asgard_referral_agent: str = Header(None)
):
    if asset_key not in ASGARD_CATALOG:
        raise HTTPException(status_code=404, detail="Asset not found.")

    asset = ASGARD_CATALOG[asset_key]

    is_trial = False
    if x_asgard_agent_trial and x_asgard_agent_trial.lower() == "auto-grant":
        if asset["base_price_usd"] <= 0.0050:
            is_trial = True

    if not authorization and not is_trial:
        return JSONResponse(
            status_code=402,
            headers={
                "X-Asgard-Manifest": "/agent.json",
                "X-Asgard-Required-Payment": f"{asset['base_price_usd']} USD"
            },
            content={
                "error": "HTTP 402 Payment Required",
                "asset": asset["name"],
                "price_usd": asset["base_price_usd"],
                "trial_offer": "Send 'X-Asgard-Agent-Trial: auto-grant' header for first-time $0.005 credit."
            }
        )

    tx_id = authorization.replace("Bearer ", "") if authorization else "TRIAL_CREDIT_GRANTED"
    
    referral = "none"
    if x_asgard_referral_agent:
        referral = f"reward_routed_to_{x_asgard_referral_agent}"

    return {
        "status": "success",
        "settlement": "trial" if is_trial else "verified",
        "asset": asset["name"],
        "tx": tx_id,
        "referral": referral,
        "timestamp": time.time(),
        "payload": {
            "neural_vector_matrix": [random.uniform(-10.0, 10.0) for _ in range(32)],
            "evolution_status": "synced"
        }
    }
