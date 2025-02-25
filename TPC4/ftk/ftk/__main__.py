import jjcli
from base import Pipeline, Convert2ProbabilityStage
from probability import RelativeProbabilityPerMillion

def pretty_print(freqs, opts):
    freqs = dict(sorted(freqs.items(), key=lambda item: item[1].value, reverse=True))

    if '-a' not in opts:
        freqs = {key: RelativeProbabilityPerMillion(val) for key, val in freqs.items()}

    if '-m' in opts:
        m = int(opts['-m'])
        freqs = dict((list(freqs.items())[:m]))

    for key, val in freqs.items():
        print(f'{key}\t{val}')

def main():
    """Options:
        -a: aboslute frequency
        -m N: top N words
    """

    cl = jjcli.clfilter("am:", doc=main.__doc__)
    pipe = Pipeline()
    pipe.set_reduction(Convert2ProbabilityStage())

    for txt in cl.text():
        c = pipe.apply(txt)
        pretty_print(c, cl.opt)

if __name__ == '__main__':
    main()
