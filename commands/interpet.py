import os
import pytz
import discord
import datetime
import utils.time as Time
from discord.ext import tasks
from discord import app_commands as apc
import json

class Petinter(apc.Group):
    """Comandos do interpet mensal"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.interpet_day = Time.format_date().date()
        self.flag = 1
        
    @apc.command(name="interpet", description="Informa o dia do próximo interpet")
    async def interpet(self, interaction: discord.Interaction):
        em = discord.Embed(color=0x9370DB)
        self.interpet_day = Time.format_date().date()
        days_to_interpet = self.interpet_day - datetime.date.today()
        if days_to_interpet.days < 2:
            if days_to_interpet.days == 1:
                em.add_field(
                    name="**Interpet**",
                    value=f'Falta {days_to_interpet.days} dia até o próximo interpet, que será no dia {self.interpet_day.day:02d}/{self.interpet_day.month:02d}.'
                )
            elif days_to_interpet.days == 0:
                em.add_field(
                    name="**Interpet**",
                    value="Hoje é o dia do interpet! Corre pra não perder a reunião."
                )
            else:
                em.add_field(
                    name="**Interpet**",
                    value="Erro na data do interpet"
                )
        else:
            em.add_field(
                name="**Interpet**",
                value=f'Faltam {days_to_interpet.days} dias até o próximo interpet, que será no dia {self.interpet_day.day:02d}/{self.interpet_day.month:02d}.'
            )
        await interaction.response.send_message(embed=em)
        
    @apc.command(name="ferias", description="Desliga o aviso de interpet")
    async def set_interpet_vacation(self, interaction: discord.Interaction):
        em = discord.Embed(color=0x9370DB)
        self.turn_off_interpet.start()
        em.add_field(
            name="**Interpet**",
            value="Bot entrando de férias das retrospectivas! Sem mais avisos ou afins."
        )
        await interaction.responde.send_message(embed=em)
        
    @apc.command(name="adicionar", description="Adiciona um novo interpet")
    async def add_interpet(self, interaction: discord.Integration, dia: int, mes: int, ano: int):
        data = Time.read_file('data/interpet_dates.json')
        date_list = data['dates']
        em = discord.Embed(color=0x9370DB)
        try:
            new_date = datetime.datetime(
                int(ano), int(mes), int(dia)).date()
            today_date = datetime.date.today()
            if (new_date - today_date).days > 0:
                if f'{dia:02d}/{mes:02d}/{ano}' in date_list:
                    em.add_field(
                        name="**Adicionar data de interpet**",
                        value="Essa data já está na lista."
                    )
                else:
                    date_list.append(f'{dia:02d}/{mes:02d}/{ano}')
                    dict = {'dates': date_list}
                    with open('data/interpet_dates.json', 'w+', encoding='utf-8') as outfile:
                        json.dump(dict, outfile)
                    em.add_field(
                        name="**Adicionar data de interpet**",
                        value=f'A data {dia:02d}/{mes:02d}/{ano} foi adicionada com sucesso!'
                    )
            else:
                raise
        except:
            em.add_field(
                name="**Adicionar data de interpet**",
                value=f'Lembre-se de usar o formato `<dd/mm/aaaa>` e com datas válidas!'
            )
        await interaction.response.send_message(embed=em)
        
        # Command: Remover data de interpet
    @apc.command(name="remover", description="Remove uma data de interpet")
    async def remove_offense(self, interaction: discord.Integration, dia: int, mes: int, ano: int):
        data = Time.read_file('data/interpet_dates.json')
        date_list = data['dates']
        em = discord.Embed(color=0x9370DB)
        if f'{dia:02d}/{mes:02d}/{ano}' in date_list:
            date_list.remove(f'{dia:02d}/{mes:02d}/{ano}')
            dict = {'dates': date_list}
            with open('data/interpet_dates.json', 'w+', encoding='utf-8') as outfile:
                json.dump(dict, outfile)
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
        data = Time.read_file('data/interpet_dates.json')
        date_list = data['dates']
        for date in date_list:
            day, month, year = date.split('/')
            difference = datetime.datetime(int(year), int(
                month), int(day)).date() - datetime.date.today()
            if (difference).days < 0:
                date_list.remove(date)
            else:
                date = f"{date} - daqui a {(difference).days}"
        printable_date_list = '\n'.join(date_list)
        em = discord.Embed(color=0x9370DB)
        em.add_field(
            name="**Datas dos próximos interpets:**",
            value=f'{printable_date_list}'
        )
        await interaction.response.send_message(embed=em)
        
    @tasks.loop(hours=1)
    async def is_interpet_eve(self):
        self.interpet_day = Time.format_date().date()
        now = datetime.datetime.now(pytz.timezone('Brazil/East'))
        if self.interpet_day == datetime.date.today() + datetime.timedelta(days=1):
            if now.hour == 20:
                self.remember_interpet.start()
        if self.interpet_day == datetime.date.today():
            if now.hour == 8:
                self.awake_interpet.start()
        if self.interpet_day == datetime.date.today() - datetime.timedelta(days=1):
            if now.hour == 1:
                self.update_interpet_day.start()


    @tasks.loop(count=1)
    async def remember_interpet(self):
        channel = self.bot.get_channel(int(os.getenv('INTERPET_CHANNEL')))
        await channel.send(f'Atenção, <@&{os.getenv("PETIANES_ID")}>!\nLembrando que amanhã é dia de interpet, estejam acordados às 9h.')
        
    @tasks.loop(count=1)
    async def awake_interpet(self):
        channel = self.bot.get_channel(int(os.getenv('INTERPET_CHANNEL')))
        await channel.send(f'Atenção, <@&{os.getenv("PETIANES_ID")}>!\nMenos de uma hora para começar o interpet, espero que todos já estejam acordados.')
        
    @tasks.loop(count=1)
    async def update_interpet_day(self):
        self.interpet_day = Time.format_date().date()
        
    @tasks.loop(count=1)
    async def startTasks(self):
            self.is_interpet_eve.start()
