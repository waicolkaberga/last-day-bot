from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import uvicorn
import os

app = FastAPI()

# ⚠️ REEMPLAZA ESTO CON TU NUEVA PUBLIC KEY DE DISCORD
DISCORD_PUBLIC_KEY = "8b2c80ef2f85cfb0963a85be1f9251c083b4286f0e6ef3f12cb08e6cc84db964"
verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))

def verify_signature(signature, timestamp, body):
    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False

@app.get("/")
async def root():
    return {"status": "NUEVO BOT ONLINE - SISTEMA INICIALIZADO"}

@app.post("/interactions")
async def interactions(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp or not verify_signature(signature, timestamp, body.decode()):
        raise HTTPException(status_code=401)

    payload = await request.json()
    
    # PING de verificación obligatorio de Discord
    if payload["type"] == 1:
        return {"type": 1}

    # Procesador de Comandos Slash
    if payload["type"] == 2:
        command_name = payload["data"]["name"]

        if command_name == "help":
            return {"type": 4, "data": {"content": "☣️ **SISTEMA DESDE CERO ACTIVO** ☣️\nUsa `/ficha crear` para empezar."}}

        elif command_name == "saquear":
            return {"type": 4, "data": {"content": "🎲 Sistema de dados en mantenimiento para la Fase 2."}}

        elif command_name == "ficha":
            return {"type": 4, "data": {"content": "📄 Sistema de almacenamiento en mantenimiento para la Fase 2."}}

    return {"type": 4, "data": {"content": "⚠ Comando no implementado."}}

if __name__ == "__main__":
    # Forzar la ejecución automática del registro al encender el servidor en Railway
    os.system("python register_commands.py")
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
