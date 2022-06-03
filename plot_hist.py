import ROOT
from ROOT import gROOT
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


MC_files = [ROOT.TFile("higgs.root", "READ"), ROOT.TFile("background.root", "READ")]
data_files = [ROOT.TFile("data_A.root", "READ"), ROOT.TFile("data_B.root", "READ"), ROOT.TFile("data_C.root", "READ"), ROOT.TFile("data_D.root", "READ")]
histnames = ['higgs_hist', 'bg_hist', 'dataA_hist', 'dataB_hist', 'dataC_hist', 'dataD_hist']

hists = []
i = 0
for file in MC_files:
    hists.append(file.Get(histnames[i]))
    i += 1

for file in data_files:
    hists.append(file.Get(histnames[i]))
    i += 1

for hist in hists:
    hist.Rebin(50)
    hist.SetLineColor(ROOT.kBlack)
    hist.SetLineWidth(2)
    hist.SetFillColor(ROOT.kViolet)

hists[0].GetYaxis().SetTitle('events [normalised]')
hists[0].GetXaxis().SetTitle('m4l [MeV]')

MC_stack = ROOT.THStack("stacked", "stacked MC and data")
for hist in hists[0:2]:
    MC_stack.Add(hist)

data_stack = ROOT.THStack("stacked data", "stacked data")
for hist in hists[2:]:
    data_stack.Add(hist)

canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
canvas.cd()

MC_stack.Draw("HIST")
data_stack.Draw("SAME P*")
canvas.Draw()

canvas.Print("histogram_m4l_stacked.jpg")
