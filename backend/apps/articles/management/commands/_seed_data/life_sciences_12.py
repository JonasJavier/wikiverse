"""Life Sciences — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Photosynthesis",
        "category": "Life Sciences",
        "categories": ["Chemistry and Materials", "Earth and Environment"],
        "short_description": "How plants, algae and some bacteria turn light into chemical energy",
        "summary": (
            "Photosynthesis uses light energy to build carbohydrate from carbon dioxide and "
            "water. The oxygen-producing form supplies nearly all the chemical energy in the "
            "biosphere and all the free oxygen in the atmosphere."
        ),
        "content": """**Photosynthesis** is the process by which plants, algae and some bacteria use light
energy to build carbohydrate from carbon dioxide and water. In its oxygen-producing form it
supplies both the chemical energy that sustains almost every food web and the free oxygen of
the atmosphere, and it moves more carbon between the air and living matter than any other
biological process.

## The overall reaction

For the oxygenic photosynthesis carried out by land plants, algae and cyanobacteria, the net
chemistry is conventionally summarised as

```
6 CO2 + 6 H2O + light energy -> C6H12O6 + 6 O2
```

The summary equation hides two important things. First, this is not one reaction but two
coupled sets of them. The light reactions occur in the thylakoid membranes inside the
chloroplast, an organelle of the plant [[The cell|cell]], and convert light energy into two
portable chemical forms: adenosine triphosphate (ATP) and the reducing agent NADPH. The
carbon-fixing reactions occur in the surrounding stroma and spend ATP and NADPH to reduce
carbon dioxide to sugar. Only the first set needs light directly.

Second, the oxygen released does not come from carbon dioxide. Samuel Ruben and Martin Kamen
established in 1941, using water enriched in the heavy isotope oxygen-18, that the evolved
oxygen carries the isotopic label of the water rather than of the carbon dioxide.[^rubenkamen]
Oxygenic photosynthesis is water-splitting chemistry with carbon fixation attached to it.

Nor is the oxygenic version the only one. Purple and green sulfur bacteria run anoxygenic
photosynthesis in which hydrogen sulfide, thiosulfate or dissolved iron replaces
[[Water|water]] as the electron donor; they deposit granules of sulfur instead of releasing
oxygen. Cornelis van Niel used exactly that comparison in the 1930s to argue that
photosynthesis is fundamentally the light-driven transfer of electrons from some donor to
carbon dioxide, and that in plants the donor must be water — a prediction the isotope work
later confirmed.

## Pigments and light capture

Absorption is the work of pigments held in protein complexes. Chlorophyll was isolated from
leaves and named in 1817 by Pierre Joseph Pelletier and Joseph Bienaimé Caventou; the several
forms it takes were distinguished later. Its commonest form, chlorophyll a, absorbs strongly in
the blue near 430 nm and in the red near 660 to 680 nm, and weakly in between; the green
[[Light|light]] it neither absorbs nor uses is what reaches the eye, which is why most foliage
looks green. Chlorophyll b and the carotenoids widen the usable spectrum and also dissipate
excess absorbed energy as heat, which protects the apparatus in bright sun.

Most pigment molecules do no chemistry at all. Several hundred of them form an antenna that
passes excitation energy inward by resonance transfer, on a timescale of picoseconds, until it
reaches a special pair of chlorophylls in a reaction centre. There the excitation is used to
push an electron onto an acceptor, and the energy of the photon becomes the energy of a
separated charge, later stored in the [[Chemical bond|chemical bonds]] of sugar.

## The light reactions

Two reaction centres act in series, an arrangement Robert Hill and Fay Bendall proposed in
1960 and universally drawn as the Z-scheme. Photosystem II, named for the order of its
discovery rather than its place in the chain, absorbs at about 680 nm. Its oxidised reaction
centre is a powerful enough oxidant to take electrons from water at a cluster of four
manganese atoms, one calcium and five oxygens; a crystal structure at 1.9 ångström resolution,
published in 2011, resolved the geometry of that cluster and the water molecules around
it.[^umena] Splitting two water molecules releases one molecule of oxygen and four protons
into the thylakoid lumen.

The electrons travel through plastoquinone, the cytochrome b6f complex and plastocyanin to
photosystem I, which absorbs at about 700 nm, re-energises them, and passes them via
ferredoxin to an enzyme that makes NADPH. Meanwhile the electron flow pumps additional protons
into the lumen. The resulting pH difference and electric potential drive ATP synthase, which
manufactures ATP as protons flow back out. Roughly eight to ten photons are needed per
molecule of oxygen released.

## Carbon fixation

The reduction of carbon dioxide runs through the Calvin–Benson cycle, worked out at Berkeley
in the late 1940s and 1950s by Melvin Calvin, Andrew Benson and James Bassham, who fed
radioactive carbon-14 dioxide to algae, killed the cells at intervals of seconds, and
separated the labelled products by two-dimensional paper chromatography. Calvin received the
Nobel Prize in Chemistry in 1961.

The cycle has three phases. Carbon dioxide is attached to the five-carbon sugar
ribulose-1,5-bisphosphate, producing two molecules of 3-phosphoglycerate; these are reduced
using ATP and NADPH; and most of the product is rearranged to regenerate the starting sugar,
so that the cycle can continue. Fixing one carbon dioxide costs three ATP and two NADPH. What
leaves the cycle is triose phosphate, exported to make sucrose for transport or retained as
starch.

