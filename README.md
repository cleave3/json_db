# JSON DB Engine

A lightweight, document-oriented database using JSON for data persistence. Inspired by MongoDB, this project supports nested queries, indexing for faster lookups, query operators, and a familiar API.

## Features

- **Document-based storage**: Data is stored in simple JSON files.
- **Automatic `_id` generation**: Every document gets a unique UUID if not provided.
- **Advanced Querying**: Supports nested field lookups and a variety of query operators.
- **Indexing**: Create indexes on specific fields to speed up queries.
- **Aggregation & Grouping**: Perform SQL-like `GROUP BY` and aggregations (`sum`, `avg`, `min`, `max`).
- **Persistence**: Data is automatically saved to disk after write operations.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/cleave3/json_db.git
cd json_db

# Install dependencies using uv
uv sync
```

---

## API Reference

### `JSONDatabase`
The main entry point for managing collections.

- `db = JSONDatabase(base_path="storage")`: Initialize the database with a storage directory.
- `collection = db.get_collection(name)`: Get or create a collection by name.

### `JSONCollection`
Represents a single collection of documents.

- `insert_one(document)`: Inserts a single document.
- `find(query)`: Returns a list of documents matching the query.
- `find_one(query)`: Returns the first document matching the query, or `None`.
- `update(query, updates)`: Updates all documents matching the query with the provided fields.
- `delete(query)`: Deletes all documents matching the query.
- `create_index(field)`: Creates an index on the specified field.
- `group_by(field)`: Groups documents by a specific field.
- `aggregate(field, operation)`: Performs an aggregation (`sum`, `avg`, `min`, `max`) on a numeric field.

---

## Basic Usage

```python
from json_db import JSONDatabase

# Initialize DB
db = JSONDatabase()
users = db.get_collection("users")

# Insert
users.insert_one({
    "name": "Alice", 
    "age": 30, 
    "address": {"city": "London", "zip": "SW1A"}
})

# Custom _id (optional)
users.insert_one({"_id": "custom-id-123", "name": "Bob"})

# Find with nested field
user = users.find_one({"address.city": "London"})
print(user)

# Update
users.update({"name": "Alice"}, {"age": 31})

# Aggregate
total_age = users.aggregate("age", "sum")
print(f"Total Age: {total_age}")
```

---

## Query Operators

JSON DB supports several operators for advanced filtering:

| Operator | Description | Example |
| :--- | :--- | :--- |
| `$gt` | Greater than | `{"age": {"$gt": 25}}` |
| `$lt` | Less than | `{"age": {"$lt": 40}}` |
| `$gte` | Greater than or equal | `{"age": {"$gte": 30}}` |
| `$lte` | Less than or equal | `{"age": {"$lte": 30}}` |
| `$ne` | Not equal | `{"status": {"$ne": "active"}}` |
| `$in` | Value in list | `{"tags": {"$in": ["python", "db"]}}` |
| `$regex`| Regular expression | `{"name": {"$regex": "^A.*"}}` |

### Complex Query Example
```python
results = users.find({
    "age": {"$gte": 20, "$lte": 50},
    "address.city": {"$in": ["London", "Paris"]},
    "name": {"$regex": "i"}
})
```

---

## Indexing for Performance

Indexes significantly speed up `find` operations by avoiding full collection scans.

```python
# Create an index on the 'email' field
users.create_index("email")

# Subsequent queries on 'email' will use the index
user = users.find_one({"email": "alice@example.com"})
```

---

## Aggregation & Grouping

### Group By
Groups documents by a specific field (supports nested fields).
```python
# Group users by city
cities = users.group_by("address.city")
for city, docs in cities.items():
    print(f"{city}: {len(docs)} users")
```

### Aggregate
Performs calculations on numeric fields. Supported operations: `sum`, `avg`, `min`, `max`.
```python
average_age = users.aggregate("age", "avg")
oldest_user = users.aggregate("age", "max")
```

---

## Testing

Run the test suite with verbose output to see the results of each test case:

```bash
uv run pytest -s test_collection.py
```

---

## Limitations
- **Not Thread-Safe**: This is a lightweight engine designed for single-process use.
- **In-Memory Reads**: Reads the entire collection into memory for operations (suitable for small to medium datasets).

## Contributing
Pull requests are welcome! For major changes, please open an issue first.

## License
[MIT](LICENSE)
