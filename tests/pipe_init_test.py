"""
pipe_init_test.py

Unit Tests (using pytest) for: class Pipe initialization
"""

# import pipe  +++++++++++++++++++++++++++++++++++++++++++++
import sys
from pathlib import Path

project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import Pipe

# TODO write tests
