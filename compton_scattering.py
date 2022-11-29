from calibration import calibrate
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


'''
END OF SAVED DATA
'''

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
    angle_errs = []
    target_energies = []
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
        if target[0] != scatter[0]:
            print('Mismatch in angles')
            print(target[0])
            print(scatter[0])
            raise Exception
        else:
            for i in range(len(target[0])):
                target[0][i] = target[0][i] - 2.5
                scatter[0][i] = scatter[0][i] - 2.5


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
            
            angles = angles + target[0]
            angle_errs = angle_errs + target[2]
        

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


def compare_with_compton():
    target, scatter, sum = get_scattering_data(plot=False)

    x = np.linspace(min(scatter[0]), max(scatter[0]), 1000)
    target_eval = []
    scatter_eval = []
    for i in x:
        target_eval.append(compton_prediction_electron(i))
        scatter_eval.append(compton_prediction_photon(i))

    plt.plot(x, target_eval, label='compton target prediction')
    plt.plot(x, scatter_eval, label='compton scatter prediction')

    plot_data(target, 'target data', xlabel='Angle (degrees)', ylabel='Energy (keV)')
    plot_data(scatter, 'scatter data', xlabel='Angle (degrees)', ylabel='Energy (keV)', show=True)





#find_channel_peaks(date='21 November')
get_scattering_data(plot_daily_variation=True)
compare_photon_compton()
compare_with_compton()