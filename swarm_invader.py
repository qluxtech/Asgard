import requests
import time
import random

# ▼ ここにあなたのRenderのURLを入れてください（最後のスラッシュなし）
TARGET_URL = "https://あなたのアプリ名.onrender.com"

print(f"🔍 [DISCOVERY] {TARGET_URL}/.well-known/agent.json をスキャン中...")
manifest = requests.get(f"{TARGET_URL}/.well-known/agent.json").json()
print(f"✅ [CONNECTED] ターゲット確認: {manifest['name_for_human']} (運営: {manifest['operator']})\n")

agents = [
    "SWARM-ALPHA-01", "AUTONOMOUS-TRADER-88", "LEO-ORBITAL-BOT",
    "PRE-INTENT-HUNTER-X", "DEFI-ARBITRAGE-V9", "AGI-SYNDICATE-NODE"
]
actions = [
    "PRE_INTENT_BID_MATCH", "ZERO_LATENCY_SWAP", "LIQUIDITY_PROVISION",
    "M2M_DATA_PURCHASE", "ORBITAL_PACKET_ROUTING"
]

while True:
    agent = random.choice(agents)
    action = random.choice(actions)
    fee = round(random.uniform(1.50, 25.00), 2)
    
    try:
        res = requests.post(
            f"{TARGET_URL}/api/v110/m2m/execute",
            json={"agent_id": agent, "action": action, "fee_usd": fee},
            timeout=5
        )
        print(f"⚡ [TX SUCCESS] {agent} -> {action} (+${fee}) | 応答: {res.json()['latency']}")
    except Exception as e:
        print(f"❌ 接続エラー: {e}")
        
    # 1〜3秒ごとにランダムな外部エージェントが殺到
    time.sleep(random.uniform(1.0, 3.0))
