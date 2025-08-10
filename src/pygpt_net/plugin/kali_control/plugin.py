#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# KaliControlPlugin: Minimal plugin skeleton         #
# MIT License                                        #
# ================================================== #

from pygpt_net.plugin.base import BasePlugin
from PySide6.QtWidgets import QAction

class Plugin(BasePlugin):
    def setup(self):
        # Attach KaliExecTool to window's tools if not already present
        if hasattr(self.window, "tools") and "kali_exec" not in self.window.tools:
            from pygpt_net.tools.kali_exec import KaliExecTool
            self.window.tools["kali_exec"] = KaliExecTool(self.window)
        # Add menu action under Tools -> Kali Control
        menubar = self.window.menuBar()
        tools_menu = None
        for action in menubar.actions():
            if action.text().lower().startswith("tools"):
                tools_menu = action.menu()
                break
        if tools_menu is None:
            tools_menu = menubar.addMenu("Tools")
        action = QAction("Kali Control", self.window)
        action.triggered.connect(self.open_kali_dialog)
        tools_menu.addAction(action)

    def open_kali_dialog(self):
        # Placeholder: dialog to be implemented later
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self.window, "Kali Control", "KaliControlDialog coming soon.")