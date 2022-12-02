from calibration import*

folder = 'data/'

dates = os.listdir(folder)

for date in dates:
    print(date)
    get_calibration_data(date)
    get_calibration_fits(date)

plot_calibration_variation(showData = True)

print(calibrate(1500, channel_err=10, detector='target', date='16 November'))