from calibration import calibrate, uncalibrate
from extract_energies import get_peak
from data_loader import read_data
import os
import matplotlib.pyplot as plt
import math
import numpy as np
from plots import plot_data

dates = os.listdir('data/')

init_energy = 661 # keV
rest_energy_e = 0.511 * (1e3) #keV

def rad(angle):
    return (math.pi * angle)/180

def compton_prediction_photon(angle):
    invE = (1/init_energy) + (1/rest_energy_e)*(1-math.cos(rad(angle)))

    return 1/invE

def compton_prediction_electron(angle):
    return init_energy - compton_prediction_photon(angle)



'''
SAVED INFORMATION ABOUT PEAKS
'''
# Via Guesstimate Method
'''
channel_peaks = {
    '14 November' : {
        'target': [
            [150, 30, 60, 90], 
            [790.0, 275.0, 445.0, 625.0], 
            [3.0, 3.0, 3.0, 3.0], 
            [10, 10, 10, 10]], 
        'scatter': [
            [150, 30, 60, 90], 
            [440.0, 1060.0, 890.0, 645.0], 
            [3.0, 3.0, 3.0, 3.0], 
            [10, 10, 10, 10]]},

    '16 November': {
        'target': [
            [15, 45], 
            [450.0, 375.0], 
            [3.0, 3.0], 
            [10, 10]], 
        'scatter': [
            [15, 45], 
            [1100.0, 1180.0], 
            [3.0, 3.0], 
            [10, 10]]},

    '18 November': {
        'target': [[0], [420.0], [3.0], [10]], 
        'scatter': [[0], [1150.0], [3.0], [10]]},
    
    '21 November': {
        'target': [
            [-30, -60, -90, 120], 
            [300.0, 540.0, 820.0, 1000.0], 
            [3.0, 3.0, 3.0, 3.0], 
            [10, 10, 10, 10]], 
        'scatter': [
            [-30, -60, -90, 120], 
            [1260.0, 1020.0, 770.0, 550.0], 
            [3.0, 3.0, 3.0, 3.0], 
            [10, 10, 10, 10]]}
}
'''

#Via Peak Fitting Method
channel_peaks = {
    '14 November' : {
        'target': [
            [150, 30, 60, 90], 
            [790.9272089051133, 271.4729702426541, 431.21690942823597, 627.7046365259916], 
            [3.0, 3.0, 3.0, 3.0], 
            [1.0962843298719873, 2.892614203151565, 1.5184902978171828, 1.4502451556813605]], 
        'scatter': [
            [150, 30, 60, 90], 
            [429.40673587461697, 1061.8789778800121, 878.802512930587, 636.5401056124769], 
            [3.0, 3.0, 3.0, 3.0], 
            [2.7143044177632083, 3.1460798322401153, 2.6979125324334516, 2.1695938112311914]]},
    '16 November': {
        'target': [
            [15, 45], 
            [442.2487649126026, 379.66539327482144], 
            [3.0, 3.0], 
            [1.7261000457267448, 2.114916311825555]], 
        'scatter': [
            [15, 45], 
            [1101.86859352851, 1176.976339550449], 
            [3.0, 3.0], 
            [2.331468769754514, 1.9792670657160563]]},
    '18 November': {
        'target': [[0], [408.3461478882692], [3.0], [6.7611503557080805]], 
        'scatter': [[0], [1135.663989851356], [3.0], [4.368555721013384]]},
    '21 November': {
        'target': [
            [-30, -60, -90, 120], 
            [299.4280843299289, 536.6959690163543, 816.0744008816902, 1002.6052945297896], 
            [3.0, 3.0, 3.0, 3.0], 
            [2.2008251824796212, 3.3436862051031953, 2.6581903441589034, 1.6875452995587925]], 
        'scatter': [
            [-30, -60, -90, 120], 
            [1265.320217694648, 1036.5830772521804, 756.922764692871, 545.4782963458681], 
            [3.0, 3.0, 3.0, 3.0], 
            [3.4791207684489645, 11.580881765299742, 4.715301571609517, 1.5666072355957783]]}
}


# From beam profile
center = -2.52974745
center_error = 0.55610793

'''
END OF SAVED DATA
'''

radius = 8 # measured in inches
detector_width = 1 # measured in inches
def scattering_angle_error(angle):
    theta1 = math.atan2((detector_width + radius*math.sin(rad(angle)) + detector_width*math.cos(rad(angle))),(radius*math.cos(rad(angle)) - detector_width*math.sin(rad(angle)))) + math.atan(detector_width/radius)

    return (((180/math.pi)*theta1) - angle) * (1/math.sqrt(12))* 2

