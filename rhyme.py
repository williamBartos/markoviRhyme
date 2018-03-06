import nltk

def generateRhymes(input, order):
    pronunDict = dict(nltk.corpus.cmudict.entries()) # CMU Pronunciation Dictionary, contains phonemes used to match rhyming words
    rhymeList = []

    inputSyllables = pronunDict.get(input)

    if inputSyllables:
        rhymeList += [word for word, pronun in pronunDict.items() if pronun[-order:] == inputSyllables[-order:] and word != input]
        return rhymeList



