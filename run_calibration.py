from calibration import*

folder = 'data/'

dates = os.listdir(folder)

for date in dates:
    print(date)
    #data = get_calibration_data(date)

    #get_calibration_fits(date)

plot_calibration_variation(showData = True)
