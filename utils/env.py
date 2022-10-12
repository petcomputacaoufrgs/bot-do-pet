import os
import discord

def load_env():
    if os.path.isfile(".env"):
        from dotenv import load_dotenv
        load_dotenv()
        
def update_env(key: str, value: str):
    if os.path.isfile(".env"):
        foundKey = False
        with open(".env", "r") as file:
            lines = file.readlines()
        for line in lines:
            if line.startswith(key):
                foundKey = True
                lines[lines.index(line)] = f"{key}={value}" + os.linesep # Adiciona o valor a variavel
                break
        if not foundKey:
            lines.append(f"{key}={value}" + os.linesep)
        with open(".env", "w") as file:
            file.writelines(lines)
    os.environ[key] = value
    

async def UpdateChannel(interaction: discord.Interaction, command: str, key: str, channel: str):
    channelId = channel.replace("<#", "").replace(">", "")  # Formata a string para o id do canal
    update_env(key, channelId)  # Atualiza o arquivo .env
    em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
    em.add_field(name=f"**Canal do comando atualizado!**", value=f"Para comandos relacionados {command} utilize agora o canal <#{channelId}>", inline=False)  # Manda a mensagem de confirmação
    await interaction.response.send_message(embed=em)
