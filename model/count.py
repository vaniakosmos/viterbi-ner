from pprint import pprint
from typing import List

from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re


def corpus_iter() -> (str, str, str, str):
    """
    Iterate through every line in training data.
    Return tuple of strings for each line in following format:
        word, POS, syntactic chunk, NE tag
    Example:
        health NN I-NP O
    """
    with open('corpus/eng.train') as file:
        for line in file:
            line = line.strip()
            if line:
                yield line.split()


def count_words():
    """
    Count words for each tag.
    Save result in file using format:
        {tag} {count} {word}
    Example:
        I-LOC 456 England
    """
    tags = {}

    # get count of words for each tag
    for word, pos, syn, tag in corpus_iter():

        if tag not in tags:
            tags[tag] = {}
        if word not in tags[tag]:
            tags[tag][word] = 0

        tags[tag][word] += 1

    # save counts in file
    with open('data/words.count', 'w') as file:
        for tag, words in tags.items():
            for word, count in words.items():
                count = str(count)
                file.write(f'{tag:7s} {count:5s} {word}\n')


def count_n_grams():
    """
        Count tag n-grams.
        Save result in file using format:
            {N}-GRAM {count} {n-gram...}
        Examples:
            1-GRAM  7650    I-LOC I-NP
            2-GRAM  193     O I-VP O I-NP
            3-GRAM  21      I-PER I-NP O I-VP O I-NP
        """
    ngram_counts = {
        '1': {},
        '2': {},
        '3': {},
    }
    init = ['O', 'I-NP']

    two, tri = list(init), list(init * 2)

    for word, pos, syn, tag in corpus_iter():
        next_gram = [tag, syn]

        two.extend(next_gram)
        tri.extend(next_gram)

        # 1-gram
        nragm = ' '.join(next_gram)
        increment_dict(ngram_counts['1'], nragm)

        # 2-gram
        ngram = ' '.join(two[-4:])
        increment_dict(ngram_counts['2'], ngram)

        # 3-gram
        ngram = ' '.join(tri[-6:])
        increment_dict(ngram_counts['3'], ngram)

        if word == '.':
            two, tri = list(init), list(init * 2)

    with open('data/ngrams.count', 'w') as file:
        for key, ngrams in ngram_counts.items():
            for ngram, count in ngrams.items():
                count = str(count)
                file.write(f'{key}-GRAM  {count:7s} {ngram}\n')


def featurize(word, pos, syn, tag):
    return [
            f'{tag} {syn}',
            syn,
            pos,
            tag,
            str(word.islower()),
            str(word.isnumeric())
    ]


def count_features():
    n_feature = 5
    counter = [{'uno': {}, 'duo': {}} for _ in range(n_feature)]
    prev_features = check_sentence(n_feature, counter)

    for word, pos, syn, tag in corpus_iter():
        curr_features = featurize(word, pos, syn, tag)

        bigram_features = list(map(lambda x: f'{x[0]} {x[1]}', zip(prev_features, curr_features)))

        for c, ungram, bigram in zip(counter, curr_features, bigram_features):
            increment_dict(c['uno'], ungram)
            increment_dict(c['duo'], bigram)
        prev_features = curr_features

        if word == '.':
            prev_features = check_sentence(n_feature, counter)

    for i in range(n_feature):
        c = counter[i]
        with open(f'data/feature{i}.count', 'w') as file:
            file.write(f'')
            for typ in c:
                for gram in c[typ]:
                    count = c[typ][gram]
                    file.write(f'{typ} {count} {gram}\n')

    # pprint(counter, width=40)


def check_sentence(n_feature, counter):
    prev_features = ['*'] * n_feature
    for c, ungram in zip(counter, prev_features):
        increment_dict(c['uno'], ungram)
    return prev_features


def increment_dict(d: dict, key):
    if key not in d:
        d[key] = 1
    else:
        d[key] += 1


def main():
    # count_words()
    # print('... have counted words')
    # count_n_grams()
    # print('... have counted n-grams')
    count_features()


if __name__ == '__main__':
    import cProfile
    cProfile.run('main()')
