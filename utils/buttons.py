import discord

from bot import Bot

users = []

class KeyMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Id da pessoa que está atualmente com a chave, 0 = com a tia
        self.location = Bot.ENV["LAST_KEY"]
        self.updateUsers()

    def updateUsers(self) -> None:
        server = Bot.get_guild(Bot.ENV["SERVER_ID"])
        users.clear()
        for user in server.members:
            if user.get_role(Bot.ENV["PETIANES_ID"]) is not None:
                users.append(discord.SelectOption(
                    label=f"{user.display_name}", value=user.id, description=f"{user.name}#{user.discriminator}"))

    def MsgChave(self) -> discord.Embed:
        em = discord.Embed(color=0xFFFFFF)  # Gera a mensagem de saida
        if self.location == 0:  # Testa se a chave está com a tia ou algum id de pessoa e gera a saida correta
            local = "Está na recepção. Qualquer coisa, converse com a tia!"
        else:
            local = f"Atualmente está com <@{self.location}>."
        em.add_field(name=f"**Cadê a chave?**", value=local, inline=False)
        # Manda a mensagem
        return em

    async def output(self, message: discord.Message) -> None:
        em = self.MsgChave()  # Gera a mensagem de saida
        await message.edit(embed=em)  # Manda a mensagem
        
    def UpdateKey(self, id: int) -> None:
        self.location = id
        Bot.ENV["LAST_KEY"] = id
        
    @discord.ui.button(label="Peguei", style=discord.ButtonStyle.green, custom_id="peguei")
    async def peguei(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Muda o id da pessoa que está com a chave
        self.UpdateKey(interaction.user.id)
        em = self.MsgChave()  # Gera a mensagem de saida
        await interaction.response.edit_message(embed=em)  # Manda a mensagem
    
    @discord.ui.select(placeholder="Passei", options=users, custom_id="passei")
    async def passei(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Muda o id da pessoa que está com a chave
        self.UpdateKey(select.values[0])
        em = self.MsgChave()  # Gera a mensagem de saida
        await interaction.response.edit_message(embed=em)  # Manda a mensagem

    @discord.ui.button(label="Devolvi", style=discord.ButtonStyle.red, custom_id="devolvi")
    async def devolvi(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.UpdateKey(0)
        em = self.MsgChave()  # Gera a mensagem de saida
        await interaction.response.edit_message(embed=em)  # Manda a mensagem
