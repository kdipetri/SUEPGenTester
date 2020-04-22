import ROOT
from DataFormats.FWLite import Events, Handle
import sys

ROOT.gROOT.SetBatch(True)

def getSample(f):
    # mScalar, mPion, T
    name = f.strip("HepMC_GEN_").strip(".root")
    return name
    
def eventdisplay(ievt,sample,particles):
    disp = ROOT.TH2F("h_display_{}_evt{}".format(sample,ievt),";eta;phi;pt",100,-3.5,3.5,100,-3.5,3.5)
    for part in particles:
        if part.status() is not 1 : continue
        if part.charge() is 0 : continue
        if abs(part.eta() > 2.5) : continue
        if part.pt() < 1 : continue
        disp.Fill(part.eta(),part.phi(),part.pt())

    c = ROOT.TCanvas()
    disp.Draw("BOX")
    c.Print("plots/eventdisplays/{}_evt{}.png".format(sample,ievt))
    
    
def loop(f,sample):

    # get events
    events = Events( "inputs/"+f )
    
    # create handles and labels outside of loop
    handle  = Handle ('std::vector<reco::GenParticle>')
    label = ("genParticles")
    
    # for plotting 
    fout = ROOT.TFile.Open("outputs/hist_{}.root".format(sample),"RECREATE")
    
    h_charged_pt    = ROOT.TH1F("h_charged_pt"    ,";track pt [GeV]"        ,100,0,10)
    h_ncharged      = ROOT.TH1F("h_ncharged"      ,";n tracks"              ,100,0,2000)
    h_ncharged_pt0p1= ROOT.TH1F("h_ncharged_pt0p1",";n tracks pt > 0.1 GeV" ,100,0,2000)
    h_ncharged_pt0p5= ROOT.TH1F("h_ncharged_pt0p5",";n tracks pt > 0.5 GeV" ,100,0,1000)
    h_ncharged_pt1  = ROOT.TH1F("h_ncharged_pt1"  ,";n tracks pt > 1 GeV"   ,100,0,300)
    h_ncharged_pt2  = ROOT.TH1F("h_ncharged_pt2"  ,";n tracks pt > 2 GeV"   ,100,0,150)
    h_ncharged_pt10 = ROOT.TH1F("h_ncharged_pt10" ,";n tracks pt > 10 GeV"  ,100,0,10)
    
    # loop over events
    ievt = 0
    for event in events:
        #print(ievt)
        #if ievt > 10: break 
    
        # use getByLabel, just like in cmsRun
        event.getByLabel (label, handle)
    
        # get the product
        particles = handle.product()
        
        if ievt < 10: eventdisplay(ievt,sample,particles) 

        ncharged = 0
        ncharged_pt0p1 = 0 
        ncharged_pt0p5 = 0 
        ncharged_pt1   = 0 
        ncharged_pt10  = 0 
        for i,part in enumerate(particles): 
            #print(part.pt())
        
            if part.status() is not 1 : continue
            if part.charge() is 0 : continue
            if abs(part.eta() > 2.5) : continue
    
            h_charged_pt.Fill(part.pt())
    
            ncharged+=1
            if part.pt() > 0.1: ncharged_pt0p1 += 1 
            if part.pt() > 0.5: ncharged_pt0p5 += 1 
            if part.pt() > 1  : ncharged_pt1   += 1 
            if part.pt() > 10 : ncharged_pt10  += 1 
                
    
        h_ncharged.Fill(ncharged)
        h_ncharged_pt0p1.Fill(ncharged_pt0p1 ) 
        h_ncharged_pt0p5.Fill(ncharged_pt0p5 ) 
        h_ncharged_pt1  .Fill(ncharged_pt1   ) 
        h_ncharged_pt10 .Fill(ncharged_pt10  ) 
    
        ievt+=1

    fout.cd()
    h_charged_pt    .Write()
    h_ncharged_pt0p1.Write()
    h_ncharged_pt0p5.Write()
    h_ncharged_pt1  .Write()
    h_ncharged_pt10 .Write()
    h_ncharged.Write()
    return

def draw1D(hist):
    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/hists/{}.png".format(hist.GetName()))

def dump_histos(sample):
    f = ROOT.TFile.Open("outputs/hist_{}.root".format(sample))
    histos = []
    histos.append("h_charged_pt")
    histos.append("h_ncharged")
    histos.append("h_ncharged_pt0p1")
    histos.append("h_ncharged_pt0p5")
    histos.append("h_ncharged_pt1")
    histos.append("h_ncharged_pt10")
    for histname in histos:
        hist = f.Get(histname)
        draw1D(hist)
    return
    
def main():
    if len(sys.argv) > 1:  f = sys.argv[1]
    #else : f = "HepMC_GEN_400_2p0_2p0.root" 
    else : f = "HepMC_GEN_400_2p0_2p0.root" 
    #else : f = "HepMC_GEN_400_2p0_2p0.root" 

    sample = getSample(f)
    loop(f,sample) 
    dump_histos(sample)

if __name__ == "__main__":
    main()
