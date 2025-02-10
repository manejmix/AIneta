import json
import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aineta.email_service import periodic_email_check, get_conversations
from aineta.utils import load_mailboxes

# Load mailbox configurations
MAILBOXES = load_mailboxes("mailboxes.json")

# FastAPI setup
app = FastAPI()

origins = [
    "http://localhost:3000",  # frontend
    "http://127.0.0.1:3000",  # alternative frontend address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/start-email-check")
async def start_email_check():
    asyncio.create_task(periodic_email_check(MAILBOXES))
    return {"message": "Started checking emails every 10 seconds."}



# Run the FastAPI app
#if __name__ == "__main__":
  #  import uvicorn
  #  uvicorn.run(app, host="0.0.0.0", port=8000)
