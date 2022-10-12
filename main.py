import os
from dotenv import load_dotenv
import discord
from discord import app_commands

# SETUP
load_dotenv() # Carrega as variaveis de ambiente para serem usada

# Importa os comandos dos arquivos para adicionarmos depois
import commands.help as Help
import commands.key as Key
MYGUILD = discord.Object(id=os.getenv("SERVER_ID")) # Salva o Id do servidor atual

class MyClient(discord.Client): # Cria o cliente que será usado
    def __init__(self):
        super().__init__(intents=discord.Intents.default()) # Carrega as permissões atuais do bot
        self.synced = False # Seta a variavel de sincronizado para falso, usado para não sincronizar mais de uma vez
        
    async def on_ready(self): # Quando o bot estiver pronto e aceitando comando
        if not self.synced: # Se a variavel for falso ele atuailiza a lista de comandos
            await tree.sync(guild=MYGUILD)
            self.synced = True
        print(f"Logado como {self.user}") # Mensagem de exito!

client = MyClient() # Cria o cliente
tree = app_commands.CommandTree(client) # Cria a arvore de comandos
tree.add_command(Help.Pethelp(client),guild=MYGUILD) # Adiciona o comando de ajuda
tree.add_command(Key.Petkey(client),guild=MYGUILD) # Adiciona o comando de key

client.run(os.getenv("TOKEN")) # Inicia o bot