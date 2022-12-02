from plots import plot_histogram
import math
import lmfit
import numpy as np
import matplotlib.pyplot as plt


def get_peak(histogram, label, method='guesstimate', num_peaks = 1):
    if method == 'guesstimate':
        return guesstimate(histogram, label, num_peaks = num_peaks)

    elif method == 'gaussian fit':
        return gaussian_fit(histogram, label, num_peaks = num_peaks)


def guesstimate(histogram, label, num_peaks):
    plot_histogram(title=label, histogram=histogram)

    if num_peaks > 1:
        print('Make sure you enter the peaks in order from smallest to largest')
        peaks = []
        for i in range(num_peaks):
            plot_histogram(title=label, histogram=histogram)
            peak = float(input('Enter peak ' + str(i+1) + ": "))
            error = 10
            peaks.append((peak, error))
        
        return peaks
    else:
        peak = float(input('Enter peak: '))
        error = 10
        
        return peak, error


def gaussian_fit(histogram, label, num_peaks):
    if num_peaks > 1:
        peaks = []
        print('Looking for ' + str(num_peaks) + ' peaks')
        for i in range(num_peaks):
            print('Enter Information for Peak # ' + str(i+1))

             # Determinine Bounds
            plot_histogram(title=label, histogram=histogram)

            minimum = int(input('Enter minimum: '))
            maximum = int(input('Enter maximum: '))
            init_guess = float(input('Initial guess: '))

            new_hist = histogram[minimum:maximum]

            x = []
            for i in range(minimum, maximum):
                x.append(i)

            plt.vlines(init_guess - minimum, min(new_hist), max(new_hist), label='inital guesss', colors='red', linestyles='dashed')
            plot_histogram(title=label, histogram=new_hist)

            center, error = fit_lin_gauss(x, new_hist, init_guess)

            peaks.append((center,error))
        return peaks
    else:
        # Determinine Bounds
        plot_histogram(title=label, histogram=histogram)

        minimum = int(input('Enter minimum: '))
        maximum = int(input('Enter maximum: '))
        init_guess = float(input('Initial guess: '))

        new_hist = histogram[minimum:maximum]

        x = []
        for i in range(minimum, maximum):
            x.append(i)

        plt.vlines(init_guess - minimum, min(new_hist), max(new_hist), label='inital guesss', colors='red', linestyles='dashed')
        plot_histogram(title=label, histogram=new_hist)

        center, error = fit_lin_gauss(x, new_hist, init_guess)

        return center,error



def fit_lin_gauss(x, hist, init_guess):

    init_amp = max(hist)
    def lin_gauss(x, a = 0, b=0, amp = init_amp, cen=init_guess, sigma = 25):
        return (a*x + b) + (amp * np.exp(-0.5*((x-cen)/sigma)**2))

    model = lmfit.Model(lin_gauss)

    weights = []

    for i in hist:
        if i != 0:
            weights.append(1/math.sqrt(i))
        else:
            weights.append(0)

    
    result = model.fit(np.array(hist), x=np.array(x), weights=np.array(weights))

    print(result.fit_report())

    params = result.params
    init_params = result.init_params

    xaxis = np.linspace(min(x), max(x), 1000)
    eval = []
    init_eval = []

    for i in xaxis:
        eval.append(lin_gauss(i, a=params['a'], b=params['b'], amp=params['amp'], cen=params['cen'], sigma=params['sigma']))
        init_eval.append(lin_gauss(i, a=init_params['a'], b=init_params['b'], amp=init_params['amp'], cen=init_params['cen'], sigma=init_params['sigma']))

    plot_histogram(title = '', histogram=hist, xaxis=x, show=False)
    plt.plot(xaxis, eval, label='fit', color='red')
    plt.plot(xaxis, init_eval, label='inital guess')
    plt.legend()
    plt.show()

    return params['cen'].value, params['cen'].stderr
    


