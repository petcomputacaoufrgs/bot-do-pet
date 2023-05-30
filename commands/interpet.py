import discord
from discord.ext import tasks
from discord import app_commands as apc
from datetime import time, date, datetime, timedelta
from asyncio import sleep

from bot import Bot

@Bot.addCommandGroup
class Petinter(apc.Group):
    """Interpet"""
    def __init__(self):
        super().__init__() # Inicializa a classe pai
        self.interpet_day = self.getNextInterpet().date() # Pega a data de hoje
        
        
    @apc.command(name="interpet", description="Informa o dia do próximo interpet")
    async def interpet(self, interaction: discord.Interaction, mostrar: bool = False): 
        em = discord.Embed(color=0x94FF26) # Cria um embed
        
        self.interpet_day = self.getNextInterpet().date() # Pega a data de hoje
        
        days_to_interpet = self.interpet_day - date.today() # Calcula a diferença entre a data de hoje e a data do interpet
        
        if days_to_interpet.day == 0:
            em.add_field(
                name="**Interpet**",
                value="Hoje é o dia do interpet! Corre pra não perder a reunião."
            )
        elif days_to_interpet.days < 0:
            em.add_field( # Se a diferença for menor que 0 dias
                    name="**Interpet**",
                    value="Erro na data do interpet"
                )
        else:
            date = f'{self.interpet_day.day:02d}/{self.interpet_day.month:02d}/{self.interpet_day.year}'
            em.add_field(
                name="**Interpet**",
                value=f'Falta {days_to_interpet.days} dia até o próximo interpet, \
                    que será no dia {self.interpet_day.day:02d}/{self.interpet_day.month:02d}.' + \
                        f" Os grupos do interpet serão: {Bot.Data.Interpet[date]}."
                        )
            
        await interaction.response.send_message(embed=em, ephemeral=not mostrar) # Envia a mensagem
        
        
    @apc.command(name="adicionar", description="Adiciona um novo interpet")
    async def add_interpet(self, interaction: discord.Interaction, dia: int, mes: int, ano: int, grupos: str):
        em = discord.Embed(color=0x94FF26) # Cria um embed
        
        difference = datetime(int(ano), int(mes), int(dia)).date() - date.today() # Calcula a diferença entre a data de hoje e a data do interpet
        if difference.days > 0:
                Bot.Data.Interpet[f'{dia:02d}/{mes:02d}/{ano}'] = grupos
                Bot.Data.Interpet.sort(self.sortDates)
                Bot.Data.Interpet.save()
                em.add_field(
                    name="**Adicionar data de interpet**",
                    value=f'A data {dia:02d}/{mes:02d}/{ano} foi adicionada com sucesso!\nOs grupos do interpet serão: {grupos}.'
                )
        else:
            em.add_field(
                name="**Adicionar data de interpet**",
                value=f'Lembre-se de usar datas válidas!'
            )
            
        await interaction.response.send_message(embed=em)

    @apc.command(name="remover", description="Remove uma data de interpet")
    async def remove_interpet(self, interaction: discord.Interaction, dia: int, mes: int, ano: int):
        em = discord.Embed(color=0x94FF26)
        if f'{dia:02d}/{mes:02d}/{ano}' in Bot.Data.Interpet.keys():
            del Bot.Data.Interpet[f'{dia:02d}/{mes:02d}/{ano}']
            Bot.Data.Interpet.save()
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
    async def show_dates(self, interaction: discord.Interaction, mostrar: bool = False):
        self.getNextInterpet()

        printable_date_list = ''.join(f'**{date}** - {Bot.Data.Interpet[date]}\n' for date in Bot.Data.Interpet.keys())

        em = discord.Embed(color=0x94FF26)
        em.add_field(
            name="**Datas dos próximos interpets:**",
            value=f'{printable_date_list}'
        )
        await interaction.response.send_message(embed=em, ephemeral=not mostrar)
        
    @tasks.loop(time=time(hour=20, tzinfo=Bot.TZ))
    async def remember_interpet(self):
        self.interpet_day = self.getNextInterpet().date() # Pega a data atual
        if date.today() + timedelta(days=1) != self.interpet_day:
            return

        em = discord.Embed(color=0x94FF26)
        em.add_field(
            name="**Interpet**",
            value='Lembrando que amanhã é dia de interpet, estejam acordados às 9h.'
        )
        
        channel = Bot.get_channel(Bot.Data.Channels['interpet'])
        await channel.send(f"Atenção, <@&{Bot.Data.Roles['petiane']}!", embed=em)
        
        
    @tasks.loop(time=time(hour=8, tzinfo=Bot.TZ))
    async def awake_interpet(self):
        self.interpet_day = self.getNextInterpet().date()  # Pega a data atual
        if date.today() != self.interpet_day:
            return
        
        em = discord.Embed(color=0x94FF26)
        em.add_field(
            name="**Interpet**",
            value="Menos de uma hora para começar o interpet, espero que todos já estejam acordados."
        )
        
        channel = Bot.get_channel(Bot.Data.Channels["interpet"])
        await channel.send(f'Atenção, <@&{Bot.Data.Roles["petiane"]}>!\n', embed=em)
        
        
    @tasks.loop(count=1)
    async def startTasks(self): # Inicia as tasks
        self.remember_interpet.start() # Inicia a task de lembrar do interpet
        self.awake_interpet.start() # Inicia a task de acordar para o interpet
        
    def getNextInterpet(self):
        dates: dict = {}
        for interpet in Bot.Data.Interpet.keys():
            day, month, year = interpet.split('/')
            day, month, year = int(day), int(month), int(year)
            difference = datetime(year, month, day).date() - date.today()
            if difference.days < 0:
                del Bot.Data.Interpet[interpet]
                continue
            
            dates[difference] = datetime(year, month, day).date()
        Bot.Data.Interpet.save()
        return dates[min(dates.keys())]    
        
    def sortDates(self, x):
        day, month, year = x[0].split('/')
        return datetime(int(year), int(month), int(day))
