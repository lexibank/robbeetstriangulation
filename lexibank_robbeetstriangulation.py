from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import Language, FormSpec, Cognate

from clldutils.misc import slug
import attr


@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)


@attr.s
class CustomCognate(Cognate):
    Root = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "robbeetstriangulation"
    language_class = CustomLanguage
    cognate_class = CustomCognate
    form_spec = FormSpec(
        missing_data=("–", "-"),
        brackets={"(": ")", "[": "]", "{": "}"},
        first_form_only=True,
        separators=(";", "/", "~", ","),
        replacements=[
            (" inf. = soˁḳïš ?", ""),
            ("arla < avərla", "arla"),
            ("? (köterip) ", ""),
            ("olur-. olïr-", "olur"),
            ("?? ", ""),
            (" + 'motion verb'", ""),
            ("kele-", "kele"),
            ("'(walking) stick'", ""), (" + motion verb", ""), (" ", "_")]
    )

    def cmd_download(self, args):

        self.raw_dir.xls2csv("16_Eurasia3angle_synthesis_SI 1_BV 254.xls")

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.number + '_' + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concepts[concept.english] = idx
        concepts['child (n.)'] = concepts['child (kin term) (n.)']
        concepts['woods  (n.)'] = concepts['wood (n.)']
        concepts['soil (n.)'] = concepts['soil (earth) (n.)']
        concepts['shade (n.)'] = concepts['shade / shadow (n.)']
        concepts['burn (v.)'] = concepts['burn (intr.) (v.)']
        concepts['leg / foot (n.)'] = concepts['leg // foot (n.)']
        concepts['skin (n.)'] = concepts['skin (hide) (n.)']
        concepts['mountain (n.)'] = concepts['mountain (hill) (n.)']
        concepts['nasal mucus'] = concepts['nasal mucus (n.)']
        concepts['1SG'] = concepts['1SG pronoun']
        concepts['rope'] = concepts['rope (n.)']
        concepts['crush (v.)'] = concepts['crush / grind (v.)']
        concepts['breast (n.)'] = concepts['breast (n.) // (chest) (n.)']

        languages = {}
        for language in self.languages:
            if language["NameInSheet"].strip():
                args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Family=language["Family"],
                    Latitude=language["Latitude"],
                    Longitude=language["Longitude"],
                    Glottocode=language["Glottocode"],
                    ISO639P3code=language["ISO639P3code"]
                )
                languages[language["NameInSheet"]] = language["ID"]
        args.writer.add_sources()
        errors = set()
        for i, row in enumerate(self.raw_dir.read_csv("16_Eurasia3angle_synthesis_SI 1_BV 254.1.csv",
                                                      dicts=True, delimiter=",")):
            # headers are inconsistent, have to clean this
            concept = row["Meaning"].strip()
            proto = row["MRCA Root"]
            for language, lid in languages.items():
                entry = row.get(language, row.get(language + ' ')).strip()
                if entry and concept in concepts:
                    for lex in args.writer.add_forms_from_value(
                            Language_ID=lid,
                            Parameter_ID=concepts[concept],
                            Value=entry,
                            Cognacy=str(i + 1)
                    ):
                        args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=str(i + 1),
                            Root=proto)
                elif concept not in concepts:
                    errors.add(concept)
        for er in errors:
            args.log.info(f"missing concept '{er}'")
