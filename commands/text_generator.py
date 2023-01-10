import discord
from discord import app_commands as apc
import utils.shakespeare as shks


class Petshakespeare(apc.Group):
    """Comando para gerar texto com Shakespeare"""
    def __init__(self, bot: discord.Client):
        super().__init__() # Inicializa o comando
        self.bot = bot # Adiciona o bot

    @apc.command(name="nome", description="Gera um nome shakespeariano!") # Adiciona o subcomando nome
    async def Nome(self, interaction: discord.Interaction, seunome: str):
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
    
    @apc.command(name="frase", description="Gera uma frase shakespeariana!") # Adiciona o subcomando frase
    async def Frase(self, interaction: discord.Interaction, seunome: str):
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
            em = discord.Embed(color=0xFF0000)
            em.add_field(
                name=f"**Erro ao gerar frase!**",       
                value=f"Lembre-se de não usar caractéres ausentes nos textos originais de Shakespeare, tais quais acentos e 'ç'.",
                inline=False
            )
            await interaction.followup.send(embed=em)
