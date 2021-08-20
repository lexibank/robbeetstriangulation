from lingpy import *
from matplotlib import pyplot as plt
from lingpy.evaluate.acd import bcubes

wl = Wordlist.from_cldf('cldf/cldf-metadata.json', columns=["language_id", "concept_name", "value", "form", "segments", "cognacy"])
wl.add_entries("cogid", "cognacy", lambda x: int(x))

lex = LexStat(wl)
lex.get_scorer(runs=10000)

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
with open("plots/f-scores.txt") as f:
    for row in results:
        f.write(" ".join(["{0:.2f}".format(x) for x in row])+"\n")

fig = plt.Figure()
plt.plot(results[0][0], results[0][3], "o", color="cornflowerblue",
        label="SCA")
plt.plot(results[0][0], results[0][-1], "o", color="crimson",
        label="SCA")
for row in results[1:]:
    plt.plot(row[0], row[3], "o", color="cornflowerblue")
    plt.plot(row[0], row[-1], "o", color="crimson")
plt.xticks([i*0.1 for i in range(3, 10)])
plt.ylim(0.3, 1.0)
plt.xlabel("cognate detection thresholds")
plt.ylabel("B-Cubed F-scores")
plt.xticks(
        list(
            range(1, 20)
            ), ["{0:.2f}".format(i*0.05) for i in range(1, 20)], rotation=90)
plt.legend(loc=1)
plt.savefig("plots/f-scores.pdf")

