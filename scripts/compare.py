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
        if len(idxs) >= 2 and len(set(families)) >= 1:
            out += [len(set(families))]
    return out

with open("subgroups.json") as f:
    subgroups = json.load(f)
        

data = []
labels = []
try:
    with open("data.json") as f:
        data, labels = json.load(f)
except:
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
with open("data.json", "w") as f:
    f.write(json.dumps([data, labels], indent=2))

plt.clf()
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
for i, (datum, ax) in enumerate(zip(data, [ax1, ax2, ax3, ax4])):
    ds = labels[i]
    for j in range(1, 11):
        count = datum.count(j) / len(datum)
        ax.bar(j, count, color="cornflowerblue")
    ax.set_xticks(range(1, 11))
    ax.set_title(ds)
    ax.set_ylim(0, 1) #400)

plt.savefig("boxes.pdf")
fig, ax = plt.subplots(figsize=(10, 2))
ax.violinplot([[x for x in row if x > 1] for row in data], [4, 8, 12, 16], widths=[3.8, 3.8, 3.8, 3.8])
ax.set_xticks([4, 8, 12, 16])
ax.set_xticklabels(labels)
plt.savefig("violin.pdf")
