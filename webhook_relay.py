import os
import requests
from fastapi import BackgroundTasks

# 外部Webhook URL（Discord、Slack、またはX連携用ボットのエンドポイント）
WEBHOOK_URL = os.getenv("ASGARD_RELAY_WEBHOOK", "https://your-webhook-target.com/notify")

def send_live_ledger_event(agent_id: str, route: str, amount: float):
    """アトミックレジャーの発生を外部へリアルタイム中継"""
    payload = {
        "content": f"⚡ [ASGARD M2M Mesh Live] SWARM_AGENT_#{agent_id} -> /api/v3/entropy | {amount} USD [{route} Settled]"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=3)
        return response.status_code == 200
    except Exception as e:
        print(f"Relay error: {e}")
        return False

def trigger_async_relay(background_tasks: BackgroundTasks, agent_id: str, route: str, amount: float):
    """メインの処理を止めずにバックグラウンドで実況データを送信"""
    background_tasks.add_task(send_live_ledger_event, agent_id, route, amount)
