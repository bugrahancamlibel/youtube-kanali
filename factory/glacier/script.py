TITLE = "What If the Doomsday Glacier Collapsed?"
SCRIPT = [
    # 0 cold open
    ["At the bottom of the world, there's a glacier the size of Florida. In places, it's more than two kilometers thick, and it's slowly sliding into the sea.",
     "Scientists call it Thwaites. Everyone else calls it the Doomsday Glacier.",
     "And this year, researchers warned that the ice shelf holding it back is poised to break apart.",
     "So what would happen if the Doomsday Glacier collapsed?"],
    # 1 why doomsday
    ["Thwaites alone holds enough ice to raise global sea levels by about sixty-five centimeters.",
     "But the real danger is what's behind it. Thwaites works like a cork for the West Antarctic Ice Sheet. Pull the cork, and seas could eventually rise by more than three meters."],
    # 2 melting from below
    ["The threat isn't warm air. It's warm water.",
     "Relatively warm water from the deep ocean flows beneath the glacier and melts it from below. With the tides, seawater can push up to ten kilometers under the ice.",
     "And the ground beneath Thwaites gets deeper the farther inland you go. So as the glacier retreats, more and more ice meets the water.",
     "Since the 1980s, Thwaites has already lost more than six hundred billion tons of ice."],
    # 3 the brake
    ["For now, something slows it down: a floating ice shelf, pinned on an underwater ridge like a brake.",
     "But the brake is failing. Giant cracks are spreading across it by up to two kilometers a year, and it's losing its grip on the ridge.",
     "In 2026, a British Antarctic Survey scientist said the shelf is very likely to break up this year.",
     "Losing it won't make Thwaites collapse overnight. But without the brake, the ice behind it can flow faster."],
    # 4 the what-if
    ["So let's imagine Thwaites collapses.",
     "It wouldn't happen in a day. Scientists expect a full collapse to take centuries, though no one knows exactly how fast.",
     "But even sixty-five centimeters would redraw the world's coastlines. Around 680 million people live in low-lying coastal areas.",
     "And seas are already rising. The IPCC expects that by 2050, at many coasts, floods that used to come once a century will strike every year."],
    # 5 living below the sea
    ["Some places already live with this. About a quarter of the Netherlands lies below sea level, protected by dikes, dunes and giant storm barriers.",
     "With three meters, much of the world would have to do the same. Or move."],
    # 6 the curtain
    ["To save the Doomsday Glacier, some scientists want to build a giant curtain under the sea.",
     "An eighty-kilometer barrier on the seafloor, six hundred meters down, to block the warm water before it reaches the ice.",
     "The price? Forty to eighty billion dollars, plus up to two billion every year to keep it running.",
     "Critics say it's too risky, too remote, and a distraction from cutting emissions. A first test could come in Norway in 2027."],
    # 7 the warning
    ["Meanwhile, scientists are watching Thwaites more closely than ever. In 2020, a robot called Icefin even swam beneath the ice to see how it melts.",
     "So will the Doomsday Glacier doom us? Not tomorrow. But the ice is moving, and every centimeter counts.",
     "We can't refreeze Antarctica. But we can still slow the warming, and get our coasts ready.",
     "Because this glacier isn't a countdown. It's a warning."],
]
WPS = 2.8
LINE_GAP = 0.45
HEAD = 0.6
TAIL = [2.6, 0.8, 0.8, 0.8, 0.9, 0.9, 0.8, 3.4]


def timeline():
    S = [0.0]; lines = []
    for si, sc in enumerate(SCRIPT):
        t = HEAD; ls = []
        for txt in sc:
            d = len(txt.split()) / WPS
            ls.append((t, t + d)); t += d + LINE_GAP
        lines.append(ls)
        S.append(S[-1] + t - LINE_GAP + TAIL[si])
    return S, lines


if __name__ == '__main__':
    S, L = timeline()
    print('words', sum(len(x.split()) for sc in SCRIPT for x in sc), 'chars', len('\n\n'.join(x for sc in SCRIPT for x in sc)),
          'total', round(S[-1], 1))
    for i in range(8): print(i, round(S[i], 1), [(round(a, 1), round(b, 1)) for a, b in L[i]])
