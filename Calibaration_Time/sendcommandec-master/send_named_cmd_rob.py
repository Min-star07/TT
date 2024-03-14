#!/usr/bin/env python3

# This script does basically the same thing as send_any_rob.py, but provices a nicer user interface

command_names = {
        "set_run_type"    : 0x03,
        "get_run_type"    : 0x04,
        "start_run"       : 0x05,
        "stop_run"        : 0x06,
        "set_HV"          : 0x10,
        "read_HV"         : 0x11,
        "update_HV"       : 0x60,
        "HV_off"          : 0x70,
        "hv_mon"          : 0x30,
        "set_LED_biais"   : 0x50,
        "read_LED_biais"  : 0x51,
        "version"         : 0x80,
        "dummy"           : 0xB0,
        "reconnect"       : 0xE1,
        }

require_nevents = [ "start_run" ]

require_value   = [ "set_HV", "set_LED_biais" , "set_hold_delay"]

require_run_type = [ "set_run_type" ]
run_types = {
        "TRT"  : 0x0,
        "PED"  : 0x1,
        "LED"  : 0x3,
        "Norm" : 0x5,
        }

if __name__ == '__main__':
    from send_any_rob import *

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ip_list", nargs="+")
    parser.add_argument("--run_sequential", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("--cmd_port", type=int, default=7)
    subparsers = parser.add_subparsers(help='sub-command help')

    for cmd in command_names.keys():
        parse_cmd = subparsers.add_parser(cmd)
        parse_cmd.set_defaults(command=cmd)
        if cmd in require_nevents:
            parse_cmd.add_argument("--nevents", type=int, required=True)
        elif cmd in require_value:
            parse_cmd.add_argument("--value", type=int, required=True)
        elif cmd in require_run_type:
            parse_cmd.add_argument("--run_type", choices=run_types.keys(), required=True)
    args = parser.parse_args()
    print(args)

    payload = []

    if args.command in require_nevents:
        payload.append(args.nevents)
    elif args.command in require_value:
        payload.append(args.value)
    elif args.command in require_run_type:
        payload.append(run_types[args.run_type])

    def run_one(this_ip):
        global args, command_names, payload

        output = ""

        try:
            data = send_command(this_ip, args.cmd_port, command_names[args.command], payload)
        except:
            output = f"Failed to get reply from {this_ip}"
            return output

        if not args.quiet:
            output += f"{this_ip}"
            if len(data) == 0:
                output += "\tOK"
            else:
                for entry in data:
                    output += f"\t{entry}"

        return output

    # JP: From some quick tests, running this script without joblib is faster in general
    #     I have nevertheless prefered to use it in case there is a hang in a process it
    #     won't affect the others -- for example if one card is taking longer to start data
    #     taking that will not delay the others (and sync will be kept to a better level).
    #     The difference in time I saw was, running for 8 cards:
    #        - 0.15s in sequential mode
    #        - 0.69s in parallel   mode
    if not args.run_sequential:
        try:
            from joblib import Parallel, delayed
        except:
            args.run_sequential = True
    if args.run_sequential:
        for ip in args.ip_list:
            output = run_one(ip)
            if output != "":
                print(output)
    else:
        outputs = Parallel(n_jobs=len(args.ip_list))(delayed(run_one)(ip) for ip in args.ip_list)
        for output in outputs:
            if output != "":
                print(output)
