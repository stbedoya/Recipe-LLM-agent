import logging
from typing import Union, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBHandler:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        """Initialize MongoDB connection.

        Args:
            uri (str): MongoDB connection URI.
            db_name (str): Database name.
            collection_name (str): Collection name.
        """
        try:
            self.client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            logger.info(
                f"Connected to database: {db_name}, collection: {collection_name}"
            )
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise

    async def insert_data(
        self, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Union[ObjectId, List[ObjectId]]:
        """Insert a single or multiple documents into the collection.

        Args:
            data (dict | list[dict]): Document(s) to insert.

        Returns:
            ObjectId | list[ObjectId]: Inserted document ID(s).
        """
        try:
            if isinstance(data, list):
                for item in data:
                    await self._validate_document(item)
                insert_many_result = await self.collection.insert_many(data)
                logger.info(
                    f"Inserted {len(insert_many_result.inserted_ids)} documents."
                )
                return insert_many_result.inserted_ids
            else:
                await self._validate_document(data)
                insert_one_result = await self.collection.insert_one(data)
                logger.info(
                    f"Inserted document with ID: {insert_one_result.inserted_id}"
                )
                return insert_one_result.inserted_id
        except errors.DuplicateKeyError:
            logger.error("Duplicate user_id detected. Ensure uniqueness.")
            raise ValueError("Duplicate user_id detected.")
        except errors.BulkWriteError:
            logger.error("Bulk insert error: Duplicate user_id detected.")
            raise ValueError("Duplicate user_id detected in batch insert.")
        except errors.PyMongoError as e:
            logger.error(f"MongoDB error during insert: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error inserting data: {e}")
            raise

    async def fetch_data(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch documents based on a query asynchronously.

        Args:
            query (dict): MongoDB query filter.

        Returns:
            list[dict]: Retrieved documents.
        """
        if query is None:
            query = {}
        try:
            cursor = self.collection.find(query)
            result = await cursor.to_list(length=None)
            logger.info(f"Fetched {len(result)} documents.")
            return result
        except errors.PyMongoError as e:
            logger.error(f"MongoDB error during fetch: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching data: {e}")
            raise

    async def update_data(
        self, query: Dict[str, Any], new_values: Dict[str, Any]
    ) -> int:
        """Update documents that match the query asynchronously.

        Args:
            query (dict): Filter to find documents.
            new_values (dict): New values to update.

        Returns:
            int: Number of modified documents.
        """
        if not query:
            raise ValueError("Update query cannot be empty.")
        try:
            result = await self.collection.update_many(
                query, {"$set": new_values}
            )
            logger.info(f"Updated {result.modified_count} documents.")
            return result.modified_count
        except errors.PyMongoError as e:
            logger.error(f"MongoDB error during update: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error updating data: {e}")
            raise

    async def delete_data(self, query: Dict[str, Any]) -> int:
        """Delete documents based on a query asynchronously.

        Args:
            query (dict): Filter to find documents.

        Returns:
            int: Number of deleted documents.
        """
        if not query:
            raise ValueError("Delete query cannot be empty.")
        try:
            result = await self.collection.delete_many(query)
            logger.info(f"Deleted {result.deleted_count} documents.")
            return result.deleted_count
        except errors.PyMongoError as e:
            logger.error(f"MongoDB error during delete: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting data: {e}")
            raise

    async def close_connection(self) -> None:
        """Close the MongoDB connection asynchronously."""
        try:
            self.client.close()
            logger.info("MongoDB connection closed.")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
            raise

    async def _validate_document(self, document: Dict[str, Any]) -> None:
        """Ensure `user_id` is correctly structured.

        Args:
            document (dict): Document to validate.

        Raises:
            ValueError: If `user_id` is missing.
        """
        if "user_id" not in document:
            raise ValueError("Each document must include a 'user_id' field.")
