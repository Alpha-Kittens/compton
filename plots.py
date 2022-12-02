import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(title, histogram, xaxis=None, vlines = [], show=True):
    plt.title("Energy channel histogram for " + title)
    plt.xlabel("MCA channel")
    plt.ylabel("Particle counts")
    plt.plot([], [], color = 'blue', label = "Poisson errors on counts")
    if xaxis is not None:
        plt.bar(xaxis, histogram, width = 1, color = 'cyan', ecolor = 'blue', label = "Histogram data", yerr = np.sqrt(histogram))
    else:
        plt.bar(range(len(histogram)), histogram, width = 1, color = 'cyan', ecolor = 'blue', label = "Histogram data", yerr = np.sqrt(histogram))
    for label, x, color in vlines:
        plt.axvline(x, color = color, label = label, ls = '--')
    plt.legend()
    if show:
        plt.show()


def plot_data(data, label, xlabel=None, ylabel=None, color = None, show=False):
    x = data[0]
    y = data[1]
    xerr = data[2]
    yerr = data[3]

    if color is not None:
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, label=label, fmt='o', color=color)
    else:
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, label=label, fmt='o')

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    if show:
        plt.legend()
        plt.show()


def plot_loaded_entry(info):
    plt.title("Energy channel histogram for "+info['detector']+" detector at scattering angle "+str(info['angle'].val))
    plt.xlabel("MCA channel")
    plt.ylabel("Particle counts")
    plt.plot([], [], color = 'blue', label = "Poisson errors on counts")
    plt.bar(range(len(info['histogram'])), info['histogram'], width = 1, color = 'cyan', ecolor = 'blue', label = "Histogram data", yerr = np.sqrt(info['histogram']))
    plt.legend()
    plt.show()

def plotting_unpack(results, mode = 'tot'):
    """
    Given an array of `Result` objects, returns array of values and errors usable with `plt.errorbar`. 
    Arguments:
        * `results` (array): array of `Result` objects.
        * `mode` (string): specifying which error to use. 
            - `tot`: total error (default)
            - `stat`: statistical error
            - `sys`: systematic error
    Returns:
        * `x`: array of values
        * `xerr`: array of errors associated with `x`
    """
    x = []
    xerr = []
    for result in results:
        x.append(result.val)
        if mode == 'tot':
            xerr.append(result.tot)
        elif mode == 'stat':
            xerr.append(result.stat)
        elif mode == 'sys':
            xerr.append(result.sys)
    return x, xerr