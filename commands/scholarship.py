import os
import pytz
import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc

class Petbolsa(apc.Group):
    """Comandos relacionados a retrospectiva bisemanal do PET"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @apc.command(name="retro", description="Informa a data da próxima retrospectiva")
    async def retrospective(self, interaction: discord.Interaction, cpf: int):
        "https://www.fnde.gov.br/consulta-publica/pagamento-bolsa-executado/#/app/consultar//"
        em = discord.Embed(color=0xF0E68C)
        em.add_field(
                name="**Retrospectiva**",
                value=f''
            )
        await interaction.response.send_message(embed=em)
    
