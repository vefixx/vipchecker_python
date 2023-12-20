import requests

token = "MTEzMTI0NzYxODQ2NzU2MTU0Mg.GZG-9C.JS7drreteZIfvL0Sj1DdJlPA-nenJgfGHohIIc"
# https://cdn.discordapp.com/avatars/1131247618467561542/2c5e8c4fa847eaf1076e9ebb14a21f17.png
# url = 'https://discord.com/api/v9/users/@me'
# url = 'https://discord.com/api/v9/users/@me/guilds'
headers = {
    "Authorization": token
}

url = "https://discord.com/api/v9/guilds/1131245472779083858/channels"

response = requests.get(url, headers=headers)

print(response.json())
