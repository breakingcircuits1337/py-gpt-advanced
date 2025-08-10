import pytest
from types import SimpleNamespace
from pygpt_net.tools.kali_exec import KaliExecTool

class DummyLLM:
    def __init__(self):
        self.prompt = None
        self.called = False
    def complete(self, prompt):
        self.prompt = prompt
        self.called = True
        return "LLM summary here"

class DummyCore:
    def __init__(self):
        self.llm = DummyLLM()

class DummyWindow:
    def __init__(self):
        self.core = DummyCore()

@pytest.fixture
def tool(monkeypatch):
    window = DummyWindow()
    t = KaliExecTool(window)
    # Always confirm execution
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.question", lambda *a, **k: 16384)  # QMessageBox.Yes
    return t

def test_run_success(monkeypatch, tool):
    # Mock subprocess.run to simulate successful command
    def fake_run(cmd, **kwargs):
        return SimpleNamespace(returncode=0, stdout="command output", stderr="")
    monkeypatch.setattr("subprocess.run", fake_run)
    # LLM summary will be "LLM summary here"
    result = tool.run({"cmd": "ls -l"})
    assert result["success"] is True
    assert "command output" in result["output"]
    assert result["summary"] == "LLM summary here"
    # Ensure the LLM was called with correct prompt
    assert "Summarize the results of the command" in tool.window.core.llm.prompt

def test_run_failure(monkeypatch):
    window = DummyWindow()
    t = KaliExecTool(window)
    # Always confirm execution
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.question", lambda *a, **k: 16384)  # QMessageBox.Yes
    # subprocess.run returns error
    def fake_run(cmd, **kwargs):
        return SimpleNamespace(returncode=1, stdout="", stderr="error output")
    monkeypatch.setattr("subprocess.run", fake_run)
    result = t.run({"cmd": "badcmd"})
    assert result["success"] is False
    assert "error output" in result["output"]
    assert result["summary"] == "LLM summary here"

def test_run_aborted(monkeypatch):
    window = DummyWindow()
    t = KaliExecTool(window)
    # Simulate user clicking "No"
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.question", lambda *a, **k: 65536)  # QMessageBox.No
    result = t.run({"cmd": "echo test"})
    assert result["success"] is False
    assert result["output"] == "Aborted by user"
    assert result["summary"] == ""