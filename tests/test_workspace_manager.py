import pytest
from i3wm_workspaces_manager.core.workspace_manager import WorkspaceManager
from unittest.mock import patch, MagicMock

def test_get_next_available_number(mock_i3):
    with patch('i3ipc.Connection', return_value=mock_i3):
        manager = WorkspaceManager()
        assert manager.get_next_available_number() == 4

@pytest.mark.i3required(reason="This test is not working because of the way i3ipc is mocked")
def test_validate_workspace_name():
    manager = WorkspaceManager()
    
    # Test empty name
    is_valid, error = manager.validate_workspace_name("")
    assert not is_valid
    assert error == "Workspace name cannot be empty"
    
    # Test valid name
    is_valid, error = manager.validate_workspace_name("test")
    assert is_valid
    assert error == ""

def test_create_workspace(mock_i3):
    with patch('i3ipc.Connection', return_value=mock_i3):
        manager = WorkspaceManager()
        manager.create_workspace("test")
        mock_i3.command.assert_called_once_with("workspace test")

def test_rename_current_workspace(mock_i3):
    with patch('i3ipc.Connection', return_value=mock_i3):
        manager = WorkspaceManager()
        manager.rename_current_workspace("new_name")
        mock_i3.command.assert_called_once_with("rename workspace to new_name")

def test_get_existing_workspaces(mock_i3):
    with patch('i3ipc.Connection', return_value=mock_i3):
        manager = WorkspaceManager()
        workspaces = manager.get_existing_workspaces()
        assert workspaces == ["1", "2", "3", "work"] 