variables=$(echo {{calo,pf}{MET,METPhi},j1{Eta,Phi,pT,CHF,NHF},metcut})
./PlotTool/plotter.py --sub Unblinded_with_signal $variables -a -s axial 1 1000
