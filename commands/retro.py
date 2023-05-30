import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc
from math import ceil

from bot import Bot

@Bot.addCommandGroup
class Petretro(apc.Group):
    """Retrospectiva"""
    def __init__(self):
        super().__init__()
            
    def getNames(self, date: datetime.date, values: bool = False) -> str:
        members: list[str] = []
        
        for petiane in Bot.Data.Members.values():
            if petiane.role == Bot.Data.Roles["petiane"]:
                members.append(f'<@{petiane.id}>\n' if values else f'{petiane.nickname}\n')
                
        size = ceil(len(members)/2)
        week = date.isocalendar()[1] % 2 == 0
        # if the week is even get the petianes of the week
        return "".join(petiane for petiane in (members[size:] if week else members[:size]))

    @apc.command(name="retro", description="Informa a data da próxima retrospectiva")
    async def retrospective(self, interaction: discord.Interaction, mostrar: bool = False):
        em = discord.Embed(color=0xF0E68C)

        today = datetime.date.today()
        friday = today + datetime.timedelta((4-today.weekday()) % 7)

        em.add_field(name=f"**Retrospectiva**\n\nA proxima retrospectiva será dia {friday.day:02d}/{friday.month:02d}/{friday.year:02d}.",
                     value="**Os Petianes dessa semana são:**\n" + self.getNames(friday, False)
                )
        await interaction.response.send_message(embed=em, ephemeral=not mostrar)

    @apc.command(name="ferias", description="Desliga/Liga os avisos de retrospectiva")
    async def retroFerias(self, interaction: discord.Interaction, estado: bool):
        em = discord.Embed(color=0xF0E68C)
        Bot.Data.Secrets["flag"] = not estado
        Bot.Data.Secrets.save()
        em.add_field(
            name="**Retrospectiva**",
            value="Bot voltandas das férias das retrospectivas! Devolta com avisos." if Bot.Data.Secrets["flag"] else "Bot entrando de férias das retrospectivas! Sem mais avisos."
        )
        await interaction.response.send_message(embed=em)

    # Task: send the warning to every petiane
    @tasks.loop(time=datetime.time(hour=12, tzinfo = Bot.TZ))
    async def remember_retrospective(self):
        if (not Bot.Data.Secrets["flag"]) or datetime.date.today().weekday() != 4:  # 4 = friday
            return
        channel = Bot.get_channel(Bot.Data.Channels["warning"])
        petText = f"**Retrospectiva**\n\nAtenção, hoje é dia de retrospectiva, deixem postado até segunda para a Erika ler.\n\n**Os Petianes dessa semana são:**\n" + \
            self.getNames(datetime.date.today(), True)
        await channel.send(petText)

    @tasks.loop(count=1)
    async def startTasks(self):
        self.remember_retrospective.start()
