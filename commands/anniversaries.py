import os
import pytz
import discord
import datetime
import utils.time as Time
from discord.ext import tasks
from discord import app_commands as apc

class Petaniver(apc.Group):
    """Comandos dos aniversarios do pet"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.data = Time.read_file("data/anniversaries.json")
        
    @apc.command(name="aniversario", description="Informa o dia do próximo aniversário")
    async def anniversary(self, interaction: discord.Interaction):
        loop = True
        today = datetime.date.today()
        today += datetime.timedelta(days=1)
        while loop:
            today_formated = today.strftime("%d/%m")
            try:
                birthday_person = self.data[f'{today_formated}']
                loop = False
            except:
                today += datetime.timedelta(days=1)
        em = discord.Embed(color=0xFF8AD2)
        em.add_field(
            name=f"**Aniversário**",
            value=f"O próximo aniversariante é {birthday_person}, no dia {today_formated}.",
            inline=False
        )
        await interaction.response.send_message(embed = em)
        
    @tasks.loop(hours=1)
    async def test_aniversary(self):
        today = datetime.date.today().strftime("%d/%m")
        now = datetime.datetime.now(pytz.timezone('Brazil/East'))
        try:
            if now.hour == 8:
                birthday_person = self.data[f'{today}']
                self.congratulate.start(birthday_person)
        except:
            pass
        
    @tasks.loop(count=1)
    async def congratulate(self, birthday_person):
        channel = self.bot.get_channel(int(os.getenv("ANNIVERSARY_CHANNEL")))
        await channel.send(f'Atenção, {os.getenv("PETIANES_ID")}, pois é dia de festa!\nO aniversariante de hoje é {birthday_person}, não se esqueçam de desejar tudo de bom e mais um pouco.')

    @tasks.loop(count=1)
    async def startTasks(self):
        self.test_aniversary.start()
