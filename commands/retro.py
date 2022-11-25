import os
from unicodedata import name
import pytz
import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc
import json

class Petretro(apc.Group):
    """Comandos relacionados a retrospectiva bisemanal do PET"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.flag = True
        with open("data/praises.json") as f:  # Abre o arquivo de ajuda.json
            # Carrega o arquivo de ajuda para a memoria
            self.petianes: dict = json.loads(f.read())
        
        
    @apc.command(name="retro", description="Informa a data da próxima retrospectiva")
    async def retrospective(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xF0E68C)
        await interaction.response.send_message(embed=em)
    
    @apc.command(name="ferias", description="Desliga os avisos de retrospectiva")
    async def retroFerias(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xF0E68C)
        self.flag = False   
        em.add_field(
            name="**Retrospectiva**",
            value="Bot entrando de férias das retrospectivas! Sem mais avisos ou afins."
        )
        await interaction.response.send_message(embed=em)

    # Task: send the warning to every petiane
    @tasks.loop(time=datetime.time(hour=14, minute=54, tzinfo=pytz.timezone('America/Sao_Paulo')))
    async def remember_retrospective(self):
        if not self.flag or datetime.datetime.today().weekday() != 3:
            return

        em = discord.Embed(color=0xF0E68C)

        offset = 0
        if datetime.datetime.today().isocalendar()[1] % 2 == 0:
            offset = 6
        petText = ""

        for petiane in list(self.petianes)[0+offset:6+offset]:
            petText += f'<@{self.petianes[petiane]}>\n'

        channel = self.bot.get_channel(int(os.getenv("WARNING_CHANNEL", 0)))
        em.add_field(
            name="**Retrospectiva**",
            value=f'Atenção, amanhã é dia de retrospectiva, deixem postado até as 12h para a Erika ler.'
        )
        em.add_field(
            name="Os Petianes dessa semana são",
            value=petiane,
            inline=True
        )
        await channel.send(em)
        
    @tasks.loop(count=1)
    async def startTasks(self):
        self.remember_retrospective.start()
