import os
import discord
from discord import app_commands
from utils.env import load_env

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
        activity = discord.Activity(type=discord.ActivityType.watching, name="Use /pet") # Atividade do bot
        super().__init__(intents=intents, activity=activity) # Inicializa o cliente
        # Seta a variavel de sincronizado para falso, usado para não sincronizar mais de uma vez
        self.synced = False

        # Variáveis adicionais
        self.commands = [] # Lista de comandos
        self.voiceListeners = [] # Listener de voz

    
    def addVoiceListener(self, func: callable):
        """Adiciona uma função a ser chamada quando houver conexão num canal de voz"""
        self.voiceListeners.append(func)
    
    async def on_voice_state_update(self, member, before, after):    
        """Função chamada pelo cliente discord quando há atualização no estado de voz de um membro"""
        for listener in self.voiceListeners:
            await listener(member, before, after)

    async def on_ready(self):  # Quando o bot estiver pronto e aceitando comando
        if not self.synced:  # Se a variavel for falso ele atuailiza a lista de comandos
            await CommandTree.sync(guild=TOKENS.GUILD)
            self.synced = True
        
        for command in self.commands: # Para cada comando na lista de comandos
            try: # Tenta registrar o inicializador de tasks
                command.startTasks.start()  # Inicializa as tasks do comando
            except: # Caso não tenha inicializador de tasks
                pass # Passa para o proximo comando
        
        print(f"Logado como {self.user}")  # Mensagem de exito!

Bot = MyClient()  # Cria o cliente que interage com o discord
CommandTree = app_commands.CommandTree(Bot)  # Cria a arvore de comandosBot.cC