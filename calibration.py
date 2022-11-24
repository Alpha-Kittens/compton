import os
from data_loader import read_data
import matplotlib.pyplot as plt
import lmfit
import numpy as np
import math


# Reference Values for the energies (in KeV)
ref = {
    'Ba1' : 81,
    'Ba2' : 302,
    'Ba3' : 356,
    'Na' : 511,
    'Cs' : 661.6
}

''''
SAVED CALIBRATION RESULTS
'''
peaks_Nov_14 = {
    'target': {'Ba1': (160.0, 10), 'Ba2': (545.0, 10), 'Ba3': (640.0, 10), 'Cs': (1160.0, 10), 'Na': (890.0, 10)}, 
    'scatter': {'Ba1': (190.0, 10), 'Ba2': (660.0, 10), 'Ba3': (775.0, 10), 'Cs': (1420.0, 10), 'Na': (1110.0, 10)}}
peaks_Nov_16 = {
    'target': {'Ba1': (210.0, 10), 'Ba2': (710.0, 10), 'Ba3': (820.0, 10), 'Cs': (1500.0, 10), 'Na': (1160.0, 10)}, 
    'scatter': {'Ba1': (210.0, 10), 'Ba2': (740.0, 10), 'Ba3': (865.0, 10), 'Cs': (1580.0, 10), 'Na': (1250.0, 10)}}
peaks_Nov_18 = {
    'target': {'Ba1': (200.0, 10), 'Ba2': (675.0, 10), 'Ba3': (800.0, 10), 'Cs': (1450.0, 10), 'Na': (1140.0, 10)}, 
    'scatter': {'Ba1': (220.0, 10), 'Ba2': (775.0, 10), 'Ba3': (900.0, 10), 'Cs': (1640.0, 10), 'Na': (1270.0, 10)}}
peaks_Nov_21 = {
    'target': {'Ba1': (218.0, 10), 'Ba2': (725.0, 10), 'Ba3': (850.0, 10), 'Cs': (1560.0, 10), 'Na': (1210.0, 10)}, 
    'scatter': {'Ba1': (215.0, 10), 'Ba2': (750.0, 10), 'Ba3': (880.0, 10), 'Cs': (1600.0, 10), 'Na': (1230.0, 10)}}

calibration_data = {
    '14 November' : peaks_Nov_14,
    '16 November' : peaks_Nov_16,
    '18 November' : peaks_Nov_18,
    '21 November' : peaks_Nov_21
}

calibration_functions = {
    '14 November' : {
        'target': (1.7627765109984652, 0.014405996477941052), 
        'scatter': (2.16312457089653, 0.010835140633579184)},
    '16 November' : {
        'target': (2.283576857623972, 0.018436318656416265), 
        'scatter': (2.41787025124466, 0.01569955991438144)},
    '18 November' : {
        'target': (2.2166456835560346, 0.015559165406804402), 
        'scatter': (2.4977501165485534, 0.0168917429663934)},
    '21 November' : {
        'target': (2.3714148178693066, 0.01531185383137925), 
        'scatter': (2.4306250803078457, 0.01653343213274613)}
}
'''
END OF SAVED CALIBRATION RESULTS
'''



'''
CALIBRATION FUNCTIONS
'''
def get_calibration_data(date):
    '''
    Returns the calibration for a specific folder datae (e.g 14 Novemeber)
    '''
    folder = 'data/' + date + '/Calibration/'
    files = os.listdir(folder)

    targetpeaks = {}
    scatterpeaks = {}

    peaks = {
        'target' : targetpeaks,
        'scatter' : scatterpeaks
    }

    for file_name in files:
        fp = folder + file_name

        data = read_data(fp)

        detector = data['detector']
        source = data['source']
        histogram = data['histogram']


        from extract_energies import get_peak

        peak = get_peak(histogram, label = file_name, method='guesstimate')

        if source == "Ba":
            for i in range(len(peak)):
                peaks[detector]['Ba' + str(i+1)] = peak[i]
        else:
            peaks[detector][source] = peak

    print(peaks)

    return peaks


def plot_calibration_data(peaks):
    
    xaxis = []
    targety = []
    scattery = []
    targeterrorsy = []
    scattererrorsy = []

    for key in ref:
        xaxis.append(ref[key])
        targety.append(peaks['target'][key][0])
        scattery.append(peaks['scatter'][key][0])
        targeterrorsy.append(peaks['target'][key][1])
        scattererrorsy.append(peaks['scatter'][key][1])

    
    plt.errorbar(x=xaxis, y=targety, yerr=targeterrorsy, label='target', fmt='o')
    plt.errorbar(x=xaxis, y=scattery, yerr=scattererrorsy, label='scatter', fmt='o')
    plt.xlabel('True Energy')
    plt.ylabel('Channel Number')
    plt.legend()
    plt.show()

