import os


folder = 'gold_scattering/'

files = os.listdir(folder)

angles = []
cpss = []
errors = []
for file_name in files:
    fp = folder + file_name