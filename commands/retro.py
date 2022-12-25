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
        with open("data/retro.json") as f:  # Abre o arquivo de retro.json
            # Carrega o arquivo de nomes para a memoria
            self.petianes: dict = json.loads(f.read())
            
    def getNames(self, date: datetime.date, values: bool = False) -> str:
        with open("data/retro.json") as f:  # Abre o arquivo de retro.json
            # Carrega o arquivo de nomes para a memoria
            self.petianes: dict = json.loads(f.read())
        offset = 0  # offset the list by 0
        # if the week is even
        if date.isocalendar()[1] % 2 == 0:
            offset = 6  # offset the list by 6
        petText = ""  # text to be sent

        # get the petianes of the week
        if values:
            for petiane in list(self.petianes.values())[offset:6+offset]:
                petText += f'{petiane}\n'
        else:
            for petiane in list(self.petianes.keys())[offset:6+offset]:
                petText += f'<@{petiane}>\n'
            
        return petText
    
    @apc.command(name="adicionar", description="Adiciona um petiano a lista de retrospectiva")
    async def adicionar(self, interaction: discord.Interaction, nome: str, id: discord.User):
        if id.id in self.petianes.values():
            await interaction.response.send_message("Petiano já está na lista!", ephemeral=True)
            return
        
        self.petianes[nome] = id.id
        # Salva o arquivo
        json.dump(self.petianes, open("data/birthdays.json", "w"))
        # Envia a mensagem
        await interaction.response.send_message(f"{nome} adicionado à lista com sucesso!")

    @apc.command(name="remover", description="Remove um petiano da lista de retrospectiva")
    async def remover(self, interaction: discord.Interaction, id: discord.User):
        if id.id not in self.petianes.values():
            await interaction.response.send_message("Petiane não está na lista!", ephemeral=True)
            return
        
        for key, value in self.petianes.items():
            if value == id.id:
                del self.petianes[key]
                break
        # Salva o arquivo
        json.dump(self.petianes, open("data/birthdays.json", "w"))
        # Envia a mensagem
        await interaction.response.send_message(f"{id.name} removido da lista com sucesso!")

    @apc.command(name="retro", description="Informa a data da próxima retrospectiva")
    async def retrospective(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xF0E68C)

        today = datetime.datetime.date.today()
        friday = today + datetime.datetime.timedelta((4-today.weekday()) % 7)

        em.add_field(name="**Retrospectiva**",
                     value=f'A proxima retrospectiva será dia {friday.day:02d}/{friday.month:02d}/{friday.year:02d} às 12h.'
                )
        em.add_field(
                    name="Os Petianes dessa semana são",
                    value=self.getNames(friday, False),
                    inline=True
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
    @tasks.loop(time=datetime.time(hour=11, minute=54, tzinfo=pytz.timezone('America/Sao_Paulo')))
    async def remember_retrospective(self):
        if not self.flag or datetime.datetime.today().weekday() != 3:  # 3 = Thursday
            return

        em = discord.Embed(color=0xF0E68C)
        channel = self.bot.get_channel(int(os.getenv("WARNING_CHANNEL", 0)))
        em.add_field(
            name="**Retrospectiva**",
            value=f'Atenção, amanhã é dia de retrospectiva, deixem postado até as 12h para a Erika ler.'
        )
        em.add_field(
            name="Os Petianes dessa semana são",
            value=self.getNames(datetime.datetime.date.today(), True),
            inline=True
        )
        await channel.send(em)

    @tasks.loop(count=1)
    async def startTasks(self):
        self.remember_retrospective.start()
