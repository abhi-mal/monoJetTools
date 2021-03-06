#!/usr/bin/env python

"""
Export systematics shape for quick systematics bands in data/mc plots
Usage: python PlotTool/export_systematics.py variable output_lnN_file.root output_scale_theory_file.root output_shape_exp_file.root output_scale_exp_file.root 
"""

from PlotTool import *
from ROOT import *

from PlotTool import ConstantNuisance
import os
import sys

# make sure to use TTree when exporting systematics
if "--branch" not in sys.argv: sys.argv.append("--branch")

group = parser.add_group(__file__,__doc__,"Script")
parser.parse_args()
variable = parser.args.argv[0]
output_lnN = TFile(parser.args.argv[1],"recreate")
output_scale_theory = TFile(parser.args.argv[2],"recreate")
output_shape_exp = TFile(parser.args.argv[3],"recreate")
output_scale_exp = TFile(parser.args.argv[4],"recreate")
rmap = {"SignalRegion":"sr","SingleEleCR":"we","SingleMuCR":"wm","DoubleEleCR":"ze","DoubleMuCR":"zm","GammaCR":"ga"}
#rmap = {"SignalRegion":"sr"}
#regions = { rmap[region]:Region(path=region,autovar=0,show=False) for region in rmap }
regions = { rmap[region]:Region(path=region,autovar=True) for region in rmap }
class lnN:
    def __init__(self,name,valuemap):
        self.name = name
        self.valuemap = valuemap
    def get(self,proc,region,year):
        name,value = self.name,self.valuemap
        def helper(key,valuemap):
            for k,v in valuemap.iteritems():
                if key in k: return v
        if helper(year,value):
          value = helper(year,value)
          name = name % year
        if helper(region,value): value = helper(region,value)
        if helper(proc,value): value = helper(proc,value)
        elif "axial" in proc : pass 
        elif "dmsimp_scalar" in proc : value = helper("dmsimp_scalar",value)
        elif "dmsimp_pseudoscalar" in proc : value = helper("dmsimp_pseudoscalar",value)
        elif "dmsimp_tchannel_0or1" in proc : value = helper("dmsimp_tchannel_0or1",value)
        elif "dmsimp_tchannel_2" in proc : value = helper("dmsimp_tchannel_2",value)
        elif "ADD" in proc : value = helper("ADD",value)
        elif "leptoquark" in proc : value = helper("leptoquark",value)
        if type(value) is not float: return None,None
        return name,value
