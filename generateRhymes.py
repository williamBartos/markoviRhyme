import markovify
import markovify.text
import markoviRhyme as markoviRhyme

def reverseCorpus(infile, outfile):

    with open(infile, 'r') as f, open(outfile, 'w') as fout:
        for s in f:
            if s is not None:
                words = s.split()
                words.reverse()
                #formattedPunc = words[0][-1] + words[0][:-1]
                #words[0] = formattedPunc
                fout.write("\n" + ' '.join(words))

def buildModels(fFile, rFile):

    with open(fFile) as f:
        forwardText = f.read()

    with open(rFile) as r:
        revText = r.read()

    forwardModel = markovify.Text(forwardText)
    revModel = markoviRhyme.rhymeText(revText)

    return (forwardModel, revModel)

def uppercaseSentence(sentence):
    return sentence[0].upper() + sentence[1:]


def formatReverseSentence(sentence):
    rev = ' '.join(sentence.split()[::-1])
    forwardRhyme = (' ').join(rev.split()[1:])
    return uppercaseSentence(forwardRhyme)


def buildRhymeSentence(fModel, revModel):
    stanza = []

    while True:
        startSentence = fModel.make_short_sentence(150)
        rhymeWord = startSentence.split()[-1][:-1]
        rhymeSentence = revModel.make_short_sentence(150, rhymeWord)

        if rhymeSentence:
            stanza.append(uppercaseSentence(startSentence))
            forwardRhyme = formatReverseSentence(rhymeSentence)
            stanza.append(forwardRhyme)
            return stanza
            break

def buildStanzas(lineCount, fFile, rFile):
    stanza = []
    forwardModel, reverseModel = buildModels(fFile, rFile)
    lines = int(lineCount/2)

    for i in range(lines):
        line = buildRhymeSentence(forwardModel, reverseModel)
        stanza.append(line)

    for s in stanza:
        for line in s:
            print(line)

if __name__ == "__main__":
    # Example
    buildStanzas(4, "don.txt", "donr.txt")