import os
from data_loader import read_data
import matplotlib.pyplot as plt
import lmfit
import numpy as np
import math


# Reference Values for the energies (in KeV)
ref = {
    'Ba1' : 81,
#    'Ba2' : 302,
    'Ba3' : 356,
    'Na' : 511,
    'Cs' : 661.6
}

''''
SAVED CALIBRATION RESULTS
'''
# Via Guesstimate Method
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

# Via fit to Gaussian
peaks_Nov_14 = {
    'target': {
        'Ba1': (161.88001005238647, 0.031422131833220686), 
 #       'Ba2': (548.8559099384635, 3.393309077356663), 
        'Ba3': (636.4006524767566, 0.3774946788271212), 
        'Cs': (1158.1298861829785, 0.22370463100880328), 
        'Na': (893.2684036745927, 0.6894125828192137)}, 
    'scatter': {
        'Ba1': (190.9068689039409, 0.09209318022780594), 
#        'Ba2': (743.6553190589032, 204.9904060775206), 
        'Ba3': (778.9771572322662, 0.2833927584838565), 
        'Cs': (1421.0702371782515, 0.16571415768378617), 
        'Na': (1105.0268713544751, 0.7383069060949691)}}

peaks_Nov_16 = {
    'target': {
        'Ba1': (209.99666577377948, 0.040072151581956275), 
#       'Ba2': (747.8496322836918, 44.506845808830356), 
        'Ba3': (826.6985855394092, 0.7790032828614307), 
        'Cs': (1497.9458439775303, 0.28715412515491784), 
        'Na': (1157.1784668122707, 0.9566635218500149)}, 
    'scatter': {
        'Ba1': (212.3641268148477, 0.11985293598136058), 
#        'Ba2': (825.7770737429115, 357.29241423245963), 
        'Ba3': (863.850383903636, 0.38421319995289616), 
        'Cs': (1579.0581161866075, 0.20484924597089502), 
        'Na': (1248.0216347498892, 0.731570332940858)}}

peaks_Nov_18 = {
    'target': {
        'Ba1': (202.16898266424752, 0.08301537729186004), 
 #       'Ba2': (682.597302492776, 2.2695774189428124), 
        'Ba3': (801.0847742357267, 0.7422499082006716), 
        'Cs': (1449.2613836195883, 0.16954041906621325), 
        'Na': (1132.7139102687252, 0.21039666286241554)}, 
    'scatter': {
        'Ba1': (222.43356802011436, 0.11511826621535487), 
  #      'Ba2': (785.6157770897626, 9.13955131673307), 
        'Ba3': (903.6833375597186, 0.4905505962065723), 
        'Cs': (1644.4466422479006, 0.16214775586020586), 
        'Na': (1272.4883071716233, 0.1722320126555845)}}

peaks_Nov_21 = {
    'target': {
        'Ba1': (218.2145067822758, 0.19005949687145637),
  #      'Ba2': (712.1593522736265, 7.118021075877319), 
        'Ba3': (854.1762009136447, 1.334535834881867), 
        'Cs': (1557.8244709284977, 1.837032052197228), 
        'Na': (1206.0695116805873, 0.7747927139922606)}, 
    'scatter': {
        'Ba1': (216.33660682900188, 0.17593653367235534), 
  #      'Ba2': (814.355852892429, 95.46292225624342), 
        'Ba3': (882.8570693741001, 0.33231210393216737), 
        'Cs': (1601.324513933364, 0.19270585533945073), 
        'Na': (1232.6363627767043, 0.7239223186881438)}}


calibration_functions = {
    '14 November' : {
        'target': (1.8503065482324255, 0.06927871774683134), 
        'scatter': (2.1602929430031854, 0.024411862686265322)},
    '16 November' : {
        'target': (2.4010691222563194, 0.09289193801262162), 
        'scatter': (2.400512847336903, 0.026502262470290635)},
    '18 November' : {
        'target': (2.2110943677955457, 0.035469491644688794), 
        'scatter': (2.49302489201182, 0.020627404884269406)},
    '21 November' : {
        'target': (2.4369006700969056, 0.0796090463064427), 
        'scatter': (2.428982461736441, 0.020009080060996873)}
}



calibration_data = {
    '14 November' : peaks_Nov_14,
    '16 November' : peaks_Nov_16,
    '18 November' : peaks_Nov_18,
    '21 November' : peaks_Nov_21
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
        
        if source == "Ba":
            peak = get_peak(histogram, label = file_name, method='gaussian fit', num_peaks=3)

            for i in range(len(peak)):
                peaks[detector]['Ba' + str(i+1)] = peak[i]
        else:
            peak = get_peak(histogram, label = file_name, method='gaussian fit')

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
    

def fit_calibration_peaks(peaks, plot=True, title=None):
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
        if title is not None:
            plot_fit_linear(xaxis, y, weightsy, a, plot_residuals=True, title=title)
        else:
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
    
    a_target, a_err_target = fit_calibration_peaks(peaks['target'], plot=True, title='target  ' +  date)
    a_scatter, a_err_scatter = fit_calibration_peaks(peaks['scatter'], plot=True, title='scatter ' +  date)

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

    inva = 1/a
    invaerr = a_error/(a**2)

    # Note that we have fit a slope energy --> calibration so we need 1/a to conver the other way
    error = math.sqrt(((invaerr) * channel_number)**2 + (inva * channel_err)**2)



    return linear(x=channel_number, a=(1/a)), error

def uncalibrate(energy, energy_err, detector, date):
    a = calibration_functions[date][detector][0]
    a_error = calibration_functions[date][detector][1]

    error = math.sqrt(((a_error) * energy)**2 + (a * energy_err)**2)
    return linear(x=energy, a=a), error

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



    



