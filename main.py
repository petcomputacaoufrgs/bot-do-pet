from utils.setup import CommandTree, Bot, TOKENS

import commands.help as Help
CommandTree.add_command(Help.Pethelp(Bot), guild=TOKENS.GUILD) # Adiciona os subcomando de ajuda

import commands.key as Key
CommandTree.add_command(Key.Petkey(Bot), guild=TOKENS.GUILD) # Adiciona os subcomando de key

import commands.test # Importa os comandos do arquivo de teste

Bot.run(TOKENS.SERVER) # Inicia o bot