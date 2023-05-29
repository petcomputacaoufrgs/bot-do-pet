import discord
from discord.ext import tasks
from discord import app_commands as apc
import datetime
from datetime import time
from utils.env import dictJSON

from bot import Bot

@Bot.addCommandGroup
class Petinter(apc.Group):
    """Interpet"""
    def __init__(self):
        super().__init__() # Inicializa a classe pai
        self.data = dictJSON("data/interpet_dates.json")  # Lê o arquivo de datas
        self.interpet_day = self.getNextInterpet().date() # Pega a data de hoje
        
        
    @apc.command(name="interpet", description="Informa o dia do próximo interpet")
    async def interpet(self, interaction: discord.Interaction): 
        em = discord.Embed(color=0x9370DB) # Cria um embed
        self.interpet_day = self.getNextInterpet().date() # Pega a data de hoje
        days_to_interpet = self.interpet_day - datetime.date.today() # Calcula a diferença entre a data de hoje e a data do interpet
        if days_to_interpet.days < 2: # Se a diferença for menor que 2 dias
            if days_to_interpet.days == 1: # Se a diferença for 1 dia
                date = f'{self.interpet_day.day:02d}/{self.interpet_day.month:02d}/{self.interpet_day.year}'
                em.add_field(
                    name="**Interpet**",
                    value=f'Falta {days_to_interpet.days} dia até o próximo interpet, que será no dia {self.interpet_day.day:02d}/{self.interpet_day.month:02d}.' + \
                    f" Os grupos do interpet serão: {self.data[date]}."
                )
            elif days_to_interpet.days == 0: # Se a diferença for 0 dias
                em.add_field(
                    name="**Interpet**",
                    value="Hoje é o dia do interpet! Corre pra não perder a reunião."
                )
            else:
                em.add_field( # Se a diferença for menor que 0 dias
                    name="**Interpet**",
                    value="Erro na data do interpet"
                )
        else:
            date = f'{self.interpet_day.day:02d}/{self.interpet_day.month:02d}/{self.interpet_day.year}'
            em.add_field( # Se a diferença for maior que 2 dias
                name="**Interpet**",
                value=f'Faltam {days_to_interpet.days} dias até o próximo interpet, que será no dia {self.interpet_day.day:02d}/{self.interpet_day.month:02d}.' + \
                f" Os grupos do interpet serão: {self.data[date]}."
            )
        await interaction.response.send_message(embed=em) # Envia a mensagem
        
        
    @apc.command(name="adicionar", description="Adiciona um novo interpet")
    async def add_interpet(self, interaction: discord.Interaction, dia: int, mes: int, ano: int, grupos: str):
        em = discord.Embed(color=0x9370DB) # Cria um embed
        try: # Tenta adicionar a data
            new_date = datetime.datetime(int(ano), int(mes), int(dia)).date()
            if (new_date - datetime.date.today()).days > 0:
                self.data[f'{dia:02d}/{mes:02d}/{ano}'] = grupos
                self.data.sort(self.sortDates)
                em.add_field(
                    name="**Adicionar data de interpet**",
                    value=f'A data {dia:02d}/{mes:02d}/{ano} foi adicionada com sucesso!\nOs grupos do interpet serão: {grupos}.'
                )
            else:
                raise
        except:
            em.add_field(
                name="**Adicionar data de interpet**",
                value=f'Lembre-se de usar datas válidas!'
            )
        await interaction.response.send_message(embed=em)
        
        # Command: Remover data de interpet
    @apc.command(name="remover", description="Remove uma data de interpet")
    async def remove_interpet(self, interaction: discord.Interaction, dia: int, mes: int, ano: int):
        em = discord.Embed(color=0x9370DB)
        if f'{dia:02d}/{mes:02d}/{ano}' in self.data.keys():
            self.data.pop(f'{dia:02d}/{mes:02d}/{ano}')
            em.add_field(
                name="**Remover data de interpet**",
                value=f'A data foi removida da lista!'
            )
        else:
            em.add_field(
                name="**Remover data de interpet**",
                value='Essa data não está na lista.'
            )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="datas", description="Mostra as datas de interpet")
    async def show_dates(self, interaction: discord.Interaction):
        self.clearInterpetDates()

        printable_date_list = ''
        for date in self.data.keys():
            printable_date_list += f'**{date}** - {self.data[date]}\n'

        em = discord.Embed(color=0x9370DB)
        em.add_field(
            name="**Datas dos próximos interpets:**",
            value=f'{printable_date_list}'
        )
        await interaction.response.send_message(embed=em)
        
    @tasks.loop(time=time(hour=20, tzinfo=Bot.TZ))
    async def remember_interpet(self):
        self.interpet_day = self.getNextInterpet().date() # Pega a data atual
        # Se o aviso de interpet estiver ligado e for dia de interpet
        if self.interpet_day == datetime.date.today() + datetime.timedelta(days=1):
            channel = Bot.get_channel(Bot.ENV['INTERPET_CHANNEL'])
            await channel.send(f'Atenção, <@&{Bot.ENV["PETIANES_ID"]}>!\nLembrando que amanhã é dia de interpet, estejam acordados às 9h.')
        
        
    @tasks.loop(time=time(hour=8, tzinfo=Bot.TZ))
    async def awake_interpet(self):
        self.interpet_day = self.getNextInterpet().date()  # Pega a data atual
        # Se o aviso de interpet estiver ligado e for dia de interpet
        if self.interpet_day == datetime.date.today():
            channel = Bot.get_channel(Bot.ENV['INTERPET_CHANNEL'])
            await channel.send(f'Atenção, <@&{Bot.ENV["PETIANES_ID"]}>!\nMenos de uma hora para começar o interpet, espero que todos já estejam acordados.')
        
        
    @tasks.loop(count=1)
    async def startTasks(self): # Inicia as tasks
        self.remember_interpet.start() # Inicia a task de lembrar do interpet
        self.awake_interpet.start() # Inicia a task de acordar para o interpet
        
    def getNextInterpet(self):
        now = datetime.datetime.now()
        actual_date = datetime.datetime(2022, 4, 9)
        for date in self.data.keys():
            day, month, year = date.split('/')
            formated_date = datetime.datetime(int(year), int(month), int(day))
            difference = formated_date - now
            if (actual_date - now).days < 0:
                actual_date = formated_date
            if difference <= (actual_date - now):
                actual_date = formated_date
        return actual_date    
        
    def clearInterpetDates(self):
        oldDates = []
        for date in self.data.keys():
            day, month, year = date.split('/')
            difference = datetime.datetime(int(year), int(
                month), int(day)).date() - datetime.date.today()
            if (difference).days < 0:
                oldDates.append(date)
                
        for date in oldDates:
            self.data.pop(date)
        
    def sortDates(self, x):
        day, month, year = x[0].split('/')
        return datetime.datetime(int(year), int(month), int(day))
