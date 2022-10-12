import os
import pytz
import discord
import datetime
import utils.time as Time
from discord.ext import tasks
from discord import app_commands as apc

class Petretro(apc.Group):
    """Comandos relacionados a retrospectiva bisemanal do PET"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.responded = False
        self.flag = 1
        self.retro_day = Time.initialize_date(datetime.date(2022, 1, 28), 14)
        
    @apc.command(name="retro", description="Informa a data da próxima retrospectiva")
    async def retrospective(self, interaction: discord.Integration):
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
    
    async def _set_retrospective(self, interaction: discord.Integration, dia: int, mes: int):
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
            if self.flag == 1:
                self.flag = 0
                await self.turn_off_retrospective.start()
                await self._set_retrospective(interaction=interaction, dia=dia, mes=mes)
            else:
                self.retro_day = datetime.date(
                    int(datetime.date.today().year), int(mes), int(dia))
                self.is_retrospective_eve.start()
                self.flag = 1
                em.add_field(
                    name="**Retrospectiva**",
                    value=f'Retrospectiva manualmente ajustada para a data {self.retro_day.day:02d}/{self.retro_day.month:02d}.'
            	)
            if not self.responded:
                await interaction.response.send_message(embed=em)
                self.responded = True
                return
            self.responded = False
    
    @apc.command(name="manual", description="Define a data da próxima retrospectiva manualmente")
    async def set_retrospective(self, interaction: discord.Integration, dia: int, mes: int):
        await self._set_retrospective(interaction=interaction, dia=dia, mes=mes)
    
    
    @apc.command(name="ferias", description="Desliga os avisos de retrospectiva")
    async def retroFerias(self, interaction: discord.Integration):
        em = discord.Embed(color=0xF0E68C)
        self.turn_off_retrospective.start()
        em.add_field(
            name="**Retrospectiva**",
            value="Bot entrando de férias das retrospectivas! Sem mais avisos ou afins."
        )
        await interaction.response.send_message(embed=em)
    
    # Internal Task: Desliga retro
    @tasks.loop(count=1)
    async def turn_off_retrospective(self):
        self.is_retrospective_eve.cancel()

    # Task: check if today is retrospective eve
    @tasks.loop(hours=1)
    async def is_retrospective_eve(self):
        now = datetime.datetime.now(pytz.timezone('Brazil/East'))
        if self.retro_day == datetime.date.today() + datetime.timedelta(days=1):
            if now.hour == 15:
                self.remember_retrospective.start()
        if self.retro_day == datetime.date.today():
            if now.hour == 23:
                self.update_retro_day.start()

    # Task: send the warning to every petiane
    @tasks.loop(count=1)
    async def remember_retrospective(self):
        channel = self.bot.get_channel(int(os.getenv("WARNING_CHANNEL")))
        await channel.send(f'Atenção, {os.getenv("PETIANES_ID")}!\nLembrando que amanhã é dia de retrospectiva, já aproveitem pra escrever o textos de vocês.')

    # Task: set the retrospective day to 2 weeks later
    @tasks.loop(count=1)
    async def update_retro_day(self):
        self.retro_day += datetime.timedelta(days=14)
        
    @tasks.loop(count=1)
    async def startTasks(self):
        self.is_retrospective_eve.start()
