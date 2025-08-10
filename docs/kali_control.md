# Kali Control

## Overview
The Kali Control tool allows executing arbitrary shell commands on the host (typically Kali Linux) from within PyGPT, with user confirmation and LLM-driven summarization of results.

**Warning:** This grants full shell access. Use responsibly.

## Usage

1. In the PyGPT GUI, open the **Tools → Kali Control** menu.
2. Enter any shell command in the input field.
3. Confirm execution when prompted.
4. View raw output and LLM summary in the dialog.

## Programmatic API

```python
args = {"cmd": "ifconfig"}
result = tool.run(args)
print(result['output'])
print(result['summary'])
```

## Dependencies

- `bash` shell
- Ensure your system PATH includes the commands you plan to run.

```bash
sudo apt-get install bash
```