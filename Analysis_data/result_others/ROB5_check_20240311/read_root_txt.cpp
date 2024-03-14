#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TH2.h>
#include <TCanvas.h>
#include <TString.h>
#include <math.h>
#include <iomanip>

using namespace std;

int read_root_txt() {

    //open root
    TString inputfilename = {"./FADC_normal_cCB-22_2024-03-11_10_24_hist.root"};
    // TString inputfilename = {"./normal_FADC_cCB-22_2024-02-12_16_13.root"};

    TFile *inputfile = new TFile(inputfilename);
    cout<<"open success" <<endl;
    UShort_t charge[64];
    TTree *mytree = (TTree *)inputfile->Get("TT_CB_ROB_data");
    mytree->SetBranchAddress("charge", &charge);
    int entries = (int)mytree->GetEntries();
    cout << "--------> test1 : " << entries << endl;
    TH1F *hist_charge[50];
    Double_t gr_charge_measured[24];
    Double_t gr_charge_injection_old[24] = {0.05, 0.06, 0.08, 0.1, 0.13, 0.16, 0.20, 0.25, 0.32, 0.40, 0.50, 0.63, 0.79, 1, 1.25, 1.58, 2.00, 2.51, 3.16, 3.98, 5.01, 6.31, 7.94, 10};
    Double_t gr_charge_injection[24];
    for (int i = 0; i < 24; i++){
        gr_charge_injection[i] = gr_charge_injection_old[23 - i];
        cout << gr_charge_injection[i] << endl;
    }

        // save t ooutfile
        TString outfile = "charge_compare_wilki.txt";
    ofstream outfile_txt;
    outfile_txt.open(outfile, ios::out);
    outfile_txt << "chargeinjection"
                << "\t"
                << "chargemeasure"
                << "\t"
                << "measureerror"
                << "\t"
                << "RMS" << endl;
    ;
    // hold time
    for (int i = 0; i < 24; i ++){
        int dt = i;
        // TString outfilename = "./charge_spectrum_dt_";
        // TString outfile = outfilename + dt + ".root";
        // TFile *outrootfile = new TFile(outfile, "RECREATE");
        // for (int j = 0; j < 64;j ++){
        TString histname = "charge_" + TString(Form("%d", i));
        cout << histname << endl;
        hist_charge[i] = new TH1F(histname, histname, 4000, 0, 4000);
        for (int eventID = i*50000; eventID < (i+1)*50000; eventID++) {
            mytree->GetEntry(eventID);
            hist_charge[i]->Fill(charge[5]);
        }

        Double_t mean = hist_charge[i]->GetMean();
        Double_t RMS = hist_charge[i]->GetRMS();
        Double_t meanerror = hist_charge[i]->GetMeanError();
        gr_charge_measured[i] = mean;
        cout << i << "\t" << mean << "\t" << meanerror << "\t" << RMS << endl;
        outfile_txt << i << "\t" << mean - 23.52 << "\t" << meanerror << "\t" << RMS << endl;
        // hist_charge[i]->Write();
        // outrootfile->Write();
        // outrootfile->Close();

        // //loop for mean and error
        
    }
    inputfile->Close();
    outfile_txt.close();
    Double_t gr_charge_measured_trans[24];
    // for (int i = 0; i < 24; i++)
    // {
    //     gr_charge_measured_trans[i] = gr_charge_measured[i] / 16.0;
    // }

    auto *gr = new TGraph(24, gr_charge_injection, gr_charge_measured);
    gr->Draw("AP*");
    return 0;
}

