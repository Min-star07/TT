#include <iostream>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include "Mystyle.h"
using namespace std;

double Getxmax(TH1F* hist){

    int maxBin = -1; // Initialize maxBin to an invalid value
    double maxContent = -1.0; // Initialize maxContent to a minimum value
    double x_value = 130;
    // Find the maximum non-zero bin content and ensure continuity
    for (int i = 2000; i >=1; i--) {
        //if (hist->GetBinContent(i) != 0 && hist->GetBinContent(i - 1) != 0 && hist->GetBinContent(i - 2) != 0) {
            if (hist->GetBinContent(i) != 0 && hist->GetBinContent(i-1) != 0 && hist->GetBinContent(i-2) != 0) {
            x_value = i;
            break;
        }
    }
    return x_value;
}