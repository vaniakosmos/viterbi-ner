import re
from pprint import pformat, pprint


class Tagger(object):
    def __init__(self, verbose=False):
        self.logs = []
        self.verbose = verbose

        self.tags = ('I-ORG', 'I-MISC', 'I-PER', 'I-LOC', 'B-LOC', 'B-MISC', 'B-ORG', 'O')
        self._set_words_count()
        self._set_n_grams_count()

    def calculate(self, obs) -> list:
        """
        Support different implementations of NER algorithms.
        :param obs: list of observations.
        :return: list of tuple: ({observation}, {tag})
        """
        pass

    def _set_words_count(self):
        """
        Set up words and tags count and save its in respective dictionaries in format:
            count_xy: dict[x][y] = count
            count_y: dict[y] = count
            Where: 
                x - word,
                y - tag
        """
        self.count_xy = {}
        self.count_y = {}

        self.count_yx = {}
        for tag in self.tags:
            self.count_yx[tag] = {}

        with open('data/words.count') as file:
            for line in file:
                tag, count, word = line.split()
                count = int(count)
                if word not in self.count_xy:
                    self.count_xy[word] = {}
                self.count_xy[word][tag] = count
                self.count_y[tag] = self.count_y.get(tag, 0) + count
                self.count_yx[tag][word] = count

    def _set_n_grams_count(self):
        self.bigrams_count = {}
        self.trigrams_count = {}

        with open('data/ngrams.count') as file:
            for line in file:
                gram_type, count, *ngram = line.split()

                count = int(count)
                ngram = ' '.join(ngram)

                if '2-' in gram_type:
                    self.bigrams_count[ngram] = count
                elif '3-' in gram_type:
                    self.trigrams_count[ngram] = count


class NaiveTagger(Tagger):
    def calculate(self, obs):
        """
        Naive implementation based on probability of word to be in specified tag-group.
        """
        v = []
        for word in obs:
            res = 'O'
            max_p = 0.0
            for tag in self.tags:
                if word in self.count_yx[tag]:
                    p = self.count_yx[tag][word] / self.count_y[tag]
                    if p > max_p:
                        max_p = p
                        res = tag
            v.append((word, res))
        return v


class ViterbiTagger(Tagger):
    def calculate(self, obs):
        if not obs:
            return []

        v = [
            {'*': {'prob': 1.0, 'prev': '*', 'word': '*'}},
        ]

        for word in obs:
            v.append({})
            if word in self.count_xy:
                for tag in self.tags:
                    emission = self.count_xy[word].get(tag, 0) / self.count_y[tag]
                    self._fill_(word, tag, emission, v)
            else:
                tag = 'O'
                emission = 1.0
                self._fill_(word, tag, emission, v)

        # self.logs.append(pformat(v, indent=2, compact=False, width=40))

        tag, o = max([(key, val) for key, val in v[-1].items()],
                     key=lambda x: x[1]['prob'])

        res = [(obs[-1], tag)]
        previous = o['prev']
        for i in range(1, len(v)-1):
            o = v[-i-1][previous]
            word, tag = obs[-i-1], previous
            res.append((word, tag))
            previous = o['prev']
        return res[::-1]

    def _fill_(self, word, tag, emission, v):
        max_t = None
        max_prev = None
        for prev_tag in v[-2]:
            tri_count = self.trigrams_count.get(' '.join([v[-2][prev_tag]['prev'], prev_tag, tag]), 0)
            bi_count = self.bigrams_count.get(' '.join([prev_tag, tag]), 0)
            # transition = v[-2][prev_tag]['prob'] * bi_count / self.count_y.get(tag)
            transition = v[-2][prev_tag]['prob'] * tri_count / bi_count if bi_count else 0
            if max_t is None or transition > max_t:
                max_t = transition
                max_prev = prev_tag
        prob = emission * max_t
        v[-1][tag] = {'prob': prob, 'prev': max_prev, 'word': word}
        self.logs.append(f'{word:11s} {tag:7s} {emission:.3e} {transition:.3e} {prob:.3e}')


def tokenize(text: str) -> list:
    """
    :param text: paragraph or sentence
    :return: list of tokens
    """
    text = re.sub(r'([.,])', r' \1 ', text)
    return text.split()


def main():
    tagger = ViterbiTagger(verbose=False)
    tests = [
        'The European Commission said on Thursday it disagreed '
        'with German advice to consumers to shun British lamb '
        'until scientists determine whether mad cow disease can '
        'be transmitted to sheep to New York or farther.',
    ]
    for text in tests:
        combos = tagger.calculate(tokenize(text))
        for word, tag in combos:
            print(f' {word:11s} {tag}')
        print()


if __name__ == '__main__':
    main()
