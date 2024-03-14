#!/usr/bin/env python3

import pyvisa

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("delta_t", type=float)
parser.add_argument("--delta_t_offset", type=float, default=-7.3)
args = parser.parse_args()
print(args)

# Offset between charge injections
args.delta_t += args.delta_t_offset

pulse_delay_1 = 0
pulse_delay_2 = 0
if args.delta_t > 0:
    pulse_delay_1 = args.delta_t
else:
    pulse_delay_2 = -args.delta_t
print(f"pulse gen 1 delay = {pulse_delay_1}")
print(f"pulse gen 2 delay = {pulse_delay_2}")

res_man = pyvisa.ResourceManager()
pulse_gen = res_man.open_resource("TCPIP0::192.168.7.73::inst0::INSTR")
pulse_gen.write("*IDN?")
print(pulse_gen.read())
print(pulse_gen.write(f":PULS:DEL1 {pulse_delay_1:.2f}ns"))
print(pulse_gen.write(f":PULS:DEL2 {pulse_delay_2:.2f}ns"))
