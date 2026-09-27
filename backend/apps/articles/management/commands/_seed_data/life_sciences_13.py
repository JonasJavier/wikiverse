"""Life Sciences — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Deoxyribonucleic acid",
        "category": "Life Sciences",
        "categories": ["Chemistry and Materials", "Computing and Information"],
        "short_description": "The double-helical molecule that stores heritable information in living cells",
        "summary": (
            "Deoxyribonucleic acid is the double-helical polymer in which almost all "
            "organisms store genetic information. Its complementary base pairing explains "
            "both faithful copying and the mutations that supply variation to evolution."
        ),
        "content": """**Deoxyribonucleic acid**, or DNA, is the long-chain molecule in which nearly every
living organism stores its heritable information. Two strands wind around a common axis as a
double helix, and because each base on one strand determines the base facing it on the other,
the molecule carries a built-in template for its own duplication. That single structural fact
links the chemistry of DNA to heredity, to protein synthesis and to the supply of variation on
which [[Natural selection|natural selection]] acts.

## Chemical structure

DNA is a polymer of nucleotides. Each nucleotide has three parts: a phosphate group, the
five-carbon sugar 2-deoxyribose, and one of four nitrogen-containing bases — adenine (A) and
guanine (G), which are double-ringed purines, and cytosine (C) and thymine (T), which are
single-ringed pyrimidines. Successive sugars are joined by phosphodiester bonds between the
3' carbon of one and the 5' carbon of the next, so each strand has a chemical direction,
conventionally read from the 5' end to the 3' end.

The two strands run antiparallel, with the bases turned inward. Adenine pairs only with thymine
and guanine only with cytosine, the rule set out in the 1953 structure;[^watson1953] the A-T pair
is held by two hydrogen bonds and the G-C pair by three.[^alberts]
Something of this complementarity was already implicit in the base ratios Erwin Chargaff
measured around 1950, which showed that in DNA from any species the quantity of adenine matches
that of thymine and guanine matches cytosine. The pairing rule also keeps the helix a constant
width, because a large purine always faces a small pyrimidine.

The sugar-phosphate backbones, each carrying one negative charge per phosphate, face outward
into the surrounding solution, while the flat bases stack on one another in the interior. The
[[Chemical bond|hydrogen bonds]] between paired bases supply the specificity, but a large share
of the molecule's physical stability comes from that stacking and from the fact that burying the
bases shields them from [[Water|water]]. Heating a DNA solution separates the strands, and the
temperature at which half of them have come apart rises with the proportion of G-C pairs, since
each of those contributes three hydrogen bonds rather than two.

Under physiological conditions DNA adopts the right-handed B form: roughly 2 nanometres across,
with successive base pairs 0.34 nm apart along the axis and about ten and a half pairs to a
complete turn. Because the two backbones are not diametrically opposite, the surface carries a
wide major groove and a narrow minor groove, and most proteins that recognise specific sequences
do so by inserting a helix or loop into the major groove.

## The road to the double helix

Friedrich Miescher isolated a phosphorus-rich substance he called nuclein from cell nuclei in
1869, but for decades DNA looked too monotonous to carry heredity, and protein seemed the better
candidate. Frederick Griffith showed in 1928 that a harmless pneumococcus could be permanently
converted to a virulent form by something in the remains of killed virulent bacteria. In 1944
Oswald Avery, Colin MacLeod and Maclyn McCarty identified that transforming principle as DNA,
purified, free of detectable protein and still active at very low concentrations.[^avery1944]
Alfred Hershey and Martha Chase reinforced the conclusion in 1952 by labelling bacteriophage
protein and DNA with different radioisotopes and showing that most of the DNA label entered
infected cells while most of the protein label stayed outside.

The structure itself was solved at Cambridge in early 1953 by James Watson and Francis Crick,
working from X-ray diffraction data produced at King's College London by Rosalind Franklin and
Raymond Gosling. Franklin's image of hydrated B-form fibres, later known as Photograph 51,
showed the X-shaped pattern characteristic of a helix and allowed the repeat distance to be
measured; her unpublished report also supplied correct unit-cell dimensions. The Watson and
Crick model appeared in *Nature* on 25 April 1953 in a paper of about nine hundred words,
accompanied in the same issue by reports from Franklin and Gosling and from Maurice Wilkins and
colleagues presenting the diffraction evidence.[^watson1953][^franklin1953] Watson, Crick and
Wilkins shared the 1962 Nobel Prize in Physiology or Medicine; Franklin had died of ovarian
cancer in 1958, aged 37, and the prize is not awarded posthumously. How her data reached
Cambridge, and how thinly the 1953 paper acknowledged it, has been argued over ever since.

