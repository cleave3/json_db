import shutil
import tempfile
import pytest
from pathlib import Path
from json_db.collection import JSONCollection


@pytest.fixture(scope="function")
def temp_collection():
    temp_dir = tempfile.mkdtemp()
    path = Path(temp_dir) / "test.json"
    collection = JSONCollection(path)
    yield collection
    shutil.rmtree(temp_dir)


def test_insert_and_find(temp_collection):
    print("\nTesting insert_one and find...")
    doc = {"name": "Alice", "age": 30, "address": {"city": "London"}}
    temp_collection.insert_one(doc)
    results = temp_collection.find({"name": "Alice"})
    print(f"Inserted: {doc}")
    print(f"Found: {results}")
    assert len(results) == 1
    assert results[0]["name"] == "Alice"
    assert "_id" in results[0]


def test_find_one(temp_collection):
    print("\nTesting find_one...")
    temp_collection.insert_one({"name": "Bob", "age": 25})
    result = temp_collection.find_one({"name": "Bob"})
    print(f"Found one: {result}")
    assert result is not None
    assert result["age"] == 25


def test_update(temp_collection):
    print("\nTesting update...")
    temp_collection.insert_one({"name": "Carol", "age": 22})
    temp_collection.update({"name": "Carol"}, {"age": 23})
    result = temp_collection.find_one({"name": "Carol"})
    print(f"Updated document: {result}")
    assert result["age"] == 23


def test_delete(temp_collection):
    print("\nTesting delete...")
    temp_collection.insert_one({"name": "Dave", "age": 40})
    temp_collection.delete({"name": "Dave"})
    result = temp_collection.find_one({"name": "Dave"})
    print(f"After deletion, found: {result}")
    assert result is None


def test_create_index_and_query(temp_collection):
    print("\nTesting create_index and query...")
    temp_collection.insert_one({"name": "Eve", "age": 28})
    temp_collection.create_index("name")
    results = temp_collection.find({"name": "Eve"})
    print(f"Indexes: {temp_collection.indexes}")
    print(f"Query results: {results}")
    assert len(results) == 1
    assert results[0]["name"] == "Eve"


def test_group_by(temp_collection):
    print("\nTesting group_by...")
    temp_collection.insert_one({"name": "Frank", "age": 20, "group": "A"})
    temp_collection.insert_one({"name": "Grace", "age": 21, "group": "A"})
    temp_collection.insert_one({"name": "Heidi", "age": 22, "group": "B"})
    grouped = temp_collection.group_by("group")
    print(f"Grouped results: {grouped}")
    assert len(grouped["A"]) == 2
    assert len(grouped["B"]) == 1


def test_aggregate(temp_collection):
    print("\nTesting aggregate...")
    temp_collection.insert_one({"name": "Ivan", "score": 10})
    temp_collection.insert_one({"name": "Judy", "score": 20})
    temp_collection.insert_one({"name": "Karl", "score": 30})
    res_sum = temp_collection.aggregate("score", "sum")
    res_avg = temp_collection.aggregate("score", "avg")
    print(f"Sum: {res_sum}, Avg: {res_avg}")
    assert res_sum == 60
    assert res_avg == 20
    assert temp_collection.aggregate("score", "min") == 10
    assert temp_collection.aggregate("score", "max") == 30


def test_index_after_delete(temp_collection):
    print("\nTesting incremental index update after delete...")
    temp_collection.create_index("name")
    temp_collection.insert_one({"name": "Liam", "_id": "123"})
    print(f"Index before delete: {temp_collection.indexes['name']}")
    assert "Liam" in temp_collection.indexes["name"]
    temp_collection.delete({"name": "Liam"})
    print(f"Index after delete: {temp_collection.indexes.get('name', {})}")
    assert "Liam" not in temp_collection.indexes.get("name", {})
    # Verify searching still works
    results = temp_collection.find({"name": "Liam"})
    assert len(results) == 0


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
