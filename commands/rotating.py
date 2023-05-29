import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc
from utils.env import dictJSON
import re

from bot import Bot

@Bot.addCommandGroup
class Petschedule(apc.Group):
    """Agendamento de atividades"""

    def __init__(self):
        super().__init__()
        self.data = dictJSON("data/schedule.json")
        
    @apc.command(name="visualizar", description="Visualiza o agendamento")
    async def view_schedule(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF8AD2)
        em.add_field(
            name="**Agendamento**",
            value=self.schedule_string(),
            inline=False
        )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="adicionar", description="Adiciona uma atividade ao final do agendamento")
    async def add_schedule(self, interaction: discord.Interaction, atividade: discord.Role):
        id = str(atividade.id)
        if id in self.data['schedule']:
            await interaction.response.send_message("Essa atividade já está no agendamento")
            return
        
        self.data['schedule'].append(id)
        self.data.save()
        await interaction.response.send_message("Atividade adicionada ao agendamento")
                
    @apc.command(name="remover", description="Remove uma atividade do agendamento")
    async def rem_schedule(self, interaction: discord.Interaction, atividade: discord.Role):
        id = str(atividade.id)
        if id not in self.data['schedule']:
            await interaction.response.send_message("Essa atividade não está no agendamento")
            return
        
        self.data['schedule'].remove(id)
        self.data.save()
        await interaction.response.send_message("Atividade removida do agendamento")
        
    @apc.command(name="atualizar", description="Atualiza o agendamento")
    async def update_schedule(self, interaction: discord.Interaction, atividade: discord.Role, local: int):
        id = str(atividade.id)
        if id not in self.data['schedule']:
            await interaction.response.send_message("Essa atividade não está no agendamento")
            return
        if local < 1 or local > len(self.data['schedule']):
            await interaction.response.send_message("Local inválido")
            return
        
        local -= 1
        self.data['schedule'].remove(id)
        self.data['schedule'].insert(local, id)
        self.data.save()
        await interaction.response.send_message("Agendamento atualizado")
        
    @apc.command(name="limpar", description="Limpa o agendamento")
    async def clear_schedule(self, interaction: discord.Interaction):
        self.data['schedule'] = []
        self.data.save()
        await interaction.response.send_message("Agendamento limpo")
        
    @apc.command(name="ordenar", description="Ordena o agendamento")
    async def sort_schedule(self, interaction: discord.Interaction, ordem: str = "1 2 3 4 5 6 7"):
        ordemlst: list = [int(i) for i in re.sub(r'[^0-9 ]', '', ordem).split()]
        if len(ordemlst) != len(self.data['schedule']):
            await interaction.response.send_message("Quantidade de atividades inválida")
            return
        if len(set(ordemlst)) != len(ordemlst):
            await interaction.response.send_message("Valores repetidos")
            return
        if min(ordemlst) < 1 or max(ordemlst) > len(ordemlst):
            await interaction.response.send_message("Valores inválidos")
            return
        
        self.data['schedule'] = [self.data['schedule'][i - 1] for i in ordemlst]
        self.data.save()
        await interaction.response.send_message("Agendamento ordenado")
        
    @tasks.loop(time=datetime.time(hour=12, minute=54, tzinfo=Bot.TZ))
    async def warn_schedule(self):
        if datetime.date.today().weekday() != 2 or self.data['num'] == 0:
            return
        
        if self.data['num'] > len(self.data['schedule']):
            self.data['num'] = 0
        
        next_project = self.data['schedule'][self.data['num']]
        em = discord.Embed(color=0xFF8AD2)
        em.add_field(
            name="**Post do Dragão!!**",
            value=f"O próximo projeto é: <@&{next_project}>",
            inline=False
        )
        channel = Bot.get_channel(Bot.ENV["WARNING_CHANNEL"])
        await channel.send(embed=em)
        self.data['num'] = (self.data['num'] + 1) % len(self.data['schedule'])
        
        
    @tasks.loop(count=1)
    async def startTasks(self):
        self.warn_schedule.start()
            
    def schedule_string(self) -> str:
        """Transforma o agendamento em uma string"""
        schedule = f"Proximo número da rotação: {self.data['num'] + 1}\n"
        server = Bot.get_guild(Bot.ENV["SERVER_ID"])
        for count, project in enumerate(self.data['schedule'], 1):
            schedule += f"{count}: {server.get_role(int(project)).name}\n"
        return schedule
    