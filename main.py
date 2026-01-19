from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.router import route_query
from agents.faq_agent import faq_agent
from agents.product_agent import product_agent
from fastapi.staticfiles import StaticFiles



import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# ----------------------------------------
# CORS CONFIGURATION
# ----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"                       # ⚠️ remove in production 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/chat")
def chat(payload: dict):
    query = payload.get("message")
    agent = route_query(query)

    if agent == "FAQ":
        return {"response": faq_agent(query)}
    elif agent == "PRODUCT":
        return {"response": product_agent(query)}
    else:
        return {"response": "Unable to route query."}
