
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Comando(BaseModel):
    texto: str

@app.post("/comando")
async def comando_handler(dado: Comando):
    txt = dado.texto.lower()
    if "hora" in txt:
        return {"resposta": f"Agora são {datetime.now().strftime('%H:%M:%S')}"}
    elif "oi" in txt or "olá" in txt:
        return {"resposta": "Olá! Como posso te ajudar hoje?"}
    else:
        return {"resposta": "Comando não reconhecido."}
