# State of the art

Andrew McCallum and Wei Li, results for Named Entity Recognition with Conditional Random Fields.

```
eng.testa
processed 51578 tokens with 5942 phrases; found: 5827 phrases; correct: 5235.
accuracy:  97.90%; precision:  89.84%; recall:  88.10%; FB1:  88.96
              LOC: precision:  93.82%; recall:  91.78%; FB1:  92.79
             MISC: precision:  83.99%; recall:  78.52%; FB1:  81.17
              ORG: precision:  84.23%; recall:  82.03%; FB1:  83.11
              PER: precision:  92.64%; recall:  93.65%; FB1:  93.14
eng.testb
processed 46666 tokens with 5648 phrases; found: 5583 phrases; correct: 4719.
accuracy:  96.56%; precision:  84.52%; recall:  83.55%; FB1:  84.04
              LOC: precision:  87.23%; recall:  87.65%; FB1:  87.44
             MISC: precision:  74.44%; recall:  71.37%; FB1:  72.87
              ORG: precision:  79.52%; recall:  78.33%; FB1:  78.92
              PER: precision:  91.05%; recall:  89.98%; FB1:  90.51
```

# Naive

```
eng.testa
processed 51578 tokens with 6003 phrases; found: 5942 phrases; correct: 3897.
accuracy:  93.48%; precision:  65.58%; recall:  64.92%; FB1:  65.25
              LOC: precision:  78.99%; recall:  81.15%; FB1:  80.06  1837
             MISC: precision:  69.41%; recall:  51.65%; FB1:  59.23  922
              ORG: precision:  60.85%; recall:  53.79%; FB1:  57.10  1341
              PER: precision:  53.75%; recall:  67.85%; FB1:  59.98  1842

eng.testb
processed 46666 tokens with 5246 phrases; found: 5648 phrases; correct: 2924.
accuracy:  90.84%; precision:  51.77%; recall:  55.74%; FB1:  53.68
              LOC: precision:  77.04%; recall:  74.58%; FB1:  75.79  1668
             MISC: precision:  60.11%; recall:  40.69%; FB1:  48.53  702
              ORG: precision:  47.50%; recall:  51.67%; FB1:  49.50  1661
              PER: precision:  26.47%; recall:  44.63%; FB1:  33.23  1617

```


# Viterbi

- Emission: tag
- Transition: tag

```
eng.testa
processed 51578 tokens with 5960 phrases; found: 5942 phrases; correct: 3863.
accuracy:  93.11%; precision:  65.01%; recall:  64.82%; FB1:  64.91
              LOC: precision:  79.53%; recall:  76.09%; FB1:  77.77  1837
             MISC: precision:  69.74%; recall:  57.21%; FB1:  62.85  922
              ORG: precision:  56.52%; recall:  50.74%; FB1:  53.47  1341
              PER: precision:  54.34%; recall:  70.39%; FB1:  61.34  1842

eng.testb
processed 46666 tokens with 5188 phrases; found: 5648 phrases; correct: 2865.
accuracy:  90.26%; precision:  50.73%; recall:  55.22%; FB1:  52.88
              LOC: precision:  76.74%; recall:  69.68%; FB1:  73.04  1668
             MISC: precision:  59.26%; recall:  43.51%; FB1:  50.18  702
              ORG: precision:  43.35%; recall:  49.28%; FB1:  46.12  1661
              PER: precision:  27.77%; recall:  48.07%; FB1:  35.20  1617
```

---

- Emission: tag
- Transition: tag
- Using O prefix instead of * when calculating transition for first words in sentences.

