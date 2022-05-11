import ROOT
import numpy as np

# opening root file
f = ROOT.TFile.Open("/data/atlas/users/mvozak/opendata/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root")

# Here we define a tree named "tree" to extract the data from the input .root file.
tree = f.Get("mini")
lumi_data = 10 #fb ^-1
number_entries = tree.GetEntries()
print "Number of entries in the tree = ", number_entries


def plot_m4l(tree, lumi_data, number_entries, scaling=False):
    """ Function to plot a histogram of invariant mass of Higgs boson via 4 lepton measurements (m4l)
    Input: 
        tree: tree object from ROOT file
        lumi_data: luminosity of the actual data [fb^-1]
        number_entries: number of entries of the generated MC data
        scaling: set True for scaling and False for no scaling

    Output:
        saved file named my_hist_m4l.jpg (no scaling) or my_hist_m4l_scaled.jpg (with scaling)

    """

    # Define a 'canvas' on which to draw a histogram. Its name is "canvas" and its header is "plot a variable". 
    # The two following arguments define the width and the height of the canvas.
    canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
    canvas.cd()

    hist = ROOT.TH1F("tryout","tryout plot m4l",10,50000,150000)

    all_m4l = []

    for event in tree:
        E4l_squared = np.sum(tree.lep_E) ** 2
        px = tree.lep_pt * np.cos(tree.lep_phi)
        py = tree.lep_pt * np.sin(tree.lep_phi)
        pz = tree.lep_pt * np.sinh(tree.lep_eta)

        p4l_squared = np.sum(px) ** 2 + np.sum(py) ** 2 + np.sum(pz) ** 2

        m4l = (E4l_squared - p4l_squared) ** 0.5

        all_m4l.append(m4l)

        # filling histogram with unweighted data
        if scaling == False:
            hist.Fill(m4l)

        # filling histogram with weighted data
        if scaling == True:

            #finalmcWeight = tree.XSection * 1000 * lumi_data * tree.mcWeight * 1/number_entries
            finalmcWeight = tree.XSection * 1000 * lumi_data * tree.mcWeight * 1/tree.SumWeights
            hist.Fill(m4l, finalmcWeight)

    print "Histogram is filled"

    # Now want to draw the histogram, and set the fill colour
    hist.SetLineColor(ROOT.kBlack) 
    hist.SetLineWidth(2) 
    hist.SetFillColor(ROOT.kAzure)
    hist.Draw("HIST")

    # Draw the canvas, which contains the histogram
    canvas.Update()

    # Next we can also normalise the histogram (so the integral is 1), to allow us to see the proportions. 
    # By doing this, you can directly read of the y-axis what fraction of events fall into each bin. 
    if scaling == False:
        scale = hist.Integral()

    if scaling == True:
        scale = 1
        #scale = tree.SumWeights
        #print('sum of weights = {}'.format(scale))
        #print('integral = {}'.format(hist.Integral()))

    hist.Scale(1/scale)

    print('The scale is {}'.format(scale))

    # Set some new colour settings for the histogram
    hist.SetLineColor(ROOT.kBlack)
    hist.SetLineWidth(2)          
    hist.SetFillColor(ROOT.kViolet)

    # Again we re-draw the histogram and canvas. 
    hist.Draw("HIST")
    canvas.Draw()

    if scaling == False:
        canvas.Print("my_hist_m4l.jpg")
    
    if scaling == True:
        canvas.Print("my_hist_m4l_scaled.jpg")

    try:
        __IPYTHON__
    except:
        raw_input('Press Enter to exit')




def find_pair(tree):
    checkpair = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    m2l = []

    for event in tree:
        E = tree.lep_E
        px = tree.lep_pt * np.cos(tree.lep_phi)
        py = tree.lep_pt * np.sin(tree.lep_phi)
        pz = tree.lep_pt * np.sinh(tree.lep_eta)

        for i,j in checkpair: 
            print(i,j)

            if tree.lep_charge[i] == - tree.lep_charge[j] and tree.lep_type[i] == tree.lep_type[j]:
                print('pair found')
                m2l = ((E[i] + E[j]) ** 2 - ((px[i] + px[j]) ** 2 + (py[i] + py[j]) ** 2 + (pz[i] + pz[j]) ** 2)) ** 0.5
                m2l_total.append(m2l)
                print(m2l)
                print(tree.lep_type[i], tree.lep_type[j])
                print(tree.lep_charge[i], tree.lep_charge[j])



#find_pair(tree)

plot_m4l(tree, lumi_data, number_entries, scaling=True)
