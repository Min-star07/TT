#include <iostream>
#include <fstream>
#include <cmath> // Include the cmath library for mathematical functions
#include "TMath.h"
// #include <TPaveStat.h>
using namespace std;

void SetMystyle()
{

   // Show the statistics box
//    gStyle->SetOptStat(1111); // Set the statistics option to show all statistics
   gStyle->SetOptFit(); 
   //Set pad Margin
   gStyle->SetPadLeftMargin(0.15);
   gStyle->SetPadBottomMargin(0.15);
   gStyle->SetPadTopMargin(0.05);
   gStyle->SetPadRightMargin(0.05);

   //Set Grid X and Y
   gStyle->SetPadGridX(1);
   gStyle->SetPadGridY(1);
   gStyle->SetPadTickY(1);
   gStyle->SetPadTickX(1);
   gStyle->SetLineWidth(2);

   //Set customize the axes
   gStyle->SetLabelSize(0.05, "XYZ");
   gStyle->SetLabelFont(132, "XYZ");
   gStyle->SetLabelOffset(0.01, "XYZ");
//    gStyle->SetNdivisions(105, "XYZ");
   // Set the label's alignment to center
   //gStyle->SetLabelAlign(22); // 22 corresponds to aligning the label at the center (X and Y axis)


   //Set Axia Title
   gStyle->SetTitleFont(132, "XYZ");
   gStyle->SetTitleOffset(1.2, "XYZ");
   gStyle->SetTitleSize(0.05, "XYZ");

   //Set legend
   gStyle->SetLegendBorderSize(0);
   gStyle->SetLegendFont(132);

   //histogram
   // Set the default line width for histograms using gStyle
   // gStyle->SetHistLineWidth(3); // Change the default histogram line width to 2 (adjust as needed)
   // gStyle->SetFuncColor(kPink); // Change the default histogram line width to 2 (adjust as needed)


}

double linearFunction(double *x, double *par) {
    return par[0] * x[0];
    // return y / a1;
}

