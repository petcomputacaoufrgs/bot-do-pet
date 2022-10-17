import os
import discord
from discord import app_commands as apc
from discord.ext import tasks
from datetime import time
from pytz import timezone
import utils.buttons as btn
from utils.env import update_env

class Petkey(apc.Group): # Cria a classe do comando, que herda de Group, utilizado para agrupar os comandos em subgrupos
    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot # Referencia para o proprio bot, caso necessario
        self.keyMessageID = int(os.getenv("KEY_MESSAGE"))# ID da mensagem que contem a chave
    
    def check_rules(self, message):
        # Deleta todas as mensagens que não são a mais recente e não estão pinned
        return not (message.id == self.keyMessageID) and (message.pinned == False)
    
    @apc.command(name="clear", description="Limpa o canal da chave") # Cria o comando /petkey clear
    async def clear(self, interaction: discord.Interaction): # Cria a função do comando
        await interaction.response.send_message("Limpando o chat da chave...") # Responde ao comando
        channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL"))) # Pega o canal da chave
        await channel.purge(check=self.check_rules) # Limpa o canal
        
    @apc.command(name="chave", description="Gera a menssagem para o bot criar os botões") # Cria o comando /petkey chave
    async def createKey(self, interaction: discord.Interaction):
        await interaction.response.send_message("Gerando a mensagem da chave...") # Responde ao comando
        try:
            await self.bot.get_channel(int(os.getenv("KEY_CHANNEL"))).get_partial_message(self.keyMessageID).edit(content="Mensagem atualizada!", embed=None, view=None)
            await self.view.stop() # Para a task de atualização da chave
        except:
            pass
        channel = self.bot.get_channel(interaction.channel_id)
        self.keyMessageID = channel.last_message_id
        update_env("KEY_CHANNEL", f"{interaction.channel_id}")
        update_env("KEY_MESSAGE", f"{self.keyMessageID}")
        self.key.restart() # Inicia o loop de atualização da chave
        
    @tasks.loop(count=1)
    async def key(self):
        channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL")))
        try:
            message = await channel.fetch_message(self.keyMessageID)
        except:
            return
        
        self.view = btn.KeyMenu(self.bot)
        em = self.view.MsgChave()
        await message.edit(content="", embed=em, view=self.view)
        await self.view.wait()

    # Loop para avisar da chave esquecida
    @tasks.loop(time=time(hour=17, minute=54, tzinfo=timezone('America/Sao_Paulo'))) # Por algum motivo, se colocamos timezone ele só roda o comando 6 minutos depois
    async def avisa(self):
        if self.view.location != 0:
            channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL")))
            await channel.send(f"<@{self.view.location }> vai levar a chave para casa hoje?", delete_after=60*60*4) # Manda a mensagem avisando que a chave está com alguem
    
    @tasks.loop(time=time(hour=23, minute=54, tzinfo=timezone('America/Sao_Paulo')))
    async def updateNames(self):
        try:
            self.view.stop()
        except:
            pass
        self.key.restart()
    
    @tasks.loop(count=1)
    async def startTasks(self):
        self.avisa.start() # Inicia o loop de avisar da chave esquecida
        self.key.start()
