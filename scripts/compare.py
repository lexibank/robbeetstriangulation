"""
Compare cognate set distributions.
"""
from pyedictor import cldf2wl
from pyedictor.util import iter_etymdict
from lexibank_robbeetsaltaic import Dataset as Altaic
from lexibank_sagartst import Dataset as ST
#from lexibank_starostinpie import Dataset as IE
from lexibank_ielexfinal import Dataset as IE
from lexibank_dravlex import Dataset as Dravidian
from matplotlib import pyplot as plt
import json

def get_distributions(wordlist, subgroup_names, subgroup_name="subgroup", ref="cogid"):
    """
    Compute distributions for the violin plots.
    """
    out = []
    for cogid, (idxs, concepts, subgroups) in iter_etymdict(
            wordlist, ref, "concepts", subgroup_name):
        families = [subgroup_names.get(subgroup, subgroup) for subgroup in
                subgroups]
        families = [f for f in families if f.strip()]
        concept = concepts[0]
        if len(idxs) >= 2 and len(set(families)) >= 2:
            out += [len(set(families))]
    return out

with open("subgroups.json") as f:
    subgroups = json.load(f)
        

plt.clf()
fig, ax = plt.subplots(figsize=(10, 3))
data = []
labels = []
for i, (dsname, ds, sg, cognacy) in enumerate(
        [
            ("IE", IE, "name", "cogid_cognateset_id"),
            ("ST", ST, "subgroup", "cognacy"), 
            ("Dravidian", Dravidian, "name", "cogid_cognateset_id"),
            ("Altaic", Altaic, "family", "cognacy")]):
    wl = cldf2wl(ds().cldf_dir / "cldf-metadata.json",
            addon={cognacy: "cog", "language_"+sg: "subgroup"})
    wl.renumber("cog")
    print("Loaded Wordlist {0}".format(dsname))
    dist = get_distributions(wl, subgroups[dsname])
    data += [dist]
    labels += [dsname]
ax.violinplot(data, [4, 8, 12, 16], widths=[3.8, 3.8, 3.8, 3.8])
ax.set_xticks([4, 8, 12, 16])
ax.set_xticklabels(labels)
plt.savefig("violinplots.pdf")
