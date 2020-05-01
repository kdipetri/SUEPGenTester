import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)


def get1D(mMed,mDark,temp,decay,histname):
    filename = "outputs/hist_mMed-{}_mDark-{}_temp-{}_decay-{}.root".format(mMed,mDark,temp,decay)
    #print(filename)
    f = ROOT.TFile.Open(filename)
    hist = f.Get(histname)
    hist.SetDirectory(0)
    #print(hist)
    return hist

def compare1D(hists,labels,filename):
    c = ROOT.TCanvas(filename,"",800,800)
    ymax = 0
    leg = ROOT.TLegend(0.5,0.7,0.86,0.86)
    for i,hist in enumerate(hists): 
        if i==0: hist.Draw("hist")
        else : hist.Draw("hist same")
        if hist.GetMaximum() > ymax: ymax=hist.GetMaximum()

        leg.AddEntry(hist,labels[i],"l")

    hists[0].SetMaximum(ymax*1.3)
    leg.Draw()
    
    c.Print("plots/{}.png".format(filename))

def compareMass():
    mMeds = []
    mMeds.append(125)
    mMeds.append(405)
    mMeds.append(750)
    mMeds.append(1000)
    temp = 2
    mDark = 2
    decay = "darkPhoHad"

    histname = "h_met_soft" 

    hists = []
    labels = []
    for mMed in mMeds:
        hists.append(get1D(mMed,mDark,temp,decay,histname))
        label = "m_{mMed}=%i GeV,%s"%(mMed,decay)
        labels.append(label)

    
    compare1D(hists,labels,"compare_mMed/"+histname)

compareMass()
