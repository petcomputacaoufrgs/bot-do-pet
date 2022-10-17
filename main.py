import os
import discord
from discord import app_commands
from utils.env import load_env
from importlib import import_module
from inspect import getmembers, isclass

# SETUP
load_env()  # Carrega as variaveis de ambiente para serem usada

# Salva os Tokens utilizados pelo bot
class TOKENS:
    # Salva o Id do servidor atual
    GUILD = discord.Object(id=os.getenv("SERVER_ID", 0))
    SERVER = os.getenv("TOKEN", 0)


class MyClient(discord.Client):  # Cria o cliente que será usado
    def __init__(self):
        # Carrega as permissões atuais do bot
        intents = discord.Intents.default()
        intents.members = True # Permite que o bot veja os membros do servidor
        super().__init__(intents=intents)
        # Seta a variavel de sincronizado para falso, usado para não sincronizar mais de uma vez
        self.synced = False
        
    async def on_ready(self):  # Quando o bot estiver pronto e aceitando comando
        if not self.synced:  # Se a variavel for falso ele atuailiza a lista de comandos
            await CommandTree.sync(guild=TOKENS.GUILD)
            self.synced = True
        
        for command in Commands: # Para cada comando na lista de comandos
            try: # Tenta registrar o inicializador de tasks
                command.startTasks.start()  # Inicializa as tasks do comando
            except: # Caso não tenha inicializador de tasks
                pass # Passa para o proximo comando
        
        print(f"Logado como {self.user}")  # Mensagem de exito!

Bot = MyClient()  # Cria o cliente que interage com o discord
CommandTree = app_commands.CommandTree(Bot)  # Cria a arvore de comandos

Commands = []  # Lista de comandos, inicializada vazia
# Carrega todos os comandos do bot e os adiciona a lista de comandos
for files in os.listdir("commands"): # Para cada arquivo na pasta commands
    if files.endswith(".py"): # Se o arquivo terminar com .py
        module = import_module(f"commands.{files[:-3]}") # Importa o arquivo
        moduleClass = getmembers(module, isclass) # Pega a classe do arquivo
        instance = moduleClass[0][1](Bot) # Cria uma instancia da classe
        Commands.append(instance) # Adiciona a instancia a lista de comandos

for command in Commands: # Para cada comando na lista de comandos
    # Adiciona os comandos na arvore
    CommandTree.add_command(command, guild=TOKENS.GUILD)

Bot.run(TOKENS.SERVER) # Inicia o bot