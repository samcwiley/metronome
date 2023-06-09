import tkinter as tk
from tkinter import Frame
import simpleaudio, time

strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
weak_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
p_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
#p_beat = simpleaudio.WaveObject.from_wave_file('p_beat.wav')

markings = {'Grave': [20,40], 'Largo' : [41,65], 'Adagio': [66,76], 
            'Andante': [77, 107], 'Moderato': [108, 120], 'Allegro': 
            [121, 168], 'Presto': [169, 200], 'Prestissimo': [200, 350]}

theme_colors = {'bg': '#52767D', 'text':'#FFFFE6', 'label_bg':'#3D998D', 'scale_through':'#A3CEC5'}
theme_fonts = ['Helvetica']
tempo_range = [30, 230]
defaults = {'tempo': 120, 'scale_length': 550}

# The main window
window = tk.Tk()
window.title('Metronome')
window.geometry('900x300')

# Three frames are created
leftFrame = Frame(window)
leftFrame.config(bg=theme_colors['bg'])
leftFrame.pack(side='left',fill='both')

midFrame = Frame(window)
midFrame.pack(side='left', fill='both')

rightFrame = Frame(window)
rightFrame.pack(side='left', fill='both', expand=1)

# In left frame
time_signatures = {1: [' 2 / 4', (2, 4)], 2: [' 3 / 4',(3 ,4)], 3: [' 4 / 4',(4, 4)], 4: [' 2 / 2',(2, 2)],
                   5: [' 6 / 8',(6, 8)], 6: [' 9 / 8',(9, 8)], 7: ['12/ 8',(12, 8)],
                   8: [' * / 4',(-1, 4)], 9: [' * / 2',(-1,2)], 10: [' * / 8',(-1,8)]}
ts_mode = tk.IntVar(leftFrame)
for mode in time_signatures.keys():
    radio_button = tk.Radiobutton(leftFrame, text = time_signatures[mode][0], variable = ts_mode,
                    value = mode, fg=theme_colors['text'],
                    bg=theme_colors['bg'], anchor='w', font=(theme_fonts[0], 17))
    if time_signatures[mode][-1] == (4, 4): # Select 4/4 by default
        radio_button.select()
    radio_button.pack(fill='x')

# In middle frame
# Label to show tempo 
tempo_label =tk.Label(midFrame, text='120', font=(theme_fonts[0], 90, 'bold'),
                      justify='center', fg = theme_colors['text'], bg = theme_colors['label_bg'], anchor='s')
tempo_label.pack(fill='both', expand=1)

marking_label =tk.Label(midFrame, text='Allegretto', font=(theme_fonts[0], 90, 'bold'),
                      justify='center', fg = theme_colors['text'], bg = theme_colors['label_bg'], anchor='n')
marking_label.pack(fill='both', expand=1)

# Use a scale to show the tempo range
scale_var = tk.IntVar(midFrame)

def update(*args):
    global scale_var, time_signature, interval_ms, tempo, tempo_label, marking_label
    tempo = scale_var.get()
    interval_ms = int((60/tempo) * (4/time_signature[-1]) * 1000)
    tempo_label['text'] = '{}'.format(tempo)
    marking = tempo_marking_of(tempo)
    marking_label['text'] = '{}'.format(marking)

scale = tk.Scale(midFrame,
             from_=tempo_range[0],
             to= tempo_range[1],
             orient=tk.HORIZONTAL,
             length=defaults['scale_length'],
             showvalue=0,
             troughcolor = theme_colors['scale_through'],
             bd = 0,
             activebackground = theme_colors['text'],
             bg = theme_colors['label_bg'],
             sliderlength = 30,
             font=(theme_fonts[0]),
             variable=scale_var,
             command=update)
scale.set(defaults['tempo'])
scale.pack(side='bottom',fill='both', expand='0')

# In right frame
# Label to show click number in a measure
count_label =tk.Label(rightFrame, text='0', fg=theme_colors['text'], bg =theme_colors['bg'], width=3, font=(theme_fonts[0], 180, 'bold'), justify='left')
count_label.pack(fill='both', expand=1)




def tempo_marking_of(tempo):
    for key in markings.keys():
        if tempo >= markings[key][0] and tempo <= markings[key][1]:
            marking = key
            break
        else :
            marking = ''
    return marking

def update_time_signature(*args):
    global temp, time_signature, count, interval_ms
    time_signature = time_signatures[ts_mode.get()][-1]
    interval_ms = int((60/tempo) * (4/time_signature[-1]) * 1000)
    count = 0
ts_mode.trace('w', update_time_signature)

# Time signature selection implementation
time_signature = time_signatures[ts_mode.get()][-1]
tempo = 120
interval_ms = int((60/tempo) * (4/time_signature[-1]) * 1000)
count = 0
def play():
    global count, time_signature, count_label
    count += 1
    count_label['text'] = '{}'.format(count)
    if time_signature[0] == -1:
        strong_beat.play()
    else:
        if count == 1:
            strong_beat.play()
        else:
            if time_signature[-1] == 8 and count % 3 == 1:
                p_beat.play()
            else:
                weak_beat.play()
    if count == time_signature[0]:
        count = 0
    window.after(interval_ms, play)

window.after(interval_ms, play)

window.mainloop()