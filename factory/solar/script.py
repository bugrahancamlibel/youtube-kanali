TITLE = "What If a Solar Superstorm Hit Earth Today?"
SCRIPT = [
    # 0 cold open: 1859
    ["On a September morning in 1859, an astronomer named Richard Carrington was sketching sunspots...",
     "when two blinding white lights flared up on the Sun.",
     "Less than a day later, the sky caught fire. Auroras lit up Cuba, Hawaii, even Colombia.",
     "Telegraph wires threw sparks. Some operators got electric shocks. Others unplugged their batteries, and kept sending messages anyway.",
     "Back then, it was a curiosity. Today, it could be a catastrophe.",
     "So what would happen if a storm like that hit us now?"],
    # 1 how the sun attacks
    ["Our Sun is not a calm ball of light. It's a churning knot of plasma and magnetic fields.",
     "Sometimes those fields snap, and the Sun hurls out a coronal mass ejection: billions of tons of charged gas, racing through space.",
     "Most of them miss us. But the Carrington storm crossed the 150 million kilometers to Earth in about seventeen hours.",
     "When a storm like that hits, Earth's magnetic field shakes. And that shaking pushes electric currents through anything long and made of metal."],
    # 2 warning shots
    ["We have already had a few warning shots.",
     "In 1989, a storm knocked out Quebec's power grid in less than ninety seconds. Millions of people sat in the dark for nine hours.",
     "In 2022, a fairly modest storm puffed up the upper atmosphere, and dragged about forty brand-new Starlink satellites out of orbit.",
     "And in May 2024, the strongest storm in twenty years sent GPS-guided tractors in the American Midwest wandering off course.",
     "None of these came close to Carrington."],
    # 3 the timeline
    ["So let's imagine it. Day zero. A giant flare erupts.",
     "Eight minutes later, its light hits us. Radio goes quiet across the daylight side of the planet.",
     "Next comes a storm of particles. Satellites glitch. GPS gets confused. Flights reroute away from the poles.",
     "Then the main blow arrives. Currents surge into the power grid, and huge transformers, the hearts of the network, start to overheat.",
     "If enough of them fail, entire regions go dark. And these machines are custom-built. Ordering a new one today can take more than two years."],
    # 4 life without power
    ["Without electricity, water pumps stop. Fuel pumps stop.",
     "Card payments, phone towers, refrigerated medicine. Almost everything we depend on runs on the grid.",
     "Lloyd's of London estimated that a Carrington-level storm could leave twenty to forty million Americans without power, for weeks, or even up to two years.",
     "The cost for the US alone: as much as two point six trillion dollars."],
    # 5 the near miss
    ["And here's the unsettling part. It almost happened.",
     "In July 2012, the Sun launched a storm at least as strong as Carrington's.",
     "It tore through Earth's orbit, about a week after our planet had passed by. A NASA spacecraft in its path recorded everything.",
     "One scientist estimated a twelve percent chance of a Carrington-class storm hitting Earth within a decade."],
    # 6 defence
    ["The good news? We are not blind anymore.",
     "Spacecraft parked between us and the Sun watch the solar wind, and can give us about fifteen to sixty minutes of warning.",
     "Grid operators can reduce the load. Quebec redesigned its network after 1989. Satellites can switch to safe mode, and planes can change course.",
     "It won't make us immune. But it can turn a catastrophe into a very bad week."],
    # 7 outro
    ["Just this October, a strong storm painted auroras across the northern sky. The Sun has only just passed the peak of its eleven-year cycle.",
     "So the next time you see the northern lights much farther south than usual, enjoy the show.",
     "It's beautiful. It's also a reminder from our star of who is really in charge."],
]
WPS = 2.8
LINE_GAP = 0.45
HEAD = 0.6
TAIL = [2.6, 0.8, 0.8, 0.9, 0.9, 0.9, 0.8, 3.4]


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
    for i in range(8): print(i, round(S[i], 1), round(S[i + 1] - S[i], 1))
