import discord
from discord import app_commands as apc
import random
import os
import json
from utils.env import update_env

class Petxingamento(apc.Group):
    """Comandos para xingar o matheus"""
    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot
        with open("data/offenses.json") as f:  # Abre o arquivo de ajuda.json
            # Carrega o arquivo de ajuda para a memoria
            self.data = json.loads(f.read())
        self.offense_list = self.data["offenses"]

    @apc.command(name="matheus", description="não é necessário gastar sua saliva xingando o Matheus, o bot faz isso por você")
    async def offend(self, interaction: discord.Interaction):
        num = random.randint(0, len(self.offense_list)-1)
        await interaction.response.send_message(f"{self.offense_list[num].capitalize()}, <@{os.getenv('MATHEUS_ID', 0)}>")
        
    @apc.command(name="adicionar", description="adicione uma nova forma de ofender o Matheus!")
    async def add_offense(self, interaction: discord.Interaction, xingamento: str):
        em = discord.Embed()
        if xingamento in self.offense_list:
            em.color = 0xFF0000
            em.add_field(
                name="**Adicionar xingamento**",
                value="Esse xingamento já está na lista."
            )
        else:
            self.offense_list.append(xingamento)
            em.color = 0xFF6347
            json.dump(self.data, open("data/offenses.json", "w"))
            em.add_field(
                name="**Adicionar xingamento**",
                value=f'"{xingamento}" foi adicionado à lista!'
            )
        await interaction.response.send_message(embed=em)
    
    @apc.command(name="remover", description="não gostou de algum xingamento? ele nunca mais será usado")
    async def rem_offense(self, interaction: discord.Interaction, xingameto: str):
        em = discord.Embed()
        if xingameto in self.offense_list:
            self.offense_list.remove(xingameto)
            json.dump(self.data, open("data/offenses.json", "w"))
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
            value="\n".join(self.offense_list)
        )
        await interaction.response.send_message(embed=em)
        
