from bot import Bot
from utils.modules import loadModules

loadModules("commands") # Carrega os modulos

Bot.run(Bot.ENV["TOKEN"]) # Inicia o bot