DefaultMap = {
    "axial":"postAxial_Mchi1_Mphi1000",
    "zprime":"postZprime_Mx1_Mv1000"
}

LegMap = {
    "axial":"Axial-Vector",
    "zprime":"Mono-Z'",
    "dmsimp_scalar":"dmsimp_scalar"
}

GetFileMap = {
    "axial":lambda mchi,mphi:"postAxial_Mchi%s_Mphi%s" % (mchi,mphi),
    "zprime":lambda mx,mv:"postZprime_Mx%s_Mv%s" % (mx,mv),
    "dmsimp_scalar": lambda mchi,mphi:"postdmsimp_scalar_Mchi%s_Mphi%s"%(mchi,mphi)
}

XsecMap = {
    "axial": {
        "postAxial_Mchi1_Mphi100":1.595e+02,
        "postAxial_Mchi1_Mphi300":3.496e+01,
        "postAxial_Mchi1_Mphi500":1.037e+01,
        "postAxial_Mchi1_Mphi750":3.150e+00,
        "postAxial_Mchi1_Mphi1000":1.181e+00,
        "postAxial_Mchi1_Mphi1500":2.445e-01,
        "postAxial_Mchi1_Mphi1750":1.217e-01,
        "postAxial_Mchi1_Mphi2000":6.429e-02,
        "postAxial_Mchi1_Mphi2250":3.583e-02,
        "postAxial_Mchi10_Mphi1750":1.230e-01,
        "postAxial_Mchi10_Mphi2000":6.513e-02,
        "postAxial_Mchi40_Mphi100":6.235e+01,
        "postAxial_Mchi100_Mphi300":2.120e+01,
        "postAxial_Mchi100_Mphi1750":1.199e-01,
        "postAxial_Mchi100_Mphi2000":6.392e-02,
        "postAxial_Mchi150_Mphi500":6.919e+00,
        "postAxial_Mchi150_Mphi1750":1.165e-01,
        "postAxial_Mchi150_Mphi2000":6.181e-02,
        "postAxial_Mchi150_Mphi2250":3.403e-02,
        "postAxial_Mchi200_Mphi100":6.831e-02,
        "postAxial_Mchi200_Mphi500":3.615e+00,
        "postAxial_Mchi200_Mphi1750":1.162e-01,
        "postAxial_Mchi200_Mphi2000":6.182e-02,
        "postAxial_Mchi300_Mphi300":2.126e-02,
        "postAxial_Mchi300_Mphi500":3.959e-02,
        "postAxial_Mchi300_Mphi750":1.057e+00,
        "postAxial_Mchi300_Mphi1000":7.801e-01,
        "postAxial_Mchi300_Mphi1500":2.022e-01,
        "postAxial_Mchi300_Mphi1750":1.048e-01,
        "postAxial_Mchi300_Mphi2000":5.770e-02,
        "postAxial_Mchi300_Mphi2250":3.167e-02,
        "postAxial_Mchi400_Mphi300":6.455e-03,
        "postAxial_Mchi400_Mphi2000":5.314e-02,
        "postAxial_Mchi400_Mphi2250":2.941e-02,
        "postAxial_Mchi500_Mphi500":2.853e-03,
        "postAxial_Mchi500_Mphi1750":8.037e-02,
        "postAxial_Mchi600_Mphi750":1.516e-03,
        "postAxial_Mchi600_Mphi1000":2.631e-03,
        "postAxial_Mchi600_Mphi1500":7.828e-02
    },
    "zprime":{
        "postZprime_Mx1000_Mv10":1.141900E-05,
        "postZprime_Mx1000_Mv1000":1.417200E-05,
        "postZprime_Mx1000_Mv10000":3.331200E-07,
        "postZprime_Mx10_Mv10":5.428000E-02,
        "postZprime_Mx10_Mv100":5.614700E-02,
        "postZprime_Mx10_Mv10000":8.268900E-06,
        "postZprime_Mx10_Mv15":5.480300E-02,
        "postZprime_Mx10_Mv50":5.754500E-02,
        "postZprime_Mx150_Mv10":7.021100E-03,
        "postZprime_Mx150_Mv1000":2.089100E-01,
        "postZprime_Mx150_Mv10000":3.756700E-06,
        "postZprime_Mx150_Mv200":7.592300E-03,
        "postZprime_Mx150_Mv295":8.354800E-03,
        "postZprime_Mx150_Mv500":1.307600E-02,
        "postZprime_Mx1_Mv10":1.655000E-04,
        "postZprime_Mx1_Mv100":9.684700E-02,
        "postZprime_Mx1_Mv1000":1.499600E+00,
        "postZprime_Mx1_Mv10000":1.036200E-05,
        "postZprime_Mx1_Mv20":5.698600E-02,
        "postZprime_Mx1_Mv200":1.062700E-01,
        "postZprime_Mx1_Mv300":1.412200E-01,
        "postZprime_Mx1_Mv50":8.907400E-02,
        "postZprime_Mx1_Mv500":2.287900E+00,
        "postZprime_Mx500_Mv10":2.752700E-04,
        "postZprime_Mx500_Mv10000":1.238300E-06,
        "postZprime_Mx500_Mv500":3.155200E-04,
        "postZprime_Mx500_Mv995":5.794600E-04,
        "postZprime_Mx50_Mv10":2.598200E-02,
        "postZprime_Mx50_Mv10000":5.741100E-06,
        "postZprime_Mx50_Mv200":2.825700E-02,
        "postZprime_Mx50_Mv300":3.635900E-02,
        "postZprime_Mx50_Mv50":2.599700E-02,
        "postZprime_Mx50_Mv95":2.556500E-02,
    },
    "dmsimp_scalar":{
        "postdmsimp_scalar_Mchi150_Mphi500" : 0.1543,
        "postdmsimp_scalar_Mchi1_Mphi100"   : 1.464,
        "postdmsimp_scalar_Mchi1_Mphi10"    : 2.183,
        "postdmsimp_scalar_Mchi1_Mphi200"   : 0.8415,
        "postdmsimp_scalar_Mchi1_Mphi300"   : 0.5766,
        "postdmsimp_scalar_Mchi1_Mphi350"   : 0.5731,
        "postdmsimp_scalar_Mchi1_Mphi400"   : 0.4599,
        "postdmsimp_scalar_Mchi1_Mphi450"   : 0.3114,
        "postdmsimp_scalar_Mchi1_Mphi500"   : 0.2064,
        "postdmsimp_scalar_Mchi1_Mphi50"    : 1.901,
        "postdmsimp_scalar_Mchi1_Mphi600"   : 0.09364,
        "postdmsimp_scalar_Mchi1_Mphi700"   : 0.04571,
        "postdmsimp_scalar_Mchi1_Mphi800"   : 0.02372,
        "postdmsimp_scalar_Mchi200_Mphi500" : 0.09118,
        "postdmsimp_scalar_Mchi20_Mphi50"   : 1.939,
        "postdmsimp_scalar_Mchi225_Mphi500" : 0.04418,
        "postdmsimp_scalar_Mchi22_Mphi50"   : 1.944,
        "postdmsimp_scalar_Mchi275_Mphi500" : 0.001084,
        "postdmsimp_scalar_Mchi28_Mphi50"   : 0.05681,
        "postdmsimp_scalar_Mchi40_Mphi100"  : 1.494,
        "postdmsimp_scalar_Mchi45_Mphi100"  : 1.503,
        "postdmsimp_scalar_Mchi4_Mphi10"    : 2.205,
        "postdmsimp_scalar_Mchi50_Mphi500"  : 0.2016,
        "postdmsimp_scalar_Mchi55_Mphi100"  : 0.03114,
        "postdmsimp_scalar_Mchi6_Mphi10"    : 0.1283
    }
}