def plot_scattering_angle_error():
    angle = np.linspace(-180, 180, 1000)
    uncertainty = []
    for i in angle:
        uncertainty.append(scattering_angle_error(i))
    
    total = []
    center_errors = []
    for i in uncertainty:
        center_errors.append(center_error)
        total.append(math.sqrt(i**2 + center_error**2))

    plt.plot(angle, uncertainty, label='scattering angle uncertainty')
    plt.plot(angle, center_errors, label='center angle uncertainty')
    plt.plot(angle, total, label='total angle uncertainty')
    plt.xlabel('Measured Angle (degrees)')
    plt.ylabel('Uncertainty in Scattering Angle (degrees)')
    plt.legend()
    plt.show()


def compton_slope_photon(angle):
    angle_min = angle - 0.001
    angle_max = angle + 0.001

    return (compton_prediction_photon(angle_max) - compton_prediction_photon(angle_min)) / (angle_max-angle_min)

def compton_slope_electron(angle):
    angle_min = angle - 0.001
    angle_max = angle + 0.001

    return (compton_prediction_electron(angle_max) - compton_prediction_electron(angle_min)) / (angle_max-angle_min)

def plot_slope():
    angle = np.linspace(-170, 170, 1000)

    photon_slope = []
    electron_slope = []

    for i in angle:
        photon_slope.append(compton_slope_photon(i))
        electron_slope.append(compton_slope_electron(i))
    
    plt.plot(angle, photon_slope, label='scatter')
    plt.plot(angle, electron_slope, label='target')
    plt.legend()
    plt.show()



def find_channel_peaks(date):
    target_angles = []
    scatter_angles = []
    target_angle_errs = []
    scatter_angle_errs = []

    target_channels = []
    target_channel_errs = []
    scatter_channels = []
    scatter_channel_errs = []

    folder = 'data/' + date + '/'
    files = os.listdir(folder)

    for file_name in files:
            fp = folder + file_name
            if '.Spe' in file_name:
                data = read_data(fp)

                histogram = data['histogram']
                angle = data['angle']
                detector = data['detector']

                peak = get_peak(histogram, label= detector + ' ' + str(angle), method='gaussian fit')

                channel = peak[0]
                channel_err = peak[1]

                if detector == 'scatter':
                    scatter_angles.append(angle.val)
                    scatter_angle_errs.append(angle.tot)
                    scatter_channels.append(channel)
                    scatter_channel_errs.append(channel_err)
                elif detector == 'target':
                    target_angles.append(angle.val)
                    target_angle_errs.append(angle.tot)
                    target_channels.append(channel)
                    target_channel_errs.append(channel_err)
    target_data = [target_angles, target_channels, target_angle_errs, target_channel_errs]
    scatter_data = [scatter_angles, scatter_channels, scatter_angle_errs, scatter_channel_errs]


    data = {
        'target' : target_data,
        'scatter': scatter_data
    }
    print(data)
    return data



