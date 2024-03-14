#!/usr/bin/env python3

from byte_hex_compat import pretty_hex
from message_wrapper import auto_int, message_wrapper, message_reader

import socket
def send_command_cb(ip, destination, command, payload=[], verbose=False, socket_type=None, port=None, port_local = None):
    mesg = message_wrapper(dst=destination, cmd=command, args=payload)
    buf_string = mesg.get_message()
    if verbose:
        print(f"Send buffer:     {pretty_hex(buf_string)}")
    with socket.socket(socket.AF_INET, socket_type) as s:
        if port_local is not None:
            s.bind(('', port_local))
        s.settimeout(60)
        s.connect((ip, int(port)))
        s.send(buf_string)

        max_size = 1024
        data = s.recv(max_size)
        reply_length = message_reader.get_buflength_preliminary(data)
        while len(data) <= reply_length:
            data += s.recv(max_size)

    if verbose:
        print(f"Response buffer: {pretty_hex(data)}")

    reply = message_reader(msg = data)
    reply.decode()

    if reply.command != command:
        raise ValueError(f"Received 0x{reply.command:x} command to a request with 0x{command:x}")

    if reply.length*2 > max_size:
        raise RuntimeError("Response length {reply.length*2} is larger than {max_size}. Please change max size and rerun")

    return reply.payload

def send_command_cb_tcp(*args, **kwargs):
    return send_command_cb(socket_type = socket.SOCK_STREAM, port = 7, *args, **kwargs)

def send_command_cb_udp(*args, **kwargs):
    return send_command_cb(socket_type = socket.SOCK_DGRAM, port = 60002, *args, **kwargs)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_list", nargs="+")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tcp", action='store_true')
    group.add_argument("--udp", action='store_true')
    parser.add_argument("--output_file", default=None)
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("--print_hex_reply", action='store_true')
    parser.add_argument("--print_dec_reply", action='store_true')
    parser.add_argument("--destination", required=True, type=auto_int )
    parser.add_argument("--command", required=True, type=auto_int )
    parser.add_argument("--payload", nargs="+", type=auto_int, default=[])
    args = parser.parse_args()

    for ip in args.ip_list:
        try:
            if args.tcp:
                data = send_command_cb_tcp(ip, args.destination, args.command, args.payload, args.verbose)
            else:
                data = send_command_cb_udp(ip, args.destination, args.command, args.payload, args.verbose)
        except TimeoutError:
            print(f"Failed to get reply from {ip}")
            continue

        if not args.quiet:
            print(f"{ip}", end='')
            for entry in data:
                if args.print_hex_reply:
                    print(f"\t0x{entry:x}", end='')
                elif args.print_dec_reply:
                    print(f"\t{entry}", end='')
                else:
                    print(f"\t{entry} [0x{entry:x}]", end='')
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

