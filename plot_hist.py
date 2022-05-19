import ROOT
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
canvas.cd()

f_higgs = ROOT.TFile("higgs.root", "READ")
f_bg = ROOT.TFile("background.root", "READ")

hist = f_higgs.Get("m4l Higgs")

hist.SetLineColor(ROOT.kBlack)
hist.SetLineWidth(2)          
hist.SetFillColor(ROOT.kViolet)
hist.GetXaxis().SetTitle('m4l [MeV]')
hist.GetYaxis().SetTitle('events [normalised]')
hist.Draw("HIST")
hist.Draw("same HIST")
canvas.Draw()

canvas.Print("histogram_m4l_new.jpg")
