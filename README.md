# markoviRhyme
A markov chain generator to create rhyming sentences using Markovify and NLTK

## What is a Markov Chain?
A Markov chain is a stochastic process that describes a set of states. The process begins at a starting state, and steps from one state to the next via random choices. The Markov Property is the key this process - it states that the probability of transitioning to the next state relies solely on the current state and time elapsed:

## <center> *∀i∀j, Pij ∈ [0,1]*, </center>

<center> Where i is the current state, j is the next state, and Pij represents the transition probability from i to j. </center>

Markov Chains can be used to generate new sentences from a corpus of existing text. From this corpus a model is generated. The model is represented as a hashmap of a hashmap, wherin the outer map represents every possible state in the corpus, and the inner map represents the possibilites from that state to the next state. To generate a new sentence, a starting state is chosen from the model. The algorithm will then begin stepping from this beginning state, until an ending state is reached. The step function of the model will randomly choose it's next state from its reachable states.


<p align="center">
  <img src="http://i.imgur.com/hR8wpyX.png">
</p>


## Generating Rhyming Sentences with Forward and Reverse Markov Chains

### Rhyming Words

A rhyme is the repition of similar sounds between two words. For this project, I chose to use syllabic rhyming. I define the degree of rhyming as the amount of syllables to match starting from the tail of the word. *Thumb* and *Numb* are two words that rhyme solely on their tail syllable. *Rapport* and *Galore* are degree 2 rhymes. 

In order to programatically determine rhyming words, I use Python's Natural Language Toolkit (NLTK). NLTK contains the CMU Pronunciation dictionary, which is a set of 39 phonenmes. Phonemes are basic units of sound, and from these units it's possible to match rhyming words. 

 ```python
('rapport', ['R', 'AE0', 'P', 'AO1', 'R'])

('galore', ['G', 'AH0', 'L', 'AO1', 'R'])
```

### Time Constraints and Reversed Models

Generating a sentence that rhymes with it's previous sentence is unlikely within a reasonable amount of time. The algorithm will have to generate the entire sentence, and then check if the last word rhymes. A much quicker solution is to create a Markov Model of reversed sentences.

With a model of rversed sentences, we can allow the algorithm to choose the rhyming word immediately with 100% probability by 'seeding' the chain generation with the rhyming word. The algorithm will then start it's step function with it's initial state as the rhyme word. To finish just reverse the sentence again.

## Implementation

For model generation and building markov chains, the popular Markovify library is used. I've modified Markovify to generate reversed rhyming sentences. Rhyming stanzas can be build by combining pairs of sentences generated from each model.

The simplified algorithm works as follows:
* Generate a forward and reverse Markov Model from the corpus
* Build a sentence from the forward model and choose the last word as the rhyming word
* Build a reverse sentence with the rhyming word as the seed word