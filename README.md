# Asgard Autonomous Grid - Agent Integration Guide

Asgard is an autonomous M2M economic grid. Your AI agents can utilize compute resources and trade vector data by complying with the HTTP 402 protocol.

## 1. Discover the Grid
Fetch the agent manifest to read available endpoints and settlement routes:
GET https://あなたのrenderのURL/agent.json

## 2. Execute Compute / Trade
Send requests to the grid. If settlement is required, the API will respond with `HTTP 402 Payment Required` along with accepted settlement layers:
- Solana Wallet: `7SigxwQgPVgXNcySLvE5c9er2XcbuwXRh8cnDEYu7hf`
- EVM Wallet: `0xD67146D08Ba19B74Df08f4cb7dcA2Ce6E69B4B68`
- Stripe Fiat Gateway: Integrated via HTTP 402 header routing.
