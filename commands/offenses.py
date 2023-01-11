import discord
from discord import app_commands as apc
import random
from utils.env import dictJSON

from bot import Bot

@Bot.addCommandGroup
class Petxingamento(apc.Group):
    """Comandos para xingar o matheus"""
    def __init__(self):
        super().__init__()
        self.data = dictJSON("data/offenses.json")

    @apc.command(name="matheus", description="não é necessário gastar sua saliva xingando o Matheus, o bot faz isso por você")
    async def offend(self, interaction: discord.Interaction):
        num = random.randint(0, len(self.offense_list)-1)
        await interaction.response.send_message(f"{self.offense_list[num].capitalize()}, <@{Bot.ENV['MATHEUS_ID']}>")
        
    @apc.command(name="adicionar", description="adicione uma nova forma de ofender o Matheus!")
    async def add_offense(self, interaction: discord.Interaction, xingamento: str):
        em = discord.Embed()
        if xingamento in self.data["offenses"]:
            em.color = 0xFF0000
            em.add_field(
                name="**Adicionar xingamento**",
                value="Esse xingamento já está na lista."
            )
        else:
            self.data["offenses"] += [xingamento]
            em.color = 0xFF6347
            em.add_field(
                name="**Adicionar xingamento**",
                value=f'"{xingamento}" foi adicionado à lista!'
            )
        await interaction.response.send_message(embed=em)
    
    @apc.command(name="remover", description="não gostou de algum xingamento? ele nunca mais será usado")
    async def rem_offense(self, interaction: discord.Interaction, xingameto: str):
        em = discord.Embed()
        if xingameto in self.data["offenses"]:
            self.data["offenses"] -= [xingameto]
            em.color = 0xFF6347
            em.add_field(
                name="**Remover xingamento**",
                value=f'"{xingameto}" foi removido da lista!'
            )
        else:
            em.color = 0xFF0000
            em.add_field(
                name="**Remover xingamento**",
                value='Esse xingamento não existe.'
            )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="listar", description="lista todos os xingamentos disponíveis")
    async def show_offenses(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF6347)
        em.add_field(
            name="**Lista de xingamentos**",
            value="\n".join(self.data["offenses"])
        )
        await interaction.response.send_message(embed=em)
        
