import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from fit_function import Linear_fc1, q_function

plt.style.use("mystyle.txt")


def read_txt_to_draw(args):
    filepath = args.mode_list
    print(filepath)
    slope_list = []
    for i, item in enumerate(filepath):
        df = pd.read_csv(item, sep="\t")
        print(df)
        ax = plt.axes(xlabel="Charge injection [pC]", ylabel="Charge measured [ADC]")
        plt.scatter(
            args.charge,
            df["chargemeasure"],
            marker="+",
            s=80,
            color="darkgreen",
            label=item,
        )
        popt, popv = curve_fit(Linear_fc1, args.charge[7:], df["chargemeasure"][7:])
        print(popt)
        fit_x = np.arange(0, 2, 0.2)
        plt.plot(
            fit_x,
            Linear_fc1(fit_x, *popt),
            color="red",
            label="slope : %.2f" % (popt[0]),
        )
        print(popt)
        plt.legend()
        plt.grid(which="both", alpha=0.3, linestyle=":")
        plt.show()

        ##add slope for conversion factor
        slope_list.append(popt[0])
    return slope_list[0] / slope_list[1]


def read_txt_to_draw_normlization(args):
    filepath = args.mode_list
    print(filepath)
    ax = plt.axes(
        xlabel="Charge injection [pC]",
        ylabel="Charge measured [ADC]",
        ylim=[0, 255],
        xlim=[0, 10],
    )
    for i, item in enumerate(filepath):
        df = pd.read_csv(item, sep="\t")
        if i == 0:
            charge_measure = df["chargemeasure"] / args.conversion_factor
        else:
            charge_measure = df["chargemeasure"]
        # plt.errorbar(
        #     charge_injection[::-1],
        #     charge_measure,
        #     df["measureerror"],
        #     capsize=7,
        #     color=color[i],
        #     fmt="o",
        #     label=label[i],
        # )
        plt.plot(
            args.charge,
            charge_measure,
            color=args.color[i],
            marker=args.marker[i],
            fillstyle="none",
            linestyle="none",
            label=args.label[i],
            markersize=10,
        )
    # add calibration fit function result
    popt = args.calibration_result.iloc[:, 4:9]
    popt = popt.values.tolist()[0]
    # result = q_function(x, popt[0], popt[1], popt[2], popt[3], popt[4])
    x = np.arange(0, 10, 0.2)
    fit_curve = []
    for i in x:
        fit_curve.append(q_function(i, *popt))
    plt.plot(x, fit_curve, color="red", label="Calibration result")
    ax.axvspan(0.16, 0.32, alpha=0.5, color="cyan")
    plt.title(f"FEB_{args.FEB}_CH_{args.CH}")
    plt.legend()
    plt.grid(which="both", alpha=0.2, linestyle=":")
    plt.savefig("test3.pdf")
    plt.show()
