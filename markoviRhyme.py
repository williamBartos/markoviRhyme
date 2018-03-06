import rhyme
from markovify.chain import Chain, BEGIN, END
import markovify.text

# Derived class from markovify.Text to generate rhyming sentences from
# a reversed markov chain

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

    def make_short_sentence(self, max_chars, rhymeWord, min_chars=0, **kwargs):

        tries = kwargs.get('tries', DEFAULT_TRIES)
        init_state = self.chooseRhymingWord(rhymeWord)

        for _ in range(tries):
            sentence = self.make_sentence(init_state=init_state, **kwargs)
            if sentence and len(sentence) <= max_chars and len(sentence) >= min_chars:
                return sentence