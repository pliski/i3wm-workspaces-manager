import pytest
import i3ipc
from unittest.mock import MagicMock

@pytest.fixture
def mock_i3():
    mock = MagicMock(spec=i3ipc.Connection)
    
    # Create workspace mocks with proper attribute access
    def create_workspace_mock(name, focused):
        ws = MagicMock()
        # Ensure name is accessed as a property
        type(ws).name = property(lambda self: name)
        type(ws).focused = property(lambda self: focused)
        return ws
    
    # Mock workspaces response
    mock.get_workspaces.return_value = [
        create_workspace_mock("1", True),
        create_workspace_mock("2", False),
        create_workspace_mock("3", False),
        create_workspace_mock("work", False)
    ]
    return mock 