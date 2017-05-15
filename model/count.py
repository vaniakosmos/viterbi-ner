def corpus_iter():
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
        1-GRAM  8286    I-LOC
        2-GRAM  86      I-MISC I-ORG
        3-GRAM  10      I-LOC B-LOC O
    """
    ngram_counts = {
        '1': {},
        '2': {},
        '3': {},
    }
    two, tri = ['*'], ['*', '*']

    for word, pos, syn, tag in corpus_iter():
        two.append(tag)
        tri.append(tag)

        # 1-gram
        increment_dict(ngram_counts['1'], tag)

        # 2-gram
        ngram = ' '.join(two[-2:])
        increment_dict(ngram_counts['2'], ngram)

        # 3-gram
        ngram = ' '.join(tri[-3:])
        increment_dict(ngram_counts['3'], ngram)

        if word == '.':
            two, tri = ['*'], ['*', '*']

    with open('data/ngrams.count', 'w') as file:
        for key, ngrams in ngram_counts.items():
            for ngram, count in ngrams.items():
                count = str(count)
                file.write(f'{key}-GRAM  {count:7s} {ngram}\n')


def increment_dict(d: dict, key):
    if key not in d:
        d[key] = 1
    else:
        d[key] += 1


def main():
    count_words()
    count_n_grams()


if __name__ == '__main__':
    main()
