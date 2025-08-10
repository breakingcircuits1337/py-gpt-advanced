import subprocess
from PySide6.QtWidgets import QAction
from PySide6.QtCore import QObject

from .network_diagnostics.ui.dialogs import NetworkDiagnosticsDialog

class NetworkDiagnosticsTool(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def setup_menu(self):
        menubar = self.window.menuBar()
        tools_menu = None
        # Try to find the Tools menu
        for action in menubar.actions():
            if action.text().lower().startswith("tools"):
                tools_menu = action.menu()
                break
        if tools_menu is None:
            # fallback: just use the menubar
            tools_menu = menubar.addMenu("Tools")
        action = QAction("Network Diagnostics", self.window)
        action.triggered.connect(self.show_dialog)
        tools_menu.addAction(action)

    def setup_dialogs(self, dialog_manager):
        dialog_manager.register_dialog("network_diagnostics", lambda: NetworkDiagnosticsDialog(self))

    def show_dialog(self):
        dialog = NetworkDiagnosticsDialog(self.window.tools["network_diagnostics"])
        dialog.exec_()

    def run(self, args):
        command = args.get("command")
        if command == "ping":
            host = args.get("host", "")
            count = args.get("count", "4")
            cmd = ["ping", "-c", count, host]
        elif command == "traceroute":
            host = args.get("host", "")
            cmd = ["traceroute", host]
        elif command == "port_scan":
            host = args.get("host", "")
            ports = args.get("ports", "1-1024")
            # Use nmap if available
            cmd = ["nmap", "-p", ports, host]
        elif command == "dns_lookup":
            domain = args.get("domain", "")
            record_type = args.get("record_type", "A")
            cmd = ["dig", domain, record_type]
        else:
            return {"output": "Unknown command", "success": False}

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            output = proc.stdout if proc.returncode == 0 else proc.stderr
            success = proc.returncode == 0
            return {"output": output, "success": success}
        except Exception as e:
            return {"output": str(e), "success": False}