import os
import pytz
import discord
import datetime
import utils.time as Time
from discord.ext import tasks
from discord import app_commands as apc
import json

leadership = Time.read_file("data/leadership.json")
months_names = {
    "1": "Janeiro",
    "2": "Fevereiro",
    "3": "Março",
    "4": "Abril",
    "5": "Maio",
    "6": "Junho",
    "7": "Julho",
    "8": "Agosto",
    "9": "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro",
}

class Petliderança(apc.Group):
    """Comandos de liderança"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @apc.command(name="lideres", description="Mostra os líderes do mês")
    async def month_leadership(self, interaction: discord.Interaction):
        global leadership
        leadership = Time.read_file("data/leadership.json")
        current_month = datetime.date.today().month
        current_leadership = leadership[f'{current_month}']
        em = discord.Embed(
            title=f"**Liderança:**",
            description=f"Neste mês de {months_names[f'{current_month}'].lower()}, o líder é **{current_leadership[0]}** e o vice é **{current_leadership[1]}**.\n\nPara os próximos meses:",
            color=0xFDFD96
        )
        i = 1
        while (current_month+i) <= 12:
            embed_month = current_month + i
            embed_month = str(embed_month)
            next_leadership = leadership[embed_month]
            em.add_field(
                name=f"**{months_names[embed_month]}**",
                value=f"__Líder__: {next_leadership[0]}\n__Vice__: {next_leadership[1]}",
                inline=False
            )
            i += 1
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="adicionar", description="Adiciona uma dupla à liderança")
    async def addLider(self, interaction: discord.Integration, mes: int, lider: str, vice: str):
        global leadership
        if f'{mes}' not in leadership:
            leadership[f'{mes}'] = [lider, vice]
            json.dump(leadership, open("data/leadership.json", "w"))
            await interaction.response.send_message("Adicionado com sucesso!")
        else:
            await interaction.response.send_message("Mês já existe!")
       
    @apc.command(name="remover", description="Remove uma dupla da liderança")
    async def remLider(self, interaction: discord.Integration, mes: int):
        global leadership
        if f'{mes}' in leadership:
            del leadership[f'{mes}']
            json.dump(leadership, open("data/leadership.json", "w"))
            await interaction.response.send_message("Removido com sucesso!")
        else:
            await interaction.response.send_message("Mês não existe!")
        
    @tasks.loop(hours=1)
    async def is_first_day_of_month(self):
        if datetime.date.today().day == 1:
            now = datetime.datetime.now(pytz.timezone('Brazil/East'))
            if now.hour == 13:
                self.disclose_leadership.start()
                
    @tasks.loop(count=1)
    async def disclose_leadership(self):
        data = Time.read_file("data/leadership.json")
        leadership = data[f'{datetime.date.today().month}']
        channel = self.bot.get_channel(int(os.getenv("LEADERSHIP_CHANNEL")))
        await channel.send(f'Atenção, {os.getenv("PETIANES_ID")}!\nNesse mês, nosso ditador passa a ser {leadership[0]} e nosso vice, {leadership[1]}.')
