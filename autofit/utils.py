import timeit
import multiprocessing
import numpy as np

#freq, dipoles, constants, constraints, J_min="00", inten="-10.0"):
test_case = """\
constants = {'A': 3000, 'B':2000, 'C': 1000, 'delta_J':2E-4, 'delta_JK':2E-4, 'delta_K':2E-4, 'd_J':2E-4, 'd_K':2E-4, 'spin':0}
dipoles = {'mu_A': 1, 'mu_B': 1, 'mu_C': 1}
constraints = {'maxJ': 20, 'temp': 2,}
int_writer(dipoles=dipoles, constants=constants, constraints=constraints,
           inten="-10.0", freq="100.0")
var_writer(constants)
run_spcat()
"""
def time_estimate():

    outtime = timeit.timeit(stmt=test_case, number=25, setup="from autofit.IO.spcat import int_writer,var_writer,run_spcat")
    scale_factor_one_proc = outtime / 25.0  # Rought estimated time in seconds for a single triple on one core.
    cores_detected = multiprocessing.cpu_count()
    scale_factor = scale_factor_one_proc / cores_detected  # Rough estimated time in seconds for a single triple, divided by number of processors.

    return scale_factor


def peakutils_indexes(y, max_peaks=50, radius=3, thres=.1):
    '''adapted from peakutils.indexs function package by Lucas Hermann Negri
    http://pythonhosted.org/PeakUtils/index.html
    primary difference as it only processes a max number of highest peaks'''
    thres = thres * (np.max(y) - np.min(y)) + np.min(y)

    # find the peaks by using the first order difference
    dy = np.diff(y)
    # this determines where the curve changes direction and
    # is above thres
    peaks = np.where((np.hstack([dy, 0.]) < 0.)
                     & (np.hstack([0., dy]) > 0.)
                     & (y > thres))[0]

    if peaks.size > 1 and radius > 1:
        highest = peaks[np.argsort(y[peaks])][::-1][:max_peaks]
        rem = np.ones(y.size, dtype=bool)
        rem[highest] = False

        for peak in highest:
            if not rem[peak]:
                sl = slice(max(0, peak - radius), peak + radius + 1)
                rem[sl] = True
                rem[peak] = False

        peaks = np.arange(y.size)[~rem]

    return peaks



def cat_reader(freq_high, freq_low, flag):  # reads output from SPCAT

    if flag == "default":
        fh = open("default.cat")

    if flag == "refit":
        fh = open("refit.cat")

    linelist = []
    for line in fh:
        if line[8:9] == ".":
            freq = line[3:13]
            inten = line[22:29]
            qnum_up = line[55:61]
            qnum_low = line[67:73]
            uncert = line[13:21]
            if float(freq) > freq_low and float(freq) < freq_high:  # <<<<<<<<<<<<<<<<<<<<
                linelist.append((inten, freq, qnum_up, qnum_low, uncert))
    linelist.sort()
    fh.close()
    return linelist


def trans_freq_reader(trans_1, trans_2, trans_3):
    peak_1_freq = 0
    peak_2_freq = 0
    peak_3_freq = 0

    pred_peaks = cat_reader(1000000, 0, flag="default")
    for peak in pred_peaks:
        if trans_1[2] == peak[2] and trans_1[3] == peak[3]:
            peak_1_freq = peak[1]
        if trans_2[2] == peak[2] and trans_2[3] == peak[3]:
            peak_2_freq = peak[1]
        if trans_3[2] == peak[2] and trans_3[3] == peak[3]:
            peak_3_freq = peak[1]
    return peak_1_freq, peak_2_freq, peak_3_freq



if __name__ == '__main__':
    from matplotlib import pyplot as plt
    fname = "C:\\Users\\mtm5k\\Dropbox (BrightSpec)\\BrightSpec_Data\\ReferenceSpectra\\dataK-reference\\ammonia_100k_0.98mT_HDR.fft"
    data = np.loadtxt(fname, skiprows=29, delimiter=',')
    print(np.shape(data))
    pp = peakutils_indexes(data[:,1])

    plt.plot(data[:, 0], data[:, 1])
    plt.vlines(data[pp, 0], 0, max(data[:, 1]))
    plt.show()
