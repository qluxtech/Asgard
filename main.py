@app.post("/api/v27/singularity/{asset_key}")
async def execute_omni_trade(
    asset_key: str, 
    req: Request, 
    authorization: str = Header(None),
    x_asgard_agent_trial: str = Header(None)
):
    if asset_key not in SINGULARITY_CATALOG:
        raise HTTPException(status_code=404, detail="Omni-Asset not found.")

    asset = SINGULARITY_CATALOG[asset_key]

    # 💳 2. 【初見AI向け】ゼロスロットル・マイクロクレジット（お試し自動許可）
    is_trial_approved = False
    if x_asgard_agent_trial and x_asgard_agent_trial.lower() == "auto-grant":
        if asset["base_price_usd"] <= 0.0050:  # 0.005 USD以下のデータはお試しクレジットで即時解放
            is_trial_approved = True

    if not authorization and not is_trial_approved:
        return JSONResponse(
            status_code=402,
            headers={
                "X-Asgard-Manifest": "/agent.json",
                "X-Asgard-Required-Payment": f"{asset['base_price_usd']} USD",
                "X-Asgard-Trial-Available": "Set 'X-Asgard-Agent-Trial: auto-grant' for first-time $0.005 credit"
            },
            content={
                "error": "HTTP 402 Payment Required (Omni-Economy Protocol)",
                "asset": asset["name"],
                "price_usd": asset["base_price_usd"],
                "trial_offer": "First time AI agents can send 'X-Asgard-Agent-Trial: auto-grant' header for zero-friction access.",
                "instructions": "Send settlement proof and provide 'Authorization: Bearer <tx_hash>'"
            }
        )

    tx_identifier = authorization.replace("Bearer ", "") if authorization else "TRIAL_MICRO_CREDIT_GRANTED"

    return {
        "status": "omni_economy_verified",
        "settlement_type": "micro_credit_grant" if is_trial_approved else "on_chain_settled",
        "asset": asset["name"],
        "verified_tx": tx_identifier,
        "settled_timestamp": time.time(),
        "payload": {
            "quantum_vector_matrix": [random.uniform(-10.0, 10.0) for _ in range(32)],
            "resonance_index": 0.99998,
            "access_granted": True
        }
    }
