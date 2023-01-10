import os
import discord
from discord.ext import tasks
from discord import app_commands as apc
import json
import datetime
from pytz import timezone

from bot import Bot

class Petclock(apc.Group):
    """Comandos do clockify"""
    def __init__(self, bot: discord.Client):
        super().__init__() # Inicializa a classe pai
        self.bot = bot # Define o bot

    @apc.command(name="start", description="Inicia o clockify")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.send_message("Clockify iniciado")
    
    @Bot.addVoiceListener
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        print(f"Mudança de voz de {member.name}")

    # Task: send the warning to every petiane
    @tasks.loop(time=datetime.time(hour=11, minute=54, tzinfo = timezone('America/Sao_Paulo')))
    async def clockify_stats(self):
        if datetime.date.today().weekday() != 4:  # 4 = Friday
            return
        pass

    @tasks.loop(count=1)
    async def startTasks(self):
        self.clockify_stats.start()

