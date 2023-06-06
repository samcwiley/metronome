import pygame
import time
from tempoAnal import analyze

def get_times(audioFileName, outputFileName=None):
    timeStamps = []
    # Initialize Pygame and create a display
    pygame.init()
    pygame.display.set_mode((1, 1))

    # Initialize Pygame mixer and load audio file
    pygame.mixer.init()
    pygame.mixer.music.load(audioFileName)

    # Start audio playback
    start_time = time.time()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # Check for key press events
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # Record button press timestamp
                    timeStamps.append((time.time() - start_time))
        time.sleep(0.005)

    if outputFileName:
        with open(outputFileName, 'a') as f:
            f.write('time \n')
            for stamp in timeStamps:
                f.write(f"{stamp:.3f}\n")

# Create empty list for storing button press timestamps

# Call the play_audio function with the name of your audio file

if __name__ == "__main__":
    get_times('FMM_2019_March_part1.wav', outputFileName='FMM_2019_Sam_1.csv')
    #analyze('FMM_2019_Sam_1.csv')
