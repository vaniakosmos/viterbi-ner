from pprint import pprint

from model.tagger import NaiveTagger, ViterbiTagger


def get_phrases(sentence):
    res = []
    last = 'new'
    for i, tag in enumerate(sentence):
        if tag != 'O':
            if tag[2:] == last[2:]:
                res[-1]['index'].append(i)
            else:
                res.append({'tag': tag[2:], 'index': [i]})
        last = tag
    out = {}
    for d in res:
        out[' '.join(map(str, d['index']))] = d['tag']
    return out


def compare(a, b):
    res = {}
    tags = ['LOC', 'MISC', 'ORG', 'PER']
    for tag in tags:
        res[tag] = {
            'tp': 0,
            'fp': 0,
            'fn': 0
        }
    pa = get_phrases(a)
    pb = get_phrases(b)
    for key in pa:
        if key in pb:
            res[pa[key]]['tp'] += 1
        else:
            res[pa[key]]['fn'] += 1
    # for key in pb:
    #     if key not in pa:
    #         res[pb[key]]['fp'] += 1
    return res


def sum_mat(m1, m2):
    for y in range(len(m1)):
        for x in range(len(m1[0])):
            m1[y][x] += m2[y][x]


def count_phrases(test_file):
    phrases = 0
    with open('corpus/' + test_file) as file:
        last = 'newline'
        for line in file:
            line = line.strip()
            if line:
                word, pos, syn, tag = line.split()
                if tag != 'O' and tag != last:
                    phrases += 1
                if tag[:2] == 'I-' and last[:2] == 'B-' and tag[2:] == last[2:]:
                    phrases -= 1
                last = tag
            else:
                last = "newline"
    return phrases


def print_cmat(cmat, tags):
    for tag in tags:
        print(f'{tag[:5]:7s}', end=' ')
    print()
    for row in cmat:
        for e in row:
            print(f'{str(e):7s}', end=' ')
        print()


def print_results(cmat, tags, test_file):
    """
    Output example:
        eng.testb
        processed 46666 tokens with 5648 phrases; found: 5620 phrases; correct: 5001.
        accuracy:  97.63%; precision:  88.99%; recall:  88.54%; FB1:  88.76
                      LOC: precision:  90.59%; recall:  91.73%; FB1:  91.15
                     MISC: precision:  83.46%; recall:  77.64%; FB1:  80.44
                      ORG: precision:  85.93%; recall:  83.44%; FB1:  84.67
                      PER: precision:  92.49%; recall:  95.24%; FB1:  93.85
    """
    out = [test_file]
    right = sum([cmat[i][i] for i in range(len(cmat))])
    summary = sum([sum(row) for row in cmat])
    accuracy = right / summary

    phrases = count_phrases(test_file)

    out.append(f'processed {summary} tokens with {phrases} phrases; found: {-1} phrases; correct: {-1}.')
    out.append(f'accuracy: {accuracy * 100:.2f}%')

    real_tags = ['LOC', 'MISC', 'ORG', 'PER']

    for line in out:
        print(line)
    print()

    # print_cmat(cmat, tags)


def sum_res(res, r):
    for key in res:
        for k in res[key]:
            res[key][k] += r[key][k]


def determine_cmat(test_file, tagger):
    res = {}
    tags = ['LOC', 'MISC', 'ORG', 'PER']
    for tag in tags:
        res[tag] = {
            'tp': 0,
            'fp': 0,
            'fn': 0
        }
    with open('corpus/' + test_file) as test, open('result/' + test_file) as result:
        t_sentence = []
        r_sentence = []
        for t_line in test:
            t_line = t_line.strip()
            r_line = result.readline().strip()

            if t_line is None:
                break

            if t_line:
                word, pos, syn, tag = t_line.split()
                r_tag = r_line
                t_sentence.append(tag)
                r_sentence.append(r_tag)
            else:
                r = compare(
                    t_sentence,
                    r_sentence
                )
                sum_res(res, r)
                t_sentence = []
                r_sentence = []
        pprint(res)
    return []


def write_result(test_file, tagger):
    res = []
    tokens = 0
    with open('corpus/' + test_file) as file:
        sentence = []
        c = []
        for line in file:
            line = line.strip()
            if line:
                word, pos, syn, tag = line.split()
                sentence.append(word)
                c.append(tag)
            else:
                combos = tagger.calculate(sentence)
                res.extend([f'{x[0]} {x[1]} {c[i]}' for i, x in enumerate(combos)])
                # res.extend([x[1] for x in combos])

                res.append('')
                tokens += len(combos)
                sentence = []
                c = []

    with open('result/' + test_file, 'w') as file:
        for line in res:
            file.write(line + '\n')

    return tokens


def main():
    tagger = NaiveTagger(verbose=False)
    # tagger = ViterbiTagger(verbose=False)

    files = [
        'eng.testa',
        'eng.testb',
        # 'eng.train'
    ]

    for test_file in files:
        tokens = write_result(test_file, tagger)
        cmat = determine_cmat(test_file, tagger)
        # print_results(cmat, tagger.tags, test_file)

if __name__ == '__main__':
    main()
