import unittest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorClient
from src.db.mongodb_handler import MongoDBHandler  # Replace with your actual import path


class TestMongoDBHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """Set up the mock MongoDB client and handler."""
        # Mock the AsyncIOMotorClient
        self.mock_client = MagicMock(spec=AsyncIOMotorClient)
        self.mock_db = MagicMock()
        self.mock_collection = MagicMock()

        # Setting up mock client return values
        self.mock_client.__getitem__.return_value = self.mock_db
        self.mock_db.__getitem__.return_value = self.mock_collection

        # Create the MongoDBHandler instance with the mock
        self.handler = MongoDBHandler("mock_uri", "mock_db", "mock_collection")
        self.handler.client = self.mock_client
        self.handler.db = self.mock_db
        self.handler.collection = self.mock_collection

    async def test_insert_single_document(self):
        """Test inserting a single document."""
        document = {"user_id": 123, "name": "John Doe"}

        # Mock the insert_one return value
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_id = ObjectId()
        self.mock_collection.insert_one = AsyncMock(return_value=mock_insert_result)

        # Call the insert_data method
        inserted_id = await self.handler.insert_data(document)

        # Assert the return value
        self.assertIsInstance(inserted_id, ObjectId)

        # Check that insert_one was called with the correct document
        self.mock_collection.insert_one.assert_awaited_with(document)

    async def test_insert_multiple_documents(self):
        """Test inserting multiple documents."""
        documents = [{"user_id": 123, "name": "John Doe"}, {"user_id": 124, "name": "Jane Doe"}]

        # Mock the insert_many return value
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_ids = [ObjectId(), ObjectId()]
        self.mock_collection.insert_many = AsyncMock(return_value=mock_insert_result)

        # Call the insert_data method
        inserted_ids = await self.handler.insert_data(documents)

        # Assert the return value
        self.assertEqual(len(inserted_ids), 2)
        self.assertTrue(all(isinstance(id, ObjectId) for id in inserted_ids))

        # Check that insert_many was called with the correct documents
        self.mock_collection.insert_many.assert_awaited_with(documents)

    async def test_insert_duplicate_key_error(self):
        """Test handling duplicate key error."""
        document = {"user_id": 123, "name": "John Doe"}

        # Mock the insert_one to raise a DuplicateKeyError
        self.mock_collection.insert_one = AsyncMock(side_effect=DuplicateKeyError)

        # Call the insert_data method and assert the exception is raised
        with self.assertRaises(ValueError):
            await self.handler.insert_data(document)

    async def test_fetch_data(self):
        """Test fetching data from the collection."""
        query = {"user_id": 123}
        mock_cursor = MagicMock()
        mock_cursor.to_list = AsyncMock(return_value=[{"user_id": 123, "name": "John Doe"}])
        self.mock_collection.find = AsyncMock(return_value=mock_cursor)

        # Call the fetch_data method
        result = await self.handler.fetch_data(query)

        # Assert the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "John Doe")

        # Check that find was called with the correct query
        self.mock_collection.find.assert_awaited_with(query)

    async def test_update_data(self):
        """Test updating documents."""
        query = {"user_id": 123}
        new_values = {"name": "John Updated"}

        # Mock the update_many return value
        mock_update_result = MagicMock()
        mock_update_result.modified_count = 1
        self.mock_collection.update_many = AsyncMock(return_value=mock_update_result)

        # Call the update_data method
        modified_count = await self.handler.update_data(query, new_values)

        # Assert the result
        self.assertEqual(modified_count, 1)

        # Check that update_many was called with the correct arguments
        self.mock_collection.update_many.assert_awaited_with(query, {"$set": new_values})

    async def test_delete_data(self):
        """Test deleting data from the collection."""
        query = {"user_id": 123}

        # Mock the delete_many return value
        mock_delete_result = MagicMock()
        mock_delete_result.deleted_count = 1
        self.mock_collection.delete_many = AsyncMock(return_value=mock_delete_result)

        # Call the delete_data method
        deleted_count = await self.handler.delete_data(query)

        # Assert the result
        self.assertEqual(deleted_count, 1)

        # Check that delete_many was called with the correct query
        self.mock_collection.delete_many.assert_awaited_with(query)

    async def test_close_connection(self):
        """Test closing the connection."""
        # Mock the close method
        self.mock_client.close = AsyncMock()

        # Call the close_connection method
        await self.handler.close_connection()

        # Assert the close method was called
        self.mock_client.close.assert_awaited_once()

    async def test_validate_document_missing_user_id(self):
        """Test validation when 'user_id' is missing."""
        document = {"name": "John Doe"}
        
        # Call _validate_document and assert ValueError is raised
        with self.assertRaises(ValueError):
            await self.handler._validate_document(document)

