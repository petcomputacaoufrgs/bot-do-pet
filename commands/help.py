import json
import discord
from discord import app_commands as apc

class Pethelp(apc.Group): # Cria a classe do comando, que herda de Group, utilizado para agrupar os comandos em subgrupos
    """HELP COMMANDS"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot # Referencia para o proprio bot, caso necessario
        self.UpdateHelp() # Atualiza o arquivo de ajuda
        
    @apc.command(name="help", description="Mostra todos os commandos do BotPET")
    async def help(self, interaction: discord.Interaction):
        self.UpdateHelp() # Atualiza o arquivo de ajuda
        helpData = self.data["help"] # Pega os dados de ajuda geral
        # Gera a mensagem de ajuda
        em=discord.Embed(title = helpData["title"], url = helpData["url"], description = helpData["description"], color = eval(helpData["color"]))
        for i in helpData["commands"]: # Para cada comando na lista de comandos
            em.add_field(name = i["name"], value = i["value"], inline = i["inline"]) # Adiciona o comando na mensagem
        em.set_thumbnail( url = "https://cdn.discordapp.com/attachments/938858934259822685/945718556732039219/LogoPET_oficial.png") # Adiciona a imagem do PET
        await interaction.response.send_message(embed = em) # Envia a mensagem de ajuda
        
    @apc.command(name="comando", description="Mostra os detalhes de um comando")
    async def comando(self, interaction: discord.Interaction, comando: str):
        self.UpdateHelp() # Atualiza o arquivo de ajuda
        commandsData = self.data["commands"] # Pega os dados de comandos
        found = False # Variavel para verificar se o comando foi encontrado
        for command in commandsData: # Para cada comando na lista de comandos
            if command["command"] == comando: # Se o comando for igual ao comando passado
                em = discord.Embed(title=command["title"], description=command["description"], color=eval(command["color"])) # Gera a mensagem de ajuda
                example = command["example"][0] # Pega o primeiro exemplo
                em.add_field(name = example["name"], value = example["value"],inline=example["inline"]) # Adiciona o exemplo na mensagem
                found = True # Seta a variavel para verdadeiro
                break # Para o loop
        if not found: # Se o comando não for encontrado
            await interaction.response.send_message("Comando não encontrado!") # Envia a mensagem de erro
        else:
            await interaction.response.send_message(embed = em) # Envia a mensagem de ajuda
            
    def UpdateHelp(self) -> None:
        with open("data/help.json") as f: # Abre o arquivo de ajuda.json
            self.data = json.loads(f.read()) # Carrega o arquivo de ajuda para a memoria