# Linux MAC Changer

A lightweight Python command-line utility for Linux that allows you to:

- List available network interfaces
- View the current MAC address
- Generate a random locally administered MAC address
- Set a custom MAC address
- Verify the applied MAC address

## Features

- Linux support
- Random MAC generation
- Custom MAC assignment
- Interface enumeration
- Verification after change
- No external Python dependencies

## Requirements

- Linux
- Python 3.8+
- iproute2 (`ip` command)
- Root privileges

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/linux-mac-changer.git
cd linux-mac-changer
```

Make executable:

```bash
chmod +x macspoofer.py
```

## Usage

### List Interfaces

```bash
python3 macspoofer.py -l
```

Example:

```text
enp2s0
wlo1
```

### Generate Random MAC

```bash
sudo python3 macspoofer.py -i wlo1 -r
```

Example output:

```text
Current MAC: 4c:23:38:75:a5:57
Changing MAC to: 02:5d:ab:19:cc:77
Current MAC after change: 02:5d:ab:19:cc:77
```

### Set Custom MAC

```bash
sudo python3 macspoofer.py -i wlo1 -m 02:11:22:33:44:55
```

### Verify MAC

```bash
cat /sys/class/net/wlo1/address
```

or

```bash
ip link show wlo1
```

## Restore Original MAC

If your original MAC was:

```text
4c:23:38:75:a5:57
```

Restore it using:

```bash
sudo python3 macspoofer.py -i wlo1 -m 4c:23:38:75:a5:57
```

## How It Works

The tool:

1. Brings the interface down
2. Applies a new MAC address
3. Brings the interface back up
4. Verifies the change

Commands used internally:

```bash
ip link set <interface> down
ip link set <interface> address <new_mac>
ip link set <interface> up
```

## Notes

- Some network managers may restore the original MAC.
- Some drivers do not support MAC changes.
- Administrative privileges are required.

## Disclaimer

Use only on networks and devices you are authorized to manage. Follow all applicable policies and laws.
