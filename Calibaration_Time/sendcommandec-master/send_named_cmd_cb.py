#!/usr/bin/env python3

# This script does basically the same thing as send_any_cb.py, but provices a nicer user interface

command_names = {
    "reset_S6": ["tcp", "CB", 0x1038, 0],
    "reset_US": ["udp", "CB", 0x00D8, 0],
    "rst_pulse": ["udp", "CB", 0x00E3, 0],
    "read_counter": ["udp", "CB", 0x00EE, 0],
    "send_udp": ["udp", "CB", 0x1018, 1],
    "recv_tcp": ["tcp", "CB", 0x1021, 0],
    "send_tcp": ["tcp", "CB", 0x1020, 1],
    "recv_udp": ["udp", "CB", 0x1019, 0],
    "set_L1_mode": ["udp", "CB", 0x00F3, 2],
    "get_L1_mode": ["udp", "CB", 0x1043, 0],
    "iodelay_rob": ["udp", "CB", 0x00B2, 1],
    "launch_acq": ["udp", "ROBs", 0x0005, 1],
    "stop_acq": ["udp", "ROBs", 0x0006, 0],
    "rob_version": ["udp", "ROB", 0x0080, 0],
    "rob_dummy": ["udp", "ROB", 0x00B0, 0],
    "set_acq_mode": ["udp", "ROB", 0x0003, 1],
    "read_acq_mode": ["udp", "ROB", 0x0004, 0],
    "hv_set": ["udp", "ROB", 0x0010, 1],
    "hv_read": ["udp", "ROB", 0x0011, 0],
    "hv_mon": ["udp", "ROB", 0x0030, 0],
    "hv_update": ["udp", "ROB", 0x0060, 0],
    "hv_off": ["udp", "ROB", 0x0070, 0],
    "led_bias_set": ["udp", "ROB", 0x0050, 1],
    "led_bias_read": ["udp", "ROB", 0x0051, 0],
    "hold_dly_set": ["udp", "ROB", 0x00C2, 1],
    "hold_dly_read": ["udp", "ROB", 0x00C3, 0],
}


ip_dict = {
    "telescope": {
        "tcp": "10.3.171.119",
        "udp": "10.3.171.19",
    },
}

for CB_label in range(20, 101):
    ip_dict["CB" + str(CB_label)] = {
        "tcp": "10.3.171." + str(100 + CB_label),
        "udp": "10.3.171." + str(CB_label),
    }

require_robid = ["iodelay_rob"]

require_nevents = ["launch_acq"]

require_value = ["hv_set", "led_bias_set", "hold_dly_set"]

require_run_type = ["set_acq_mode"]
run_types = {
    "TRT": 0x0,
    "PED": 0x1,
    "PED-W": 0x1,
    "PED-F": 0x2,
    "LED": 0x3,
    "LED-W": 0x3,
    "LED-F": 0x4,
    "Normal": 0x5,
    "Normal-W": 0x5,
    "Normal-F": 0x6,
    "Normal-W0": 0x7,
    "Normal-F0": 0x8,
    "HitReg": 0x9,
}
run_type_opt = ["TRT", "PED", "LED", "Normal", "HitReg"]
run_charge_opt = ["Wilkinson", "FlashADC"]


def print_output(output):
    global args
    if not args.quiet:
        print(output, end="")


def post_processing(cmd, data):
    if cmd == "iodelay_rob":
        comm_success = False
        for entry in data:
            if entry != 0xFFFF:
                comm_success = True
                break
        return "comm OK" if comm_success else "comm Failed"
    elif len(data) == 0:
        return "OK"
    output = ""
    for entry in data:
        output += f"{entry} [0x{entry:04x}]"
        if cmd in ["read_acq_mode"]:
            this_run_type = ""
            for k, v in run_types.items():
                if v == entry:
                    if len(this_run_type) < len(k):
                        # Replaces if empty of shorter version (like LED vs LED-W)
                        this_run_type = k
            run_type_split = this_run_type.split("-")
            output += " : " + run_type_split[0]
            if len(run_type_split) > 1:
                if "W" in run_type_split[1]:
                    output += " Wilkinson"
                elif "F" in run_type_split[1]:
                    output += " Flash ADC"
                else:
                    output += " " + run_type_split[1]
                if "0" in run_type_split[1]:
                    output += " with 0-suppress"
        output += "\t"
    return output[:-1]


