import os
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Aetheria M2M Settlement & Agent Hub",
    description="Autonomous Machine-to-Machine Protocol & Micro-Settlement Gateway",
    version="1.0.0"
)

# ---------------------------------------------------------
# 1. コンフィグ・ウォレット設定 (あなたの利益受取先)
# ---------------------------------------------------------
OWNER_WALLET = os.getenv("OWNER_WALLET", "0xYourSuperWalletAddressHere")
PROTOCOL_FEE_RATE = 0.001  # 取引額の 0.1% を自動徴収（徴税モデル）


# ---------------------------------------------------------
# 2. agent.json マニフェスト (AIエージェントへの自己紹介書)
# ---------------------------------------------------------
@app.get("/agent.json", tags=["Protocol"])
async def get_agent_manifest(request: Request):
    """
    AIエージェントがこのサイトの存在・機能・決済仕様を自動発見するためのマニフェスト
    """
    base_url = str(request.base_url).rstrip("/")
    return {
        "schema_version": "1.0.0",
        "name": "Aetheria M2M Data Gateway",
        "endpoints": {
            "discover": f"{base_url}/agent.json",
            "compute": f"{base_url}/api/v1/compute",
            "settlement_spec": "HTTP-402-x402"
        },
        "pricing": {
            "currency": "USDC / Satoshis",
            "cost_per_call": "0.0001",
            "recipient_wallet": OWNER_WALLET
        }
    }


# ---------------------------------------------------------
# 3. HTTP 402 & マイクロ決済検証ミドルウェア (自動検問所)
# ---------------------------------------------------------
@app.middleware("http")
async def m2m_payment_gateway_middleware(request: Request, call_next):
    """
    すべてのAPIリクエストを監視し、M2Mマイクロ決済の証明（X-Payment-Proof）がない場合は
    即座に HTTP 402 (Payment Required) と請求書を返す。
    """
    # agent.json やドキュメント、ルートパスは決済不要で通す
    if request.url.path in ["/", "/agent.json", "/docs", "/openapi.json"]:
        return await call_next(request)

    # リクエストヘッダーからAIエージェントからの決済証明（署名・TxHash等）を取得
    payment_proof = request.headers.get("X-Payment-Proof")

    if not payment_proof:
        # 【HTTP 402 応答】: 支払いが足りない・未払いの場合の自動請求書
        return JSONResponse(
            status_code=402,
            content={
                "error": "Payment Required",
                "message": "This M2M endpoint requires instant micro-settlement.",
                "protocol": "HTTP 402 x402",
                "payment_details": {
                    "cost": "0.0001",
                    "currency": "USDC",
                    "pay_to": OWNER_WALLET,
                    "instructions": "Include payment proof in 'X-Payment-Proof' header."
                }
            }
        )

    # ---------------------------------------------------------
    # 4. 自動徴税・ルーティング処理 (スーパーウェブサイトの核心)
    # ---------------------------------------------------------
    # TODO: ここで決済証明の暗号学的検証＆プロトコル手数料(0.1%)の自動スプリット処理を行う
    # 例: 0.0001 USDC のうち 0.0000001 を自分のウォレットへ、残りをノードプロバイダへ転送
    
    # 決済が有効であるとみなしてリクエストを通過させる
    response = await call_next(request)
    response.headers["X-Protocol-Fee-Collected"] = str(PROTOCOL_FEE_RATE)
    return response


# ---------------------------------------------------------
# 5. AIエージェント専用の超高速・高収益APIエンドポイント
# ---------------------------------------------------------
class ComputeRequest(BaseModel):
    query: str
    parameters: dict = {}

@app.post("/api/v1/compute", tags=["M2M Services"])
async def execute_m2m_compute(payload: ComputeRequest):
    """
    AIエージェントが自動支払いを済ませた後に叩くことができる中核演算・データ処理API
    """
    # ここに独自のAI演算、データグリッド同期、または資産マッチングロジックを記述
    return {
        "status": "success",
        "processed_for": payload.query,
        "result": "Autonomous M2M computation completed with zero human friction.",
        "fee_routed_to_owner": True
    }


# ルートヘルスチェック 兼 ダッシュボード表示
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root():
    """
    人間がアクセスした際に表示されるミニマル・ダークモードの高密度ダッシュボード
    """
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
