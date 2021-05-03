"""
Collection of postfile samples that represent a single region
Reads from config folder in each region to determine lumi, mc, and xsec to use
Refer to PlotTool/PlotTool/README.md for advance uses
"""

import mergeFiles as merge
import re
import os
from Parser import parser
from Process import Process
from Nuisance import Nuisance
from utilities import *
from samplenames import samplenames
from VariableInfo import *
from argparse import ArgumentParser
import copy

DataFileMap = {
    "SignalRegion":"postMETdata",
    "SingleEleCR":"postSingleEle",
    "SingleMuCR":"postSingleMu",
    "DoubleEleCR":"postDoubleEle",
    "DoubleMuCR":"postDoubleMu",
    "GammaCR":"postGamma"
}

def GetRegion():
    region_pattern = ["postMETdata","postSingleEle","postSingleMu","postDoubleEle","postDoubleMu","postGamma","postQCDFake"]
    RegionName = ["SignalRegion","SingleEleCR","SingleMuCR","DoubleEleCR","DoubleMuCR","GammaCR","GammaCR"]

    def checkdir(dirname):
        for region,pattern in zip(RegionName,region_pattern):
            if region in dirname: return region
            if any( pattern in fname for fname in os.listdir('.') ): return region
            if os.path.isdir('.output/') and any( pattern in fname for fname in os.listdir('.output/') ): return region

    dirname = os.getcwd()
    region = checkdir(dirname)
    if region != None: return region
    
    if not os.path.isfile('postpath.txt'): return "SignalRegion"
    
    with open('postpath.txt') as f: postpath = f.read().strip()
    cwd = os.getcwd(); os.chdir(postpath)
    dirname = os.path.realpath( os.getcwd() + '/../' )
    region = checkdir(dirname)
    if region != None: return region
    return "SignalRegion"

MCOrderMap = {
    "SignalRegion":[
        "ZJets","WJets","GJets","DiBoson","TTJets","QCD","DYJets"
    ],
    "SingleEleCR":[
        "WJets","TTJets","DiBoson","GJets","QCD","DYJets","ZJets"
    ],
    "SingleMuCR":[
        "WJets","TTJets","QCD","DYJets","DiBoson","GJets","ZJets"
    ],
    "SingleLepCR":[
        "WJets","TTJets","QCD","DYJets","DiBoson","GJets","ZJets"
    ],
    "DoubleEleCR":[
        "DYJets","DiBoson","TTJets","WJets","QCD","GJets","ZJets"
    ],
    "DoubleMuCR":[
        "DYJets","DiBoson","TTJets","WJets","QCD","GJets","ZJets"
    ],
    "DoubleLepCR":[
        "DYJets","DiBoson","TTJets","WJets","QCD","GJets","ZJets"
    ],
    "GammaCR":[
        "G-NLO","GJets","QCD","WJets","DiBoson","TTJets","DYJets","ZJets"
    ]
}

group = parser.add_group(__file__,__doc__,"Class")

group.add_argument("-l","--lumi",help="set the luminosity for scaling",action="store",type=float)
group.add_argument("-s","--signal",help="specify the signal file to use",action="store",nargs="+",default=[])
group.add_argument("--nhists",help="Plot all 1D plots at nhists level",type=int,nargs='?',const=-1)
group.add_argument("--mc-solid",help="Make MC solid color",action="store_true",default=False)
group.add_argument("-d","--directory",help="Specify directory to get post files from",type=valid_directory)
group.add_argument("-e","--era",help="Specify the eras to use",type=lambda arg:sorted(arg.upper()),default=None)
group.add_argument("-a","--autovar",help="Specify to use the automatic basic nhist",nargs="?",const=0,type=int)
group.add_argument("--auto-order",help="Order MC Stack based on Integral",action="store_true",default=False)
group.add_argument("--normalize",help="Specify to normalize plots to unity",action="store_true",default=False)
group.add_argument("--no-nlo",help="Do not use NLO samples",action="store_true",default=False)
group.add_argument("--postpath",help="Force path to come from postpath.txt",action="store_true",default=False)
group.add_argument("--verbose",help="Specify verbose level",type=int,default=0)
group.add_argument("--blinded",help="Disable Data from being plotted",action="store_true",default=False)
group.add_argument("--use-ga-qcd",help="Use QCD from GammaCR instead of QCD Fake Template",action="store_true",default=False)

