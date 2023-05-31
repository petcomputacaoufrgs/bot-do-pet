import discord
from discord import app_commands as apc
from utils.projects import Project

from bot import Bot

@Bot.addCommandGroup
class Projetos(apc.Group):
    """Projetos"""
    def __init__(self):
        super().__init__()
        
    @apc.command(name="listar", description="Lista os projetos")
    async def listProjects(self, interaction: discord.Interaction, mostrar: bool = False):
        embed = discord.Embed(title="Projetos", color=0xFFFFFF)
        projects: list[Project] = sorted(Bot.Data.Projects.values(), key=lambda x: x.name)
        
        for project in projects:
            embed.add_field(name=project.name, value=f"<@&{project.id}>\n{project.description if project.description is not None else 'Sem descrição'}", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral= not mostrar)
        
    @apc.command(name="projeto", description="Mostra o projeto")
    async def showProject(self, interaction: discord.Interaction, projeto: discord.Role, mostrar: bool = False):
        if projeto.id not in Bot.Data.Projects:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        project: Project = Bot.Data.Projects[projeto.id]
        embed = discord.Embed(title=f"Projeto {project.name}", color=int(project.color))
        embed.add_field(name="ID", value=f"<@&{project.id}>")
        embed.add_field(name="Descrição", value=project.description if project.description is not None else "Sem descrição")
        embed.add_field(name="Lider", value=f"<@{project.leader}>" if project.leader is not None else "Não definido")
        
        members = ""
        for member in project.members:
            members += f"<@{member}>\n"
        if not members:
            members = "Sem membros"
        embed.add_field(name="Membros", value=members)
        
        channels = ""
        for channel in project.channels:
            channels += f"<#{channel}>\n"
        if not channels:
            channels = "Sem canais"
        embed.add_field(name="Canais", value=channels)
        
        await interaction.response.send_message(embed=embed, ephemeral= not mostrar)
        
    @apc.command(name="adicionar", description="Adiciona um projeto")
    async def addProject(self, interaction: discord.Interaction, nome: str, projeto: discord.Role, confirmar: bool = False):
        if projeto.id in Bot.Data.Projects:
            await interaction.response.send_message(f"Projeto {projeto.mention} já existe!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Confirme a adição do projeto {projeto.mention} ao sistema!", ephemeral=True)
            return
        
        project = Project(id=projeto.id, name=nome, color=int(projeto.color))
        Bot.Data.Projects[project.id] = project
        Bot.Data.Projects.save()
        #! Remover ephemeral
        await interaction.response.send_message(f"Projeto {projeto.mention} adicionado!", ephemeral=True)
        
    @apc.command(name="remover", description="Remove um projeto")
    async def removeProject(self, interaction: discord.Interaction, projeto: discord.Role, confirmar: bool = False):
        if projeto.id not in Bot.Data.Projects:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Confirme a remoção do projeto {projeto.mention} do sistema!", ephemeral=True)
            return
        
        nome = Bot.Data.Projects[projeto.id].name
        del Bot.Data.Projects[projeto.id]
        Bot.Data.Projects.save()
        #! Remover ephemeral
        await interaction.response.send_message(f"Projeto {nome} removido!", ephemeral=True)
        
    @apc.command(name="criar", description="Cria um projeto")
    async def createProject(self, interaction: discord.Interaction, nome: str, cor: int, apelido: str = None, confirmar: bool = False):
        if apelido is None:
            apelido = nome
            
        if not confirmar:
            await interaction.response.send_message(f"Confirme a criação do projeto {apelido} no servidor!", ephemeral=True)
            return
        
        server = Bot.get_guild(Bot.Data.Secrets["serverID"])
        project = await server.create_role(name=apelido, colour=cor, mentionable=True, hoist=False)
        
        Bot.Data.Projects[project.id] = Project(id=project.id, name=nome, color=cor)
        Bot.Data.Projects.save()
        #! Remover ephemeral
        await interaction.response.send_message(f"Projeto {project.mention} criado!", ephemeral=True)
        
    @apc.command(name="deletar", description="Deleta um projeto")
    async def deleteProject(self, interaction: discord.Interaction, projeto: discord.Role, confirm: bool = False):
        if projeto.id not in Bot.Data.Projects:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        if not confirm:
            await interaction.response.send_message(f"Confirme a exclusão do projeto {projeto.mention} do servidor!", ephemeral=True)
            return

        nome = Bot.Data.Projects[projeto.id].name
        
        for member in Bot.Data.Projects[projeto.id].members:
            Bot.Data.Members[member].projects.remove(projeto.id)
            
        del Bot.Data.Projects[projeto.id]
        Bot.Data.Projects.save()
        await projeto.delete()
        #! Remover ephemeral
        await interaction.response.send_message(f"Projeto {nome} deletado!", ephemeral=True)
        
    @apc.command(name="modificar", description="Modifica um projeto")
    async def modifyProject(self, interaction: discord.Interaction, projeto: discord.Role, 
                            nome: str = None, descricao: str = None, lider: discord.Member = None, 
                            canal: discord.TextChannel = None, cor: int = None, apelido: str = None, confirmar: bool = False):
        if projeto.id not in Bot.Data.Projects:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Confirme a modificação do projeto {projeto.mention}!", ephemeral=True)
            return
        
        project: Project = Bot.Data.Projects[projeto.id]
        
        if nome is not None:
            project.name = nome
        if cor is not None:
            project.color = cor
            await projeto.edit(color=cor)
        if descricao is not None:
            project.description = descricao
        if lider is not None:
            project.leader = lider.id
        if canal is not None:
            project.channels.append(canal.id)
        if apelido is not None:
            await projeto.edit(name=apelido)
        
        Bot.Data.Projects[project.id] = project
        Bot.Data.Projects.save()
        #! Remover ephemeral
        await interaction.response.send_message(f"Projeto {projeto.mention} modificado!", ephemeral=True)
        
    @apc.command(name="membro", description="Modifica um membro de projeto")
    async def modifyMember(self, interaction: discord.Interaction, projeto: discord.Role, membro: discord.Member, remover: bool = False, confirmar: bool = False):   
        if projeto.id not in Bot.Data.Projects:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        if not confirmar:
            await interaction.response.send_message(f"Confirme a modificação do membro {membro.mention} no projeto {projeto.mention}!", ephemeral=True)
            return
        
        project: Project = Bot.Data.Projects[projeto.id]
        if remover:
            if membro.id not in project.members:
                await interaction.response.send_message(f"Membro {membro.mention} não está no projeto!", ephemeral=True)
                return
            
            if membro.id == project.leader:
                project.leader = None
            
            if project.id in Bot.Data.Members[membro.id].projects:
                Bot.Data.Members[membro.id].projects.remove(project.id)
            if membro.get_role(project.id) is not None:
                await membro.remove_roles(projeto)
                
            project.members.remove(membro.id)
        else:
            if membro.id in project.members:
                await interaction.response.send_message(f"Membro {membro.mention} já está no projeto!", ephemeral=True)
                return
            
            if project.id not in Bot.Data.Members[membro.id].projects:
                Bot.Data.Members[membro.id].projects.append(project.id)
            if membro.get_role(project.id) is None:
                await membro.add_roles(projeto)
    
            project.members.append(membro.id)
        
        Bot.Data.Projects[project.id] = project
        Bot.Data.Projects.save()
        #! Remover ephemeral
        await interaction.response.send_message(f"Membro {membro.mention} modificado no projeto {projeto.mention}!", ephemeral=True)
        
        
        
        
        