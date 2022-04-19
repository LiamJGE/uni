import csv
import numpy as np
import matplotlib.pyplot as plt
from statistics import *

with open("pima-indians-diabetes.csv", "r", newline="") as file:
    plist = list(csv.reader(file))

## Print in tabular way
for instance in plist:
    for attr in instance:
        print("{:<10}".format(attr), end="")
    print()

## Print number of instances
print("Number of instances " + str(len(plist)))

## Times pregnant min, max, avg
plist = np.array(plist)
preg = plist[:,0].astype(int)
print("Times pregnant minimum " + str(min(preg)))
print("Times pregnant maximum " + str(max(preg)))
print("Times pregnant mean " + str(mean(preg)))

# print()

## Class breakdown
add = 0
for el in plist:
        add += int(el[8])    
print("Class breakdown\nYes: " + str(add) +"\nNo: " + str(len(plist[:,8]) - add))

## Age plot
data = plist[:,7].astype('float')
plt.hist(data, align='left', edgecolor='black', linewidth=1.2)
oneStd = np.std(data)
meanV = mean(data)
print("Mean: " + str(meanV))
print("One StdV: " + str(oneStd))
plt.title("Age")
plt.axvline(x=(meanV - 2*oneStd), label='Two STD', c="r")
plt.axvline(x=(meanV + 2*oneStd), c="r")
plt.axvline(x=(meanV - 3*oneStd), label='Three STD', c="g")
plt.axvline(x=(meanV + 3*oneStd), c="g")
plt.legend()
plt.show()

## Skinfold thickness plot
data = plist[:,3].astype('float')
plt.hist(data, align='left', edgecolor='black', linewidth=1.2)
oneStd = np.std(data)
meanV = mean(data)
print("Mean: " + str(meanV))
print("One StdV: " + str(oneStd))
plt.title("Skinfold thickness")
plt.axvline(x=(meanV - 2*oneStd), label='Two STD', c="r")
plt.axvline(x=(meanV + 2*oneStd), c="r")
plt.axvline(x=(meanV - 3*oneStd), label='Three STD', c="g")
plt.axvline(x=(meanV + 3*oneStd), c="g")
plt.legend()
plt.show()

## BMI plot
data = plist[:,5].astype('float')
plt.hist(data, align='left', edgecolor='black', linewidth=1.2)
oneStd = np.std(data)
meanV = mean(data)
print("Mean: " + str(meanV))
print("One StdV: " + str(oneStd))
plt.title("Body Mass Index")
plt.axvline(x=(meanV - 2*oneStd), label='Two STD', c="r")
plt.axvline(x=(meanV + 2*oneStd), c="r")
plt.axvline(x=(meanV - 3*oneStd), label='Three STD', c="g")
plt.axvline(x=(meanV + 3*oneStd), c="g")
plt.legend()
plt.show()

## Number of times pregnant plot
plt.hist(preg, align='left', edgecolor='black', linewidth=1.2)
oneStd = np.std(preg)
meanV = mean(preg)
print("Mean: " + str(meanV))
print("One StdV: " + str(oneStd))
plt.title("Number of times pregnant")
plt.axvline(x=(meanV - 2*oneStd), label='Two STD', c="r")
plt.axvline(x=(meanV + 2*oneStd), c="r")
plt.axvline(x=(meanV - 3*oneStd), label='Three STD', c="g")
plt.axvline(x=(meanV + 3*oneStd), c="g")
plt.legend()
plt.show()

