from __future__ import annotations
from json import load, dump, JSONDecodeError

class dictJSON(dict):
    def __init__(self, path: str, dumper: callable = None, loader: callable = lambda k, v: (k, v), **kwargs ):
        self.path = path
        self.dumper = dumper
        self.loader = loader
        if kwargs:
            data = kwargs
        else:
            with open(self.path, 'r', encoding='utf-8') as json_file:
                try:
                    data = load(json_file)
                except JSONDecodeError as e:
                    if e.pos == 0:
                        data = {}
                    else:
                        raise e
        super().__init__(map(loader, data, data.values()))
    
    def __save__(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as json_file:
            dump(self, json_file, indent=4, default=self.dumper)
        
    def sort(self, key = None, reverse: bool = False) -> None:
        sorted_list = sorted(self.items(), key=key, reverse=reverse)
        super().clear()
        for key, value in sorted_list:
            self[key] = value
        
    def save(self) -> None:
        self.__save__()
    
    def copy(self) -> dictJSON:
        val = super().copy()
        return dictJSON(self.path, **val)
