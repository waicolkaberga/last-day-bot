from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import uvicorn
import os
import json
import random

app = FastAPI()

DISCORD_PUBLIC_KEY = "c35fe088cb4a969777c8541168680720ecdf202bfe45dfee68378c225dfd099a"
verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))

DB_FILE = "database.json"

PROFESIONES = {
    "SOCIOPATA": {"puntos": 0, "stats": {"Arma blanca": 2, "Sigilo": 1, "Carrera": 1}, "limit": ["Incapacidad de confiar plenamente", "Reacciones impulsivas bajo tensión", "Dificultades para mantener vínculos"]},
    "VETERANO": {"puntos": -8, "stats": {"Puntería": 2, "Recarga": 3}, "limit": ["TEPT", "Insensible"]},
    "TIRADOR DE OPERACIONES ESPECIALES": {"puntos": -3, "stats": {"Puntería": 6, "Recarga": 6, "Estado físico": 1, "Fuerza": 2}, "limit": ["Alta especialización", "Dependencia de equipamiento adecuado", "Exposición a roles de alto riesgo"], "nota": "🔒 ÚNICAMENTE POR SORTEO"},
    "MILITAR ACTIVO": {"puntos": -6, "stats": {"Puntería": 3, "Recarga": 2, "Estado físico": 2, "Fuerza": 1, "Correr": 2}, "limit": ["Dependencia de disciplina táctica", "Dificultad para improvisar sin liderazgo", "Mayor exposición a conflictos armados"], "nota": "🔒 ALIANZAS / 4 BOOSTEOS"},
    "JEFE DE MAFIA": {"puntos": -4, "stats": {"Puntería": 1, "Recarga": 2, "Estado físico": 1, "Correr": 1}, "limit": ["Alta exposición a traiciones", "Dificultad para confiar", "Resolución mediante violencia"], "nota": "🔒 ALIANZAS"},
    "ATLETA DE PARKOUR": {"puntos": -1, "stats": {"Estado físico": 2, "Rebuscar": 2, "Trampas": 2, "Fuerza": 1, "Sigilo": 1}, "limit": ["Alto desgaste físico", "Dependencia de espacios urbanos", "Menor efectividad en combate directo"], "nota": "🔒 2 SERVER BOOSTS"},
    "MIEMBRO SWAT": {"puntos": -5, "stats": {"Puntería": 2, "Recarga": 2, "Sigilo": 2, "Carrera": 2, "Pies ligeros": 1}, "limit": ["Exigencia física y mental constante", "Dependencia de coordinación en equipo", "Menor adaptabilidad sin planificación"], "nota": "🔒 ÚNICAMENTE CON BOOSTEOS"},
    "PANDILLERO": {"puntos": -6, "stats": {"Puntería": 1, "Buscar": 2, "Carrera": 1, "Sigilo": 1}, "limit": ["Tendencia violenta", "Baja confianza en autoridades", "Riesgo de atraer problemas por su pasado"]},
    "BOMBERO": {"puntos": -3, "stats": {"Carrera": 1, "Estado Físico": 1, "Fuerza": 1, "Hacha": 1}, "limit": ["Alto desgaste físico", "Dependencia de trabajo en equipo", "Mayor exposición al riesgo"]},
    "AGENTE DE POLICIA": {"puntos": -4, "stats": {"Destreza": 1, "Puntería": 1, "Recarga": 2}, "limit": ["Trauma psicológico por caída del orden", "Dependencia de estructura", "Menor adaptación al caos"]},
    "GUARDIA FORESTAL": {"puntos": -4, "stats": {"Trampas": 3, "Hacha": 1, "Sigilo": 1}, "limit": ["Rendimiento reducido en zonas urbanas", "Dependencia del terreno natural", "Menor eficacia en combate abierto"]},
    "CARPINTERO": {"puntos": -4, "stats": {"Carpintería": 3, "Arma corta contundente": 1}, "limit": ["Dependencia de materiales", "Menor eficacia sin preparación", "Valor condicionado al grupo"]},
    "LADRON": {"puntos": -6, "stats": {"Destreza": 1, "Pies ligeros": 2, "Sigilo": 2, "Buscar": 1}, "limit": ["Baja eficacia en combate directo", "Dependencia de oportunidades", "Riesgo elevado si es descubierto"]},
    "PESCADOR": {"puntos": -2, "stats": {"Pesca": 3}, "limit": ["Dependencia de cuerpos de agua", "Baja utilidad urbana", "Recursos limitados sin agua"]},
    "MEDICO": {"puntos": -4, "stats": {"Primeros Auxilios": 3, "Arma de hoja corta": 1}, "limit": ["Dependencia de suministros médicos", "Alto valor estratégico (Objetivo prioritario)", "Poco enfoque en combate directo"]},
    "LEÑADOR": {"puntos": -2, "stats": {"Fuerza": 1, "Hacha": 2}, "limit": ["Dependencia de herramientas", "Menor eficacia a distancia", "Estilo puramente físico"]},
    "MONITOR FITNESS": {"puntos": -6, "stats": {"Carrera": 2, "Estado Físico": 3}, "limit": ["Mantenimiento constante de condición", "Desgaste más rápido sin descanso", "Penalización por mala alimentación"]},
    "MECANICO": {"puntos": -4, "stats": {"Mecánica": 3, "Armas cortas contundentes": 1}, "limit": ["Dependencia de herramientas", "Eficacia disminuida sin recursos", "No sobresale en combate directo"]},
    "CAZADOR": {"puntos": -6, "stats": {"Puntería": 1, "Armas blancas cortas": 2, "Trampas": 1}, "limit": ["Desventaja contra grupos grandes", "Eficacia reducida sin rastros", "Dependencia de la observación"]}
}

