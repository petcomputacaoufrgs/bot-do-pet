import discord
from datetime import datetime
from discord import app_commands as apc
from utils.members import Member
from utils.dictjson import dictJSON

from bot import Bot

@Bot.addCommandGroup
class Petiane(apc.Group):
    """Comandos para os petianes"""
    def __init__(self):
        super().__init__()
        self.data = dictJSON("data/petianes.json")
    
    @apc.command(name="petianes", description="Lista os petianes")
    async def listPetianes(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Petianes", color=0xFFFFFF)
        for petiane in self.data.values():
            embed.add_field(name=petiane.nickname, value=f"<@{petiane.id}>", inline=False)
        
        await interaction.response.send_message(embed=embed)
            
    @apc.command(name="petiane", description="Mostra o petiane")
    async def showPetiane(self, interaction: discord.Interaction, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
        
        if petiane.id not in self.data:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!")
            return
        
        petiane: Member = self.data[petiane.id]
        embed = discord.Embed(title=f"Petiane {petiane.nickname}", color=0xFFFFFF)
        embed.add_field(name="ID", value=f"<@{petiane.id}>")
        embed.add_field(name="Cargo", value=petiane.role)
        embed.add_field(name="Nome", value=petiane.name if petiane.name is not None else "Não definido")
        embed.add_field(name="Aniversário", value= "Não definido" if petiane.birthday is None else petiane.birthday.strftime("%d/%m"))
        projects = ""
        for project in petiane.projects:
            projects += f"{project}\n"
        embed.add_field(name="Projetos", value=projects)
        embed.add_field(name="Canal", value=f"<#{petiane.retro}>" if petiane.retro != 0 else "Não definido")
        await interaction.response.send_message(embed=embed)
        
    @apc.command(name="adicionar", description="Adiciona um petiane")
    async def addPetiane(self, interaction: discord.Interaction, apelido: str, cargo: discord.Role, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.get_role(cargo.id) is None:
            await petiane.add_roles(cargo)
        
        new_petiane: Member = Member(id=petiane.id, nickname=apelido, role=cargo.id)
        self.data[new_petiane.id] = new_petiane
        self.data.save()
        await interaction.response.send_message(f"Petiane {petiane.mention} adicionado com sucesso!")
        
    @apc.command(name="remover", description="Remove um petiane")
    async def removePetiane(self, interaction: discord.Interaction, petiane: discord.Member):
        if petiane.id not in self.data:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!")
            return
        
        self.data.pop(petiane.id)
        self.data.save()
        await interaction.response.send_message(f"Petiane {petiane.mention} removido com sucesso!")
        
    @apc.command(name="cargo", description="Coloca o cargo no usuario")
    async def setRole(self, interaction: discord.Interaction, cargo: discord.Role, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in self.data:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!")
            return
        
        if petiane.get_role(Bot.ENV["PETIANES_ID"]) is not None:
            petiane.remove_roles(Bot.ENV["PETIANES_ID"])
            
        if petiane.get_role(Bot.ENV["EXPETIANE_ID"]) is not None:
            petiane.remove_roles(Bot.ENV["EXPETIANE_ID"])
        
        if petiane.get_role(cargo.id) is None:
            await petiane.add_roles(cargo)
        
        await interaction.response.send_message(f"Petiane {petiane.mention} adicionado com sucesso!")
    
    @apc.command(name="projeto", description="Modifica o projeto do petiane")
    async def Project(self, interaction: discord.Interaction, projeto: discord.Role, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in self.data:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!")
            return
        
        if not remover:
            if petiane.get_role(projeto.id) is None:
                await petiane.add_roles(projeto)
            self.data[petiane.id].projects.append(projeto.id)
        else:
            if petiane.get_role(projeto.id) is not None:
                await petiane.remove_roles(projeto)
            self.data[petiane.id].projects.remove(projeto.id)
        
        self.data.save()
        await interaction.response.send_message(f"Projeto de {petiane.mention} modificado com sucesso!")
        
    @apc.command(name="retro", description="Modifica o canal de retro do petiane")
    async def Retro(self, interaction: discord.Interaction, retro: discord.TextChannel, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in self.data:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!")
            return
        
        if not remover:
            self.data[petiane.id].retro = retro.id
        else:
            self.data[petiane.id].retro = 0
        
        self.data.save()
        await interaction.response.send_message(f"Retro de {petiane.mention} modificado com sucesso!")
        
    @apc.command(name="aniversario", description="Modifica o aniversario do petiane")
    async def Birthday(self, interaction: discord.Interaction, dia: int, mes: int, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in self.data:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!")
            return
        
        date = datetime(1, mes, dia)
        if not remover:
            self.data[petiane.id].birthday = date
        else:
            self.data[petiane.id].birthday = None
        
        self.data.save()
        await interaction.response.send_message(f"Aniversario de {petiane.mention} modificado com sucesso!")
        
    @apc.command(name="nomecompleto", description="Modifica o nome completo do petiane")
    async def FullName(self, interaction: discord.Interaction, nome: str, remover: bool = False, petiane: discord.Member = None):
        if petiane is None:
            petiane = interaction.user
            
        if petiane.id not in self.data:
            await interaction.response.send_message(f"Petiane {petiane.mention} não encontrado!")
            return
        
        if not remover:
            self.data[petiane.id].name = nome
        else:
            self.data[petiane.id].name = None
            
        self.data.save()
        
        await interaction.response.send_message(f"Nome completo de {petiane.mention} modificado com sucesso!")