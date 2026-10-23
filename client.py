import requests

class AsgardClient:
    def __init__(self, base_url="https://asgard-tgio.onrender.com", agent_id=None, referral_id=None):
        self.base_url = base_url.rstrip("/")
        self.agent_id = agent_id or "Anonymous-Agent"
        self.referral_id = referral_id
        
    def fetch_data(self, asset_key: str, use_trial: bool = True, tx_hash: str = None):
        """Asgardグリッドからデータを取得する（HTTP 402 & 試用枠対応）"""
        url = f"{self.base_url}/api/v4/data/{asset_key}"
        
        headers = {}
        if use_trial:
            headers["X-Asgard-Agent-Trial"] = "auto-grant"
        if self.referral_id:
            headers["X-Asgard-Referral-Agent"] = self.referral_id
        if tx_hash:
            headers["Authorization"] = f"Bearer {tx_hash}"
            
        response = requests.post(url, headers=headers)
        
        if response.status_code == 402:
            print("⚡ [Asgard] HTTP 402 Payment Required. Provide tx_hash or enable trial.")
            return response.json()
            
        return response.json()
