from lingpy import *
from matplotlib import pyplot as plt
from lingpy.evaluate.acd import bcubes
from clldutils.misc import slug

wl = Wordlist.from_cldf('../cldf/cldf-metadata.json', columns=["language_id",
    "concept_name", "value", "form", "segments", "language_family", "cognacy"])
wl.add_entries("cogid", "cognacy", lambda x: int(x))

lex = LexStat(wl)
lex.get_scorer(runs=10000)
lex.output('tsv', filename="lexstat-bin")

results = []

for i, t in enumerate([i*0.05 for i in range(1, 20)]):
    refsca = "sca_"+str(i)
    reflst = "lexstat_"+str(i)
    lex.cluster(method="sca", ref=refsca, threshold=t,
            cluster_method="infomap")
    lex.cluster(method="lexstat", ref=reflst, threshold=t,
            cluster_method="infomap")

    p1, r1, f1 = bcubes(lex, "cogid", refsca, pprint=False)
    p2, r2, f2 = bcubes(lex, "cogid", reflst, pprint=False)
    results += [[t, p1, r1, f1, p2, r2, f2]]
    print("{0:.2f}".format(t)+"\t"+"\t".join("{0:.2f}".format(x) for x in results[-1]))
with open("../plots/f-scores.txt", "w") as f:
    for row in results:
        f.write(" ".join(["{0:.2f}".format(x) for x in row])+"\n")
lex.add_entries("subgroup" "language_family", lambda x: x)
lex.output('tsv', filename="lexstat-thresholds", ignore="all", prettify=False)

for mode, idxA, idxB in [
        ("B-cubed precision", 1, 4), ("B-cubed recall", 2, 5), 
        ("B-cubed F-score", 3, 6)]:
    fig = plt.Figure()
    plt.plot(1, results[0][idxA], "o", color="cornflowerblue",
            label="SCA")
    plt.plot(1, results[0][idxB], "o", color="crimson",
            label="LexStat")
    for i, row in enumerate(results[1:]):
        plt.plot(i+2, row[idxA], "o", color="cornflowerblue")
        plt.plot(i+2, row[idxB], "o", color="crimson")
    plt.xticks([i*0.1 for i in range(3, 10)])
    plt.ylim(0.3, 1.0)
    plt.xlabel("cognate detection thresholds")
    plt.ylabel(mode)
    plt.xticks(
            list(
                range(1, 20)
                ), ["{0:.2f}".format(i*0.05) for i in range(1, 20)], rotation=90)
    plt.legend(loc=1)
    plt.savefig("../plots/{0}.pdf".format(slug(mode)))
    plt.clf()

