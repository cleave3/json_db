from pathlib import Path

from collection import JSONCollection


class JSONDatabase:
    def __init__(self, base_path="storage"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def get_collection(self, name: str) -> JSONCollection:
        return JSONCollection(self.base_path / f"{name}.json")
