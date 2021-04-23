variables=$(echo {{calo,pf}{MET,METPhi},j1{Eta,Phi,pT,CHF,NHF},metcut})
#variables=$(echo {caloMET,metcut})
echo $variables
for my_variable in $variables
do
#      ./PlotTool/export_systematics.py "$my_variable" "shape_lnn_sys_$my_variable.root" "shape_theory_sys_$my_variable.root" "shape_exp_sys_$my_variable.root"
#      mkdir "RootFiles/sys_shape/$my_variable/" 
#      mv "shape_lnn_sys_$my_variable.root" "RootFiles/sys_shape/$my_variable/shape_lnn_sys.root" 
#      mv "shape_theory_sys_$my_variable.root" "RootFiles/sys_shape/$my_variable/shape_theory_sys.root" 
#      mv "shape_exp_sys_$my_variable.root" "RootFiles/sys_shape/$my_variable/shape_exp_sys.root"
      ./PlotTool/plotter.py "$my_variable" -a --sub full_lumi_unblinded #--sub JES_JER_test
done

#test
#variables=$(echo recoil)
#./PlotTool/export_systematics.py $variables shape_lnn_sys_$variables.root shape_theory_sys_$variables.root &&
#mv shape_lnn_sys_$variables.root RootFiles/sys_shape/$variables/shape_lnn_sys.root &&
#mv shape_theory_sys_$variables.root RootFiles/sys_shape/$variables/shape_theory_sys.root &&
#./PlotTool/plotter.py $variables -a --sub systematics_added
