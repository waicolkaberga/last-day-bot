import requests

# ⚠️ REEMPLAZA ESTOS TRES DATOS CON LOS TUYOS PROPIOS
APPLICATION_ID = "1508204657087090878"
BOT_TOKEN = "MTUwODIwNDY1NzA4NzA5MDg3OA.GFxhWk.NVASAcYq6KTMwT1n_oGOdl_WNo0D3i324_S_C0"
GUILD_ID = "1507973620130123806" 

url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"
headers = {"Authorization": f"Bot {BOT_TOKEN}"}

commands = [
    {
        "name": "help",
        "description": "Muestra la guía de comandos de supervivencia"
    },
    {
        "name": "ficha",
        "description": "Gestiona tus personajes (Slot 1 y Slot 2)",
        "options": [
            {
                "name": "crear",
                "description": "Crea un personaje en el rol",
                "type": 1,
                "options": [
                    {"name": "slot", "description": "Selecciona el slot", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]},
                    {"name": "nombre", "description": "Nombre del personaje", "type": 3, "required": True},
                    {"name": "edad", "description": "Edad", "type": 4, "required": True},
                    {"name": "profesion", "description": "Escribe la profesión (Ej: VETERANO, MEDICO)", "type": 3, "required": True}
                ]
            },
            {
                "name": "ver",
                "description": "Mira una ficha técnica",
                "type": 1,
                "options": [
                    {"name": "slot", "description": "Selecciona el slot", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]},
                    {"name": "usuario", "description": "Usuario a consultar", "type": 6, "required": False}
                ]
            }
        ]
    },
    {
        "name": "saquear",
        "description": "Busca recursos usando un dado 1d100",
        "options": [
            {"name": "zona", "description": "Lugar a registrar", "type": 3, "required": True}
        ]
    }
]

response = requests.put(url, headers=headers, json=commands)
print("Status Code:", response.status_code)
print("Response:", response.json())
