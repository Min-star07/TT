#include <iostream>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include "Mystyle.h"
using namespace std;

double *FitHistogramWithGaussian(TString rootfilename, TString histoname) {

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
    TF1 *gaussianFit = new TF1("gaussianFit", "gaus");
    // TF1 *gaussianFit = new TF1("gaussianFit", "gaus", 20, 40);
    //TF1 *gaussianFit = new TF1("gaussianFit", "gaus");
    
    // Fit the histogram with the Gaussian function
    // histogram->Fit(gaussianFit, "R");
    histogram->Fit(gaussianFit);
    // Create a canvas
    //TCanvas *canvas = new TCanvas("canvas", "Fitted Histogram", 800, 600);

    // Draw the histogram
    //  TCanvas *canvas3 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    // canvas3->cd();
    // gPad->SetLogy(); // Sets logarithmic scale for the current pad
    // histogram->Draw();
    // canvas3->SaveAs("ped.pdf");
    static double fit_result[2];
    fit_result[0] = gaussianFit->GetParameter(1);
    fit_result[1] = gaussianFit->GetParameter(2);
 
    // Print fit parameters
    std::cout << "Fit Parameters for Gaussian Function:\n";
    std::cout << "Mean: " << fit_result[0] << std::endl;
    std::cout << "Sigma: " << fit_result[1] << std::endl;
    delete file;
    return fit_result;
}