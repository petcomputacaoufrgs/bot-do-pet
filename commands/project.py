import discord
from discord import app_commands as apc
from utils.projects import Project
from utils.dictjson import dictJSON

from bot import Bot

@Bot.addCommandGroup
class Projetos(apc.Group):
    """Comandos para os petianes"""
    def __init__(self):
        super().__init__()
        self.data: dictJSON = dictJSON("data/projects.json", dumper=lambda o: o.to_json(), loader=lambda k, v: (int(k), Project.from_json(v)))
        
    @apc.command(name="projetos", description="Lista os projetos")
    async def listProjects(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Projetos", color=0xFFFFFF)
        for project in self.data.values():
            embed.add_field(name=project.name, value=project.description if project.description is not None else "Sem descrição", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @apc.command(name="projeto", description="Mostra o projeto")
    async def showProject(self, interaction: discord.Interaction, projeto: discord.Role):
        if projeto.id not in self.data:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        project: Project = self.data[projeto.id]
        embed = discord.Embed(title=f"Projeto {Project.name}", color=int(project.color))
        embed.add_field(name="ID", value=f"<@&{project.id}>")
        embed.add_field(name="Descrição", value=project.description if project.description is not None else "Não definido")
        embed.add_field(name="Lider", value=f"<@{project.leader}>" if project.leader is not None else "Não definido")
        
        members = ""
        for member in project.members:
            members += f"<@{member}>\n"
        embed.add_field(name="Membros", value=members)
        
        channels = ""
        for channel in project.channels:
            channels += f"<#{channel}>\n"
        embed.add_field(name="Canais", value=channels)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @apc.command(name="adicionar", description="Adiciona um projeto")
    async def addProject(self, interaction: discord.Interaction, nome: str, projeto: discord.Role):
        if projeto.id in self.data:
            await interaction.response.send_message(f"Projeto {projeto.mention} já existe!", ephemeral=True)
            return
        
        project = Project(id=projeto.id, name=nome, color=int(projeto.color))
        self.data[project.id] = project
        self.data.save()
        await interaction.response.send_message(f"Projeto {projeto.mention} adicionado!", ephemeral=True)
        
    @apc.command(name="remover", description="Remove um projeto")
    async def removeProject(self, interaction: discord.Interaction, projeto: discord.Role):
        if projeto.id not in self.data:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        del self.data[projeto.id]
        self.data.save()
        await interaction.response.send_message(f"Projeto {projeto.name} removido!", ephemeral=True)
        
    @apc.command(name="criar", description="Cria um projeto")
    async def createProject(self, interaction: discord.Interaction, nome: str, cor: int, apelido: str = None):
        if apelido is None:
            apelido = nome
        server = Bot.get_guild(Bot.ENV["SERVER_ID"])
        project = await server.create_role(name=apelido, colour=cor, mentionable=True, hoist=False)
        
        self.data[project.id] = Project(id=project.id, name=nome, color=cor)
        self.data.save()
        await interaction.response.send_message(f"Projeto {project.mention} criado!", ephemeral=True)
        
    @apc.command(name="deletar", description="Deleta um projeto")
    async def deleteProject(self, interaction: discord.Interaction, projeto: discord.Role, confirm: bool):
        if projeto.id not in self.data:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        if not confirm:
            await interaction.response.send_message(f"Confirme a exclusão do projeto {projeto.mention}!", ephemeral=True)
            return

        await projeto.delete()
        del self.data[projeto.id]
        self.data.save()
        await interaction.response.send_message(f"Projeto {projeto.mention} deletado!", ephemeral=True)
        
    @apc.command(name="modificar", description="Modifica um projeto")
    async def modifyProject(self, interaction: discord.Interaction, projeto: discord.Role, 
                            nome: str = None, color: int = None, description: str = None,
                            leader: discord.Member = None, channel: discord.TextChannel = None):
        if projeto.id not in self.data:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        project: Project = self.data[projeto.id]
        if nome is not None:
            project.name = nome
        if color is not None:
            project.color = color
        if description is not None:
            project.description = description
        if leader is not None:
            project.leader = leader.id
        if channel is not None:
            project.channels.append(channel.id)
        
        self.data[project.id] = project
        self.data.save()
        await interaction.response.send_message(f"Projeto {projeto.mention} modificado!", ephemeral=True)
        
    @apc.command(name="membro", description="Modifica um membro de projeto")
    async def modifyMember(self, interaction: discord.Interaction, projeto: discord.Role, membro: discord.Member, remover: bool = False):
        if projeto.id not in self.data:
            await interaction.response.send_message(f"Projeto {projeto.mention} não encontrado!", ephemeral=True)
            return
        
        project: Project = self.data[projeto.id]
        if remover:
            if membro.id not in project.members:
                await interaction.response.send_message(f"Membro {membro.mention} não está no projeto!", ephemeral=True)
                return
            project.members.remove(membro.id)
        else:
            if membro.id in project.members:
                await interaction.response.send_message(f"Membro {membro.mention} já está no projeto!", ephemeral=True)
                return
            project.members.append(membro.id)
        
        self.data[project.id] = project
        self.data.save()
        await interaction.response.send_message(f"Membro {membro.mention} modificado no projeto {projeto.mention}!", ephemeral=True)
        
        
        
        
        