if __name__ == "__main__":
    unittest.main()




# import unittest
# from unittest.mock import AsyncMock, patch
# from bson import ObjectId
# from pymongo import errors
# from src.db.mongodb_handler import MongoDBHandler  # Import MongoDBHandler from the correct module

# class TestMongoDBHandler(unittest.TestCase):

#     @patch("src.db.mongodb_handler.AsyncIOMotorClient")  # Mock AsyncIOMotorClient from mongodb_handler
#     def setUp(self, MockAsyncIOMotorClient):
#         """Set up the mock MongoDB client and collection for the tests."""
#         self.mock_client = AsyncMock()
#         self.mock_db = AsyncMock()
#         self.mock_collection = AsyncMock()

#         MockAsyncIOMotorClient.return_value = self.mock_client
#         self.mock_client.__getitem__.return_value = self.mock_db
#         self.mock_db.__getitem__.return_value = self.mock_collection

#         # Initialize MongoDBHandler with mock values
#         self.uri = "mongodb://localhost:27017"
#         self.db_name = "test_db"
#         self.collection_name = "test_collection"
#         self.handler = MongoDBHandler(self.uri, self.db_name, self.collection_name)

#     async def test_insert_data_single(self):
#         """Test inserting a single document."""
#         document = {"_id": ObjectId(), "user_id": 123, "name": "John Doe"}

#         # Mock insert_one
#         self.mock_collection.insert_one.return_value.inserted_id = ObjectId()

#         # Call insert_data method
#         inserted_id = await self.handler.insert_data(document)

#         # Assertions
#         self.mock_collection.insert_one.assert_called_once_with(document)
#         self.assertIsInstance(inserted_id, ObjectId)

#     async def test_insert_data_multiple(self):
#         """Test inserting multiple documents."""
#         documents = [
#             {"_id": ObjectId(), "user_id": 123, "name": "John Doe"},
#             {"_id": ObjectId(), "user_id": 124, "name": "Jane Doe"},
#         ]

#         # Mock insert_many
#         self.mock_collection.insert_many.return_value.inserted_ids = [ObjectId(), ObjectId()]

#         # Call insert_data method
#         inserted_ids = await self.handler.insert_data(documents)

#         # Assertions
#         self.mock_collection.insert_many.assert_called_once_with(documents)
#         self.assertEqual(len(inserted_ids), 2)

#     async def test_insert_data_duplicate_key_error(self):
#         """Test inserting data that causes a duplicate key error."""
#         document = {"_id": ObjectId(), "user_id": 123, "name": "John Doe"}

#         # Simulate a duplicate key error
#         self.mock_collection.insert_one.side_effect = errors.DuplicateKeyError("duplicate key error")

#         with self.assertRaises(ValueError):
#             await self.handler.insert_data(document)

#     async def test_fetch_data(self):
#         """Test fetching data from MongoDB."""
#         # Simulate a fetched result
#         self.mock_collection.find.return_value.to_list.return_value = [{"_id": ObjectId(), "user_id": 123, "name": "John Doe"}]

#         result = await self.handler.fetch_data()

#         # Assertions
#         self.mock_collection.find.assert_called_once_with({})
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]["user_id"], 123)

#     async def test_update_data(self):
#         """Test updating documents."""
#         query = {"user_id": 123}
#         new_values = {"name": "John Doe Updated"}

#         # Mock update_many
#         self.mock_collection.update_many.return_value.modified_count = 1

#         modified_count = await self.handler.update_data(query, new_values)

#         # Assertions
#         self.mock_collection.update_many.assert_called_once_with(query, {"$set": new_values})
#         self.assertEqual(modified_count, 1)

#     async def test_delete_data(self):
#         """Test deleting documents."""
#         query = {"user_id": 123}

#         # Mock delete_many
#         self.mock_collection.delete_many.return_value.deleted_count = 1

#         deleted_count = await self.handler.delete_data(query)

#         # Assertions
#         self.mock_collection.delete_many.assert_called_once_with(query)
#         self.assertEqual(deleted_count, 1)

