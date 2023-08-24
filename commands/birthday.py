import discord
from datetime import date, timedelta, datetime, time
from discord.ext import tasks
from discord import app_commands as apc
from utils.members import Member

from bot import Bot

@Bot.addCommandGroup
class Petaniver(apc.Group):
    """Anivers\u00e1rio"""

    def __init__(self):
        super().__init__() # Inicializa a classe pai

    @apc.command(name="aniversario", description="Informa o dia do próximo aniversário")
    async def nextbirthday(self, interaction: discord.Interaction, mostrar: bool = False):
        today = datetime(2000, date.today().month, date.today().day, tzinfo=Bot.TZ) # Cria uma data com o dia e mes de hoje no ano dos aniversario
        
        days: dict[timedelta, list[Member]] = {} # Cria uma lista de dias
        for member in Bot.Data.Members.values():
            if member.birthday is None: 
                continue
            
            difference = member.birthday - today # Pega a diferença entre a data de hoje e o aniversario
            if (difference.days < 0): # Se a diferença for menor que 0
                difference += timedelta(days=365) # Adiciona 365 dias a diferença
            
            if difference not in days:
                days[difference] = []
                
            days[difference].append(member) # Adiciona a diferença na lista de dias
                  
        if len(days) == 0: # Se não tiver nenhum aniversario
            em = discord.Embed(color=0xFF8AD2) # Cria um embed
            em.add_field( # Adiciona um campo ao embed
                name=f"**Aniversário**",
                value=f"Não há cadastrados.",
                inline=False
            )
            await interaction.response.send_message(embed=em, ephemeral=not mostrar) # Envia a mensagem
            return
        
        smallest = min(days.keys()) # Pega a menor diferença
        birthday_person = self.birthday_string(days[smallest]) # Transforma a lista de pessoas em uma string
        
        em = discord.Embed(color=0xFF8AD2) # Cria um embed
        em.add_field( # Adiciona um campo ao embed
            name=f"**Aniversário**",
            value=f"{'O próximo aniversariante é' if len(days[smallest]) == 1 else 'Os próximos aniversariantes são'} \
                {birthday_person}, no dia {days[smallest][0].birthday.strftime('%d/%m')}.",
            inline=False
        )
        await interaction.response.send_message(embed=em, ephemeral=not mostrar) # Envia a mensagem
        
    @tasks.loop(time=time(hour=8, tzinfo=Bot.TZ))
    async def test_birthday(self):
        today = datetime(2000, date.today().month, date.today().day, tzinfo=Bot.TZ) # Cria uma data com o dia e mes de hoje no ano dos aniversario
        aniversaries: list[Member] = [] # Cria uma lista de aniversarios
        for member in Bot.Data.Members.values():
            if member.birthday is None: 
                continue
            
            if member.birthday != today: # Se for o aniversario de alguem
                continue
            
            aniversaries.append(member) # Adiciona a pessoa na lista de aniversarios
        
        if len(aniversaries) == 0: # Se não tiver aniversario hoje
            return # Sai da função
        
        birthday_person = self.birthday_string(aniversaries) # Transforma a lista de pessoas em uma string
        
        channel = Bot.get_channel(Bot.Data.Channels['birthday'])  # Pega o canal de aniversarios
        em = discord.Embed(color=0xFF8AD2) # Cria um embed
        em.add_field(
            name=f"**Aniversário**",
            value=f'Atenção, hoje é dia de festa!\n\
                {"O aniversariante de hoje é" if len(aniversaries) == 1 else "Os aniversariantes de hoje são"} \
                {birthday_person}, não se esqueçam de desejar tudo de bom e mais um pouco.'
        )
        await channel.send(embed=em) # Envia a mensagem
        
    def birthday_string(self, data: list[Member]):
        birthday_string = "".join(f'<@{person.id}>, e' for person in data) # Inicializa a string
        
        birthday_string = birthday_string[:-3] # Remove o ultimo "e"
        return birthday_string # Retorna a string
        
    @tasks.loop(count=1)
    async def startTasks(self): # Função para iniciar as tasks
        self.test_birthday.start()   # Inicia a task de aniversario  
        
