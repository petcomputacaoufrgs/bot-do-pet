import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc
from utils.dictjson import dictJSON

from bot import Bot

@Bot.addCommandGroup
class Petlider(apc.Group):
    """Lideran\u00e7a"""
    def __init__(self):
        super().__init__()
        self.months_names = { "1": "Janeiro", "2": "Fevereiro","3": "Março","4": "Abril","5": "Maio","6": "Junho","7": "Julho","8": "Agosto","9": "Setembro","10": "Outubro","11": "Novembro","12": "Dezembro",}
        self.leadership = dictJSON("data/leadership.json")
        
    @apc.command(name="lideres", description="Mostra os líderes do mês")
    async def month_leadership(self, interaction: discord.Interaction, mostrar: bool = False):
        await interaction.response.defer()
        if self.leadership == {}:
            await interaction.followup.send("Não há líderes cadastrados!", ephemeral=not mostrar)
            return
        current_month = datetime.date.today().month
        if str(current_month) not in self.leadership.keys():
            await interaction.followup.send("Não há líderes cadastrados para este mês!", ephemeral=not mostrar)
            return
        
        current_leadership = self.leadership[f'{current_month}']
        em = discord.Embed(
            title=f"**Liderança:**",
            description=f"Neste mês de {self.months_names[f'{current_month}'].lower()}, o líder é **{current_leadership[0]}** e o vice é **{current_leadership[1]}**.\n\nPara os próximos meses:",
            color=0xFDFD96
        )
        while current_month <= 12:
            embed_month = str(current_month)
            if embed_month in self.leadership.keys():
                next_leadership = self.leadership[embed_month]
                em.add_field(
                    name=f"**{self.months_names[embed_month]}**",
                    value=f"__Líder__: {next_leadership[0]}\n__Vice__: {next_leadership[1]}",
                    inline=False
                )
            current_month += 1
            
        await interaction.followup.send(embed=em, ephemeral=not mostrar)
        
    @apc.command(name="adicionar", description="Adiciona uma dupla à liderança")
    async def addLider(self, interaction: discord.Interaction, mes: int, lider: str, vice: str):
        if f'{mes}' not in self.leadership:
            self.leadership[f'{mes}'] = [lider, vice]
            await interaction.response.send_message("Adicionado com sucesso!")
        else:
            await interaction.response.send_message("Mês já existe!")
       
    @apc.command(name="remover", description="Remove uma dupla da liderança")
    async def remLider(self, interaction: discord.Interaction, mes: int):
        if f'{mes}' in self.leadership:
            del self.leadership[f'{mes}']
            await interaction.response.send_message("Removido com sucesso!")
        else:
            await interaction.response.send_message("Mês não existe!")
            
    @apc.command(name="clear", description="Limpa todas as duplas da liderança")
    async def clearLider(self, interaction: discord.Interaction, confirmacao: bool = False):
        if not confirmacao:
            await interaction.response.send_message("Confirmação necessaria para executar esse comando!")
        else:
            self.leadership.clear()
            await interaction.response.send_message("Lideres do ano deletados!")
        
    @tasks.loop(time=datetime.time(hour=13, tzinfo=Bot.TZ))
    async def leadership_alert(self):
        if not datetime.date.today().day == 1:
            return
        
        leadership = self.leadership[f'{datetime.date.today().month}']
        channel = Bot.get_channel(Bot.ENV["LEADERSHIP_CHANNEL"])
        await channel.send(f'Atenção, <@&{Bot.ENV["PETIANES_ID"]}>!\nNesse mês, nosso ditador passa a ser {leadership[0]} e nosso vice, {leadership[1]}.')

    @tasks.loop(count=1)
    async def startTasks(self):
        self.leadership_alert.start()
        