#     async def test_close_connection(self):
#         """Test closing the connection."""
#         # Mock close method
#         self.mock_client.close = AsyncMock()

#         # Call close_connection method
#         await self.handler.close_connection()

#         # Assertions
#         self.mock_client.close.assert_called_once()


# if __name__ == "__main__":
#     unittest.main()






# import unittest
# from bson import ObjectId
# from unittest.mock import patch, MagicMock
# from pymongo.errors import PyMongoError, ConnectionFailure, DuplicateKeyError
# from src.db.mongodb_handler import MongoDBHandler


# class TestMongoDBHandler(unittest.TestCase):
#     """Unit tests for MongoDBHandler class."""

#     def setUp(self):
#         self.mock_client = MagicMock()
#         self.mock_db = MagicMock()
#         self.mock_collection = MagicMock()

#         patcher = patch(
#             "src.db.mongodb_handler.MongoClient", return_value=self.mock_client
#         )
#         self.addCleanup(patcher.stop)
#         self.mock_mongo_client = patcher.start()
#         self.mock_client.__getitem__.return_value = self.mock_db
#         self.mock_db.__getitem__.return_value = self.mock_collection

#         self.handler = MongoDBHandler(
#             uri="mongodb://mockhost:27017/",
#             db_name="testdb",
#             collection_name="testcollection",
#         )

#         self.mock_id = ObjectId()

#         self.sample_data = {
#             "_id": self.mock_id,
#             "user_id": "USR-12556",
#             "client_name": "stefany",
#             "ingredients": [
#                 {"name": "onions", "like": True},
#                 {"name": "chicken", "like": True},
#             ],
#         }

#     def tearDown(self):
#         """Close mock MongoDB connection."""
#         self.handler.close_connection()

#     def test_insert_data_single(self):
#         """Test inserting a single document successfully with _id and user_id."""
#         self.mock_collection.insert_one.return_value.inserted_id = self.mock_id

#         result = self.handler.insert_data(self.sample_data)

#         self.mock_collection.insert_one.assert_called_once_with(
#             self.sample_data
#         )
#         self.assertEqual(result, self.mock_id)

#     def test_insert_data_multiple(self):
#         """Test inserting multiple documents successfully with _id and user_id."""
#         self.mock_collection.insert_many.return_value.inserted_ids = [
#             self.mock_id,
#             ObjectId(),
#         ]

#         data = [
#             self.sample_data,
#             {
#                 "_id": ObjectId(),
#                 "user_id": "USR-12557",
#                 "client_name": "john",
#                 "ingredients": [{"name": "tomato", "like": False}],
#             },
#         ]
#         result = self.handler.insert_data(data)

#         self.mock_collection.insert_many.assert_called_once_with(data)
#         self.assertEqual(len(result), 2)

#     def test_insert_data_duplicate_user_id(self):
#         """Test handling of duplicate user_id."""
#         self.mock_collection.insert_one.side_effect = DuplicateKeyError(
#             "Duplicate user_id"
#         )

#         with self.assertRaises(ValueError):
#             self.handler.insert_data(self.sample_data)

#     def test_fetch_data(self):
#         """Test fetching documents successfully."""
#         self.mock_collection.find.return_value = [self.sample_data]

#         result = self.handler.fetch_data()
#         self.mock_collection.find.assert_called_once_with({})
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]["user_id"], "USR-12556")
#         self.assertEqual(result[0]["client_name"], "stefany")
#         self.assertEqual(result[0]["ingredients"][0]["name"], "onions")
#         self.assertTrue(result[0]["ingredients"][0]["like"])

#     def test_update_data(self):
#         """Test updating documents successfully."""
#         self.mock_collection.update_many.return_value.modified_count = 1

#         query = {"user_id": "USR-12556"}
#         new_values = {"client_name": "updated_stefany"}
#         result = self.handler.update_data(query, new_values)

#         self.mock_collection.update_many.assert_called_once_with(
#             query, {"$set": new_values}
#         )
#         self.assertEqual(result, 1)

#     def test_delete_data(self):
#         """Test deleting documents successfully."""
#         self.mock_collection.delete_many.return_value.deleted_count = 1

#         query = {"user_id": "USR-12556"}
#         result = self.handler.delete_data(query)

#         self.mock_collection.delete_many.assert_called_once_with(query)
#         self.assertEqual(result, 1)


# if __name__ == "__main__":
#     unittest.main()
