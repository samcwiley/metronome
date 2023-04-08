import time
import keyboard
import matplotlib.pyplot as plt

def get_tempo(window_size, filename=None):
    all_taps = []
    last_tap = time.time()
    window_tempos = []
    window_times = []
    start_time = None
    if filename:
        with open(filename, 'w') as f:
            f.write('time\n')
    while True:
        try:
            keyboard.wait('space')
            tap_time = time.time()
            if tap_time - last_tap > 2:  # if the user waits more than 2 seconds, reset the list of taps
                all_taps = []
                start_time = None
            else:
                all_taps.append(tap_time - last_tap)
                if start_time is None:
                    start_time = tap_time
                if len(all_taps) > 1:
                    tempo = 60 / (sum(all_taps) / len(all_taps))
                    print(f"All taps tempo: {int(tempo)} bpm")
                    
                    # Calculate the tempo for the last `window_size` taps
                    if len(all_taps) > window_size:
                        window_taps = all_taps[-window_size:]
                        window_tempo = 60 / (sum(window_taps) / len(window_taps))
                        window_tempos.append(window_tempo)
                        window_times.append(tap_time - start_time)
                        print(f"Last {window_size} taps tempo: {int(window_tempo)} bpm")
                        
                        if filename:
                            with open(filename, 'a') as f:
                                f.write(f"{tap_time - start_time:.2f}\n")
                        
            last_tap = tap_time
        except KeyboardInterrupt:
            print("Exiting...")
            break
            
    # Plot the average tempo over time
    plt.plot(window_times, window_tempos, label='tempo, 6 beat window')
    plt.axhline(y=tempo, color='r', linestyle='-', label = 'overall average')
    plt.title('LAK Tempo over time, FMM 2019 World\'s Finals MSR')
    plt.xlabel('Time (s)')
    plt.ylabel('Tempo (BPM)')
    plt.legend(loc='upper right')
    plt.show()

get_tempo(window_size=8, filename='FMM_2019_3.csv')