import json
from pathlib import Path


class LevelLoader:
    def __init__(self, carpeta=None):
        base = Path(__file__).resolve().parent.parent
        self.carpeta = Path(carpeta) if carpeta else base / "levels"

    def cargar(self, nombre):
        ruta = self.carpeta / f"{nombre}.json"
        with ruta.open("r", encoding="utf-8") as f:
            return json.load(f)