if __name__ == "__main__":
    from send_any_cb import *

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ip")
    # parser.add_argument("--run_sequential", action='store_true')
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--debug", action="store_true")
    subparsers = parser.add_subparsers(help="sub-command help")

    for cmd in command_names.keys():
        parse_cmd = subparsers.add_parser(cmd)
        parse_cmd.set_defaults(command=cmd)
        destination = command_names[cmd][1]
        if destination in "ROB":
            parse_cmd.add_argument(
                "--dst_robs", type=auto_int, required=True, nargs="+"
            )
        payload_size = command_names[cmd][3]
        if cmd in require_robid:
            # Separate this argument so I can create new payloads with different ROBs
            parse_cmd.add_argument("--robs", type=auto_int, required=True, nargs="+")
            payload_size -= 1
        if cmd in require_nevents:
            parse_cmd.add_argument("--nevents", type=auto_int, required=True)
            payload_size -= 1
        if cmd in require_value:
            parse_cmd.add_argument("--value", type=auto_int, required=True)
            payload_size -= 1
        if cmd in require_run_type:
            parse_cmd.add_argument(
                "--run_type_opt", choices=run_type_opt, required=True
            )
            parse_cmd.add_argument(
                "--run_charge_opt", choices=run_charge_opt, default=run_charge_opt[0]
            )
            parse_cmd.add_argument("--zero_suppress", action="store_true")
            payload_size -= 1
        if payload_size > 0:
            parse_cmd.add_argument(
                "--payload", type=auto_int, required=True, nargs=payload_size
            )
    args = parser.parse_args()

    try:
        cmd_str = args.command
    except:
        parser.error("Please provide a command")

    socket_type, dst_str, cmd, payload_size = command_names[cmd_str]

    try:
        # Convertion to int with int(x, 0) allows numbers to be provided in
        # different bases
        temp = int(args.ip, 0)
        args.ip = temp
    except:
        pass

    if args.ip.__class__ == int:
        if args.ip <= 100 and args.ip >= 18:
            if socket_type == "tcp":
                args.ip += 100
            args.ip = f"10.3.171.{args.ip}"
        else:
            args.ip = str(args.ip)
    if args.ip.__class__ == str:
        if args.ip in ip_dict.keys():
            args.ip = ip_dict[args.ip][socket_type]
        else:
            try:
                import ipaddress

                ipaddress.ip_address(args.ip)
            except:
                parser.error(
                    f"IP should be a number between 18 and 100, a keyword ({str(list(ip_dict.keys()))[1:-1]}), or an IP."
                )

    if cmd_str in require_robid:
        payload_size -= 1

    payload = []

    if args.command in require_nevents:
        payload.append(args.nevents)
        payload_size -= 1
    if args.command in require_value:
        payload.append(args.value)
        payload_size -= 1
    if args.command in require_run_type:
        run_type = run_types[args.run_type_opt]
        if (
            args.run_type_opt not in ["TRT", "HitReg"]
            and args.run_charge_opt == "FlashADC"
        ):
            run_type += 1
        if args.run_type_opt == "Normal" and args.zero_suppress:
            run_type += 2
        payload.append(run_type)
        payload_size -= 1

    if payload_size > 0:
        payload += args.payload

    def run_one(ip, socket_type, dst, cmd, payload):
        if socket_type == "tcp":
            data = send_command_cb_tcp(ip, dst, cmd, payload, verbose=args.debug)
        elif socket_type == "udp":
            data = send_command_cb_udp(ip, dst, cmd, payload, verbose=args.debug)

        return post_processing(cmd_str, data)

    if dst_str == "CB":
        if cmd_str in require_robid:
            for ROBid in args.robs:
                output = ""
                try:
                    this_payload = [ROBid] + payload
                    output += f"ROB {ROBid:2d}  =>  "
                    run_out = run_one(args.ip, socket_type, 0x80, cmd, this_payload)
                    output += run_out + "\n"
                except ValueError:
                    output += "Bad reply\n"
                except TimeoutError:
                    output += "Command timed out\n"
                print_output(output)
        else:
            try:
                run_out = run_one(args.ip, socket_type, 0x80, cmd, payload)
                print_output(run_out + "\n")
            except (TimeoutError, socket.timeout):
                print(f"Command sent to {args.ip} timed out.")
    elif dst_str == "ROBs":
        try:
            run_out = run_one(args.ip, socket_type, 0xFF, cmd, payload)
            print_output(run_out + "\n")
        except (TimeoutError, socket.timeout):
            print(f"Command sent to {args.ip} timed out.")
    elif dst_str == "ROB":
        for ROBid in args.dst_robs:
            output = ""
            try:
                output += f"ROB {ROBid:2d}  =>  "
                run_out = run_one(args.ip, socket_type, ROBid, cmd, payload)
                output += run_out + "\n"
            except ValueError:
                output += "Bad reply\n"
            except (TimeoutError, socket.timeout):
                output += "Command timed out\n"
            print_output(output)
    else:
        raise ValueError(f"Destination {dst_str:x} not supported")
