import os
from importlib import import_module
from inspect import getmembers, isclass

from bot import Bot, TOKENS, CommandTree

# Carrega todos os comandos do bot e os adiciona a lista de comandos
for files in os.listdir("commands"): # Para cada arquivo na pasta commands
    if files.endswith(".py"): # Se o arquivo terminar com .py
        module = import_module(f"commands.{files[:-3]}") # Importa o arquivo
        moduleClass = getmembers(module, isclass) # Pega a classe do arquivo
        instance = moduleClass[0][1](Bot) # Cria uma instancia da classe
        Bot.commands.append(instance) # Adiciona a instancia a lista de comandos

for command in Bot.commands: # Para cada comando na lista de comandos
    # Adiciona os comandos na arvore
    CommandTree.add_command(command, guild=TOKENS.GUILD)

Bot.run(TOKENS.SERVER) # Inicia o bot