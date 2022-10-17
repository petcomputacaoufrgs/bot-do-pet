import os
import discord
from discord import app_commands as apc
from discord.ext import tasks
from datetime import time
from pytz import timezone
import utils.buttons as btn
from utils.env import update_env


class Petkey(apc.Group):  # Cria a classe do comando, que herda de Group, utilizado para agrupar os comandos em subgrupos
    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot  # Referencia para o proprio bot, caso necessario
        # ID da mensagem que contem a chave
        self.keyMessageID = int(os.getenv("KEY_MESSAGE", 0))

    async def MessageExists(self) -> discord.Message | None:
        channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL", 0)))  # Pega o canal da chave
        try:
            # Pega a mensagem da chave
            message = await channel.fetch_message(self.keyMessageID)
        except:
            return None # Se não encontrar a mensagem, retorna
        
        return message

    def check_rules(self, message):
        # Deleta todas as mensagens que não são a mais recente e não estão pinned
        return not (message.id == self.keyMessageID) and (message.pinned == False)

    # Cria o comando /petkey clear
    @apc.command(name="clear", description="Limpa o canal da chave")
    async def clear(self, interaction: discord.Interaction):  # Cria a função do comando
        # Responde ao comando
        await interaction.response.send_message("Limpando o chat da chave...")
        channel = self.bot.get_channel(
            int(os.getenv("KEY_CHANNEL", 0)))  # Pega o canal da chave
        await channel.purge(check=self.check_rules)  # Limpa o canal

    # Cria o comando /petkey chave
    @apc.command(name="chave", description="Gera a menssagem para o bot criar os botões")
    async def createKey(self, interaction: discord.Interaction):
        # Verifica se o comando foi executado no canal correto
        if interaction.channel_id != int(os.getenv("KEY_CHANNEL", 0)):
            await interaction.response.send_message("Você precisa estar no canal da chave para executar esse comando!", ephemeral=True)
            return  # Sai da função

        # Responde ao comando
        await interaction.response.send_message("Gerando a mensagem da chave...")
        try:
            await self.bot.get_channel(int(os.getenv("KEY_CHANNEL", 0))).get_partial_message(self.keyMessageID).edit(content="Mensagem atualizada!", embed=None, view=None)
            await self.view.stop()  # Para a task de atualização da chave
        except:
            pass  # Se não conseguir editar a mensagem, ignora o erro

        channel = self.bot.get_channel(interaction.channel_id)  # Pega o canal da chave
        # Pega o ID da ultima mensagem enviada
        self.keyMessageID = channel.last_message_id
        update_env("KEY_MESSAGE", f"{self.keyMessageID}")  # Atualiza o .env
        try:
            self.key.start()  # Inicia a task de atualização da chave
        except:
            self.key.restart()  # Inicia o loop de atualização da mensagem da chave

    @apc.command(name="peguei", description="Pega a chave pra ti")
    async def peguei(self, interaction: discord.Interaction):
        message = await self.MessageExists()
        if message is None:
            await interaction.response.send_message("A chave ainda não foi gerada!", ephemeral=True)
            return
            
        self.view.UpdateKey(interaction.user.id) # Marca que o usuário pegou a chave
        await self.view.output(message)  # Atualiza a mensagem da chave
        await interaction.response.send_message("A chave atualizada!", ephemeral=True)
        
    @apc.command(name="passei", description="Passa a chave pra alguem ai.")
    async def passei(self, interaction: discord.Interaction, usuario: discord.User):
        message = await self.MessageExists()
        if message is None:
            await interaction.response.send_message("A chave ainda não foi gerada!", ephemeral=True)
            return
            
        # Marca que o usuário pegou a chave
        self.view.UpdateKey(usuario.id)
        await self.view.output(message)  # Atualiza a mensagem da chave
        await interaction.response.send_message("A chave atualizada!", ephemeral=True)

    @apc.command(name="devolvi", description="Devolve a chave para a tia.")
    async def devolvi(self, interaction: discord.Interaction):
        message = await self.MessageExists()
        if message is None:
            await interaction.response.send_message("A chave ainda não foi gerada!", ephemeral=True)
            return
        
        # Marca que o usuário pegou a chave
        self.view.UpdateKey(0)
        await self.view.output(message)  # Atualiza a mensagem da chave
        await interaction.response.send_message("A chave atualizada!", ephemeral=True)

    # Loop que roda apenas uma vez quando o programa inicia
    @tasks.loop(count=1)
    async def key(self):
        message = await self.MessageExists()
        if message is None:
            return

        self.view = btn.KeyMenu(self.bot)  # Cria a view
        em = self.view.MsgChave()  # Cria a embed
        # Edita a mensagem da chave
        await message.edit(content="", embed=em, view=self.view)
        # Espera a view ser finalizada, para evitar crie duas views ao mesmo tempo
        await self.view.wait()

    # Loop para avisar da chave esquecida
    # Por algum motivo, se colocamos timezone ele só roda o comando 6 minutos depois
    @tasks.loop(time=time(hour=17, minute=54, tzinfo=timezone('America/Sao_Paulo')))
    async def avisa(self):
        if self.view.location != 0:  # Se a chave não estiver na tia
            channel = self.bot.get_channel(
                int(os.getenv("KEY_CHANNEL", 0)))  # Pega o canal da chave
            # Manda a mensagem avisando que a chave está com alguem
            await channel.send(f"<@{self.view.location }> vai levar a chave para casa hoje?", delete_after=60*60*4)

    @tasks.loop(time=time(hour=23, minute=54, tzinfo=timezone('America/Sao_Paulo')))
    async def updateNames(self):  # Loop para atualizar os nomes dos usuarios
        try:  # Tenta atualizar os nomes
            self.view.stop()  # Para a view
        except:
            pass  # Se não tiver view, ignora
        self.key.restart()  # Inicia o loop de atualização da mensagem da chave

    @tasks.loop(count=1)
    async def startTasks(self):
        self.avisa.start()  # Inicia o loop de avisar da chave esquecida
        self.key.start()  # Inicia o loop de atualização da mensagem da chave
