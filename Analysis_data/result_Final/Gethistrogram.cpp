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
#include <TPaveStats.h>
#include <iomanip>
#include "Mystyle.h"
#include "FitHistogramWithGaussian.h"
using namespace std;

// Gaussian function with parameters: amplitude (A), mean (mu), and standard deviation (sigma)
Double_t gaussian(Double_t *x, Double_t *par) {
    return par[0] * TMath::Gaus(x[0], par[1], par[2], kTRUE);
}
std::string formatNumber(int num) {
    // Format the number with leading zeros
    std::stringstream ss;
    ss << std::setw(2) << std::setfill('0') << num;

    // Copy the formatted result to a new variable
    std::string formattedNum;
    ss >> formattedNum;

    return formattedNum;
}
std::tuple<std::vector<int>, std::vector<int>, std::vector<double> >returnThreeArrays(TString inputfilename){
    cout << "Reading file " << inputfilename << endl;
   
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
    static int  mark[64] = {0};
    double err1[64]={0};
    double err2[64]={0};
    double err3[64]={0};
    double err4[64]={0};
    double err5[64]={0};
    double err6[64]={0};
    double err7[64]={0};
    double err8[64]={0};
    string A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X, Y,Z, a;
    ifstream inputfile;
    inputfile.open(inputfilename, ios::in);
    inputfile>>A >>B >>C >> D>> E >>F >>G >>H >>I >>J >>K >>L >>M >> N >> O >>P>>Q>>R>>S>>T>>U>>V>>W>>X>>Y>>Z>>a;
    // cout << A << "\t" << B <<endl;
    int i =0;
    while(i<64){
        inputfile>> rob[i] >> channel[i] >> method[i] >> chi2[i] >> chi2ndf[i] >>ped_mean[i] >>ped_sigma[i]>> sigma[i] >> min[i] >> max[i] >> n[i] >> q0[i] >> q1[i] >> sigma0[i] >> sigma1[i] >> w[i] >> alpha[i] >> mu[i] >>err1[i] >>err2[i] >>err3[i]>>err4[i]>>err5[i]>>err6[i]>>err7[i]>>err8[i]>>mark[i]; 
        // cout << rob[i] << "\t"<< channel[i] << "\t"<< method[i] << "\t"<< chi2[i] << "\t"<<  chi2ndf[i] << "\t"<< sigma[i] << "\t"<< min[i] << "\t"<< max[i] << "\t"<< n[i] << "\t"<< q0[i] << "\t"<< q1[i] << "\t"<< sigma0[i] << "\t"<< sigma1[i] << "\t"<< w[i] << "\t"<< alpha[i] << "\t"<< mu[i]<< endl;
        i++;
        //cout << i << endl;
    }
    inputfile.close();

    //copy array to vector
    int array_size = sizeof(sigma)/sizeof(sigma[0]);
    // cout << array_size << endl;
    std::vector<int> sigma_vector ={sigma, sigma + array_size};
    std::vector<int> mark_vector ={mark, mark+array_size};
    std::vector<double> sigma0_vector ={sigma0, sigma0 + array_size};
    //print(sigma_vector.size());
    //print(mark_vector.size());
    // for(const auto& elem :sigma_vector){
    //     cout << elem << endl;
    // }
    return std::make_tuple(sigma_vector, mark_vector, sigma0_vector);
}

