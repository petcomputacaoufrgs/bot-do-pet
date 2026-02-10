import discord
from bot import Bot


class KeyMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Id da pessoa que está atualmente com a chave
        self.location = Bot.Data.Key["last"]
        
        # 1. Busca os usuários e cria as opções DENTRO do init
        user_options = self.get_users_options()

        # 2. Cria o Select Menu dinamicamente
        self.select_menu = discord.ui.Select(
            placeholder="Passei para...",
            options=user_options,
            custom_id="passei",
            row=1 # Garante que fique na linha do meio
        )
        
        # 3. Vincula a função de resposta (callback) ao menu
        self.select_menu.callback = self.passei_callback
        
        # 4. Adiciona o menu na View
        self.add_item(self.select_menu)

    def get_users_options(self):
        """Gera a lista de opções para o menu, com proteção contra lista vazia."""
        server = Bot.get_guild(Bot.Data.Secrets["serverID"])
        options = []
        
        if server:
            for user in server.members:
                # Verifica se tem o cargo de petiane
                if user.get_role(Bot.Data.Roles["petiane"]) is not None:
                    options.append(discord.SelectOption(
                        label=f"{user.display_name}", 
                        value=str(user.id), # Value deve ser string
                        description=f"{user.name}"
                    ))
        
        # PROTEÇÃO CRÍTICA: Se a lista estiver vazia, cria uma opção "dummy"
        # Isso evita o erro "Invalid Form Body"
        if not options:
            options.append(discord.SelectOption(
                label="Nenhum petiane encontrado",
                value="0",
                description="Verifique as permissões do bot ou cargos",
                default=True
            ))
            
        # O Discord limita o select a 25 opções. Cortamos para garantir.
        return options[:25]

    def MsgChave(self) -> discord.Embed:
        em = discord.Embed(color=0xFFFFFF)
        if self.location == 0:
            local = "Está na recepção. Qualquer coisa, converse com a tia!"
        else:
            local = f"Atualmente está com <@{self.location}>."
        em.add_field(name=f"**Cadê a chave?**", value=local, inline=False)
        return em

    def UpdateKey(self, id: int) -> None:
        self.location = id
        Bot.Data.Key["last"] = id
        Bot.Data.Key.save()

    # --- BOTÕES (Estáticos) ---
    
    @discord.ui.button(label="Peguei", style=discord.ButtonStyle.green, custom_id="peguei", row=0)
    async def peguei(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.UpdateKey(interaction.user.id)
        em = self.MsgChave()
        await interaction.response.edit_message(embed=em)

    @discord.ui.button(label="Devolvi", style=discord.ButtonStyle.red, custom_id="devolvi", row=2)
    async def devolvi(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.UpdateKey(0)
        em = self.MsgChave()
        await interaction.response.edit_message(embed=em)

    # --- CALLBACK DO SELECT (Agora é uma função normal) ---
    
    async def passei_callback(self, interaction: discord.Interaction):
        # Pega o valor selecionado no menu
        selected_id = int(self.select_menu.values[0])
        
        if selected_id == 0: # Caso tenha selecionado a opção de erro/vazia
            await interaction.response.send_message("Opção inválida.", ephemeral=True)
            return

        self.UpdateKey(selected_id)
        em = self.MsgChave()
        await interaction.response.edit_message(embed=em)