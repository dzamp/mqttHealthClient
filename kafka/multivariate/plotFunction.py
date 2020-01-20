import matplotlib.pyplot as plt
import csv

x = []
y = []
z = []
with open('multivariate_temperature_change.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(long(row[0])-1575453247939)
        y.append(float(row[1]))
        z.append(float(row[2]))


# plt.plot(x,y, label='Loaded from file!', color = 'r')
# plt.xlabel('timestamp')
# plt.ylabel('temperature')
# plt.title('f(timestamp)')
# plt.legend()
# plt.show()

#
x1 = []
y1 = []
with open('multivariate_predictions.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x1.append(long(row[1])-1575453247939)
        y1.append(float(row[0]))

plt.plot(x,y,x1,y1)
plt.xlabel('timestamp')
plt.ylabel('temperature')
plt.title('f(timestamp)')
plt.legend()
plt.show()