double expfunction(double *x, double *par)
// double expfunction(double x, double a00, double a2, double a3,  double a4)
{
    double a00 = par[0];
    double a2 = par[1];
    double a3 = par[2];
    double a4 = par[3];
    double exponent = -1 * a3 * pow(x[0], a4); // Exponent value
    cout << exponent << endl;
    
    return a00 + a2 * (1 - exp(exponent));
    // return par[0] + par[1] * (1 - exp(-1 * par[2] * (pow(x[0], par[3]))));

    // double f1 = TMath::Log(1 - (y - a00) / a2);
    // double f2 = -f1 / a3;
    // double exponent = 1 / a4;
    // double f = TMath::Power(f, exponent);
    // cout << f1 << "\t"
    //      << f2
    //      << "\t" << exponent << "\t" << f << endl;
    // return f;
}
Double_t Q_inj_fit(Double_t *X, Double_t *par)
{
    Double_t x = *X;
    Double_t a0 = par[0];
    Double_t a00= par[1];
    Double_t a1 = par[2];
    Double_t a2 ;
     Double_t a3;
    Double_t a4 ;
    Double_t a5 = par[3];
    Double_t b  = par[4];
    Double_t val= 0;
    a4 = a1*b*(exp(a5) -1)/(a5* (a0-a00+a1*b) );
    a3 = a5*pow(b,-1*a4);
    a2 = a1*b*exp(a5)/(a4*a5);
    // cout << a1 << "\t" << a2 << "\t" << a3 << "\t" << a4 << "\t" << a5 << endl;
    if(x<=b)        {val = a0 + a1*x;}
    else if (x>=b)  {val = a00 + a2*( 1 - exp( -1*a3*pow(x, a4) ) ); }
    return val;
}
void read_root_compare(){
    SetMystyle();
    Double_t Q_injected[2][24];
    Double_t Q_measured[2][24];
    TString filename[2] = {"charge_compare_FADC.txt", "charge_compare_wilki.txt"};
    TString A, B, C, D;
    Double_t Q_error[2][24];
    Double_t RMS[2][24];
    Double_t Q_injected_new[24] = {10, 7.94, 6.31, 5.01, 3.98, 3.16, 2.51, 2.00, 1.58, 1.25, 1.00, 0.79, 0.63, 0.50, 0.40, 0.32, 0.25, 0.20, 0.16, 0.13, 0.10, 0.08, 0.06, 0.05};
    for (Int_t i = 0; i < 2; i++)
    {
        TString inputfile = filename[i];
        ifstream input;
        input.open(inputfile, ios::in);
        if(input.is_open()){
            cout << "read file from now ....." << endl;
            input >> A >> B >> C >> D;
            int j = 0;
            while (j<24)
            { 
                input >> Q_injected[i][j] >> Q_measured[i][j] >> Q_error[i][j] >> RMS[i][j];
                cout << Q_injected[i][j] << Q_measured[i][j] << Q_error[i][j] << RMS[i][j] << endl;
                j++;
            }
        }
    }
    
    // Define your exponential function
    // TF1 *expFunc = new TF1("expFunc", "[0] * exp([1] * x)", 2, 10);
    TF1 *Fit_function1 = new TF1("linearFunction", linearFunction, 0, 2, 1);
    TF1 *Fit_function3 = new TF1("linearFunction", linearFunction, 0, 2, 1);
    TF1 *Fit_function2 = new TF1("expfunction", expfunction, 2, 10, 4);
    TF1 *Fit_function4 = new TF1("expfunction", expfunction, 2, 10, 4);

    TF1 *Fit_function5 = new TF1("Q_inj_fit", Q_inj_fit, 0., 10, 5);
    Fit_function5->SetParameters(0.0, 1.5299210459820358, 53.51563939649799, 0.5462009562425585, 2.0);
    Fit_function5->SetNpx(500);
    // Fit_function5->FixParameter(0, 0.0);
    // Fit_function5->FixParameter(1, 1.5299210459820358);
    // Fit_function5->FixParameter(2, 53.51563939649799);
    // Fit_function5->FixParameter(3, 0.5462009562425585);
    // Fit_function5->FixParameter(4, 2.0);
    // vector<double> result;
    // int i = 0;
    // while (i < 10)
    // {
    //     result.push_back (Q_inj_fit(i));
    //     i = i + 1;

    // }
    auto *gr1 = new TGraph(24, Q_injected_new, Q_measured[0]);
    gr1->Fit(Fit_function1, "R");
    gr1->SetMarkerColor(kBlue);
    gr1->SetMarkerStyle(3);
    gr1-> SetMarkerSize(2);
    gr1-> GetXaxis() -> SetTitle("Charge injection [pC]");
            gr1-> GetYaxis() -> SetTitle("Charge measured [ADC]");
            gr1->GetXaxis()->CenterTitle();
            gr1->GetYaxis()->CenterTitle();
            gr1->SetTitle(""); // Cancels the title of the histogram
    double *slope_FADC = Fit_function1->GetParameters();
    Fit_function1->SetLineColor(kBlack);
    // gr1->Fit(Fit_function2, "R+");

    auto *canvas = new TCanvas("c1", "c1", 800, 600);
    canvas->cd();
    gr1->Draw("AP");
     
    canvas->SaveAs("test1.pdf");

    auto *gr2 = new TGraph(24, Q_injected_new, Q_measured[1]);
    gr2->SetMarkerColor(kRed);
    gr2->SetMarkerStyle(53);
    gr2-> SetMarkerSize(2);
    gr2->Fit(Fit_function3, "R");
    gr2-> GetXaxis() -> SetTitle("Charge injection [pC]");
            gr2-> GetYaxis() -> SetTitle("Charge measured [ADC]");
            gr2->GetXaxis()->CenterTitle();
            gr2->GetYaxis()->CenterTitle();
            gr2->SetTitle(""); // Cancels the title of the histogram
    double *slope_wilki = Fit_function3->GetParameters();
    Fit_function3->SetLineColor(kBlack);
    // gr2->Fit(Fit_function4, "R+");
    auto *canvas2 = new TCanvas("c2", "c2", 800, 600);
    canvas2->cd();
    gr2->Draw("AP");
    canvas2->SaveAs("test2.pdf");

    Double_t factor = slope_FADC[0] / slope_wilki[0];
    cout << factor << endl;
    Double_t Q_measured_norm[24];
    for (Int_t i = 0; i < 24; i++)
    {
        Q_measured_norm[i] = Q_measured[0][i] / factor;
        cout << Q_measured_norm[i] << "==========" << endl;
    }
    auto *gr3 = new TGraph(24, Q_injected_new, Q_measured_norm);
    gr3-> GetXaxis() -> SetTitle("Charge injection [pC]");
    gr3-> GetYaxis() -> SetTitle("Charge measured [ADC]");
    gr3->SetTitle("");
    gr3->SetMarkerColor(kBlue);
    gr3->SetMarkerStyle(3);
    gr3->SetMarkerSize(2);
    auto *gr4 = new TGraph(24, Q_injected_new, Q_measured[1]);
    gr4->SetMarkerColor(kRed);
    gr4->SetMarkerStyle(53);
    gr4-> SetMarkerSize(2);

    auto *canvas3 = new TCanvas("c3", "c3", 800, 600);
    canvas3->cd();
    gr3->Draw("AP");
    gr4->Draw("P1 same");
    Fit_function5->Draw("same");
    canvas3->SaveAs("test3.pdf");
}