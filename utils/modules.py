import os
from importlib import import_module

def loadModules(path: str):
    for files in os.listdir(path):  # Para cada arquivo na pasta commands
        if files.endswith(".py"):  # Se o arquivo terminar com .py
            import_module(f"commands.{files[:-3]}")  # Importa o arquivo