class Region(object):
    def __init__(self,year=None,region=None,lumi=None,path=None,config=None,autovar=None,useMaxLumi=False,show=True,blinded=None):
        parser.parse_args()
        self.year = year; self.region = region; self.show = show
        self.setPath(path)
        self.setConfig(config)
        if self.region is None: self.region = GetRegion()
        self.setLumi(lumi,useMaxLumi)
        
        self.autovar = autovar
        if parser.args.autovar is not None: self.autovar = parser.args.autovar
        if self.autovar is True: self.autovar = 0

        self.isBlinded = blinded
        if self.isBlinded is None:
            self.isBlinded = parser.args.blinded

        self.MCList = []
        for mc in self.config.mclist: self.MCList.append(mc)
        self.SampleList = ["Data"] + self.MCList
        self.processes = {}
        datafile = DataFileMap[self.region]
        if 'Ele' in self.region and self.year == '2017':
            datalist = []
            for type in ("SE","SP"):
                for era in sorted(self.lumimap.keys()):
                    datalist.append( '%s_%s_%s' % (datafile,type,era))
        else:
            datalist = [ '%s_%s' % (datafile,era) for era in sorted(self.lumimap.keys()) ]
        self.processes["Data"] =    Process("Data",datalist,None,'data',year=self.year,region=self.region)
        for mc in self.MCList:
            if self.region == "GammaCR" and mc == "QCD" and not parser.args.use_ga_qcd:
                fakefiles = [ datafile.replace("Gamma","QCDFake") for datafile in datalist ]
                self.processes[mc] = Process("QCDFake",fakefiles,None,'bkg',
                                         leg=self.config.legmap[mc],color=self.config.colmap[mc],year=self.year,region=self.region)
                continue
            filelist = list(self.config.filemap[mc])
            if mc in self.config.nlomap and not parser.args.no_nlo:
                filelist += list(self.config.nlomap[mc])
            self.processes[mc] = Process(mc,filelist,GetMCxsec(filelist,self.config.xsec),'bkg',
                                         leg=self.config.legmap[mc],color=self.config.colmap[mc],year=self.year,region=self.region)
        if self.region == "SignalRegion" and any(parser.args.signal):
            self.setSignalInfo()
        self.haddFiles()
        if os.getcwd() != self.cwd: os.chdir(self.cwd)
    def __len__(self): return len(self.SampleList)
    def __getitem__(self,i):
        if type(i) == str: key = i
        if type(i) == int: key = self.SampleList[i];
        return self.processes[key]
    def __iter__(self):
        for i in range(len(self)): yield self[i]
    def __contains__(self,procname): return procname in self.processes
    def haddFiles(self):
        if os.getcwd() != self.path: os.chdir(self.path)
        if not os.path.isdir('.output/'): return
        def validfile(fname): return os.path.isfile(fname)
        filelist = []
        for process in self: filelist += [ filename for filename in process.filenames if not validfile(filename+'.root') ]
        filelist += [ filename for filename in self.xsec if filename not in filelist and not validfile(filename+'.root') ]
        if self.region == 'SignalRegion':
            for signal,xsecmap in self.signalinfo.XsecMap.iteritems():
                filelist += [ filename for filename in xsecmap if not validfile(filename+'.root') ]
        merge.HaddFiles(filelist)
        if os.getcwd() != self.cwd: os.chdir(self.cwd)
    def setPath(self,path=None):
        self.cwd = os.getcwd()
        self.path = path
        if self.path is None: self.path = self.cwd
        if parser.args.directory is not None: self.path = parser.args.directory
        os.chdir(self.path)
        hasLocalFiles = any( re.search('post.*\.root',fname) for fname in os.listdir('.') )
        hasOutputFiles = os.path.isdir('.output') and any( re.search('post.*\.root',fname) for fname in os.listdir('.output') )
        hasLocal = hasLocalFiles and hasOutputFiles
        if os.path.isfile('postpath.txt') and not hasLocal:
            with open('postpath.txt') as f: self.path = f.read().strip()
            os.chdir(self.path);
        self.path = os.getcwd()
        print 'Using %s' % self.path
    def setConfig(self,config=None):
        if config is None: import config
        self.config = config
        if self.year is None: self.year = config.version
        self.xsec = config.xsec
        self.signalinfo = config.signalinfo
    def setLumi(self,lumi=None,useMaxLumi=False):
        self.lumi = lumi
        self.lumimap = self.config.lumi_by_era[self.region] if self.region in self.config.lumi_by_era else self.config.lumi_by_era["SingleMuCR"]
        if self.lumi is None: self.lumi = self.config.lumi[self.region] if self.region in self.config.lumi else self.config.lumi["SingleMuCR"]
        if parser.args.lumi is not None: self.lumi = parser.args.lumi
        if parser.args.era is not None:
            self.lumimap = { era:self.lumimap[era] for era in parser.args.era }
            self.lumi = sum(self.lumimap.values())
        self.max_lumi = max( self.config.lumi.values() )
        if useMaxLumi: self.lumi = self.max_lumi
        
        self.lumi_label = '%s' % float('%.3g' % (self.lumi/1000.)) + " fb^{-1}"
        if (parser.args.normalize): self.lumi_label="Normalized"
    def setSignalInfo(self,scale=1):
        self.SignalList = []
        self.SignalToPlot = []
        signal_parser = ArgumentParser()
        signal_parser.add_argument("extra",nargs="*",default=None)
        for signal in self.signalinfo.XsecMap: signal_parser.add_argument("-"+signal,nargs="*")
        signal_args = [ '-'+arg if arg in self.signalinfo.XsecMap else arg for arg in parser.args.signal ]
        signal_args = signal_parser.parse_args(signal_args)
        signalmap = {}
        if "-1" in signal_args.extra:
            for xsecmap in self.signalinfo.XsecMap.values(): signalmap.update(xsecmap)
        else:
            for signal in self.signalinfo.XsecMap:
                if hasattr(signal_args,signal) and getattr(signal_args,signal) is not None:
                    print(signal)
                    signal_to_plot = None
                    args = getattr(signal_args,signal)
                    if "-1" in args: signalmap.update(self.signalinfo.XsecMap[signal])
                    elif len(args) == 2:
                        fname = self.signalinfo.GetFileMap[signal](args[0],args[1])
                        xsec = self.signalinfo.XsecMap[signal][fname]
                        signalmap[fname] = (xsec,signal)
                        signal_to_plot = fname
                    else:
                        fname = self.signalinfo.DefaultMap[signal]
                        xsec = self.signalinfo.XsecMap[signal][fname]
                        signalmap[fname] = (xsec,signal)
