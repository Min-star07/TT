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

int *Getsigma(TString inputfilename, TString ROB){
    int  rob[64]={0};
    int  channel[64]={0};
    int  method[64]={0};
    int  chi2[64]={0};
    double chi2ndf[64]={0};
    static int sigma[64]={0};
    double ped_mean[64] ={0};
    double ped_sigma[64]={0};
    double min[64]={0};
    double max[64]={0};
    double n[64]={0.0};
    double q0[64]={0};
    double q1[64]={0};
    double sigma0[64]={0};
    double sigma1[64]={0};
    double w[64]={0};
    double alpha[64]={0};
    double mu[64]={0};
    double err1[64]={0};
    double err2[64]={0};
    double err3[64]={0};
    double err4[64]={0};
    double err5[64]={0};
    double err6[64]={0};
    double err7[64]={0};
    double err8[64]={0};
    string A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,R,S,T,U,V,W,X, Y,Z, a;
    ifstream inputfile;
    inputfile.open(inputfilename, ios::in);
    inputfile>>A >>B >>C >> D>> E >>F >>G >>H >>I >>J >>K >>L >>M >> N >> O >>P>>R>>S>>T>>U>>V>>W>>X>>Y>>Z>>a;
    // cout << A << "\t" << B <<endl;
    int i =0;
    while(i<64){
        inputfile>> rob[i] >> channel[i] >> method[i] >> chi2[i] >> chi2ndf[i] >>ped_mean[i] >>ped_sigma[i]>> sigma[i] >> min[i] >> max[i] >> n[i] >> q0[i] >> q1[i] >> sigma0[i] >> sigma1[i] >> w[i] >> alpha[i] >> mu[i] >>err1[i] >>err2[i] >>err3[i]>>err4[i]>>err5[i]>>err6[i]>>err7[i]>>err8[i];
        
        cout << rob[i] << "\t"<< channel[i] << "\t"<< method[i] << "\t"<< chi2[i] << "\t"<<  chi2ndf[i] << "\t"<< sigma[i] << "\t"<< min[i] << "\t"<< max[i] << "\t"<< n[i] << "\t"<< q0[i] << "\t"<< q1[i] << "\t"<< sigma0[i] << "\t"<< sigma1[i] << "\t"<< w[i] << "\t"<< alpha[i] << "\t"<< mu[i]<<"\t" << err1[i] <<"\t" << err2[i] <<"\t" <<err3[i] <<"\t" <<err4[i]<<"\t" <<err5[i]<<"\t" <<err6[i]<<"\t" <<err7[i]<<"\t" <<err8[i] << endl;
  
        i++;
        //cout << i << endl;
    }
    inputfile.close();

    // tree->Fill();
    // tree->Write();
    // outfile->Close();
    return sigma;

}
int main (int argc, char** argv){
    SetMystyle();  
     string rob_id = "1";
     string mode_id = "1";
     string cb_id = "1";
     for (int i = 0; i < argc; i++)
     {
        if (strcmp(argv[i], "-CB") == 0)
         {
             cb_id = argv[i + 1];
         }
       if (strcmp(argv[i], "-ROB") == 0)
         {
             rob_id = argv[i + 1];
         }  
         if (strcmp(argv[i], "-MODE") == 0)
         {
             mode_id = argv[i + 1];
         }
     }

    TString ROB = rob_id;
    TString CB = cb_id;
    TString MODE = mode_id;
    int rob_id_toint = atoi(rob_id.c_str());
    int mode_id_toint = atoi(mode_id.c_str());

    TString pathDir1 = "../result_GEN/Result/CB";
    TString pathDir2 = "/ROB";
    TString pathDir3 = "./Result/CB" + CB + "/ROB" + ROB;
    TString pathDir = pathDir1 + CB + pathDir2 + ROB;
    TString inrootfile = pathDir + "/fit_result_ROB_" + ROB + "_mode_"+ MODE + ".root";
    TString filename = "/CB" + CB + "_ROB" + ROB + "_final_result_mode_"+ MODE +".txt";
    TString inputfilename = pathDir3 + filename;
    TString outfilename =  "/CB" + CB + "_ROB" + ROB + "_final_result_mode_"+ MODE +".root";
    TString outrootfilename = pathDir3 + outfilename;
    int *Sigma = Getsigma(inputfilename, ROB);
    TFile *infile = new TFile(inrootfile, "READ");
    
    TFile *outfile = new TFile(outrootfilename, "RECREATE");
    // Check if the file is opened successfully
    if (!infile || infile->IsZombie()) {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 0;
    }
    
    TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    canvas1->Print(pathDir3 + "/CB" + CB + "_ROB" + ROB + "_final_result_mode_"+ MODE +".pdf[");
    gPad->SetLogy();     
    for(int id = 0 ; id < 64; id ++){
        
        TString histname;

         if (rob_id_toint <10){
        if (id < 10)
            histname = "h_charge_ROB0" + ROB + "_ch0" + id  + "_sigma_" + Sigma[id];
        else
            histname = "h_charge_ROB0" + ROB + "_ch" + id + "_sigma_" + Sigma[id];
    }
    else{
       if (id < 10)
            histname = "h_charge_ROB" + ROB + "_ch0" + id  + "_sigma_" + Sigma[id];
        else
            histname = "h_charge_ROB" + ROB + "_ch" + id + "_sigma_" + Sigma[id];
    }
    
        
        cout << histname << endl;
        TH1F *histogram = (TH1F*)infile->Get(histname);
        histogram->SetLineWidth(2); // Set the line width to 2
        histogram->SetLineColor(1); // Set the line width to 2
        if(mode_id_toint == 1)
            {histogram->GetXaxis()->SetRangeUser(0, 200);
            }
        else
            {histogram->GetXaxis()->SetRangeUser(0, 1500);}
         // Sets logarithmic scale for the current pad
            outfile->cd();
            histogram->Write();
            histogram->Draw();
            canvas1->Print(pathDir3 + "/CB" + CB + "_ROB" + ROB + "_final_result_mode_"+ MODE +".pdf");   
    }
    canvas1->Print(pathDir3 + "/CB" + CB + "_ROB" + ROB + "_final_result_mode_"+ MODE +".pdf]");
    outfile->Close();
    return 0;
}