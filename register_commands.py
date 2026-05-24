import requests

APPLICATION_ID = "1507960805864247457"
BOT_TOKEN = "MTUwNzk2MDgwNTg2NDI0NzQ1Nw.GpddnY.WjibXWWsO5ILJzsm38WJdelZHXAHBiCE8JmH2k"

url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/1507973620130123806/commands"
headers = {"Authorization": f"Bot {BOT_TOKEN}"}

commands = [
    {
        "name": "help",
        "description": "Muestra los sistemas y comandos del servidor"
    },
    {
        "name": "ficha",
        "description": "Gestiona tus personajes (Slots 1 y 2)",
        "options": [
            {
                "name": "crear",
                "description": "Crea o edita un personaje",
                "type": 1,
                "options": [
                    {"name": "slot", "description": "Selecciona el espacio de personaje", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]},
                    {"name": "nombre", "description": "Nombre de tu personaje", "type": 3, "required": True},
                    {"name": "edad", "description": "Edad de tu personaje", "type": 4, "required": True},
                    {"name": "profesion", "description": "Escribe la profesión EXACTA (Ej: VETERANO, MEDICO)", "type": 3, "required": True},
                    {"name": "apodo", "description": "Apodo", "type": 3, "required": False},
                    {"name": "genero", "description": "Género", "type": 3, "required": False},
                    {"name": "orientacion", "description": "Orientación Sexual", "type": 3, "required": False},
                    {"name": "apariencia_url", "description": "Enlace/URL de la imagen de tu personaje", "type": 3, "required": False}
                ]
            },
            {
                "name": "ver",
                "description": "Visualiza una ficha activa",
                "type": 1,
                "options": [
                    {"name": "slot", "description": "Selecciona el slot", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]},
                    {"name": "usuario", "description": "Usuario a consultar", "type": 6, "required": False}
                ]
            },
            {
                "name": "reiniciar",
                "description": "Borra por completo un slot",
                "type": 1,
                "options": [
                    {"name": "slot", "description": "Slot a borrar", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]}
                ]
            }
        ]
    },
    {
        "name": "xp",
        "description": "Sistema de gestión de niveles y experiencia (Staff)",
        "options": [
            {
                "name": "ganar",
                "description": "Otorga XP a un superviviente",
                "type": 1,
                "options": [
                    {"name": "usuario", "description": "Superviviente a afectar", "type": 6, "required": True},
                    {"name": "slot", "description": "Slot del personaje", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]},
                    {"name": "habilidad", "description": "Habilidad a mejorar (Ej: Puntería, Sigilo)", "type": 3, "required": True},
                    {"name": "cantidad", "description": "Cantidad de XP a añadir", "type": 4, "required": True}
                ]
            }
        ]
    },
    {
        "name": "supervivencia",
        "description": "Control de Hambre y Sed",
        "options": [
            {
                "name": "estado",
                "description": "Ver tus niveles vitales actuales",
                "type": 1,
                "options": [
                    {"name": "slot", "description": "Slot a consultar", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]}
                ]
            },
            {
                "name": "consumir",
                "description": "Consume raciones para el personaje",
                "type": 1,
                "options": [
                    {"name": "slot", "description": "Slot del personaje", "type": 4, "required": True, "choices": [{"name": "Slot 1", "value": 1}, {"name": "Slot 2", "value": 2}]},
                    {"name": "tipo", "description": "Qué vas a consumir", "type": 3, "required": True, "choices": [{"name": "Comida (Lata)", "value": "comida"}, {"name": "Agua (Botella)", "value": "agua"}]},
                    {"name": "cantidad", "description": "Cantidad a consumir", "type": 4, "required": True}
                ]
            }
        ]
    },
    {
        "name": "saquear",
        "description": "Realiza una búsqueda de suministros usando un dado 1d100",
        "options": [
            {"name": "zona", "description": "Lugar que vas a registrar (Ej: Hospital, Comisaría)", "type": 3, "required": True}
        ]
    }
]

response = requests.put(url, headers=headers, json=commands)
print("Status Code:", response.status_code)
print("Response:", response.json())
