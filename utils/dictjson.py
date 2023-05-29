from __future__ import annotations
from json import load, dump
from typing import Optional

class dictJSON(dict):
    def __init__(self, path: str, **kwargs):
        self.path = path
        if kwargs:
            data = kwargs
        else:
            with open(self.path, 'r', encoding='utf-8') as json_file:
                data = load(json_file)
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
        
    def sort(self, key = None) -> None:
        sorted_list = sorted(self.items(), key=key)
        super().clear()
        for key, value in sorted_list:
            self[key] = value
        self.__save__()
        
    def save(self) -> None:
        self.__save__()
    
    def copy(self) -> dictJSON:
        val = super().copy()
        return dictJSON(self.path, **val)
