"""
Test configuration and fixtures for the Mergington High School API
"""

import mongomock
from unittest.mock import patch

# Patch pymongo.MongoClient at module level so it applies before any import
_mongo_patcher = patch("pymongo.MongoClient", mongomock.MongoClient)
_mongo_patcher.start()

import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.backend import database


@pytest.fixture(scope="session")
def client():
    database.init_database()
    with TestClient(app) as c:
        yield c
