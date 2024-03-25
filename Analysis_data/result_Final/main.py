import argparse
import analysis_Q1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=int, help="mode number", required=True)
    args = parser.parse_args()

    # check Q1 parameters
    filepath = "./CB" + str(args.CB) + "/ROB" + str(args.ROB)

    parser.add_argument("--filepath", default=filepath, help="filepath list")
    args = parser.parse_args()
    filename = "/Final_result_CB" + str(args.CB) + "_ROB" + str(args.ROB) + ".txt"
    print(args)
    infile = filepath + filename

    analysis_Q1.Calculate_chi2ndf(filepath, infile, args.CB, args.ROB, args.mode)
    analysis_Q1.Hist1D_Q1_distrubution(filepath, infile, args.CB, args.ROB, args.mode)
    analysis_Q1.Hist2D_Q1_distrubution(filepath, infile, args.CB, args.ROB, args.mode)
