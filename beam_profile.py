import os
from data_loader import read_data
import matplotlib.pyplot as plt
from plots import plot_histogram, plot_data
import math
import lmfit
import numpy as np



folder = 'data/21 November/Beam_profile/'


def get_profile_data(folder, plot=True):
    files = os.listdir(folder)

    cpss = []
    angles = []
    angleserrs = []
    cpsserrs = []
    for file_name in files:
        fp = folder + file_name

        data = read_data(fp)

        histogram = data['histogram']

        angle = data['angle']

        #plot_histogram(title=str(angle), histogram=histogram)

        #counts = sum(histogram)
        #countserr = math.sqrt(counts)

        counts = data['counts'].val
        countserr= data['counts'].tot

        cps = counts/data['time'].val

        cpss.append(cps)
        cpsserrs.append(countserr/data['time'].val)
        angles.append(angle.val)
        angleserrs.append(angle.tot)

    profile_data = [angles, cpss, angleserrs, cpsserrs]

    if plot:
        plot_data(profile_data, label='beam profile', xlabel='Angle (degrees)', ylabel='Counts per second', show=True)

    return profile_data


#def triangle_model(x, aL = 50, aR = -50, x0 = 0, y0 = 1600):
def triangle_model(x, a=50, x0 = 0, y0 = 1600):
    ''''
    the triangle model used for fitting to the beam profile
    '''
    a_L = a
    a_R = -a
    x_0 = x0
    y_0 = y0

    try:
        if x < x0:
            y  = a_L *(x-x0) + y0
        else:
            y = a_R * (x-x0) + y0
        
        if y > 0:
            return y
        else:
            return 0
    except:
        y = []
        for i in x:
            #y.append(triangle_model(i, aL = a_L, aR = a_R, x0 = x_0, y0 = y_0))
            y.append(triangle_model(i, a=a_L, x0 = x_0, y0 = y_0))

        return y


def fit_profile(profile_data):
    model = lmfit.Model(triangle_model)

    y= profile_data[1]
    x=profile_data[0]


    # Propogate x uncertainties into y uncertaintes
    slope = 50  #make sure this matches intial guess in triangle model

    angle_y_errors = []
    for i in profile_data[2]:
        angle_y_errors.append(abs(slope * i))
    
    yerrs = []

    for i in range(len(profile_data[3])):
        yerrs.append(math.sqrt(profile_data[3][i]**2 + angle_y_errors[i]**2))


    data_angle_y_errs = [profile_data[0], profile_data[1], 0, angle_y_errors]
    data_tot_propagated = [profile_data[0], profile_data[1], 0, yerrs]

    plot_data(data_tot_propagated, label='total error', xlabel='Angle (degrees)', ylabel='Counts per second', show=False)
    plot_data(data_angle_y_errs, label='propagated angle error', xlabel='Angle (degrees)', ylabel='Counts per second', show=True)




    weights = 1/np.array(yerrs[3])

    result = model.fit(y, x=x, weights=weights)

    print(lmfit.fit_report(result))
    
    params = result.params
    init_params = result.init_params

    eval = []
    init_eval = []

    xaxis = np.linspace(min(x), max(x), 1000)

    for i in xaxis:
        #eval.append(triangle_model(i, aL=params['aL'].value, aR=params['aR'].value, x0=params['x0'].value, y0=params['y0'].value))
        #init_eval.append(triangle_model(i, aL=init_params['aL'].value, aR=init_params['aR'].value, x0=init_params['x0'].value, y0=init_params['y0'].value))

        eval.append(triangle_model(i, a=params['a'].value,  x0=params['x0'].value, y0=params['y0'].value))
        init_eval.append(triangle_model(i, a=init_params['a'].value, x0=init_params['x0'].value, y0=init_params['y0'].value))

    plt.plot(xaxis, eval, label='fit')
    plt.plot(xaxis, init_eval, label='initial guess')
    plot_data(data_tot_propagated, label='profile data', xlabel='Angle (degrees)', ylabel='Counts per second', show=True)

    residuals = []

    for i in range(len(data_tot_propagated[0])):
        #predicted = triangle_model(data_tot_propagated[0][i], aL=params['aL'].value, aR=params['aR'].value, x0=params['x0'].value, y0=params['y0'].value)
        predicted = triangle_model(data_tot_propagated[0][i], a=params['a'].value, x0=params['x0'].value, y0=params['y0'].value)
        actual = data_tot_propagated[1][i]
        residuals.append(predicted - actual)

    residuals_data = [profile_data[0], residuals, 0, yerrs]

    plt.hlines(0, min(residuals_data[0]), max(residuals_data[0]), colors='red', linestyles='dashed')
    plot_data(residuals_data, label='residuals', xlabel='Angle (degrees)', ylabel='Counts per second', show=True)


profile_data = get_profile_data(folder)
fit_profile(profile_data)
