from data_loader import *
from results import *
import numpy as np
import os
import matplotlib.pyplot as plt
from plots import *
import lmfit
import math

folder = "data/cps_stuff/"
pfolder = "data/attenuation_stuff/"

###### Constants Etc ######
R = 2 * 2.54 # cm
H = 2 * 2.54 # cm
Z = H # cm

x0 = Result(-2.52974745, stat = 0.55610793)

E_0 = 661.6 # keV
m_e = 510.99895000 # keV

mu = lambda E : (E/100)**(-0.368) * 0.514 + (E/100)**(-2.75) * 5.51 # for NaI. keV
mu_plastic = lambda E : 0.177 * (E / 100)**-0.37
E = lambda theta : ((1 - np.cos(theta)) * E_0/m_e + 1)**-1 * E_0

q = lambda r : r / R
x = lambda r, phi : R * (np.sqrt(1 - (q(r)*np.sin(phi))**2) - q(r) * np.cos(phi))
y = lambda r, psi : R * (np.sqrt(1 - (q(r)*np.sin(psi))**2) - q(r) * np.cos(psi))
psi = lambda theta, phi : np.pi - theta + phi

int_num = lambda r, phi, theta : np.exp(-mu(E(theta)) * x(r, phi)) * np.exp(-mu(E(theta)) * y(r, psi(theta, phi))) * (1 - np.exp(-mu(E(theta)) * H))
int_denom = lambda r, phi, theta : np.exp(-mu(E(theta)) * x(r, phi))

klein_nishina = lambda theta : (E(theta)/E_0)**2 * (E(theta)/E_0 + E_0/E(theta) - np.sin(theta)**2)
chi = lambda theta : np.pi - np.abs(theta)
thomson = lambda theta : (1 + np.cos(chi(theta))**2) / 2

"""testx = np.linspace(0, np.pi, 100)
ky = klein_nishina(testx)
ty = thomson(testx)
plt.plot(testx, ky/np.sum(ky), label = "klein-nishina", color = 'red')
plt.plot(testx, ty/np.sum(ty), label = "thomson", color = 'blue')
plt.legend()
plt.show()"""

def eta(theta, stepsr = 100, stepsphi = 100):
    dr = R / stepsr
    dphi = 2*np.pi / stepsphi
    num = np.zeros(np.shape(theta))
    denom = np.zeros(np.shape(theta))
    for r in np.arange(0, R, dr):
        for phi in np.arange(0, 2*np.pi, dphi):
            num += int_num(r, phi, theta) * r*dr*dphi * Z
            """            if int_num(r, phi, theta)[-1] > 1: 
                print ("Sadge")
                print (x(r, phi))
                print (y(r, psi(theta, phi)))
                print (int_num(r, phi, theta)[-1])"""
            denom += int_denom(r, phi, theta) * r*dr*dphi * Z # uniform in Z
    #print (theta)
    #print (E(theta))
    #print (mu(E(theta)))
    #print (num)
    #print (denom)
    return num / denom



ch_cutoffs = [1742, 1742, 1350, 1350, 949, 949, -1, -1, 860, 860, 610, 610, 1400, 1400, 1320, 1320, 1500, 1500, 1220, 1220, 980, 980]
#ch_cutoffs = [-1 for ch in ch_cutoffs]

def generate_cutoffs():
    cutoffs = []
    for file in os.listdir(folder):
        info = read_data(folder + file)
        if info['detector'] == "scatter":
            plot_loaded_entry(info)
            cutoff = input("Enter approximate channel cutoff: ")
            cutoffs.append(int(cutoff))
        else:
            cutoffs.append(cutoffs[-1]) # scatter -> target
    print (cutoffs)
#generate_cutoffs()

def cps_data(plot = False):
    scatter = {}
    target = {}
    for i, file in enumerate(os.listdir(folder)):
        info = read_data(folder + file)
        #plot_loaded_entry(info)
        #if True:
        if info['detector'] == "scatter" and info['angle'].val == 15:
            dict = scatter if info['detector'] == "scatter" else target
            cut_counts = np.sum(info['histogram'][:ch_cutoffs[i]])
            #print(info['angle'])
            #print(info['counts'])
            #print(cut_counts)
            #print(info['time'])
            if plot:
                #plot_histogram(str(info['angle'])+info['detector'], info['histogram'])
                plt.title("Energy channel histogram for " + str(info['angle'].val) + " " + info['detector'])
                plt.xlabel("MCA channel")
                plt.ylabel("Particle counts")
                plt.plot([], [], color = 'blue', label = "Poisson errors on counts")
                plt.bar(range(len(info['histogram'])), info['histogram']/np.sum(info['histogram']), width = 1, color = 'cyan', ecolor = 'blue', label = "Histogram data", yerr = np.sqrt(info['histogram'])/np.sum(info['histogram']))
                plt.axvline(ch_cutoffs[i], color = 'r', label = "cutoff estimate", ls = '--')
                plt.text(1500, max(info['histogram']/np.sum(info['histogram'])), "time: %.3f" % info['time'].val)
                plt.text(1500, 9/10 * max(info['histogram']/np.sum(info['histogram'])), "cps: %.3f" % info['cps'].val)
                plt.text(1500, 4/5 * max(info['histogram']/np.sum(info['histogram'])), "cut cps: %.3f" % (cut_counts/info['time'].val))
                plt.legend()
                plt.show()

            #print ("==")
            #print (info['angle'])
            #print (info['time'])
            #print (info['counts'])
            #print (cut_counts)
            #print (info['counts'] / info['time'])
            dict[info['angle'].val] = info['angle'], Result(cut_counts, stat = np.sqrt(cut_counts)) / info['time']
    return target, scatter

