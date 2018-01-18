import markovify
import rhyme
from markovify.chain import Chain, BEGIN, END
import markovify.text

DEFAULT_TRIES = 10
DEFAULT_MAX_OVERLAP_RATIO = 0.7
DEFAULT_MAX_OVERLAP_TOTAL = 15

class rhymeText(markovify.Text):
    def __init__(self, input_text, state_size=1, chain=None, parsed_sentences=None, retain_original=True):
        can_make_sentences = parsed_sentences is not None or input_text is not None
        self.retain_original = retain_original and can_make_sentences
        self.state_size = state_size
        self.rhymeWord = ""

        if self.retain_original:
            self.parsed_sentences = parsed_sentences or list(self.generate_corpus(input_text))

            # Rejoined text lets us assess the novelty of generated sentences
            self.rejoined_text = self.sentence_join(map(self.word_join, self.parsed_sentences))
            self.chain = chain or Chain(self.parsed_sentences, state_size)
        else:
            if not chain:
                parsed = parsed_sentences or self.generate_corpus(input_text)
            self.chain = chain or Chain(parsed, state_size)

    def chooseRhymingWord(self, rhymeWord, matchedWord=None):
        rhymeList = rhyme.generateRhymes(rhymeWord, 2)
        if rhymeList is None:
            return None
        for word in rhymeList:
            formatted = (word,)
            formattedPunc = (word + '.',)

            if formatted in self.chain.model:
                matchedWord = formatted
                return matchedWord

            elif formattedPunc in self.chain.model:
                macthedWord = formattedPunc
                return matchedWord

        return None

    def make_sentence(self, rhymeWord, init_state=None, **kwargs):
            init_state = self.chooseRhymingWord(rhymeWord)
            if(init_state == None):
                return None
            tries = kwargs.get('tries', DEFAULT_TRIES)
            mor = kwargs.get('max_overlap_ratio', DEFAULT_MAX_OVERLAP_RATIO)
            mot = kwargs.get('max_overlap_total', DEFAULT_MAX_OVERLAP_TOTAL)
            test_output = kwargs.get('test_output', True)
            max_words = kwargs.get('max_words', None)

            if init_state != None:
                prefix = list(init_state)
                for word in prefix:
                    if word == BEGIN:
                        prefix = prefix[1:]
                    else:
                        break
            else:
                prefix = []

            for _ in range(tries):
                words = prefix + self.chain.walk(init_state)
                if max_words != None and len(words) > max_words:
                    continue
                if test_output and hasattr(self, "rejoined_text"):
                    if self.test_sentence_output(words, mor, mot):
                        return self.word_join(words)
                else:
                    return self.word_join(words)
            return None

    def make_short_sentence(self, max_chars, rhymeWord, min_chars=0, **kwargs):

        tries = kwargs.get('tries', DEFAULT_TRIES)

        for _ in range(tries):
            sentence = self.make_sentence(rhymeWord, **kwargs)
            if sentence and len(sentence) <= max_chars and len(sentence) >= min_chars:
                return sentence

def reverseCorpus(infile, outfile):

    with open(infile, 'rb') as f, open(outfile, 'w') as fout:
        for s in f:
            words = s.split()
            words.reverse()
            fout.write("\n" + ' '.join(words))

def buildModels(fFile, rFile):

    with open(fFile) as f:
        forwardText = f.read()

    with open(rFile) as r:
        revText = r.read()

    forwardModel = markovify.Text(forwardText)
    revModel = rhymeText(revText)

    return (forwardModel, revModel)

def buildRhymeSentence( fModel, revModel):
    stanza = []
    startSentence = fModel.make_short_sentence(150)
    rhymeWord = startSentence.split()[-1][:-1]
    while True:
        rhymeSentence = revModel.make_short_sentence(150, rhymeWord)
        if rhymeSentence:
            rev = ' '.join(rhymeSentence.split()[::-1])
            stanza.append(startSentence)
            forwardRhyme = (' ').join(rev.split()[1:])
            formattedLine = forwardRhyme[0].upper() + forwardRhyme[1:]
            stanza.append(forwardRhyme)
            return stanza
            break
        else:
            startSentence = fModel.make_short_sentence(150)
            rhymeWord = startSentence.split()[-1][:-1]

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

