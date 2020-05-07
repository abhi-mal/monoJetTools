#!/usr/bin/env python
import os
import sys
sys.path.append("PlotTool")
from PlotTool import *
import config
import re
config.mclist = ["GJets"]

parser.add_argument("--plot",action="store_true")
parser.add_argument("--clean",action="store_true",default=True)
parser.add_argument("--save",action="store_true")

if not os.path.isdir("templates"):
    # Create directory to store templates and make git ignore it
    os.mkdir("templates")
    with open("templates/.gitignore","w") as f: f.write("*")
    
from ROOT import TCanvas,gStyle,kRed,kGreen,kBlue,TLatex,TPad

sig_path = "SigTemplate"
bkg_path = "BkgTemplate"

sig_template = Region(path=sig_path,autovar=True,show=0)
bkg_template = Region(path=bkg_path,autovar=True,show=0)

xaxismap = {
    "photonPFIso":"Photon PF Isolation [GeV]"
}

def save_template(template,output):
    output.cd()
    template.Write()
def temp_style(hs,color):
    hs.SetLineColor(color)
    hs.SetLineWidth(2)
    hs.SetFillColor(0)
    hs.SetFillStyle(0)
def PtRangeText(x=0.55,y=0.8,ptrange=(-1,-1)):
    rangetext = TLatex(x,y,"%s < Photon P_{T} < %s"%(ptrange[0],ptrange[1]))
    rangetext.SetNDC()
    rangetext.SetTextFont(42)
    rangetext.SetTextSize(0.035)
    rangetext.Draw()
    return rangetext
def PlotBkg(templates):
    data = templates["Data"].histo.Clone()
    gjets = templates["GJets"].histo.Clone()
    sideband = templates["Sideband"].histo.Clone()

    c = TCanvas("c", "canvas",800,800);
    gStyle.SetOptStat(0);
    gStyle.SetLegendBorderSize(0);
    c.SetLeftMargin(0.15);
    c.SetLogy();
    #c.cd();

    temp_style(sideband,kRed)
    temp_style(gjets,kGreen+2)
    DataStyle(data)

    leg = getLegend(ymin=0.6,ymax=0.8)

    sideband.Draw("hist")
    hslist = [sideband]

    sideband.SetTitle("")
    sideband.GetYaxis().SetTitle("Events")

    if templates.variable.xaxis_title == "":
        templates.variable.xaxis_title = next( (vartitle for var,vartitle in xaxismap.items() if var in templates.variable.variable) ,"" )
    sideband.GetXaxis().SetTitle(templates.variable.xaxis_title)

    if parser.args.clean:
        gjets.Draw("hist same")
        data.Draw("pex0 same")
        hslist = hslist + [gjets,data]

        leg.AddEntry(data,"Sideband Data","lp")
        leg.AddEntry(gjets,"Sideband GJets","l")
    leg.AddEntry(sideband,"QCD Fake Template","l")
    leg.Draw()

    SetBounds(hslist,scale=5,log=10)

    lumi_label = '%s' % float('%.3g' % (templates.lumi/1000.)) + " fb^{-1}"
    texLumi,texCMS = getCMSText(lumi_label,templates.year,scale=0.8)

    if re.search("(\d+to\d+|\d+toInf)",templates.variable.variable):
        ptrange = templates.variable.variable.split("_")[1].split("to")
        rtext = PtRangeText(0.55,0.85,ptrange)
    
    SaveAs(c,"sideband_template_%s"%templates.varname,year=templates.year,sub="GammaPurity")
def BkgTemplates(variable,output):
    bkg_template.initiate(variable)

    sidebandproc = Process("Sideband",[],{},"sideband",year=bkg_template.year,region=bkg_template.year)
    sidebandproc.add( bkg_template["Data"] )

    bkg_template.processes["Sideband"] = sidebandproc

    if parser.args.save: save_template(bkg_template["Sideband"].histo.Clone("fake_qcd"),output)
    if parser.args.clean: bkg_template["Sideband"].histo.Add( bkg_template["GJets"].histo,-1 )
    if parser.args.plot: PlotBkg(bkg_template)

    return bkg_template
