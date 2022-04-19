import csv
import numpy as np
import matplotlib.pyplot as plt
from statistics import *

with open("weatherRaw.csv", "r", newline="") as file:
    wlist = list(csv.reader(file))

## Print in tabular way
for instance in wlist:
    for attr in instance:
        print("{:<15}".format(attr), end="")
    print()

## Print number of instances
print("Number of instances " + str(len(wlist)))

## Temperature min, max, avg
wlist = np.array(wlist)
temp = wlist[:,1].astype('float')
print("Temperature minimum " + str(min(temp)))
print("Temperature maximum " + str(max(temp)))
print("Temperature mean " + str(mean(temp)))

print()
## Humidity min, max, avg
hum = wlist[:,2].astype('float')
print("Humidity minimum " + str(min(hum)))
print("Humidity maximum " + str(max(hum)))
print("Humidity mean " + str(mean(hum)))

## Class breakdown
add = 0
for el in wlist:
    if el[4] == "yes":
        add += 1    
print("Class breakdown\nYes: " + str(add) +"\nNo: " + str(len(wlist[:,1]) - add))

## Temperature plot
plt.hist(temp)
oneStd = np.std(temp)
meanV = mean(temp)
print("Mean: " + str(meanV))
print("One StdV: " + str(oneStd))
plt.title("Checking for outliers")
plt.axvline(x=(meanV - 2*oneStd), label='Two STD', c="r")
plt.axvline(x=(meanV + 2*oneStd), c="r")
plt.axvline(x=(meanV - 3*oneStd), label='Three STD', c="g")
plt.axvline(x=(meanV + 3*oneStd), c="g")
plt.legend()
plt.show()

## Humidity plot
plt.hist(hum)
oneStd = np.std(hum)
meanV = mean(hum)
plt.title("Checking for outliers")
plt.axvline(x=(meanV - 2*oneStd), label='Two STD', c="r")
plt.axvline(x=(meanV + 2*oneStd), c="r")
plt.axvline(x=(meanV - 3*oneStd), label='Three STD', c="g")
plt.axvline(x=(meanV + 3*oneStd), c="g")
plt.legend()
plt.show()

