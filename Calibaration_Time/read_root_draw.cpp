#include <iostream>
#include <fstream>
#include <TFile.h>
#include <TGraph.h>
#include <math.h>
#include <TMath.h>
#include "TGraphErrors.h"
#include "TCanvas.h"
// #include "Mystyle.h"
using namespace std;
Double_t Q_function(Double_t *Xarr, Double_t *par)
{
    Double_t x      = *Xarr;
    Double_t N_0    = par[0];
    Double_t mu     = par[1];
    Double_t sigma  = par[2];
    Double_t y      = (x-mu)/sigma;
    Double_t Q      = 0.5*N_0*TMath::Erfc(y/sqrt(2));
    return Q;
}

void SetMystyle()
{

   // Show the statistics box
   //  gStyle->SetOptStat(1111); // Set the statistics option to show all statistics
   gStyle->SetOptFit(1111); 
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

int read_root_draw (){
    SetMystyle();  
    TString outfilename =  "./efficiency_vs_threshold_graph.root";
    TFile *outfile_root = new TFile(outfilename, "RECREATE");
     // Open a file for writing
     Double_t mu[17] = {0};
     Double_t mu_error[17] = {0};
    ofstream outfile_txt;
    TString outfile1= "fitresult.txt"; 
    outfile_txt.open(outfile1, ios::app);
    outfile_txt << "N" << "\t" << "mu" << "\t" << "sigma" << "\t" << "err1" <<"\t" << "err2"<< "\t"<<"err3"<< endl;
    
    TString threshold[17] = {"0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0", "2.2", "2.5"};
    for (int j = 0; j < 17; j++){
        Double_t DAC[13] = {0};
        Double_t Count[13] = {0};
        Double_t Eff[13] = {0};
        Double_t error[13] = {0};
        Double_t ex[13] = {0};
        
        TString filename = "./DT_data_20240122/photo_" + threshold[j] + ".txt";
        cout << filename << endl;
        ifstream inputfile;
        inputfile.open(filename, ios::in);
        TString A, B, C, D;
        inputfile >> A >> B >> C >>D;
            int i =0;
        while(i<13){
            inputfile>> DAC[i] >> Count[i] >> Eff[i] >>error[i] ;
            cout << DAC[i] << "\t" << Count[i] << "\t" << Eff[i] << endl;
            i++;
            //cout << i << endl;
        }
        inputfile.close();
        Int_t n = 13;
        // auto gr = new TGraph(n, DAC, Eff);
        auto gr = new TGraphErrors(n, DAC, Eff,ex,error);
        TF1 *Fit_function = new TF1("Q_function", Q_function, DAC[0], DAC[11], 3);
        Fit_function->SetParameters(100, DAC[6], 10);
        Fit_function->FixParameter(0, 100);
        Fit_function->SetParNames("N_{0}","#mu", "#sigma" );
        TString gr_name = "photo_" + threshold[j];
        // Modify the name of the TGraph
        gr->SetName(gr_name);
        gr->Fit(Fit_function, "RL");
        double *para_fit;
        const double *para_fit_error;
        para_fit = Fit_function->GetParameters();
        para_fit_error = Fit_function->GetParErrors();
        cout << para_fit[0] << "\t" << para_fit[1] << "\t" << para_fit[2] << endl;
        outfile_txt << para_fit[0] << "\t" << para_fit[1] << "\t" << para_fit[2] << para_fit_error[0] << "\t" << para_fit_error[1] << "\t" << para_fit_error[2]<< endl;
        mu[j] = para_fit[1];
        mu_error[j] = para_fit_error[1];
        // auto c = new TCanvas("c","A Zoomed Graph",200,10,700,500);
        // c->DrawFrame(0,1,0.5,8);
        // gr->Draw("LP");
        gr->Write();   

        if (j == 3){
            cout << "========================" << endl;
            gr->SetMarkerColor(kBlue);
            gr->SetMarkerStyle(3);
            gr-> SetMarkerSize(2);
            gr-> GetXaxis() -> SetRangeUser(420, 480);
            gr-> GetXaxis() -> SetTitle("Charge injection [p.e.]");
            gr-> GetYaxis() -> SetTitle("Efficiency [%]]");
            gr->GetXaxis()->CenterTitle();
            gr->GetYaxis()->CenterTitle();
            gr->SetTitle(""); // Cancels the title of the histogram
            gr->Draw();
        }
    }
    outfile_txt.close();
    outfile_root->Close();



     // Create a linear function: f(x) = mx + b
    TF1 *linearFunc = new TF1("linearFunc", "[0]*x + [1]");
    // Set initial values for the parameters (slope and intercept)
    // linearFunc->SetParameter(0, 1.0); // Initial guess for the slope (m)
    // linearFunc->SetParameter(1, 0.0); // Initial guess for the intercept (b)
    linearFunc->SetParNames("Slope", "Intercept");
    Double_t pe[17] = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5};
    Double_t pe_error[17] = {0.0};

    TGraphErrors *graph = new TGraphErrors(17, pe, mu, pe_error, mu_error);



    // / Customize the graph properties (optional)
    // graph->SetTitle("Graph with Error Bars");
    graph->SetMarkerStyle(20);
    graph->SetMarkerSize(1.0);
    graph->SetLineColor(kBlue);
    graph->Fit("linearFunc", "Q");

    // Access the fit results
    double slope = linearFunc->GetParameter(0);
    double slopeError = linearFunc->GetParError(0);
    double intercept = linearFunc->GetParameter(1);
    double interceptError = linearFunc->GetParError(1);

    // Print the fit results
    std::cout << "Slope: " << slope << " +/- " << slopeError << std::endl;
    std::cout << "Intercept: " << intercept << " +/- " << interceptError << std::endl;

    // Set x-axis label
    graph->GetXaxis()->SetTitle("p.e.");
    graph->GetXaxis()->CenterTitle();
    // Set x-axis label
    graph->GetYaxis()->SetTitle("DAC [ADC]");
    graph->GetYaxis()->CenterTitle();
    graph->SetTitle(""); // Cancels the title of the histogram
    // Create a canvas and draw the graph

 
    TCanvas *canvas = new TCanvas("canvas", "Graph with Error Bars", 800, 600);
    graph->Draw("AP"); // "AP" option draws both the markers and the error bars

    // Optionally, add a legend or other decorations
    // (e.g., canvas->BuildLegend(), canvas->SetGrid(), etc.)
    
       // Assuming graph is a TGraph object
Double_t x = 1/3.0; // x coordinate where you want to place the marker
Double_t y = slope * 1/3.0 + intercept;  // y coordinate where you want to place the marker
Int_t pointIndex = graph->GetN(); // Get the number of points in the graph (to determine the index of the new point)

// Add the point to the graph
graph->SetPoint(pointIndex, x, y);
// graph->SetMarkerColor(kRed); // Set marker color to red
    // Save the canvas as an image or display it

    // Create a TLatex object
TLatex *text = new TLatex(x+ 0.03, y-1, "428 ADC @ 1/3 p.e.");

// Set text properties
text->SetTextSize(0.03);
text->SetTextColor(kBlack);

// Add the text to the graph
text->Draw("same");
    canvas->SaveAs("DAC_vs_pe.pdf");
    return 0;
}