from bot import Bot
from utils.env import loadModules

loadModules("commands") # Carrega os modulos

Bot.run(Bot.ENV["TOKEN"]) # Inicia o bot