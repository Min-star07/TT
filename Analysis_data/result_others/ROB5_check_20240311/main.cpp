//
// Created by Min Li on 2023/6/27.
//
#include <iostream>
#include <fstream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TFitResult.h>
#include <TStopwatch.h>
#include <TLatex.h>
#include <TStyle.h>
#include <iomanip>


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


int main(){
   SetMystyle();
   TString filename[2] = {"FADC_normal_cCB-22_2024-03-11_10_24_hist.root", "FADC_normal_cCB-22_2024-03-11_10_24_hist.root"};
    
   TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    canvas1->Print("Compare_charge_spectrum.pdf[");
    gPad->SetLogy(); 
    gStyle->SetOptStat(0);
   // Define a Gaussian function
    TF1 *gaussian = new TF1("gaussian", "gaus", 100,270);
    for (Int_t id = 0; id < 64; id++)
    {
       TString histname;
       if (id < 10)
          histname = Form("h_charge_ROB05_ch0%d", id);
       else
          histname = Form("h_charge_ROB05_ch%d", id);
       cout << histname << endl;
       for (int j = 0; j < 2; j++)
       {
          TString inputfilename = filename[j];
          TFile *inputfile = new TFile(inputfilename);
          TH1F *histogram = (TH1F *)inputfile->Get(histname);
          Double_t factor = 100000;
          histogram->Scale(factor/histogram->Integral());
          histogram->GetXaxis()->SetRangeUser(0, 1500);
          histogram->Fit("gaussian", "R");
          TLegend *legend = new TLegend(0.6, 0.7, 0.9, 0.9);
          if(j ==0)
            {
               histogram->SetLineWidth(2); // Set the line width to 2
               histogram->SetLineColor(2); // Set the line width to 2
               histogram->Draw("hist");
               // Fit the histogram with the Gaussian function
               gPad->Update();
             TPaveStats *smcp = (TPaveStats *)histogram->GetListOfFunctions()->FindObject("stats");
             smcp->SetX1NDC(0.70);
             smcp->SetX2NDC(0.90);
             smcp->SetY1NDC(0.62);
             smcp->SetY2NDC(0.92);
             smcp->SetTextColor(kBlack);
             legend->AddEntry(histogram, "Pedestal", "l");
             legend->Draw("same");

            }
          
         else
         {
             histogram->SetLineWidth(2); // Set the line width to 2
             histogram->SetLineColor(4); // Set the line width to 2
             histogram->Draw("histsame");
             // Fit the histogram with the Gaussian function
            //  histogram->Fit("gaussian", "R");
            gPad->Update();
             TPaveStats *smcp = (TPaveStats *)histogram->GetListOfFunctions()->FindObject("stats");
             smcp->SetX1NDC(0.20);
             smcp->SetX2NDC(0.50);
             smcp->SetY1NDC(0.62);
             smcp->SetY2NDC(0.92);
             smcp->SetTextColor(kBlack);
             legend->AddEntry(histogram, "normal pededtal", "l");
             legend->Draw("same");

            
         }
         // Get the fit parameters
          gaussian->Draw("histsame");
         double mean = gaussian->GetParameter(1);
         double sigma = gaussian->GetParameter(2);
         // Create a legend to display fit statistics
         
         
         
         
    // Print the fit parameters
    std::cout << "Mean: " << mean << std::endl;
    std::cout << "Sigma: " << sigma << std::endl;
        

                    
        }
    canvas1->Print("Compare_charge_spectrum.pdf"); 
    }
     canvas1->Print("Compare_charge_spectrum.pdf]");

    return 0;
}