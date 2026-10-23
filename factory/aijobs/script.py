TITLE = "What If AI Took All the Jobs?"
SCRIPT = [
    # 0 cold open
    ["It's a Monday morning in the near future. Your alarm doesn't ring. You don't need it anymore.",
     "Trucks drive themselves. AI writes the code, reads the X-rays, answers the phones, and argues the court cases.",
     "Every job, from cashier to CEO, is done by machines that never sleep and never ask for a raise.",
     "Is that paradise? Or the beginning of a disaster?"],
    # 1 it's already starting
    ["This isn't pure fantasy. Just this week, Barclays said it would cut five thousand jobs, partly because of AI.",
     "And a Stanford study found that young workers in the jobs most exposed to AI, like customer service and coding, saw employment fall by thirteen percent compared to other jobs."],
    # 2 we've been here before
    ["But we have been here before. In 1900, almost four in ten American workers were farmers. Today, it's fewer than two in a hundred.",
     "In 1811, the Luddites smashed weaving machines, sure they would destroy their livelihoods.",
     "When ATMs arrived, everyone expected bank tellers to vanish. Instead, banks opened more branches, and the number of tellers held steady for decades.",
     "New jobs appeared that nobody could imagine. Most of today's jobs didn't even exist in 1940."],
    # 3 this time is different
    ["So why worry? Because old machines replaced our muscles. AI is coming for our brains.",
     "The IMF estimates that almost forty percent of jobs worldwide are exposed to AI. In rich countries, it's about sixty percent.",
     "Lawyers, accountants, programmers, writers. The jobs we once thought were safe are now the most exposed.",
     "About half of those jobs could benefit. The other half could shrink, or vanish."],
    # 4 the extreme
    ["So let's push it to the extreme. AI does everything.",
     "Companies could produce more than ever, for almost nothing. But there's a catch: wages are how most of us get money.",
     "If nobody earns a salary, who buys all those products? The wealth would flow to whoever owns the machines.",
     "That's why some people want to tax the robots themselves. Bill Gates suggested exactly that back in 2017."],
    # 5 basic income
    ["One idea is universal basic income: a regular payment to everyone, no strings attached.",
     "In one large study, a thousand people got a thousand dollars a month for three years. They worked only about an hour less per week, and spent most of it on food, rent and transport.",
     "Alaska has paid a yearly dividend to almost every resident since 1982, funded by oil. In an AI world, the oil could be computing power."],
    # 6 meaning
    ["But a job gives us more than money. It gives us structure, friends, and a sense of purpose.",
     "In 1930, the economist John Maynard Keynes predicted his grandchildren would work just fifteen hours a week. We got far richer. We kept working anyway."],
    # 7 what stays human
    ["And some things we may simply want from humans. In 1997, a computer beat the world chess champion.",
     "Today, chess is more popular than ever. One website alone has around 250 million users, playing and watching people.",
     "Nurses, teachers, artists, athletes. Some work we value precisely because a human does it.",
     "So the real question isn't whether AI can do our jobs. It's who AI will work for.",
     "And whether we use all that free time to finally live."],
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
    for i in range(8): print(i, round(S[i], 1), round(S[i + 1] - S[i], 1))
