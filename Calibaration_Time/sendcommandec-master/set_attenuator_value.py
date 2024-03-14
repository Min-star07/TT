#!/usr/bin/env python3

import pyvisa

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("attenuation", type=int, help="in dB")
parser.add_argument("--ch", type=int, default=1)
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

res_man = pyvisa.ResourceManager()
attenuator = res_man.open_resource("TCPIP0::192.168.7.116::inst0::INSTR")
attenuator.write("*IDN?")
IDN = attenuator.read().strip()
if args.debug:
    print(IDN)

if IDN != "Agilent Technologies,L4490A,MY61410001,2.49-2.43-0.00-0.00":
    print(f"IDN changed from reference! IDN='{IDN}'")

fine_step = args.attenuation % 10
coarse_step = int(args.attenuation / 10) * 10

fine_query = f"ROUT:SEQ:TRIG ATTEN_{args.ch}_1_{fine_step}"
coarse_query = f"ROUT:SEQ:TRIG ATTEN_{args.ch}_2_{coarse_step}"
print(fine_query)
print(coarse_query)
for query in [fine_query, coarse_query]:
    if args.debug:
        print(f"Query: {query}")
    att_set = attenuator.write(query)
    if args.debug:
        print(att_set)

import numpy as np

### Check set number
clos_sec_list = {
    1: "1101,1102,1103,1104,1105,1106,1107,1108",
    2: "1121,1122,1123,1124,1125,1126,1127,1128",
    3: "1141,1142,1143,1144,1145,1146,1147,1148",
    4: "1161,1162,1163,1164,1165,1166,1167,1168",
    5: "2125,2121,2122,2120,2116,2112,2113,2111",
}
attn_wgt = np.array([1, 2, 4, 4, 10, 20, 40, 40])

while True:
    attenuator.write(f"ROUT:CLOS? (@{clos_sec_list[args.ch]})")
    read_attn = attenuator.read().strip()
    attn_read = np.sum(np.array([1 - int(x) for x in read_attn.split(",")]) * attn_wgt)
    if args.debug:
        print(f"Attenuator set to {attn_read} dB")
    if attn_read == args.attenuation:
        break
