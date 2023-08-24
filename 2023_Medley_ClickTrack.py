from tune import Tune, Part, Medley

# constructing tunes using: Tune(title, tune_type, tempo, numParts, transition)
opener = Tune("John MacDonald of Glencoe", "4/4 March", 96, 2, False)
jig1 = Tune("Minnie Hynd", "6/8 Jig", 106, 2, False)
jig2 = Tune("Irish Jig", "6/8 Jig", 106, 2, False)
air = Tune("Cha Til MacCrimmon", "6/4 Slow March", 92, 2, False)
strath1 = Tune("Stumpie", "Strathspey", 106, 2, False)
strath2 = Tune("She put a knee in the old man", "Strathspey", 106, 2, False)
reel1 = Tune("Wretched Man", "Reel", 74, 2, False)
reel2 = Tune("Ceapaval", "Reel", 74, 2, False)
reel3 = Tune("Kelsey's Wee Reel", "Reel", 74, 2, False)
# turn them bitches into a medley
tune_list = [opener, jig1, jig2, air, strath1, strath2, reel1, reel2, reel3]
medley = Medley("2023_APB", tune_list, True)

# adding breaks between opener and strath, and strath and jigs using: medley.add_break(start_tune_index, num_beats, starting beat)
medley.add_break(1, 2, 1)
medley.add_break(3, 2, 1)
medley.add_break(5, 3, 1)
medley.make_mp3()
