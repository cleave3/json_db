# JSON DB Engine

Added group_by and aggregate methods to the JSON DB engine. The group_by method groups documents by a field, and aggregate supports operations like sum, avg, min, and max.
A lightweight document-oriented database using JSON for data persistence. Inspired by MongoDB, this project supports nested queries, indexing for faster lookups, query operators, and a familiar API.

## Features

* Document-based storage using JSON files
* Automatic `_id` generation (UUID)
* Query operators: `$gt`, `$lt`, `$gte`, `$lte`, `$ne`, `$in`, `$regex`
* Nested field query support (e.g., `address.city`)
* Create and use indexes for fast lookup
* Basic operations: `insert_one`, `find`, `find_one`, `update`, `delete`, `group_by`, `aggregate`

## Installation

```bash
pip install json-db-engine  # Assuming packaging is done
```

## Basic Usage

```python
from json_db import JSONDatabase

db = JSONDatabase()
users = db.get_collection("users")

# Insert a document
users.insert_one({"name": "Alice", "age": 30, "address": {"city": "London"}})

# Find documents
results = users.find({"age": {"$gt": 25}})
print(results)

# Find one document
user = users.find_one({"name": "Alice"})
print(user)

# Update documents
users.update({"name": "Alice"}, {"age": 31})

# Delete documents
users.delete({"name": "Alice"})

# Create an index
users.create_index("name")

# Group by a field
grouped = users.group_by("address.city")
print(grouped)

# Aggregate
total_age = users.aggregate("age", "sum")
print(total_age)
```

## Custom Storage Directory

By default, all collections and indexes are stored in the `storage/` directory. However, you can specify a custom directory using the `base_path` parameter:

```python
from json_db_engine import JSONDatabase

db = JSONDatabase(base_path="my_data")
users = db.get_collection("users")
users.insert_one({"name": "Bob", "age": 28})
```

This will store data in:

* `my_data/users.json`
* `my_data/users.index.json`

## Using in Frameworks

### Flask Example

```python
from flask import Flask, jsonify
from json_db_engine import JSONDatabase

app = Flask(__name__)
db = JSONDatabase()

@app.route("/users")
def get_users():
    users = db.get_collection("users")
    return jsonify(users.find())
```

### FastAPI Example

```python
from fastapi import FastAPI
from json_db_engine import JSONDatabase

app = FastAPI()
db = JSONDatabase()

@app.get("/users")
def read_users():
    users = db.get_collection("users")
    return users.find()
```

## Indexing

```python
users = db.get_collection("users")
users.create_index("name")
```

## Advanced Queries

```python
users.find({"age": {"$gt": 20, "$lt": 40}})
users.find({"address.city": "London"})
users.find({"name": {"$regex": "^A"}})
```

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
