from tune import Tune, Part, Medley


#Tune(title, tune_type, tempo, numParts, transition)
opener = Tune("Thin Red Line", "2/4 March", 72, 4, False)
strath1 = Tune("Munlochy Bridge", "Strathspey", 110, 2, False)
strath2 = Tune("Highland Whisky", "Strathspey", 110, 2, False)
jig1 = Tune("Mrs. MacPherson", "12/8 Jig", 105, 2, False)
jig2 = Tune("Jig 2", "6/8 Jig", 105, 2, False)
air = Tune("Simple Gifts", "4/4 Slow March", 70, 2, False)
reel1 = Tune("Simple Gifts Reel", "Reel", 80, 2, False)
reel2 = Tune("Angus MacLellan", "Reel", 80, 2, False)
reel3 = Tune("Hurlock's Reel", "Reel", 80, 2, False)
closer = Tune("Simple Gifts Reprise", "Reel", 80, 1, False)

tune_list = [opener, strath1, strath2, jig1, jig2, air, reel1, reel2, reel3, closer]
medley = Medley("1-Simple Gifts", tune_list, 72)
#medley.toString()
#   medley.make_mp3()
opener.make_mp3()
opener.toString()