```
eng.testa
processed 51578 tokens with 5786 phrases; found: 5942 phrases; correct: 3873.
accuracy:  93.52%; precision:  65.18%; recall:  66.94%; FB1:  66.05
              LOC: precision:  79.53%; recall:  84.35%; FB1:  81.87  1837
             MISC: precision:  68.33%; recall:  54.74%; FB1:  60.78  922
              ORG: precision:  58.46%; recall:  52.51%; FB1:  55.33  1341
              PER: precision:  54.18%; recall:  70.78%; FB1:  61.38  1842
eng.testb
processed 46666 tokens with 5018 phrases; found: 5648 phrases; correct: 2863.
accuracy:  90.73%; precision:  50.69%; recall:  57.05%; FB1:  53.68
              LOC: precision:  76.56%; recall:  76.51%; FB1:  76.54  1668
             MISC: precision:  58.40%; recall:  42.09%; FB1:  48.93  702
              ORG: precision:  44.13%; recall:  50.52%; FB1:  47.11  1661
              PER: precision:  27.40%; recall:  47.94%; FB1:  34.87  1617
```

---

- Emission: tag
- Transition: tag + pos

```
eng.testa
processed 51578 tokens with 5942 phrases; found: 5333 phrases; correct: 3990.
accuracy:  90.92%; precision:  74.82%; recall:  67.15%; FB1:  70.78
              LOC: precision:  90.71%; recall:  79.21%; FB1:  84.57  1604
             MISC: precision:  84.40%; recall:  74.51%; FB1:  79.15  814
              ORG: precision:  56.18%; recall:  65.77%; FB1:  60.60  1570
              PER: precision:  71.82%; recall:  52.44%; FB1:  60.62  1345
eng.testb
processed 46666 tokens with 5648 phrases; found: 4626 phrases; correct: 3033.
accuracy:  89.21%; precision:  65.56%; recall:  53.70%; FB1:  59.04
              LOC: precision:  82.24%; recall:  75.78%; FB1:  78.88  1537
             MISC: precision:  67.47%; recall:  63.53%; FB1:  65.44  661
              ORG: precision:  57.69%; recall:  52.14%; FB1:  54.78  1501
              PER: precision:  49.30%; recall:  28.26%; FB1:  35.93  927
```

---

- Emission: tag
- Transition: tag + syn
- -

```
eng.testa
processed 51578 tokens with 5942 phrases; found: 5210 phrases; correct: 4083.
accuracy:  94.42%; precision:  78.37%; recall:  68.71%; FB1:  73.22
              LOC: precision:  92.85%; recall:  78.44%; FB1:  85.04  1552
             MISC: precision:  82.41%; recall:  77.22%; FB1:  79.73  864
              ORG: precision:  66.41%; recall:  69.57%; FB1:  67.95  1405
              PER: precision:  71.78%; recall:  54.13%; FB1:  61.71  1389
eng.testb
processed 46666 tokens with 5648 phrases; found: 4729 phrases; correct: 3075.
accuracy:  91.32%; precision:  65.02%; recall:  54.44%; FB1:  59.27
              LOC: precision:  83.97%; recall:  75.66%; FB1:  79.60  1503
             MISC: precision:  65.80%; recall:  65.24%; FB1:  65.52  696
              ORG: precision:  55.63%; recall:  53.82%; FB1:  54.71  1607
              PER: precision:  49.95%; recall:  28.51%; FB1:  36.30  923
```

---

- Emission: tag
- Transition: tag + syn
- custom rules for rare words

```
eng.testa
processed 51578 tokens with 6340 phrases; found: 5942 phrases; correct: 4958.
accuracy:  96.76%; precision:  83.44%; recall:  78.20%; FB1:  80.74
              LOC: precision:  81.06%; recall:  91.29%; FB1:  85.87  1837
             MISC: precision:  77.11%; recall:  81.91%; FB1:  79.44  922
              ORG: precision:  76.21%; recall:  64.20%; FB1:  69.69  1341
              PER: precision:  94.25%; recall:  77.19%; FB1:  84.87  1842
eng.testb
processed 46666 tokens with 6248 phrases; found: 5648 phrases; correct: 4367.
accuracy:  95.11%; precision:  77.32%; recall:  69.89%; FB1:  73.42
              LOC: precision:  77.82%; recall:  85.45%; FB1:  81.46  1668
             MISC: precision:  66.38%; recall:  64.90%; FB1:  65.63  702
              ORG: precision:  67.55%; recall:  61.85%; FB1:  64.58  1661
              PER: precision:  91.59%; recall:  67.41%; FB1:  77.66  1617
```
