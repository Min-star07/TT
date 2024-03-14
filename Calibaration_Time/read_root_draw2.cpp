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
    Double_t a    = par[0];
    Double_t b     = par[1];
    Double_t c  = par[2];
     Double_t d  = par[3];
    Double_t Q      = a*pow(x,3) + b *pow(x,2) + c*x +d;
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
   gStyle->SetNdivisions(706, "XYZ");
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

int read_root_draw2 (){
    SetMystyle();  
    TString infilename =  "./holddelay_test2.root";
    TFile *inputrootfile = new TFile(infilename);
    cout<<"open success" <<endl;
    Double_t holddelay;
    Double_t holdtime;
    Double_t HT[52];
    Double_t HD[52];
    TTree *mytree = (TTree *)inputrootfile->Get("tree");
    mytree->SetBranchAddress("holdtime", &holdtime);
    mytree->SetBranchAddress("holddelay", &holddelay);
    Int_t entries = (int)mytree->GetEntries();
    cout << "--------> test1 : " << entries << endl;
    for (int i = 0; i < entries; i ++){
        mytree -> GetEntry(i);
        HT[i] = holdtime;
        HD[i] = holddelay;
    }
    TF1 *Fit_function = new TF1("Q_function", Q_function, 0, 255, 4);
    auto *gr = new TGraph(entries, HD, HT);
    gr->Fit(Fit_function, "RL");
    auto *canvas = new TCanvas("c1", "c1", 800, 600);
    canvas->cd();
    gr->Draw("AP*");
    canvas->SaveAs("holddelay_test2_1.pdf");
    inputrootfile->Close();
    return 0;
}