def get_scattering_data(plot=True, plot_daily_variation = False):
    angles = []
    target_energies = []
    angle_errs = []
    scatter_energies = []
    target_energy_errs = []
    scatter_energy_errs = []

    sum_energies = []
    sum_energy_errs = []

    colors = ['red', 'blue', 'green', 'purple']
    color_index = 0

    if plot_daily_variation:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
        fig.suptitle('Variation between Days')

    for date in channel_peaks:
        target = channel_peaks[date]['target']
        scatter = channel_peaks[date]['scatter']

        energies_target = []
        energies_scatter = []
        sums = []
        angle_err = []
        if target[0] != scatter[0]:
            print('Mismatch in angles')
            print(target[0])
            print(scatter[0])
            raise Exception
        else:
            for i in range(len(target[0])):

                # shift the center
                target[0][i] = target[0][i] + center
                scatter[0][i] = scatter[0][i] + center


                target_channel = target[1][i]
                target_channel_err = target[3][i]
                scatter_channel = scatter[1][i]
                scatter_channel_err = scatter[3][i]
            
                targetenergy,targetenergyerr = calibrate(channel_number=target_channel, channel_err=target_channel_err, detector='target', date=date)
                scatterenergy,scaterenergyerr = calibrate(channel_number=scatter_channel, channel_err=scatter_channel_err, detector='scatter', date=date)

                energies_target.append(targetenergy)
                target_energy_errs.append(targetenergyerr)
                energies_scatter.append(scatterenergy)
                scatter_energy_errs.append(scaterenergyerr)
        
                sums.append(scatterenergy + targetenergy)
                sum_energy_errs.append(math.sqrt(scaterenergyerr **2 + targetenergyerr**2))

                angle_err.append(math.sqrt((scattering_angle_error(angle=target[0][i]))**2 + center_error**2))
            
            angles = angles + target[0]
            angle_errs = angle_errs + angle_err
        

        scatter_energies = scatter_energies + energies_scatter
        target_energies = target_energies + energies_target
        sum_energies = sum_energies + sums

        if plot_daily_variation:
            ax1.errorbar(target[0], sums, label=date, color=colors[color_index], fmt='o')
            ax2.errorbar(target[0], energies_scatter, label=date, color=colors[color_index], fmt='o')
            ax3.errorbar(target[0], energies_target, label=date, color=colors[color_index], fmt='o')
            ax1.set_title('Sums')
            ax2.set_title('Scatter')
            ax3.set_title('Target')

            ax1.set(xlabel='Angle (degrees)')
            ax1.set(ylabel='Energy (keV)')
            ax2.set(xlabel='Angle (degrees)')
            ax3.set(xlabel='Angle (degrees)')


            color_index +=1
    if plot_daily_variation:
        plt.legend()
        plt.show()
        
    scatter_data = [angles, scatter_energies, angle_errs, scatter_energy_errs]
    target_data = [angles, target_energies, angle_errs, target_energy_errs]
    sum_data = [angles, sum_energies, angle_errs, sum_energy_errs]

    if plot:
        plot_data(scatter_data, label = 'scatter', xlabel='Angle (degrees)', ylabel='Energy (keV)')
        plot_data(target_data, label='target', xlabel='Angle (degrees)', ylabel='Energy (keV)')
        plot_data(sum_data, label='sum', xlabel='Angle (degrees)', ylabel='Energy (keV)', show=True)

    return target_data,scatter_data, sum_data


def compare_photon_compton():
    target, scatter, sum = get_scattering_data(plot=False)

    invScattEnergy = []
    invScatterEnergyErr = []

    for i in range(len(scatter[1])):
        invScattEnergy.append(1/scatter[1][i])
        invScatterEnergyErr.append(abs(scatter[3][i]/((scatter[1][i])**2)))


    scatterx = []
    scatterxerr = []

    for i in range(len(scatter[0])):
        scatterx.append(1-math.cos(rad(scatter[0][i])))
        scatterxerr.append(abs(math.sin(rad(scatter[0][i]) * rad(scatter[2][i]))))


    
    scatter_data = [scatterx, invScattEnergy, scatterxerr, invScatterEnergyErr]


    scatter_eval = []
    predicted_x = []
    x = np.linspace(min(scatter[0]), max(scatter[0]), 1000)

    for i in x:
        scatter_eval.append(1/compton_prediction_photon(i))
        predicted_x.append(1-math.cos(rad(i)))

    plt.plot(predicted_x, scatter_eval, label='compton scattering prediction')
    plot_data(scatter_data, label='scatter data', xlabel='1-cos(Angle)', ylabel='1/Energy (1/keV)', show=True)


def compare_with_compton(target_data, scatter_data, residual_plot = False):
    #target, scatter, sum = get_scattering_data(plot=False)

    x = np.linspace(min(scatter_data[0]), max(scatter_data[0]), 1000)
    target_eval = []
    scatter_eval = []
    for i in x:
        target_eval.append(compton_prediction_electron(i))
        scatter_eval.append(compton_prediction_photon(i))

    plt.plot(x, target_eval, label='compton target prediction')
    plt.plot(x, scatter_eval, label='compton scatter prediction')

    plot_data(target_data, 'target data', xlabel='Angle (degrees)', ylabel='Energy (keV)')
    plot_data(scatter_data, 'scatter data', xlabel='Angle (degrees)', ylabel='Energy (keV)', show=True)

    if residual_plot:
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

        residuals_target = []
        residuals_scatter = []

        for i in range(len(scatter_data[0])):
            residuals_target.append(target_data[1][i] - compton_prediction_electron(target_data[0][i]))
            residuals_scatter.append(scatter_data[1][i] - compton_prediction_photon(scatter_data[0][i]))
    
        target_residual_data = [target_data[0], residuals_target, 0, target_data[3]]
        scatter_residual_data = [scatter_data[0], residuals_scatter, 0, scatter_data[3]]

        ax1.errorbar(target_data[0], residuals_target, yerr=target_data[3], fmt='o')
        ax1.set(title='Target Residuals', xlabel='Angle (degrees)', ylabel='Energy (keV)')
        ax2.errorbar(scatter_data[0], residuals_scatter, yerr=scatter_data[3], fmt='o')
        ax2.set(title='Scatter Residuals', xlabel='Angle (degrees)', ylabel='Energy (keV)')
        ax1.hlines(0, min(target_data[0]), max(target_data[0]), colors='red', linestyles = 'dashed')
        ax2.hlines(0, min(target_data[0]), max(target_data[0]), colors='red', linestyles = 'dashed')

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

        ax1.errorbar(target_data[0], np.array(residuals_target)/np.array(target_data[3]), yerr=1, fmt='o')
        ax1.set(title='Target Residuals (normalized by error)', xlabel='Angle (degrees)', ylabel='Energy (keV)')
        ax2.errorbar(scatter_data[0], np.array(residuals_scatter)/np.array(scatter_data[3]), yerr=1, fmt='o')
        ax2.set(title='Scatter Residuals (normalized by error)', xlabel='Angle (degrees)', ylabel='Energy (keV)')
        ax1.hlines(0, min(target_data[0]), max(target_data[0]), colors='red', linestyles = 'dashed')
        ax2.hlines(0, min(target_data[0]), max(target_data[0]), colors='red', linestyles = 'dashed')

        plt.show()


        