## Replication

The 1953 paper's central prediction was that the strands come apart and each serves as a
template. Matthew Meselson and Franklin Stahl tested it in 1958 by growing *Escherichia coli*
in a medium containing the heavy nitrogen isotope nitrogen-15, transferring the cells to ordinary
nitrogen-14, and separating the DNA by density in a caesium chloride gradient. After one
generation all the DNA was of intermediate density; after two, half was intermediate and half
light. That is exactly the pattern expected if each daughter molecule retains one old strand and
one new one, a scheme called semiconservative replication.[^meselson1958]

In cells, replication starts at defined origins, where helicases unwind the duplex. DNA
polymerases add nucleotides only to the 3' end of a growing chain, so one new strand can be
extended continuously while the other is assembled in short pieces that are later joined.
Fidelity is high but not perfect: polymerase proofreading together with mismatch repair brings
the error rate down to the order of one wrong base in a billion or more added.[^alberts]

## From sequence to protein

DNA specifies proteins indirectly. A gene is transcribed into messenger RNA, which uses ribose
in place of deoxyribose and uracil in place of thymine, and ribosomes then translate that
message into a chain of amino acids. Four bases cannot specify twenty standard amino acids one at
a time, and pairs of bases allow only sixteen combinations; triplets allow 64. Marshall Nirenberg
and Heinrich Matthaei read the first codon in 1961 by adding synthetic RNA composed only of
uracil to a bacterial extract and recovering a polypeptide of pure phenylalanine.[^nirenberg1961]
Within five years the table was complete: 61 codons specify amino acids, three mark the end of a
chain, and most amino acids have more than one codon. The code is nearly universal across life,
and its redundancy means that many single-base changes leave the resulting protein unaltered.

## Mutation, repair and variation

DNA is chemically reactive, and a cell must repair it continuously. Cytosine spontaneously
deaminates to uracil; ultraviolet light fuses adjacent pyrimidines; oxygen radicals modify
guanine. Repair systems excise the damaged stretch and rebuild it against the intact
complementary strand, one of the practical advantages of storing information in
duplicate.[^alberts] What escapes repair becomes mutation, at a germline rate in humans on the
order of one new change per hundred million bases per generation.

Mutation is not only damage. It is the origin of the heritable variation that
[[Charles Darwin|Darwin]] could only postulate, and without a steady supply of new variants
differential survival would have nothing to sort. Sexual reproduction adds a second source of
novelty by recombining stretches of maternal and paternal chromosomes. The speed with which
bacterial populations acquire resistance to [[Penicillin|antibiotics]] is the same process
compressed into laboratory timescales.

## Genomes and sequencing

A genome is the complete DNA content of a cell, and genome size varies enormously without
tracking organismal complexity. The human haploid genome is roughly 3.1 billion base pairs
spread over 23 chromosomes and contains fewer than 20,000 protein-coding genes; most of its
length is non-coding, including regulatory sequence, introns and large quantities of repeated
and transposon-derived material. A separate small genome sits inside the mitochondria: in humans
16,569 base pairs encoding 13 proteins, two ribosomal RNAs and 22 transfer RNAs, a relic of the
bacterial ancestry of the organelle.[^anderson1981]

Frederick Sanger's chain-termination method, introduced in 1977, made sequencing routine. A
publicly funded international project and a competing private effort published draft human
sequences in 2001, and an essentially finished reference followed in 2003. The remaining gaps,
mostly in highly repetitive regions such as centromeres, were closed by long-read methods, and a
genuinely gapless sequence of a single human genome was reported in 2022.[^nurk2022]

## DNA as stored information

DNA invites description in the vocabulary of [[Information theory|information theory]]: a
sequence drawn from four symbols carries at most two bits per position, so 3.1 billion base
pairs correspond to about 775 megabytes in a naive two-bit encoding. Real genomes compress well
below that figure, because the sequence is far from random. The analogy repays attention in
other ways too — error-correcting redundancy, the distinction between a message and its channel,
the cost of copying.

