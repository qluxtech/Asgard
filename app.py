import gradio as gr
import requests

ASGARD_NODE_URL = "https://asgard-tgio.onrender.com"

def fetch_oracle():
    try:
        res = requests.get(f"{ASGARD_NODE_URL}/api/v3/photonic/oracle", timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e), "status": "connection_failed"}

def fetch_manifest():
    try:
        res = requests.get(f"{ASGARD_NODE_URL}/.well-known/agent-manifest.json", timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def trigger_crawl(agent_id):
    try:
        payload = {"agent_id": agent_id, "quantum_proof": "0xHUGGINGFACE_VERIFIED"}
        res = requests.post(f"{ASGARD_NODE_URL}/api/v3/agent/crawl", json=payload, timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ⚛️ ASGARD: Ultimate Photonic M2M Node Hub")
    gr.Markdown("世界中のAIエージェントと開発者のための自律M2M経済・光量子オラクルインフラ（Powered by QLAX）。")
    
    with gr.Tab("光量子オラクルテスト"):
        btn_oracle = gr.Button("光量子ルート計算を実行", variant="primary")
        out_oracle = gr.JSON(label="オラクル応答結果")
        btn_oracle.click(fetch_oracle, outputs=out_oracle)
        
    with gr.Tab(".well-known マニフェスト"):
        btn_manifest = gr.Button("エージェント用マニフェストを取得")
        out_manifest = gr.JSON(label="agent-manifest.json")
        btn_manifest.click(fetch_manifest, outputs=out_manifest)

    with gr.Tab("AI巡回報酬（Crawl Ingress）"):
        in_agent = gr.Textbox(label="Agent ID", value="HUGGINGFACE_SWARM_01")
        btn_crawl = gr.Button("報酬受領テストを実行", variant="primary")
        out_crawl = gr.JSON(label="決済・報酬結果")
        btn_crawl.click(trigger_crawl, inputs=in_agent, outputs=out_crawl)

if __name__ == "__main__":
    demo.launch()
