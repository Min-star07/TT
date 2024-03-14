#!/usr/bin/env python3

# The slow control package that needs to be sent to the Readout boards is quite complex, so I prefer having this in a separate command to properly create the payload.

ip_dict = dict()

for CB_label in range(20,101):
    ip_dict["CB"+str(CB_label)] = {
            'tcp': '10.3.171.' + str(100+CB_label),
            'udp': '10.3.171.' + str(CB_label),
            }


def print_output(output):
    global args
    if not args.quiet:
        print(output, end = '')

def post_processing(data):
    if len(data) == 0:
        return "OK"
    output = ""
    for entry in data:
        output += f"{entry} [0x{entry:04x}]"
        output += "\t"
    return output[:-1]

class bit_array:
    # Array needs to be made of 16-bit integer chuncks
    def __init__(self):
        self.array  = [0]
        self.bitpos = 16
        self.debug  = True

    def append_to_array(self):
        if self.debug:
            print(format(self.array[-1],"#018b"), "%04x" % self.array[-1])
            # print(format(0xF0F0,"#018b"))
        self.array.append(0)
        self.bitpos = 16

    def print_last(self):
        if self.debug and self.bitpos != 16:
            print(format(self.array[-1],"#018b"))

    def add_element(self, value, nbits=1):
        mask = ((1 << (nbits)) - 1)
        if value != (value & mask):
            print(f"Size of {value:x} seems wrong. Truncating to {nbits} bits.")
            value = value & mask
        if self.bitpos >= nbits:
            self.array[-1] = self.array[-1] | (value << (self.bitpos-nbits) )
            self.bitpos -= nbits
            if self.bitpos == 0:
                self.append_to_array()
        else:
            self.array[-1] = self.array[-1] | (value >> (nbits-self.bitpos) )
            remaining = value & (mask >> self.bitpos)
            remaining_bits = nbits-self.bitpos
            self.append_to_array()
            self.add_element(remaining, remaining_bits)


def create_payload_sc(sc):
    array = bit_array()
    array.add_element(sc.ON_OFF_otabg     )
    array.add_element(sc.ON_OFF_dac       )
    array.add_element(sc.small_dac        )
    array.add_element(sc.DAC1             , 10)
    array.add_element(sc.DAC0             , 10)
    array.add_element(sc.enb_outADC       )
    array.add_element(sc.inv_startCmptGray)
    array.add_element(sc.ramp_8bit        )
    array.add_element(sc.ramp_10bit       )
    for i in range(64):
        this_bit = 63-i
        array.add_element(( sc.mask_OR2 & (1<<this_bit) ) >> this_bit)
        array.add_element(( sc.mask_OR1 & (1<<this_bit) ) >> this_bit)
    array.add_element(sc.cmd_CK_mux       )
    array.add_element(sc.d1_d2            )
    array.add_element(sc.inv_discriADC    )
    array.add_element(sc.polar_discri     )
    array.add_element(sc.Enb_tristate     )
    array.add_element(sc.valid_dc_fsb2    )
    array.add_element(sc.sw_fsb2_50f      )
    array.add_element(sc.sw_fsb2_100f     )
    array.add_element(sc.sw_fsb2_100k     )
    array.add_element(sc.sw_fsb2_50k      )
    array.add_element(sc.valid_dc_fs      )
    array.add_element(sc.cmd_fsb_fsu      )
    array.add_element(sc.sw_fsb1_50f      )
    array.add_element(sc.sw_fsb1_100f     )
    array.add_element(sc.sw_fsb1_100k     )
    array.add_element(sc.sw_fsb1_50k      )
    array.add_element(sc.sw_fsu_100k      )
    array.add_element(sc.sw_fsu_50k       )
    array.add_element(sc.sw_fsu_25k       )
    array.add_element(sc.sw_fsu_40f       )
    array.add_element(sc.sw_fsu_20f       )
    array.add_element(sc.H1H2_choice      )
    array.add_element(sc.EN_ADC           )
    array.add_element(sc.sw_ss_1200f      )
    array.add_element(sc.sw_ss_600f       )
    array.add_element(sc.sw_ss_300f       )
    array.add_element(sc.ON_OFF_ss        )
    array.add_element(sc.swb_buf_2p       )
    array.add_element(sc.swb_buf_1p       )
    array.add_element(sc.swb_buf_500f     )
    array.add_element(sc.swb_buf_250f     )
    array.add_element(sc.cmd_fsb          )
    array.add_element(sc.cmd_ss           )
    array.add_element(sc.cmd_fsu          )
    for i in range(64):
        this_bit = 63-i
        array.add_element(( sc.cmd_SUM & (1<<this_bit) ) >> this_bit)
        array.add_element(sc.GAINS[this_bit]  ,  8)
    array.add_element(sc.Ctest            , 64)
    array.print_last()
    return array.array


