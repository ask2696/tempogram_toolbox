import numpy as np
#from scipy.io import wavfile
#import utilFunctions as UF
from math import *
#from audio_to_STFT import audiotoSTFT
import matplotlib.pyplot as plt
import numpy.matlib
from scipy import signal
#from master import noveltyCurve
#np.seterr(divide='ignore', invalid='ignore')

def myhann1(n):
    res =  0.5 -0.5 * np.cos(2*pi*(np.arange(n)/(n-1)))                         
    return res

def NoveltyCurve_to_Tempogram(noveltyCurve,parameter):
    win_len = np.round(parameter['tempoWindow'] * parameter['featureRate'])
    win_len = win_len + (win_len%2)-1

    parameter['tempoRate'] = parameter['featureRate']/parameter['stepsize']
    #print win_len
    
    windowTempogram = myhann1(win_len)
    #print windowTempogram

    novelty = np.append(np.zeros([1,int(round(win_len/2))]),np.append(noveltyCurve,np.zeros([1,int(round(win_len/2))]))).T
    #fourierCoefficients_matlab(novelty,windowTempogram,win_len-parameter.stepsize
    #, parameter.BPM./60, parameter.featureRate);
    #print novelty[200:1000]
    f = (parameter['BPM'].T)/60.0
    #print f
    n_overlap = win_len - parameter['stepsize']
    #print n_overlap
    hopsize = win_len - n_overlap
    #print hopsize

    f_s = parameter['featureRate']
    #print f_s
    T = np.arange(win_len)/f_s
    
    T = T.T
    #print T
    win_num = np.floor((len(novelty)- n_overlap)/(win_len - n_overlap))
    x = np.zeros([int(win_num),len(f)],dtype=complex)
    t = np.arange( win_len/2, len(novelty) -(win_len/2), hopsize)/f_s

    twoPiT = 2 * pi* T

    for f0 in np.arange(len(f)):

        twoPiFT = f[f0] * twoPiT;
        cosine = np.cos(twoPiFT)
        sine = np.sin(twoPiFT)

        for w in np.arange(int(win_num)):

            start = w * hopsize
            stop = start + win_len

            sig = np.multiply(novelty[int(start):int(stop)],windowTempogram)
            co = sum(np.multiply(sig,cosine))
            si = sum(np.multiply(sig,sine))
            
            x[w,f0] = complex(co,si)
            #print complex(co,si)
    #print x[200]
    tempogram = x.T
    #print tempogram[3,3]
    #tempogram = tempogram /sqrt(win_len) / sum(windowTempogram)
    BPM = f* 60

    abs_tempogram = abs(tempogram)

    t = t - t[0]
    #plt.figure(2)
    #plt.pcolormesh(t,BPM,abs_tempogram)
    #plt.show()
    return (tempogram,T,BPM,parameter['tempoRate'])