The carboxylating enzyme, ribulose-1,5-bisphosphate carboxylase/oxygenase or RuBisCO, is
remarkable for being both indispensable and inefficient. Each active site fixes only a few
molecules of carbon dioxide per second, thousands of times slower than many enzymes, so plants
compensate with quantity: RuBisCO commonly makes up a quarter or more of the soluble protein
in a leaf, and is plausibly the most abundant protein on Earth.

## Photorespiration and the C4 and CAM variants

RuBisCO cannot reliably tell carbon dioxide from oxygen. When it attaches oxygen instead, the
product is 2-phosphoglycolate, a dead end that must be salvaged through a pathway spanning
three compartments, consuming ATP and releasing carbon dioxide that the plant had already
fixed. This photorespiration becomes proportionally worse as temperature rises, because the
solubility of carbon dioxide in water falls faster than that of oxygen, and worse again when
heat or drought forces the stomata shut and internal carbon dioxide is drawn down.

Two independent solutions evolved, both of them concentrating carbon dioxide around RuBisCO
rather than improving the enzyme. In C4 photosynthesis, described in sugarcane by Marshall
Hatch and Roger Slack in 1966, an outer layer of mesophyll cells fixes carbon dioxide with the
fast and oxygen-insensitive enzyme PEP carboxylase into a four-carbon acid.[^hatchslack] That
acid is shuttled into interior bundle-sheath cells and decarboxylated there, flooding RuBisCO
with carbon dioxide. The pathway requires extra ATP and a modified leaf anatomy, and pays off
in hot, bright and dry conditions; it has evolved independently in more than sixty plant
lineages and includes maize, sugarcane and sorghum among the world's largest crops.

Crassulacean acid metabolism, or CAM, separates the same two steps in time rather than space.
Stomata open at night, when evaporative loss is lowest, and carbon dioxide is fixed into malic
acid and stored in vacuoles; by day the stomata close and the acid is broken down to feed the
Calvin cycle behind sealed pores. Cacti, agaves, many orchids and pineapple use it, and the
water saving is large enough to make CAM the standard strategy of succulents.

## Origins and the oxygenation of the atmosphere

Oxygenic photosynthesis evolved in the ancestors of cyanobacteria. Its consequences appear in
the rock record as the Great Oxidation Event, beginning about 2.4 billion years ago, when
atmospheric oxygen rose from negligible levels — a shift recorded in the disappearance of
certain sulfur isotope signatures and in the fate of iron and other redox-sensitive elements
in marine sediments.[^lyons] Free oxygen was initially a poison to the anaerobic biosphere and
is the reason the aerobic respiration that most life now depends on became possible at all.

Chloroplasts are descended from a cyanobacterium engulfed by a eukaryotic host and retained,
an interpretation proposed by Konstantin Mereschkowsky in 1905 and revived with evidence by
Lynn Margulis in the 1960s. Chloroplasts still carry their own circular genome of roughly a
hundred genes and divide by fission. Several algal lineages acquired plastids a second time by
swallowing another alga; among them are the dinoflagellates that live inside reef-building
corals, whose expulsion under heat stress is what bleaching of a [[Coral reef|coral reef]]
physically consists of.

## Global scale and efficiency

Satellite measurements of land greenness and ocean colour, combined with models, put global
net primary production — the carbon fixed by photosynthesis after the organisms' own
respiration — at roughly 105 billion tonnes of carbon a year, divided almost evenly between
land and sea.[^field] On land the largest single contribution comes from tropical forest,
including [[The Amazon rainforest]]; at sea it comes from microscopic plankton, among them the
picocyanobacterium *Prochlorococcus*, described only in 1988 and now counted among the most
abundant photosynthetic organisms on the planet. This flux is the fast, biological arm of
[[The carbon cycle]].

Considered as an energy converter, photosynthesis is not efficient. Accounting for the
unusable parts of the spectrum, reflection, the quantum requirement and respiration, the
theoretical ceiling for conversion of total incident solar energy into biomass is about 4.6
per cent for C3 plants and 6 per cent for C4 plants, and real field crops over a season
typically achieve about a third of that or less.[^zhu] The gap between the two figures is the
target of efforts to raise crop yields by engineering the pathway, including attempts to
install C4 traits or improved carbon-concentrating machinery in C3 species such as rice.

## Investigating the process

