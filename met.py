import simpleaudio, time
strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
weak_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
p_beat = simpleaudio.WaveObject.from_wave_file('p_beat.wav')

markings = {'Grave': [20,40], 'Largo' : [41,65], 'Adagio': [66,76], 
            'Andante': [77, 107], 'Moderato': [108, 120], 'Allegro': 
            [121, 168], 'Presto': [169, 200], 'Prestissimo': [200, 350]}
time_list = [1648565267.9251342, 1648565268.482229, 1648565269.013833, 1648565269.560467, 1648565270.105812, 1648565270.644593, 1648565271.175668]


def tempo_marking_of(tempo):
    for key in markings.keys():
        if tempo >= markings[key][0] and tempo <= markings[key][1]:
            marking = key
            break
        else:
            marking = ''
    return marking
for tempo in range(30, 230, 40):
    print("The marking of {} BPM is {}.".format(tempo, tempo_marking_of(tempo)))


def tempo_estimate(times):
    N=6
    length = len(times)
    if length < N:
        interval = (times[-1] - times[0])/ (length - 1)
    else: 
        interval = (times[-1] - times[-N]) / (N - 1)
    temp = int(60/interval)
    return temp
print('The estimated tempo is {} BPM.'.format(tempo_estimate(time_list)))

temp = 120
timeSig = 8
medBeat = [5]

count = 1
while True:
    if count == 1:
        p_beat.play()
    elif count in medBeat:
        strong_beat.play()
    else:
        weak_beat.play()
    count += 1
    if count == timeSig:
        count = 0
    time.sleep(60/temp)
