import discord
from discord import app_commands as apc

from bot import Bot

@Bot.addCommandGroup
class Pethelp(apc.Group): # Cria a classe do comando, que herda de Group, utilizado para agrupar os comandos em subgrupos
    """Ajuda"""
    def __init__(self):
        super().__init__() # Inicializa a classe pai
        
    @apc.command(name="help", description="Mostra todos os commandos do BotPET")
    async def help(self, interaction: discord.Interaction, mostrar: bool = False):
        # Gera a mensagem de ajuda
        em=discord.Embed(title = "**Bem-vinde ao Bot do PET!**", 
                         url="https://github.com/petcomputacaoufrgs/botdopet", 
                         description="Aqui est\u00e1 a lista com todos os comandos dispon\u00edveis.\n",
                         color=0xFFFFFF)
        i = 0
        for commands in Bot.CommandTree.get_commands(guild=discord.Object(id=Bot.Data.Secrets["serverID"])):
            i += 1
            
            string: str = ""
            for command in commands.walk_commands():
                string += f"{command.name}\n"
            em.add_field(
                name=f"**{commands.description}:\n`/{commands.name} <opção>`**", value=string, inline=True)
            if i % 3 == 0:
                em.add_field(name="\u2800", value="\u2800", inline=False)
        
        em.add_field(name="\u2800", value="\u2800", inline=False)
        em.set_thumbnail( url = "https://cdn.discordapp.com/attachments/938858934259822685/945718556732039219/LogoPET_oficial.png") # Adiciona a imagem do PET
        em.add_field(
            name="**Tem alguma outra sugestão para o bot?**",
            value=f'Escreva pra gente no chat <#{Bot.Data.Channels["botRecomendations"]}>! Toda ajuda é sempre bem-vinda 🥰',
            inline=False
        )
        await interaction.response.send_message(embed = em, ephemeral=not mostrar) # Envia a mensagem de ajuda