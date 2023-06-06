import numpy as np
import matplotlib.pyplot as plt

def getTimes(filename):
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    times = data[:]
    times = times - times[0]
    return times

def getTempo(windowSize, times):
    tempos = []
    parts = []
    for i in range (0, len(times) - windowSize):
        windowAverage = windowSize / (times[i+windowSize] - times[i])
        tempos.append(60*windowAverage)
    windowTimes = times[0:-(windowSize-1)]
    for i in range (4, len(times), 16): #starts at index 4 (beat 5) to disregard rolls for now
        try:
            partAverage = 16 / (times[i+16]-times[i])
            partTempo = 60*partAverage
            for j in range (0,16):
                parts.append(partTempo)
        except IndexError:
            print(len(times), (len(times)-4)%16)
            lastPartLength = (len(times)-4)%16
            print(i, i+lastPartLength-1)
            partAverage = lastPartLength / (times[i+lastPartLength-1]-times[i])
            partTempo = 60*partAverage
            for j in range (0,lastPartLength-1):
                parts.append(partTempo)
    return(windowTimes, tempos, parts)

def timesAverage(times):
    avgTimes = []
    for i in range(len(times[0])):
        count = 0
        for time in times:
            count += time[i]
        avgTimes.append(count/len(times))
    return avgTimes

def analyze(csv_filename):
    times = getTimes(csv_filename)
    windowTimes, tempos, parts = getTempo(8, times)
    plt.plot(windowTimes[:-1], tempos, label = 'Tempo over time')
    plt.plot(times, parts, label = 'Tempo per part')
    plt.title('Tempo over time')
    plt.legend(loc = 'best')
    plt.xlabel('Time (s)')
    plt.ylabel('Tempo (BPM)')
    plt.show()

if __name__ == "__main__":
    times1 = getTimes('FMM_2019_Sam_1.csv')
    windowTimes1, tempos1, parts1 = getTempo(8, times1)
    plt.plot(windowTimes1, tempos1, label = 'Run')


'''if __name__ == "__main__":
    times1 = getTimes('FMM_2019_1.csv')
    times2 = getTimes('FMM_2019_2.csv')
    times3 = getTimes('FMM_2019_3.csv')
    windowTimes1, tempos1, parts1 = getTempo(8, times1)
    windowTimes2, tempos2, parts2 = getTempo(8, times2)
    windowTimes3, tempos3, parts3 = getTempo(8, times3)

    avgTimes = timesAverage([times1, times2, times3])
    avgWindowTimes, avgTempos, avgParts = getTempo(8, avgTimes)

    #plt.plot(windowTimes1[:-1], tempos1, label = 'Run 1')
    #plt.plot(windowTimes2[:-1], tempos2, label = 'Run 2')
    #plt.plot(windowTimes3[:-1], tempos3, label = 'Run 3')
    plt.plot(avgWindowTimes[:-1], avgTempos, label = '3-Run average')
    plt.plot(avgTimes, avgParts, label = '3-Run average parts')
    plt.title('Tempo over time')
    plt.legend(loc = 'best')
    plt.xlabel('Time (s)')
    plt.ylabel('Tempo (BPM)')
    plt.show()
    '''