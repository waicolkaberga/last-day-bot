from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import uvicorn
import os

app = FastAPI()

# PUBLIC KEY DE DISCORD
DISCORD_PUBLIC_KEY = "c35fe088cb4a969777c8541168680720ecdf202bfe45dfee68378c225dfd099a"

verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))


def verify_signature(signature, timestamp, body):
    try:
        verify_key.verify(
            f"{timestamp}{body}".encode(),
            bytes.fromhex(signature)
        )
        return True
    except BadSignatureError:
        return False


@app.get("/")
async def root():
    return {"status": "LAST DAY ON EARTH BOT ONLINE"}


@app.post("/interactions")
async def interactions(request: Request):
    body = await request.body()

    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        raise HTTPException(status_code=401)

    if not verify_signature(signature, timestamp, body.decode()):
        raise HTTPException(status_code=401)

    payload = await request.json()

    # Discord verification ping
    if payload["type"] == 1:
        return {"type": 1}

    # Slash Commands
    if payload["type"] == 2:

        command_name = payload["data"]["name"]

        if command_name == "help":
            return {
                "type": 4,
                "data": {
                    "content": (
                        "☣ **LAST DAY ON EARTH** ☣\n\n"
                        "Comandos:\n"
                        "/help\n"
                        "/ficha\n"
                        "/inventario\n"
                        "/stats"
                    )
                }
            }

        elif command_name == "ficha":
            return {
                "type": 4,
                "data": {
                    "content": "📄 No tienes ficha registrada."
                }
            }

        elif command_name == "inventario":
            return {
                "type": 4,
                "data": {
                    "content": "🎒 Inventario vacío."
                }
            }

        elif command_name == "stats":
            return {
                "type": 4,
                "data": {
                    "content": "📊 Stats aún no disponibles."
                }
            }

    return {
        "type": 4,
        "data": {
            "content": "⚠ Comando desconocido."
        }
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)