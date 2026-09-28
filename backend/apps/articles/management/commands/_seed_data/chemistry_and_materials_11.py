"""Chemistry and Materials — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Alchemy",
        "category": "Chemistry and Materials",
        "categories": ["History", "Philosophy and Religion"],
        "short_description": (
            "Pre-modern chemistry: laboratory craft, transmutation theory and symbolic language"
        ),
        "summary": (
            "Alchemy was the pre-modern science of matter, pursuing the transmutation of metals "
            "and chemical medicines while building the apparatus, reagents and techniques that "
            "chemistry inherited. It was not treated as distinct from chemistry until about 1700."
        ),
        "content": """**Alchemy** is the pre-modern science of matter, combining laboratory work on
metals, minerals and distilled substances with theories of transmutation and, in several
traditions, a symbolic reading of chemical change. Practised from Hellenistic Egypt to
eighteenth-century Europe, and independently in China and India, it produced most of the
apparatus, reagents and techniques that chemistry later took over.

## Name and scope

The English word reached modern usage through medieval Latin *alchimia* from Arabic
*al-kimiya*, itself probably from Greek *khemeia*, a term connected with the working of
metals. For most of its history alchemy was not a separate thing from chemistry.
Seventeenth-century authors wrote of *chymistry* and used "alchemy" and "chemistry"
interchangeably for a single discipline covering assaying, pharmacy, pigment-making,
distilling and the pursuit of gold; the modern division, in which alchemy means credulous
gold-making and chemistry means science, was not settled until about 1700 and was then read
backwards onto earlier centuries.[^newmanprincipe] Historians of science accordingly use
"chymistry" for the undivided early modern field.

Alchemical projects fell into three broad groups: *chrysopoeia*, the transmutation of base
metals into gold or silver; the preparation of elixirs and chemically compounded medicines;
and the ordinary manufacture of acids, salts, alloys, pigments and spirits, which paid for
the rest.

## Greco-Egyptian beginnings

The oldest surviving alchemical texts are Egyptian recipe collections of the third and
fourth centuries CE, the Leyden and Stockholm papyri, which give practical instructions for
imitating gold, silver, gemstones and purple dye. Written alchemy grew up in the same
Greek-speaking scholarly world as the mathematics and astronomy of
[[The Library of Alexandria|Alexandria]], and it took its theory from [[Aristotle|Aristotelian]]
natural philosophy: four elements, four qualities, and matter capable in principle of taking
any form. Zosimos of Panopolis, active around 300 CE, is the earliest alchemist whose
writings survive in quantity; they move without warning between furnace instructions and
allegorical dream visions, a mixture typical of the literature. Maria the Jewess, quoted by
Zosimos, is traditionally credited with the sealed heating vessel called the *kerotakis* and
with the gentle water bath that survives in kitchens as the *bain-marie*.

Chinese alchemy developed independently along two lines: *waidan*, the compounding of
external elixirs, and *neidan*, an inner discipline of breath and meditation. The incendiary
mixture of saltpetre, sulfur and charcoal that became gunpowder is first described in that
literature. Indian *rasashastra* placed mercury at the centre of both metallurgy and
medicine.

## The Arabic tradition

Alchemy was systematised in Arabic during [[The Islamic Golden Age]]. The enormous corpus
attributed to Jabir ibn Hayyan — several thousand titles, treated since Paul Kraus's work in
the 1940s as the collective output of a later school rather than of one man — set out the
sulfur-mercury theory of metals: every metal is a compound of a combustible sulfurous
principle and a fluid, metallic mercurial one, so altering their proportion should convert
one metal into another. The theory made transmutation a reasonable research programme and
gave [[Mercury (element)|mercury]] its central place in the craft. Abu Bakr al-Razi, who died
around 925, wrote in his *Book of Secrets* the first systematic classification of mineral
substances alongside an inventory of furnaces, vessels and procedures, reading much like a
laboratory manual.

## Latin Europe