lnNlist = [
    lnN("QCD_NormEleR",{"we":{"QCD":1.75}}),
    lnN("QCD_NormMuonR",{"wm":{"QCD":1.75}}),
    lnN("QCD_NormPurity",{"ga":{"QCDFake":1.25}}),
    lnN("QCD_NormSignal",{"sr":{"QCD":1.75}}),
    lnN("lumi_13TeV_%s",{
        "2017":{
            "ze":{("TTJets","DiBoson"):1.025},
            "zm":{("TTJets","DiBoson"):1.025},
            "sr":{("DiBoson","TTJets","QCD","axial","ggh","vbf","zh","wh"):1.025},
            "we":{("GJets","DiBoson","DYJets","TTJets","QCD"):1.025},
            "wm":{("DYJets","TTJets","DiBoson","QCD"):1.025}},
        "2018": {
            "ze":{("TTJets","DiBoson"):1.023},
            "zm":{("TTJets","DiBoson"):1.023},
            "sr":{("DiBoson","TTJets","QCD"):1.023},
            "we":{("GJets","DiBoson","DYJets","TTJets","QCD"):1.023},
            "wm":{("DYJets","TTJets","DiBoson","QCD"):1.023}}}),
    lnN("CMS_eff%s_btag",{
        "2017":{
            "ze":{"TTJets":1.06,"DiBoson":1.02},
            "zm":{"TTJets":1.06,"DiBoson":1.02},
            "sr":{"TTJets":1.06,("DiBoson","QCD"):1.02},
            "we":{"TTJets":1.06,("GJets","DiBoson","DYJets","QCD"):1.02},
            "wm":{"TTJets":1.06,("DYJets","DiBoson","QCD"):1.02}},
        "2018":{
            "ze":{"TTJets":1.06,"DiBoson":1.02},
            "zm":{"TTJets":1.06,"DiBoson":1.02},
            "sr":{"TTJets":1.06,("DiBoson","QCD"):1.02},
            "we":{"TTJets":1.06,("GJets","DiBoson","DYJets","QCD"):1.02},
            "wm":{"TTJets":1.06,("DYJets","DiBoson","QCD"):1.02}}}),
    lnN("CMS_eff%s_e",{
        "2017":{
            "ze":{("DYJets","TTJets","DiBoson"):1.02},
            "we":{("GJets","DiBoson","DYJets","TTJets","WJets","QCD"):1.01}},
        "2018":{
            "ze":{("DYJets","TTJets","DiBoson"):1.02},
            "we":{("GJets","DiBoson","DYJets","TTJets","WJets","QCD"):1.01}}}),
    lnN("CMS_eff%s_e_reco",{
        "2017":{
            "ze":{("DYJets","TTJets","DiBoson"):1.02},
            "we":{("GJets","DiBoson","DYJets","TTJets","WJets","QCD"):1.01}},
        "2018":{
            "ze":{("DYJets","TTJets","DiBoson"):1.02},
            "we":{("GJets","DiBoson","DYJets","TTJets","WJets","QCD"):1.01}}}),
    lnN("CMS_eff%s_eletrig",{
        "2017":{
            "ze":{("DYJets","TTJets","DiBoson"):1.01},
            "we":{("GJets","DiBoson","DYJets","TTJets","WJets","QCD"):1.01}},
        "2018":{
            "ze":{("DYJets","TTJets","DiBoson"):1.01},
            "we":{("GJets","DiBoson","DYJets","TTJets","WJets","QCD"):1.01}}}),
    lnN("CMS_eff%s_m",{
        "2017":{
            "zm":{("DYJets","TTJets","DiBoson"):1.02},
            "wm":{("DYJets","TTJets","DiBoson","WJets","QCD"):1.01}},
        "2018":{
            "zm":{("DYJets","TTJets","DiBoson"):1.02},
            "wm":{("DYJets","TTJets","DiBoson","WJets","QCD"):1.01}}}),
    lnN("CMS_eff%s_m_iso",{
        "2017":{
            "zm":{("DYJets","TTJets","DiBoson"):1.02},
            "wm":{("DYJets","TTJets","DiBoson","WJets","QCD"):1.01}},
        "2018":{
            "zm":{("DYJets","TTJets","DiBoson"):1.02},
            "wm":{("DYJets","TTJets","DiBoson","WJets","QCD"):1.01}}}),
    lnN("CMS_eff%s_m_reco",{
        "2017":{
            "zm":{("DYJets","TTJets","DiBoson"):1.02},
            "wm":{("DYJets","TTJets","DiBoson","WJets","QCD"):1.01}},
        "2018":{
            "zm":{("DYJets","TTJets","DiBoson"):1.02},
            "wm":{("DYJets","TTJets","DiBoson","WJets","QCD"):1.01}}}),
    lnN("CMS_eff%s_pho",{
        "2017":{"ga":{"GJets":1.05}},
        "2018":{"ga":{"GJets":1.05}}}),
    lnN("CMS_eff%s_photrig",{
        "2017":{"ga":{"GJets":1.01}},
        "2018":{"ga":{"GJets":1.01}}}),
    lnN("CMS_scale%s_j",{
        "2017":{
            "ze":{("TTJets","DiBoson"):1.04},
            "zm":{("TTJets","DiBoson"):1.04},
            "sr":{("DiBoson","TTJets","QCD","axial","ggh","vbf","zh","wh"):1.04},
            "we":{("GJets","DiBoson","DYJets","TTJets","QCD"):1.04},
            "wm":{("DYJets","TTJets","DiBoson","QCD"):1.04}},
        "2018": {
            "ze":{("TTJets","DiBoson"):1.04},
            "zm":{("TTJets","DiBoson"):1.04},
            "sr":{("DiBoson","TTJets","QCD","axial","ggh","vbf","zh","wh"):1.04},
            "we":{("GJets","DiBoson","DYJets","TTJets","QCD"):1.04},
            "wm":{("DYJets","TTJets","DiBoson","QCD"):1.04}}}),
    lnN("axial_Norm13TeV",{"sr":{"axial":1.05}}),
    lnN("dmsimp_scalar_Norm13TeV",{"sr":{"dmsimp_scalar":1.05}}),
    lnN("dmsimp_pseudoscalar_Norm13TeV",{"sr":{"dmsimp_pseudoscalar":1.05}}),
    lnN("dmsimp_tchannel_0or1_Norm13TeV",{"sr":{"dmsimp_tchannel_0or1":1.05}}),
    lnN("dmsimp_tchannel_2_Norm13TeV",{"sr":{"dmsimp_tchannel_2":1.05}}),
    lnN("ADD_Norm13TeV",{"sr":{"ADD":1.05}}),
    lnN("leptoquark_Norm13TeV",{"sr":{"leptoquark":1.05}}),
    lnN("ggh_Norm13TeV",{"sr":{"ggh":1.05}}),
    lnN("vbf_Norm13TeV",{"sr":{"vbf":1.05}}),
    lnN("wh_Norm13TeV",{"sr":{"wh":1.05}}),
    lnN("zh_Norm13TeV",{"sr":{"zh":1.05}}),
    lnN("gjet_Norm13TeV",{"we":{"GJets":1.2}}),
    lnN("top_Norm13TeV",{("ze","zm","sr","we","wm"):{"TTJets":1.1}}),
    lnN("top_Reweight13TeV",{("ze","zm","sr","we","wm"):{"TTJets":1.1}}),
    lnN("vv_Norm13TeV",{("ze","zm","sr","we","wm"):{"DiBoson":1.2}}),
    lnN("zll_Norm13TeV",{("we","wm"):{"DYJets":1.2}})
]

