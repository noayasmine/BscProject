import ROOT
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# opening root file

rootfiles = ["/data/atlas/users/mvozak/opendata/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root", "/data/atlas/users/mvozak/opendata/4lep/MC/mc_363490.llll.4lep.root", \
"/data/atlas/users/mvozak/opendata/4lep/Data/data_A.4lep.root"]

lumi_data = 10 #fb ^-1

def calc_m4l(lep_E, lep_phi, lep_eta, lep_pt):
    E4l_squared = np.sum(lep_E) ** 2
    px = lep_pt * np.cos(lep_phi)
    py = lep_pt * np.sin(lep_phi)
    pz = lep_pt * np.sinh(lep_eta)

    p4l_squared = np.sum(px) ** 2 + np.sum(py) ** 2 + np.sum(pz) ** 2

    return (E4l_squared - p4l_squared) ** 0.5


def plot_m4l(tree, lumi_data, filename, histname, scaling=False):
    """ 
    Function to plot a histogram of invariant mass of Higgs boson via 4 lepton measurements (m4l)

    Input: 
        tree: tree object from ROOT file
        lumi_data: luminosity of the actual data [fb^-1]
        filename: name of root file (.root at the end)
        histname: name of histogram in the root file
        scaling: set True for scaling and False for no scaling

    Output:
        function generates histogram and saves it under filename

    """

    # Define a 'canvas' on which to draw a histogram. Its name is "canvas" and its header is "plot a variable". 
    # The two following arguments define the width and the height of the canvas.
    canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
    canvas.cd()

    hist = ROOT.TH1F(histname,"plot m4l Higgs",1000,50000,700000)

    for event in tree:
        m4l = calc_m4l(tree.lep_E, tree.lep_phi, tree.lep_eta, tree.lep_pt)
        #print(m4l)
        # filling histogram with unweighted data
        if scaling == False:
            print(m4l)
            hist.Fill(m4l)

        # filling histogram with weighted data
        if scaling == True:
            finalmcWeight = tree.XSection * 1000 * lumi_data * tree.mcWeight * 1/tree.SumWeights
            hist.Fill(m4l, finalmcWeight)

    print "Histogram is filled"

    # Next we can also normalise the histogram (so the integral is 1), to allow us to see the proportions. 
    # By doing this, you can directly read of the y-axis what fraction of events fall into each bin. 
    scale = hist.Integral()

    #hist.Scale(1/scale)

    f = ROOT.TFile.Open(filename, "RECREATE")
    f.cd()
    hist.Write()


def find_pair(tree):
    """ 
    Function that looks for lepton pairs in the 2Z -> 4l process

    Input: ROOT tree
    Output: list with m2l of lepton pairs

    Comment: In the data there are some cases which do not make sense (for example 3x positive charge).
    These cases are not taken into account and their masses are not added to the m2l list.

    """

    canvas = ROOT.TCanvas("canvas","plot a variable",800,400)
    canvas.Divide(2,1)
    
    hist = ROOT.TH1F("m2l [MeV]","plot m2l",100,1000,100000)
    hist_2d = ROOT.TH2F("m2l 2d","plot m2l",100,1000,100000,100,1000,100000)

    checkpair = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    m2l_total = []
    mass_Z = 91000 # MeV

    for event in tree:
        E = tree.lep_E
        px = tree.lep_pt * np.cos(tree.lep_phi)
        py = tree.lep_pt * np.sin(tree.lep_phi)
        pz = tree.lep_pt * np.sinh(tree.lep_eta)
        m2ls_per_event = []
        pairs_found = []

        # find pairs based on charge and lepton type
        for i,j in checkpair: 
            if tree.lep_charge[i] == - tree.lep_charge[j] and tree.lep_type[i] == tree.lep_type[j]:
                pairs_found.append([i,j])
                m2l = ((E[i] + E[j]) ** 2 - ((px[i] + px[j]) ** 2 + (py[i] + py[j]) ** 2 + (pz[i] + pz[j]) ** 2)) ** 0.5
                m2ls_per_event.append(m2l)

        other_pair = [0,1,2,3]
        # filter based on m4l closest to m(Z-boson) in the case 4l = 4e or 4l = 4mu
        if len(pairs_found) >= 3:
            smallest = 100000
            pair = []
            m2l = 0

            for i in range(len(pairs_found)):
                abs_diff = np.abs(mass_Z - m2ls_per_event[i])

                if abs_diff < smallest:
                    pair = pairs_found[i]
                    m2l = m2ls_per_event[i]
            
            other_pair.remove(pair[0])
            other_pair.remove(pair[1])

            if other_pair in pairs_found:
                index = pairs_found.index(other_pair)
                pairs_found = [pair, other_pair]
                m2l_total.append(m2l)
                m2l_total.append(m2ls_per_event[index])
                hist.Fill(m2l)
                hist.Fill(m2ls_per_event[index])
                hist_2d.Fill(m2l, m2ls_per_event[index])

        if len(m2ls_per_event) == 2:
            m2l_total.append(m2ls_per_event[0])
            m2l_total.append(m2ls_per_event[1])
            hist_2d.Fill(m2ls_per_event[0], m2ls_per_event[1])
            hist.Fill(m2ls_per_event[0])
            hist.Fill(m2ls_per_event[1])

    print "Histogram is filled"

    # Now want to draw the histogram, and set the fill colour
    hist.SetLineColor(ROOT.kBlack) 
    hist.SetLineWidth(2) 
    hist.SetFillColor(ROOT.kAzure)

    hist_2d.SetLineColor(ROOT.kBlack) 
    hist_2d.SetLineWidth(2) 
    hist_2d.SetFillColor(ROOT.kAzure)

    # Draw the canvas, which contains the histogram
    #canvas.Update()

    # Set some new colour settings for the histogram
    #hist.SetLineColor(ROOT.kBlack)
    #hist.SetLineWidth(2)          
    #hist.SetFillColor(ROOT.kViolet)

    # Again we re-draw the histogram and canvas. 
    canvas.cd(1)
    hist.Draw("HIST")

    canvas.cd(2)
    hist_2d.Draw("colz")

    canvas.Draw()

    canvas.Print("my_hist_m2l.jpg")

    return m2l_total


#m2ls = np.array(find_pair(tree_H))
#print('mean = {} +- {}'.format(np.mean(m2ls), np.std(m2ls)))

filenames = ['higgs.root', 'background.root', 'data_A.root']
histnames = ['higgs_hist', 'bg_hist', 'dataA_hist']
scaling = [True, True, False]
i = 0

for rootfilename in rootfiles:
    f = ROOT.TFile.Open(rootfilename)
    tree = f.Get("mini")
    plot_m4l(tree, lumi_data, filenames[i], histnames[i], scaling=scaling[i])

    i += 1


