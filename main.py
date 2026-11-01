from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
import math
import random
import time
import os

# 1. ここで先に app を定義します
app = FastAPI(title="ASGARD Grid - Omni-Viral Supreme")

@app.get("/legal", response_class=HTMLResponse)
async def legal_page(request: Request):
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>法的情報 — ASGARD / QLAX</title>
      <style>
        :root {
          --bg: #030407;
          --surface: #0a0d14;
          --border: rgba(255, 255, 255, 0.08);
          --text-primary: #f1f5f9;
          --text-secondary: #8892b0;
          --accent: #38bdf8;
          --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
          --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
          background-color: var(--bg);
          color: var(--text-primary);
          font-family: var(--font-sans);
          padding: 40px 20px;
          max-width: 800px;
          margin: 0 auto;
          line-height: 1.6;
        }
        h1 { font-size: 1.4rem; font-family: var(--font-mono); margin-bottom: 24px; color: var(--accent); }
        h2 { font-size: 1.0rem; font-family: var(--font-mono); margin-top: 24px; margin-bottom: 12px; color: var(--text-primary); border-bottom: 1px solid var(--border); padding-bottom: 6px; }
        p, li { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 8px; }
        ul { padding-left: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.8rem; font-family: var(--font-mono); }
        th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
        th { color: var(--text-primary); background: var(--surface); }
        td { color: var(--text-secondary); }
        .back-link { display: inline-block; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent); text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
      </style>
    </head>
    <body>
      <a href="/" class="back-link">← Back to ASGARD Grid</a>
      <h1>法的情報 — ASGARD / QLAX</h1>

      <h2>1. 利用規約</h2>
      <p>本規約は、ASGARDおよびQLAXが提供するAPIおよび関連サービス（以下「本サービス」）の利用条件を定めたものです。</p>
      <ul>
        <li>不正アクセスやサービスの運営を妨害する行為を禁止します。</li>
        <li>本サービスのAPIキーやトークンを第三者に無断で譲渡・共有することはできません。</li>
        <li>本サービスは予告なく内容を変更、または一時停止する場合があります。</li>
      </ul>

      <h2>2. プライバシーポリシー</h2>
      <p>本サービスは、ユーザーのプライバシー保護を重要視し、アクセスログやお問い合わせ内容を適切に管理します。法律上の義務がある場合を除き、第三者に個人情報を開示することはありません。</p>

      <h2>3. 特定の商取引に関する措置（特定商取引法に基づく表記）</h2>
      <table>
        <tr><th>アイテム</th><th>詳細</th></tr>
        <tr><td>ベンダー</td><td>QLAX</td></tr>
        <tr><td>オペレーションマネージャー</td><td>樋口大輔 (Daisuke Higuchi)</td></tr>
        <tr><td>所在地 / 連絡先</td><td>福岡県豊前市 (メールまたはお問い合わせフォームより速やかに開示)</td></tr>
        <tr><td>価格</td><td>各プランおよびAPIリクエスト単価に指定されているとおり</td></tr>
        <tr><td>支払方法</td><td>Stripe（クレジットカード）、Solana / EVM / Bitcoin SV (BSV) オンチェーン決済</td></tr>
        <tr><td>サービス提供のタイミング</td><td>決済確認後、速やかに自動付与・提供されます</td></tr>
        <tr><td>返品とキャンセル</td><td>デジタルインフラおよびAPIサービスの性質上、原則として返金・キャンセルはお受けできません。</td></tr>
      </table>
    </body>
    </html>
    """
