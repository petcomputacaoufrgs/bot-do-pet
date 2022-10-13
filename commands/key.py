import os
import discord
from discord import app_commands as apc
from discord.ext import tasks
from datetime import datetime, time
from pytz import timezone

class Petkey(apc.Group): # Cria a classe do comando, que herda de Group, utilizado para agrupar os comandos em subgrupos
    def __init__(self, bot):
        super().__init__()
        self.bot = bot # Referencia para o proprio bot, caso necessario
        self.location = 0 # Id da pessoa que está atualmente com a chave, 0 = com a tia
        self.lastMessageID = 0 # Id da mensagem mais recente do bot para não ser apagada e causar erro
    
    async def sendMsgChave(self, interaction: discord.Interaction):
        """Função para gerar a mensagem de saida, tambem testa se o canal está correto."""
        def check_rules(message):
                return not (message.id == self.lastMessageID) and (message.pinned == False) # Deleta todas as mensagens que não são a mais recente e não estão pinned
        
        KEYCHANNEL = os.getenv("KEY_CHANNEL") # Pega o Id do canal da chave
        
        if int(interaction.channel.id) != int(KEYCHANNEL): # Testa se o canal é o correto para não apagar errado
            em = discord.Embed(color=0xFF0000) # Gera a mensagem de erropet
            em.add_field(name=f"**Canal Errado!**", value=f"Para comandos relacionados à chave utilize o canal <#{KEYCHANNEL}>", inline=False)
            await interaction.response.send_message(embed = em) # Manda a mensagem
        else:
            em = discord.Embed(color=0xFFFFFF) # Gera a mensagem de saida
            if self.location == 0: # Testa se a chave está com a tia ou algum id de pessoa e gera a saida correta
                local = "Está na recepção. Qualquer coisa, converse com a tia!"
            else:
                local = f"Atualmente está com <@{self.location}>."
            em.add_field(name=f"**Cadê a chave?**", value=local, inline=False)
            await interaction.response.send_message(embed=em) # Manda a mensagem
            self.lastMessageID = interaction.channel.last_message_id # Pega o id da mensagem recem mandada
            await interaction.channel.purge(check=check_rules) # Deleta todas as mensagems que não batem na regra de exclusão
        
    @apc.command(name="chave",description="Verificar aonde a chave da salinha está no momento!")
    async def chave(self, interaction: discord.Interaction):
        await self.sendMsgChave(interaction) # Chama a função para enviar a mensagem
        
    @apc.command(name="peguei",description="Pegar a chave para o usuario atual.")
    async def peguei(self, interaction: discord.Interaction):
        self.location = interaction.user.id # Atualiza o id para o id do usuario que mandou a mensagem
        self.avisa.stop()
        self.avisa.start()
        await self.sendMsgChave(interaction) # Chama a função para enviar a mensagem
        
    @apc.command(name="devolvi",description="Devolve a chave para a tia.")
    async def devolvi(self, interaction: discord.Interaction):
        self.avisa.stop()
        self.location = 0 # Atualiza o id para 0 (id da tia)
        await self.sendMsgChave(interaction) # Chama a função para enviar a mensagem
        
    @apc.command(name="passei",description="Passa a chave para o usuario especificado.")
    async def passei(self, interaction: discord.Interaction, usuario: discord.User):
        usuario.id # Pega o id do usuario
        self.avisa.stop()
        self.avisa.start()
        self.location = usuario.id # Atualiza o id para o id informado na mensagem pela string pessoa, na formatação correta
        await self.sendMsgChave(interaction) # Chama a função para enviar a mensagem
        
    # Loop para avisar da chave esquecida
    @tasks.loop(time=time(hour=17, minute=54, tzinfo=timezone('America/Sao_Paulo'))) # Por algum motivo, se colocamos timezone ele só roda o comando 6 minutos depois
    async def avisa(self):
        channel = self.bot.get_channel(int(os.getenv("KEY_CHANNEL")))
        await channel.send(f"<@{self.location}> vai levar a chave para casa hoje?") # Manda a mensagem avisando que a chave está com alguem