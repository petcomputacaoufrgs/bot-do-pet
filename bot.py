import os
import discord
from discord import app_commands
from utils.env import dictJSON

# SETUP
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
        self.ENV = dictJSON(".env")  # Carrega as variaveis de ambiente
        self.classes = [] # Lista de comandos
        self.tasks = (cls.startTasks for cls in self.classes if hasattr(cls, "startTasks"))
        self.voiceListeners: callable = [] # Listener de voz
        self.CommandTree = app_commands.CommandTree(self)  # Cria a arvore de comandosBot.cC
    
    def addVoiceListener(self, func: callable):
        """Adiciona uma função a ser chamada quando houver conexão num canal de voz"""
        self.voiceListeners.append(func)
            
    def addCommandGroup(self, MyClass: callable):
        aClass = MyClass()
        self.classes.append(aClass)
        self.CommandTree.add_command(
            aClass, guild=discord.Object(id=self.ENV["SERVER_ID"]))
    
    async def on_voice_state_update(self, member, before, after):    
        """Função chamada pelo cliente discord quando há atualização no estado de voz de um membro"""
        for listener in self.voiceListeners:
            await listener(member, before, after)

    async def on_ready(self):  # Quando o bot estiver pronto e aceitando comando
        if not self.synced:  # Se a variavel for falso ele atuailiza a lista de comandos
            await self.CommandTree.sync(guild=discord.Object(id=self.ENV["SERVER_ID"]))
            self.synced = True
        # Gera uma lista de comandos que tenham inicializador de tasks
        
        for func in self.tasks:
            func.start()
               
        print(f"Logado como {self.user}")  # Mensagem de exito!

Bot = MyClient()  # Cria o cliente que interage com o discord
