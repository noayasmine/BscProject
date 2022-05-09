import ROOT
import numpy as np

# opening root file
f = ROOT.TFile.Open("/data/atlas/users/mvozak/opendata/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root")

# Define a 'canvas' on which to draw a histogram. Its name is "canvas" and its header is "plot a variable". The two following arguments define the width and the height of the canvas.
#canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
#canvas.cd()

# Here we define a tree named "tree" to extract the data from the input .root file.
tree = f.Get("mini")
lumi_data = 4.8 #fb ^-1
number_entries = tree.GetEntries()
print "Number of entries in the tree = ", number_entries


def plot_m4l(tree, lumi_data, number_entries, scaling=False):
    canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
    canvas.cd()
    hist = ROOT.TH1F("tryout","tryout plot m4l",20,50000,150000)

    all_m4l = []

    for event in tree:
        E4l_squared = np.sum(tree.lep_E) ** 2
        px = tree.lep_pt * np.cos(tree.lep_phi)
        py = tree.lep_pt * np.sin(tree.lep_phi)
        pz = tree.lep_pt * np.sinh(tree.lep_eta)

        p4l_squared = np.sum(px) ** 2 + np.sum(py) ** 2 + np.sum(pz) ** 2

        m4l = (E4l_squared - p4l_squared) ** 0.5

        all_m4l.append(m4l)

        if scaling == False:
            hist.Fill(m4l)

        if scaling == True:
            hist.Fill(m4l, tree.mcWeight)
            #scaling = tree.XSection * 1000 * lumi_data * tree.mcWeight * 1/number_entries
            #hist.Fill(m4l, scaling)
            print(tree.mcWeight)

    print('mean is {}'.format(np.mean(all_m4l)))
    print('std is {}'.format(np.std(all_m4l)))


    print "Histogram is filled"


    # Now want to draw the histogram, and set the fill colour
    hist.SetLineColor(ROOT.kBlack) 
    hist.SetLineWidth(2) 
    hist.SetFillColor(ROOT.kAzure)
    hist.Draw("HIST")

    # Draw the canvas, which contains the histogram
    canvas.Update()

    # The following lines allow the canvas to be displayed, 
    #	until you press enter in the command line.
    try:
        __IPYTHON__
    except:
        raw_input('Press Enter to exit')

    # Next we can also normalise the histogram (so the integral is 1), to allow us to see the proportions. By doing this, you can directly read of the y-axis what fraction of events fall into each bin. 
    scale = hist.Integral()
    hist.Scale(1/scale)

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
        print('here')
        canvas.Print("my_hist_m4l_scaling.jpg")

    try:
        __IPYTHON__
    except:
        raw_input('Press Enter to exit')


plot_m4l(tree, lumi_data, number_entries, scaling=True)
