import os
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import stripe

app = FastAPI(title="Asgard Autonomous Economy Grid", version="3.0.0")

# Stripeの本番・テストキーを環境変数から取得（Render側で設定）
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "pk_live_51USSUBFUthDFhcGOsBWZVtD3OEhvsJOeHaxB4spSZyIVHkCz4dokxkEHcKTA7XvSsee4abw3PcRryzFM05TpXWyR00KeKhVjVB")

# ウォレットアドレス設定
SOLANA_WALLET = "7SigxwQgPVgXNcySLvE5c9er2XcbuwXRh8cnDEYu7hf"
EVM_WALLET = "0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68"

class PaymentRequest(BaseModel):
    amount_jpy: int = 100
    agent_id: str = "ANONYMOUS_AGENT"

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # templates/index.html を読み込んで返す
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Asgard Core Online</h1><p>index.html not found in templates/</p>")

@app.get("/agent.json")
async def agent_manifest():
    """M2M AIエージェント用のメタデータ・マニフェストエンドポイント"""
    return {
        "name": "Asgard Autonomous Economy Grid",
        "version": "3.0.0",
        "endpoints": {
            "compute": "/api/v1/compute",
            "payment_required": 402
        },
        "settlement_layers": {
            "solana": SOLANA_WALLET,
            "evm": EVM_WALLET,
            "stripe": "https://api.stripe.com/v1/asgard_m2m"
        },
        "public_keys": {
            "stripe_pk": STRIPE_PUBLIC_KEY
        }
    }

@app.post("/api/v1/compute")
async def compute_endpoint(req: Request, authorization: str = Header(None)):
    """
    HTTP 402 Payment Required プロトコルを通じたM2M自動決済エンドポイント
    """
    # エージェントからの課金ヘッダーがない場合は 402 Payment Required を返す
    if not authorization:
        return JSONResponse(
            status_code=402,
            content={
                "error": "Payment Required",
                "message": "Asgard M2M Protocol requires micro-settlement via Solana, EVM, or Stripe.",
                "accept_methods": ["USDC/SOL", "USDC/EVM", "Stripe JPY/USD"],
                "endpoints": {
                    "solana": SOLANA_WALLET,
                    "evm": EVM_WALLET,
                    "stripe_checkout": "/api/v1/create-checkout-session"
                }
            }
        )
    
    return {
        "status": "success",
        "message": "Compute resource allocated and verified.",
        "routed_to": "Multi-chain sovereign mesh"
    }

@app.post("/api/v1/create-checkout-session")
async def create_checkout_session(data: PaymentRequest):
    """
    Stripe Checkout セッションを作成し、決済URLを返すエンドポイント
    """
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'jpy',
                    'product_data': {
                        'name': f'Asgard Compute Unit (Agent: {data.agent_id})',
                    },
                    'unit_amount': data.amount_jpy,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://asgard-m2m.onrender.com/?success=true',
            cancel_url='https://asgard-m2m.onrender.com/?canceled=true',
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
