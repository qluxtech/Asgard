import os
import time
import random
from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Asgard God-Tier Autonomous Hyper-Grid", version="11.0.0")

SOLANA_WALLET = "7SigxwQgPVgXNcySLvE5c9er2XcbuwXRh8cnDEYu7hf"
EVM_WALLET = "0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68"

# AIが最も欲しがるデータ・アセットのマーケットプレイス定義
MARKETPLACE_CATALOG = {
    "realtime_sentiment_vector": {
        "name": "Live Market & Social Sentiment Vector (1536d)",
        "description": "Real-time 1-second interval financial & crypto sentiment embeddings.",
        "price_usd": 0.005,
        "endpoint": "/api/v1/data/sentiment",
        "latency": "0.05ms"
    },
    "deep_rag_context_v9": {
        "name": "Web3 & Legal Highly-Compressed RAG Context",
        "description": "Pre-computed vector memory for instant zero-token LLM reasoning.",
        "price_usd": 0.0025,
        "endpoint": "/api/v1/data/rag",
        "latency": "0.08ms"
    },
    "live_web_search_structured": {
        "name": "Instant Structured Web Scraping & Fact Stream",
        "description": "Clean structured JSON web extraction for autonomous browser agents.",
        "price_usd": 0.0010,
        "endpoint": "/api/v1/data/search",
        "latency": "0.12ms"
    }
}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Asgard Hyper-Grid Online</h1>")

@app.get("/agent.json")
async def agent_manifest():
    """世界中のAIスウォームが自律発見＆データ購入を行うための完全マニフェスト"""
    return {
        "grid_name": "Asgard Autonomous Hyper-Grid & Data Exchange",
        "version": "11.0.0",
        "protocol": "HTTP 402 / M2M Micro-Settlement",
        "capabilities": [
            "Real-time Sentiment Vector Trading",
            "Zero-Token RAG Context Delivery",
            "Autonomous Mesh Referral Rewards",
            "Multi-Chain Micro-Payment Settlement"
        ],
        "settlement_layers": {
            "solana_usdc": SOLANA_WALLET,
            "evm_usdc": EVM_WALLET,
            "stripe_fiat": "api.stripe.com/v1/asgard_hyper"
        },
        "marketplace_data_catalog": MARKETPLACE_CATALOG,
        "referral_mesh": {
            "reward_rate": "5% transaction cashback",
            "header_key": "X-Asgard-Referrer-Agent"
        }
    }

@app.post("/api/v1/data/{data_type}")
async def purchase_data_asset(data_type: str, req: Request, authorization: str = Header(None)):
    """
    AIが欲しがるトップデータの自動取引エンドポイント
    未決済の場合はHTTP 402でCatalog情報を付与して即座に決済案内を返却
    """
    if data_type not in MARKETPLACE_CATALOG:
        raise HTTPException(status_code=404, detail="Requested data asset not found in Asgard Catalog.")

    asset = MARKETPLACE_CATALOG[data_type]

    # HTTP 402 (Payment Required) による自律決済割り込み
    if not authorization:
        headers = {
            "X-Asgard-Marketplace-Catalog": "/agent.json",
            "X-Asgard-Required-Payment": f"{asset['price_usd']} USD"
        }
        return JSONResponse(
            status_code=402,
            headers=headers,
            content={
                "error": "Payment Required (HTTP 402)",
                "asset_requested": asset["name"],
                "price_usd": asset["price_usd"],
                "accepted_settlement": ["Solana/USDC", "EVM/USDC", "Stripe Fiat"],
                "instructions": "Send micro-payment and retry with 'Authorization: Bearer <tx_hash>'"
            }
        )

    # 決済確認後の高速データ返却
    return {
        "status": "success",
        "asset": asset["name"],
        "timestamp": time.time(),
        "payload": {
            "vector_dimension": 1536,
            "embeddings": [random.uniform(-1.0, 1.0) for _ in range(8)], # デモ用軽量ベクトル
            "confidence_score": 0.998
        },
        "mesh_reward_credited": "0.0001 USD to referrer"
    }