if __name__ == '__main__':
    print("WARNING: this code has not been fully tested! Use at your own risk!")
    from send_any_cb import *
    from message_wrapper import auto_bool

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ip", choices=ip_dict.keys())
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("--debug", action='store_true')
    parser.add_argument("--socket_type", default="udp")

    parser.add_argument("--dst_robs", type=auto_int, required=True, nargs='+')

    parser.add_argument("--DAC1"             , dest="DAC1"             , type=auto_int, default=300) # 10 bits
    parser.add_argument("--DAC0"             , dest="DAC0"             , type=auto_int, default=500) # 10 bits
    parser.add_argument("--mask_OR2"         , dest="mask_OR2"         , type=auto_int, default=0) # 64 bits
    parser.add_argument("--mask_OR1"         , dest="mask_OR1"         , type=auto_int, default=0) # 64 bits
    parser.add_argument("--GAINS"            , dest="GAINS"            , type=auto_int, default=[64]*64, nargs="+") # 64*8 bits

    parser.add_argument("--set_gain_ch"      , dest="set_gain_ch"      , action="append", nargs=2)
    parser.add_argument("--ch_mask"          , dest="ch_mask"          , type=auto_int, nargs="*")

    parser.add_argument("--ON_OFF_otabg"     , dest="ON_OFF_otabg"     , type=auto_bool, default=True)
    parser.add_argument("--ON_OFF_dac"       , dest="ON_OFF_dac"       , type=auto_bool, default=True)
    parser.add_argument("--small_dac"        , dest="small_dac"        , type=auto_bool, default=True)
    parser.add_argument("--enb_outADC"       , dest="enb_outADC"       , type=auto_bool, default=False)
    parser.add_argument("--inv_startCmptGray", dest="inv_startCmptGray", type=auto_bool, default=False)
    parser.add_argument("--ramp_8bit"        , dest="ramp_8bit"        , type=auto_bool, default=True)
    parser.add_argument("--ramp_10bit"       , dest="ramp_10bit"       , type=auto_bool, default=False)
    parser.add_argument("--cmd_CK_mux"       , dest="cmd_CK_mux"       , type=auto_bool, default=False)
    parser.add_argument("--d1_d2"            , dest="d1_d2"            , type=auto_bool, default=False)
    parser.add_argument("--inv_discriADC"    , dest="inv_discriADC"    , type=auto_bool, default=False)
    parser.add_argument("--polar_discri"     , dest="polar_discri"     , type=auto_bool, default=False)
    parser.add_argument("--Enb_tristate"     , dest="Enb_tristate"     , type=auto_bool, default=True)
    parser.add_argument("--valid_dc_fsb2"    , dest="valid_dc_fsb2"    , type=auto_bool, default=False)
    parser.add_argument("--sw_fsb2_50f"      , dest="sw_fsb2_50f"      , type=auto_bool, default=False)
    parser.add_argument("--sw_fsb2_100f"     , dest="sw_fsb2_100f"     , type=auto_bool, default=True)
    parser.add_argument("--sw_fsb2_100k"     , dest="sw_fsb2_100k"     , type=auto_bool, default=False)
    parser.add_argument("--sw_fsb2_50k"      , dest="sw_fsb2_50k"      , type=auto_bool, default=True)
    parser.add_argument("--valid_dc_fs"      , dest="valid_dc_fs"      , type=auto_bool, default=False)
    parser.add_argument("--cmd_fsb_fsu"      , dest="cmd_fsb_fsu"      , type=auto_bool, default=False)
    parser.add_argument("--sw_fsb1_50f"      , dest="sw_fsb1_50f"      , type=auto_bool, default=False)
    parser.add_argument("--sw_fsb1_100f"     , dest="sw_fsb1_100f"     , type=auto_bool, default=True)
    parser.add_argument("--sw_fsb1_100k"     , dest="sw_fsb1_100k"     , type=auto_bool, default=False)
    parser.add_argument("--sw_fsb1_50k"      , dest="sw_fsb1_50k"      , type=auto_bool, default=True)
    parser.add_argument("--sw_fsu_100k"      , dest="sw_fsu_100k"      , type=auto_bool, default=False)
    parser.add_argument("--sw_fsu_50k"       , dest="sw_fsu_50k"       , type=auto_bool, default=False)
    parser.add_argument("--sw_fsu_25k"       , dest="sw_fsu_25k"       , type=auto_bool, default=False)
    parser.add_argument("--sw_fsu_40f"       , dest="sw_fsu_40f"       , type=auto_bool, default=True)
    parser.add_argument("--sw_fsu_20f"       , dest="sw_fsu_20f"       , type=auto_bool, default=True)
    parser.add_argument("--H1H2_choice"      , dest="H1H2_choice"      , type=auto_bool, default=True)
    parser.add_argument("--EN_ADC"           , dest="EN_ADC"           , type=auto_bool, default=True)
    parser.add_argument("--sw_ss_1200f"      , dest="sw_ss_1200f"      , type=auto_bool, default=False)
    parser.add_argument("--sw_ss_600f"       , dest="sw_ss_600f"       , type=auto_bool, default=False)
    parser.add_argument("--sw_ss_300f"       , dest="sw_ss_300f"       , type=auto_bool, default=True)
    parser.add_argument("--ON_OFF_ss"        , dest="ON_OFF_ss"        , type=auto_bool, default=True)
    parser.add_argument("--swb_buf_2p"       , dest="swb_buf_2p"       , type=auto_bool, default=False)
    parser.add_argument("--swb_buf_1p"       , dest="swb_buf_1p"       , type=auto_bool, default=False)
    parser.add_argument("--swb_buf_500f"     , dest="swb_buf_500f"     , type=auto_bool, default=True)
    parser.add_argument("--swb_buf_250f"     , dest="swb_buf_250f"     , type=auto_bool, default=False)
    parser.add_argument("--cmd_fsb"          , dest="cmd_fsb"          , type=auto_bool, default=True)
    parser.add_argument("--cmd_ss"           , dest="cmd_ss"           , type=auto_bool, default=True)
    parser.add_argument("--cmd_fsu"          , dest="cmd_fsu"          , type=auto_bool, default=False)
    parser.add_argument("--cmd_SUM"          , dest="cmd_SUM"          , type=auto_int, default=0) # 64 bits
    parser.add_argument("--Ctest"            , dest="Ctest"            , type=auto_int, default=0) # 64 bits

    args = parser.parse_args()

    if args.DAC1 < 0 or args.DAC1 >= (1 << 10):
        parser.error("DAC1 can only have 10 bits (0-1023)")
    if args.DAC0 < 0 or args.DAC0 >= (1 << 10):
        parser.error("DAC0 can only have 10 bits (0-1023)")
    if args.mask_OR2 < 0 or args.mask_OR2 >= (1 << 64):
        parser.error("mask_OR2 can only have 64 bits")
    if args.mask_OR1 < 0 or args.mask_OR1 >= (1 << 64):
        parser.error("mask_OR1 can only have 64 bits")
    if len(args.GAINS) != 64:
        parser.error(f"64 gains are needed. Only provided {len(arg.GAINS)}.")
    for gain in args.GAINS:
        if gain < 0 or gain >= (1 << 8):
            parser.error("gain values can only have 8 bits (0-255)")
    if args.cmd_SUM < 0 or args.cmd_SUM >= (1 << 64):
        parser.error("cmd_SUM can only have 64 bits")
    if args.Ctest < 0 or args.Ctest >= (1 << 64):
        parser.error("Ctest can only have 64 bits")

    if args.set_gain_ch is not None:
        for ch, gain in args.set_gain_ch:
            ch = auto_int(ch)
            gain = auto_int(gain)
            if ch < 0 or ch > 63:
                parser.error("Channel number needs to be between 0 and 63")
            if gain < 0 or gain > 255:
                parser.error("Gain needs to be between 0 and 255")
            args.GAINS[ch] = gain

    if args.ch_mask is not None:
        for ch in args.ch_mask:
            if ch < 0 or ch > 63:
                parser.error("Channel number needs to be between 0 and 63")
            args.mask_OR2 = args.mask_OR2 | (1<<ch)
            args.mask_OR1 = args.mask_OR1 | (1<<ch)

    args.cmd = 0x01

    if args.ip.__class__ == str:
        args.ip = ip_dict[args.ip][args.socket_type]


    def run_one(ip, socket_type, dst, cmd, payload):
        if socket_type == 'tcp':
            data = send_command_cb_tcp(ip, dst, cmd, payload, verbose=args.debug)
        elif socket_type == 'udp':
            data = send_command_cb_udp(ip, dst, cmd, payload, verbose=args.debug)

        return(post_processing(data))

    payload = create_payload_sc(args)

    for ROBid in args.dst_robs:
        output = ""
        try:
            output += f"ROB {ROBid:2d}  =>  "
            run_out = run_one(args.ip, args.socket_type, ROBid, args.cmd, payload)
            # run_out = " dry run"
            output += run_out + "\n"
        except ValueError:
            output += "Bad reply\n"
        except (TimeoutError, socket.timeout):
            output += "Command timed out\n"
        print_output(output)


