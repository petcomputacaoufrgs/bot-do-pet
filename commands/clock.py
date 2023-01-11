import discord
from discord.ext import tasks
from discord import app_commands as apc
import datetime

from bot import Bot

@Bot.addCommandGroup
class Petclock(apc.Group):
    """Comandos do clockify"""
    def __init__(self):
        super().__init__() # Inicializa a classe pai


    @apc.command(name="start", description="Inicia o clockify")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.send_message("Clockify iniciado")
    
    @Bot.addVoiceListener
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        print(f"Mudança de voz de {member.name}")

    # Task: send the warning to every petiane
    @tasks.loop(time=datetime.time(hour=11, minute=54, tzinfo = Bot.TZ))
    async def clockify_stats(self):
        if datetime.date.today().weekday() != 4:  # 4 = Friday
            return
        pass

    @tasks.loop(count=1)
    async def startTasks(self):
        self.clockify_stats.start()