# Linear model
def linear(x, a=2):
        return a*x
    

def fit_calibration_peaks(peaks, plot=True):
    xaxis = []
    y = []
    weightsy = []

    for key in ref:
        xaxis.append(ref[key])
        y.append(peaks[key][0])
        weightsy.append(1/peaks[key][1])

    model = lmfit.Model(linear)
    result = model.fit(y, x=xaxis, weights=np.array(weightsy))
    params = result.params
    print(lmfit.fit_report(result))
    a = params['a'].value
    erra = params['a'].stderr

    if plot:
        plot_fit_linear(xaxis, y, weightsy, a, plot_residuals=True)
    
    return a, erra

def plot_fit_linear(datax, datay, weightsy, a, plot_residuals = False, color = None, title=None, show=True):
    x=np.linspace(min(datax), max(datax), 1000)
    y_eval = []
    for i in x:
        y_eval.append(linear(i, a=a))
    if color is not None:
        plt.plot(x, y_eval, color = color, label='fit')
    else:
        plt.plot(x, y_eval, label='fit')
    if color is not None:
        plt.errorbar(datax, datay, yerr=1/np.array(weightsy), color=color, fmt='o', label='data')
    else:
        plt.errorbar(datax, datay, yerr=1/np.array(weightsy), fmt='o', label='data')

    if title is not None:
        plt.title(title)

    if show:
        plt.legend()
        plt.show()

    if plot_residuals:
        residuals = []
        for i in range(len(datax)):
            residuals.append(linear(datax[i], a=a) - datay[i])
        plt.hlines(y=0, xmin=min(datax), xmax=max(datax), colors='red', linestyles='dashed')
        plt.errorbar(datax, residuals, yerr=1/np.array(weightsy), fmt='o')
        if title is not None:
            plt.title(title)
        plt.show()


def get_calibration_fits(date, findPeaks = False):
    if findPeaks:
        peaks = get_calibration_data(date)
    else:
        peaks = calibration_data[date]
    
    a_target, a_err_target = fit_calibration_peaks(peaks['target'], plot=True)
    a_scatter, a_err_scatter = fit_calibration_peaks(peaks['scatter'], plot=True)

    fit_results = {
        'target' : (a_target, a_err_target),
        'scatter' : (a_scatter, a_err_scatter)
    }

    print(fit_results)

    return fit_results

def calibrate(channel_number, channel_err, detector, date, refit=False, findPeaks=False):
    if findPeaks:
        peaks = get_calibration_data(date)[detector]
    else:
        peaks = calibration_data[date][detector]
    if refit:
        a, a_error = fit_calibration_peaks(peaks, plot=False)
    else:
        a = calibration_functions[date][detector][0]
        a_error = calibration_functions[date][detector][1]


    # Note that we have fit a slope energy --> calibration so we need 1/a to conver the other way
    error = math.sqrt((a_error * channel_number)**2 + ((1/a) * channel_err)**2)



    return linear(x=channel_number, a=(1/a)), error

def plot_calibration_variation(showData=False):
    plt.title('Variation in Calibration Functions')
    plt.ylabel('Channel Number')
    plt.xlabel('Energy (keV)')

    colors = ['red', 'blue', 'green', 'purple']
    index= 0
    for date in calibration_functions:
        atarget = calibration_functions[date]['target'][0]
        ascatter = calibration_functions[date]['scatter'][0]

        if showData == True:
            xaxis = []
            y = []
            weightsy = []
            peaks = calibration_data[date]['scatter']
            for key in ref:
                xaxis.append(ref[key])
                y.append(peaks[key][0])
                weightsy.append(1/peaks[key][1])
            plot_fit_linear(xaxis, y, weightsy, atarget, plot_residuals=False, color = colors[index], show=False)

            xaxis = []
            y = []
            weightsy = []
            peaks = calibration_data[date]['target']
            for key in ref:
                xaxis.append(ref[key])
                y.append(peaks[key][0])
                weightsy.append(1/peaks[key][1])
            plot_fit_linear(xaxis, y, weightsy, ascatter, plot_residuals=False, color = colors[index], show=False)

        else:
            x=np.linspace(0, 2048, 2000)
            y_evaltarget = []
            y_evalscatter = []
            for i in x:
                y_evaltarget.append(linear(i, a=atarget))
                y_evalscatter.append(linear(i, a=ascatter))
            plt.plot(x, y_evaltarget, color=colors[index], label= key + ' target')
            plt.plot(x, y_evalscatter, color=colors[index], label= key + ' scatter')

        index+=1

    plt.legend()
    plt.show()



    



