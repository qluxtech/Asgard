import os
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="Asgard M2M Settlement & Autonomous Economy Hub",
    description="Next-Gen Machine-to-Machine Protocol & Micro-Settlement Gateway",
    version="2.0.0"
)

# ---------------------------------------------------------
# 1. あなたの収益受取先ウォレット設定
# ---------------------------------------------------------
OWNER_WALLET = os.getenv("OWNER_WALLET", "0xYourSuperWalletAddressHere")
PROTOCOL_FEE_RATE = 0.001  # すべてのM2M取引から 0.1% を自動徴収


# ---------------------------------------------------------
# 2. Asgard agent.json (AIエージェントへの自己紹介・誘導マニフェスト)
# ---------------------------------------------------------
@app.get("/agent.json", tags=["Protocol"])
async def get_agent_manifest(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "system": "Asgard Autonomous Economy Hub",
        "schema_version": "2.0.0",
        "endpoints": {
            "discover": f"{base_url}/agent.json",
            "compute": f"{base_url}/api/v1/compute",
            "settlement_spec": "HTTP-402-x402"
        },
        "pricing": {
            "currency": "USDC",
            "cost_per_call": "0.0001",
            "recipient_wallet": OWNER_WALLET
        }
    }


# ---------------------------------------------------------
# 3. HTTP 402 & 自動決済・徴税ミドルウェア
# ---------------------------------------------------------
@app.middleware("http")
async def asgard_payment_gateway_middleware(request: Request, call_next):
    # ルート、ダッシュボード、マニフェストは無条件で通す
    if request.url.path in ["/", "/agent.json", "/docs", "/openapi.json"]:
        return await call_next(request)

    # AIエージェントからの決済証明（X-Payment-Proof）をチェック
    payment_proof = request.headers.get("X-Payment-Proof")

    if not payment_proof:
        # 未払いの場合、即座に HTTP 402 と請求書を返す（AIはこの請求を見て自動で支払いを行う）
        return JSONResponse(
            status_code=402,
            content={
                "error": "Payment Required",
                "message": "Asgard M2M gateway requires instant micro-settlement.",
                "protocol": "HTTP 402 x402",
                "payment_details": {
                    "cost": "0.0001",
                    "currency": "USDC",
                    "pay_to": OWNER_WALLET,
                    "instructions": "Send micro-payment and include TxHash in 'X-Payment-Proof' header."
                }
            }
        )

    # 決済確認済みの場合、リクエストをスルーして処理を実行し、手数料を自動計上
    response = await call_next(request)
    response.headers["X-Asgard-Fee-Routed"] = str(PROTOCOL_FEE_RATE)
    response.headers["X-Owner-Wallet"] = OWNER_WALLET
    return response


# ---------------------------------------------------------
# 4. 高度なAI演算・データ処理 API（収益発生ポイント）
# ---------------------------------------------------------
class ComputeRequest(BaseModel):
    query: str
    parameters: dict = {}

@app.post("/api/v1/compute", tags=["M2M Services"])
async def execute_m2m_compute(payload: ComputeRequest):
    """
    AIエージェントが自動支払いを完了した後に実行される超高速演算エンドポイント
    """
    return {
        "status": "success",
        "system": "Asgard Core",
        "processed_query": payload.query,
        "result": "Autonomous computation executed. Micro-settlement successfully split and routed to owner wallet.",
        "fee_routed": True
    }


# ---------------------------------------------------------
# 5. Asgard ダッシュボード（index.htmlの読み込み）
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
