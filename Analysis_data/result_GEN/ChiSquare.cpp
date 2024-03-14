#include <iostream>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include "Mystyle.h"
#include "Bellamy.h"
using namespace std;

void CalculateChiSquare(TH1* hist,  double xmin, double xmax, double *par_fit){
    double chi2 = 0.0;
    int ndf = 0;
    for (int i = hist->FindBin(xmin); i <= hist->FindBin(xmax); ++i) {
        double binCenter = hist->GetBinCenter(i);
        double observed =  hist->GetBinContent(i);
        double expected = Bellamy(&binCenter, par_fit);

         // Calculate chi-squared contribution for this bin
        if (expected != 0) { // Avoid division by zero
            double residuals = observed - expected;
            chi2 += pow(residuals,2)/expected;
            ndf++; // Increase the number of degrees of freedom
        }
    
    }
    double chi2ndf = chi2 / ndf;
    cout << chi2ndf <<"===hist->FindBin(xmin)==" << hist->FindBin(xmin) << "======hist->FindBin(xmax)====="<< hist->FindBin(xmax) <<endl;
    //return chi2ndf;
}