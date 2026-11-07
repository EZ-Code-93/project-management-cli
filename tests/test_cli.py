import os
import sys
import json
import pytest
from unittest.mock import patch
import main
from services import storage_service

# ==============================================================================
#   PYTEST FIXTURES (Setup and Tear-down Environments)
# ==============================================================================

@pytest.fixture
def mock_db_env(tmp_path):
    """
    Creates a pristine temporary data folder and points your storage service 
    path straight to it so your production project_data.json stays clean.
    """
    # Create a temporary path directory
    temp_data_dir = tmp_path / "data"
    temp_data_dir.mkdir()
    temp_file = temp_data_dir / "project_data.json"
    
    # Initialize it with empty database structure arrays
    initial_structure = {"users": [], "projects": []}
    temp_file.write_text(json.dumps(initial_structure))
    
    # Patch the storage service path layout to point to our test environment file
    with patch("services.storage_service.DATA_FILE", str(temp_file)):
        yield temp_file

# ==============================================================================
#  HELPERS
# ==============================================================================

def run_cli_command(args_list):
    """Executes main.py with modified command-line flags injected directly."""
    # sys.argv[0] is traditionally the name of the script being run
    with patch.object(sys, 'argv', ['main.py'] + args_list):
        main.main()

# ==============================================================================
#  THE UNIT TESTS
# ==============================================================================

def test_create_user(mock_db_env):
    """Verifies that a user profile registers inside the JSON registry mapping layer."""
    # 1. Trigger the CLI action command
    run_cli_command(["create-user", "--name", "Ezra"])
    
    # 2. Assert structural validation changes by parsing the mock file state
    current_data = storage_service.load_all_data()
    assert len(current_data["users"]) == 1
    assert current_data["users"][0]["name"] == "Ezra"


def test_create_project_enforces_user_existence(mock_db_env, capsys):
    """Verifies that the app safely blocks creation if the owner name doesn't exist."""
    # Try to initialize a project for a non-existent account entry
    run_cli_command([
        "create-project", 
        "--title", "Ghost Project", 
        "--desc", "Testing user boundary blocks", 
        "--due", "2026-11-20", 
        "--user", "Nobody"
    ])
    
    # Read output and verify the system boundary blocks bad assignments
    captured = capsys.readouterr()
    assert "Error: User 'Nobody' does not exist" in captured.out
    
    # Verify that nothing was written to the projects database listing array
    current_data = storage_service.load_all_data()
    assert len(current_data["projects"]) == 0


def test_create_project_success(mock_db_env):
    """Verifies that a project instantiates and automatically populates its timestamp."""
    # 1. Set up prerequisite user registration
    run_cli_command(["create-user", "--name", "Ezra"])
    
    # 2. Create the project target row entry mapping
    run_cli_command([
        "create-project", 
        "--title", "Build CLI", 
        "--desc", "Pytest Suite implementation", 
        "--due", "2026-12-05", 
        "--user", "Ezra"
    ])
    
    # 3. Assert properties were captured accurately
    current_data = storage_service.load_all_data()
    assert len(current_data["projects"]) == 1
    
    proj = current_data["projects"][0]
    assert proj["title"] == "Build CLI"
    assert proj["owner_name"] == "Ezra"
    assert "created_at" in proj  # Confirms dynamic automatic timestamp generation worked!
    assert proj["project_id"] == 1


def test_add_and_update_task_workflow(mock_db_env):
    """Tests the combined lifecycle of adding a task and advancing its status properties."""
    # 1. Setup baseline environment entries
    run_cli_command(["create-user", "--name", "Ezra"])
    run_cli_command(["create-project", "--title", "Core Engine", "--desc", "Test Core", "--due", "2026-12-01", "--user", "Ezra"])
    
    # 2. Add a new nested task slot
    run_cli_command(["add-task", "--project-id", "1", "--desc", "Write test fixtures"])
    
    # Verify task injection succeeded
    data_after_add = storage_service.load_all_data()
    tasks_list = data_after_add["projects"][0]["tasks"]
    assert len(tasks_list) == 1
    assert tasks_list[0]["description"] == "Write test fixtures"
    assert tasks_list[0]["status"] == "Pending"  # Verifies property default configuration rules
    
    # 3. Advance the status property using our new command switch
    run_cli_command(["update-task", "--project-id", "1", "--task-id", "1", "--status", "Complete"])
    
    # Verify state transition saved correctly down inside our model properties
    data_after_update = storage_service.load_all_data()
    updated_task = data_after_update["projects"][0]["tasks"][0]
    assert updated_task["status"] == "Complete"
