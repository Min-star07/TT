#!/usr/bin/env python3

# This is a command with a long payload, so I have most of it fixed, and will add 'changeable bits'
# as needed.

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ip_list", nargs="+")
parser.add_argument("--quiet", action='store_true')
parser.add_argument("--cmd_port", type=int, default=7)
parser.add_argument("--hold_delay", type=int, default=4)

args = parser.parse_args()

if args.hold_delay < 0 or args.hold_delay > 0xFF:
    parser.error("hold delay must be between 0 and 0xFF")

command=0x2

payload = [ ]

payload.append(args.hold_delay<<8 | 0x08)
payload.append(0x9C40)
payload.append(0x0)
payload.append(0x40)
payload.append(0x0)
payload.append(0x0)

from send_any_rob import *

for this_ip in args.ip_list:
    try:
        data = send_command(this_ip, args.cmd_port, command, payload)
    except:
        print(f"Failed to get reply from {this_ip}")
        continue

    output = ""
    if not args.quiet:
        output += f"{this_ip}"
        if len(data) == 0:
            output += "\tOK"
        else:
            for entry in data:
                output += f"\t{entry}"

    output += f"    hold delay {args.hold_delay}"
    print(output)


