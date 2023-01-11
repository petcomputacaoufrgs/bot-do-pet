import os
from importlib import import_module
from json import load, dump
from typing import Optional

class dictJSON(dict):
    def __init__(self, path: str, imported: bool = True, **kwargs):
        self.path = path
        if imported:
            with open(self.path, 'r', encoding='utf-8') as json_file:
                data = load(json_file)
        elif kwargs:
            data = kwargs
        else:
            data = {}
        super().__init__(data)
        self.__save__()
    
    def __save__(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as json_file:
            dump(self, json_file)
    
    def __delitem__(self, __key) -> None:
        val = super().__delitem__(__key)
        self.__save__()
        return val
    
    def __setitem__(self, __key, __value) -> None:
        val = super().__setitem__(__key, __value)
        self.__save__()
        return val

    def __getitem__(self, __key) -> any:
        try:
            return super().__getitem__(__key)
        except:
            return 0

    def pop(self, __key, __default = None) -> any:
        if __default is None:
            val = super().pop(__key)
        else:
            val = super().pop(__key, __default)
        self.__save__()
        return val
    
    def popitem(self) -> tuple:
        val = super().popitem()
        self.__save__()
        return val
    
    def clear(self) -> None:
        val = super().clear()
        self.__save__()
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

def loadModules(path: str):
    for files in os.listdir(path):  # Para cada arquivo na pasta commands
        if files.endswith(".py"):  # Se o arquivo terminar com .py
            import_module(f"commands.{files[:-3]}")  # Importa o arquivo
