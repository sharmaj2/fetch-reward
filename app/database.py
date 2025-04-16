import sqlite3
from typing import Dict, Any, Optional
import json
from app.models import Receipt, generate_receipt_id
from collections import defaultdict


class SQLiteClient:
    def __init__(self, db="file:memdb1?mode=memory&cache=shared"):
        """Initialize SQLite database with persistent connection"""
        self.db_name = db
        self.conn = sqlite3.connect(self.db_name, uri=True, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS receipts (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL
        )
        """
        )
        self.conn.commit()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS receipts_data (
            id TEXT PRIMARY KEY,
            retailer TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            purchase_time TEXT NOT NULL,
            total TEXT NOT NULL             
        )
        """
        )
        self.conn.commit()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS receipt_items (
            receipt_id TEXT NOT NULL,
            short_description TEXT NOT NULL,
            price TEXT NOT NULL,
            FOREIGN KEY(receipt_id) REFERENCES receipts_data(id)         
        )
        """
        )
        self.conn.commit()

    def store_receipt(self, receipt: Receipt) -> str:
        receipt_id = generate_receipt_id()
        receipt_json = receipt.model_dump_json()

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO receipts (id, data) VALUES (?, ?)",
            ((receipt_id, receipt_json)),
        )
        self.conn.commit()
        return receipt_id

    def store_receipt_data(self, receipt_id: str, receipt: Receipt) -> str:
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO receipts_data (id, retailer, purchase_date, purchase_time, total) VALUES (?, ?, ?, ?, ?)",
                (
                    receipt_id,
                    receipt.retailer,
                    receipt.purchaseDate,
                    receipt.purchaseTime.strftime("%H:%M:%S"),
                    receipt.total,
                ),
            )
            self.conn.commit()

            for item in receipt.items:
                cursor.execute(
                    "INSERT INTO receipt_items (receipt_id, short_description, price) VALUES (?, ?, ?)",
                    (receipt_id, item.shortDescription, item.price),
                )

            self.conn.commit()

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to store receipt data: {str(e)}")

    def get_receipt(self, receipt_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM receipts WHERE id = ?", (receipt_id,))
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None
    

    def get_receipt_data(self, receipt_id: str):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT 
                            r.id,
                            r.retailer,
                            r.purchase_date,
                            r.purchase_time,
                            r.total,
                            i.short_description,
                            i.price
                        FROM receipts_data r
                        INNER JOIN receipt_items i ON r.id = i.receipt_id
                        WHERE r.id = ?
                        """, (receipt_id,))
        rows = cursor.fetchall()

        if not rows:
            return None  # Or raise HTTP 404 if using FastAPI

        # Start with the first row to build the base receipt
        first = rows[0]
        receipt = {
            "id": first[0],
            "retailer": first[1],
            "purchaseDate": first[2],
            "purchaseTime": first[3],
            "total": first[4],
            "items": []
        }

        # Add all items
        for row in rows:
            item = {
                "shortDescription": row[5],
                "price": row[6]
            }
            receipt["items"].append(item)

        return receipt


    # def receipt_exists(self, receipt_id: str) -> bool:
    #     cursor = self.conn.cursor()
    #     cursor.execute(
    #         "SELECT 1 FROM receipts WHERE id = ?",
    #         (receipt_id,)
    #     )
    #     return cursor.fetchone() is not None


# Create a global SQLite client instance
db_client = SQLiteClient()


def get_db_client():
    """Return the SQLite client instance"""
    return db_client