int main (int argc, char** argv){
    SetMystyle();  
    // gStyle->SetOptFit(1111);                                                        
    //set initial parmeters
    TString rootfile;
    string ROB_default = "1";
    string mode_default = "1";
    string CB_default = "1";
    for (int i = 0; i < argc; i++){
         if (strcmp(argv[i], "-rob") == 0)
         {
             ROB_default = argv[i + 1];
         }
         if (strcmp(argv[i], "-mode") == 0)
         {
             mode_default = argv[i + 1];
         }
         if (strcmp(argv[i], "-cb") == 0)
         {
             CB_default = argv[i + 1];
         }
    }

    TString ROB = ROB_default;
    TString CB = CB_default;
    TString mode = mode_default;

    int ROB_int = atoi(ROB_default.c_str());
    int mode_int = atoi(mode_default.c_str());
     // Call the function to format the number
    std::string formatted_ROB = formatNumber(ROB_int);
    // Output the formatted number
    // std::cout << "Formatted number: " << formatted_ROB << std::endl;
    
    TString inputfilename = "./CB"+ CB +"/ROB" + ROB  + "/Final_result_CB" + CB  + "_ROB"+ ROB +".txt";
    TString inputrootfile_ori = "../result_ANA/Result/CB" + CB + "/ROB" + ROB + "/CB" + CB + "_ROB" + ROB + "_final_result_mode_" + mode + ".root";
    cout << inputrootfile_ori << endl;
    TString inputrootfile_mod_path = "../result_Check/check/Result/";
    // std::tuple<std::vector<int>, std::vector<int>, std::vector<double>> arrays = returntwoarrays(inputfilename);
    auto result = returnThreeArrays(inputfilename);
    std::vector<int> Sigma = std::get<0>(result);
    std::vector<int> mark = std::get<1>(result);
    std::vector<double> sigma0 = std::get<2>(result);
    // print(Sigma.size());
    TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    canvas1->Print("CB"+ CB +"/ROB" + ROB + "/Final_result_CB" + CB + "_ROB" + ROB +".pdf[");
    gPad->SetLogy(); 
    for(int i = 0; i < Sigma.size(); i++){
        // cout <<i << "\t"<< Sigma[i] << "\t" << mark[i] << "\t" << sigma0[i] << endl;
        // Call the function to format the number
        std::string formatted_cn = formatNumber(i);
        // Output the formatted number
        // std::cout << "Formatted number: " << formatted_cn << std::endl;
        TString histname = Form("h_charge_ROB%s_ch%s_sigma_%d", formatted_ROB.data(), formatted_cn.data(), Sigma[i]);
        cout << histname << endl;
        TFile* inputroot;
        TString inputrootfile_mod;
        if (mark[i] == 1)
        {
            inputroot = new TFile( inputrootfile_ori, "READ");
            // histogram = (TH1F*)inputroot->Get(histname);
        }
        else{
            inputrootfile_mod = inputrootfile_mod_path + "fit_result_ROB_" + ROB + "_channel_" + i + ".root";
            cout << inputrootfile_mod << endl;
            inputroot =new TFile(inputrootfile_mod, "READ") ;
        }
        TH1F *histogram = (TH1F*)inputroot->Get(histname);
        histogram->SetLineWidth(2); // Set the line width to 2
        // histogram->SetLineColor(1); // Set the line width to 2
        if(mode_int == 1)
            {
                histogram->GetXaxis()->SetRangeUser(0, 200);
            }
        else
            {
                histogram->GetXaxis()->SetRangeUser(0, 1500);
            }
         // Sets logarithmic scale for the current pad
            // canvas1->cd();
            histogram->Draw();
            if (sigma0[i] > 8 && mark[i] == 2)
            {
                // Create a Gaussian function with specific parameters
                double * ped_gauss;
                double fitMin;
                ped_gauss = FitHistogramWithGaussian(inputrootfile_mod, histname, mode_int);
                cout << ped_gauss[0] << "========" << ped_gauss[1] << "========" << ped_gauss[2] <<"=================="<< ped_gauss[5] << "========" << ped_gauss[6] << endl;
                TF1 *gaussFunc = new TF1("gaussFunc", gaussian, ped_gauss[3],ped_gauss[4], 3);
                gaussFunc->SetParameters(ped_gauss[0]*15, ped_gauss[1], ped_gauss[2]); // Amplitude, mean, and sigma
                gaussFunc->SetLineColor(3);
                TF1 *fitFunction = histogram->GetFunction("func1");
                if(fitFunction){
                    cout << fitFunction->GetParameter(1) << "========" << fitFunction->GetParameter(3) << "========" << endl;
                    fitFunction->SetParameter(1, ped_gauss[1]);
                    fitFunction->SetParameter(3, ped_gauss[2]);
                    fitFunction->SetParError(1, ped_gauss[5]);
                    fitFunction->SetParError(3, ped_gauss[6]);
                
                
                }
                else{
                TF1 *fitFunction = histogram->GetFunction("func0");
                    cout << fitFunction->GetParameter(1) << "========" << fitFunction->GetParameter(3) << "========" << endl;
                    fitFunction->SetParameter(1, ped_gauss[1]);
                    fitFunction->SetParameter(3, ped_gauss[2]);
                    fitFunction->SetParError(1, ped_gauss[5]);
                    fitFunction->SetParError(3, ped_gauss[6]);
                
                }
                histogram->Draw();
                gaussFunc->Draw("same");
                // canvas1->Update();
            }
                
        canvas1->Print("CB"+ CB +"/ROB" + ROB + "/Final_result_CB" + CB + "_ROB" + ROB +".pdf");    
    }
    canvas1->Print("CB"+ CB +"/ROB" + ROB + "/Final_result_CB" + CB + "_ROB" + ROB +".pdf]");
    return 0;
}