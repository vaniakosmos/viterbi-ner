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
        self.unograms_count = {}
        self.bigrams_count = {}
        self.trigrams_count = {}

        with open('data/ngrams.count') as file:
            for line in file:
                gram_type, count, *ngram = line.split()

                count = int(count)
                ngram = ' '.join(ngram)

                if '1-' in gram_type:
                    self.unograms_count[ngram] = count
                elif '2-' in gram_type:
                    self.bigrams_count[ngram] = count
                elif '3-' in gram_type:
                    self.trigrams_count[ngram] = count

    def print_logs(self, i=-1):
        if i == -1:
            for log in self.logs:
                self._print_log(log)
        else:
            log = self.logs[i]
            self._print_log(log)

    def _print_log(self, log):
        for line in log:
            print(line)
        print('\n' + ' -' * 33 + '\n')


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

        self.logs.append([])

        init = 'O I-NP'
        v = [{init: {'prob': 1.0, 'prev': init, 'word': '*', 'emission': 1.0}}]

        for word, *os in obs:
            v.append({})
            if word in self.count_xy:
                for tag in self.tags:
                    emission = self.count_xy[word].get(tag, 0) / self.count_y[tag] * 10
                    ngram = tag + ' ' + ' '.join(os)
                    self._determine_max_transaction(word, ngram, emission, v)
            else:
                if not re.match(r'[A-Z].*', word) or len(v) == 2 and self.count_xy.get(word.lower(), None):
                    tag = 'O'
                else:
                    tag = self._rules(v, word)
                emission = 1.0
                ngram = tag + ' ' + ' '.join(os)
                self._determine_max_transaction(word, ngram, emission, v)

        tag_pos, o = max([(key, val) for key, val in v[-1].items()],
                         key=lambda x: x[1]['prob'])
        tag, *os = tag_pos.split()

        res = [(obs[-1][0], tag)]
        previous = o['prev']
        for i in range(1, len(v) - 1):
            o = v[-i - 1][previous]
            word, tag_pos = obs[-i - 1][0], previous
            tag, *os = tag_pos.split()
            res.append((word, tag))
            previous = o['prev']
        return res[::-1]

    def _rules(self, v, word) -> str:
        ngram = max(v[-2].keys(), key=lambda x: v[-2][x]['prob'])
        prev_tag, syn = ngram.split()
        prev_word = v[-2][ngram]['word'].lower()
        if (prev_tag.endswith('PER') or
                syn.endswith('VP')):
            return 'I-PER'
        elif (prev_tag.endswith('ORG') or
              re.match(r'[A-Z].*[A-Z].*', word) or
              prev_word == 'the'):
            return 'I-ORG'
        else:
            return 'I-PER'

    def _determine_max_transaction(self, word, tag_pos, emission, v):
        uno_count = self.unograms_count.get(tag_pos, 0)
        cache = []

        for prev_tag in v[-2]:
            bi_count = self.bigrams_count.get(' '.join([prev_tag, tag_pos]), 0)
            # tri_count = self.trigrams_count.get(' '.join([v[-2][prev_tag]['prev'], prev_tag, tag_pos]), 0)

            transition = v[-2][prev_tag]['prob'] * (bi_count + 1) / (uno_count + 2)
            cache.append((prev_tag, transition))

        max_prev, max_t = max(cache, key=lambda x: x[1])
        prob = emission * max_t
        v[-1][tag_pos] = {'prob': prob, 'prev': max_prev, 'word': word, 'emission': emission}
        self.logs[-1].append(f'{word:11s} {max_prev:15s} {tag_pos:15s} {emission:.3e} {max_t:.3e} {prob:.3e}')


def tokenize(text: str) -> list:
    """
    :param text: paragraph or sentence
    :return: list of tokens
    """
    text = re.sub(r'([.,])', r' \1 ', text)
    return text.split()


def check_viterbi():
    tagger = ViterbiTagger(verbose=False)

    with open('corpus/min.test') as file:
        obs = []
        right = []
        for line in file:
            line = line.strip()
            if line:
                word, pos, syn, tag = line.split()
                obs.append((word, syn))
                right.append(tag)
            else:
                combos = tagger.calculate(obs)
                obs = []
                for word, tag in combos:
                    print(f' {word:11s} {tag:7s} {right.pop(0)}')
                print()
    # tagger.print_logs(-1)


def main():
    check_viterbi()


if __name__ == '__main__':
    main()
