#!/usr/bin/env python3

import argparse
import random
import re
import subprocess
import sys
import time


def get_current_mac(interface):
    try:
        output = subprocess.check_output(
            ["ip", "link", "show", interface],
            text=True,
            stderr=subprocess.STDOUT
        )

        match = re.search(
            r"link/ether\s+([0-9a-f:]{17})",
            output,
            re.IGNORECASE
        )

        return match.group(1).lower() if match else None

    except subprocess.CalledProcessError:
        return None


def generate_random_mac():
    first_byte = (random.randint(0, 255) & 0xFC) | 0x02
    mac = [first_byte] + [random.randint(0, 255) for _ in range(5)]
    return ":".join(f"{b:02x}" for b in mac)


def validate_mac(mac):
    return bool(
        re.match(
            r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$",
            mac
        )
    )


def list_interfaces():
    output = subprocess.check_output(
        ["ip", "-o", "link", "show"],
        text=True
    )

    for line in output.splitlines():
        match = re.match(r"^\d+:\s+([^:]+):", line)

        if match:
            iface = match.group(1)

            if iface != "lo":
                print(iface)


def change_mac(interface, mac):
    subprocess.run(
        ["ip", "link", "set", interface, "down"],
        check=True
    )

    subprocess.run(
        ["ip", "link", "set", interface, "address", mac],
        check=True
    )

    subprocess.run(
        ["ip", "link", "set", interface, "up"],
        check=True
    )


def main():
    parser = argparse.ArgumentParser(
        description="Linux MAC Address Changer"
    )

    parser.add_argument("-i", "--interface")
    parser.add_argument("-m", "--mac")
    parser.add_argument("-r", "--random", action="store_true")
    parser.add_argument("-l", "--list", action="store_true")

    args = parser.parse_args()

    if args.list:
        list_interfaces()
        return

    if not args.interface:
        parser.print_help()
        return

    current = get_current_mac(args.interface)

    if current is None:
        print(f"Interface not found: {args.interface}")
        sys.exit(1)

    print(f"Current MAC: {current}")

    if args.random:
        new_mac = generate_random_mac()

    elif args.mac:
        if not validate_mac(args.mac):
            print("Invalid MAC format")
            sys.exit(1)

        new_mac = args.mac.lower()

    else:
        print("Specify --random or --mac")
        sys.exit(1)

    print(f"Changing MAC to: {new_mac}")

    change_mac(args.interface, new_mac)

    time.sleep(1)

    verify = get_current_mac(args.interface)

    print(f"Current MAC after change: {verify}")


if __name__ == "__main__":
    main()