rad = lambda deg : deg * np.pi / 180
deg = lambda rad : rad * 180 / np.pi
def plot_cps(useeta = True):
    target, scatter = cps_data()
    tx = []
    ty = []
    for key, (angle, cps) in target.items():
        print(angle, "|", cps)
        tx.append(angle + x0)
        if useeta:
            ty.append(cps/eta(rad(angle + x0).val)) # oversimplified error, eta doesn't work yet
        else:
            ty.append(cps)
    sx = []
    sy = []
    for key, (angle, cps) in target.items():
        sx.append(angle)
        if useeta:
            sy.append(cps/eta(rad(angle + x0).val)) # oversimplified error, eta doesn't work with Result yet
            print (eta(angle.val))
        else:
            sy.append(cps)
    tx, txerr = plotting_unpack(tx)
    ty, tyerr = plotting_unpack(ty)
    sx, sxerr = plotting_unpack(sx)
    sy, syerr = plotting_unpack(sy)
    testx = np.linspace(0, 180, 100)
    testy = klein_nishina(np.pi / 180 * testx)
    testty = thomson(np.pi / 180 * testx)
    print (sx)
    print (sy)
    plt.title("Normalized scattering detector data")
    plt.plot(testx, testy/np.sum(testy)/(np.pi/180*(testx[1]-testx[0])), label = "klein-nishina theta-dependence")
    plt.plot(testx, testty/np.sum(testty)/(np.pi/180*(testx[1]-testx[0])), label = "thomson theta-dependence")
    plt.plot(testx, eta(rad(testx)), label = "50x eta")
    plt.errorbar(sx, sy/np.sum(sy)/(np.pi/len(sy)), xerr = sxerr, yerr = syerr/np.sum(sy)/(np.pi/len(sy)), ls = 'none', label = "scatter cps" if not useeta else "eta-adjusted scatter cps")
    plt.legend()
    plt.show()
    #plt.plot(testx, testy * max(sy) / max(testy), label = "klein-nishina theta-dependence")
    #plt.plot(testx, 50 * eta(rad(testx)), label = "50x eta")
    #plt.errorbar(tx, ty, xerr = txerr, yerr = tyerr, ls = 'none', label = "target counts")
    #plt.legend()
    #plt.show()

    
    

plastic_lengths = [1, 1, 1, 15/16, 1]
def attenuation_data():
    cpss = []
    xs = []
    for i, file in enumerate(os.listdir(pfolder)):
        #print (file)
        info = read_data(pfolder + file)
        #print (info)
        cpss.append(info['cps'])
        xs.append(Result(np.sum(plastic_lengths[:i]), stat = 1/16/np.sqrt(12)))
    y_raw = [cps.log() for cps in cpss]
    x_raw = [x * 2.54 for x in xs]
    x, xerr = plotting_unpack(x_raw)
    print (x)
    y, yerr = plotting_unpack(y_raw)

    linear = lambda x, a, b : a*x + b
    quadratic = lambda x, a, b, c : a*x**2 + b*x + c
    model = lmfit.Model(linear)
    quadmodel = lmfit.Model(quadratic)
    result_raw = model.fit(y, x = x, a = -1, b = 0)
    slope_raw = result_raw.params['a'].value
    weights = 1 / np.sqrt((slope_raw * np.array(xerr))**2 + np.array(yerr)**2) # missing slope
    result = model.fit(y, x = x, a = slope_raw, b = result_raw.params['b'].value, weights = weights)
    quadresult = quadmodel.fit(y, x = x, b = slope_raw, c = result_raw.params['b'].value, a = 0.05, weights = weights)
    testx = np.linspace(0, max(x), 100)
    print (lmfit.fit_report(result))
    print (lmfit.fit_report(quadresult))
    print ("mu estimate: "+str(-1 * result.params['a'].value))
    print ("mu given: " + str(mu_plastic(E_0)))
    plt.plot(testx, result.params['a'].value*testx + result.params['b'].value, label = "Linear fit. χ² = %.3f" % result.redchi, color = 'r')
    plt.plot(testx, quadratic(testx, quadresult.params['a'].value, quadresult.params['b'].value, quadresult.params['c'].value), label = "Quadratic fit. χ² = %.3f" % quadresult.redchi, color = 'b')
    plt.errorbar(x, y, xerr = xerr, yerr = yerr, label = "Attenuation data", color = 'black', ls = 'none')
    plt.xlabel("Thickness of plastic (inches)")
    plt.ylabel("log(counts per second)")
    plt.title("Plastic attenuation data")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    cps_data(plot = True)
    #testx = np.linspace(1/10, 180 - 1/10, 10)
    #eta(rad(testx))
    #plot_cps(useeta = False)
    #plot_cps()
    #print (eta(Result(0)))
    #attenuation_data()
    #target, scatter = cps_data()
    pass