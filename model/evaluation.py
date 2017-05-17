from pprint import pprint

from model.tagger import NaiveTagger, ViterbiTagger


def write_result(test_file, tagger):
    res = []
    tokens = 0
    with open('corpus/' + test_file) as file:
        obs = []
        original = []
        for line in file:
            line = line.strip()
            if line:
                word, pos, syn, tag = line.split()
                obs.append((word, syn))
                original.append((tag, syn))
            else:
                combos = tagger.calculate(obs)
                for i, x in enumerate(combos):
                    word, tag = x
                    r_tag, syn = original[i]
                    # res.append(f'{word:15s} {syn:7s} {" " if tag == r_tag else "x"}  {tag:7s} {r_tag}')
                    res.append(f'{word} {tag} {r_tag}')

                res.append('')
                tokens += len(combos)
                obs = []
                original = []

    with open('result/' + test_file, 'w') as file:
        for line in res:
            file.write(line + '\n')

    return tokens


def main():
    # tagger = NaiveTagger(verbose=False)
    tagger = ViterbiTagger(verbose=False)

    files = [
        'eng.testa',
        'eng.testb',
        # 'eng.train'
    ]

    for test_file in files:
        write_result(test_file, tagger)

if __name__ == '__main__':
    main()
