import numpy as np
import matplotlib.pyplot as plt 
import math
f = open('data', 'r')

x = []
y = []
for line in f:
    x.append(math.log(float(line.split(' ')[0].strip('\n'))))
    y.append(math.log(float(line.split(' ')[1].strip('\n'))))
plt.plot(x, y, 'k-')
plt.show()
