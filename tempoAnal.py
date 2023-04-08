import numpy as np
import matplotlib.pyplot as plt

filename = 'FMM_2019_1.csv'

# Load the data from the file
data = np.genfromtxt(filename, delimiter=',', skip_header=1)

# Extract the time column and calculate the corresponding tempo values
times = data[:]
tempos = 60 / np.diff(times)

# Plot the tempo over time
plt.plot(times[:-1], tempos)
plt.title('Tempo over time')
plt.xlabel('Time (s)')
plt.ylabel('Tempo (BPM)')
plt.show()