import argparse
from read_root import read_calibration_result
from read_txt import read_txt_to_draw, read_txt_to_draw_normlization

if __name__ == "__main__":
    charge_injection = [
        0.05,
        0.06,
        0.08,
        0.1,
        0.13,
        0.16,
        0.20,
        0.25,
        0.32,
        0.40,
        0.50,
        0.63,
        0.79,
        1,
        1.25,
        1.58,
        2.00,
        2.51,
        3.16,
        3.98,
        5.01,
        6.31,
        7.94,
        10,
    ]
    label = ["FADC mode", "Wilki mode"]
    color = ["blue", "red"]
    marker = ["+", "o"]
    parser = argparse.ArgumentParser(
        description="Read the TT electronics calibration result from ROOT file"
    )
    parser.add_argument("--FEB", type=int, help="FEB number", required=True)
    parser.add_argument("--CH", type=int, help="CH number", required=True)
    parser.add_argument("--mode_list", nargs="+", help="filepath list", required=True)
    parser.add_argument(
        "--charge", default=charge_injection[::-1], help="default charge"
    )
    parser.add_argument("--color", nargs="+", default=color, help="color list")
    parser.add_argument("--label", nargs="+", default=label, help="label list")
    parser.add_argument("--marker", nargs="+", default=marker, help="marker list")
    args = parser.parse_args()
    cali_result = read_calibration_result(args)
    con_factor = read_txt_to_draw(args)
    parser.add_argument(
        "--conversion_factor", default=con_factor, help="conversion factor"
    )
    parser.add_argument(
        "--calibration_result", default=cali_result, help="calibration result"
    )
    args = parser.parse_args()
    print(args.conversion_factor)
    read_txt_to_draw_normlization(args)
