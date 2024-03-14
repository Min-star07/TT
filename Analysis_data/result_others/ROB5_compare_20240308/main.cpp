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
   TString filename[2] = {"FADC_led_cCB-22_2024-03-06_17_05_hist.root", "FADC_led_cCB-22_2024-03-06_16_22_hist.root"};
    
   TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    canvas1->Print("Compare_charge_spectrum.pdf[");
    gPad->SetLogy(); 
    gStyle->SetOptStat(0);
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
          Double_t factor = 1.;
          histogram->Scale(factor/histogram->Integral());
          histogram->GetXaxis()->SetRangeUser(0, 1500);
          if(j ==0)
            {
               histogram->SetLineWidth(2); // Set the line width to 2
               histogram->SetLineColor(2); // Set the line width to 2
               histogram->Draw("hist");
            }
          
         else
         {
             histogram->SetLineWidth(2); // Set the line width to 2
             histogram->SetLineColor(4); // Set the line width to 2
             histogram->Draw("histsame");
         }
        

          //  TLegend *led1 = new TLegend(0.7, 0.7, 0.9, 0.9);
          //  led1->SetTextFont(132);
          //  led1->SetTextSize(0.05);
          //  led1->SetFillColorAlpha(0, 0);
          //  led1->SetBorderSize(0);
          //  if (j == 0)
          //      led1->AddEntry(histogram, "FEB 985", "l");
          //  else
          //      led1->AddEntry(histogram, "FEB 2", "l");
          //  led1->Draw("same");
                    
        }
    canvas1->Print("Compare_charge_spectrum.pdf"); 
    }
     canvas1->Print("Compare_charge_spectrum.pdf]");

    return 0;
}