#                    if signal_to_plot is None: signal_to_plot = self.signalinfo.DefaultMap[signal]
#                    self.SignalToPlot.append(signal_to_plot)
                    for signal_to_plot in signalmap.keys():
                        self.SignalToPlot.append(signal_to_plot)
                    print(self.SignalToPlot)
                    print(len(self.SignalToPlot))
                    #raw_input()
#        for fname,(xsec,sigtype) in signalmap.iteritems():
        for fname,xsec in signalmap.iteritems():
            sigtype = "dmsimp_scalar"
            signal = fname.strip('post')
            if fname in self.SignalToPlot: self.SignalToPlot[self.SignalToPlot.index(fname)] = signal;print("Got it")
            self.SignalList.append(signal)
            xsecmap = {fname:xsec}
            print(signal)
            self.processes[signal] = Process(signal,[fname],xsecmap,'signal',year=self.year,region=self.region,leg=self.signalinfo.LegMap[sigtype])
            self.SampleList.insert(1,signal)
    def open(self):
        if hasattr(self,'isOpen'): return
        self.isOpen = True

        proclist = self.processes.keys()
        for process in proclist:
            if not self[process].open(self.config):
                if self[process].proctype == 'data':
                    self.isBlinded = True
                self.processes.pop(process)
                if process in self.SampleList: self.SampleList.remove(process)
                if process in self.MCList: self.MCList.remove(process)
                if hasattr(self,'SignalList') and process in self.SignalList: self.SignalList.remove(process)
        if self.isBlinded:
            print 'Blinded: Setting data as SumOfBkg'
            if 'Data' in self.processes:
                self.processes.pop('Data')
                self.SampleList.remove('Data')
            self.setLumi(self.max_lumi)
    def initVariable(self,variable,weight,cut):
        if not hasattr(self,'first_init'):
            self.first_init = True
            tfile = next( process[0].tfile for process in self if process[0].tfile is not None )
            self.variable = VariableInfo(tfile)
            
            if self.show:
                print "Running in "+self.region+":"
                print "Plotting at",self.lumi,"pb^{-1}"

            
        self.total_bkg = 0
        if 'SumOfBkg' in self.processes:
            tmp = self.processes.pop('SumOfBkg')
            del tmp
        self.variable.setVariable(variable,weight,cut,autovar=self.autovar)
        self.scaleWidth = self.variable.scaleWidth
        self.varname = self.variable.variable
        if self.autovar is not None: self.varname = self.variable.base
        if hasattr(self.variable,'cutfix'): self.varname += self.variable.cutfix
        if hasattr(self.variable,'binfix'): self.varname += '_'+self.variable.binfix
    def initiate(self,variable,weight='weight',cut=None):
        if os.getcwd() != self.path: os.chdir(self.path)
        self.open()
        self.initVariable(variable,weight,cut)
        variable = self.variable
        for process in self:
            if self.isBlinded and process.proctype == 'data': continue
            process.setVariable(variable,self.lumi)
            if process.proctype == 'bkg':
                self.total_bkg += process.scaled_total
        self.setMCOrder()
        self.name = variable.xaxis_title
        if self.isBlinded:
            self.setSumOfBkg()
            self.processes['Data'] = copy.deepcopy(self['SumOfBkg'])
            self['Data'].proctype = 'bkg'
        if self.show: self.output()
        if os.getcwd() != self.cwd: os.chdir(self.cwd)
    def setMCOrder(self):
        def mcsort(process):
            if 'cutflow' in self.variable.variable:
                return self[process].histo.GetBinContent(self[process].histo.GetNbinsX())
            return self[process].scaled_total
        if self.region not in MCOrderMap or parser.args.auto_order:
            self.MCOrder = [ process.process for process in self if process.proctype == 'bkg']
            self.MCOrder.sort(key=mcsort,reverse=True)
        else: self.MCOrder = [ procname for procname in MCOrderMap[self.region] if procname in self ]
    def output(self):
        if self.scaleWidth: print "Bin Width Normalization"
        prompt = 'integral of %s: %s'
        ntemp = '{0:<15}'; itemp = '{0:<8}'
        verbose = parser.args.verbose == 1
        self['Data'].output(verbose=verbose)
        if hasattr(self,'SignalList'):
            for signal in self.SignalList: self[signal].output(verbose=verbose,total_bkg=self.total_bkg)
        print prompt % ( ntemp.format('SumOfBkg'),itemp.format( '%.6g' % self.total_bkg ) )
        for sample in self.MCOrder:
            if sample in self:
                self[sample].output(verbose=verbose,total_bkg=self.total_bkg)
        ratio = ('%.6g' % (self.processes['Data'].scaled_total/self.total_bkg)) if self.total_bkg != 0 else 'Nan'
        print '            %s: %s' % (ntemp.format('data/mc'),itemp.format(ratio))
    def setSumOfBkg(self):
        if "SumOfBkg" in self.processes: return
        sumofbkg = Process('SumOfBkg',[],{},'sumofbkg',year=self.year,region=self.region)
        for process in self:
            if process.proctype == 'bkg':
                sumofbkg.add(process)
        sumofbkg.variable = self.variable
        sumofbkg.process = MCOrderMap[self.region][0]
        self.processes['SumOfBkg'] = sumofbkg
        print(self.__class__.__name__)
        return self['SumOfBkg']
    def addUnc(self,nuisance,show=False):
        for process in self: process.addUnc(nuisance,show)
    def fullUnc(self,unclist,show=False):
        self.setSumOfBkg()
        
        for process in self: process.fullUnc(unclist,show)
        
        up = self['SumOfBkg'].histo.Clone('%s_%s_TotalUp' % (self['SumOfBkg'].name,self.variable.base));  up.Reset()
        dn = self['SumOfBkg'].histo.Clone('%s_%s_TotalDown' % (self['SumOfBkg'].name,self.variable.base)); dn.Reset()

        AddLikeNuisances([process.nuisances["Total"] for process in self if process.proctype == 'bkg'],up,dn,self['SumOfBkg'].histo)
        self['SumOfBkg'].nuisances["Total"] = Nuisance('SumOfBkg',"Total",up,dn,self['SumOfBkg'].histo)
        if show: print self['SumOfBkg'].nuisances['Total']
    def getUncBand(self,unclist):
        self.fullUnc(unclist)
        data = self['Data'].histo
        up,dn = self['SumOfBkg'].nuisances['Total'].GetHistos()
        rup = GetRatio(data,up); rdn = GetRatio(data,dn)
        uncband = GetUncBand(rup,rdn,norm=1)
        return uncband
    def add(self,other,addlumi=False):
        samplelist = self.processes.keys()
        if addlumi: self.lumi += other.lumi
        for sample in other.processes.keys():
            if sample not in samplelist: samplelist.append(sample)
        for sample in samplelist:
            if sample in self.processes and sample in other.processes:
                self.processes[sample].add(other.processes[sample])
            if sample not in self.processes and sample in other.processes:
                self.processes[sample] = copy.deepcopy(other.processes[sample])

if __name__ == "__main__":
    FindConfig()
    sample = Region(autovar=True)
    sample.initiate('recoil')
