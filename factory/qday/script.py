TITLE = "What If Quantum Computers Broke All Encryption?"
SCRIPT = [
    # 0 cold open
    ["It's an ordinary morning. You tap your card, send a message, and log into your bank.",
     "Every one of those actions is protected by math so hard that today's best supercomputers would need millions of years to crack it.",
     "Now imagine that one morning, a single machine can break it in days.",
     "No alarms. No explosions. Just secrets, suddenly readable. Experts even have a name for that day: Q-Day."],
    # 1 the padlock
    ["Almost everything online is guarded by public-key cryptography. You hand out a public key, like an open padlock that anyone can snap shut.",
     "Only you hold the private key that opens it. And working backwards, from the padlock to the key, is practically impossible for normal computers."],
    # 2 quantum computers
    ["Quantum computers play by different rules. Their qubits use superposition and interference to attack certain problems in a completely new way.",
     "In 1994, a mathematician named Peter Shor showed that a big enough quantum computer could pick exactly these locks.",
     "For decades, that was only theory. Real machines were far too small, and far too noisy.",
     "Google's Willow chip, unveiled in 2024, has 105 qubits. Breaking real encryption would take a machine many times bigger."],
    # 3 the shrinking target
    ["But here's what has experts nervous. The size of that machine keeps shrinking.",
     "In 2012, researchers estimated that breaking a common lock called RSA would take up to a billion qubits. By 2019, twenty million. In 2025, Google said under one million.",
     "This year, new studies pushed it below a hundred thousand. One even claimed ten thousand could be enough.",
     "The machines are growing. And the finish line is moving toward them."],
    # 4 q-day
    ["So, what if Q-Day came tomorrow?",
     "Any system still using the old locks could be opened. Bank connections, card payments, private messages.",
     "Attackers could impersonate websites and forge software updates that your phone would trust.",
     "And part of the attack may already be happening. Spies can record encrypted data today, and simply wait. It's called harvest now, decrypt later."],
    # 5 bitcoin
    ["Now think about Bitcoin. Its wallets are guarded by elliptic-curve cryptography, exactly the kind of math a big enough quantum computer could break.",
     "One industry group estimates that about 6.4 million bitcoin, roughly thirty percent of all coins, sit in addresses whose public keys are already exposed.",
     "Around 1.1 million of them are believed to belong to Bitcoin's mysterious creator, Satoshi Nakamoto, untouched for over fifteen years.",
     "The first quantum computer strong enough could simply take them.",
     "Some now argue those coins should be frozen. Others say that would break Bitcoin's most sacred rule."],
    # 6 new locks
    ["The good news? We already have new locks. In 2024, the US standards agency NIST published its first post-quantum encryption standards.",
     "They're built on math problems that are believed to stump even quantum computers.",
     "NIST has proposed retiring today's vulnerable locks by 2035. Google set itself a deadline of 2029.",
     "But changing the locks on the entire internet is a monumental job. Every bank, every phone, every smart device."],
    # 7 when
    ["So when is Q-Day? Nobody knows. Some experts say as early as 2028. Most estimates land somewhere around 2030.",
     "And the same machines could also help design new medicines and materials, and simulate nature like never before.",
     "The real race isn't to build the machine. It's to change the locks before it arrives.",
     "Because on Q-Day, there won't be an alarm."],
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
