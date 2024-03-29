import discord
from discord import app_commands as apc

from bot import Bot

@Bot.addCommandGroup
class PetSetEnv(apc.Group):
    """Mudar o ID de Canais"""
    def __init__(self):
        super().__init__()
        
    @apc.command(name="keychannel", description="Seta o canal da chave.")
    async def setKeyChannel(self, interaction: discord.Interaction, canal: discord.channel.TextChannel):
        """Função para setar o canal da chave, apenas o dono do servidor pode usar."""
        Bot.Data.Key['channel'] = canal.id
        Bot.Data.Key.save()
        em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
        em.add_field(name=f"**Canal da Chave atualizado!**",
                value=f"Para os comandos da chave utilize agora o canal <#{canal.id}>", 
                inline=False
                )  # Manda a mensagem de confirmação
        # Envia a mensagem de confirmação
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="warnchannel", description="Seta o canal de avisos.")
    async def setWarnChannel(self, interaction: discord.Interaction, canal: discord.channel.TextChannel):
        """Função para setar o canal de avisos"""
        Bot.Data.Channels['warning'] = canal.id
        Bot.Data.Channels.save()
        em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
        em.add_field(name=f"**Canal da avisos atualizado!**",
                     value=f"Os avisos gerais agora serão no canal <#{canal.id}>",
                     inline=False
                     )  # Manda a mensagem de confirmação
        # Envia a mensagem de confirmação
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="interpetchannel", description="Seta o canal de avisos do interpet.")
    async def setInterChannel(self, interaction: discord.Interaction, canal: discord.channel.TextChannel):
        """Função para setar o canal do interpet"""
        Bot.Data.Channels['interpet'] = canal.id
        Bot.Data.Channels.save()
        em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
        em.add_field(name=f"**Canal de interpet atualizado!**",
                     value=f"Os avisos de interpet agora serão no canal <#{canal.id}>",
                     inline=False
                     )  # Manda a mensagem de confirmação
        # Envia a mensagem de confirmação
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="petianesid", description="Seta o id do cargo para aviso de petianes.")
    async def setPetId(self, interaction: discord.Interaction, cargo: discord.Role):
        """Função para setar o cargo dos petianes"""
        Bot.Data.Roles['petianes'] = cargo.id
        Bot.Data.Roles.save()
        em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
        em.add_field(name=f"**ID dos petines atualizado!**",
                     value=f"Os avisos vão pingar <@&{cargo.id}>",
                     inline=False
                     )  # Manda a mensagem de confirmação
        # Envia a mensagem de confirmação
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="leadershipchannel", description="Seta o canal de avisos de liderença.")
    async def setLiderChannel(self, interaction: discord.Interaction, canal: discord.channel.TextChannel):
        """Função para setar o canal de liderança"""
        Bot.Data.Channels['leadership'] = canal.id
        Bot.Data.Channels.save()
        em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
        em.add_field(name=f"**Canal de liderança atualizado!**",
                     value=f"Os avisos de liderança agora serão no canal <#{canal.id}>",
                     inline=False
                     )  # Manda a mensagem de confirmação
        # Envia a mensagem de confirmação
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="birthdaychannel", description="Seta o canal de avisos de aniversários.")
    async def setAniverChannel(self, interaction: discord.Interaction, canal: discord.channel.TextChannel):
        """Função para setar o canal de aniversarios"""
        Bot.Data.Channels['birthday'] = canal.id
        Bot.Data.Channels.save()
        em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
        em.add_field(name=f"**Canal de aniversários atualizado!**",
                     value=f"Os avisos de Aniversarios agora serão no canal <#{canal.id}>",
                     inline=False
                     )  # Manda a mensagem de confirmação
        # Envia a mensagem de confirmação
        await interaction.response.send_message(embed=em)
    
    @apc.command(name="recommendchannel", description="Seta o canal de recomendações do bot.")
    async def setRecomChannel(self, interaction: discord.Interaction, canal: discord.channel.TextChannel):
        """Função para setar o canal de recomendações do bot"""
        Bot.Data.Channels['botRecomendations'] = canal.id
        Bot.Data.Channels.save()
        em = discord.Embed(color=0xFF00FF)  # Gera a mensagem de resposta
        em.add_field(name=f"**Canal de recomendações do bot atualizado!**",
                     value=f"O canal de recomendações do bot agora é <#{canal.id}>",
                     inline=False
                     )  # Manda a mensagem de confirmação
        # Envia a mensagem de confirmação
        await interaction.response.send_message(embed=em)
        