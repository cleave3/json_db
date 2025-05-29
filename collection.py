from collections import defaultdict
import json
import uuid
import re
from pathlib import Path
from typing import Any, Dict, List, Union


class JSONCollection:
    def __init__(self, path: Path):
        self.path = path
        self.index_path = path.with_suffix(".index.json")
        self._ensure_file()
        self.indexes = self._load_indexes()

    def _ensure_file(self):
        if not self.path.exists():
            with open(self.path, "w") as f:
                json.dump([], f)

    def _load(self) -> List[Dict[str, Any]]:
        with open(self.path, "r") as f:
            return json.load(f)

    def _save(self, data: List[Dict[str, Any]]):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def _load_indexes(self) -> Dict[str, Dict[str, List[str]]]:
        if self.index_path.exists():
            with open(self.index_path, "r") as f:
                return json.load(f)
        return {}

    def _save_indexes(self):
        with open(self.index_path, "w") as f:
            json.dump(self.indexes, f, indent=2)

    def _match(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        for k, v in query.items():
            keys = k.split(".")
            val = doc
            for key in keys:
                if isinstance(val, dict):
                    val = val.get(key)
                else:
                    return False
            if isinstance(v, dict):
                for op, cond_val in v.items():
                    if op == "$gt" and not (val > cond_val):
                        return False
                    elif op == "$lt" and not (val < cond_val):
                        return False
                    elif op == "$gte" and not (val >= cond_val):
                        return False
                    elif op == "$lte" and not (val <= cond_val):
                        return False
                    elif op == "$in" and not (val in cond_val):
                        return False
                    elif op == "$regex" and not re.search(cond_val, str(val)):
                        return False
                    elif op == "$ne" and not (val != cond_val):
                        return False
            else:
                if val != v:
                    return False
        return True

    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    def insert_one(self, document: Dict[str, Any]):
        data = self._load()
        if "_id" not in document:
            document["_id"] = self._generate_id()
        data.append(document)
        self._save(data)
        self._update_indexes(document)
        self._save_indexes()

    def find(self, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        data = self._load()
        indexed_results = self._query_using_indexes(query)
        if indexed_results is not None:
            data = [doc for doc in data if doc["_id"] in indexed_results]
        return [doc for doc in data if self._match(doc, query)]

    def find_one(self, query: Dict[str, Any] = {}) -> Union[Dict[str, Any], None]:
        data = self._load()
        indexed_results = self._query_using_indexes(query)
        if indexed_results is not None:
            data = [doc for doc in data if doc["_id"] in indexed_results]
        for doc in data:
            if self._match(doc, query):
                return doc
        return None

    def update(self, query: Dict[str, Any], updates: Dict[str, Any]):
        data = self._load()
        for doc in data:
            if self._match(doc, query):
                doc.update(updates)
                self._update_indexes(doc)
        self._save(data)
        self._save_indexes()

    def delete(self, query: Dict[str, Any]):
        data = self._load()
        new_data = [doc for doc in data if not self._match(doc, query)]
        self._save(new_data)
        self._rebuild_indexes(new_data)
        self._save_indexes()

    def _update_indexes(self, document: Dict[str, Any]):
        for key in self.indexes:
            value = self._get_nested_value(document, key)
            if value is not None:
                value = str(value)
                if value not in self.indexes[key]:
                    self.indexes[key][value] = []
                if document["_id"] not in self.indexes[key][value]:
                    self.indexes[key][value].append(document["_id"])

    def _get_nested_value(self, doc: Dict[str, Any], key: str) -> Any:
        keys = key.split(".")
        val = doc
        for k in keys:
            val = val.get(k, {}) if isinstance(val, dict) else {}
        return val if val != {} else None

    def _query_using_indexes(self, query: Dict[str, Any]) -> Union[None, List[str]]:
        matched_ids = None
        for field, value in query.items():
            if isinstance(value, dict):
                return None  # Skip if query uses operators
            index = self.indexes.get(field)
            if index and str(value) in index:
                current_ids = set(index[str(value)])
                if matched_ids is None:
                    matched_ids = current_ids
                else:
                    matched_ids &= current_ids
            else:
                return None
        return list(matched_ids) if matched_ids is not None else None

    def _rebuild_indexes(self, documents: List[Dict[str, Any]]):
        for key in self.indexes:
            self.indexes[key] = {}
        for doc in documents:
            self._update_indexes(doc)

    def create_index(self, field: str):
        self.indexes[field] = {}
        for doc in self._load():
            self._update_indexes(doc)
        self._save_indexes()

    def group_by(self, field: str) -> Dict[Any, List[Dict[str, Any]]]:
        data = self._load()
        grouped = defaultdict(list)
        for doc in data:
            key = self._get_nested_value(doc, field)
            grouped[key].append(doc)
        return dict(grouped)

    def aggregate(self, field: str, operation: str) -> Any:
        data = self._load()
        values = [
            self._get_nested_value(doc, field)
            for doc in data
            if isinstance(self._get_nested_value(doc, field), (int, float))
        ]
        if operation == "sum":
            return sum(values)
        elif operation == "avg":
            return sum(values) / len(values) if values else 0
        elif operation == "min":
            return min(values) if values else None
        elif operation == "max":
            return max(values) if values else None
        return None
