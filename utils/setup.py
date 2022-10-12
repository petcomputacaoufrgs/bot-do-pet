import os
from dotenv import load_dotenv
import discord
from discord import app_commands

# SETUP
load_dotenv() # Carrega as variaveis de ambiente para serem usada

# Salva os Tokens utilizados pelo bot
class TOKENS:
    GUILD = discord.Object(id=os.getenv("SERVER_ID")) # Salva o Id do servidor atual
    SERVER = os.getenv("TOKEN")

class MyClient(discord.Client): # Cria o cliente que será usado
    def __init__(self):
        super().__init__(intents=discord.Intents.default()) # Carrega as permissões atuais do bot
        self.synced = False # Seta a variavel de sincronizado para falso, usado para não sincronizar mais de uma vez
        
    async def on_ready(self): # Quando o bot estiver pronto e aceitando comando
        if not self.synced: # Se a variavel for falso ele atuailiza a lista de comandos
            await CommandTree.sync(guild=TOKENS.GUILD)
            self.synced = True
        print(f"Logado como {self.user}") # Mensagem de exito!

Bot = MyClient() # Cria o cliente
CommandTree = app_commands.CommandTree(Bot) # Cria a arvore de comandos