import json
from pathlib import Path


class SaveManager:
    def __init__(self, archivo=None):
        base = Path(__file__).resolve().parent.parent
        self.archivo = Path(archivo) if archivo else base / "record.json"

    def cargar_record(self):
        if not self.archivo.exists():
            return 0

        try:
            with self.archivo.open("r", encoding="utf-8") as f:
                return json.load(f).get("record", 0)
        except (json.JSONDecodeError, OSError):
            return 0

    def guardar_record(self, puntaje):
        if puntaje <= self.cargar_record():
            return

        with self.archivo.open("w", encoding="utf-8") as f:
            json.dump({"record": puntaje}, f)
