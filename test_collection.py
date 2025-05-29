import shutil
import tempfile
import pytest
from pathlib import Path
from .collection import JSONCollection

@pytest.fixture(scope="function")
def temp_collection():
    temp_dir = tempfile.mkdtemp()
    path = Path(temp_dir) / "test.json"
    collection = JSONCollection(path)
    yield collection
    shutil.rmtree(temp_dir)

def test_insert_and_find(temp_collection):
    doc = {"name": "Alice", "age": 30, "address": {"city": "London"}}
    temp_collection.insert_one(doc)
    results = temp_collection.find({"name": "Alice"})
    assert len(results) == 1
    assert results[0]["name"] == "Alice"
    assert "_id" in results[0]

def test_find_one(temp_collection):
    temp_collection.insert_one({"name": "Bob", "age": 25})
    result = temp_collection.find_one({"name": "Bob"})
    assert result is not None
    assert result["age"] == 25

def test_update(temp_collection):
    temp_collection.insert_one({"name": "Carol", "age": 22})
    temp_collection.update({"name": "Carol"}, {"age": 23})
    result = temp_collection.find_one({"name": "Carol"})
    assert result["age"] == 23

def test_delete(temp_collection):
    temp_collection.insert_one({"name": "Dave", "age": 40})
    temp_collection.delete({"name": "Dave"})
    result = temp_collection.find_one({"name": "Dave"})
    assert result is None

def test_create_index_and_query(temp_collection):
    temp_collection.insert_one({"name": "Eve", "age": 28})
    temp_collection.create_index("name")
    results = temp_collection.find({"name": "Eve"})
    assert len(results) == 1
    assert results[0]["name"] == "Eve"

def test_group_by(temp_collection):
    temp_collection.insert_one({"name": "Frank", "age": 20, "group": "A"})
    temp_collection.insert_one({"name": "Grace", "age": 21, "group": "A"})
    temp_collection.insert_one({"name": "Heidi", "age": 22, "group": "B"})
    grouped = temp_collection.group_by("group")
    assert len(grouped["A"]) == 2
    assert len(grouped["B"]) == 1

def test_aggregate(temp_collection):
    temp_collection.insert_one({"name": "Ivan", "score": 10})
    temp_collection.insert_one({"name": "Judy", "score": 20})
    temp_collection.insert_one({"name": "Karl", "score": 30})
    assert temp_collection.aggregate("score", "sum") == 60
    assert temp_collection.aggregate("score", "avg") == 20
    assert temp_collection.aggregate("score", "min") == 10
    assert temp_collection.aggregate("score", "max") == 30
