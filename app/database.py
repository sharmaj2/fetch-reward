import sqlite3
from typing import Dict, Any, Optional
import json
from contextlib import contextmanager
from app.models import Receipt, generate_receipt_id

class SQLiteClient:
    def __init__(self, db=":memory:"):
        """Initialize SQLite database with persistent connection"""
        self.db_name = db
        self.conn = sqlite3.connect(self.db_name, uri=True, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def store_receipt(self, receipt: Receipt) -> str:
        receipt_id = generate_receipt_id()
        receipt_json = receipt.model_dump_json()
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO receipts (id, data) VALUES (?, ?)",
            ((receipt_id, receipt_json))
        )
        self.conn.commit()
        return receipt_id

    def get_receipt(self, receipt_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT data FROM receipts WHERE id = ?",
            (receipt_id,)
        )
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None

    def receipt_exists(self, receipt_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT 1 FROM receipts WHERE id = ?",
            (receipt_id,)
        )
        return cursor.fetchone() is not None


# Create a global SQLite client instance
db_client = SQLiteClient(db="file:memdb1?mode=memory&cache=shared")

def get_db_client():
    """Return the SQLite client instance"""
    return db_client