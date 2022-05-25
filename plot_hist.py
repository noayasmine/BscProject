import ROOT
from ROOT import gROOT
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#MC_files = [ROOT.TFile("higgs.root", "READ"), ROOT.TFile("background.root", "READ")]
f_higgs = ROOT.TFile("higgs.root", "READ")
f_bg = ROOT.TFile("background.root", "READ")
f_dataA = ROOT.TFile("data_A.root", "READ")
f_dataB = ROOT.TFile("data_B.root", "READ")

hist_higgs = f_higgs.Get("higgs_hist")
hist_bg = f_bg.Get("bg_hist")
hist_data = f_dataA.Get("dataA_hist")
hist_dataB = f_dataB.Get("dataB_hist")
#hist.ClassName()

canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
canvas.cd()

hist_higgs.SetLineColor(ROOT.kBlack)
hist_higgs.SetLineWidth(2)       
hist_higgs.Rebin(20) 
hist_higgs.SetFillColor(ROOT.kViolet)
hist_higgs.GetXaxis().SetTitle('m4l [MeV]')
hist_higgs.GetYaxis().SetTitle('events [normalised]')
#hist_higgs.Draw("HIST")

hist_bg.Rebin(20)
hist_bg.Draw("HIST")

hist_data.Rebin(20)

hist_higgs.Draw("SAME HIST")


#stacked = ROOT.THStack('one', 'two')
#stacked.Add(hist_higgs)
#stacked.Add(hist_bg)
#stacked.Draw("HIST")
hist_data.Draw("SAME P*")
canvas.Draw()

canvas.Print("histogram_m4l_stacked.jpg")


