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
- Transition: tag pos

```

```
