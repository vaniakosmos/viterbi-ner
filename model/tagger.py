import re
from math import log
from pprint import pprint
from typing import List, Tuple

from model.count import featurize


class Tagger(object):
    def __init__(self):
        self.tags = ('I-ORG', 'I-MISC', 'I-PER', 'I-LOC', 'B-LOC', 'B-MISC', 'B-ORG', 'O')
        self._set_words_count()
        # self._set_n_grams_count()
        self._set_features()

    def calculate(self, obs) -> list:
        """
        Support different implementations of NER algorithms.
        :param obs: list of observations.
        :return: list of tuple: ({observation}, {tag})
        """
        pass

    def _set_features(self):
        self.n_feature = 5
        self.features = [{'uno': {}, 'duo': {}} for _ in range(self.n_feature)]

        for i in range(self.n_feature):
            with open(f'data/feature{i}.count', 'r') as file:
                for line in file:
                    typ, count, *gram = line.split()
                    gram = ' '.join(gram)
                    self.features[i][typ][gram] = int(count)

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
    def calc_str(self, sentence: str):
        obs = []
        for word in sentence.split():  # tokenize sentence
            pos = ''  # get POS tag
            syn = ''  # get syntactic chunk
            obs.append((word, pos, syn))
        return self.calculate(obs)

    def calculate(self, obs: List[Tuple[str, str, str]]):
        """
        :param obs: list of marked observations that was got from sentence, 
            `[ (word, pos, syn) ]`
        :return: list of tagged observations, 
            `[ (word, NER tag) ]` 
        """
        if not obs:
            return []
        v = self.prob_seq(obs)
        # pprint(v, width=60)
        return self.backtrack_prob_seq(obs, v)

    def prob_seq(self, obs):
        prev_features = '* *'.split()
        v = [{'*': {'prob': 0, 'prev': '*', 'features': prev_features, 'word': '*'}}]

        for word, pos, syn in obs:
            v.append({})
            if word in self.count_xy:
                for tag in self.tags:
                    # emission = self.count_xy[word].get(tag, 0) / self.count_y[tag]
                    emission = self.smooth(self.count_xy[word].get(tag, 0), self.count_y[tag])
                    features = featurize(word, pos, syn, tag)
                    v[-1][tag] = self.determine_max_transaction(features, v[-2], emission, word)
            else:
                tag = self.apply_rules(word, pos, syn, v[-2])
                emission = 0
                features = featurize(word, pos, syn, tag)
                v[-1][tag] = self.determine_max_transaction(features, v[-2], emission, word)
        return v

    def determine_max_transaction(self, features, prev_tags, emission, word):
        tags_trans = []

        for prev_tag in prev_tags:
            prev_features = prev_tags[prev_tag]['features']
            transition = prev_tags[prev_tag]['prob']

            for i, f1, f2 in zip(range(1), prev_features, features):
                uno_count = self.features[i]['uno'].get(f2, 0)
                duo_count = self.features[i]['duo'].get(f'{f1} {f2}', 0)
                transition += self.smooth(duo_count, uno_count)

            tags_trans.append((prev_tag, transition, prev_features))

        max_prev, max_trans, max_prev_features = max(tags_trans, key=lambda x: x[1])
        prob = emission + max_trans
        return {'prob': prob, 'prev': max_prev, 'features': features, 'word': word}

    @staticmethod
    def smooth(a, b):
        if a == 0:
            return -100
        return log(a / b)

    @staticmethod
    def backtrack_prob_seq(obs, v):
        tag, connected_tags = max(list(v[-1].items()), key=lambda x: x[1]['prob'])

        res = [(obs[-1][0], tag)]
        previous = connected_tags['prev']
        for i in range(1, len(v) - 1):
            connected_tags = v[-i-1][previous]
            word, tag = obs[-i-1][0], previous
            previous = connected_tags['prev']
            res.append((word, tag))
        return res[::-1]

    def apply_rules(self, word, pos, syn, prev_tags) -> str:
        # todo: get prev and curr features as parameters
        """
        :return: tag determined by handwritten rules
        """
        if not re.match(r'[A-Z].*', word) or self.count_xy.get(word.lower(), None):
            return 'O'

        max_prev_tag = max(prev_tags.keys(), key=lambda x: prev_tags[x]['prob'])
        prev_word = prev_tags[max_prev_tag]['word'].lower()

        prev_syn, prev_pos, *_ = prev_tags[max_prev_tag]['features']

        if (max_prev_tag.endswith('PER') or
                prev_syn.endswith('VP')):
            return 'I-PER'
        elif (max_prev_tag.endswith('ORG') or
              re.match(r'[A-Z].*[A-Z].*', word) or
              prev_word == 'the'):
            return 'I-ORG'
        else:
            return 'I-PER'


def tokenize(text: str) -> list:
    """
    :param text: paragraph or sentence
    :return: list of tokens
    """
    text = re.sub(r'([.,])', r' \1 ', text)
    return text.split()


def check_viterbi():
    tagger = ViterbiTagger()

    with open('corpus/min.test') as file:
        obs = []
        right = []
        for line in file:
            line = line.strip()
            if line:
                word, pos, syn, tag = line.split()
                obs.append((word, pos, syn))
                right.append(tag)
            else:
                combos = tagger.calculate(obs)
                obs = []
                for word, tag in combos:
                    print(f' {word:11s} {tag:7s} {right.pop(0)}')
                print()
                # break
    # tagger.print_logs(-1)


def main():
    check_viterbi()


if __name__ == '__main__':
    main()
