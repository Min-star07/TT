#include <iostream>
#include <fstream>
#include <string>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TFitResult.h>
#include <TStopwatch.h>
#include <TLatex.h>
#include <TStyle.h>
#include <iomanip>
#include <fstream> // Required for file operations
#include "Mystyle.h"
#include "Bellamy.h"
#include "FitHistogramWithGaussian.h"
#include "GetXmax_hist.h"
#include "ChiSquare.h"
#include "Checkpath.h"
using namespace std;


int main(int argc, char** argv){
    //set initial parmeters
    string led_rootfile = "./Data/led_cCB-19_2023-11-10_10_50_hist.root";
    string ped_rootfile = "./Data/ped_cCB-19_2023-11-10_10_49_hist.root";
    string rob_id = "1";
    string channel_start = "0";
    string channel_end = "64";
    string sigma = "3";
    string mode = "1";
    string time = "2";
    string cb = "22";
    for (int i = 0; i < argc; i++)
    {
        if(strcmp(argv[i], "-mode") == 0){
            mode = argv[i+1];
        }
        if(strcmp(argv[i], "-led") == 0){
            led_rootfile = argv[i+1];
        }
        if(strcmp(argv[i], "-ped") == 0){
            ped_rootfile = argv[i+1];
        }
        if(strcmp(argv[i], "-ROB") == 0){
            rob_id = argv[i+1];
        }
        if(strcmp(argv[i], "-channel_start") == 0){
            channel_start = argv[i+1];
        }
        if(strcmp(argv[i], "-channel_end") == 0){
            channel_end = argv[i+1];
        }
        if(strcmp(argv[i], "-time") == 0){
            time = argv[i+1];
        }
        if(strcmp(argv[i], "-cb") == 0){
            cb = argv[i+1];
        }
    }

    //define canvas style
    SetMystyle();
    
    // Open the ROOT file containing the histogram
    TString filename_LED = led_rootfile;
    TString filename_PED = ped_rootfile;
    
    TString ROB_id = rob_id;
    TString mode_id = mode;
    int Chanel_start = atoi(channel_start.c_str());
    int Chanel_end = atoi(channel_end.c_str());
    int ROB_id_new = atoi(rob_id.c_str());
    int mode_new = atoi(mode.c_str());
    int times = atoi(time.c_str());
    int Sigma = -1;

    TFile *infile = new TFile(filename_LED, "READ");

    // Check if the file is opened successfully
    if (!infile || infile->IsZombie()) {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 0;
    }

    // const char* pathDir_create = "../../Result/CB22/ROB15";
    const char *str1 = "./Result/CB";
    const char *str2 = "/ROB";

    std::string result = std::string(str1) + std::string(cb) + std::string(str2) + std::string(rob_id);
    // // const char* CB = cb.c_str();
    // // const char* pathDir_create = "../../Result/CB" + CB + "/ROB15";
    const char* pathDir_create = result.c_str();
    // string pathDir = "../../Result/CB22/ROB15";
    string pathDir= result;
    Createpath (pathDir_create);
    
    TString outrootfilename =  pathDir + "/fit_result_ROB_" + ROB_id + "_mode_" + mode_id +".root";
    TFile *outfile_root = new TFile(outrootfilename, "RECREATE");
    // Open a file for writing
    ofstream outfile_txt;
    TString outfilename = pathDir   + "/fit_result_ROB_" + ROB_id  + "_mode_" + mode_id +".txt"; 

    outfile_txt.open(outfilename, ios::app);


    // Check if the file is opened successfully
    if (!outfile_txt.is_open()) {
        std::cerr << "Error opening the file!" << std::endl;
        return 0;
    }
    outfile_txt << "ROB" << "\t" << "Channel" << "\t" << "flag_fit_method" << "\t" << "flag_chi2" <<"\t" << "Chi2NDF"<< "\t"<<"ped_mean"<<"\t" << "ped_sigma"<< "\t" <<"ped_constant" << "\t" << "Sigma" << "\t" << "Min_x"<< "\t" << "Max_x" << "\t" << "N0" << "\t" << "Q_{0}" << "\t" << "Q_{1}" << "\t" << "#sigma_{0}"<< "\t" <<"#sigma_{1}" << "\t" <<"w" << "\t" << "#alpha"<< "\t" << "#mu" << "\t" << "err1" << "\t" << "err2" << "\t" << "err3" << "\t" << "err4" << "\t" << "err5" << "\t" << "err6" << "\t" << "err7" << "\t" << "err8"<< endl;
    
    while(Sigma < 4){
    for(int id = Chanel_start;id < Chanel_end; id ++){
    //for(int id = 7;id < 8; id ++){
    // Get the histogram from the file
    TString histname;
    if (ROB_id_new < 10)
    {
        if (id < 10)
            histname = "h_charge_ROB0" + ROB_id + "_ch0" + id;
        else
             histname = "h_charge_ROB0" + ROB_id + "_ch" + id;
    }
    else{
        if (id < 10)
            histname = "h_charge_ROB" + ROB_id + "_ch0" + id;
        else
            histname = "h_charge_ROB" + ROB_id + "_ch" + id;
    }
    cout << histname << endl;
    TH1F *histogram = (TH1F*)infile->Get(histname);
    TH1F *histogram1 = (TH1F*)infile->Get(histname);
    // histogram->GetXaxis()->SetRangeUser(0, 250);
    histogram->GetXaxis()->SetRangeUser(0, 1500);
    histogram->GetXaxis()->CenterTitle();
    histogram->GetYaxis()->CenterTitle();
    // Check if the histogram is retrieved successfully
    if (!histogram) {
        std::cerr << "Error: Unable to retrieve histogram!" << std::endl;
        infile->Close();
        return 0 ;
    }
    //prepare the dataset for fitting

    //2.define the fit initial parameters
    //2.1 get the initial of parameters of pedestral
    double * ped_gauss;
    double fitMin;
    ped_gauss = FitHistogramWithGaussian(filename_PED, histname, mode_new);
    cout << ped_gauss[0] << "========"<< ped_gauss[1]<< "========"<< ped_gauss[2] << endl;
    //2.2 set the fit range
    double mu_value;
    double q1_new;
    double sigma1_new;
    if (mode_new == 1)
    {

        fitMin = ped_gauss[0] - Sigma * ped_gauss[1]; // fit left range: mu - 3 * sigma
        mu_value = 1.0;
        q1_new = 12;
        sigma1_new = 5;
    }
   else{
        fitMin = ped_gauss[0]- Sigma * times; //fit left range: mu - 3 * sigma
        mu_value = 1.0;
        q1_new = 90;
        sigma1_new = 10;
   }
    double fitMax = Getxmax(histogram);
    // double fitMax = 200;
    //3.fit use atleastsquare and likelihood and select min chi2/ndf method as final result
    double chi2ndf_chi2, chi2ndf_likelihood;
    double *para_chi2, *para_likelihood;
    const double *chi2_error;
    const double *likelihood_error;
    int flag_fit_method = 0, flag_chi2 = 0;
    TF1 *func[2];
    for(int i = 0; i < 2; i++) { //0: least square 1:likelihood
        func[i] = new TF1(Form("func%d", i), Bellamy, fitMin, fitMax, 8);
        int entries_number = histogram->Integral();
        // func[i]->SetParameters(55000, ped_gauss[0], 12, ped_gauss[1], 10, 0.1, 0.2, 1.0);
        func[i]->SetParameters(entries_number, ped_gauss[0], q1_new, ped_gauss[1], sigma1_new, 0.1, 0.1, 1.0);
        // func[i]->SetParameters(entries_number, 20, 12, 1, 10, 0.1, 0.2, 0.5);
        func[i]->SetParNames("N_{0}","Q_{0}","Q_{1}", "#sigma_{0}","#sigma_{1}", "w","#alpha", "#mu");
        func[i]->FixParameter(0, entries_number);
        // func[i]->FixParameter(1, ped_gauss[0]);
        // func[i]->FixParameter(3, ped_gauss[1]);
        func[i]->SetRange(fitMin, fitMax);
        func[i]->SetNpx(500);
        if(i % 2 == 0){
            histogram->Fit(func[0], "R");
            func[0]->SetLineColor(4);
            chi2ndf_chi2 = func[0]->GetChisquare() / func[0]->GetNDF();
            }
        else{
            histogram1->Fit(func[1], "RL");
            func[1]->SetLineColor(2);
            chi2ndf_likelihood = func[1]->GetChisquare() / func[1]->GetNDF();
            }
    }
    // TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    // canvas1->cd();
    // gPad->SetLogy(); // Sets logarithmic scale for the current pad
    TString histname_new = histname + "_sigma_" + Sigma;
    if(chi2ndf_chi2 < chi2ndf_likelihood){        
            func[0]->SetRange(fitMin, fitMax);
            histogram->Fit(func[0], "R");
            outfile_root->cd();
            //Rename the histogram
            histogram->SetName(histname_new)  ;
            histogram->Write();
            chi2ndf_chi2 = func[0]->GetChisquare() / func[0]->GetNDF();
            // canvas1->SaveAs(Form("./ROB"+ ROB_id + "/charge_rob" + ROB_id + "_channel_%d" + "_sigma_" + Sigma+ ".pdf", id));
            flag_fit_method = 1;
            //save data
              if(chi2ndf_chi2 > 3){
              flag_chi2 = 1;
           }
        
        para_chi2 = func[0]->GetParameters();
        chi2_error = func[0]->GetParErrors();
        //CalculateChiSquare(histogram, fitMin, fitMax, para_chi2);
        outfile_txt << ROB_id << "\t" << id << "\t" << flag_fit_method << "\t" << flag_chi2 << "\t" << setprecision(5)<< chi2ndf_chi2 << "\t"<<ped_gauss[0] << "\t" << ped_gauss[1] << "\t" <<ped_gauss[2] << "\t" << Sigma << "\t" << fitMin << "\t" << fitMax ;
        for(int i = 0; i < 8; i++){
        outfile_txt << "\t" << para_chi2[i];
        }
        for(int i = 0; i < 8; i++){
        outfile_txt << "\t" << chi2_error[i];
        }
        }
    else{
        func[1]->SetRange(fitMin, fitMax);
        flag_fit_method = 2;
        histogram1->Fit(func[1], "RL");
        outfile_root->cd();
         //Rename the histogram
        histogram1->SetName(histname_new) ; 
        histogram1->Write();
        chi2ndf_likelihood = func[1]->GetChisquare() / func[1]->GetNDF();
        // canvas1->SaveAs(Form("./ROB"+ ROB_id + "/charge_rob" + ROB_id  +"_channel_%d" + "_sigma_" + Sigma + ".pdf", id));
        if(chi2ndf_likelihood > 3){
             flag_chi2 = 1;
           }
        //save data
        para_likelihood = func[1]->GetParameters();
        likelihood_error = func[1]->GetParErrors();
        //CalculateChiSquare(histogram, fitMin, fitMax, para_likelihood);
        outfile_txt << ROB_id << "\t" << id << "\t" << flag_fit_method << "\t" << flag_chi2 << "\t" << setprecision(5)<< chi2ndf_likelihood << "\t"<<ped_gauss[0] << "\t" << ped_gauss[1]<< "\t" <<Sigma<< "\t" << fitMin << "\t" << fitMax ;
        for(int i = 0; i < 8; i++){
        outfile_txt << "\t" << para_likelihood[i];
        }
        for(int i = 0; i < 8; i++){
        outfile_txt << "\t" << likelihood_error[i];
        }
        }
    outfile_txt << endl;  
   }
   Sigma ++;
}
    outfile_root->Close();
    infile->Close();
    outfile_txt.close();
return 0;
}
