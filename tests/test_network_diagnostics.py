import pytest
import subprocess

from types import SimpleNamespace

from pygpt_net.tools.network_diagnostics import NetworkDiagnosticsTool

@pytest.fixture
def tool():
    # For run() tests, window can be None
    return NetworkDiagnosticsTool(None)

def mock_run_success(cmd, stdout="success", stderr="", **kwargs):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr=stderr)

def mock_run_failure(cmd, stdout="", stderr="error", **kwargs):
    return SimpleNamespace(returncode=1, stdout=stdout, stderr=stderr)

@pytest.mark.parametrize("args,expected_cmd,success,output_key", [
    ({"command": "ping", "host": "example.com", "count": "3"}, ["ping", "-c", "3", "example.com"], True, "stdout"),
    ({"command": "traceroute", "host": "example.com"}, ["traceroute", "example.com"], True, "stdout"),
    ({"command": "port_scan", "host": "example.com", "ports": "80"}, ["nmap", "-p", "80", "example.com"], True, "stdout"),
    ({"command": "dns_lookup", "domain": "example.com", "record_type": "A"}, ["dig", "+short", "A", "example.com"], True, "stdout"),
])
def test_run_success(monkeypatch, tool, args, expected_cmd, success, output_key):
    def fake_run(cmd, **kwargs):
        assert cmd == expected_cmd
        return SimpleNamespace(returncode=0, stdout="mocked output", stderr="")
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = tool.run(args)
    assert result["success"] is True
    assert "mocked output" in result["output"]

@pytest.mark.parametrize("args,expected_cmd", [
    ({"command": "ping", "host": "example.com", "count": "2"}, ["ping", "-c", "2", "example.com"]),
    ({"command": "traceroute", "host": "example.com"}, ["traceroute", "example.com"]),
    ({"command": "port_scan", "host": "example.com", "ports": "1-1024"}, ["nmap", "-p", "1-1024", "example.com"]),
    ({"command": "dns_lookup", "domain": "example.com", "record_type": "MX"}, ["dig", "+short", "MX", "example.com"]),
])
def test_run_failure(monkeypatch, tool, args, expected_cmd):
    def fake_run(cmd, **kwargs):
        assert cmd == expected_cmd
        return SimpleNamespace(returncode=1, stdout="", stderr="failure error")
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = tool.run(args)
    assert result["success"] is False
    assert "Error running command:" in result["output"]
    assert "failure error" in result["output"]

def test_missing_parameters(monkeypatch, tool):
    # ping missing host
    result = tool.run({"command": "ping"})
    assert result["success"] is False
    assert "host" in result["output"]

    # traceroute missing host
    result = tool.run({"command": "traceroute"})
    assert result["success"] is False
    assert "host" in result["output"]

    # port_scan missing host
    result = tool.run({"command": "port_scan"})
    assert result["success"] is False
    assert "host" in result["output"]

    # dns_lookup missing domain
    result = tool.run({"command": "dns_lookup"})
    assert result["success"] is False
    assert "domain" in result["output"]

def test_unknown_command(tool):
    result = tool.run({"command": "foobar"})
    assert result["success"] is False
    assert "Unknown command" in result["output"]