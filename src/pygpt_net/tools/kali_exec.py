#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# KaliExecTool: Run arbitrary shell commands on Kali #
# MIT License                                        #
# ================================================== #

import subprocess
from typing import Dict

from PySide6.QtWidgets import QMessageBox, QAction
from pygpt_net.tools.base import BaseTool

from .ui.dialogs import KaliControlDialog

class KaliExecTool(BaseTool):
    def __init__(self, window=None):
        super().__init__()
        self.window = window

    def name(self) -> str:
        return "kali_exec"

    def description(self) -> str:
        return "Execute arbitrary shell commands on Kali Linux with user confirmation and summarization"

    def run(self, args: Dict) -> Dict:
        cmd = args.get("cmd", "")
        if not cmd:
            return {"output": "No command specified", "success": False, "summary": ""}

        # Confirm with user before execution
        proceed = QMessageBox.question(
            self.window,
            'Confirm Execution',
            f'About to run: {cmd}\n\nProceed?',
            QMessageBox.Yes | QMessageBox.No
        )
        if proceed != QMessageBox.Yes:
            return {"output": "Aborted by user", "success": False, "summary": ""}

        try:
            proc = subprocess.run(
                ["/bin/bash", "-c", cmd],
                capture_output=True,
                text=True
            )
            output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
            output = output.strip()
            success = proc.returncode == 0

            # LLM-driven summarization
            prompt = (
                f"Summarize the results of the command `{cmd}`:\n"
                "```\n"
                f"{output}\n"
                "```\n"
                "Provide a concise summary, highlighting key successes or errors."
            )
            if (
                hasattr(self.window, "core")
                and hasattr(self.window.core, "llm")
                and hasattr(self.window.core.llm, "complete")
            ):
                summary = self.window.core.llm.complete(prompt)
            else:
                summary = "LLM summarization unavailable."

            return {"output": output, "success": success, "summary": summary}
        except Exception as e:
            return {"output": f"Exception: {str(e)}", "success": False, "summary": ""}

    def setup_dialogs(self, dialog_manager):
        dialog_manager.register_dialog("kali_exec", lambda: KaliControlDialog(self))

    def setup_menu(self):
        menubar = self.window.menuBar()
        tools_menu = None
        for action in menubar.actions():
            if action.text().lower().startswith("tools"):
                tools_menu = action.menu()
                break
        if tools_menu is None:
            tools_menu = menubar.addMenu("Tools")
        action = QAction("Kali Control", self.window)
        action.triggered.connect(self.show_dialog)
        tools_menu.addAction(action)

    def show_dialog(self):
        dialog = KaliControlDialog(self)
        dialog.exec_()