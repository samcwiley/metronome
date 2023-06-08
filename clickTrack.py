from tune import Tune, Part, Medley

#constructing tunes using: Tune(title, tune_type, tempo, numParts, transition)
opener = Tune("Thin Red Line", "2/4 March", 72, 4, False)
strath1 = Tune("Munlochy Bridge", "Strathspey", 110, 2, False)
strath2 = Tune("Highland Whisky", "Strathspey", 110, 2, False)
jig1 = Tune("Mrs. MacPherson", "12/8 Jig", 105, 2, False)
jig2 = Tune("Rocking the Baby", "6/8 Jig", 105, 2, False)
air = Tune("Simple Gifts", "4/4 Slow March", 70, 2, False)
reel1 = Tune("Simple Gifts Reel", "Reel", 80, 2, False)
reel2 = Tune("Angus MacLellan", "Reel", 80, 2, False)
reel3 = Tune("Hurlock's Reel", "Reel", 80, 2, False)
closer = Tune("Simple Gifts Reprise", "Reel", 80, 1, False)
#turn them bitches into a medley
tune_list = [opener, strath1, strath2, jig1, jig2, air, reel1, reel2, reel3, closer]
medley = Medley("2024_APB", tune_list, True)
#adding two beats to bars 2, 4, 6, 8 to make part 1 of the air mixed meter
for bar_number in [1, 3, 5, 7]:
    for _ in range(2):
        air.parts[0].bars[bar_number].append([1, 60/air.tempo])
air.parts[0].bars[0].insert(0, [1, 60/air.tempo])
reel1.parts[0].add_off_beats(0, 2, 2)
reel1.parts[0].accelerando(0, 2, air.tempo, 2*reel1.tempo)
reel1.parts[0].bars[5].append([1, 60/reel1.tempo])
#adding breaks between opener and strath, and strath and jigs using: medley.add_break(start_tune_index, num_beats, starting beat)
medley.add_break(1, 2, 1)
medley.add_break(3, 2, 1)
medley.add_break(5, 3, 1)
medley.make_mp3()