Latin Europe acquired alchemy by translation, beginning with Robert of Chester's version of
an Arabic treatise in 1144. Within a century and a half European practitioners had something
their Greek and Arabic predecessors lacked: the mineral acids. Nitric acid, and the mixture
with hydrochloric acid called *aqua regia* that dissolves gold, transformed assaying and
separation, while the distillation of wine yielded concentrated alcohol as both solvent and
medicine.[^britannica] The most influential Latin textbook, the *Summa perfectionis* of about
1300, circulated under the name of Geber although it was written in Italy.

Alchemical recipe books were copied alongside artists' handbooks; the bright red vermilion
made by subliming mercury with sulfur came out of this literature, while
[[Ultramarine|ultramarine]] remained a ground mineral that no alchemist could imitate. Rulers
watched the craft closely for the obvious reason: an English statute of 13 January 1404 made
it a felony to multiply gold or silver, for fear of debased coinage, and the prohibition was
not repealed until 1689.[^britannicaact] Paracelsus, who died in 1541, turned alchemy towards
medicine, replacing the four elements with the *tria prima* of salt, sulfur and mercury and
insisting that chemically prepared minerals could be remedies.

## Alchemy and the new science

Alchemy was not the rival of early modern science but part of it. Robert Boyle attacked loose
chemical theorising in *The Sceptical Chymist* of 1661 while pursuing transmutation himself
and lobbying successfully for repeal of the 1404 statute. [[Isaac Newton]] wrote or
transcribed roughly a million words on alchemy, more than he left on optics; the manuscripts
were scattered at a Sotheby's sale in 1936 and are only now being edited in
full.[^newtonproject] Neither man saw a contradiction, because none existed in the categories
of [[The Scientific Revolution|the period]].

## What alchemy left behind

The inheritance is largely material and procedural: the alembic, retort and water bath;
furnace design and controlled heating; sublimation, calcination, crystallisation and
filtration; the mineral acids; and the habit of recording procedures in enough detail to
repeat them. Specific discoveries came out of failed transmutations. Hennig Brand isolated
phosphorus from urine in 1669 while hunting the philosophers' stone, and Johann Friedrich
Böttger, detained to make gold for Augustus the Strong of Saxony, produced European
hard-paste porcelain at Meissen instead.

