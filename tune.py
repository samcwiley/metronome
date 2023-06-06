from pydub import AudioSegment
from pydub.generators import Sine
from pydub.utils import make_chunks
import time

class Medley:
    def __init__(self, title, tunes, rolls):
        self.title = title
        self.tunes = tunes
        self.rolls = rolls #(Zero if no rolls)

    def toString(self):
        print(f"{self.title} Medley. Rolls start at {self.rolls}. The tunes are: ")
        for tune in self.tunes:
            print(f"{tune.title}, a {tune.numParts}-parted {tune.tune_type} at {tune.tempo} BPM.")

    def make_mp3(self):
        result = AudioSegment.silent(duration=0)
        output_file = f"{self.title.replace(' ', '')}_medley_click_track.mp3"
        for tune in self.tunes:
            print(f"Adding {tune.title} at time {result.duration_seconds}")
            tune.add_tune(result)

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
    
    def toString(self):
        print(self.title, self.parts)
    
    def make_mp3(self):
        result = AudioSegment.silent(duration=0)
        output_file = 'clickTrack.mp3'
        self.add_tune(result)
        result.export(output_file, format="mp3")

    def add_tune(self, track):
        for part in self.parts:
            print(f"Adding {part.tune_name} part {part.part_number}.")
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
            case "2/4 March":
                beats_per_measure = 2
                bars_per_part = 8
                repeats = True
            case "4/4 March":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False
            case "Strathspey":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False
            case "Reel":
                beats_per_measure = 2
                bars_per_part = 8
                repeats = False
            case "6/8 Jig":
                beats_per_measure = 2
                bars_per_part = 8
                repeats = True
            case "12/8 Jig":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False
            case "4/4 Slow March":
                beats_per_measure = 4
                bars_per_part = 8
                repeats = False

        for bar in range(bars_per_part):
            beats = []
            beats.append((0, 60/self.tempo))
            for beat in range(1, beats_per_measure):
                beats.append((1, 60/self.tempo))
            self.bars.append(beats)

    def toString(self):
        print(self.tune_name, self.part_number, self.bars)

    
    def addPart(self, track):
        strong_beat = 'strong_beat.wav'
        weak_beat = 'weak_beat.wav'
        strong = AudioSegment.from_file(strong_beat)
        weak = AudioSegment.from_file(weak_beat)
        for bar in self.bars:
            for beat in bar:
                if beat[0] == 0:
                    track += strong
                if beat[0] == 1:
                    track += weak
                silence_duration = beat[1] * 1000 - len(strong) if beat[0] == 0 else beat[1] * 1000 - len(weak)
                if silence_duration > 0:
                    silence = AudioSegment.silent(duration=silence_duration)
                    track += silence
        return track