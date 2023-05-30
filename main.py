from bot import Bot
from utils.modules import loadModules

loadModules("commands") # Carrega os modulos

Bot.run(Bot.Data.Secrets["token"]) # Inicia o bot