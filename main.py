from bot import Bot
from utils.env import loadModules

loadModules("commands") # Carrega os modulos

Bot.run(Bot.TOKENS.SERVER) # Inicia o bot