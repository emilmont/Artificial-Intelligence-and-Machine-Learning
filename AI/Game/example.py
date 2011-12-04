from Game.game import Game

PRISONER_DILEMMA = {
    "players": (
        ("A", "testify", "refuse"),
        ("B", "testify", "refuse")
    ),
    "matrix": (
        ((-5, -5), (-10,0)),
        (( 0,-10), (-1,-1))
    )
}
g = Game(PRISONER_DILEMMA)
print "Dominant strategy for A: %s" % g.dominant_strategy("A")
print "Dominant strategy for B: %s" % g.dominant_strategy("B")
print "Equilibrium Points: %s" % str(g.equilibrium())


CONSOLE_GAME = {
    "players": (
        ("A", "blu", "dvd"),
        ("B", "blu", "dvd")
    ),
    "matrix": (
        (( 9, 9), (-4,-1)),
        ((-3,-1), ( 5, 5))
    )
}
g = Game(CONSOLE_GAME)
print "Dominant strategy for A: %s" % g.dominant_strategy("A")
print "Dominant strategy for B: %s" % g.dominant_strategy("B")
print "Equilibrium Points: %s" % str(g.equilibrium())