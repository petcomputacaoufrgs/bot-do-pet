import os
import discord
from discord import app_commands as apc
from discord.ext import tasks
from datetime import datetime, time
from pytz import timezone
import utils.buttons as btn

class Petkey(apc.Group): # Cria a classe do comando, que herda de Group, utilizado para agrupar os comandos em subgrupos
    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot # Referencia para o proprio bot, caso necessario
    
    def check_rules(self, message):
        # Deleta todas as mensagens que não são a mais recente e não estão pinned
        return not (message.id == self.message) and (message.pinned == False)
    
    @apc.command(name="clear", description="Limpa o canal da chave") # Cria o comando /petkey clear
    async def clear(self, interaction: discord.Interaction): # Cria a função do comando
        await interaction.response.send_message("Limpando o chat da chave...") # Responde ao comando
        channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL"))) # Pega o canal da chave
        await channel.purge(check=self.check_rules) # Limpa o canal
        
    @tasks.loop(count=1)
    async def key(self):
        self.view = btn.KeyMenu(self.bot)
        em = self.view.MsgChave()
        channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL")))
        await channel.send(embed=em, view=self.view)
        self.message = channel.last_message_id
        await channel.purge(check=self.check_rules)

    # Loop para avisar da chave esquecida
    @tasks.loop(time=time(hour=17, minute=54, tzinfo=timezone('America/Sao_Paulo'))) # Por algum motivo, se colocamos timezone ele só roda o comando 6 minutos depois
    async def avisa(self):
        if self.view.location != 0:
            channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL")))
            await channel.send(f"<@{self.view.location }> vai levar a chave para casa hoje?", delete_after=60*60*4) # Manda a mensagem avisando que a chave está com alguem
    
    @tasks.loop(count=1)
    async def startTasks(self):
        self.avisa.start() # Inicia o loop de avisar da chave esquecida
        self.key.start()