def propogate_angle_error(data, detector):
    init_y_err = data[3]
    angle_err = data[2]
    propagated_angle_err = []
    angle = data[0]
    for i in range(len(angle)):
        if detector == 'target':
            propagated_angle_err.append(abs(compton_slope_electron(angle[i]) * angle_err[i]))
        elif detector == 'scatter':
            propagated_angle_err.append(abs(compton_slope_photon(angle[i]) * angle_err[i]))
    
    
    total_error = []
    for i in range(len(init_y_err)):
        total_error.append(math.sqrt(init_y_err[i]**2 + propagated_angle_err[i]**2))
    
    return total_error


def get_final_data(target_data, scatter_data):
    new_errors_target = propogate_angle_error(target_data, 'target')
    new_errors_scatter = propogate_angle_error(scatter_data, 'scatter')

    #new_target = [target_data[0], target_data[1], 0, new_errors_target]
    #new_scatter = [scatter_data[0], scatter_data[1], 0, new_errors_scatter]

    final_angle = []
    final_target_err = []
    final_scatter_err = []
    final_target = []
    final_scatter = []
    for i in range(len(target_data[0])):
        if abs(target_data[0][i]) > 20:
            final_angle.append(target_data[0][i])
            final_target_err.append(new_errors_target[i])
            final_scatter_err.append(new_errors_scatter[i])
            final_target.append(target_data[1][i])
            final_scatter.append(scatter_data[1][i])
    
    final_target_data = [final_angle, final_target, 0, final_target_err]
    final_scatter_data = [final_angle, final_scatter, 0, final_scatter_err]

    return final_target_data, final_scatter_data




def uncalibrate_prediction_plot():
    target, scatter, sum = get_scattering_data(plot=False)

    x = np.linspace(min(scatter[0]), max(scatter[0]), 1000)

    colors = ['blue', 'purple', 'green', 'red']
    colorindex = 0

    for date in channel_peaks:
        target_eval = []
        scatter_eval = []
        for i in x:
            target_eval.append(uncalibrate(energy=compton_prediction_electron(i), energy_err=0, detector='target', date=date)[0])
            scatter_eval.append(uncalibrate(energy=compton_prediction_photon(i), energy_err=0, detector='scatter', date=date)[0])

        plot_data(data=channel_peaks[date]['target'], label='target data ' + date, color=colors[colorindex])
        plot_data(data=channel_peaks[date]['scatter'], label='scatter data ' + date, color=colors[colorindex])        
        
        plt.plot(x, target_eval, label='compton target prediction ' + date, color=colors[colorindex])
        plt.plot(x, scatter_eval, label='compton scatter prediction ' + date, color=colors[colorindex])

        colorindex +=1
    
    plt.hlines(y=60, xmin = min(x), xmax=max(x), colors='black', linestyles='dashed', label='discrimnator value')
    plt.xlabel('Angle (degrees)')
    plt.ylabel('channel number')
    #plt.legend()
    plt.show()



plot_scattering_angle_error()
plot_slope()
#find_channel_peaks(date='16 November')
target_data, scatter_data, sum_data = get_scattering_data(plot_daily_variation=True)
#compare_photon_compton()
compare_with_compton(target_data, scatter_data)

final_target_data, final_scatter_data = get_final_data(target_data, scatter_data)
compare_with_compton(final_target_data, final_scatter_data, residual_plot=True)

#uncalibrate_prediction_plot()