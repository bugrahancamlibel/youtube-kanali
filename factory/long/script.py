SCRIPT = [
    # 0 cold open
    ["Look at these two people.",
     "One of them is real. The other was invented by a computer in a fraction of a second.",
     "Trick question. Neither of them exists.",
     "And soon, that won't just be true for faces. It will be true for voices, phone calls, and live video.",
     "So in a world where anything can be faked... how do we know what's real?"],
    # 1 the duel
    ["It started in 2014, with an idea called a generative adversarial network.",
     "Picture two AIs locked in a duel. One is a forger. The other is a detective.",
     "The forger paints fake faces. The detective tries to catch them.",
     "Every time the forger gets caught, it learns. Millions of rounds later, the detective can no longer tell the difference.",
     "In 2017, a Reddit user gave face-swapped videos made with this kind of AI a name: deepfakes."],
    # 2 how good it got
    ["Since then, the technology has exploded.",
     "In a 2025 study, two thousand people were shown a mix of real and fake images and videos.",
     "Only two of them spotted every single fake.",
     "In another study, people judged AI-generated faces to be human more often than actual human faces.",
     "And voices? Some AI models need just three seconds of audio to clone yours."],
    # 3 the heist
    ["In early 2024, a finance worker in Hong Kong got a message from his company's CFO, asking for a secret transaction.",
     "He was suspicious. So they jumped on a video call.",
     "His CFO was there. So were several colleagues. They looked right. They sounded right.",
     "So he made fifteen transfers. About twenty-five million dollars in total.",
     "Every other person on that call was a deepfake.",
     "And this may be just the beginning. Deloitte estimates that AI-powered fraud could cost the US forty billion dollars a year by 2027."],
    # 4 politics
    ["Now imagine this at the scale of a whole country.",
     "In January 2024, thousands of voters in New Hampshire got a robocall in the voice of President Biden, telling them to skip the primary.",
     "It was fake. The consultant behind it was fined six million dollars.",
     "In Slovakia, two days before a national election, a fake audio clip of a leading candidate spread across social media.",
     "No one knows for sure if it changed the result. But it showed how easily it could."],
    # 5 liar's dividend
    ["But maybe the strangest danger isn't the fakes themselves.",
     "It's what they do to the truth.",
     "When anything could be fake, real evidence can be dismissed too. Caught on camera? Just say it was AI.",
     "Researchers call this the liar's dividend."],
    # 6 fighting back
    ["So, are we doomed? Not quite.",
     "AI companies are hiding invisible watermarks inside the content they generate.",
     "And a growing number of cameras and apps attach content credentials: a kind of digital receipt showing where a photo came from and how it was edited.",
     "Laws are catching up too. Since August 2026, the EU requires deepfakes to be clearly labeled. In the US, platforms must now remove non-consensual intimate deepfakes within 48 hours.",
     "But detection is an arms race. Every new detector teaches the next forger what to avoid."],
    # 7 outro
    ["So the best defense might be older than any algorithm: healthy skepticism.",
     "If a message is urgent, emotional, and asks for money or secrecy, stop.",
     "Call back on a number you already know. Agree on a safe word with your family. And check where something came from, not just how real it looks.",
     "For millions of years, our eyes were the most reliable source of truth we had.",
     "Now, trust has to come from somewhere else.",
     "So don't just trust. Verify."],
]
WPS = 2.8          # design narration pace (words / second)
LINE_GAP = 0.45
HEAD = 0.6         # silence at scene start
TAIL = [2.4, 0.8, 0.8, 0.9, 0.9, 1.0, 0.8, 3.2]


def timeline():
    """Returns scene starts S (len 9) and per-scene list of (start, end) relative times."""
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
    words = sum(len(x.split()) for sc in SCRIPT for x in sc)
    print('words', words, 'total', round(S[-1], 1))
    for i in range(8): print(i, round(S[i], 1), round(S[i + 1] - S[i], 1))
