import nltk

def generateRhymes(input, order):
    pronunDict = dict(nltk.corpus.cmudict.entries())
    rhymeList = []

    inputSyllables = pronunDict.get(input)

    if inputSyllables is not None:
        rhymeList += [word for word, pronun in pronunDict.items() if pronun[-order:] == inputSyllables[-order:] and word != input]
        return rhymeList



