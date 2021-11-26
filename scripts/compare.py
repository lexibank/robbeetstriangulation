"""
Compare cognate set distributions.
"""
from pyedictor import cldf2wl
from pyedictor.util import iter_etymdict
from lexibank_robbeetsaltaic import Dataset as Altaic
from lexibank_sagartst import Dataset as ST
from lexibank_starostinpie import Dataset as IE
from lexibank_dravlex import Dataset as Dravidian
from matplotlib import pyplot as plt

def get_distributions(wordlist, subgroup_names, subgroup_name="subgroup", ref="cogid"):
    """
    Compute distributions for the violin plots.
    """
    out = []
    for cogid, (idxs, concepts, subgroups) in iter_etymdict(
            wordlist, ref, "concepts", subgroup_name):
        if True: #len(idxs) > 1:
            families = [subgroup_names.get(subgroup, subgroup) for subgroup in
                    subgroups]
            families = [f for f in families if f]
            concept = concepts[0]
            if len(idxs) >= 2 and len(set(families)) >= 2:
                out += [len(set(families))]
    return out

subgroups = {
        "ST": {
            "Bodic": "Tani-Yidu",
            "Burmish": "Tibeto-Dulong", #"Lolo-Burmese",
            "Chepang": None, #"Chepang",
            "Chin": "Kuki-Chin",
            "Deng": "Tani-Yidu",
            "Garo": "Sal",
            "Jingpho": "Sal",
            "Kiranti": "Kiranti",
            "Koch": "Sal",
            "Loloish": "Tibeto-Dulong", #"Lolo-Burmese",
            "Mikir": "Kuki-Chin",
            "Mizo": "Kuki-Chin",
            "Naga": "Kuki-Chin",
            "Nungic": "Tibeto-Dulong", #"Dulong",
            "Qiangic": "Tibeto-Dulong", #"rGyalrong",
            "Sinitic": "Sinitic",
            "Tangut": "Tibeto-Dulong", #"rGyalrong",
            "Tani": "Tani-Yidu",
            "Tibetan": "Tibeto-Dulong", #"Tibetan",
            "Tibeto-Kinauri": "Tibeto-Kinauri",
            "rGyalrong": "Tibeto-Dulong", #"rGyalrong"
            },
        "Altaic": {
            "Japonic": "Japonic",
            "Turkic": "Turkic",
            "Mongolic": "Mongolic",
            "Korean": "Koreanic",
            "Koreanic": "Koreanic",
            },
        "IE": {
            "Spanish": "Romance",
            "Czech": "Slavic",
            "Hindi": "Indo-Aryan",
            "German": "Germanic",
            "Dutch": "Germanic",
            "Portuguese": "Romance",
            "Greek": "Greek",
            "Russian": "slavic",
            "French": "Romance",
            "Polish": "Slavic",
            "Romanican": "Romance",
            "Bulgarian": "Slavic",
            "Danish": "Germanic",
            "Norwegian": "Germanic",
            "Italian": "Romance",
            "English": "Germanic",
            "Armenian": "Armenian",
            "Icelandic": "Germanic",
            "Swedish": "Germanic"
            },
        "Dravidian": {
            "Badga": "South Dravidian",
            "Betta_Kurumba": "South Dravidian",
            "Brahui": "North Dravidian",
            "Gondi": "South Dravidian",
            "Kannada": "South-Dravidian",
            "Kodava": "South Dravidian",
            "Kolami": "Central Dravidian",
            "Kota": "South Dravidian",
            "Koya": "South Dravidian II",
            "Kurukh": "North Dravidian",
            "Kuwi": "South Dravidian",
            "Malayalam": "South Dravidian",
            "Malto": "North Dravidian",
            "Ollari_Gadba": "Central Dravidian",
            "Parji": "Central Dravidian",
            "Tamil": "South Dravidian",
            "Telugu": "South Dravidian II",
            "Toda": "South Dravidian",
            "Tulu": "South Dravidian",
            "Yeruva": "South Dravidian",
            }
        }
        

plt.clf()
fig, ax = plt.subplots()
data = []
labels = []
for i, (dsname, ds, sg, cognacy) in enumerate(
        [
            ("ST", ST, "subgroup", "cognacy"), 
            ("IE", IE, "name", "cogid_cognateset_id"),
            ("Dravidian", Dravidian, "name", "cogid_cognateset_id"),
            ("Altaic", Altaic, "family", "cognacy")]):
    wl = cldf2wl(ds().cldf_dir / "cldf-metadata.json",
            addon={cognacy: "cog", "language_"+sg: "subgroup"})
    wl.renumber("cog")
    print("Loaded Wordlist {0}".format(dsname))
    dist = get_distributions(wl, subgroups[dsname])
    data += [dist]
    labels += [dsname]
ax.violinplot(data, [2, 4, 6, 8], widths=[1.8, 1.8, 1.8, 1.8])
ax.set_xticks([2, 4, 6, 8])
ax.set_xticklabels(labels)
plt.savefig("violinplots.pdf")
