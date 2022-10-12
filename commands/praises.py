import discord
from discord import app_commands as apc
import random
import json


class Petelogio(apc.Group):
    """Comandos para elogiar os petianos"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        with open("data/praises.json") as f:  # Abre o arquivo de ajuda.json
            # Carrega o arquivo de ajuda para a memoria
            self.data = json.loads(f.read())
        self.praise_list = self.data["praises"]

    @apc.command(name="elogiar", description="elogie alguém que fez um bom trabalho recentemente!")
    async def praise(self, interaction: discord.Integration, usuario: discord.User):
        num = random.randint(0, len(self.praise_list))
        await interaction.response.send_message(f"{self.praise_list[num].capitalize()}, <@{usuario.id}>!")

    @apc.command(name="adicionar", description="adicione mais uma forma de falarmos bem dos nossos coleguinhas")
    async def add_praise(self, interaction: discord.Integration, elogio: str):
        em = discord.Embed()
        if elogio in self.praise_list:
            em.color = 0xFF0000
            em.add_field(
                name="**Adicionar elogio**",
                value="Esse elogio já está na lista."
            )
        else:
            self.praise_list.append(elogio)
            em.color = 0xFF6347
            json.dump(self.data, open("data/praises.json", "w"))
            em.add_field(
                name="**Adicionar elogio**",
                value=f'"{elogio}" foi adicionado à lista!'
            )
        await interaction.response.send_message(embed=em)
    
    @apc.command(name="remover", description="não gostou de algum elogio? só mandar o elogio a ser removido")
    async def rem_praise(self, interaction: discord.Integration, elogio: str):
        em = discord.Embed()
        if elogio in self.praise_list:
            self.praise_list.remove(elogio)
            json.dump(self.data, open("data/praises.json", "w"))
            em.color = 0xFF6347
            em.add_field(
                name="**Remover elogio**",
                value=f'"{elogio}" foi removido da lista!'
            )
        else:
            em.color = 0xFF0000
            em.add_field(
                name="**Remover elogio**",
                value='Esse elogio não existe.'
            )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="listar", description="lista todos os elogios")
    async def show_praises(self, interaction: discord.Integration):
        em = discord.Embed()
        em.color = 0xFF6347
        em.add_field(
            name="**Lista de elogios**",
            value="\n".join(self.praise_list)
        )
        await interaction.response.send_message(embed=em)
