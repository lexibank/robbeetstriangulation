"""
Compare external and internal delta scores for a dataset.
"""
from pyedictor import cldf2wl
from lingpy import Wordlist
from lexibank_robbeetsaltaic import Dataset as Altaic
from lexibank_sagartst import Dataset as ST
from lexibank_ielexfinal import Dataset as IE
from lexibank_dravlex import Dataset as Dravidian
from phylogemetric.delta import DeltaScoreMetric
from pylodata.wordlist import get_multistate_patterns
import statistics as stats
from tabulate import tabulate
from matplotlib import pyplot as plt
import json
from tqdm import tqdm as progressbar

def get_matrix(taxa, patterns):
    
    matrix = {t: [] for t in taxa}
    for p, v in patterns.items():
        for taxon in taxa:
            matrix[taxon] += [v[taxon][0] if v[taxon] else "-"]
    return matrix


def delta_by_subgroup(wordlist, subgroups, ref="cogid"):
    
    # get shorter wordlist
    deltas = {}
    patterns = get_multistate_patterns(wordlist, ref=ref)[0]
    delta = DeltaScoreMetric(matrix=get_matrix(wordlist.cols, patterns))

    deltas["all"] = delta.score()

    for s in progressbar(sorted(set(subgroups.values()))):
        if s.strip():
            print(s)
            D = {0: [h for h in wordlist.columns]}
            for idx, subgroup in wordlist.iter_rows("subgroup"):
                if s.strip() and subgroups[subgroup] == s:
                    D[idx] = wordlist[idx]
            wln = Wordlist(D)
            if wln.width >= 4:
                patterns = get_multistate_patterns(wln, ref=ref, missing=None)[0]
                delta = DeltaScoreMetric(matrix=get_matrix(wln.cols, patterns))
                deltas[s] = delta.score()
    return deltas


with open("subgroups.json") as f:
    subgroups = json.load(f)


for i, (dsname, ds, sg, cognacy) in enumerate(
        [
            #("Indo-European", IE, "name", "cogid_cognateset_id"),
            #("Sino-Tibetan", ST, "subgroup", "cognacy"), 
            #("Dravidian", Dravidian, "name", "cogid_cognateset_id"),
            ("Altaic", Altaic, "family", "cognacy")
            ]
            ):
    wl = cldf2wl(ds().cldf_dir / "cldf-metadata.json",
            addon={cognacy: "cog", "language_"+sg: "subgroup"})
    wl.renumber("cog")
    print("# {0}".format(dsname))

    deltas = delta_by_subgroup(wl, subgroups[dsname], ref="cogid")
    table = [
            [
                "all", 
                stats.mean(deltas["all"].values()),
                stats.stdev(deltas["all"].values())
                ]
            ]
    for s in sorted(set(subgroups[dsname].values())):
        if s in deltas:
            table += [
                   [
                       s, 
                       stats.mean(deltas[s].values()),
                       stats.stdev(deltas[s].values())
                           ]
                       ]
    print(
            tabulate(
                table, 
                headers=["Subgroup", "Delta", "STD"], tablefmt="pipe", floatfmt=".2f"))



