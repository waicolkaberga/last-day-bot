import requests

APPLICATION_ID = "1507960805864247457"
BOT_TOKEN = "MTUwNzk2MDgwNTg2NDI0NzQ1Nw.GpddnY.WjibXWWsO5ILJzsm38WJdelZHXAHBiCE8JmH2k"

url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}"
}

commands = [
    {
        "name": "help",
        "description": "Ver comandos"
    },
    {
        "name": "ficha",
        "description": "Ver ficha"
    },
    {
        "name": "inventario",
        "description": "Ver inventario"
    },
    {
        "name": "stats",
        "description": "Ver estadísticas"
    }
]

for command in commands:
    response = requests.post(
        url,
        headers=headers,
        json=command
    )

    print(response.status_code)
    print(response.json())