The theory did not survive. The sulfurous principle persisted into the eighteenth century as
phlogiston until [[Combustion|Lavoisier's account of combustion]] displaced it, and the
elements were re-founded on measurement, first through [[Atomic theory|combining ratios]] and
then through the periodicity of [[The periodic table|the periodic table]]. Transmutation
itself turned out to be real, but nuclear rather than chemical: the spontaneous conversion of
one element into another was first measured in the radioactive substances studied by
[[Marie Curie]] and her contemporaries, and no furnace could have hurried it.
Twentieth-century readings that treated alchemical imagery mainly as psychological symbolism,
those of C. G. Jung above all, have given way to scholarship that reads the texts as
deliberately encoded chemistry, whose cover names can often be resolved into identifiable
substances and repeatable operations.
""",
        "tier": "standard",
        "kind": "discipline",
        "infobox": {
            "title": "Alchemy",
            "subtitle": "Pre-modern science of matter",
            "rows": [
                {"kind": "header", "value": "Overview"},
                {"kind": "row", "label": "Also known as", "value": "Chymistry, before about 1700"},
                {
                    "kind": "row",
                    "label": "Etymology",
                    "value": "Arabic *al-kimiya*, via medieval Latin *alchimia*",
                },
                {"kind": "row", "label": "Period", "value": "1st century CE to 18th century"},
                {
                    "kind": "row",
                    "label": "Main traditions",
                    "value": "Greco-Egyptian, Arabic, Latin European, Chinese, Indian",
                },
                {"kind": "header", "value": "Characteristic aims"},
                {
                    "kind": "row",
                    "label": "Chrysopoeia",
                    "value": "Transmutation of base metals into gold or silver",
                },
                {
                    "kind": "row",
                    "label": "Medicine",
                    "value": "Elixirs and chemically prepared remedies",
                },
                {
                    "kind": "row",
                    "label": "Production",
                    "value": "Acids, salts, pigments, alloys and distilled spirits",
                },
                {"kind": "header", "value": "Legacy"},
                {
                    "kind": "full",
                    "value": (
                        "Bequeathed distillation, sublimation and crystallisation, glass "
                        "apparatus and the mineral acids to chemistry."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a0/The_Alchemist_by_Mattheus_van_Helmont.jpg",
            "alt": "Oil painting of an alchemist at work among flasks, books and a furnace",
            "caption": (
                "*The Alchemist* by Mattheus van Helmont (1623-1679). The workshop combines "
                "furnace, glassware and books, the three staples of alchemical practice."
            ),
            "credit": "Mattheus van Helmont",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:The_Alchemist_by_Mattheus_van_Helmont.jpg",
        },
        "references": [
            {
                "key": "newmanprincipe",
                "title": (
                    "Alchemy vs. Chemistry: The Etymological Origins of a Historiographic Mistake"
                ),
                "url": "https://doi.org/10.1163/157338298X00022",
                "authors": "William R. Newman and Lawrence M. Principe",
                "publisher": "Early Science and Medicine, volume 3, pages 32-65",
                "published_on": "1998",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1163/157338298X00022",
                "quote": (
                    "Argues that the separation of the words alchemy and chemistry was not widely "
                    "accepted until the end of the seventeenth century."
                ),
            },
            {
                "key": "britannica",
                "title": "Alchemy",
                "url": "https://www.britannica.com/topic/alchemy",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannicaact",
                "title": "January 13: Alchemy outlawed by Henry IV of England",
                "url": "https://www.britannica.com/today-in-history/January-13-Alchemy-Outlawed-By-Henry-IV-of-England",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "newtonproject",
                "title": "The Chymistry of Isaac Newton",
                "url": "https://webapp1.dlib.indiana.edu/newton/",
                "authors": "William R. Newman, general editor",
                "publisher": "Indiana University Digital Library Program",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "Newton wrote and transcribed about a million words on the subject of alchemy, "
                    "of which only a tiny fraction has today been published."
                ),
            },
        ],
        "see_also": [
            "The periodic table",
            "Atomic theory",
            "Mercury (element)",
            "Isaac Newton",
            "The Islamic Golden Age",
            "The Scientific Revolution",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["alchemy", "history of chemistry", "chrysopoeia", "distillation", "chymistry"],
    },
    {
        "title": "Mercury (element)",
        "category": "Chemistry and Materials",
        "categories": ["Physics", "Earth and Environment"],
        "short_description": (
            "The only metal liquid at room temperature, kept fluid by relativistic effects"
        ),
        "summary": (
            "Mercury is the element of atomic number 80, the only metal liquid at room "
            "temperature, a fluidity traced to relativistic effects on its electrons. Long used "
            "in mirrors, thermometers and amalgams, it is now restricted worldwide as a toxin."
        ),
        "content": """**Mercury** is the chemical element of atomic number 80 and symbol Hg, the
only metal that is liquid at ordinary temperature and pressure. It sits at the end of the 5d
transition series, in group 12 of [[The periodic table|the periodic table]], and almost every
one of its properties is anomalous for a metal in that position.

## Name and symbol

The symbol comes from *hydrargyrum*, the Latin form of Greek *hydrargyros*, "water-silver",
and the English name from the Roman god and the planet. Ancient and medieval writers assigned
each of the seven known metals to a planet, and mercury, being restless, took the fast-moving
innermost one. The older English word *quicksilver* renders the same idea of living silver.
The planet, the metal and the god are separated at [[Mercury]]; the planet has its own article
at [[Mercury (planet)]].

## Physical properties

Mercury melts at -38.83 °C and boils at 356.6 °C, a liquid range of nearly four hundred
degrees, and its density of 13.534 grams per cubic centimetre at 25 °C means a one-litre
flask holds about 13.5 kilograms of it.[^rsc] Its surface tension is very high, and because it
does not wet glass it beads on a surface and stands in a tube with a meniscus that bulges
upward rather than dipping. Thermal expansion is close to linear across most of the liquid
range, which is why mercury made accurate thermometers, while both its electrical and its
thermal conductivity are poor for a metal: it served in switches and rectifiers because a
liquid conductor makes and breaks contact cleanly, not because it conducts especially well.
The triple point at -38.8344 °C is one of the defining fixed points of
the International Temperature Scale of 1990. Mercury also opened low-temperature physics: in
1911 Heike Kamerlingh Onnes cooled a mercury thread below 4.2 kelvin and found its electrical
resistance vanish, the first observation of superconductivity.

## Why mercury is liquid

The anomalies follow from relativity. Around a nucleus of 80 protons, electrons in s orbitals,
which have appreciable probability density close to the nucleus, reach a substantial fraction
of the speed of light there, and the resulting relativistic mass increase contracts and
stabilises the 6s orbital.[^norrby] Mercury's two 6s electrons are
therefore bound tightly and shared reluctantly, so neighbouring atoms in the solid and the
liquid are held mostly by weak dispersion forces rather than by strong metallic bonding —
closer in this respect to a noble gas than to its neighbours gold and thallium. The
consequences are a melting point lower than that of any other metal, the highest first
ionisation energy of any metal, and feeble thermal conduction. Monte Carlo simulations run
with and without relativistic terms in the interaction between mercury atoms put the size of
the effect at about 105 kelvin: a hypothetical non-relativistic mercury would be solid at room
temperature.[^calvo] The case is a standard demonstration that relativity, usually filed under
[[Special relativity|the physics of high speeds]], reaches into the chemistry of heavy
elements, and it became explicable only once [[Atomic theory|atomic structure]] was described
in terms of electron shells and made quantitative by [[Quantum mechanics|quantum mechanics]].

## Occurrence and extraction

Mercury is rare in the crust and occurs chiefly as the brick-red sulfide cinnabar. Extraction
is unusually simple: roasting the ore in air drives off sulfur dioxide and mercury vapour,
which is condensed to the liquid metal. Two deposits dominated historical supply — Almadén in
central Spain, worked since antiquity, and Idrija in Slovenia, found in 1490 — and the two
were jointly inscribed on the UNESCO World Heritage List in 2012 as the largest mercury mines
in the world.[^unesco] The mine at Huancavelica in Peru, expropriated by the crown in 1572,
supplied mercury for the amalgamation process that separated silver at Potosí; developed in New
Spain in the 1550s and imposed on the Andean refineries in the 1570s, it made mercury a
strategic commodity of the Spanish empire.

## Uses

[[Alchemy|Alchemical]] theory made mercury one of the two principles of all metals and one of
the seven metals answering to the planets; in practice alchemists used it to make vermilion
and to gild. Its readiness to alloy with gold and silver as an amalgam underlies both
precious-metal extraction and fire-gilding. Tin-mercury amalgam spread on glass produced the
first good flat mirrors, a speciality of the glassworks of [[Venice]], until Justus von
Liebig's silvering process of 1835 replaced it. Evangelista Torricelli built the first
barometer with mercury in 1643 and Daniel Fahrenheit the first mercury thermometer in 1714;
the millimetre of mercury survives as a unit of pressure in medicine. Mercury(II) nitrate was
used from the eighteenth century to mat rabbit fur for felt hats, and the tremor, irritability
and mental disturbance it produced in hatters gave English the phrase "mad as a hatter" and
gave Danbury, Connecticut the "Danbury shakes"; American manufacturers abandoned the process
in December 1941. Mercury compounds, calomel above all, were mainstays of medical practice and
the standard treatment for syphilis until arsenical drugs and then [[Penicillin|penicillin]]
displaced them. Twentieth-century uses ran to electrical switches, arc rectifiers, dental
amalgam, mercury-vapour street lamps and fluorescent tubes, most of them since restricted or
replaced.

## Toxicity and regulation

Mercury is toxic in three chemically distinct ways. Elemental mercury is dangerous mainly as
vapour, absorbed through the lungs and damaging to the nervous system; inorganic salts attack
the kidneys and gut; and organic methylmercury crosses the blood-brain barrier and the
placenta and accumulates up aquatic food chains, so that predatory fish carry far higher
concentrations than the water around them. The clearest demonstration came at Minamata in
Japan, where a chemical works discharged methylmercury into the bay; the resulting
neurological disease was identified in 1956 and traced to contaminated fish and shellfish. The
Minamata Convention on Mercury, adopted at Kumamoto on 10 October 2013 and in force since 16
August 2017, restricts primary mining, trade and mercury-added products.[^minamata] The United
Nations Environment Programme's 2018 assessment put anthropogenic emissions to air in 2015 at
about 2,220 tonnes, with artisanal and small-scale gold mining the largest single source at
roughly 38 per cent, ahead of the stationary combustion of coal at about 21 per cent.[^unep]
Mercury thus
belongs with radium, whose hazards went unrecognised in the laboratories of [[Marie Curie]] and
her contemporaries, among the substances whose usefulness was understood long before their
harm.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Mercury",
            "subtitle": "Chemical element, symbol Hg, atomic number 80",
            "rows": [
                {"kind": "header", "value": "Identification"},
                {"kind": "row", "label": "Symbol", "value": "Hg, from Latin *hydrargyrum*"},
                {"kind": "row", "label": "Atomic number", "value": "80"},
                {"kind": "row", "label": "Standard atomic weight", "value": "200.592"},
                {"kind": "row", "label": "Group and period", "value": "Group 12, period 6"},
                {
                    "kind": "row",
                    "label": "Electron configuration",
                    "value": "Xenon core, then 4f14 5d10 6s2",
                },
                {"kind": "header", "value": "Physical properties"},
                {"kind": "row", "label": "Appearance", "value": "Silvery liquid metal"},
                {"kind": "row", "label": "Melting point", "value": "-38.83 °C"},
                {"kind": "row", "label": "Boiling point", "value": "356.6 °C"},
                {
                    "kind": "row",
                    "label": "Density",
                    "value": "13.534 grams per cubic centimetre at 25 °C",
                },
                {"kind": "header", "value": "Occurrence"},
                {
                    "kind": "row",
                    "label": "Principal ore",
                    "value": "Cinnabar, mercury(II) sulfide",
                },
                {
                    "kind": "row",
                    "label": "Historic mines",
                    "value": "Almadén, Spain; Idrija, Slovenia; Huancavelica, Peru",
                },
                {
                    "kind": "full",
                    "value": (
                        "Mercury and its compounds are toxic; the Minamata Convention on Mercury "
                        "has restricted their production and trade since 2017."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/9/99/Pouring_liquid_mercury_bionerd.jpg",
            "alt": "Silvery liquid mercury being poured from a small vessel",
            "caption": (
                "Mercury poured at room temperature. Because it does not wet most surfaces the "
                "metal gathers into beads rather than spreading."
            ),
            "credit": "bionerd, via Wikimedia Commons",
            "license": "CC BY 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:Pouring_liquid_mercury_bionerd.jpg",
        },
        "references": [
            {
                "key": "rsc",
                "title": "Mercury - Element information, properties and uses",
                "url": "https://periodic-table.rsc.org/element/80/mercury",
                "authors": "",
                "publisher": "Royal Society of Chemistry",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "norrby",
                "title": (
                    "Why is mercury liquid? Or, why do relativistic effects not get into "
                    "chemistry textbooks?"
                ),
                "url": "https://doi.org/10.1021/ed068p110",
                "authors": "Lars J. Norrby",
                "publisher": "Journal of Chemical Education, volume 68, page 110",
                "published_on": "1991",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1021/ed068p110",
                "quote": "",
            },
            {
                "key": "calvo",
                "title": "Evidence for Low-Temperature Melting of Mercury owing to Relativity",
                "url": "https://doi.org/10.1002/anie.201302742",
                "authors": "Florent Calvo, Elke Pahl, Michael Wormit and Peter Schwerdtfeger",
                "publisher": "Angewandte Chemie International Edition, volume 52, pages 7583-7585",
                "published_on": "2013",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1002/anie.201302742",
                "quote": (
                    "Simulations show the melting temperature of bulk mercury is lowered by about "
                    "105 kelvin by relativistic effects."
                ),
            },
            {
                "key": "unesco",
                "title": "Heritage of Mercury. Almaden and Idrija",
                "url": "https://whc.unesco.org/en/list/1313/",
                "authors": "",
                "publisher": "UNESCO World Heritage Centre",
                "published_on": "2012",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "minamata",
                "title": "Minamata Convention on Mercury",
                "url": "https://minamataconvention.org/en",
                "authors": "",
                "publisher": "Secretariat of the Minamata Convention on Mercury, UNEP",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "unep",
                "title": "Global Mercury Assessment 2018",
                "url": "https://www.unep.org/resources/publication/global-mercury-assessment-2018",
                "authors": "",
                "publisher": "United Nations Environment Programme",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "The periodic table",
            "Alchemy",
            "Atomic theory",
            "Mercury (planet)",
            "Mercury",
        ],
        "aliases": ["Quicksilver", "Hg"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["mercury", "metals", "relativistic effects", "toxicology", "amalgam"],
    },
    {
        "title": "Marie Curie",
        "category": "Chemistry and Materials",
        "categories": ["Physics", "Medicine and the Mind"],
        "short_description": (
            "Physicist and chemist who discovered polonium and radium and named radioactivity"
        ),
        "summary": (
            "Marie Curie (1867-1934) established radioactivity as a measurable property of atoms, "
            "discovered polonium and radium, and became the first woman to receive a Nobel Prize "
            "and the only person to receive one in two different sciences."
        ),
        "content": """**Marie Curie** (1867-1934) was a Polish-born French physicist and chemist
who established radioactivity as a measurable property of atoms, discovered the elements
polonium and radium, and remains the only person to have received Nobel Prizes in two
different sciences.

## Early life and education

She was born Maria Salomea Skłodowska in Warsaw on 7 November 1867, in the part of partitioned
Poland then ruled by the Russian Empire, the youngest of five children of two teachers.
Russian policy barred women from the university in Warsaw, so she read with the clandestine
"Flying University" and worked as a governess, partly to fund her elder sister's medical
studies in Paris. She followed her sister in 1891, enrolled at the Sorbonne, and took degrees
in physics in 1893 and in mathematics in 1894. In 1895 she married Pierre Curie, a physicist
then working on crystals and magnetism.[^britannica]

## Radioactivity

In 1896 Henri Becquerel found that uranium salts emit radiation able to fog a photographic
plate through opaque wrappings. Curie took the phenomenon as her doctoral subject and made the
decisive methodological choice: instead of photographic plates she measured the minute
electric current the radiation produced by ionising air, using an electrometer paired with a
piezoelectric quartz balance devised by Pierre and his brother Jacques. That turned a
qualitative effect into a number, and two results followed. The activity of a uranium compound
was proportional to the mass of uranium present and independent of the compound's chemical
form or physical state, which implied that the effect belonged to the atom and not to any
molecule; and some minerals, notably the uranium ore pitchblende, were considerably more
active than their uranium content allowed. Curie coined the term *radioactivity* and inferred
that pitchblende held an unknown and far more active substance.[^nobeltheme]

Working with Pierre, she announced polonium in July 1898, named for her occupied homeland, and
radium in December 1898 with the chemist Gustave Bémont; radium was identified from a new line
in the spectrum of a barium fraction before any of it had been isolated. Because radioactivity
meant that atoms of one element were turning into atoms of another, the transmutation that
[[Alchemy|alchemists]] had pursued by chemical means proved to be an ordinary and
uncontrollable fact of nature.

## Isolating radium

Establishing radium as an element meant separating it in quantity from chemically almost
identical barium. Curie processed pitchblende residues from the mines at Joachimsthal in
Bohemia by repeated fractional crystallisation of the chlorides, thousands of operations
carried out with iron vessels and hand stirring in an unheated shed on the rue Lhomond. By
1902, after nearly four years and several tonnes of residue, she had about a tenth of a gram
of radium chloride pure enough to establish radium's atomic weight and to fix its place
beneath barium in [[The periodic table|the periodic table]].[^nobel1911] She defended her
doctoral thesis in 1903. Radium was obtained as a metal in 1910, with André-Louis Debierne.
The Curies published their separation methods in full and took out no patent on them.

## Prizes, chair and institute

The 1903 Nobel Prize in Physics went half to Becquerel for his discovery of spontaneous
radioactivity and half jointly to Pierre and Marie Curie for their research on the radiation
phenomena he had found. She was the first woman to receive a Nobel Prize, and she had not
appeared in the original nomination.[^nobel1903][^nobeltheme] Pierre was killed by a
horse-drawn wagon in a Paris street on 19 April 1906, and the faculty gave her his chair,
making her the first woman to teach at the Sorbonne; she was appointed its first woman titular
professor in 1908. In 1911 she received the Nobel Prize in Chemistry alone, cited for the
discovery of radium and polonium, the isolation of radium, and the study of that element's
nature and compounds.[^nobel1911] Her Nobel lecture set out
radium's chemistry and the new principle that an element could be characterised by its
radiation as well as by its reactions.[^lecture] The Institut du radium, built jointly by the
University of Paris and the Pasteur Institute, opened on the eve of the First World War with
Curie directing its physics and chemistry laboratory; the unit of radioactivity called the
curie was defined from the activity of one gram of radium.

## The First World War

Curie turned the study of radiation into a battlefield service. She equipped about twenty
vehicles as mobile radiological units — an X-ray tube, a generator driven by the car engine
and a darkroom, known to soldiers as *petites Curies* — and helped install some two hundred
fixed radiological rooms in military hospitals, so that surgeons could locate shrapnel and
fractures against the structures described by [[Human anatomy|anatomy]] before cutting. A
total of 150 women, her daughter Irène among them, were trained by her to operate the
equipment, and the number of wounded men given X-ray examinations during the war is estimated
to have exceeded a million.[^jorgensen] She also collected radon given off by her radium stock
and sealed it in glass needles for use in treatment.

## Radiation injury and death

Nobody working with radium in its first two decades used shielding, and Curie handled
concentrated preparations for more than thirty years. She developed cataracts and damaged
fingertips, and her health declined through the 1920s, by which time the danger of prolonged
exposure was becoming plain from the illnesses of radium dial painters. She died on 4 July 1934
at a sanatorium at Passy in Haute-Savoie, of aplastic anaemia attributed to long exposure to
radiation.[^britannica] Her laboratory notebooks remain contaminated with radium-226, whose
half-life is about 1,600 years, and are kept in lead-lined boxes at the Bibliothèque nationale
de France. Radium belongs with [[Mercury (element)|mercury]] and lead among industrially useful
substances whose harm was recognised only after decades of use.

## Legacy

Radioactivity remade the picture of matter: the atom was no longer indivisible or unchanging,
and the emissions the Curies measured became the probe with which Ernest Rutherford and others
opened up [[Atomic theory|atomic structure]], a problem only [[Quantum mechanics]] would
finally describe. Radium's continuous output of energy, which no account of
[[Light|radiation]] then available could explain, was among the anomalies that forced the
change. Her daughter Irène Joliot-Curie shared the 1935 Nobel Prize in Chemistry for the
artificial production of radioactive elements. Element 96, curium, is named for Pierre and
Marie Curie, and in 1995 their remains were moved to the Panthéon in Paris, where she became
the first woman interred for her own achievements.
""",
        "tier": "standard",
        "kind": "person",
        "infobox": {
            "title": "Marie Curie",
            "subtitle": "Physicist and chemist, 1867-1934",
            "rows": [
                {"kind": "header", "value": "Life"},
                {
                    "kind": "row",
                    "label": "Born",
                    "value": "Maria Salomea Skłodowska, 7 November 1867, Warsaw, Russian Empire",
                },
                {
                    "kind": "row",
                    "label": "Died",
                    "value": "4 July 1934, Passy, Haute-Savoie, France",
                },
                {"kind": "row", "label": "Nationality", "value": "Polish and French"},
                {"kind": "row", "label": "Fields", "value": "Physics, chemistry, radioactivity"},
                {
                    "kind": "row",
                    "label": "Institutions",
                    "value": "University of Paris; Institut du radium",
                },
                {"kind": "header", "value": "Work and honours"},
                {
                    "kind": "row",
                    "label": "Known for",
                    "value": "Coining *radioactivity*; polonium and radium; isolating radium",
                },
                {
                    "kind": "row",
                    "label": "Nobel Prize in Physics",
                    "value": "1903, with Pierre Curie and Henri Becquerel",
                },
                {"kind": "row", "label": "Nobel Prize in Chemistry", "value": "1911"},
                {
                    "kind": "full",
                    "value": (
                        "The first woman to receive a Nobel Prize and the only person to have "
                        "received one in two different sciences."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Marie_Curie_c._1920s.jpg",
            "alt": "Studio photograph of Marie Curie, seated and facing slightly to her left",
            "caption": (
                "Marie Curie photographed by Henri Manuel in the 1920s, while she directed the "
                "laboratory at the Institut du radium in Paris."
            ),
            "credit": "Henri Manuel",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Marie_Curie_c._1920s.jpg",
        },
        "references": [
            {
                "key": "nobel1903",
                "title": "Marie Curie - Facts, The Nobel Prize in Physics 1903",
                "url": "https://www.nobelprize.org/prizes/physics/1903/marie-curie/facts/",
                "authors": "",
                "publisher": "Nobel Prize Outreach",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nobel1911",
                "title": "Marie Curie - Facts, The Nobel Prize in Chemistry 1911",
                "url": "https://www.nobelprize.org/prizes/chemistry/1911/marie-curie/facts/",
                "authors": "",
                "publisher": "Nobel Prize Outreach",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "In recognition of her services to the advancement of chemistry by the "
                    "discovery of the elements radium and polonium, by the isolation of radium "
                    "and the study of the nature and compounds of this remarkable element."
                ),
            },
            {
                "key": "nobeltheme",
                "title": "Marie and Pierre Curie and the discovery of polonium and radium",
                "url": "https://www.nobelprize.org/prizes/themes/marie-and-pierre-curie-and-the-discovery-of-polonium-and-radium/",
                "authors": "",
                "publisher": "Nobel Prize Outreach",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "lecture",
                "title": "Radium and the New Concepts in Chemistry, Nobel Lecture",
                "url": "https://www.nobelprize.org/prizes/chemistry/1911/marie-curie/lecture/",
                "authors": "Marie Curie",
                "publisher": "Nobel Prize Outreach",
                "published_on": "11 December 1911",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica",
                "title": "Marie Curie",
                "url": "https://www.britannica.com/biography/Marie-Curie",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "jorgensen",
                "title": "How Marie Curie Brought X-Ray Machines to the Battlefield",
                "url": "https://www.smithsonianmag.com/history/how-marie-curie-brought-x-ray-machines-to-battlefield-180965240/",
                "authors": "Timothy J. Jorgensen",
                "publisher": "Smithsonian Magazine",
                "published_on": "11 October 2017",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "In the end, a total of 150 women received X-ray training from Curie.",
            },
        ],
        "see_also": [
            "The periodic table",
            "Atomic theory",
            "Quantum mechanics",
            "Light",
            "Human anatomy",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["radioactivity", "radium", "polonium", "nobel prize", "history of physics"],
    },
]
