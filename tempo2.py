import time
import matplotlib.pyplot as plt

def calculate_tempo(taps, window_size):
    if len(taps) < 2:
        return None
    
    time_diffs = [taps[i] - taps[i-1] for i in range(1, len(taps))]
    tempo_candidates = [60 / diff for diff in time_diffs]
    
    if len(tempo_candidates) <= window_size:
        return sum(tempo_candidates) / len(tempo_candidates)
    
    return sum(tempo_candidates[-window_size:]) / window_size

def main():
    taps = []
    window_size = 6
    all_tempos = []
    start_time = time.time() 
    
    while True:
        input("Press enter to tap. Press ctrl+c to exit.")
        tap_time = time.time()
        taps.append(tap_time - start_time)
        tempo = calculate_tempo(taps, window_size)
        if tempo:
            all_tempos.append(tempo)
        plt.plot(all_tempos)
        plt.axhline(y=sum(all_tempos) / len(all_tempos), color="r", linestyle="--")
        plt.ylim(min(all_tempos)-5, max(all_tempos)+5)
        plt.xlabel("Number of Taps")
        plt.ylabel("Tempo (BPM)")
        plt.title("Tap Tempo")
        plt.show(block=False)
        plt.pause(0.001)

if __name__ == '__main__':
    main()
