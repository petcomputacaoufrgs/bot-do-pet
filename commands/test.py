from utils.setup import CommandTree, TOKENS # This is the setup file that you will create, see below.
import discord

@CommandTree.command(name="test", description="Teste de comando", guild = TOKENS.GUILD)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Teste")