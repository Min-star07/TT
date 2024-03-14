#!/usr/bin/env python3

from message_wrapper import auto_int, message_wrapper, message_reader

import socket
def send_command(ip, port, command, payload=[]):
    mesg = message_wrapper(cmd=command, args=payload)
    buf_string = mesg.get_message()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect((ip, int(port)))
    s.send(buf_string)

    max_size = 1024
    data = s.recv(max_size)
    s.close()

    reply = message_reader(msg = data)
    reply.decode()

    if reply.command != command:
        raise ValueError(f"Received 0x{reply.command:x} command to a request with 0x{command:x}")

    if reply.length*2 > max_size:
        raise RuntimeError("Response length {reply.length*2} is larger than {max_size}. Please change max size and rerun")

    return reply.payload

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_list", nargs="+")
    parser.add_argument("--output_file", default=None)
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("--cmd_port", type=int, default=7)
    parser.add_argument("--command", required=True, type=auto_int )
    parser.add_argument("--payload", nargs="+", type=auto_int, default=[])
    args = parser.parse_args()

    for ip in args.ip_list:
        try:
            data = send_command(ip, args.cmd_port, args.command, args.payload)
        except:
            print(f"Failed to get reply from {ip}")
            continue

        if not args.quiet:
            print(f"{ip}", end='')
            for entry in data:
                print(f"\t{entry}", end='')
            print("")
        if args.output_file is not None:
            import time
            date = time.time()
            fname = args.output_file.replace('{ip}', ip)
            with open(fname, 'a') as fout:
                fout.write(f"{date}")
                for entry in data:
                    fout.write(f"\t{entry}")
                fout.write("\n")

