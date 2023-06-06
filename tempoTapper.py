import simpleaudio
import time
from pynput import keyboard
from tempoAnal import analyze

def get_times(audioFileName, outputFileName=None):
    timeStamps = []
    audio = simpleaudio.WaveObject.from_wave_file(audioFileName)
    start_time = time.time()
    play_obj = audio.play()
    
    def on_press(key):
        if key == keyboard.Key.space:
            tap_time = time.time()
            timeStamps.append(tap_time)
            print("new keypress")

    with keyboard.Listener(on_press=on_press) as listener:
        while play_obj.is_playing():
            listener.join(0.1)  # Check for key presses every 0.1 seconds
        listener.stop()  # Stop the listener when the audio finishes
    
    print('finished', len(timeStamps))
    
    if outputFileName:
        with open(outputFileName, 'w') as f:
            f.write('time\n')
            for stamp in timeStamps:
                f.write(f"{stamp - start_time:.4f}\n")

if __name__ == "__main__":
    get_times('FMM_2019_March_part1.wav', outputFileName='FMM_2019_Sam_1.csv')
    analyze('FMM_2019_Sam_1.csv')
