#ifndef HISTOGRAMMANAGER_H
#define HISTOGRAMMANAGER_H

#include "TH1.h"
#include "TFile.h"
#include <vector>
#include <string>

class HistogramManager {
public:
    HistogramManager(TString filename);
    ~HistogramManager();
    void addHistogram(TH1* hist);
    void saveHistograms();

private:
    TFile* m_file;
    std::vector<TH1*> m_histograms;
};

#endif
