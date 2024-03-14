#!/usr/bin/env python3

def read_value(bit_pair):
    return int.from_bytes(bit_pair, "little")

import socket
def readHV(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.01)
    s.connect((ip, int(port)))
    # Command is 0x30 (read HV) 0x03 (3 words being sent) 0x33 (CRC)
    buf_string = b''
    buf_string += int.to_bytes(0x30, 2, "little")
    buf_string += int.to_bytes(0x03, 2, "little")
    buf_string += int.to_bytes(0x03 ^ 0x30, 2, "little")
    # b'\x30\x00\x03\x00\x33\x00'
    # print(buf_string)
    s.send(buf_string)
    data = s.recv(1024)
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    cmd = read_value(data[0:2])
    length = read_value(data[2:4])
    if cmd == 0x30 and length == 0x4:
        # expected from HV reading, otherwise the user will decode the output...
        hv = read_value(data[4:6])
        crc = read_value(data[6:8])
        if crc == cmd ^ length ^ hv:
            data = hv
        else:
            print(f"CRC failed on {data}")
            print(cmd ^ length ^ hv, crc)
            raise
    else:
        print(cmd)
        print(length)
    return data

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_list", nargs="+")
    parser.add_argument("--output_file", default=None)
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("--cmd_port", type=int, default=7)
    args = parser.parse_args()

    for ip in args.ip_list:
        try:
            data = readHV(ip, args.cmd_port)
        except:
            print(f"Failed to read info from {ip}")
            continue

        if not args.quiet:
            print(f"{ip}\t{data}")
        if args.output_file is not None:
            import time
            date = time.time()
            try:
                data = int(data)
            except:
                continue
            fname = args.output_file.replace('{ip}', ip)
            with open(fname, 'a') as fout:
                fout.write(f"{date}\t{data}\n")

