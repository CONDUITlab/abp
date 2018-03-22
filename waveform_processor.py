import pywt
import math
import pandas as pd
import numpy as np

class ABPWaveformProcessor():
#     def __init__(self):
        
    def segmenter(self, waveform, level=5, window_multiplier=1):
        DATA_TIME_CONST = 0.004166747
        section_size = math.ceil(13.5 / DATA_TIME_CONST)
        section_size = int((100*2**level / 4)) * window_multiplier
        return np.arange(0, len(waveform), section_size)

    def listCreator(self, levels):
        new_list = []
        for i in range(levels, 0, -1):
            new_list.append(["cA{0}".format(i),"cD{0}".format(i)])
        return new_list
        
    def generateSWTCoeffs(self, waveform, level=5):
        return pywt.swt(waveform, pywt.Wavelet('db4'), level=level)

    def calcEnergy(self, coeff):
        return np.sqrt(np.sum(np.array(coeff ** 2)) / len(coeff))

    def processWaveform(self, waveform, level, window_multiplier, column_name="AR1"):
        energy = {}

        for label in self.listCreator(level):
            energy[label[0]] = []
            energy[label[1]] = []

        segments = self.segmenter(waveform, level, window_multiplier)

        for i in range(1, len(segments)):
            if (isinstance(waveform, pd.Series)):
                signal = waveform.iloc[segments[i-1]:segments[i]]
            else:
                signal = waveform.iloc[segments[i-1]:segments[i]][column_name]

            for coeff, label in zip(self.generateSWTCoeffs(signal, level), self.listCreator(level)):
                for single_coeff, single_label in zip(coeff, label):
                    nrgCoeff = self.calcEnergy(single_coeff)
                    energy[single_label].append(nrgCoeff)

        return pd.DataFrame(data=energy)
    
#     def processWaveformPartial(self, waveform, level, window_multiplier, partial=True):
#         energy = {}

#         for label in self.listCreator(level):
#             energy[label[0]] = []
#             energy[label[1]] = []

#         segments = self.segmenter(waveform, level, window_multiplier)

#         for i in range(1, len(segments)):
#             if not partial:
#                 signal = waveform.iloc[segments[i-1]:segments[i]]['AR1']
#             else:
#                 signal = waveform.iloc[segments[i-1]:segments[i]]
            
#             for coeff, label in zip(self.generateSWTCoeffs(signal, level), self.listCreator(level)):
#                 for single_coeff, single_label in zip(coeff, label):
#                     nrgCoeff = self.calcEnergy(single_coeff)
#                     energy[single_label].append(nrgCoeff)

#         return pd.DataFrame(data=energy)
    
    def segment_waves_with_labels(self, ecg_signal, abp_signal):
        seg_waves = ecg.christov_segmenter(signal=ecg_signal.values, sampling_rate=240.)
        R_peaks = np.array(seg_waves).tolist()[0]
        systolic = [] #max
        diastolic = [] #min

        ABP_waves = []
        ABP_waves_len = []

        for i in range(0,len(R_peaks)-1):
            abp_seg = abp_signal[list(range(R_peaks[i],R_peaks[i+1]))]

            abp_max = abp_seg.index.get_loc(abp_seg[abp_seg == abp_seg.max()].index[0])
            abp_min = abp_seg.index.get_loc(abp_seg[abp_seg == abp_seg.min()].index[0])

            ABP_waves.append(abp_seg)

            if systolic == []:
                systolic.append(abp_max + R_peaks[0])
                diastolic.append(abp_min + R_peaks[0])
            else:
                wave_int = sum(ABP_waves_len) + R_peaks[0]
                systolic.append(wave_int + abp_max)
                diastolic.append(wave_int + abp_min)

            ABP_waves_len.append(len(abp_seg))

        return R_peaks, systolic, diastolic