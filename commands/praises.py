import discord
from discord import app_commands as apc
import random
from utils.env import dictJSON

from bot import Bot

@Bot.addCommandGroup
class Petelogio(apc.Group):
    """Comandos para elogiar os petianos"""

    def __init__(self):
        super().__init__()
        self.data = dictJSON("data/praises.json")

    @apc.command(name="elogiar", description="elogie alguém que fez um bom trabalho recentemente!")
    async def praise(self, interaction: discord.Interaction, usuario: discord.User):
        num = random.randint(0, len(self.data["praises"])-1)
        await interaction.response.send_message(f"{self.data['praises'][num].capitalize()}, <@{usuario.id}>!")

    @apc.command(name="adicionar", description="adicione mais uma forma de falarmos bem dos nossos coleguinhas")
    async def add_praise(self, interaction: discord.Interaction, elogio: str):
        em = discord.Embed()
        if elogio in self.data["praises"]:
            em.color = 0xFF0000
            em.add_field(
                name="**Adicionar elogio**",
                value="Esse elogio já está na lista."
            )
        else:
            self.data["praises"] += [elogio]
            em.color = 0xFF6347
            em.add_field(
                name="**Adicionar elogio**",
                value=f'"{elogio}" foi adicionado à lista!'
            )
        await interaction.response.send_message(embed=em)
    
    @apc.command(name="remover", description="não gostou de algum elogio? só mandar o elogio a ser removido")
    async def rem_praise(self, interaction: discord.Interaction, elogio: str):
        em = discord.Embed()
        if elogio in self.data["praises"]:
            self.data["praises"] -= [elogio]
            em.color = 0xFF6347
            em.add_field(
                name="**Remover elogio**",
                value=f'"{elogio}" foi removido da lista!'
            )
        else:
            em.color = 0xFF0000
            em.add_field(
                name="**Remover elogio**",
                value='Esse elogio não existe.'
            )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="listar", description="lista todos os elogios")
    async def show_praises(self, interaction: discord.Interaction):
        em = discord.Embed()
        em.color = 0xFF6347
        em.add_field(
            name="**Lista de elogios**",
            value="\n".join(self.data["praises"])
        )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="hug", description="demonstre seu carinho por alguém")
    async def show_praises(self, interaction: discord.Interaction, pessoa: discord.User):
        await interaction.response.send_message(f"<@{interaction.user.id}> abraçou beeeeem forte <@{pessoa.id}> <3")
