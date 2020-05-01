import ROOT
from DataFormats.FWLite import Events, Handle
from plothelper import *
import sys
import time


def getSample(f):
    # mScalar, mPion, T
    f = f.replace("step1_","")
    f = f.replace("_13TeV-pythia8_n-10000_part-1.root","")
    return f 

def isNeutrino(part):
    if abs(part.eta() > 5.0 ) : return False
    elif abs(part.pdgId()) == 12 : return True
    elif abs(part.pdgId()) == 14 : return True
    elif abs(part.pdgId()) == 16 : return True
    else : return False

def isInvisible(part):
    # https://github.com/cms-sw/cmssw/blob/703f4fc1732e0410acad217a4acc70c739a8741e/RecoMET/METAlgorithms/src/GenSpecificAlgo.cc
    # https://github.com/cms-sw/cmssw/blob/703f4fc1732e0410acad217a4acc70c739a8741e/RecoMET/METProducers/python/genMetCalo_cfi.py
    # doesn't have a pT threshold...

    if abs(part.eta() > 5.0 ) : return False
    elif isNeutrino(part) : return True
    elif part.pt() < 0.7 : return True # guessing based on need to reach calo for charged and cal thresholds. can change, do eta dependent charged dependent etc
    # (Particles with a pT between 200 and 700 MeV never reach the calorimeter barrel, but follow a helical trajectory to one of the calorimeter endcaps.) 
    else : return False
    
def loop(f,sample):

    # get events
    events = Events( f )
    
    # create handles and labels outside of loop
    handle  = Handle ('std::vector<reco::GenParticle>')
    label = ("genParticles")
    
    # loop over events
    ievt = 0
    for event in events:
        
        # for debug
        #print(ievt)
        if ievt > 1000: break 

        if ievt%10==0 : print(ievt)
    
        # use getByLabel, just like in cmsRun
        event.getByLabel (label, handle)
    
        # get the product
        particles = handle.product()
       
        ncharged = 0
        ncharged_pt0p1 = 0 
        ncharged_pt0p5 = 0 
        ncharged_pt1   = 0 
        ncharged_pt10  = 0 

        n_dark_mes = 0
        n_dark_pho = 0

        met_vector_nu   = ROOT.TLorentzVector()
        met_vector_soft = ROOT.TLorentzVector()
        p4 = ROOT.TLorentzVector()
        for i,part in enumerate(particles): 

            # 
            # Truth Particles 
            # 
            if part.pdgId() == 25 and part.status() == 62: # found scalar
                plot1D("h_scalar_m"   ,";scalar m [GeV]"    ,part.mass() ,100,0,1200)
                plot1D("h_scalar_pt"  ,";scalar pT [GeV]"   ,part.pt()   ,100,0,500)
                plot1D("h_scalar_eta" ,";scalar eta"        ,part.eta()  ,100,-3.5,3.5)
                plot1D("h_scalar_phi" ,";scalar phi"        ,part.phi()  ,100,-3.5,3.5)
            elif part.pdgId() == 999999 : # found meson
                plot1D("h_dmeson_m"   ,";meson m [GeV]"    ,part.mass()  ,100,0,20)
                plot1D("h_dmeson_pt"  ,";meson pT [GeV]"   ,part.pt()    ,100,0,20)
                plot1D("h_dmeson_eta" ,";meson eta"        ,part.eta()   ,100,-3.5,3.5)
                plot1D("h_dmeson_phi" ,";meson phi"        ,part.phi()   ,100,-3.5,3.5)
                n_dark_mes+=1
            elif part.pdgId() == 999998 : # found dark photon
                plot1D("h_dphoton_m"   ,";photon m [GeV]"    ,part.mass()  ,100,0,20)
                plot1D("h_dphoton_pt"  ,";photon pT [GeV]"   ,part.pt()    ,100,0,20)
                plot1D("h_dphoton_eta" ,";photon eta"        ,part.eta()   ,100,-3.5,3.5)
                plot1D("h_dphoton_phi" ,";photon phi"        ,part.phi()   ,100,-3.5,3.5)
                n_dark_pho+=1
            #else : continue
     

            # 
            # met... 
            # 
            if part.status() is not 1 : continue
            if isInvisible(part) : 
                p4.SetPtEtaPhiM(part.pt(),part.eta(),part.phi(),part.mass())
                met_vector_soft += p4
            if isNeutrino(part) : 
                p4.SetPtEtaPhiM(part.pt(),part.eta(),part.phi(),part.mass())
                met_vector_nu += p4

            #
            # truth track selection 
            #
            if part.charge() is 0 : continue
            if abs(part.eta() > 2.5) : continue
        
            plot1D("h_charged_pt" ,";track pt [GeV]" ,part.pt()  ,100,0,10)
        
            ncharged+=1
            if part.pt() > 0.1: ncharged_pt0p1 += 1 
            if part.pt() > 0.5: ncharged_pt0p5 += 1 
            if part.pt() > 1  : 
                    ncharged_pt1   += 1 
                    if ievt < 10 : plot2D("h_evtdisplay_evt{}".format(ievt), ";eta;phi;pt" ,
                        part.eta(), part.phi(),
                        100,-3.5,3.5,
                        100,-3.5,3.5,
                        part.pt() ) 
            if part.pt() > 10 : ncharged_pt10  += 1 
                
        plot1D("h_n_dark_mesons" ,";n dark mesons" ,n_dark_mes,100,0,100)
        plot1D("h_n_dark_photons",";n dark photon" ,n_dark_pho,100,0,100)
        
        plot1D("h_ncharged"      ,";n tracks"              ,ncharged      ,100,0,2000)
        plot1D("h_ncharged_pt0p1",";n tracks pt > 0.1 GeV" ,ncharged_pt0p1,100,0,2000)
        plot1D("h_ncharged_pt0p5",";n tracks pt > 0.5 GeV" ,ncharged_pt0p5,100,0,1000)
        plot1D("h_ncharged_pt1"  ,";n tracks pt > 1 GeV"   ,ncharged_pt1  ,100,0,300)
        plot1D("h_ncharged_pt10" ,";n tracks pt > 10 GeV"  ,ncharged_pt10 ,100,0,10)

        plot1D("h_met_nu"  ,";met [GeV]", met_vector_nu.Pt()   , 100, 0, 300)
        plot1D("h_met_soft",";met [GeV]", met_vector_soft.Pt() , 100, 0, 300)
    
        ievt+=1

    return

    
def makeHistos():

    start = time.time()
    setStyle() 
    
    # Loop through files
    path = "root://cmseos.fnal.gov//store/user/kdipetri/SUEP/gen_MINIAOD_v0.0"
    infile = "step1_mMed-125_mDark-2_temp-2_decay-darkPho_13TeV-pythia8_n-10000_part-1.root" 
    if len(sys.argv) > 1: 
        infile = sys.argv[1]
    f = "{}/{}".format(path,infile) 

    # get sample name
    sample = getSample(infile)
    print(sample)
    loop(f,sample) 
    
    # save output
    fout = ROOT.TFile.Open("outputs/hist_{}.root".format(sample),"RECREATE")
    c1 = ROOT.TCanvas("c1","",900,800)
    c2 = ROOT.TCanvas("c2","",900,800)
    drawAll1D(c1)
    drawAll2D(c2)
    
    print("It took {} s".format(time.time()-start))

if __name__ == "__main__":
    makeHistos()
