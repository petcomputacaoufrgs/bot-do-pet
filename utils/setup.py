# import os
# import discord
# from discord import app_commands
# from utils.env import load_env

# # SETUP
# load_env() # Carrega as variaveis de ambiente para serem usada

# # Salva os Tokens utilizados pelo bot
# class TOKENS:
#     GUILD = discord.Object(id=os.getenv("SERVER_ID")) # Salva o Id do servidor atual
#     SERVER = os.getenv("TOKEN")

# import commands.test as Test

# class MyClient(discord.Client): # Cria o cliente que será usado
#     def __init__(self):
#         super().__init__(intents=discord.Intents.default()) # Carrega as permissões atuais do bot
#         self.synced = False # Seta a variavel de sincronizado para falso, usado para não sincronizar mais de uma vez
        
#     # async def setup_hook(self):
#     #     Test.Pettest.testmsg.start()  # Adiciona os subcomando de test

#     async def on_ready(self): # Quando o bot estiver pronto e aceitando comando
#         if not self.synced: # Se a variavel for falso ele atuailiza a lista de comandos
#             await CommandTree.sync(guild=TOKENS.GUILD)
#             self.synced = True
#         print(f"Logado como {self.user}") # Mensagem de exito!

# Bot = MyClient() # Cria o cliente
# CommandTree = app_commands.CommandTree(Bot) # Cria a arvore de comandos