import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def add_project_root_into_sys_path():
    project_root_path = str(Path(__file__).resolve().parents[1])
    if project_root_path not in sys.path:
        sys.path.insert(0, project_root_path)
