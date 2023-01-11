import os
import pytz
import discord
import datetime
from discord.ext import tasks
from discord import app_commands as apc
from utils.env import readDataFile, writeDataFile

from bot import Bot

@Bot.addCommandGroup
class Petaniver(apc.Group):
    """Comandos dos aniversarios do pet"""

    def __init__(self):
        super().__init__() # Inicializa a classe pai
        self.data = readDataFile("birthdays") # Carrega o arquivo de aniversarios

    @apc.command(name="aniversario", description="Informa o dia do próximo aniversário")
    async def nextbirthday(self, interaction: discord.Interaction):
        day = datetime.date.today() # Pega a data de hoje
        while True: # Loop para encontrar o proximo aniversario
            day += datetime.timedelta(days=1) # Adiciona um dia a data de hoje
            # Se a data for igual a data de hoje
            if day.strftime("%d/%m") in self.data.keys():
                birthday_people = self.data[day.strftime("%d/%m")] # Pega a lista de pessoas que fazem aniversario nesse dia
                break # Quebra o loop
        
        birthday_person = self.birthday_string(birthday_people) # Transforma a lista de pessoas em uma string
        startofMsg = "O próximo aniversariante é"  # Define a primeira parte da mensagem
        if len(birthday_people) != 1: # Se tiver mais de uma pessoa fazendo aniversario
            startofMsg = "Os próximos aniversariantes são" # Muda a mensagem inicial
        
        em = discord.Embed(color=0xFF8AD2) # Cria um embed
        em.add_field( # Adiciona um campo ao embed
            name=f"**Aniversário**",
            value=f"{startofMsg} {birthday_person}, no dia {day.strftime('%d/%m')}.",
            inline=False
        )
        await interaction.response.send_message(embed=em) # Envia a mensagem
        
    @apc.command(name="adicionar", description="Adiciona um aniversariante em uma data!")
    async def add_ani(self, interaction: discord.Interaction, nome: str, dia: int, mes: int):
        if dia > 31 or dia < 1 or mes > 12 or mes < 1: # Verifica se a data é valida
            await interaction.response.send_message("Data inválida") # Envia a mensagem
            return # Sai da função
        if f'{dia:02d}/{mes:02d}' in self.data.keys(): # Verifica se a data já existe
            self.data[f"{dia:02d}/{mes:02d}"].append(nome) # Adiciona o nome a lista de nomes
        else: # Se não existir
            self.data[f"{dia:02d}/{mes:02d}"] = [nome] # Cria a data com o nome
        writeDataFile(self.data, "birthdays")  # Salva o arquivo
        await interaction.response.send_message(f"Aniversariante {nome} adicionado com sucesso!") # Envia a mensagem
        
    @apc.command(name="remover", description="Remove um aniversariante") # Comando para remover um aniversariante
    async def rem_ani(self, interaction: discord.Interaction, nome: str): # Função para remover um aniversariante
        for date in self.data.keys(): # Itera sobre as datas
            if nome in self.data[date]: # Se o nome estiver na lista de nomes
                self.data[date].remove(nome) # Remove o nome da lista
                if self.data[date] == []: # Se a lista ficar vazia
                    self.data.pop(date) # Remove a data
                writeDataFile(self.data, "birthdays") # Salva o arquivo
                await interaction.response.send_message(f"Aniversariante {nome} removido com sucesso!") # Envia a mensagem
                return # Sai da função
        await interaction.response.send_message(f"Aniversariante {nome} não encontrado!") # Envia a mensagem
        
    @tasks.loop(time=datetime.time(hour=7, minute=54, tzinfo=pytz.timezone("America/Sao_Paulo")))
    async def test_birthday(self):
        today = datetime.date.today().strftime("%d/%m") # Pega a data de hoje
        if today not in self.data.keys(): # Se não tiver aniversario hoje
            return # Sai da função
        
        birthday_people = self.data[today]    # Pega a lista de pessoas que fazem aniversario hoje 
        birthday_person = self.birthday_string(birthday_people) # Transforma a lista de pessoas em uma string
        startofMsg = "O aniversariante de hoje é"  # Define a primeira parte da mensagem
        if len(birthday_people) != 1: # Se tiver mais de uma pessoa fazendo aniversario
            startofMsg = "Os aniversariantes de hoje são" # Muda a mensagem inicial
        
        channel = Bot.get_channel(int(os.getenv("BIRTHDAY_CHANNEL", 0))) # Pega o canal de aniversarios
        await channel.send(f'Atenção, <@&{os.getenv("PETIANES_ID", 0)}>, pois é dia de festa!\n{startofMsg} {birthday_person}, não se esqueçam de desejar tudo de bom e mais um pouco.')
        
    def birthday_string(self, data):
        birthday_string = "" # Inicializa a string
        if len(data) != 1: # Se tiver mais de uma pessoa
            for names in data: # Itera sobre as pessoas
                if names != data[-1]: # Se não for a ultima pessoa
                    birthday_string += f"{names}, e " # Adiciona a pessoa e uma virgula
        birthday_string += f"{data[-1]}" # Adiciona a ultima pessoa
        return birthday_string # Retorna a string
        
    @tasks.loop(count=1)
    async def startTasks(self): # Função para iniciar as tasks
        self.test_birthday.start()   # Inicia a task de aniversario  
        
