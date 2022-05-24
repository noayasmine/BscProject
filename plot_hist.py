import ROOT
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
canvas.cd()

f_higgs = ROOT.TFile("higgs.root", "READ")
f_bg = ROOT.TFile("background.root", "READ")
f_dataA = ROOT.TFile("data_A.root", "READ")

hist_higgs = f_higgs.Get("higgs_hist")
hist_bg = f_bg.Get("bg_hist")
hist_data = f_bg.Get("dataA_hist")
#hist.ClassName()

hist_higgs.SetLineColor(ROOT.kBlack)
hist_higgs.SetLineWidth(2)          
hist_higgs.SetFillColor(ROOT.kViolet)
hist_higgs.GetXaxis().SetTitle('m4l [MeV]')
hist_higgs.GetYaxis().SetTitle('events [normalised]')
hist_higgs.Draw("HIST")
hist_bg.Draw("same HIST")
hist_data.Draw("same HIST")
canvas.Draw()

canvas.Print("histogram_m4l_new3.jpg")
