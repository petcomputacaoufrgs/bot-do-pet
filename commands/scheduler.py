import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc
from re import sub

from bot import Bot

@Bot.addCommandGroup
class Petagenda(apc.Group):
    """Agendamento de atividades"""

    def __init__(self):
        super().__init__()
        
    @apc.command(name="visualizar", description="Visualiza o agendamento")
    async def view_schedule(self, interaction: discord.Interaction, mostrar: bool = False):
        em = discord.Embed(color=0xFF8AD2)
        em.add_field(
            name="**Agendamento**",
            value=self.schedule_string(),
            inline=False
        )
        await interaction.response.send_message(embed=em, ephemeral=not mostrar)
        
    @apc.command(name="adicionar", description="Adiciona uma atividade ao final do agendamento")
    async def add_schedule(self, interaction: discord.Interaction, atividade: discord.Role):
        if atividade.id not in Bot.Data.Projects:
            await interaction.response.send_message("Essa atividade não existe", ephemeral=True)
            return
        
        if atividade.id in Bot.Data.Schedule["projects"]:
            await interaction.response.send_message("Essa atividade já está no agendamento", ephemeral=True)
            return
        
        Bot.Data.Schedule["projects"].append(atividade.id)
        Bot.Data.Schedule.save()
        
        await interaction.response.send_message("Atividade adicionada ao agendamento")
                
    @apc.command(name="remover", description="Remove uma atividade do agendamento")
    async def rem_schedule(self, interaction: discord.Interaction, atividade: discord.Role):
        if atividade.id not in Bot.Data.Projects:
            await interaction.response.send_message("Essa atividade não existe", ephemeral=True)
            return
        
        if atividade.id not in Bot.Data.Schedule["projects"]:
            await interaction.response.send_message("Essa atividade não está no agendamento", ephemeral=True)
            return
        
        Bot.Data.Schedule["projects"].remove(atividade.id)
        Bot.Data.Schedule.save()
        
        await interaction.response.send_message("Atividade removida do agendamento")
        
    @apc.command(name="atualizar", description="Atualiza o agendamento")
    async def update_schedule(self, interaction: discord.Interaction, atividade: discord.Role, local: int):
        if atividade.id not in Bot.Data.Projects:
            await interaction.response.send_message("Essa atividade não existe", ephemeral=True)
            return
        
        if atividade.id not in Bot.Data.Schedule["projects"]:
            await interaction.response.send_message("Essa atividade não está no agendamento", ephemeral=True)
            return
        if local < 1 or local > len(Bot.Data.Schedule["projects"]):
            await interaction.response.send_message("Local inválido", ephemeral=True)
            return
        
        local -= 1
        Bot.Data.Schedule["projects"].remove(atividade.id)
        Bot.Data.Schedule["projects"].insert(local, atividade.id)
        Bot.Data.Schedule.save()
        
        await interaction.response.send_message("Agendamento atualizado")
        
    @apc.command(name="limpar", description="Limpa o agendamento")
    async def clear_schedule(self, interaction: discord.Interaction):
        Bot.Data.Schedule["current"] = 0
        Bot.Data.Schedule["projects"] = []
        Bot.Data.Schedule.save()
        
        await interaction.response.send_message("Agendamento limpo")
        
    @apc.command(name="ordenar", description="Ordena o agendamento")
    async def sort_schedule(self, interaction: discord.Interaction, ordem: str):
        try:
            ordemlst: list = [int(i) for i in sub(r'[^0-9 ]', '', ordem).split()]
        except:
            await interaction.response.send_message("Formato inválido, use \"1 2 3 4 5\"", ephemeral=True)
            return
        
        if len(ordemlst) != len(Bot.Data.Schedule["projects"]):
            await interaction.response.send_message("Quantidade de atividades inválida", ephemeral=True)
            return
        if len(set(ordemlst)) != len(ordemlst):
            await interaction.response.send_message("Valores repetidos", ephemeral=True)
            return
        if min(ordemlst) < 1 or max(ordemlst) > len(ordemlst):
            await interaction.response.send_message("Valores inválidos", ephemeral=True)
            return
        
        Bot.Data.Schedule["projects"] = [Bot.Data.Schedule["projects"][i - 1] for i in ordemlst]
        Bot.Data.Schedule.save()
        await interaction.response.send_message("Agendamento ordenado")
        
    @apc.command(name="link", description="Define o link do formulário")
    async def set_form(self, interaction: discord.Interaction, link: str):
        Bot.Data.Schedule["form_link"] = link
        Bot.Data.Schedule.save()
        await interaction.response.send_message("Link do formulário atualizado")
        
    @tasks.loop(time=datetime.time(hour=14, tzinfo=Bot.TZ))
    async def warn_schedule(self):
        if datetime.date.today().weekday() != 0:
            return
        
        if Bot.Data.Schedule["current"] >= len(Bot.Data.Schedule["projects"]):
            Bot.Data.Schedule["current"] = 0
        
        next_project = Bot.Data.Projects[Bot.Data.Schedule["projects"][Bot.Data.Schedule["current"]]]
        form = Bot.Data.Schedule["form_link"]
        
        em = discord.Embed(color=0xFF8AD2)
        
        em.add_field(
            name="**Post do Dragão!!**",
            value=f"O próximo projeto é: <@&{next_project.id}>\nRespondam o Formulário: {form}",
            inline=False
        )
        
        channel = Bot.get_channel(Bot.Data.Channels["warning"])
        await channel.send(embed=em)
        
        Bot.Data.Schedule["current"] = (Bot.Data.Schedule["current"] + 1) % len(Bot.Data.Schedule["current"])
        Bot.Data.Secrets.save()
        
        
    @tasks.loop(count=1)
    async def startTasks(self):
        self.warn_schedule.start()
            
    def schedule_string(self) -> str:
        """Transforma o agendamento em uma string"""
        schedule = f"Proximo número da rotação: {Bot.Data.Schedule['current'] + 1}\n"
        
        projects = [Bot.Data.Projects[projectid].name for projectid in Bot.Data.Schedule["projects"]]
        
        for count, project in enumerate(projects, 1):
            schedule += f"{count}: {project}\n"
        return schedule
    