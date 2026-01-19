# Gemini Multi-Agent Chatbot

## Agents
1. FAQ Agent (PDF-based RAG)
2. Product Agent (Magento GraphQL)
3. Router Agent (Gemini decides routing)

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```
