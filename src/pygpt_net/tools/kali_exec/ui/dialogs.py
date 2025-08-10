from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QTabWidget
)
from PySide6.QtCore import Qt

class KaliControlDialog(QDialog):
    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.setWindowTitle("Kali Control")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Command input
        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(QLabel("Shell Command:"))
        self.cmd_edit = QLineEdit()
        cmd_layout.addWidget(self.cmd_edit)
        layout.addLayout(cmd_layout)

        # Run button
        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_command)
        layout.addWidget(self.run_btn)

        # Tab widget for output and summary
        self.tabs = QTabWidget()
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        self.summary_edit = QTextEdit()
        self.summary_edit.setReadOnly(True)
        self.tabs.addTab(self.output_edit, "Output")
        self.tabs.addTab(self.summary_edit, "Summary")
        layout.addWidget(self.tabs)

    def run_command(self):
        cmd = self.cmd_edit.text().strip()
        if not cmd:
            self.output_edit.setPlainText("No command entered.")
            self.summary_edit.setPlainText("Summary will appear here...")
            return
        result = self.tool.run({"cmd": cmd})
        output = result.get("output", "")
        summary = result.get("summary", "")
        self.output_edit.setPlainText(output)
        self.summary_edit.setPlainText(summary)