import ROOT
import os
from ROOT import TCanvas, TPad, TFile, TDirectory
import argparse

parser = argparse.ArgumentParser(
    "Get the recoil_250cut/recoil_100cut for QCD leading jet distributions")
parser.add_argument(
    "inputFile_distributions",
    action="store",
  #  dest="inputFile", for positional arguments, we don't need the dest, the name supplied(here inputFile_nocalib) will itself be the name of the argument)
    help="Provide the relative path to the target input root file from which to get the QCD distributions for the leading jet variables")

args = parser.parse_args()
infile_name = args.inputFile_distributions
assert (infile_name != None), "Please provide a proper file"
infile = ROOT.TFile( infile_name, "r" )
recoil_250_hist = infile.Get("recoil_250_cut/j1pT_recoil_250_cut")
recoil_100_hist = infile.Get("recoil_100_cut/j1pT_recoil_100_cut")
N_events_num = recoil_250_hist.Integral()
N_events_den = recoil_100_hist.Integral()
SF = N_events_num/N_events_den
print(SF)
print("SF = %f"%SF)
