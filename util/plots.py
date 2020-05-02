import ROOT
from plothelper import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)

one   = ROOT.TColor(2001,92 /255.,39 /255.,81 /255.,"darkPurple")#dark purple
two   = ROOT.TColor(2002,119/255.,133/255.,172/255.,"blahBlue")#blue
three = ROOT.TColor(2003,229/255.,107/255.,111/255.,"pinkRed")#pink-red
four  = ROOT.TColor(2004,247/255.,178/255.,103/255.,"orange")#orange
five  = ROOT.TColor(2005,42 /255.,157/255.,143/255.,"PersianGreen")# persian green
six   = ROOT.TColor(2006,38 /255.,70 /255.,83 /255.,"Charcol")# charcol
eight = ROOT.TColor(2008,233/255.,196/255.,106/255.,"Maize")# maize
nine  = ROOT.TColor(2009,244/255.,162/255.,97 /255.,"SandyBrown")# sandy brown
ten   = ROOT.TColor(2010,231/255.,111/255.,81 /255.,"TerraCotta")# terra cotta
#five  = ROOT.TColor(2005,103/255.,155/255.,94 /255.,"Green")#green
colors = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010]
setStyle()

def get1D(mMed,mDark,temp,decay,histname):

    # Get hist
    filename = "outputs/hist_mMed-{}_mDark-{}_temp-{}_decay-{}.root".format(mMed,mDark,temp,decay)
    f = ROOT.TFile.Open(filename)
    hist = f.Get(histname)

    # Clean
    hist.SetLineWidth(2)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetXaxis().SetNdivisions(505)
    hist.SetDirectory(0)

    return hist

def compare1D(hists,labels,filename):
    c = ROOT.TCanvas(filename,"",800,800)

    dy = 0.06*len(hists)
    leg = ROOT.TLegend(0.25,0.86-dy,0.86,0.86)
    leg.SetTextSize(0.045)
    leg.SetBorderSize(0)

    ymax = 0
    for i,hist in enumerate(hists): 
        hist.SetLineColor(colors[i])
        if i==0: hist.Draw("hist")
        else : hist.Draw("hist same")
        if hist.GetMaximum() > ymax: ymax=hist.GetMaximum()

        leg.AddEntry(hist,labels[i],"l")

    hists[0].SetMaximum(ymax*1.4)

    leg.Draw()
    
    c.Print("plots/{}.png".format(filename))

def compareMass(temp,mDark,decay,histname):
    mMeds = []
    mMeds.append(125)
    mMeds.append(405)
    mMeds.append(750)
    mMeds.append(1000)

    hists = []
    labels = []
    for mMed in mMeds:
        hists.append(get1D(mMed,mDark,temp,decay,histname))
        label = "m_{Med}=%i GeV,%s"%(mMed,decay)
        labels.append(label)
    
    compare1D(hists,labels,"compare_mMed/temp{}_mDark{}_decay_{}_{}".format(temp,mDark,decay,histname))

def compareDecay(mMed,temp,mDark,histname):
    decays = []
    decays.append("darkPho")
    decays.append("darkPhoHad")
    decays.append("generic")

    hists = []
    labels = []
    for decay in decays:
        hists.append(get1D(mMed,mDark,temp,decay,histname))
        label = "m_{mMed}=%i GeV,%s"%(mMed,decay)
        labels.append(label)
    
    compare1D(hists,labels,"compare_decay/mMed{}_temp{}_mDark{}_{}".format(mMed,temp,mDark,histname))


dists=[]
dists.append("h_ncharged_pt0p1")	
dists.append("h_ncharged")	
dists.append("h_ncharged_pt0p5")	
dists.append("h_met_nu")	
dists.append("h_dmeson_phi")	
dists.append("h_dphoton_phi")	
dists.append("h_scalar_pt")	
dists.append("h_charged_pt")	
dists.append("h_dmeson_pt")	
dists.append("h_n_dark_mesons")	
dists.append("h_met_soft")	
dists.append("h_ncharged_pt1")	
dists.append("h_dmeson_m")	
dists.append("h_dphoton_pt")	
dists.append("h_dphoton_eta")	
dists.append("h_scalar_m")	
dists.append("h_n_dark_photons")	
dists.append("h_ncharged_pt10")	
dists.append("h_dphoton_m")	
dists.append("h_dmeson_eta")	
dists.append("h_scalar_eta")	
dists.append("h_scalar_phi")

for dist in dists:
    compareMass(2,2,"darkPho",dist)
    compareMass(2,2,"darkPhoHad",dist)
    compareMass(2,2,"generic",dist)
    compareDecay(750,2,2,dist)
