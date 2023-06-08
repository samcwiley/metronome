from pydub import AudioSegment
from pydub.generators import Sine
from pydub.utils import make_chunks
import numpy as np

strong_beat = 'strong_beat.wav'
weak_beat = 'weak_beat.wav'
break_beat = 'cymbal.wav'
off_beat = 'off_beat.wav'
strong = AudioSegment.from_file(strong_beat)
weak = AudioSegment.from_file(weak_beat)
break_beat = AudioSegment.from_file(break_beat)
off_beat = AudioSegment.from_file(off_beat)


class Medley:
    def __init__(self, title, tunes, rolls=False):
        self.title = title
        self.tunes = tunes
        self.rolls = rolls
        if self.rolls:
            rolls = Tune("Rolls", "Rolls", self.tunes[0].tempo, 1, False)
            self.tunes.insert(0, rolls)


    def add_break(self, first_tune_index, num_Beats, start_Beat):
        self.tunes[first_tune_index].parts[-1].bars[-1] = self.tunes[first_tune_index].parts[-1].bars[-1][0:-start_Beat]
        tempo = self.tunes[first_tune_index+1].tempo
        for i in range (num_Beats):
            self.tunes[first_tune_index].parts[-1].bars[-1].append([2, 60/tempo])
        

    def toString(self):
        print(f"{self.title} Medley. Rolls start at {self.rolls}. The tunes are: ")
        for tune in self.tunes:
            print(f"{tune.title}, a {tune.numParts}-parted {tune.tune_type} at {tune.tempo} BPM.")

    def make_mp3(self):
        result = AudioSegment.silent(duration=0)
        output_file = f"{self.title.replace(' ', '')}_medley_click_track.mp3"
        


        for tune in self.tunes:
            print(f"Adding {tune.title} at time {result.duration_seconds}")
            result = tune.add_tune(result)
        result.export(output_file, format="mp3")


class Tune:
    def __init__(self, title, tune_type, tempo, numParts, transition):
        self.title = title
        self.tune_type = tune_type
        self.tempo = tempo
        self.numParts = numParts
        self.transition = transition

        self.parts = []

        for part_number in range(self.numParts):
            self.parts.append(Part(self.title, self.tune_type, part_number + 1, self.tempo))
    
    def toString(self, listParts=False):
        print(f"{self.title}, a {self.numParts}-parted {self.tune_type} at {self.tempo} BPM.")
        if listParts:
            print("It contains parts:")
            for part in self.parts:
                print(f"{part.part_number}:")
                for bar in part.bars:
                    print(bar)
    
    def make_mp3(self):
        result = AudioSegment.silent(duration=0)
        output_file = 'clickTrack.mp3'
        result = self.add_tune(result)
        result.export(output_file, format="mp3")

    def add_tune(self, track):
        for part in self.parts:
            track = part.addPart(track)
        return track


class Part:
    def __init__(self, tune_name, tune_type, part_number, tempo):
        self.tune_name = tune_name
        self.tune_type = tune_type
        self.part_number = part_number
        self.tempo = tempo
        self.bars = []

        match tune_type:
            case "Rolls":
                beats_per_measure = 4
                bars_per_part = 2
                repeats = False
                beat_pattern = [2, 2, 2, 4]
            case "2/4 March":
                beats_per_measure = 2
                bars_per_part = 8
                #repeats = True
                repeats = False
                beat_pattern = [0, 1]
            case "4/4 March":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False
                beat_pattern = [0, 1, 1, 1]
            case "Strathspey":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False
                beat_pattern = [0, 1, 1, 1]
            case "Reel":
                beats_per_measure = 2
                bars_per_part = 8
                repeats = False
                beat_pattern = [0, 1]
            case "6/8 Jig":
                beats_per_measure = 2
                bars_per_part = 8
                repeats = True
                beat_pattern = [0, 1]
            case "12/8 Jig":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False
                beat_pattern = [0, 1, 1, 1]
            case "4/4 Slow March":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False
                beat_pattern = [0, 1, 1, 1]

        for bar in range(bars_per_part):
            beats = []
            #beats.append([0, 60/self.tempo])
            #for beat in range(1, beats_per_measure):
            #    beats.append([1, 60/self.tempo])
            for beat in beat_pattern:
                beats.append([beat, 60/self.tempo])
            self.bars.append(beats)
            if repeats:
                self.bars.append(beats)


    def toString(self):
        print(self.tune_name, self.part_number, self.bars)

    
    def addPart(self, track):
        for bar in self.bars:
            for beat in bar:
                if beat[0] == 0:
                    track += strong
                    sound_length = len(strong)
                if beat[0] == 1:
                    track += weak
                    sound_length = len(weak)
                if beat[0] == 2:
                    track += break_beat
                    sound_length = len(break_beat)
                if beat[0] == 3:
                    track += off_beat
                    sound_length = len(off_beat)
                if beat[0] == 4:
                    sound_length = 0
                silence_duration = beat[1] * 1000 - sound_length
                if silence_duration > 0:
                    silence = AudioSegment.silent(duration=silence_duration)
                    track += silence
        return track
    
    def accelerando(self, start_bar, end_bar, start_tempo, end_tempo):
        total_beats = 0
        for bar in self.bars[start_bar:end_bar]:
            total_beats = total_beats + len(bar)
        beat_durations = np.linspace(60/start_tempo, 60/end_tempo, num=total_beats).tolist()
        print(beat_durations)
        for bar in self.bars[start_bar:end_bar]:
            for beat in bar:
                beat[1] = beat_durations.pop(0)

    def add_off_beats(self, start_bar, end_bar, meter):
        for bar in self.bars[start_bar:end_bar]: 
            updated_bar = []
            for beat in bar:
                beat_type = beat[0]
                beat_duration = beat[1]
                updated_bar.append([beat_type, beat_duration / meter])
                for _ in range(1, meter):
                    updated_bar.append([3, beat_duration / meter])
            bar.clear()
            bar.extend(updated_bar)