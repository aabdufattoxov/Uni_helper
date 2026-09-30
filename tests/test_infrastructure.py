import os
import pytest
from uni_helper.infrastructure.database.connection import DatabaseManager

def test_database_initialization(tmp_path):
    # Use a temporary database file for testing
    db_file = tmp_path / "test_uni_helper.db"
    db_url = f"sqlite:///{db_file}"
    
    db_manager = DatabaseManager(db_url=db_url)
    db_manager.init_db()
    
    assert os.path.exists(db_file)
    
    with db_manager.get_session() as session:
        assert session is not None