The stepwise unpicking of photosynthesis is one of the better-documented cases of a mechanism
being established by measurement. Jan Baptist van Helmont, working in the early seventeenth
century, reported growing a willow from about five pounds to some 169 pounds over five years
in 200 pounds of soil that lost only around two ounces, and concluded — half rightly — that
the substance of the plant came from water. Joseph Priestley showed in 1771 and 1772 that a
plant could restore air in which a candle had burnt out. Jan Ingenhousz demonstrated in 1779
that the restorative effect required sunlight and came from the green parts of the
plant.[^ingenhousz] Jean Senebier identified carbon dioxide as the carbon source, and
Nicolas-Théodore de Saussure showed by weighing that water is incorporated too. Julius von
Sachs established in 1862 that starch grains accumulate in chloroplasts in the
light.[^britannica] Robert Hill separated the two halves of the process in 1937 by showing that
chloroplasts isolated from leaves evolve oxygen in the light when supplied with an artificial
electron acceptor and no carbon dioxide at all.[^hill1937]
Each of those results narrowed the question the next generation had to answer, and the
selective advantage of the resulting machinery is itself a standard illustration of
[[Natural selection]] acting on biochemistry.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Photosynthesis",
            "subtitle": "Light-driven carbon fixation",
            "rows": [
                {"kind": "header", "value": "Overview"},
                {"kind": "row", "label": "Type", "value": "Biochemical process"},
                {"kind": "row", "label": "Inputs", "value": "Carbon dioxide, water, light"},
                {
                    "kind": "row",
                    "label": "Outputs",
                    "value": "Carbohydrate; oxygen in the oxygenic form",
                },
                {
                    "kind": "row",
                    "label": "Site",
                    "value": "Chloroplast thylakoids and stroma; cyanobacterial membranes",
                },
                {"kind": "header", "value": "Key components"},
                {
                    "kind": "row",
                    "label": "Pigments",
                    "value": "Chlorophyll a and b, carotenoids",
                },
                {
                    "kind": "row",
                    "label": "Reaction centres",
                    "value": "Photosystem II (P680) and photosystem I (P700)",
                },
                {"kind": "row", "label": "Carboxylating enzyme", "value": "RuBisCO"},
                {
                    "kind": "row",
                    "label": "Cost per carbon fixed",
                    "value": "3 ATP and 2 NADPH",
                },
                {"kind": "header", "value": "Scale"},
                {
                    "kind": "row",
                    "label": "Global net primary production",
                    "value": "About 105 billion tonnes of carbon per year",
                },
                {
                    "kind": "row",
                    "label": "Theoretical efficiency ceiling",
                    "value": "About 4.6 per cent (C3) and 6 per cent (C4) of incident sunlight",
                },
                {
                    "kind": "full",
                    "value": "The oxygen released originates from water, not carbon dioxide",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "rubenkamen",
                "title": "Heavy Oxygen (O18) as a Tracer in the Study of Photosynthesis",
                "url": "https://doi.org/10.1021/ja01848a512",
                "authors": "Samuel Ruben, Merle Randall, Martin Kamen, James L. Hyde",
                "publisher": "Journal of the American Chemical Society, vol. 63, pp. 877–879",
                "published_on": "1941",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1021/ja01848a512",
                "quote": "",
            },
            {
                "key": "umena",
                "title": "Crystal structure of oxygen-evolving photosystem II at 1.9 Å",
                "url": "https://doi.org/10.1038/nature09913",
                "authors": "Yasufumi Umena, Keisuke Kawakami, Jian-Ren Shen, Nobuo Kamiya",
                "publisher": "Nature, vol. 473, pp. 55–60",
                "published_on": "2011",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature09913",
                "quote": "",
            },
            {
                "key": "hatchslack",
                "title": (
                    "Photosynthesis by sugar-cane leaves: a new carboxylation reaction and "
                    "the pathway of sugar formation"
                ),
                "url": "https://doi.org/10.1042/bj1010103",
                "authors": "Marshall D. Hatch, C. Roger Slack",
                "publisher": "Biochemical Journal, vol. 101, pp. 103–111",
                "published_on": "1966",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1042/bj1010103",
                "quote": "",
            },
            {
                "key": "lyons",
                "title": "The rise of oxygen in Earth's early ocean and atmosphere",
                "url": "https://doi.org/10.1038/nature13068",
                "authors": "Timothy W. Lyons, Christopher T. Reinhard, Noah J. Planavsky",
                "publisher": "Nature, vol. 506, pp. 307–315",
                "published_on": "2014",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature13068",
                "quote": "",
            },
            {
                "key": "field",
                "title": (
                    "Primary Production of the Biosphere: Integrating Terrestrial and "
                    "Oceanic Components"
                ),
                "url": "https://doi.org/10.1126/science.281.5374.237",
                "authors": (
                    "Christopher B. Field, Michael J. Behrenfeld, James T. Randerson, "
                    "Paul Falkowski"
                ),
                "publisher": "Science, vol. 281, pp. 237–240",
                "published_on": "1998",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.281.5374.237",
                "quote": "",
            },
            {
                "key": "zhu",
                "title": "Improving photosynthetic efficiency for greater yield",
                "url": "https://doi.org/10.1146/annurev-arplant-042809-112206",
                "authors": "Xin-Guang Zhu, Stephen P. Long, Donald R. Ort",
                "publisher": "Annual Review of Plant Biology, vol. 61, pp. 235–261",
                "published_on": "2010",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1146/annurev-arplant-042809-112206",
                "quote": "",
            },
            {
                "key": "ingenhousz",
                "title": (
                    "Experiments upon Vegetables, Discovering Their Great Power of Purifying "
                    "the Common Air in the Sun-shine"
                ),
                "url": "",
                "authors": "Jan Ingenhousz",
                "publisher": "P. Elmsly and H. Payne, London",
                "published_on": "1779",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "hill1937",
                "title": "Oxygen Evolved by Isolated Chloroplasts",
                "url": "https://doi.org/10.1038/139881a0",
                "authors": "Robert Hill",
                "publisher": "Nature, vol. 139, pp. 881–882",
                "published_on": "1937",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/139881a0",
                "quote": "",
            },
            {
                "key": "britannica",
                "title": "Photosynthesis",
                "url": "https://www.britannica.com/science/photosynthesis",
                "authors": "",
                "publisher": "Encyclopædia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "The cell",
            "The carbon cycle",
            "Light",
            "Water",
            "The Amazon rainforest",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "photosynthesis",
            "chloroplast",
            "carbon fixation",
            "chlorophyll",
            "plant physiology",
        ],
    },
    {
        "title": "Natural selection",
        "category": "Life Sciences",
        "categories": ["Earth and Environment", "Medicine and the Mind"],
        "short_description": "Differential survival and reproduction of heritable variants",
        "summary": (
            "Natural selection is the process by which heritable traits that improve survival "
            "or reproduction become more common over generations. It is the principal "
            "explanation for adaptation in living things."
        ),
        "content": """**Natural selection** is the process by which heritable differences between
individuals lead to differences in survival or reproduction, so that the more successful
variants become more common in later generations. Reached independently by
[[Charles Darwin]] and Alfred Russel Wallace, announced jointly in 1858 and set out at length
in Darwin's *On the Origin of Species* the following year, it remains the only well-supported
mechanism that
explains why organisms appear designed for the conditions they live in.[^darwin1859]

## The argument

The reasoning requires no specialised vocabulary and rests on three conditions that are
matters of observation rather than theory.

1. **Variation.** Individuals in a population differ from one another in size, colour,
   chemistry, timing and behaviour.
2. **Heredity.** Some of that variation is passed from parent to offspring.
3. **Differential success.** More offspring are produced than can survive and reproduce, and
   which ones do so is not independent of the traits they carry.

If all three hold, the frequency of the favoured variants must rise. Nothing is added to the
argument by intention or striving; the outcome follows from unequal reproduction among
differing heritable types. Darwin arrived at the third condition partly through Thomas
Malthus's *Essay on the Principle of Population*, which he read in 1838 and which supplied the
arithmetic of populations outgrowing their resources.

Because success is measured statistically rather than individually, natural selection is a
probabilistic process and is described with the tools of [[Probability theory]]. Fitness is
defined as an expected number of descendants, not a guaranteed one: a favoured variant may
still be lost by chance, particularly in a small population.

## Variation, heredity and the modern synthesis

Darwin had no correct account of inheritance. His own proposal, pangenesis, supposed that
particles shed by the body's tissues collected in the reproductive organs, and it was wrong.
Gregor Mendel's experiments on peas, published in 1866 and largely unread until 1900,
supplied the missing piece by showing that heredity is particulate: traits are carried by
discrete factors that are not blended away.

Reconciling Mendelian genetics with Darwinian selection took the first four decades of the
twentieth century and produced the population genetics of Ronald Fisher, J. B. S. Haldane and
Sewall Wright, and then the broader modern synthesis associated with Theodosius Dobzhansky,
Ernst Mayr and George Gaylord Simpson.[^mayr] Selection was recast as change in the frequency
of alleles, quantified with a selection coefficient, and the mutation rate became a measurable
parameter rather than an assumption. The identification of
[[Deoxyribonucleic acid|DNA]] as the hereditary molecule gave the process a physical substrate
and, later, a way of detecting selection directly in sequence data by comparing the rates of
change at sites where substitutions alter a protein and sites where they do not.

## Modes of selection

Selection is classified by its effect on the distribution of a trait. **Directional**
selection shifts the mean, as when a predator removes the slowest individuals. **Stabilising**
selection removes both extremes and narrows the distribution; human birth weight, penalised at
both tails, is a standard example. **Disruptive** selection favours both extremes over
intermediates and can begin to split a population.

**Sexual selection**, which Darwin treated at length in 1871, acts through competition for
mates and mate choice rather than survival, and explains traits that are costly in every other
respect, such as the peacock's train. **Kin selection**, formalised by W. D. Hamilton in 1964,
accounts for behaviour that reduces an individual's own reproduction while raising that of
close relatives; it resolves what Darwin himself called a special difficulty, the existence of
sterile worker castes in social insects such as the [[Honey bee]].

## Evidence

Natural selection is unusual among historical explanations in being observable in progress.

- **Field measurement.** Peter and Rosemary Grant monitored ground finches on the small
  Galápagos island of Daphne Major from 1973. A severe drought in 1977 destroyed the supply of
  small seeds and killed most of the medium ground finch population; survivors had on average
  deeper, stronger bills able to crack the large hard seeds that remained, and their offspring
  inherited the difference. Later wet years reversed the trend.[^grants]
- **Industrial melanism.** A dark form of the peppered moth, first recorded near Manchester in
  1848, rose to dominate populations in sooty industrial districts and declined again after
  air-quality legislation. A controlled predation experiment published in 2012 confirmed that
  birds do take the more conspicuous form more often, the mechanism the classic account had
  assumed.[^cook2012]
- **Antibiotic resistance.** Resistance to [[Penicillin]] appeared in *Staphylococcus aureus*
  within a few years of the drug's introduction, and methicillin-resistant strains were
  reported in 1961. Resistance is selection watched in real time on a human timescale, with the
  selective agent supplied deliberately.
- **Experimental evolution.** Twelve populations of *Escherichia coli* founded from a single
  ancestor in 1988 have been propagated daily ever since. One population acquired the ability
  to use citrate as a carbon source after roughly 31,500 generations, and replaying the
  experiment from frozen samples showed that the innovation depended on earlier mutations that
  were not themselves advantageous for citrate use.[^lenski]
- **Islands and biogeography.** [[The Galápagos Islands]], Hawaii and the Caribbean anoles
  show repeated patterns in which a few colonising lineages diversify to fill available roles,
  producing local species found nowhere else and resemblances between unrelated islands.
- **Convergence.** The camera eye of the [[Octopus]] and that of vertebrates evolved
  separately from different tissues and arrive at similar optics, which is what a process that
  repeatedly finds workable solutions to the same physical problem would produce.
- **Mutualism.** Arrangements that benefit both partners — the algae inside reef-building
  corals on a [[Coral reef]], the pollination mechanisms Darwin dissected in orchids — are the
  product of selection acting simultaneously on two lineages.

## What natural selection does not claim

Several misreadings are persistent enough to be worth stating plainly.[^berkeley][^sep]

Selection is not random. Mutation, the source of new variation, is undirected with respect to
what would be useful, but the filtering of that variation by survival and reproduction is
systematically biased, which is precisely why it can accumulate complex adaptation.

"Survival of the fittest" is a phrase Herbert Spencer coined in 1864 and Darwin adopted only in
the fifth edition of the *Origin*. It invites two errors: that fitness means physical strength,
when it means expected reproductive success in a particular environment; and that the statement
is an empty tautology, when it is a testable claim about which measurable traits correlate with
reproductive success in which conditions.

Selection has no goal and does not produce progress toward complexity. Parasites with reduced
bodies and cave animals that have lost their eyes are as much products of selection as
vertebrate eyes are. Nor does selection anticipate: it can act only on variation already
present, which is why adaptations are often improvisations on inherited material rather than
optimal designs.

Individuals do not evolve; populations do. An organism's traits are fixed at conception in
their heritable component, and it is the composition of the population that changes.

Not every trait is an adaptation. Genetic drift — random change in allele frequencies,
strongest in small populations — can fix neutral or even mildly harmful variants, and the
neutral theory advanced by Motoo Kimura in 1968 holds that much molecular change is of this
kind. Developmental constraint, gene flow between populations and historical accident all leave
marks that no selective story explains. A 1979 critique by Stephen Jay Gould and Richard
Lewontin argued that evolutionary biology too readily assumed an adaptive purpose for every
feature.

Finally, selection offers no guarantee of survival. Environments change faster than populations
can track, and most species that have existed are extinct; the causes and patterns of
[[Extinction]] are studied as a separate question.

## Reception and misapplication

The joint Darwin–Wallace papers were read to the Linnean Society of London on 1 July 1858 and
attracted little notice.[^darwinwallace1858] The *Origin* the following year did, and the
argument about common descent was substantially settled within scientific circles during
Darwin's lifetime, while the sufficiency of selection as a mechanism remained contested until
the population genetics of the 1920s and 1930s.

From the late nineteenth century onward, various social and political programmes invoked
selection as a warrant, including eugenic policies pursued in several countries in the first
half of the twentieth century. These arguments move from a description of how populations
change to a prescription about how societies should act, an inference that does not follow: a
biological account of what happens carries no implication about what ought to be done.
Historians treat such movements as part of the history of politics rather than of evolutionary
biology.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Natural selection",
            "subtitle": "Mechanism of adaptive evolution",
            "rows": [
                {"kind": "header", "value": "Overview"},
                {"kind": "row", "label": "Field", "value": "Evolutionary biology"},
                {
                    "kind": "row",
                    "label": "Proposed by",
                    "value": "Charles Darwin and Alfred Russel Wallace",
                },
                {
                    "kind": "row",
                    "label": "First announced",
                    "value": "Linnean Society of London, 1 July 1858",
                },
                {
                    "kind": "row",
                    "label": "Full statement",
                    "value": "*On the Origin of Species* (1859)",
                },
                {"kind": "header", "value": "Conditions"},
                {
                    "kind": "full",
                    "value": (
                        "Variation among individuals; heredity of that variation; differences "
                        "in survival or reproduction associated with it"
                    ),
                },
                {"kind": "header", "value": "Modes"},
                {"kind": "row", "label": "Directional", "value": "Shifts the trait mean"},
                {
                    "kind": "row",
                    "label": "Stabilising",
                    "value": "Narrows variation around the mean",
                },
                {
                    "kind": "row",
                    "label": "Disruptive",
                    "value": "Favours extremes over intermediates",
                },
                {
                    "kind": "row",
                    "label": "Sexual",
                    "value": "Acts through mate choice and competition for mates",
                },
                {"kind": "header", "value": "Other evolutionary processes"},
                {
                    "kind": "row",
                    "label": "Genetic drift",
                    "value": "Random change in allele frequency, strongest in small populations",
                },
                {
                    "kind": "row",
                    "label": "Mutation",
                    "value": "Source of new variation; undirected",
                },
                {
                    "kind": "row",
                    "label": "Gene flow",
                    "value": "Movement of alleles between populations",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "darwin1859",
                "title": "On the Origin of Species by Means of Natural Selection",
                "url": "http://darwin-online.org.uk/",
                "authors": "Charles Darwin",
                "publisher": "John Murray, London (first edition)",
                "published_on": "1859",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "darwinwallace1858",
                "title": (
                    "On the Tendency of Species to form Varieties; and on the Perpetuation "
                    "of Varieties and Species by Natural Means of Selection"
                ),
                "url": "http://darwin-online.org.uk/",
                "authors": "Charles Darwin, Alfred Russel Wallace",
                "publisher": (
                    "Journal of the Proceedings of the Linnean Society of London, Zoology, "
                    "vol. 3, pp. 45–62"
                ),
                "published_on": "1858",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1111/j.1096-3642.1858.tb02500.x",
                "quote": "",
            },
            {
                "key": "grants",
                "title": "40 Years of Evolution: Darwin's Finches on Daphne Major Island",
                "url": "",
                "authors": "Peter R. Grant, B. Rosemary Grant",
                "publisher": "Princeton University Press",
                "published_on": "2014",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-691-16046-7",
                "quote": "",
            },
            {
                "key": "cook2012",
                "title": (
                    "Selective bird predation on the peppered moth: the last experiment of "
                    "Michael Majerus"
                ),
                "url": "https://doi.org/10.1098/rsbl.2011.1136",
                "authors": "L. M. Cook, B. S. Grant, I. J. Saccheri, J. Mallet",
                "publisher": "Biology Letters, vol. 8, pp. 609–612",
                "published_on": "2012",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rsbl.2011.1136",
                "quote": "",
            },
            {
                "key": "lenski",
                "title": (
                    "Historical contingency and the evolution of a key innovation in an "
                    "experimental population of Escherichia coli"
                ),
                "url": "https://doi.org/10.1073/pnas.0803151105",
                "authors": "Zachary D. Blount, Christina Z. Borland, Richard E. Lenski",
                "publisher": (
                    "Proceedings of the National Academy of Sciences, vol. 105, pp. 7899–7906"
                ),
                "published_on": "2008",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1073/pnas.0803151105",
                "quote": "",
            },
            {
                "key": "mayr",
                "title": (
                    "One Long Argument: Charles Darwin and the Genesis of Modern "
                    "Evolutionary Thought"
                ),
                "url": "",
                "authors": "Ernst Mayr",
                "publisher": "Harvard University Press",
                "published_on": "1991",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sep",
                "title": "Natural Selection",
                "url": "https://plato.stanford.edu/entries/natural-selection/",
                "authors": "Peter Gildenhuys",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2019, substantive revision 2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "berkeley",
                "title": "Understanding Evolution",
                "url": "https://evolution.berkeley.edu/",
                "authors": "",
                "publisher": "University of California Museum of Paleontology",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Charles Darwin",
            "Deoxyribonucleic acid",
            "The Galápagos Islands",
            "Extinction",
            "Penicillin",
        ],
        "aliases": ["Evolution", "Survival of the fittest"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "evolution",
            "natural selection",
            "adaptation",
            "population genetics",
            "heredity",
        ],
    },
    {
        "title": "Charles Darwin",
        "category": "Life Sciences",
        "categories": ["History", "Earth and Environment"],
        "short_description": "English naturalist who established evolution by natural selection",
        "summary": (
            "Charles Darwin (1809–1882) was an English naturalist and geologist whose voyage "
            "on HMS Beagle and two decades of subsequent work produced the theory of "
            "evolution by natural selection."
        ),
        "content": """**Charles Darwin** (12 February 1809 – 19 April 1882) was an English naturalist
and geologist who established that living species descend from common ancestors and proposed
[[Natural selection]] as the mechanism by which they change. His nearly five years aboard HMS
*Beagle* supplied the observations; two further decades of patient collecting, breeding,
dissection and
correspondence supplied the case; and *On the Origin of Species*, published in 1859, presented
it.

## Early life and training

Darwin was born in Shrewsbury, the fifth of six children of Robert Darwin, a prosperous
physician, and Susannah Wedgwood, daughter of the potter Josiah Wedgwood. His mother died when
he was eight. His grandfather Erasmus Darwin had written verse and speculation about the
transmutation of species, so the idea was not unfamiliar in the household.

Sent to Edinburgh in 1825 to study medicine, Darwin found the lectures dull and the surgery
unbearable, but learned marine invertebrate dissection from Robert Grant. His father then
redirected him to Christ's College, Cambridge, for an ordinary degree that might lead to a
country parsonage. There the botanist John Stevens Henslow and the geologist Adam Sedgwick
became his real teachers; a fortnight of fieldwork in north Wales with Sedgwick in 1831 gave
him the practical geology he used for the rest of his life. He was also an obsessive beetle
collector, which trained the eye for small differences that his later work depended on.

## The voyage of the Beagle

On Henslow's recommendation, Darwin was invited to sail as a gentleman naturalist and
companion to Captain Robert FitzRoy on HMS *Beagle*, whose official task was to complete the
hydrographic survey of the southern coasts of South America and to carry a chain of longitude
measurements around the world. The ship carried more than twenty timekeepers for that purpose,
making the voyage as much an exercise in [[Marine chronometer|chronometry]] and
[[Cartography|chart-making]] as in natural history. The *Beagle* left Plymouth on 27 December
1831 and returned to Falmouth on 2 October 1836.

Darwin spent much of the voyage ashore. In Patagonia he excavated the bones of large extinct
mammals, among them *Megatherium*, *Toxodon* and *Macrauchenia*, and a fossil horse tooth in
strata that contained no living horses — evidence both of [[Extinction]] and of a succession of
related forms in the same region. He felt the great Chilean earthquake of February 1835 while
ashore near Valdivia and inspected the ruins of Concepción a fortnight later, noting the
evidence that the land had been permanently lifted; he found raised beds of marine shells high
in the Andes, and read the first volume
of Charles Lyell's *Principles of Geology*, which taught him to think in terms of slow,
cumulative change.

He reached [[The Galápagos Islands]] on 15 September 1835 and left on 20 October, a little over
five weeks. The visit is remembered for the finches, but at the time it was the mockingbirds,
which he did label by island, and the vice-governor's remark that the giant tortoises differed
from island to island, that struck him as significant. The finch specimens were poorly
localised; only when the ornithologist John Gould sorted them in London in March 1837 and
declared them distinct species did their implication become clear. Darwin published his
*Journal of Researches* in 1839, a travel narrative that sold well and established his
reputation.[^journal1839]

## Coral reefs and geology

Darwin's first monograph was not about species at all. *The Structure and Distribution of
Coral Reefs* (1842) proposed that fringing reefs, barrier reefs and atolls are three stages of
one process: a reef grows upward on the flank of a volcanic island while the island slowly
subsides, so that the ring of living [[Coral reef|coral]] eventually encloses a lagoon where
the peak used to be.[^coral1842] He formed the theory before seeing an atoll, and regarded it
as among his best work. It was confirmed more than a century later when deep boreholes on
Pacific atolls passed through more than a kilometre of reef limestone before reaching the
volcanic basement beneath.[^ladd1960]

His geology was not uniformly successful. An 1839 paper explained the parallel terraces of Glen
Roy in Scotland as old marine beaches; the correct account involves lakes dammed by glaciers
during the last [[Ice age]], and Darwin later called the paper a great failure. He worked on
glacial landforms in Wales in 1842 and accepted the glacial interpretation once the evidence
for it accumulated.

## Two decades of evidence

Darwin opened a notebook on the transmutation of species in 1837 and drew a branching diagram
of descent above the words "I think". By 1838, after reading Malthus, he had the selective
mechanism. He then delayed publication for twenty years.

He wrote a 35-page pencil sketch of the theory in 1842 and expanded it into an essay of about
230 pages in 1844, leaving instructions for his wife to have it published if he died. That year
the anonymous *Vestiges of the Natural History of Creation* was savaged for its evolutionary
speculation, a warning Darwin took seriously. Instead of publishing, he accumulated evidence:
eight years of dissecting and describing barnacles, published as four monographs between 1851
and 1854, which showed him how much variation a single species contains; experiments on seed
dispersal in salt water; measurements of pigeon and dog breeds; and a correspondence that
survives in more than 15,000 letters, in which he questioned breeders, gardeners, diplomats and
naval officers about the variation they saw.[^correspondence] He also lacked any correct theory
of heredity, a gap only filled long after his death by Mendelian genetics and the
identification of [[Deoxyribonucleic acid|DNA]].

He was elected a Fellow of the Royal Society in 1839, married his cousin Emma Wedgwood on 29
January 1839, and moved in 1842 to Down House at Downe in Kent, which became laboratory,
garden and greenhouse for the rest of his life. Of their ten children, three died young; the
death of his daughter Annie in 1851, aged ten, affected him deeply. From the late 1830s he
suffered chronic vomiting, skin eruptions and palpitations that repeatedly interrupted his
work and sent him to hydropathic establishments; the cause was never determined, and
retrospective diagnoses proposed by later physicians remain unresolved.[^browne1]

## On the Origin of Species

On 18 June 1858 Darwin received an essay from Alfred Russel Wallace, then in the Malay
Archipelago, outlining substantially the same mechanism. Friends arranged for extracts of
Darwin's earlier writing to be read alongside Wallace's paper at the Linnean Society on 1 July
1858. Darwin then compressed his planned multi-volume work into what he called an abstract.

*On the Origin of Species by Means of Natural Selection* was published by John Murray on 24
November 1859 in an edition of 1,250 copies, which the booksellers took up immediately. The
argument proceeds from variation under domestication to variation in nature, then to the
struggle for existence, then to selection, and devotes a long chapter to difficulties with the
theory, including the imperfection of the fossil record and the sterile castes of social
insects. Darwin revised the book through six editions, the last in 1872. He avoided human
evolution almost entirely in 1859, treating it only in *The Descent of Man, and Selection in
Relation to Sex* (1871).

## Later work

The books that followed are often treated as a coda, but they were the experimental programme
that made the theory concrete.[^browne2] *Fertilisation of Orchids* (1862) showed how floral
structures are machinery for cross-pollination by particular insects, and led Darwin to predict
a moth with a proboscis long enough to reach the nectar of the Madagascan orchid *Angraecum
sesquipedale*; a hawkmoth answering the description was identified decades later. *The
Variation of Animals and Plants under Domestication* (1868) assembled his breeding data. *The
Expression of the Emotions in Man and Animals* (1872) used photographs and questionnaires sent
to correspondents overseas. *Insectivorous Plants* (1875) and *The Power of Movement in Plants*
(1880) reported experiments on sundews, Venus flytraps and seedling growth.

His last book, *The Formation of Vegetable Mould, through the Action of Worms* (1881), measured
how earthworms bury stones and coins, pass soil through their bodies and steadily rework the
surface of the land; it sold briskly and is a founding text of soil science.[^worms1881]

## Death and reputation

Darwin died at Down House on 19 April 1882 and was buried in Westminster Abbey on 26 April,
near the astronomer John Herschel and close to [[Isaac Newton]]. His scientific standing was
already secure — he had received the Royal Medal in 1853, the Wollaston Medal in 1859 and the
Copley Medal in 1864 — although natural selection itself remained disputed as a sufficient
mechanism until population genetics settled the question in the 1920s and 1930s.[^britannicadarwin]
His manuscripts, notebooks and published works are now available in full online, together with
his correspondence.[^darwinonline]
""",
        "tier": "feature",
        "kind": "person",
        "infobox": {
            "title": "Charles Darwin",
            "subtitle": "English naturalist and geologist",
            "rows": [
                {
                    "kind": "row",
                    "label": "Born",
                    "value": "12 February 1809, Shrewsbury, Shropshire, England",
                },
                {
                    "kind": "row",
                    "label": "Died",
                    "value": "19 April 1882 (aged 73), Down House, Downe, Kent",
                },
                {
                    "kind": "row",
                    "label": "Resting place",
                    "value": "Westminster Abbey, London",
                },
                {
                    "kind": "row",
                    "label": "Education",
                    "value": "University of Edinburgh; Christ's College, Cambridge",
                },
                {"kind": "header", "value": "Work"},
                {"kind": "row", "label": "Fields", "value": "Natural history, geology"},
                {
                    "kind": "row",
                    "label": "Known for",
                    "value": "Natural selection; common descent; the subsidence theory of atolls",
                },
                {
                    "kind": "row",
                    "label": "Voyage",
                    "value": "HMS *Beagle*, 27 December 1831 – 2 October 1836",
                },
                {
                    "kind": "row",
                    "label": "Major works",
                    "value": (
                        "*Journal of Researches* (1839); *Coral Reefs* (1842); "
                        "*On the Origin of Species* (1859); *The Descent of Man* (1871)"
                    ),
                },
                {"kind": "header", "value": "Personal"},
                {
                    "kind": "row",
                    "label": "Spouse",
                    "value": "Emma Wedgwood, married 29 January 1839",
                },
                {"kind": "row", "label": "Children", "value": "Ten, three of whom died young"},
                {
                    "kind": "row",
                    "label": "Honours",
                    "value": "Fellow of the Royal Society (1839); Copley Medal (1864)",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "journal1839",
                "title": (
                    "Journal of Researches into the Geology and Natural History of the "
                    "Various Countries Visited by H.M.S. Beagle"
                ),
                "url": "http://darwin-online.org.uk/",
                "authors": "Charles Darwin",
                "publisher": "Henry Colburn, London",
                "published_on": "1839",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "coral1842",
                "title": "The Structure and Distribution of Coral Reefs",
                "url": "http://darwin-online.org.uk/",
                "authors": "Charles Darwin",
                "publisher": "Smith, Elder and Co., London",
                "published_on": "1842",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "ladd1960",
                "title": (
                    "Bikini and nearby atolls, Marshall Islands: drilling operations on "
                    "Eniwetok Atoll"
                ),
                "url": "https://pubs.usgs.gov/publication/pp260Y",
                "authors": "Harry S. Ladd, Seymour O. Schlanger",
                "publisher": "U.S. Geological Survey Professional Paper 260-Y",
                "published_on": "1960",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "correspondence",
                "title": "Darwin Correspondence Project",
                "url": "https://www.darwinproject.ac.uk/",
                "authors": "",
                "publisher": "University of Cambridge",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "browne1",
                "title": "Charles Darwin: Voyaging",
                "url": "",
                "authors": "Janet Browne",
                "publisher": "Jonathan Cape, London",
                "published_on": "1995",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "browne2",
                "title": "Charles Darwin: The Power of Place",
                "url": "",
                "authors": "Janet Browne",
                "publisher": "Jonathan Cape, London",
                "published_on": "2002",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "worms1881",
                "title": (
                    "The Formation of Vegetable Mould, through the Action of Worms, with "
                    "Observations on their Habits"
                ),
                "url": "http://darwin-online.org.uk/",
                "authors": "Charles Darwin",
                "publisher": "John Murray, London",
                "published_on": "1881",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "darwinonline",
                "title": "The Complete Work of Charles Darwin Online",
                "url": "http://darwin-online.org.uk/",
                "authors": "John van Wyhe (editor)",
                "publisher": "University of Cambridge",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannicadarwin",
                "title": "Charles Darwin",
                "url": "https://www.britannica.com/biography/Charles-Darwin",
                "authors": "",
                "publisher": "Encyclopædia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Natural selection",
            "The Galápagos Islands",
            "Coral reef",
            "Extinction",
            "Deoxyribonucleic acid",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "Charles Darwin",
            "evolution",
            "HMS Beagle",
            "Victorian science",
            "naturalists",
        ],
    },
]
