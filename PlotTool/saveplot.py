#!/usr/bin/env python

"""
Exports variable from single years regions (sr & cr) into input file for monoJetLimits
Usage: ./PlotTool/saveplot.py variable -s signal
Refer to PlotTool/README,md for advance uses
"""

from sys import argv,path
from PlotTool import *
from ROOT import *
from os import system,getcwd,path,mkdir
import config

gROOT.SetBatch(1)

group = parser.add_group(__file__,__doc__,"Script")

dirlist = ["SignalRegion","SingleEleCR","SingleMuCR","DoubleEleCR","DoubleMuCR","GammaCR"]
dirmap = {"SignalRegion":"signal","DoubleEleCR":"Zee","DoubleMuCR":"Zmm","SingleEleCR":"Wen","SingleMuCR":"Wmn","GammaCR":"gjets"}
procmap = {"Data":"data","ZJets":"zjets","WJets":"wjets","DYJets":"zll","GJets":"gjets","TTJets":"top","DiBoson":"diboson","QCD":"qcd","QCDFake":"qcd"}
signalmap = {"Axial":"axial","Zprime":"zprime","dmsimp_scalar":"dmsimp_scalar"}
if not path.isdir("Systematics"): mkdir("Systematics")

def validHisto(hs,total=0,threshold=0.2):return hs.Integral() > threshold*total
def validShape(up,dn):return any( up[ibin] != dn[ibin] for ibin in range(1,up.GetNbinsX()+1) ) and validHisto(up) and validHisto(dn)

def SaveRegion(region,save):
#    region = Region(path=region,show=False,autovar=True,blinded=region=="SignalRegion")
    region = Region(path=region,show=False,autovar=True)
    region.initiate(variable)
    print(region.variable.nuisances)
    raw_input()
    
    if save.tfile is None: save.tfile = TFile("Systematics/%s_%s.sys.root" % (region.varname,region.year),'recreate')
    output = save.tfile
    
    print "Writing Histograms from %s" % region.region
    output.cd();
    # region['SumOfBkg'].histo.Write("SumOfBkg")
    if region.isBlinded:
        data = region['Data'].histo
        name = "%s_data" % dirmap[region.region]
        data.SetName(name)
        data.SetTitle(name)
        data.Write()
        
    region.setSumOfBkg()
    sumofbkg = region["SumOfBkg"].histo
    export = "%s_sumofbkg"% dirmap[region.region]
    sumofbkg.SetName(export)
    sumofbkg.SetTitle(export)
    sumofbkg.Write()

    theory_sys = ["NNLO_EWK","NNLO_Sud","NNLO_Miss"] + ["QCD_Scale","QCD_Proc","QCD_Shape","QCD_EWK_Mix"]
    exp_sys = ["JER","JES"]
    #["lnn_sys"] not needed as added directly in datacard, but btagging some vetos, prefiring are not included! FIXM
    
    for process in region:
        print "--Writing %s Histogram" % process.name
        
        if process.proctype == "signal":
            print(process.process)
            sigproc = next( signalmap[signal] for signal in signalmap if signal in process.process )
#            export = "%s_%s" % (dirmap[region.region],sigproc) -- for only 1 mass point
            my_sig_tag = process.process.replace("Axial","")
            export = "%s_%s%s" % (dirmap[region.region],sigproc,my_sig_tag)
            
        else: export = "%s_%s" % (dirmap[region.region],procmap[process.process])
        process.histo.SetName(export)
        process.histo.SetTitle(export)
        process.histo.Write()
        for nuisance in region.variable.nuisances:
                 if nuisance in theory_sys : nuisance= "THEORY_" + nuisance
                 elif nuisance in exp_sys  : nuisance= "EXP_" + nuisance
                 process.addUnc(nuisance)
                 output.cd()
#                 #cwd.cd()
                 nuisance = nuisance.replace("THEORY_","").replace("EXP_","")
                 if nuisance in process.nuisances:
                     print("in nuisance loop");print(nuisance);raw_input()
                     up,dn = process.nuisances[nuisance].GetHistos()
                     if not validShape(up,dn): print("not valid");continue
                     print "----Writing",process.nuisances[nuisance]
                     up.Write("%s_%s_%sUp"%(dirmap[region.region],process.process,nuisance))
                     dn.Write("%s_%s_%sDown"%(dirmap[region.region],process.process,nuisance))
    return region
def SavePlot(variable):
    print variable

    class save: pass
    save.tfile = None
    regionmap = { dirmap[region]:SaveRegion(region,save) for region in dirlist }
################################################################################
if __name__ == "__main__":
    
    import sys
    if "--no-width" not in sys.argv: sys.argv.append("--no-width")
    parser.parse_args()
    parser.args.no_width = True
    for variable in parser.args.argv: SavePlot(variable)
