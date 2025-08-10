# Network Diagnostics

## Overview

The Network Diagnostics tool provides a graphical and programmatic interface to common network troubleshooting utilities: **ping**, **traceroute**, **port scan** (via nmap), and **DNS lookup** (via dig).  
This tool enables users to quickly test network connectivity, trace network paths, scan host ports, and resolve DNS records—all within the PyGPT interface.

**Prerequisites:**  
You must have the following tools installed and available in your system's PATH:
- `ping`
- `traceroute`
- `nmap`
- `dig` (usually provided by the `dnsutils` package)

## Usage

### In the GUI

1. Open PyGPT.
2. Go to the **Tools** menu and select **Network Diagnostics**.
3. In the dialog:
   - Choose the desired command (ping, traceroute, port_scan, dns_lookup).
   - Enter the required fields (e.g., host or domain).
   - Click **Run**.
   - Output will be shown in the results area, color-coded for success or failure.

![Network Diagnostics Dialog Screenshot](network_diagnostics_screenshot.png)  
*Replace with an actual screenshot after running the tool.*

### Using the Tool API

You can invoke the tool programmatically by passing a JSON-like dictionary to the `run` method.

**Examples:**

#### Ping

```python
args = {"command": "ping", "host": "8.8.8.8", "count": 3}
result = tool.run(args)
```

#### Traceroute

```python
args = {"command": "traceroute", "host": "example.com"}
result = tool.run(args)
```

#### Port Scan

```python
args = {"command": "port_scan", "host": "scanme.nmap.org", "ports": "22,80,443"}
result = tool.run(args)
```

#### DNS Lookup

```python
args = {"command": "dns_lookup", "domain": "example.com", "record_type": "A"}
result = tool.run(args)
```

## Dependencies

Make sure the following system tools are installed:

- `nmap` (for port scanning)
- `traceroute` (for network path tracing)
- `dnsutils` (for dig/DNS lookup)
- `ping` (usually available by default)

On Ubuntu/Debian:

```bash
sudo apt-get install nmap traceroute dnsutils iputils-ping
```

On macOS (with Homebrew):

```bash
brew install nmap
brew install traceroute
brew install bind  # for dig
# ping is included by default
```

On Windows:

- `ping` is built-in.
- `nmap` can be downloaded from https://nmap.org/download.html
- `traceroute` is called `tracert`.
- For `dig`, use BIND tools or online alternatives.