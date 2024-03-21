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
    double x_value = 0;
    // Find the maximum non-zero bin content and ensure continuity
    for (int i = 0; i < 400; i++) {
        
        //if (hist->GetBinContent(i) != 0 && hist->GetBinContent(i - 1) != 0 && hist->GetBinContent(i - 2) != 0) {
            if (hist->GetBinContent(i) < hist->GetBinContent(i-1) && hist->GetBinContent(i) <  hist->GetBinContent(i-2) && hist->GetBinContent(i) < hist->GetBinContent(i+1) && hist->GetBinContent(i) <  hist->GetBinContent(i+2) ) {
            x_value = i;
            break;
        }
    }
    return x_value;
}

double Getxmin(TH1F* hist){

    double x_value = 0;
    // Find the maximum non-zero bin content and ensure continuity
    for (int i = 0; i < 300; i++) {
        //if (hist->GetBinContent(i) != 0 && hist->GetBinContent(i - 1) != 0 && hist->GetBinContent(i - 2) != 0) {
            if (hist->GetBinContent(i) < hist->GetBinContent(i+1) && hist->GetBinContent(i) <  hist->GetBinContent(i+2) && hist->GetBinContent(i) < hist->GetBinContent(i+3)) {
            x_value = i;
            break;
        }
    }
    return x_value;
}