#noveltyC = np.array([[0.004177,0.180181,0.361323,0.554022,0.658699,0.495659,0.204222,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.039311,0.154515,0.234873,0.212814,0.095493,-0.000000,-0.000000,-0.000000,0.012071,0.001314,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.022007,0.073772,0.240175,0.523533,0.599455,0.444682,0.241287,0.075969,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.195690,0.573225,0.780773,0.578224,0.267959,0.033960,-0.000000,-0.000000,-0.000000,0.169782,0.672401,1.137687,1.164735,0.652050,0.184197,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.134243,0.488234,0.757699,0.675830,0.282511,-0.000000,-0.000000,-0.000000,-0.000000,0.250212,0.767572,1.142171,1.137839,0.737385,0.254534,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.076682,0.472961,0.794921,0.827863,0.521057,0.181126,-0.000000,-0.000000,-0.000000,0.127518,0.606303,1.126804,1.333971,1.003338,0.416228,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.230902,0.584359,0.785653,0.559031,0.192146,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.197123,0.368639,0.373814,0.275248,0.122597,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.087112,0.313050,0.530522,0.569858,0.428145,0.239055,0.070174,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.093807,0.237224,0.352466,0.436380,0.362572,0.141387,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.007984,0.226544,0.411255,0.444173,0.309693,0.079973,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.081728,0.320673,0.527625,0.612658,0.478215,0.229318,0.026283,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.044634,0.220555,0.343231,0.346766,0.244991,0.095893,0.000729,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.119576,0.413783,0.775703,0.907831,0.645183,0.271184,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.162086,0.471796,0.568525,0.422897,0.188437,0.040919,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.020505,0.398679,0.818306,1.011937,0.916258,0.672818,0.378037,0.105400,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.095914,0.388627,0.649124,0.627205,0.331963,0.049125,-0.000000,-0.000000,-0.000000,0.016070,0.281452,0.591185,0.839179,0.794143,0.496767,0.184549,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.115912,0.442234,0.585621,0.476737,0.223204,-0.000000,-0.000000,-0.000000,-0.000000,0.242774,0.637599,0.914651,0.835165,0.532588,0.250099,0.034279,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.138957,0.394627,0.516913,0.463555,0.271744,0.063687,-0.000000,-0.000000,-0.000000,0.158012,0.493431,0.696438,0.582511,0.308896,0.013653,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.048953,0.207946,0.202102,0.080306,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.026446,0.050433,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.015421,0.171203,0.232015,0.102828,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.176702,0.504656,0.756969,0.804518,0.588073,0.216918,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.003688,0.045411,0.031243,0.020129,0.002815,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.397203,0.847558,0.987937,0.684204,0.196321,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.298365,0.707443,1.035489,1.046773,0.706505,0.300773,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.005496,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.021555,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.363006,0.738786,0.893432,0.742251,0.408299,0.071992,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.230186,0.538401,0.688824,0.639546,0.464907,0.248600,0.051077,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.185412,0.883748,1.464852,1.405856,0.689587,0.101966,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.095654,0.303385,0.280210,0.156932,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.011053,0.196667,0.325118,0.041743,0.054031,0.052441,-0.000000,-0.000000,-0.000000,-0.000000,0.105675,0.345815,0.174007,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.438348,0.898677,1.182004,0.672622,0.066877,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.132983,0.531796,0.335928,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.094928,0.703307,1.377566,1.736574,1.636287,0.888731,0.005375,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.069144,0.373561,0.667583,0.524095,0.049312,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.254373,0.635752,0.595787,0.191535,0.035544,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.042191,0.630686,1.228984,1.551283,1.067874,0.097927,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.667658,1.298923,1.200739,0.491980,0.032976,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.279461,0.581244,0.360483,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.399924,0.810858,0.936494,0.736365,0.382587,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.283719,0.553112,0.772592,0.446475,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.139188,0.295462,0.285672,0.128550,-0.000000,-0.000000,0.009357,-0.000000,-0.000000,-0.000000,0.081012,0.214530,0.146193,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.103349,0.249238,0.247708,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.516986,1.364277,1.941410,1.411458,0.568820,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.103752,0.625248,0.717754,0.378148,0.178378,0.211172,0.254488,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.212067,0.318507,0.242184,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.157677,0.901028,1.469916,1.762858,1.015188,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.211690,0.610341,0.695972,0.760141,0.872773,0.935694,0.319634,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.032020,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.111879,0.689642,1.195734,1.518524,0.844638,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.003542,0.395981,0.803753,0.720826,0.393036,0.185714,0.167196,0.318346,0.374199,0.258600,0.029526,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.374283,0.779446,0.918402,0.549533,0.185865,0.102974,0.097852,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.179849,0.482070,0.561634,0.263000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.061659,0.175174,0.039255,0.004144,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.144649,0.583792,0.910689,1.031613,0.951483,0.447194,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.109107,0.236147,0.364341,0.329146,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.060394,0.294113,0.459210,0.468438,0.368703,0.040053,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.112856,0.362121,0.529788,0.452106,0.104102,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.104452,0.331992,0.366916,0.198431,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.048560,0.230534,0.402397,0.424875,0.157558,0.050989,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.257008,0.540725,0.468456,0.253814,0.037694,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.056747,0.177999,0.300793,0.112717,-0.000000,-0.000000,0.011376,0.151555,0.032706,-0.000000,-0.000000,-0.000000,-0.000000,0.036294,0.165339,0.302409,0.240717,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.170075,0.333317,0.534354,0.428871,0.051280,-0.000000,-0.000000,-0.000000,-0.000000,0.028382,0.205511,0.178372,0.178287,0.071614,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.062281,0.312395,0.402878,0.186807,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.009413,0.283602,0.342248,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.048391,0.331663,0.685189,0.707459,0.172722,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.001009,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.010277,0.285335,0.604297,0.801435,0.442810,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.106922,0.392029,0.717855,0.787847,0.500671,0.128316,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.241308,0.473654,0.371757,0.198475,0.133540,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.047179,0.073059,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.215510,0.476095,0.578341,0.783274,0.763393,0.450229,0.098155,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.033514,0.095116,0.138868,0.078652,-0.000000,-0.000000,-0.000000,0.095790,0.113895,0.090456,0.073518,0.006982,-0.000000,0.026240,0.024278,-0.000000,-0.000000,-0.000000,-0.000000,0.018250,0.038794,0.095782,0.098941,0.026338,0.005575,-0.000000,0.000765,0.030429,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.062967,0.469282,1.137591,1.791018,1.292028,0.307578,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,0.070395,0.311419,0.469278,0.398155,0.159010,-0.000000,-0.000000,-0.000000,-0.000000]])
#print np.shape(noveltyC)
"""
(Fs,audio) = UF.wavread('./data_wav/open_004.wav');
noveltyC = noveltyCurve(audio,Fs)
parameterTempogram = {}
parameterTempogram['featureRate'] = 43.066406250000000#featureRate
parameterTempogram['tempoWindow'] = 8
parameterTempogram['BPM'] = np.arange(30,600)
parameterTempogram['stepsize'] = np.ceil(parameterTempogram['featureRate']/5)
temp,freq = NoveltyCurve_to_Tempogram(noveltyC,parameterTempogram)
#print np.shape(temp)
#print freq
"""


            

            

            
    
    