def PlotSig(templates,sideband_templates):
    data = templates["Data"].histo.Clone()
    gjets = templates["GJets"].histo.Clone()
    sideband = sideband_templates["Sideband"].histo.Clone()
    full = gjets.Clone(); full.Add(sideband)

    c = TCanvas("c", "canvas",800,800);
    gStyle.SetOptStat(0);
    gStyle.SetLegendBorderSize(0);
    # c.SetLeftMargin(0.15);
    # c.SetLogy();
    #c.cd();

    pad1 = TPad("pad1","pad1",0.01,0.25,0.99,0.99);
    pad1.SetBottomMargin(0.);
    pad1.Draw(); pad1.cd();
    pad1.SetLogy();
    pad1.SetFillColor(0); pad1.SetFrameBorderMode(0); pad1.SetBorderMode(0);
    

    temp_style(gjets,kGreen+2)
    temp_style(sideband,kRed)
    temp_style(full,kBlue+2)
    DataStyle(data)

    leg = getLegend(ymin=0.6,ymax=0.8)

    gjets.Draw("hist")

    gjets.SetTitle("")
    gjets.GetYaxis().SetTitle("Events")

    if templates.variable.xaxis_title == "":
        templates.variable.xaxis_title = next( (vartitle for var,vartitle in xaxismap.items() if var in templates.variable.variable) ,"" )
    gjets.GetXaxis().SetTitle(templates.variable.xaxis_title)
    
    sideband.Draw("hist same")
    full.Draw("hist same")
    data.Draw("pex0 same")
    hslist = [data,gjets,sideband]
    
    leg.AddEntry(data,"Data","lp")
    leg.AddEntry(gjets,"Real GJets","l")
    leg.AddEntry(sideband,"Sideband QCD","l")
    leg.AddEntry(full,"Full","l")

    SetBounds(hslist,scale=5,log=10)
    leg.Draw()
    
    lumi_label = '%s' % float('%.3g' % (templates.lumi/1000.)) + " fb^{-1}"
    texLumi,texCMS = getCMSText(lumi_label,templates.year)

    if re.search("(\d+to\d+|\d+toInf)",templates.variable.variable):
        ptrange = templates.variable.variable.split("_")[1].split("to")
        rtext = PtRangeText(0.55,0.85,ptrange)

    
    c.cd();
    pad2 = TPad("pad2","pad2",0.01,0.01,0.99,0.25);
    pad2.SetGridy()
    pad2.Draw(); pad2.cd();
    pad2.SetFillColor(0); pad2.SetFrameBorderMode(0); pad2.SetBorderMode(0);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.35);
    
    ratio = GetRatio(data,full)
    
    RatioStyle(ratio,rymin=-0.25,rymax=2.25,xname=templates.variable.xaxis_title,yname="Data/Full")
    ratio.Draw("pex0");
    line = getRatioLine(data.GetXaxis().GetXmin(),data.GetXaxis().GetXmax())
    line.Draw("same");
    
    SaveAs(c,"real_template_%s"%templates.varname,year=templates.year,sub="GammaPurity")
def SigTemplates(variable,output,sideband_templates=None):
    sig_template.initiate(variable)

    if parser.args.save:
        save_template(sig_template["Data"].histo.Clone("data"),output)
        save_template(sig_template["GJets"].histo.Clone("signal_gjets"),output)
    if parser.args.plot and sideband_templates: PlotSig(sig_template,sideband_templates)

    return sig_template

if __name__ == "__main__":
    parser.parse_args()

    ptbins = [230, 250, 280, 320, 375, 425, 475, 550, "Inf"]

    for variable in list(parser.args.argv):
        if "ptbins" in variable:
            parser.args.argv.remove(variable)
            for i in range(len(ptbins)-1): parser.args.argv.append(variable.replace("ptbins","%sto%s"%(ptbins[i],ptbins[i+1])))

    output = None
    for variable in parser.args.argv:
        if parser.args.save:
            output = TFile("templates/template_%s.root"%variable,"recreate")
            print "Writing templates to",output.GetName()
        sideband = BkgTemplates(variable,output)
        real = SigTemplates(variable,output,sideband)