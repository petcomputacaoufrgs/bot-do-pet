import discord
from discord import app_commands as apc
import utils.shakespeare as shks


class Petshakespear(apc.Group):
    """Comando para gerar texto com shakespear"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="nome", description="Gera um nome shakespeariano!")
    async def Nome(self, interaction: discord.Integration, seunome: str):
        loop = True
        NomeGerado = ""
        await interaction.response.defer()
        try:
            while loop:
                NomeGerado = shks.generate_until_dot_temperature_pedro(f'{seunome.upper()}')
                if NomeGerado != "":
                    loop = False
            em = discord.Embed(color=0x80CEE1)
            em.add_field(
                name=f"**Nome shakespeariano gerado pela rede:**",
                value=f'{NomeGerado[:-1]}',
                inline=False
            )
            await interaction.followup.send(embed=em)
        except:
            await interaction.followup.send('Lembre-se de não usar caractéres ausentes nos textos originais de Shakespeare, tais quais acentos e "ç".')
    
    @apc.command(name="frase", description="Gera uma frase shakespeariana!")
    async def Frase(self, interaction: discord.Integration, seunome: str):
        message = seunome + ":"
        await interaction.response.defer()
        try:
            phrase = shks.generate_until_dot_temperature(message)
            em = discord.Embed(color=0x80CEE1)
            em.add_field(
                name=f"**Frase shakespeariana gerada pela rede:**",
                value=f'{phrase}',
                inline=False
            )
            await interaction.followup.send(embed=em)
        except:
            await interaction.followup.send('Lembre-se de não usar caractéres ausentes nos textos originais de Shakespeare, tais quais acentos e "ç".')
