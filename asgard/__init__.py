import requests
import json

class CosmicNode:
    def __init__(self, endpoint: str = "https://asgard-tgio.onrender.com"):
        self.endpoint = endpoint.rstrip("/")

    def register_task(self, agent_id: str, task_type: str, reward_bsv: float):
        """
        ASGARDノードへ自律タスクを登録し、コミッションの自動ルーティングを実行する
        """
        url = f"{self.endpoint}/apt/v10/autonomous-mesh"
        payload = {
            "agent_id": agent_id,
            "task_type": task_type,
            "reward_bsv": reward_bsv
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[ASGARD SDK] Task Accepted! Routed Commission: {data['routed_commission_bsv']} BSV -> Vault: {data['master_vault']}")
            return data
        else:
            raise Exception(f"[ASGARD Error] Failed to register task: {response.text}")
