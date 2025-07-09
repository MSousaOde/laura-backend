
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from supabase import create_client
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class Comando(BaseModel):
    texto: str

@app.post("/comando")
async def comando_handler(dado: Comando):
    try:
        prompt = dado.texto
        chat = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        resposta = chat.choices[0].message.content
        supabase.table("historico").insert({
            "mensagem": prompt,
            "resposta": resposta,
            "data": datetime.now().isoformat()
        }).execute()
        return {"resposta": resposta}
    except Exception as e:
        return {"resposta": f"Erro: {str(e)}"}

@app.get("/historico")
async def listar():
    dados = supabase.table("historico").select("*").order("data", desc=True).limit(100).execute()
    return dados.data
