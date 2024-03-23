#include "HistogramManager.h"

// HistogramManager::HistogramManager(const std::string& filename) {
//     m_file = new TFile(filename.c_str(), "RECREATE");
// }
HistogramManager::HistogramManager(TString filename) {
    m_file = new TFile(filename, "RECREATE");
}

HistogramManager::~HistogramManager() {
    delete m_file;
}

void HistogramManager::addHistogram(TH1* hist) {
    m_histograms.push_back(hist);
}

void HistogramManager::saveHistograms() {
    m_file->cd();
    for (auto hist : m_histograms) {
        hist->Write();
    }
}
