import sys
sys.path.append('../../')
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import WSandTW
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model

def test_WSandTW():
    out = WSandTW(False, Conv,ISA_model)
    assert out[0] == Conv.ParStruc.MTOW
