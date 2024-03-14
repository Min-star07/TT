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
   // TString filename[4] = {"FADC_normal_cCB-22_2024-03-12_13_36_hist.root","FADC_led_cCB-22_2024-03-12_13_38_hist.root",  "FADC_normal_cCB-22_2024-03-12_13_41_hist.root", "FADC_led_cCB-22_2024-03-12_14_57_hist.root"};
   // TString filename[6] = {"FADC_led_cCB-22_2024-03-12_15_12_hist.root","FADC_led_cCB-22_2024-03-12_15_14_hist.root",  "FADC_led_cCB-22_2024-03-12_15_15_hist.root", "FADC_led_cCB-22_2024-03-12_15_16_hist.root", "FADC_led_cCB-22_2024-03-12_14_57_hist.root", "FADC_normal_cCB-22_2024-03-12_13_41_hist.root"};
   TString filename[5] = {"FADC_normal_cCB-22_2024-03-12_13_41_hist.root", "FADC_led_cCB-22_2024-03-12_15_16_hist.root", "FADC_led_cCB-22_2024-03-12_15_12_hist.root", "FADC_led_Bon_cCB-22_2024-03-12_15_59_hist.root", "FADC_led_ABon_cCB-22_2024-03-12_16_01_hist.root"};
   
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
       for (int j = 0; j < 5; j++)
       {
          TString inputfilename = filename[j];
          TFile *inputfile = new TFile(inputfilename);
          TH1F *histogram = (TH1F *)inputfile->Get(histname);
          Double_t factor = 100000;
          histogram->Scale(factor/histogram->Integral());
          histogram->GetXaxis()->SetRangeUser(200, 300);
          histogram->GetYaxis()->SetRangeUser(0.1,100000);
         //  histogram->Fit("gaussian", "R");
         //  TLegend *legend = new TLegend(0.6, 0.7, 0.9, 0.9);
          if(j ==0)
            {
               histogram->SetLineWidth(3); // Set the line width to 2
               histogram->SetLineColor(3); // Set the line width to 2
               histogram->Draw("hist");
               // Fit the histogram with the Gaussian function

            }
            if (j ==1){
             histogram->SetLineWidth(3); // Set the line width to 2
             histogram->SetLineColor(2); // Set the line width to 2
             histogram->Draw("histsame");
             // Fit the histogram with the Gaussian function
            //  histogram->Fit("gaussian", "R");
            }
          
         if(j==2)
         {
             histogram->SetLineWidth(3); // Set the line width to 2
             histogram->SetLineColor(4); // Set the line width to 2

             histogram->Draw("histsame");
             // Fit the histogram with the Gaussian function
            //  histogram->Fit("gaussian", "R");
         }
         if(j==3)
         {
             histogram->SetLineWidth(3); // Set the line width to 2
             histogram->SetLineColor(2); // Set the line width to 2
              histogram->SetLineStyle(2); // Set the line width to 2
             histogram->Draw("histsame");
             // Fit the histogram with the Gaussian function
            //  histogram->Fit("gaussian", "R");
         }
         if(j==4)
         {
             histogram->SetLineWidth(3); // Set the line width to 2
             histogram->SetLineColor(4); // Set the line width to 2
             histogram->SetLineStyle(2); // Set the line width to 2
             histogram->Draw("histsame");
             // Fit the histogram with the Gaussian function
            //  histogram->Fit("gaussian", "R");
         }
         // Get the fit parameters
         //  gaussian->Draw("histsame");
         // double mean = gaussian->GetParameter(1);
         // double sigma = gaussian->GetParameter(2);
         // Create a legend to display fit statistics
         
         
         
         
    // Print the fit parameters
   //  std::cout << "Mean: " << mean << std::endl;
   //  std::cout << "Sigma: " << sigma << std::endl;
        

                    
        }
    canvas1->Print("Compare_charge_spectrum.pdf"); 
    }
     canvas1->Print("Compare_charge_spectrum.pdf]");

    return 0;
}