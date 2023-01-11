import os
from importlib import import_module
from json import load, dump
from typing import Optional

class dictJSON(dict):
    def __init__(self, path: str):
        self.path = path
        with open(self.path, 'r', encoding='utf-8') as json_file:
            data = load(json_file)
        super().__init__(data)
    
    def __delitem__(self, __key) -> None:
        val = super().__delitem__(__key)
        with open(self.path, 'w+', encoding='utf-8') as json_file:
            dump(self, json_file)
        return val
    
    def __setitem__(self, __key, __value) -> None:
        val = super().__setitem__(__key, __value)
        with open(self.path, 'w+', encoding='utf-8') as json_file:
            dump(self, json_file)
        return val

    def __getitem__(self, __key) -> any:
        try:
            return super().__getitem__(__key)
        except:
            return 0

    def pop(self, __key, __default) -> any:
        val = super().pop(__key, __default)
        with open(self.path, 'w+', encoding='utf-8') as json_file:
            dump(self, json_file)
        return val
    
    def popitem(self) -> tuple:
        val = super().popitem()
        with open(self.path, 'w+', encoding='utf-8') as json_file:
            dump(self, json_file)
        return val
    
    def clear(self) -> None:
        val = super().clear()
        with open(self.path, 'w+', encoding='utf-8') as json_file:
            dump(self, json_file)
        return val
    
    def update(self, __m: Optional[dict] = ..., **kwargs) -> None:
        val = super().update(__m, **kwargs)
        with open(self.path, 'w+', encoding='utf-8') as json_file:
            dump(self, json_file)
        return val
    
    def get(self, __key, __default) -> any:
        try:
            return super().get(__key, __default)
        except:
            return 0
        

def readDataFile(name: str) -> dict:
    if not name.endswith(".json"):
        name = name + ".json"
    with open("data/" + name, 'r', encoding='utf-8') as json_file:
        data = load(json_file)
    return data

def writeDataFile(data: dict, name: str):
    if not name.endswith(".json"):
        name = name + ".json"
    with open("data/" + name, 'w+', encoding='utf-8') as json_file:
        dump(data, json_file)

def loadModules(path: str):
    for files in os.listdir(path):  # Para cada arquivo na pasta commands
        if files.endswith(".py"):  # Se o arquivo terminar com .py
            import_module(f"commands.{files[:-3]}")  # Importa o arquivo
