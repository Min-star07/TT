#include <iostream>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include "Mystyle.h"
#include "GetXmax_hist.h"
using namespace std;

double *FitHistogramWithGaussian(TString rootfilename, TString histoname, int mode) {

    TFile *file = new TFile(rootfilename);

    if (!file || file->IsZombie()) {
        std::cerr << "Error: Unable to open file " << std::endl;
        return 0;
    }

    // Get the histogram from the ROOT file
    TH1F *histogram = (TH1F*)file->Get(histoname);
    if (!histogram) {
        std::cerr << "Error: Unable to retrieve histogram from file" << std::endl;
        file->Close();
        return 0;
    }

    // Create a Gaussian fit function
    double xmin = Getxmin(histogram);
    double xmax = Getxmax(histogram);
    cout << "xmin: " << xmin << " xmax: " << xmax << endl;
    TF1 *gaussianFit;
    // if (mode == 1)
    // {
    //     gaussianFit = new TF1("gaussianFit", "gaus", 20, 30);
    // }
    // else{
    //     gaussianFit = new TF1("gaussianFit", "gaus", 200, 300);
    // }

    // TF1 *gaussianFit = new TF1("gaussianFit", "gaus");
    
    // Fit the histogram with the Gaussian function
    gaussianFit = new TF1("gaussianFit", "gaus", xmin, xmax);
    histogram->Fit(gaussianFit , "R");
    gaussianFit->Draw();

    static double fit_result[5];
    fit_result[0] = gaussianFit->GetParameter(0);
    fit_result[1] = gaussianFit->GetParameter(1);
    fit_result[2] = gaussianFit->GetParameter(2);
    fit_result[3] = xmin;
    fit_result[4] = xmax;
 
    // Print fit parameters
    std::cout << "Fit Parameters for Gaussian Function:\n";
    std::cout << "Mean: " << fit_result[1] << std::endl;
    std::cout << "Sigma: " << fit_result[2] << std::endl;
    std::cout << "Constant: " << fit_result[0] << std::endl;
    delete file;
    return fit_result;
}
