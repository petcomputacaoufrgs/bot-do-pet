import os
import discord

def load_env():
    """Função para carregar as variaveis de ambiente"""
    if os.path.isfile(".env"): # Verifica se o arquivo .env existe
        from dotenv import load_dotenv # Importa a função para carregar o arquivo .env
        load_dotenv() # Carrega o arquivo .env
        
def update_env(key: str, value: str): # Função para atualizar o arquivo .env
    if os.path.isfile(".env"): # Verifica se o arquivo .env existe
        foundKey = False # Variavel para verificar se a chave já existe
        with open(".env", "r") as file: # Abre o arquivo .env
            lines = file.readlines() # Lê todas as linhas do arquivo
        for line in lines: # Percorre todas as linhas do arquivo
            if line.startswith(key): # Verifica se a linha começa com a chave
                foundKey = True # Se sim, a chave já existe
                lines[lines.index(line)] = f"{key}={value}" + os.linesep # Adiciona o valor a variavel
                break # Para o loop
        if not foundKey: # Se a chave não existir
            lines.append(f"{key}={value}" + os.linesep) # Adiciona a chave e o valor
        with open(".env", "w") as file: # Abre o arquivo .env
            file.writelines(lines) # Escreve as linhas no arquivo
    os.environ[key] = value # Adiciona a variavel de ambiente
    
async def UpdateChannel(interaction: discord.Interaction, command: str, key: str, channel: str):
    channelId = channel.replace("<#", "").replace(">", "")  # Formata a string para o id do canal
    update_env(key, channelId)  # Atualiza o arquivo .env
    em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
    em.add_field(name=f"**Canal do comando atualizado!**", value=f"Para comandos relacionados {command} utilize agora o canal <#{channelId}>", inline=False)  # Manda a mensagem de confirmação
    await interaction.response.send_message(embed=em) # Envia a mensagem de confirmação
