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