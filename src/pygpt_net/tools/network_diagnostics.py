#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Genie (CosineAI)                     #
# Updated Date: 2025.08.10                           #
# ================================================== #

import subprocess
from typing import Dict

from pygpt_net.tools.base import BaseTool

class NetworkDiagnosticsTool(BaseTool):
    def name(self) -> str:
        return "network_diagnostics"

    def description(self) -> str:
        return "Run ping, traceroute, port scan, and DNS lookup commands"

    def run(self, args: Dict) -> Dict:
        """
        Run a network diagnostic command.

        Args:
            args (dict): Must contain "command" and required params.

        Returns:
            dict: {"output": <stdout+stderr>, "success": True/False}
        """
        command = args.get("command")
        output = ""
        success = False

        try:
            if command == "ping":
                host = args.get("host")
                count = str(args.get("count", 4))
                if not host:
                    return {"output": "Missing required parameter: host", "success": False}
                cmd = ["ping", "-c", str(count), host]
            elif command == "traceroute":
                host = args.get("host")
                if not host:
                    return {"output": "Missing required parameter: host", "success": False}
                cmd = ["traceroute", host]
            elif command == "port_scan":
                host = args.get("host")
                ports = args.get("ports", "1-1024")
                if not host:
                    return {"output": "Missing required parameter: host", "success": False}
                cmd = ["nmap", "-p", str(ports), host]
            elif command == "dns_lookup":
                domain = args.get("domain")
                record_type = args.get("record_type", "A")
                if not domain:
                    return {"output": "Missing required parameter: domain", "success": False}
                cmd = ["dig", "+short", record_type, domain]
            else:
                return {"output": f"Unknown command: {command}", "success": False}

            # Run the command
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
            success = proc.returncode == 0
            if not success:
                output = f"Error running command:\n{output}"
        except FileNotFoundError as e:
            output = f"Command not found: {e}"
            success = False
        except Exception as e:
            output = f"Exception: {str(e)}"
            success = False

        return {"output": output.strip(), "success": success}