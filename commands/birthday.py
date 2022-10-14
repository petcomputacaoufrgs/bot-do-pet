import os
import pytz
import discord
import datetime
import utils.time as Time
from discord.ext import tasks
from discord import app_commands as apc
import json

class Petaniver(apc.Group):
    """Comandos dos aniversarios do pet"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.data = Time.read_file("data/anniversaries.json")

    @apc.command(name="aniversario", description="Informa o dia do próximo aniversário")
    async def nextbirthday(self, interaction: discord.Interaction):
        loop = True
        today = datetime.date.today()
        while loop:
            today += datetime.timedelta(days=1)
            for date in self.data.keys():
                if date == today.strftime("%d/%m"):
                    birthday_people = self.data[date]
                    loop = False
                    break
        
        birthday_person = self.birthday_string(birthday_people)
        startofMsg = "O próximo aniversariante é"
        if len(birthday_people) != 1:
            startofMsg = "Os próximos aniversariantes são"
        
        em = discord.Embed(color=0xFF8AD2)
        em.add_field(
            name=f"**Aniversário**",
            value=f"{startofMsg} {birthday_person}, no dia {today.strftime('%d/%m')}.",
            inline=False
        )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="adicionar", description="Adiciona um aniversariante em uma data!")
    async def add_ani(self, interaction: discord.Integration, nome: str, dia: int, mes: int):
        if dia > 31 or dia < 1 or mes > 12 or mes < 1:
            await interaction.response.send_message("Data inválida")
            return
        if f'{dia:02d}/{mes:02d}' in self.data.keys():
            self.data[f"{dia:02d}/{mes:02d}"].append(nome)
        else:
            self.data[f"{dia:02d}/{mes:02d}"] = [nome]
        json.dump(self.data, open("data/anniversaries.json", "w"))
        await interaction.response.send_message(f"Aniversariante {nome} adicionado com sucesso!")
        
    @apc.command(name="remover", description="Remove um aniversariante")
    async def rem_ani(self, interaction: discord.Integration, nome: str):
        for date in self.data.keys():
            if nome in self.data[date]:
                self.data[date].remove(nome)
                if self.data[date] == []:
                    self.data.pop(date)
                json.dump(self.data, open("data/anniversaries.json", "w"))
                await interaction.response.send_message(f"Aniversariante {nome} removido com sucesso!")
                return
        await interaction.response.send_message(f"Aniversariante {nome} não encontrado!")
        
    @tasks.loop(time=datetime.time(hour=7, minute=54, tzinfo=pytz.timezone("America/Sao_Paulo")))
    async def test_birthday(self):
        today = datetime.date.today().strftime("%d/%m")
        if not today in self.data.keys():
            return
        
        birthday_people = self.data[today]    
        birthday_person = self.birthday_string(birthday_people)
        startofMsg = "O aniversariante de hoje é"
        if len(birthday_people) != 1:
            startofMsg = "Os aniversariantes de hoje são"
        
        channel = self.bot.get_channel(int(os.getenv("ANNIVERSARY_CHANNEL")))
        await channel.send(f'Atenção, <@&{os.getenv("PETIANES_ID")}>, pois é dia de festa!\n{startofMsg} {birthday_person}, não se esqueçam de desejar tudo de bom e mais um pouco.')
        
    def birthday_string(self, data):
        birthday_string = ""
        if len(data) != 1:
            for names in data:
                if names != data[-1]:
                    birthday_string += f"{names}, e "
        birthday_string += f"{data[-1]}"
        return birthday_string
        
    @tasks.loop(count=1)
    async def startTasks(self):
        self.test_birthday.start()     
