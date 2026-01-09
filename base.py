import json
from dataclasses import dataclass

@dataclass
class Model:
    text: str
    image: str

class JsonDB:
    def __init__(self, path: str):
        self.path = path
        self.data = self.open(path)

    @staticmethod
    def open(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError as e:
            return []

    @staticmethod
    def record(path, data: dict):
        with open(path, 'w', encoding='utf-8') as file:
            js = json.dumps(data)
            file.write(js)

    def commit(self):
        try:
            self.record(self.path, self.data)
        except Exception as e:
            print(e)

    def add(self, model: Model):
        self.data.append(model.__dict__)