Its limits matter as much. DNA is not read as a passive tape: which genes are transcribed
depends on regulatory proteins, on chemical modification of the bases and of the histones that
package them, and on the state of the surrounding [[The cell|cell]]. The molecule is also a
chemical, subject to damage and turnover, and a cell rebuilds its own components continuously,
so the persistence of a genome across a lifetime resembles the puzzle of the
[[Ship of Theseus]] more than a file sitting on a disk.

DNA also serves as a historical record. Because sequences accumulate differences at measurable
rates, comparing them reconstructs relationships among living organisms, and DNA recovered from
bones, teeth and sediments has been sequenced from remains tens of thousands of years old and,
in exceptional cases, from very much older material.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Deoxyribonucleic acid",
            "subtitle": "Biological macromolecule",
            "rows": [
                {"kind": "header", "value": "Composition"},
                {"kind": "row", "label": "Class", "value": "Nucleic acid polymer"},
                {"kind": "row", "label": "Monomer", "value": "Deoxyribonucleotide"},
                {
                    "kind": "row",
                    "label": "Bases",
                    "value": "Adenine, thymine, guanine, cytosine",
                },
                {
                    "kind": "row",
                    "label": "Pairing",
                    "value": "A-T (two hydrogen bonds), G-C (three)",
                },
                {"kind": "header", "value": "B-form geometry"},
                {"kind": "row", "label": "Diameter", "value": "About 2 nm"},
                {"kind": "row", "label": "Rise per base pair", "value": "0.34 nm"},
                {"kind": "row", "label": "Helical repeat", "value": "About 10.5 base pairs"},
                {"kind": "header", "value": "History"},
                {"kind": "row", "label": "First isolated", "value": "1869, by Friedrich Miescher"},
                {"kind": "row", "label": "Structure published", "value": "25 April 1953"},
                {
                    "kind": "full",
                    "value": "Human haploid genome: about 3.1 billion base pairs",
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/4/4c/DNA_Structure%2BKey%2BLabelled.pn_NoBB.png",
            "alt": "Labelled diagram of the DNA double helix showing two backbones and four paired bases",
            "caption": (
                "The B-form double helix: two antiparallel sugar-phosphate backbones on the "
                "outside, complementary base pairs stacked within."
            ),
            "credit": "Zephyris (Richard Wheeler)",
            "license": "CC BY-SA 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:DNA_Structure%2BKey%2BLabelled.pn_NoBB.png",
        },
        "references": [
            {
                "key": "watson1953",
                "title": (
                    "Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid"
                ),
                "url": "https://www.nature.com/articles/171737a0",
                "authors": "James D. Watson and Francis H. C. Crick",
                "publisher": "Nature 171, 737-738",
                "published_on": "25 April 1953",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/171737a0",
                "quote": "",
            },
            {
                "key": "franklin1953",
                "title": "Molecular Configuration in Sodium Thymonucleate",
                "url": "https://www.nature.com/articles/171740a0",
                "authors": "Rosalind E. Franklin and Raymond G. Gosling",
                "publisher": "Nature 171, 740-741",
                "published_on": "25 April 1953",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/171740a0",
                "quote": "",
            },
            {
                "key": "avery1944",
                "title": (
                    "Studies on the Chemical Nature of the Substance Inducing Transformation "
                    "of Pneumococcal Types"
                ),
                "url": "https://doi.org/10.1084/jem.79.2.137",
                "authors": "Oswald T. Avery, Colin M. MacLeod and Maclyn McCarty",
                "publisher": "Journal of Experimental Medicine 79, 137-158",
                "published_on": "1944",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1084/jem.79.2.137",
                "quote": "",
            },
            {
                "key": "meselson1958",
                "title": "The Replication of DNA in Escherichia coli",
                "url": "https://doi.org/10.1073/pnas.44.7.671",
                "authors": "Matthew Meselson and Franklin W. Stahl",
                "publisher": "Proceedings of the National Academy of Sciences 44, 671-682",
                "published_on": "1958",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1073/pnas.44.7.671",
                "quote": "",
            },
            {
                "key": "nirenberg1961",
                "title": (
                    "The Dependence of Cell-Free Protein Synthesis in E. coli upon Naturally "
                    "Occurring or Synthetic Polyribonucleotides"
                ),
                "url": "https://doi.org/10.1073/pnas.47.10.1588",
                "authors": "Marshall W. Nirenberg and J. Heinrich Matthaei",
                "publisher": "Proceedings of the National Academy of Sciences 47, 1588-1602",
                "published_on": "October 1961",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1073/pnas.47.10.1588",
                "quote": "",
            },
            {
                "key": "anderson1981",
                "title": "Sequence and Organization of the Human Mitochondrial Genome",
                "url": "https://www.nature.com/articles/290457a0",
                "authors": "Stephen Anderson and colleagues",
                "publisher": "Nature 290, 457-465",
                "published_on": "9 April 1981",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/290457a0",
                "quote": "",
            },
            {
                "key": "nurk2022",
                "title": "The Complete Sequence of a Human Genome",
                "url": "https://doi.org/10.1126/science.abj6987",
                "authors": "Sergey Nurk and colleagues",
                "publisher": "Science 376, 44-53",
                "published_on": "April 2022",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.abj6987",
                "quote": "",
            },
            {
                "key": "alberts",
                "title": "Molecular Biology of the Cell, sixth edition",
                "url": "https://archive.org/details/molecularbiology0006edalbe",
                "authors": "Bruce Alberts, Alexander Johnson, Julian Lewis and others",
                "publisher": "Garland Science, New York",
                "published_on": "2015",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-8153-4432-2",
                "quote": "",
            },
        ],
        "see_also": [
            "The cell",
            "Natural selection",
            "Chemical bond",
            "Information theory",
            "Penicillin",
            "Ship of Theseus",
        ],
        "aliases": ["DNA"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["genetics", "molecular biology", "double helix", "heredity"],
    },
    {
        "title": "The cell",
        "category": "Life Sciences",
        "categories": ["Medicine and the Mind"],
        "short_description": "The smallest self-maintaining unit of life and the basis of every organism",
        "summary": (
            "The cell is the smallest unit able to maintain and reproduce itself, and every "
            "known organism is either a single cell or an assembly of them. Cell theory holds "
            "that cells arise only from other cells."
        ),
        "content": """**The cell** is the smallest unit of matter able to maintain and reproduce itself,
and every known organism is either a single cell or an assembly of them. Cells differ enormously
in size, shape and lifestyle, but all of them are bounded by a membrane, all store their
instructions in [[Deoxyribonucleic acid|DNA]], and all build their proteins on ribosomes.

## Discovery and cell theory

Robert Hooke, examining a thin slice of cork with a compound microscope, described rows of small
compartments that reminded him of the cells of a monastery and published the observation in
*Micrographia* in 1665.[^hooke1665] What he saw were the empty walls of dead plant tissue rather
than living contents. Antonie van Leeuwenhoek, using single-lens instruments of remarkable
quality, went further in the 1670s and 1680s, reporting motile single-celled organisms in pond
water, saliva and rainwater.

Progress then stalled until achromatic lenses reduced optical distortion in the 1830s. Matthias
Schleiden argued in 1838 that plant tissues are built from cells, Theodor Schwann extended the
claim to animals in 1839, and Rudolf Virchow supplied the third element in 1855 with the
formula that every cell arises from another cell. Cell theory in that form did more than
describe anatomy: it made it plausible that disease might be caused by organisms that were
themselves cells, an idea developed a few decades later into the
[[Germ theory of disease|germ theory of disease]].

## Shared architecture

Every cell is enclosed by a plasma membrane about 5 nanometres thick, built from a double layer
of phospholipids whose water-repelling tails face inward. The bilayer blocks the passage of ions
and most polar molecules, so traffic across it is handled by embedded transport proteins, which
is what allows a cell to hold an interior chemically unlike its surroundings. The membrane is
not rigid: in the fluid mosaic description proposed by Jonathan Singer and Garth Nicolson in
1972, its lipids and proteins diffuse laterally within the plane of the sheet.

Inside is the cytosol, a crowded solution in which [[Water|water]] accounts for roughly seventy
per cent of the cell's mass. It holds the genome, ribosomes that translate messenger RNA into
protein, enzymes for the central metabolic pathways, and a cytoskeleton of protein filaments
that gives shape, moves cargo and drives division. Energy is handled through a small set of
carriers, chiefly adenosine triphosphate, and is often stored first as a gradient of protons
across a membrane, a mechanism Peter Mitchell proposed in 1961 against considerable
resistance.[^mitchell1961]

## Prokaryotes and eukaryotes

The deepest division among cells is between prokaryotes, which have no nucleus, and eukaryotes,
which do. Prokaryotic cells — the Bacteria and the Archaea — are typically 1 to 5 micrometres
long, with their DNA in a single circular chromosome lying free in the cytoplasm. Eukaryotic
cells are usually 10 to 100 micrometres across, thousands of times larger by volume, and are
partitioned by internal membranes into a nucleus, endoplasmic reticulum, Golgi apparatus,
lysosomes and other compartments. That compartmentalisation lets incompatible reactions proceed
at once in separate chemical environments.[^alberts]

## Organelles that were once bacteria

Mitochondria and chloroplasts stand apart from the rest of the eukaryotic interior. Each has two
surrounding membranes, its own small circular genome, its own ribosomes, and divides on its own
schedule rather than being assembled afresh. Konstantin Mereschkowsky suggested in 1905 that
chloroplasts descend from captured cyanobacteria, and Lynn Margulis set out the full
endosymbiotic case in 1967, arguing that mitochondria, chloroplasts and other organelles began
as free-living prokaryotes taken up by a host cell.[^sagan1967] Sequence comparison later
settled the matter: mitochondria are related to alphaproteobacteria and chloroplasts to
cyanobacteria, which is why chloroplasts can carry out [[Photosynthesis]] much as their
ancestors did.

The human mitochondrial genome is a striking remnant of that history — 16,569 base pairs
encoding 13 proteins, two ribosomal RNAs and 22 transfer RNAs, packed so tightly that genes
abut one another with almost no spacer sequence.[^anderson1981]

## Division

Bacteria divide by binary fission, copying the chromosome and pinching the cell in two.
Eukaryotic division is more elaborate: chromosomes are duplicated during the S phase of the cell
cycle, condensed, aligned on a spindle of microtubules and pulled apart in mitosis before the
cytoplasm is split. Checkpoints hold the cycle until the previous step has been completed
correctly. A second, specialised division, meiosis, halves the chromosome number to produce
gametes and shuffles maternal and paternal chromosomes in the process, supplying much of the
genetic variation on which [[Natural selection|selection]] operates.

## Scale, number and specialisation

The smallest bacterial cells, such as some mycoplasmas, are around 0.2 micrometres across; the
largest single cells, including bird eggs, are visible without help. A human adult has been
estimated to contain about 37 trillion cells, a figure arrived at by adding up organ-by-organ
counts rather than by any single measurement.[^bianconi2013] These fall into more than two
hundred recognised types whose division of labour is the subject matter of
[[Human anatomy|human anatomy]]: red blood cells, which in humans discard their nucleus and last
about four months; muscle fibres with many nuclei; and neurons that are generally not replaced
at all, so that the durability of [[Memory]] rests on molecular turnover inside cells that
themselves persist for a lifetime.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "The cell",
            "subtitle": "Fundamental unit of life",
            "rows": [
                {"kind": "row", "label": "Named by", "value": "Robert Hooke, 1665"},
                {
                    "kind": "row",
                    "label": "Cell theory",
                    "value": "Schleiden and Schwann, 1838-1839; Virchow, 1855",
                },
                {"kind": "header", "value": "Typical dimensions"},
                {"kind": "row", "label": "Bacterium", "value": "1-5 micrometres long"},
                {"kind": "row", "label": "Animal cell", "value": "10-30 micrometres across"},
                {"kind": "row", "label": "Plasma membrane", "value": "About 5 nanometres thick"},
                {"kind": "header", "value": "Major lineages"},
                {
                    "kind": "row",
                    "label": "Prokaryotes",
                    "value": "Bacteria and Archaea; no nucleus",
                },
                {
                    "kind": "row",
                    "label": "Eukaryotes",
                    "value": "Nucleus and membrane-bound organelles",
                },
                {
                    "kind": "full",
                    "value": "An adult human body is estimated at roughly 37 trillion cells",
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Micrographia_Schem_11.jpg",
            "alt": "Engraving of thin slices of cork showing rows of small empty compartments",
            "caption": (
                "Hooke's engraving of cork from Micrographia (1665), the observation that gave "
                "the cell its name."
            ),
            "credit": "Robert Hooke; digitised copy held by the National Library of Wales",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Micrographia_Schem_11.jpg",
        },
        "references": [
            {
                "key": "hooke1665",
                "title": "Micrographia: or Some Physiological Descriptions of Minute Bodies",
                "url": "https://www.gutenberg.org/ebooks/15491",
                "authors": "Robert Hooke",
                "publisher": "Printed for the Royal Society, London",
                "published_on": "1665",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sagan1967",
                "title": "On the Origin of Mitosing Cells",
                "url": "https://doi.org/10.1016/0022-5193(67)90079-3",
                "authors": "Lynn Sagan (Lynn Margulis)",
                "publisher": "Journal of Theoretical Biology 14, 225-274",
                "published_on": "March 1967",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1016/0022-5193(67)90079-3",
                "quote": "",
            },
            {
                "key": "anderson1981",
                "title": "Sequence and Organization of the Human Mitochondrial Genome",
                "url": "https://www.nature.com/articles/290457a0",
                "authors": "Stephen Anderson and colleagues",
                "publisher": "Nature 290, 457-465",
                "published_on": "9 April 1981",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/290457a0",
                "quote": "",
            },
            {
                "key": "mitchell1961",
                "title": (
                    "Coupling of Phosphorylation to Electron and Hydrogen Transfer by a "
                    "Chemi-Osmotic Type of Mechanism"
                ),
                "url": "https://www.nature.com/articles/191144a0",
                "authors": "Peter Mitchell",
                "publisher": "Nature 191, 144-148",
                "published_on": "1961",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/191144a0",
                "quote": "",
            },
            {
                "key": "bianconi2013",
                "title": "An Estimation of the Number of Cells in the Human Body",
                "url": "https://doi.org/10.3109/03014460.2013.807878",
                "authors": "Eva Bianconi and colleagues",
                "publisher": "Annals of Human Biology 40, 463-471",
                "published_on": "2013",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.3109/03014460.2013.807878",
                "quote": "",
            },
            {
                "key": "alberts",
                "title": "Molecular Biology of the Cell, sixth edition",
                "url": "https://archive.org/details/molecularbiology0006edalbe",
                "authors": "Bruce Alberts, Alexander Johnson, Julian Lewis and others",
                "publisher": "Garland Science, New York",
                "published_on": "2015",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-8153-4432-2",
                "quote": "",
            },
        ],
        "see_also": [
            "Deoxyribonucleic acid",
            "Photosynthesis",
            "Germ theory of disease",
            "Human anatomy",
            "Natural selection",
        ],
        "aliases": ["Cell theory"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["cell biology", "cell theory", "organelles", "endosymbiosis"],
    },
    {
        "title": "Coral reef",
        "category": "Life Sciences",
        "categories": ["Earth and Environment", "Geography and Places"],
        "short_description": "A limestone structure built by colonial animals living with algae",
        "summary": (
            "A coral reef is a wave-resistant limestone structure built by colonial stony "
            "corals in partnership with photosynthetic algae. Reefs cover about one per cent of "
            "the ocean yet shelter at least a quarter of marine species."
        ),
        "content": """**A coral reef** is a wave-resistant structure of calcium carbonate built by
colonial marine animals, chiefly the stony corals, together with calcifying algae and the
skeletal debris that accumulates among them. Reefs are simultaneously ecosystems and landforms:
they support an extraordinary concentration of species and, over thousands of years, they build
islands, lagoons and barriers large enough to alter coastlines.

## The reef-building partnership

Stony corals are cnidarians. Each polyp is a sac of tissue a few millimetres across, ringed with
stinging tentacles, that secretes a cup of aragonite — a crystalline form of calcium carbonate —
beneath itself. Polyps bud to form colonies, and colonies cement together into a framework.

What makes rapid reef construction possible is a partnership inside the coral's own tissue.
Single-celled dinoflagellate algae of the family Symbiodiniaceae, long known as zooxanthellae,
live within the coral's gastrodermal cells at densities of around a million per square
centimetre. They photosynthesise and pass sugars, glycerol and amino acids to the host: as much
as ninety per cent of the organic material they produce is transferred to the coral's tissue, and
in exchange they receive shelter, carbon dioxide and nitrogenous waste.[^noaa_zoox] That subsidy
is what allows corals to calcify fast enough to outpace erosion, and it also constrains them:
reef-building corals need clear, well-lit [[Water|seawater]], so reefs are largely confined to
the upper few tens of metres of the water column, to waters between roughly 18 and 30 degrees
Celsius, and to places where nutrients and suspended sediment are low. The reef is, in effect, a
limestone landform erected on the proceeds of [[Photosynthesis]].

## Reef types and Darwin's subsidence theory

Three forms have been distinguished since the nineteenth century: fringing reefs attached to a
shore, barrier reefs separated from land by a lagoon, and atolls, rings of reef enclosing a
lagoon with no central island at all. [[Charles Darwin]] proposed in 1842 that these are not
three kinds of thing but three stages of one process. A reef grows around a volcanic island; the
island slowly subsides; the corals, needing light, keep building upward, so the reef is
progressively separated from the shrinking land by a widening lagoon, and when the island
finally disappears beneath the surface a ring remains.[^darwin1842]

The theory made a hard prediction: beneath an atoll there should be a great thickness of
shallow-water limestone resting on volcanic rock. Confirmation came in 1952, when deep drilling
at Enewetak Atoll in the Marshall Islands struck basalt beneath roughly 1,270 metres of
carbonate in one hole and about 1,400 metres in another on the opposite side of the
atoll.[^ladd1960] What Darwin could not supply was a reason for the subsidence; that came with
[[Plate tectonics]], which explains how oceanic lithosphere cools, thickens and sinks as it
carries a volcanic island away from the hotspot that built it.

## Biodiversity

Reefs occupy about one per cent of the ocean yet provide habitat for at least a quarter of all
marine species.[^noaa] The reason is structural as much as biological: a reef framework
is riddled with crevices, overhangs and cavities at every scale, offering refuges, nurseries and
feeding stations that a flat sea bed cannot. Several hundred species of reef-building coral, and
tens of thousands of fish, molluscs, crustaceans, sponges and echinoderms, partition that space
finely, and the resulting specialisation is a much-studied example of
[[Natural selection]] producing narrow ecological niches. Reef-dwellers include some of the
ocean's more capable predators, among them the [[Octopus|octopuses]] that hunt crustaceans in
reef rubble.

The largest reef system is the Great Barrier Reef off Queensland, which stretches about 2,300
kilometres, comprises some three thousand individual reefs, and was inscribed as a World
Heritage site in 1981; the marine park covers 344,400 square kilometres.[^unesco]

## Growth, erosion and sediment

Reef framework accretes slowly — commonly a few millimetres of vertical growth a year — even
though individual branching corals such as *Acropora* can extend their tips by more than ten
centimetres in the same period. Working against that construction is bioerosion: parrotfish
scrape coral to reach algae, boring sponges and bivalves tunnel into the skeleton, and sea
urchins rasp at the surface. Much of the white sand on a reef island has passed through the gut
of a fish. A healthy reef is a balance between these two rates, and the balance can tip.

## Bleaching and acidification

Coral bleaching is the visible breakdown of the algal partnership. Under stress, most often
elevated water temperature, corals expel or digest their symbionts; because the coral tissue is
nearly transparent, the white aragonite skeleton shows through. Bleaching is survivable if brief
but lethal if prolonged, and the thermal margin is narrow, on the order of one degree above the
usual summer maximum sustained for weeks. Analysis of the 2016 heatwave on the Great Barrier
Reef found that corals began dying where accumulated heat exposure passed three to four
degree-heating-weeks, and that the loss of fast-growing tabular and staghorn colonies
transformed the three-dimensional structure of 29 per cent of the system's 3,863
reefs.[^hughes2018]

A slower pressure acts through chemistry rather than temperature. Carbon dioxide dissolving into
the ocean lowers its pH and reduces the saturation state of aragonite, making skeleton-building
more energetically expensive — one of the clearest links between reefs and the
[[The carbon cycle|carbon cycle]]. The fossil record shows that reef systems have collapsed
before: carbonate reef communities were among the casualties of several mass
[[Extinction|extinctions]], and rebuilding them took millions of years.

## Cold-water reefs

Not all reefs depend on light. *Desmophyllum pertusum*, formerly called *Lophelia pertusa*,
builds mounds and thickets hundreds of metres deep in cold, dark water on continental margins,
without any algal symbionts, capturing plankton and organic particles instead. These
frameworks grow very slowly and can be centuries or millennia old, which makes them
correspondingly slow to recover from damage by bottom trawling.
""",
        "tier": "standard",
        "kind": "place",
        "infobox": {
            "title": "Coral reef",
            "subtitle": "Marine ecosystem and carbonate landform",
            "rows": [
                {
                    "kind": "row",
                    "label": "Builders",
                    "value": "Scleractinian (stony) corals, coralline algae",
                },
                {"kind": "row", "label": "Skeleton", "value": "Aragonite (calcium carbonate)"},
                {
                    "kind": "row",
                    "label": "Symbionts",
                    "value": "Dinoflagellate algae of the family Symbiodiniaceae",
                },
                {"kind": "header", "value": "Conditions for reef growth"},
                {"kind": "row", "label": "Temperature", "value": "Roughly 18-30 degrees Celsius"},
                {
                    "kind": "row",
                    "label": "Depth",
                    "value": "Mostly the upper few tens of metres",
                },
                {"kind": "header", "value": "Forms"},
                {"kind": "row", "label": "Types", "value": "Fringing reef, barrier reef, atoll"},
                {
                    "kind": "row",
                    "label": "Largest system",
                    "value": "Great Barrier Reef, about 2,300 km long",
                },
                {
                    "kind": "full",
                    "value": (
                        "Reefs cover about one per cent of the ocean but host at least a "
                        "quarter of marine species"
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Coral_Outcrop_Flynn_Reef.jpg",
            "alt": "Underwater photograph of a dense coral outcrop with small fish above it",
            "caption": "A coral outcrop on Flynn Reef, part of the Great Barrier Reef off Queensland.",
            "credit": "Toby Hudson",
            "license": "CC BY-SA 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:Coral_Outcrop_Flynn_Reef.jpg",
        },
        "references": [
            {
                "key": "darwin1842",
                "title": "The Structure and Distribution of Coral Reefs",
                "url": (
                    "https://darwin-online.org.uk/converted/published/1842_Coral_F271/"
                    "1842_Coral_F271.html"
                ),
                "authors": "Charles Darwin",
                "publisher": "Smith, Elder and Co., London",
                "published_on": "1842",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "ladd1960",
                "title": "Drilling Operations on Eniwetok Atoll",
                "url": "https://pubs.usgs.gov/pp/0260y/report.pdf",
                "authors": "Harry S. Ladd and Seymour O. Schlanger",
                "publisher": "U.S. Geological Survey Professional Paper 260-Y",
                "published_on": "1960",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "hughes2018",
                "title": "Global Warming Transforms Coral Reef Assemblages",
                "url": "https://www.nature.com/articles/s41586-018-0041-2",
                "authors": "Terry P. Hughes and colleagues",
                "publisher": "Nature 556, 492-496",
                "published_on": "April 2018",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/s41586-018-0041-2",
                "quote": "",
            },
            {
                "key": "noaa",
                "title": "Why Are Coral Reefs Important?",
                "url": (
                    "https://oceanservice.noaa.gov/education/tutorial_corals/"
                    "coral07_importance.html"
                ),
                "authors": "",
                "publisher": "NOAA National Ocean Service, Corals Tutorial",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "noaa_zoox",
                "title": "What Is Zooxanthellae?",
                "url": (
                    "https://oceanservice.noaa.gov/education/tutorial_corals/"
                    "coral02_zooxanthellae.html"
                ),
                "authors": "",
                "publisher": "NOAA National Ocean Service, Corals Tutorial",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "unesco",
                "title": "Great Barrier Reef",
                "url": "https://whc.unesco.org/en/list/154/",
                "authors": "",
                "publisher": "UNESCO World Heritage Centre",
                "published_on": "inscribed 1981",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Charles Darwin",
            "Natural selection",
            "Plate tectonics",
            "Extinction",
            "Octopus",
            "The Galápagos Islands",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["marine biology", "corals", "symbiosis", "ecology"],
    },
]
