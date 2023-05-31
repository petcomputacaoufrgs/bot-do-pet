import discord
from datetime import datetime
from discord import app_commands as apc
from utils.members import Member

from bot import Bot

@Bot.addCommandGroup
class Petiane(apc.Group):
    """Petianes"""
    def __init__(self):
        super().__init__()
    
    @apc.command(name="listar", description="Lista os petianes")
    async def listPetianes(self, interaction: discord.Interaction, cargo: discord.Role = None, mostrar: bool = False):
        if cargo is not None and cargo.id not in [None, Bot.Data.Roles["petiane"], Bot.Data.Roles["expetiane"]]:
            await interaction.response.send_message(f'Escolha entre <@&{Bot.Data.Roles["petiane"]}>, <@&{Bot.Data.Roles["expetiane"]}> ou todos', ephemeral=True)
            return
        
        if cargo is None:
            cargo = [Bot.Data.Roles["petiane"], Bot.Data.Roles["expetiane"]] 
        else:
            cargo = [cargo.id]
            
        petianes: list[Member] = []
        
        for petiane in Bot.Data.Members.values():
            if petiane.role in cargo:
                petianes.append(petiane)

        embed = discord.Embed(title="Membros", color=0xFFFFFF)
        for petiane in petianes:
            embed.add_field(name=petiane.nickname, value=f"<@{petiane.id}>", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral= not mostrar)
            
    @apc.command(name="petiane", description="Mostra o petiane")
    async def showPetiane(self, interaction: discord.Interaction, petiane: discord.Member = None, mostrar: bool = False):
        if petiane is None:
            petiane = interaction.user
        
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral= not mostrar)
            return
        
        petiane: Member = Bot.Data.Members[petiane.id]
        embed = discord.Embed(title=f"Petiane {petiane.nickname}", color=0xFFFFFF)
        embed.add_field(name="ID", value=f"<@{petiane.id}>")
        embed.add_field(name="Cargo", value=f"<@&{petiane.role}>")
        embed.add_field(name="Nome", value=petiane.name if petiane.name is not None else "Não informado")
        embed.add_field(name="Aniversário", value= "Não informado" if petiane.birthday is None else petiane.birthday.strftime("%d/%m"))
        projects = ""
        for project in petiane.projects:
            projects += f"<@&{project}>\n"
        embed.add_field(name="Projetos", value=projects if projects != "" else "Nenhum projeto")
        embed.add_field(name="Canal", value=f"<#{petiane.retro}>" if petiane.retro is not None else "Não informado")
        
        await interaction.response.send_message(embed=embed, ephemeral= not mostrar)
        
    @apc.command(name="adicionar", description="Adiciona um petiane")
    async def addPetiane(self, interaction: discord.Interaction, apelido: str, cargo: discord.Role, petiane: discord.Member = None, confirmar: bool = False):
        if petiane is None:
            petiane = interaction.user
           
        if cargo.id not in [Bot.Data.Roles['petiane'], Bot.Data.Roles['expetiane']]:
            await interaction.response.send_message(f"Cargo {cargo.mention} não é um cargo de petiane!", ephemeral=True)
            return
        
        if petiane.id in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} já existe!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Tem certeza que deseja adicionar o petiane {apelido} ao sistema?", ephemeral=True)
            return
        
        if petiane.get_role(cargo.id) is None:
            await petiane.add_roles(cargo)
        
        new_petiane: Member = Member(id=petiane.id, nickname=apelido, role=cargo.id)
        Bot.Data.Members[new_petiane.id] = new_petiane
        Bot.Data.Members.save()
        #! Remover Ephemeral
        await interaction.response.send_message(f"Petiane {petiane.mention} adicionado com sucesso!", ephemeral=True)
        
    @apc.command(name="remover", description="Remove um petiane")
    async def removePetiane(self, interaction: discord.Interaction, petiane: discord.Member, confirmar: bool = False):
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Tem certeza que deseja remover o petiane {petiane.mention} do sistema?", ephemeral=True)
            return
        
        del Bot.Data.Members[petiane.id]
        Bot.Data.Members.save()
        #! Remover Ephemeral
        await interaction.response.send_message(f"Petiane {petiane.mention} removido com sucesso!", ephemeral=True)
        
    @apc.command(name="cargo", description="Coloca o cargo no usuario")
    async def setRole(self, interaction: discord.Interaction, cargo: discord.Role, petiane: discord.Member = None, confirmar: bool = False):
        if petiane is None:
            petiane = interaction.user
            
        if cargo.id not in [Bot.Data.Roles['petiane'], Bot.Data.Roles['expetiane']]:
            await interaction.response.send_message(f"Cargo {cargo.mention} não é um cargo de petiane!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Tem certeza que deseja colocar o cargo {cargo.mention} no petiane {petiane.mention}?", ephemeral=True)
            return
        
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        server = Bot.get_guild(Bot.Data.Secrets["serverID"])
        role = server.get_role(Bot.Data.Members[petiane.id].role)
        await petiane.remove_roles(role)
        await petiane.add_roles(cargo)
        
        Bot.Data.Members[petiane.id].role = cargo.id
        Bot.Data.Members.save()
        #! Remover Ephemeral
        await interaction.response.send_message(f"Petiane {petiane.mention} adicionado com sucesso!", ephemeral=True)
    
    @apc.command(name="projeto", description="Modifica o projeto do petiane")
    async def Project(self, interaction: discord.Interaction, projeto: discord.Role, remover: bool = False, petiane: discord.Member = None, confirmar: bool = False):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if projeto.id not in Bot.Data.Projects:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Tem certeza que deseja modificar o petiane {petiane.mention} no projeto {projeto.mention}?", ephemeral=True)
            return
        
        if not remover:
            if petiane.get_role(projeto.id) is None:
                await petiane.add_roles(projeto)
                
            if projeto.id not in Bot.Data.Members[petiane.id].projects:
                Bot.Data.Members[petiane.id].projects.append(projeto.id)
                Bot.Data.Members.save()
            
            if projeto.id in Bot.Data.Projects and petiane.id not in Bot.Data.Projects[projeto.id].members:
                Bot.Data.Projects[projeto.id].members.append(petiane.id)
                Bot.Data.Projects.save()
        else:
            if petiane.get_role(projeto.id) is not None:
                await petiane.remove_roles(projeto)
                
            if projeto.id in Bot.Data.Members[petiane.id].projects:
                Bot.Data.Members[petiane.id].projects.remove(projeto.id)
                Bot.Data.Members.save()
                
            if projeto.id in Bot.Data.Projects and petiane.id in Bot.Data.Projects[projeto.id].members:
                Bot.Data.Projects[projeto.id].members.remove(petiane.id)
                Bot.Data.Projects.save()
        
        #! Remover Ephemeral
        await interaction.response.send_message(f"Projeto de {petiane.mention} modificado com sucesso!", ephemeral=True)
        
    @apc.command(name="retro", description="Modifica o canal de retro do petiane")
    async def Retro(self, interaction: discord.Interaction, retro: discord.TextChannel, remover: bool = False, petiane: discord.Member = None, confirmar: bool = False):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Tem certeza que deseja modificar o canal da retro do petiane {petiane.mention}?", ephemeral=True)
            return
        
        if not remover:
            Bot.Data.Members[petiane.id].retro = retro.id
        else:
            Bot.Data.Members[petiane.id].retro = None
        
        Bot.Data.Members.save()
        #! Remover Ephemeral
        await interaction.response.send_message(f"Retro de {petiane.mention} modificado com sucesso!", ephemeral=True)
        
    @apc.command(name="aniversario", description="Modifica o aniversario do petiane")
    async def Birthday(self, interaction: discord.Interaction, dia: int, mes: int, remover: bool = False, petiane: discord.Member = None, confirmar: bool = False):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Tem certeza que deseja modificar o aniversario do petiane {petiane.mention}?", ephemeral=True)
            return
        
        date = datetime(2000, mes, dia, tzinfo=Bot.TZ)
        if not remover:
            Bot.Data.Members[petiane.id].birthday = date
        else:
            Bot.Data.Members[petiane.id].birthday = None
        
        Bot.Data.Members.save()
        #! Remover Ephemeral
        await interaction.response.send_message(f"Aniversario de {petiane.mention} modificado com sucesso!", ephemeral=True)
        
    @apc.command(name="nome", description="Modifica o nome completo do petiane")
    async def FullName(self, interaction: discord.Interaction, nome: str, remover: bool = False, petiane: discord.Member = None, confirmar: bool = False):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in Bot.Data.Members:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Tem certeza que deseja modificar o nome completo do petiane {petiane.mention}?", ephemeral=True)
            return
        
        if not remover:
            Bot.Data.Members[petiane.id].name = nome
        else:
            Bot.Data.Members[petiane.id].name = None
            
        Bot.Data.Members.save()
        #! Remover Ephemeral
        await interaction.response.send_message(f"Nome completo de {petiane.mention} modificado com sucesso!", ephemeral=True)