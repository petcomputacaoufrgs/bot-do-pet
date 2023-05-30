import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc
from utils.members import Member

from bot import Bot

@Bot.addCommandGroup
class Petlider(apc.Group):
    """Lideran\u00e7a"""
    def __init__(self):
        super().__init__()
        self.months_names = { "1": "Janeiro", "2": "Fevereiro","3": "Março","4": "Abril","5": "Maio","6": "Junho","7": "Julho","8": "Agosto","9": "Setembro","10": "Outubro","11": "Novembro","12": "Dezembro",}
        
    @apc.command(name="lideres", description="Mostra os líderes do mês")
    async def month_leadership(self, interaction: discord.Interaction, mostrar: bool = False):
        
        if not Bot.Data.Leadership:
            em = discord.Embed(0xFF0000)
            em.add_field(
                name="Erro!",
                value="Não há líderes cadastrados!"
            )
            await interaction.response.send(embed=em, ephemeral=not mostrar)
            return
        
        current_month = datetime.date.today().month
        if str(current_month) not in Bot.Data.Leadership.keys():
            em = discord.Embed(0xFF0000)
            em.add_field(
                name="Erro!",
                value="Não há líderes cadastrados!"
            )
            await interaction.response.send(embed=em, ephemeral=not mostrar)
            return
        
        current_leadership = Bot.Data.Leadership[f'{current_month}']
        em = discord.Embed(0xFDFD96)
        em.add_field(
            title=f"**Liderança:**",
            value=f"Neste mês de {self.months_names[f'{current_month}'].lower()}, o líder é <@{current_leadership[0]}> e o vice é <@{current_leadership[1]}>.\n\nPara os próximos meses:",
            inline=False
        )
        
        for month in range(current_month + 1, 13):
            embed_month = str(month)
            if embed_month in Bot.Data.Leadership.keys():
                next_leadership = Bot.Data.Leadership[embed_month]
                em.add_field(
                    name=f"**{self.months_names[embed_month]}**",
                    value=f"__Líder__: <@{next_leadership[0]}>\n__Vice__: <@{next_leadership[1]}>",
                    inline=False
                )
                
        await interaction.response.send(embed=em, ephemeral=not mostrar)
        
    @apc.command(name="adicionar", description="Adiciona uma dupla à liderança")
    async def addLider(self, interaction: discord.Interaction, mes: int, lider: discord.Member, vice: discord.Member):
        if f'{mes}' not in Bot.Data.Leadership:
            Bot.Data.Leadership[f'{mes}'] = [lider.id, vice.id]
            Bot.Data.Leadership.save()
            await interaction.response.send_message("Adicionado com sucesso!")
        else:
            await interaction.response.send_message("Mês já existe!")
       
    @apc.command(name="remover", description="Remove uma dupla da liderança")
    async def remLider(self, interaction: discord.Interaction, mes: int):
        if f'{mes}' in Bot.Data.Leadership:
            del Bot.Data.Leadership[f'{mes}']
            Bot.Data.Leadership.save()
            await interaction.response.send_message("Removido com sucesso!")
        else:
            await interaction.response.send_message("Mês não existe!")
            
    @apc.command(name="clear", description="Limpa todas as duplas da liderança")
    async def clearLider(self, interaction: discord.Interaction, confirmacao: bool = False):
        if not confirmacao:
            await interaction.response.send_message("Confirmação necessaria para executar esse comando!")
        else:
            Bot.Data.Leadership.clear()
            Bot.Data.Leadership.save()
            await interaction.response.send_message("Lideres do ano deletados!")
        
    @tasks.loop(time=datetime.time(hour=13, tzinfo=Bot.TZ))
    async def leadership_alert(self):
        if not datetime.date.today().day == 1:
            return
        
        leadership = Bot.Data.Leadership[f'{datetime.date.today().month}']
        em = discord.Embed(0xFDFD96)
        em.add_field(
            title=f"**Liderança:**",
            value=f"Nesse mês, nosso ditador passa a ser <@{leadership[0]}> e nosso vice, <@{leadership[1]}>.",
            inline=False
        )
        channel = Bot.get_channel(Bot.Data.Channels["leadership"])
        await channel.send(f'Atenção, <@&{Bot.Data.Roles["petiane"]}>!', embed=em)

    @tasks.loop(count=1)
    async def startTasks(self):
        self.leadership_alert.start()
        