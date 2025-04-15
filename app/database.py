import redis
import os
from typing import Dict, Any, Optional
import json
from app.models import Receipt, generate_receipt_id


class RedisClient:
    def __init__(self, host="localhost", port=6379):
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
        self.client = redis.Redis(host=host, port=port, db=0, decode_responses=True)

    def store_receipt(self, receipt: Receipt) -> str:
        receipt_id = generate_receipt_id()
        receipt_json = receipt.model_dump_json()
        self.client.set(receipt_id, receipt_json)
        return receipt_id

    def get_receipt(self, receipt_id: str) -> Optional[Dict[str, Any]]:
        value = self.client.get(receipt_id)
        return json.loads(value) if value else None

    def receipt_exists(self, receipt_id: str) -> bool:
        return self.client.exists(receipt_id) == 1


# Singleton Redis client
db_client = RedisClient()


def get_db_client():
    return db_client


# # Create a global SQLite client instance
# db_client = SQLiteClient()

# def get_db_client():
#     """Return the SQLite client instance"""
#     return db_client
