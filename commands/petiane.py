import discord
from datetime import datetime
from discord import app_commands as apc
from utils.members import Member

from bot import Bot

@Bot.addCommandGroup
class Petiane(apc.Group):
    """Comandos para os petianes"""
    def __init__(self):
        super().__init__()
    
    @apc.command(name="petianes", description="Lista os petianes")
    async def listPetianes(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Petianes", color=0xFFFFFF)
        for petiane in Bot.Data.Members.values():
            embed.add_field(name=petiane.nickname, value=f"<@{petiane.id}>", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
            
    @apc.command(name="petiane", description="Mostra o petiane")
    async def showPetiane(self, interaction: discord.Interaction, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
        
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        petiane: Member = Bot.Data.Members[petiane.id]
        embed = discord.Embed(title=f"Petiane {petiane.nickname}", color=0xFFFFFF)
        embed.add_field(name="ID", value=f"<@{petiane.id}>")
        embed.add_field(name="Cargo", value=f"<@&{petiane.role}>")
        embed.add_field(name="Nome", value=petiane.name if petiane.name is not None else "Não definido")
        embed.add_field(name="Aniversário", value= "Não definido" if petiane.birthday is None else petiane.birthday.strftime("%d/%m"))
        projects = ""
        for project in petiane.projects:
            projects += f"<@&{project}>\n"
        embed.add_field(name="Projetos", value=projects if projects != "" else "Nenhum projeto")
        embed.add_field(name="Canal", value=f"<#{petiane.retro}>" if petiane.retro is not None else "Não definido")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @apc.command(name="adicionar", description="Adiciona um petiane")
    async def addPetiane(self, interaction: discord.Interaction, apelido: str, cargo: discord.Role, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
           
        if cargo.id not in Bot.Data.Roles['petiane'] and cargo.id not in Bot.Data.Roles['expetiane']:
            await interaction.response.send_message(f"Cargo {cargo.mention} não é um cargo de petiane!", ephemeral=True)
            return
        
        if petiane.get_role(cargo.id) is None:
            await petiane.add_roles(cargo)
        
        new_petiane: Member = Member(id=petiane.id, nickname=apelido, role=cargo.id)
        Bot.Data.Members[new_petiane.id] = new_petiane
        Bot.Data.Members.save()
        await interaction.response.send_message(f"Petiane {petiane.mention} adicionado com sucesso!", ephemeral=True)
        
    @apc.command(name="remover", description="Remove um petiane")
    async def removePetiane(self, interaction: discord.Interaction, petiane: discord.Member):
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        del Bot.Data.Members[petiane.id]
        Bot.Data.Members.save()
        await interaction.response.send_message(f"Petiane {petiane.mention} removido com sucesso!", ephemeral=True)
        
    @apc.command(name="cargo", description="Coloca o cargo no usuario")
    async def setRole(self, interaction: discord.Interaction, cargo: discord.Role, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if cargo.id not in Bot.Data.Roles['petiane'] and cargo.id not in Bot.Data.Roles['expetiane']:
            await interaction.response.send_message(f"Cargo {cargo.mention} não é um cargo de petiane!", ephemeral=True)
            return
        
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if petiane.get_role(Bot.Data.Roles["petiane"]) is not None:
            petiane.remove_roles(Bot.Data.Roles["petiane"])
            
        if petiane.get_role(Bot.Data.Roles['expetiane']) is not None:
            petiane.remove_roles(Bot.Data.Roles['expetiane'])
        
        if petiane.get_role(cargo.id) is None:
            await petiane.add_roles(cargo)
        
        await interaction.response.send_message(f"Petiane {petiane.mention} adicionado com sucesso!", ephemeral=True)
    
    @apc.command(name="projeto", description="Modifica o projeto do petiane")
    async def Project(self, interaction: discord.Interaction, projeto: discord.Role, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if not remover:
            if petiane.get_role(projeto.id) is None:
                await petiane.add_roles(projeto)
            Bot.Data.Members[petiane.id].projects.append(projeto.id)
            if projeto.id in Bot.Data.Projects and petiane.id not in Bot.Data.Projects[projeto.id].members:
                Bot.Data.Projects[projeto.id].members.append(petiane.id)
        else:
            if petiane.get_role(projeto.id) is not None:
                await petiane.remove_roles(projeto)
            Bot.Data.Members[petiane.id].projects.remove(projeto.id)
            if projeto.id in Bot.Data.Projects and petiane.id in Bot.Data.Projects[projeto.id].members:
                Bot.Data.Projects[projeto.id].members.remove(petiane.id)
        
        Bot.Data.Members.save()
        await interaction.response.send_message(f"Projeto de {petiane.mention} modificado com sucesso!", ephemeral=True)
        
    @apc.command(name="retro", description="Modifica o canal de retro do petiane")
    async def Retro(self, interaction: discord.Interaction, retro: discord.TextChannel, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if not remover:
            Bot.Data.Members[petiane.id].retro = retro.id
        else:
            Bot.Data.Members[petiane.id].retro = None
        
        Bot.Data.Members.save()
        await interaction.response.send_message(f"Retro de {petiane.mention} modificado com sucesso!", ephemeral=True)
        
    @apc.command(name="aniversario", description="Modifica o aniversario do petiane")
    async def Birthday(self, interaction: discord.Interaction, dia: int, mes: int, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        date = datetime(2000, mes, dia, tzinfo=Bot.TZ)
        if not remover:
            Bot.Data.Members[petiane.id].birthday = date
        else:
            Bot.Data.Members[petiane.id].birthday = None
        
        Bot.Data.Members.save()
        await interaction.response.send_message(f"Aniversario de {petiane.mention} modificado com sucesso!", ephemeral=True)
        
    @apc.command(name="nome", description="Modifica o nome completo do petiane")
    async def FullName(self, interaction: discord.Interaction, nome: str, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if not remover:
            Bot.Data.Members[petiane.id].name = nome
        else:
            Bot.Data.Members[petiane.id].name = None
            
        Bot.Data.Members.save()
        
        await interaction.response.send_message(f"Nome completo de {petiane.mention} modificado com sucesso!", ephemeral=True)