# Para comandos agrupos em subgrupos, utilize essa template e chame add_command no main.py
import discord
from discord import app_commands as apc

class PetTEMPLATE(apc.Group):
    """TEMPLATE DE ARQUIVO, SUBSTITUA 'TEMPLATE' PARA USAR"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @apc.command(name="COMMANDNAME", description="COMMAND DESCRIPTION")
    async def COMMANDNAME(self, interaction: discord.Integration):
        # YOUR CODE HERE
        pass

# Para comandos na raiva do projeto, utilize essa template e simplesmente importe o arquivo no main.py
import discord
from utils.setup import CommandTree, TOKENS 

@CommandTree.command(name="test", description="Teste de comando", guild = TOKENS.GUILD)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Teste")