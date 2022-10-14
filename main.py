import os
import discord
from discord import app_commands
from utils.env import load_env

# SETUP
load_env()  # Carrega as variaveis de ambiente para serem usada

# Salva os Tokens utilizados pelo bot
class TOKENS:
    # Salva o Id do servidor atual
    GUILD = discord.Object(id=os.getenv("SERVER_ID"))
    SERVER = os.getenv("TOKEN")


class MyClient(discord.Client):  # Cria o cliente que será usado
    def __init__(self):
        # Carrega as permissões atuais do bot
        super().__init__(intents=discord.Intents.default())
        # Seta a variavel de sincronizado para falso, usado para não sincronizar mais de uma vez
        self.synced = False
        
    async def on_ready(self):  # Quando o bot estiver pronto e aceitando comando
        if not self.synced:  # Se a variavel for falso ele atuailiza a lista de comandos
            await CommandTree.sync(guild=TOKENS.GUILD)
            self.synced = True
        
        for command in Commands:
            try:
                command.startTasks.start()  # Adiciona os subcomando de test
            except:
                pass
        
        print(f"Logado como {self.user}")  # Mensagem de exito!



Bot = MyClient()  # Cria o cliente
CommandTree = app_commands.CommandTree(Bot)  # Cria a arvore de comandos

import commands.help as Help
import commands.key as Key
import commands.text_generator as Shks
import commands.offenses as Offenses
import commands.praises as Praises
import commands.setenvvar as SEV
import commands.retro as Retro
import commands.interpet as Interpet
import commands.leader as Leadership
import commands.birthday as Birthdays

Commands =  [
            Help.Pethelp(Bot), Key.Petkey(Bot), 
            Shks.Petshakespear(Bot), Offenses.Petxingamento(Bot), 
            Praises.Petelogio(Bot), SEV.PetSetEnv(Bot), 
            Retro.Petretro(Bot), Interpet.Petinter(Bot), 
            Leadership.Petliderança(Bot), Birthdays.Petaniver(Bot)
            ]

for command in Commands:
    CommandTree.add_command(command, guild=TOKENS.GUILD) # Adiciona os comandos na arvore

Bot.run(TOKENS.SERVER) # Inicia o bot