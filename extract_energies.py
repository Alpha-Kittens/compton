from plots import plot_histogram


def get_peak(histogram, label, method='guesstimate'):
    if method == 'guesstimate':
        plot_histogram(title=label, histogram=histogram)

        #num_peaks = int(input("Enter number of peaks to find: "))

        num_peaks = 1

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

