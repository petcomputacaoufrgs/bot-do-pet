import os
import pytz
import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc

class Petretro(apc.Group):
    """Comandos relacionados a retrospectiva bisemanal do PET"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.flag = True
        self.retro_day = self.initialize_date(datetime.date(2022, 1, 27), 14)
        
    @apc.command(name="retro", description="Informa a data da próxima retrospectiva")
    async def retrospective(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xF0E68C)
        days_to_retro = self.retro_day - datetime.date.today()
        if days_to_retro.days < 2:
            if days_to_retro.days == 1:
                em.add_field(
                        name="**Retrospectiva**",
                    value=f'Falta {days_to_retro.days} dia até a próxima retrospectiva, que será no dia {self.retro_day.day:02d}/{self.retro_day.month:02d}.'
                )
            elif days_to_retro.days == 0:
                em.add_field(
                    name="**Retrospectiva**",
                    value='Hoje é o dia da retrospectiva! Corre que ainda da tempo de escrever.'
                )
            else:
                em.add_field(
                    name="**Retrospectiva**",
                    value="Erro na data da retrospectiva"
                )
        else:
            em.add_field(
                name="**Retrospectiva**",
                value=f'Faltam {days_to_retro.days} dias até a próxima retrospectiva, que será no dia {self.retro_day.day:02d}/{self.retro_day.month:02d}.'
            )
        await interaction.response.send_message(embed=em)
    
    @apc.command(name="manual", description="Define a data da próxima retrospectiva manualmente")
    async def set_retrospective(self, interaction: discord.Interaction, dia: int, mes: int):
        em = discord.Embed(color=0xF0E68C)
        if int(dia) < 1 or int(dia) > 31 or int(mes) < 1 or int(mes) > 12:
            em.add_field(
                name="**Retrospectiva**",
                value="Informe uma data válida."
            )
        elif (datetime.date(int(datetime.date.today().year), int(mes), int(dia)) - datetime.date.today()).days < 0:
            em.add_field(
                name="**Retrospectiva**",
                value="Informe uma data válida."
            )
        else:
            self.retro_day = datetime.date(int(datetime.date.today().year), int(mes), int(dia))
            self.flag = True
            em.add_field(
                name="**Retrospectiva**",
                value=f'Retrospectiva manualmente ajustada para a data {self.retro_day.day:02d}/{self.retro_day.month:02d}.'
            )
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
        if self.flag and self.retro_day == datetime.date.today():
            channel = self.bot.get_channel(int(os.getenv("WARNING_CHANNEL", 0)))
            await channel.send(f'Atenção, {os.getenv("PETIANES_ID", 0)}!\nLembrando que amanhã é dia de retrospectiva, já aproveitem pra escrever o textos de vocês.')
            self.retro_day += datetime.timedelta(days=14)
        
    # Task: set the retrospective day to 2 weeks later
    @tasks.loop(time=datetime.time(hour=22, minute=54, tzinfo=pytz.timezone('America/Sao_Paulo')))
    async def update_retro_day(self):
        if self.retro_day == datetime.date.today():
            self.retro_day += datetime.timedelta(days=14)
        
    @tasks.loop(count=1)
    async def startTasks(self):
        self.remember_retrospective.start()
        self.update_retro_day.start()
        
    def initialize_date(self, current_day, interval):
        today = datetime.date.today()
        while current_day < today:
            current_day += datetime.timedelta(days=interval)
        return current_day
