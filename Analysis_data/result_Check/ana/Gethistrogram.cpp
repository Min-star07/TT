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
#include "Mystyle.h"
using namespace std;

int main (int argc, char** argv){
    SetMystyle();  
    // gStyle->SetOptFit(1111);                                                        
    //set initial parmeters
    TString rootfile;
    TString inputfilename;
    string rob_id = "2";
    string channel_id = "2";
    TString sigma_id = "2";

     for(int i = 0; i < argc; i ++){
        if(strcmp(argv[i], "-ROB") == 0){
            rob_id = argv[i+1];
        }
         if(strcmp(argv[i], "-CH") == 0){
            channel_id = argv[i+1];
        }
    }

    TString ROB_id = rob_id;
    TString CH = channel_id;
    int ROB_id_new = atoi(rob_id.c_str());
    int Chanel_id = atoi(channel_id.c_str());
    TString pathDir1 = "../check/Result";
    TString pathDir2 = "./Final_Result";
    rootfile = pathDir1 + "/fit_result_ROB_"+ ROB_id + "_channel_" + CH +".root";
    TString filename = rootfile;
    TFile *infile = new TFile(filename, "READ");
    // Check if the file is opened successfully
    if (!infile || infile->IsZombie()) {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 0;
    }
     TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    canvas1->Print("Final_Result/ROB_" + ROB_id + "_check_channel_" + CH + "_result.pdf[");
    gPad->SetLogy();     
    for (int i = 0; i < 4; i ++)
    {
        TString histname;
        if (ROB_id_new < 10)
        {
            if (Chanel_id < 10)
                histname = "h_charge_ROB0" + ROB_id + "_ch0" + CH + "_sigma_" + i;
            else
                histname = "h_charge_ROB0" + ROB_id + "_ch" + CH + "_sigma_" + i;
        }
        else{
            if (Chanel_id < 10)
                 histname = "h_charge_ROB" + ROB_id + "_ch0" + CH  + "_sigma_" + i;
            else
                histname = "h_charge_ROB" + ROB_id + "_ch" + CH + "_sigma_" + i;
    }
        cout << histname << endl;
        TH1F *histogram = (TH1F*)infile->Get(histname);
        histogram->SetLineWidth(2); // Set the line width to 2
        histogram->SetLineColor(1); // Set the line width to 2
        histogram->GetXaxis()->SetRangeUser(0, 1200);
         // Sets logarithmic scale for the current pad
        histogram->Draw();
        canvas1->Print("Final_Result/ROB_" + ROB_id + "_check_channel_" + CH + "_result.pdf");   
    }
      canvas1->Print("Final_Result/ROB_" + ROB_id + "_check_channel_" + CH + "_result.pdf]");  
    return 0;
}