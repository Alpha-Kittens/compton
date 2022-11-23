import os
from data_loader import read_data
from plots import plot_histogram
import  matplotlib.pyplot as plt


folder = 'data/14 November/'

files = os.listdir(folder)

scatter_channel = []
target_channel = []
calibration_channel = []

for file_name in files:
    if file_name != "Calibration":
        fp = folder + file_name

        data = read_data(fp)

        if data['source'] == 'Cs-main':

            histogram = data['histogram']
            plot_histogram(title=file_name, histogram=histogram)

            '''
            min = int(input('Cut min: '))
            max = int(input('Cut max: '))

            histogram = histogram[min:max]
            plot_histogram(title='cut ' + file_name, histogram=histogram)
            
            sum = 0
            total = 0
            for i in range(len(histogram)):
                sum += histogram[i] * i
                total += histogram[i]
            channel_est = (sum/total) + min
            '''
            channel_est = float(input('channel_est?: '))
            print(file_name + ' ' + str(channel_est))

            if data['detector'] == 'scatter':
                scatter_channel.append((data['angle'].val, channel_est))
            elif data['detector'] == 'target':
                target_channel.append((data['angle'].val, channel_est))
            else:
                raise Exception




print(scatter_channel)
print(target_channel)

#scatter_channel = [(120, 491.7544107268878), (150, 416.50668111231494), (30, 1046.6172727272728), (60, 860.4795787310558), (90, 608.8434737389496)]
#target_channel = [(120, 500.6700356718193), (150, 787.1681547619048), (30, 1138.1482254697287), (60, 1144.8621794871794), (90, 614.7184726522188)]


x_scatter = []
y_scatter = []
x_target = []
y_target = []
y_sum = []

for entry in scatter_channel:
    x_scatter.append(entry[0])
    y_scatter.append(entry[1])

for entry in target_channel:
    x_target.append(entry[0])
    y_target.append(entry[1])

for i in range(len(x_target)):
    if x_target[i] != x_scatter[i]:
        raise Exception('error')
    else:
        y_sum.append(y_target[i] + y_scatter[i])

plt.scatter(x_scatter, y_scatter, label='scatter')
plt.scatter(x_target, y_target, label='target')
plt.legend()
plt.show()
plt.title('sum')
plt.scatter(x_target, y_sum, label='sum')
plt.show()


print(x_scatter)
print(x_target)