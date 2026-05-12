# Owi JSONDB

[![PyPI version](https://img.shields.io/pypi/v/owi-jsondb.svg)](https://pypi.org/project/owi-jsondb/)
[![Downloads](https://static.pepy.tech/badge/owi-jsondb)](https://pepy.tech/project/owi-jsondb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/owi-jsondb.svg)](https://pypi.org/project/owi-jsondb/)
[![GitHub](https://img.shields.io/badge/GitHub-cleave3%2Fowi--jsondb-blue?logo=github)](https://github.com/cleave3/owi-jsondb)

**Owi JSONDB** is a lightweight, document-oriented database engine designed for Python applications that need a simple, schema-less data store without the overhead of a full database server. Inspired by MongoDB, it provides a familiar API, supports nested queries, indexing, and powerful aggregation tools—all using standard JSON files for persistence.

---

## 🚀 Key Features

- **📂 Document-Oriented**: Store data as flexible, schema-less JSON documents.
- **🆔 Auto-ID**: Automatic UUID generation for every document (custom IDs also supported).
- **🔍 Advanced Querying**: Support for nested field lookups (e.g., `user.profile.city`) and rich query operators.
- **⚡ Fast Performance**: In-memory data processing with disk-based indexing for optimized lookups.
- **📊 Aggregations**: Built-in support for `GROUP BY` and numeric aggregations (`sum`, `avg`, `min`, `max`).
- **🛡️ Simple & Reliable**: Pure Python implementation with automatic data persistence on writes.

---

## 📦 Supported Data Types

Owi JSONDB supports all standard JSON-serializable Python types:
- **Primitives**: `str`, `int`, `float`, `bool`, `None`.
- **Collections**: `list` (Arrays) and `dict` (Objects).

---

## 🛠️ Installation

```bash
pip install owi-jsondb
```

Or using `uv`:

```bash
uv add owi-jsondb
```

---

## 📖 Complete Use Case Guide

### 1. Database & Collection Management
Initialize your database and access collections.

```python
from owi_jsondb import JSONDatabase

# Initialize with a custom storage path (defaults to "storage")
db = JSONDatabase(base_path="my_app_data")

# Get or create a collection
users = db.get_collection("users")
products = db.get_collection("products")
```

### 2. Inserting Documents
Supports automatic ID generation or manual ID assignment.

```python
# Insert with auto-generated UUID
users.insert_one({"name": "Alice", "age": 30})

# Insert with a custom manual _id
users.insert_one({"_id": "user_101", "name": "Bob", "role": "admin"})
```

### 3. Finding Documents
Powerful filtering with support for nested fields.

```python
# Find all documents
all_users = users.find()

# Find with exact match
admins = users.find({"role": "admin"})

# Find ONE document
bob = users.find_one({"_id": "user_101"})

# Deeply nested field lookup
uk_users = users.find({"address.country": "UK"})
```

### 4. Advanced Query Operators
Filter data using MongoDB-like operators.

```python
# Greater Than / Less Than
young_users = users.find({"age": {"$lt": 25}})
senior_users = users.find({"age": {"$gte": 65}})

# Not Equal
active_users = users.find({"status": {"$ne": "banned"}})

# In List
specific_groups = users.find({"group": {"$in": ["A", "C"]}})

# Regular Expressions (Case-insensitive search)
smiths = users.find({"name": {"$regex": "(?i)smith"}})

# Multiple operators on one field
filtered = users.find({"score": {"$gt": 50, "$lt": 100}})
```

### 5. Updating Data
Modify existing documents using filters.

```python
# Update a single document's field
users.update({"_id": "user_101"}, {"role": "super-admin"})

# Bulk update all matching documents
users.update({"status": "active"}, {"last_login": "2024-01-01"})
```

### 6. Deleting Data
Remove documents selectively.

```python
# Delete a specific document
users.delete({"_id": "user_101"})

# Bulk delete
users.delete({"age": {"$lt": 18}})

# Delete all documents in a collection
users.delete({})
```

### 7. Indexing for Speed
Significantly improve performance for large datasets.

```python
# Create index on the 'email' field
users.create_index("email")

# Create index on a NESTED field
users.create_index("metadata.auth_id")

# Queries on these fields will now use the fast index lookup
user = users.find_one({"email": "alice@example.com"})
```

> **💡 Pro Tip**: Owi JSONDB maintains index files (`.index.json`) automatically. Calling `create_index()` is idempotent and can be safely called every time your app starts.

---

## 📝 Simple Application Example: Todo List

```python
from owi_jsondb import JSONDatabase

# Setup
db = JSONDatabase(base_path="todo_app")
tasks = db.get_collection("tasks")
tasks.create_index("name") # create index

# Add tasks
tasks.insert_one({"title": "Record Demo", "priority": 1, "completed": False})
tasks.insert_one({"title": "Publish Package", "priority": 0, "completed": False})

# Mark task as completed
tasks.update({"title": "Record Demo"}, {"completed": True})

# Get pending high-priority tasks
high_priority = tasks.find({"priority": {"$lt": 1}, "completed": False})
print(f"Pending High Priority: {[t['title'] for t in high_priority]}")
```

---

## 📊 Aggregation & Grouping

#### Group By
```python
# Group documents by city
by_city = users.group_by("address.city")
```

#### Numeric Aggregations
```python
# Supported: sum, avg, min, max
total_score = users.aggregate("score", "sum")
average_age = users.aggregate("age", "avg")
oldest_user = users.aggregate("age", "max")
youngest_user = users.aggregate("age", "min")
```

---

## 🔍 Operator Summary Table

| Operator | Function | Example Usage |
| :--- | :--- | :--- |
| `$gt` | Greater than | `{"age": {"$gt": 21}}` |
| `$lt` | Less than | `{"price": {"$lt": 9.99}}` |
| `$gte` | Greater or equal | `{"score": {"$gte": 50}}` |
| `$lte` | Less or equal | `{"stock": {"$lte": 10}}` |
| `$ne` | Not equal | `{"type": {"$ne": "internal"}}` |
| `$in` | Exists in list | `{"tags": {"$in": ["python", "db"]}}` |
| `$regex`| Regex match | `{"name": {"$regex": "^A.*"}}` |

---

## 📂 API Reference

### `JSONDatabase`
- `JSONDatabase(base_path="storage")`: Initialize database directory.
- `get_collection(name)`: Returns a `JSONCollection` instance.

### `JSONCollection`
- `insert_one(document)`: Add a document.
- `find(query={})`: Find matching documents.
- `find_one(query={})`: Find first match.
- `update(query, updates)`: Update matching documents.
- `delete(query)`: Remove matching documents.
- `create_index(field)`: Enable indexing for a field.
- `group_by(field)`: Group by field value.
- `aggregate(field, operation)`: `sum`, `avg`, `min`, `max`.

---

## 🧪 Testing

```bash
uv run pytest -s test_collection.py
```

---

## 🔗 Links
- **GitHub**: [cleave3/owi-jsondb](https://github.com/cleave3/owi-jsondb)
- **PyPI**: [owi-jsondb](https://pypi.org/project/owi-jsondb/)
- **Issues**: [Report a bug](https://github.com/cleave3/owi-jsondb/issues)

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.