allbkg = ["ZJets","WJets","DYJets","GJets","TTJets","DiBoson","QCD"] #majorbkg = ["ZJets","DYJets","WJets","GJets"] adding all backgrounds
# shapeList = ["PSW_isrCon","PSW_fsrCon"]
scaleList_theory = ["QCD_Scale","QCD_Shape","QCD_Proc","QCD_EWK_Mix","NNLO_Miss","NNLO_Sud","NNLO_EWK"]
scaleList_exp = ['btag_sf','prefiring','eleveto_sf','muveto_sf','tauveto_sf']#2017
#scaleList_exp = ['btag_sf','eleveto_sf','muveto_sf','tauveto_sf']#2018-no prefiring
shapeList_exp = ["JES","JER"]

def export_region(region,output_lnN,output_scale_theory,output_shape_exp,output_scale_exp):
    print "Exporting",region.region
    region.initiate(variable)
    tdir_lnN_file = output_lnN.mkdir(rmap[region.region])#; tdir.cd()
    tdir_scale_theory_file = output_scale_theory.mkdir(rmap[region.region])#; tdir.cd()
    tdir_shape_exp_file = output_shape_exp.mkdir(rmap[region.region])
    tdir_scale_exp_file = output_scale_exp.mkdir(rmap[region.region])
    def export_process(process):
        print "\tExporting",process.name
        unclist = []
        for lnn in lnNlist:
            name,value = lnn.get(process.process,rmap[process.region],process.year)
            if not name: continue
            print(value)
            value -= 1
            ConstantNuisance(process,name,value)
            unclist.append(name)
        process.fullUnc(unclist,show=False)
        up = process.nuisances["Total"].up.Clone("%s_%sUp"%(process.process,"sys"))
        dn = process.nuisances["Total"].dn.Clone("%s_%sDown"%(process.process,"sys"))
        
        tdir_lnN_file.cd()
        up.Write()
        dn.Write()
        

        if process.process in allbkg:
            for shape in scaleList_theory:
                #print("****")
                #print(process.process)
                #print("****")
                process.addUnc(shape)
                unclist.append(shape)
        
                up = process.nuisances[shape].up.Clone("%s_%sUp"%(process.process,shape))
                dn = process.nuisances[shape].dn.Clone("%s_%sDown"%(process.process,shape))
                
                tdir_scale_theory_file.cd()
                up.Write()
                dn.Write()

            for shape in shapeList_exp:
                #print("****")
                #print(process.process)
                #print("****")
                process.addUnc(shape)
                unclist.append(shape)

                up = process.nuisances[shape].up.Clone("%s_%sUp"%(process.process,shape))
                dn = process.nuisances[shape].dn.Clone("%s_%sDown"%(process.process,shape))

                tdir_shape_exp_file.cd()
                up.Write()
                dn.Write()         

            for shape in scaleList_exp:
                #print("****")
                #print(process.process)
                #print("****")
                process.addUnc(shape)
                unclist.append(shape)

                up = process.nuisances[shape].up.Clone("%s_%sUp"%(process.process,shape))
                dn = process.nuisances[shape].dn.Clone("%s_%sDown"%(process.process,shape))

                tdir_scale_exp_file.cd()
                up.Write()
                dn.Write()


        elif ('dmsimp' in process.process) or ('ADD' in process.process) or ('leptoquark' in process.process) :# for the signal processes 
            for shape in scaleList_theory:
                #print("****")
                #print(process.process)
                #print("****")
                process.addUnc(shape)
                unclist.append(shape)
        
                up = process.nuisances[shape].up.Clone("%s_%sUp"%(process.process,shape))
                dn = process.nuisances[shape].dn.Clone("%s_%sDown"%(process.process,shape))
                
                tdir_scale_theory_file.cd()
                up.Write()
                dn.Write()

            for shape in shapeList_exp:
                #print("****")
                #print(process.process)
                #print("****")
                process.addUnc(shape)
                unclist.append(shape)

                up = process.nuisances[shape].up.Clone("%s_%sUp"%(process.process,shape))
                dn = process.nuisances[shape].dn.Clone("%s_%sDown"%(process.process,shape))

                tdir_shape_exp_file.cd()
                up.Write()
                dn.Write()        

            for shape in scaleList_exp:
                #print("****")
                #print(process.process)
                #print("****")
                process.addUnc(shape)
                unclist.append(shape)

                up = process.nuisances[shape].up.Clone("%s_%sUp"%(process.process,shape))
                dn = process.nuisances[shape].dn.Clone("%s_%sDown"%(process.process,shape))

                tdir_scale_exp_file.cd()
                up.Write()
                dn.Write()
 

    for process in region:
        print(process.process)
#        if process.proctype != "bkg": continu # exporting systematics for signal processed also
        if process.proctype == "data": continue
        export_process(process)

for region in regions.values(): export_region(region,output_lnN,output_scale_theory,output_shape_exp,output_scale_exp) 
            

