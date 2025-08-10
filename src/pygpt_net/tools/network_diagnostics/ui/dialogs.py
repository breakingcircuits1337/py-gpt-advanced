from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor

class NetworkDiagnosticsDialog(QDialog):
    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.setWindowTitle("Network Diagnostics")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Command selector
        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(QLabel("Command:"))
        self.command_combo = QComboBox()
        self.command_combo.addItems(["ping", "traceroute", "port_scan", "dns_lookup"])
        self.command_combo.currentTextChanged.connect(self._update_fields)
        cmd_layout.addWidget(self.command_combo)
        layout.addLayout(cmd_layout)

        # Host/domain input
        self.host_layout = QHBoxLayout()
        self.host_label = QLabel("Host:")
        self.host_edit = QLineEdit()
        self.host_layout.addWidget(self.host_label)
        self.host_layout.addWidget(self.host_edit)
        layout.addLayout(self.host_layout)

        self.domain_layout = QHBoxLayout()
        self.domain_label = QLabel("Domain:")
        self.domain_edit = QLineEdit()
        self.domain_layout.addWidget(self.domain_label)
        self.domain_layout.addWidget(self.domain_edit)
        self.domain_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.domain_layout)
        self.domain_layout.parent = layout

        # Ports (for port_scan)
        self.ports_layout = QHBoxLayout()
        self.ports_label = QLabel("Ports:")
        self.ports_edit = QLineEdit()
        self.ports_edit.setPlaceholderText("e.g. 1-1024")
        self.ports_edit.setText("1-1024")
        self.ports_layout.addWidget(self.ports_label)
        self.ports_layout.addWidget(self.ports_edit)
        layout.addLayout(self.ports_layout)

        # Count (for ping)
        self.count_layout = QHBoxLayout()
        self.count_label = QLabel("Count:")
        self.count_edit = QLineEdit()
        self.count_edit.setText("4")
        self.count_layout.addWidget(self.count_label)
        self.count_layout.addWidget(self.count_edit)
        layout.addLayout(self.count_layout)

        # Record Type (for dns_lookup)
        self.record_layout = QHBoxLayout()
        self.record_label = QLabel("Record Type:")
        self.record_edit = QLineEdit()
        self.record_edit.setText("A")
        self.record_layout.addWidget(self.record_label)
        self.record_layout.addWidget(self.record_edit)
        layout.addLayout(self.record_layout)

        # Output
        layout.addWidget(QLabel("Output:"))
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        # Run button
        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_command)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)
        self._update_fields("ping")

    def _update_fields(self, command):
        # Hide/show fields based on command
        self.host_label.setVisible(command in ("ping", "traceroute", "port_scan"))
        self.host_edit.setVisible(command in ("ping", "traceroute", "port_scan"))
        self.host_layout.setEnabled(command in ("ping", "traceroute", "port_scan"))

        self.domain_label.setVisible(command == "dns_lookup")
        self.domain_edit.setVisible(command == "dns_lookup")
        self.domain_layout.setEnabled(command == "dns_lookup")

        self.ports_label.setVisible(command == "port_scan")
        self.ports_edit.setVisible(command == "port_scan")
        self.ports_layout.setEnabled(command == "port_scan")

        self.count_label.setVisible(command == "ping")
        self.count_edit.setVisible(command == "ping")
        self.count_layout.setEnabled(command == "ping")

        self.record_label.setVisible(command == "dns_lookup")
        self.record_edit.setVisible(command == "dns_lookup")
        self.record_layout.setEnabled(command == "dns_lookup")

    def run_command(self):
        args = {
            "command": self.command_combo.currentText(),
            "host": self.host_edit.text().strip(),
            "domain": self.domain_edit.text().strip(),
            "ports": self.ports_edit.text().strip(),
            "count": self.count_edit.text().strip(),
            "record_type": self.record_edit.text().strip(),
        }
        self.output_edit.clear()
        try:
            result = self.tool.run(args)
            output = result.get("output", "")
            success = result.get("success", True)
            self.display_output(output, success)
        except Exception as e:
            self.display_output(str(e), False)

    def display_output(self, output, success):
        self.output_edit.clear()
        cursor = self.output_edit.textCursor()
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("green" if success else "red"))
        cursor.setCharFormat(fmt)
        cursor.insertText(output)
        self.output_edit.setTextCursor(cursor)
        self.output_edit.ensureCursorVisible()