TABLA_NIVELES = [
    {"lv": 1, "req": 100}, {"lv": 2, "req": 300}, {"lv": 3, "req": 500},
    {"lv": 4, "req": 700}, {"lv": 5, "req": 900}, {"lv": 6, "req": 1000}
]

def load_db():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def verify_signature(signature, timestamp, body):
    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError: return False

@app.get("/")
async def root(): return {"status": "LAST DAY ON EARTH BOT ONLINE"}

@app.post("/interactions")
async def interactions(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp or not verify_signature(signature, timestamp, body.decode()):
        raise HTTPException(status_code=401)

    payload = await request.json()
    if payload["type"] == 1: return {"type": 1}

    if payload["type"] == 2:
        command_name = payload["data"]["name"]
        user_id = payload["member"]["user"]["id"]
        
        db = load_db()
        if user_id not in db: db[user_id] = {"slot1": None, "slot2": None}

        # HELP COMMAND
        if command_name == "help":
            return {"type": 4, "data": {"content": "☣ **LAST DAY ON EARTH ROLEPLAY** ☣\n\n• `/ficha crear` - Registra tu PJ (Slot 1 o 2)\n• `/ficha ver` - Muestra los stats de un superviviente\n• `/ficha reiniciar` - Borra un personaje\n• `/supervivencia estado` - Mira tu Hambre y Sed\n• `/supervivencia consumir` - Come o bebe agua\n• `/saquear` - Lanza un dado 1d100 en una zona\n• `/xp ganar` - Da experiencia (Staff)"}}

        # FICHA COMMAND
        elif command_name == "ficha":
            subcommand = payload["data"]["options"][0]["name"]
            sub_opts = payload["data"]["options"][0].get("options", [])
            opts = {o["name"]: o["value"] for o in sub_opts}
            slot_key = f"slot{opts.get('slot')}"

            if subcommand == "crear":
                prof_input = opts["profesion"].upper().strip()
                if prof_input not in PROFESIONES:
                    return {"type": 4, "data": {"content": f"❌ Profesión '{prof_input}' inválida. Escríbela bien y en mayúsculas.", "flags": 64}}
                
                skills_base = {"Puntería": 0, "Recarga": 0, "Fuerza": 0, "Estado físico": 0, "Sigilo": 0, "Carrera": 0, "Correr": 0, "Hacha": 0, "Carpintería": 0, "Destreza": 0, "Pies ligeros": 0, "Buscar": 0, "Rebuscar": 0, "Trampas": 0, "Pesca": 0, "Primeros Auxilios": 0, "Arma blanca": 0, "Arma de hoja corta": 0, "Arma corta contundente": 0, "Armas cortas contundentes": 0, "Armas blancas cortas": 0, "Mecánica": 0}
                for sk, val in PROFESIONES[prof_input]["stats"].items(): skills_base[sk] = val

                db[user_id][slot_key] = {
                    "nombre": opts["nombre"], "edad": opts["edad"], "profesion": prof_input,
                    "apodo": opts.get("apodo", "Ninguno"), "genero": opts.get("genero", "No definido"),
                    "orientacion": opts.get("orientacion", "No definido"), "apariencia": opts.get("apariencia_url", None),
                    "skills_xp": {}, "skills_lv": skills_base, "hambre": 100, "sed": 100
                }
                save_db(db)
                return {"type": 4, "data": {"content": f"✅ **Personaje creado con éxito en el Slot {opts['slot']}!** Escribe `/ficha ver` para revisar tus datos."}}

            elif subcommand == "ver":
                target_id = opts.get("usuario", user_id)
                if target_id not in db or not db[target_id].get(slot_key):
                    return {"type": 4, "data": {"content": f"❌ No hay personaje activo en el Slot {opts['slot']}.", "flags": 64}}
                
                char = db[target_id][slot_key]
                p_info = PROFESIONES[char["profesion"]]
                limites = "\n".join([f"• {l}" for l in p_info["limit"]])
                stats_activos = "\n".join([f"• **{k}:** Nivel {v}" for k, v in char["skills_lv"].items() if v > 0])
                if not stats_activos: stats_activos = "• Ninguna habilidad por encima de nivel 0."

                embed = {
                    "title": f"📋 Ficha: {char['nombre']} (Slot {opts['slot']})",
                    "description": f"*\"{char['apodo']}\"*",
                    "color": 0x2f3136,
                    "fields": [
                        {"name": "🧠 Identidad", "value": f"**Edad:** {char['edad']} años\n**Género:** {char['genero']}\n**Orientación:** {char['orientacion']}\n**Profesión:** {char['profesion']} ({p_info['puntos']} Pts)", "inline": False},
                        {"name": "🥫 Vitalidad", "value": f"**Hambre:** {char['hambre']}/100\n**Sed:** {char['sed']}/100", "inline": True},
                        {"name": "⚠️ Limitaciones", "value": limites, "inline": False},
                        {"name": "📈 Habilidades", "value": stats_activos, "inline": False}
                    ]
                }
                if char.get("apariencia"): embed["image"] = {"url": char["apariencia"]}
                return {"type": 4, "data": {"embeds": [embed]}}

            elif subcommand == "reiniciar":
                if not db[user_id].get(slot_key): return {"type": 4, "data": {"content": "❌ El slot ya está vacío.", "flags": 64}}
                db[user_id][slot_key] = None
                save_db(db)
                return {"type": 4, "data": {"content": f"💥 **Slot {opts['slot']} borrado.** Has eliminado al personaje."}}

        # XP COMMAND (STAFF ONLY)
        elif command_name == "xp":
            permissions = int(payload["member"].get("permissions", 0))
            if not (permissions & 0x0000000000002000): # Gestionar Mensajes (Staff)
                return {"type": 4, "data": {"content": "❌ No tienes permisos de Staff para dar experiencia.", "flags": 64}}

            sub_opts = payload["data"]["options"][0]["options"]
            opts = {o["name"]: o["value"] for o in sub_opts}
            target_user = opts["usuario"]
            skill_name = opts["habilidad"]
            xp_add = opts["cantidad"]
            slot_key = f"slot{opts['slot']}"

            if target_user not in db or not db[target_user].get(slot_key):
                return {"type": 4, "data": {"content": "❌ El usuario no tiene ficha creada en ese slot.", "flags": 64}}

            char = db[target_user][slot_key]
            if skill_name not in char["skills_xp"]: char["skills_xp"][skill_name] = 0
            if skill_name not in char["skills_lv"]: char["skills_lv"][skill_name] = 0

            char["skills_xp"][skill_name] += xp_add
            actual_lv = char["skills_lv"][skill_name]
            subio = False

            for n in TABLA_NIVELES:
                if char["skills_xp"][skill_name] >= n["req"] and n["lv"] > actual_lv:
                    if skill_name.lower() == "puntería" and n["lv"] > 5: continue
                    if n["lv"] > 6: continue
                    actual_lv = n["lv"]
                    subio = True

            char["skills_lv"][skill_name] = actual_lv
            db[target_user][slot_key] = char
            save_db(db)

            msg = f"⚔️ **+{xp_add} XP** a la habilidad **{skill_name}** de `{char['nombre']}`.\n• **Total XP:** {char['skills_xp'][skill_name]}\n• **Nivel Actual:** Nivel {char['skills_lv'][skill_name]}"
            if subio: msg += "\n\n🔺 **¡SUBIDA DE NIVEL EN EL ROL!**"
            return {"type": 4, "data": {"content": msg}}

        # SUPERVIVENCIA COMMAND
        elif command_name == "supervivencia":
            subcommand = payload["data"]["options"][0]["name"]
            sub_opts = payload["data"]["options"][0].get("options", [])
            opts = {o["name"]: o["value"] for o in sub_opts}
            slot_key = f"slot{opts['slot']}"

            if not db[user_id].get(slot_key): return {"type": 4, "data": {"content": "❌ No tienes personaje en ese slot.", "flags": 64}}
            char = db[user_id][slot_key]

            if subcommand == "estado":
                alerta = "\n⚠️ *¡Tu personaje está sufriendo debilidad por hambre/sed!*" if (char["hambre"] <= 30 or char["sed"] <= 30) else ""
                return {"type": 4, "data": {"content": f"🥫 **Estado Vital de {char['nombre']}:**\n🍖 **Hambre:** {char['hambre']}/100\n💧 **Sed:** {char['sed']}/100{alerta}"}}

            elif subcommand == "consumir":
                if opts["tipo"] == "comida": char["hambre"] = min(100, char["hambre"] + (opts["cantidad"] * 50))
                else: char["sed"] = min(100, char["sed"] + (opts["cantidad"] * 65))
                db[user_id][slot_key] = char
                save_db(db)
                return {"type": 4, "data": {"content": f"🍽️ **{char['nombre']}** consumió sus suministros y estabilizó sus stats vitales."}}

        # SAQUEAR COMMAND
        elif command_name == "saquear":
            zona = payload["data"]["options"][0]["value"]
            dado = random.randint(1, 100)
            
            if dado <= 20: rareza, color, desc = "🗑️ BASURA", 0x7f8c8d, "Objetos inservibles o chatarra sin valor."
            elif dado <= 30: rareza, color, desc = "👕 OBJETOS BÁSICOS", 0x95a5a6, "Ropa común, armas contundentes improvisadas o comida fresca."
            elif dado <= 50: rareza, color, desc = "🔪 SUMINISTROS COMUNES", 0x3498db, "Armas de filo, herramientas comunes, comida enlatada y pastillas."
            elif dado <= 70: rareza, color, desc = "🩹 EQUIPO ÚTIL", 0x9b59b6, "Balas de bajo calibre, vendas/alcohol, rodilleras y mochilas."
            elif dado <= 80: rareza, color, desc = "⚔️ LOOT AVANZADO", 0xe67e22, "Botiquines completos, armas CaC modificadas y armas de fuego cortas."
            elif dado <= 90: rareza, color, desc = "🔫 LOOT RARO", 0xf1c40f, "Armas de fuego civiles, vehículos comunes o equipo táctico básico."
            elif dado <= 99: rareza, color, desc = "☣️ LOOT MILITAR", 0xe74c3c, "Armas de grado militar, chalecos balísticos, munición avanzada y blindados."
            else: rareza, color, desc = "💀 LOOT EXCEPCIONAL", 0x1abc9c, "Armas especiales únicas (Aprobadas por narrador), vehículos pesados o lotes masivos de balas."

            embed = {
                "title": f"🔍 Saqueo en: {zona.upper()}",
                "color": color,
                "fields": [
                    {"name": "🎲 Dado d100", "value": f"`[ {dado} ]`", "inline": True},
                    {"name": "📦 Calidad", "value": f"**{rareza}**", "inline": True},
                    {"name": "📋 Contenido", "value": f"{desc}\n\n*Nota: El botín debe tener sentido lógico con la zona ({zona}).*", "inline": False}
                ]
            }
            return {"type": 4, "data": {"embeds": [embed]}}

    return {"type": 4, "data": {"content": "⚠ Comando no reconocido."}}

if __name__ == "__main__":
    # Este comando obligará a Railway a ejecutar tu script de registro al encender
    os.system("python register_commands.py") 

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
