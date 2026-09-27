"""Chemistry and Materials — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Chemical bond",
        "category": "Chemistry and Materials",
        "categories": ["Physics"],
        "short_description": "What holds atoms together in molecules, crystals and metals",
        "summary": (
            "A chemical bond is an attraction between atoms strong enough to hold them in a "
            "stable arrangement. Ionic, covalent and metallic bonding, together with weaker "
            "hydrogen bonds, account for the structure of almost all ordinary matter."
        ),
        "content": """**A chemical bond** is an attraction between atoms strong enough to hold them in a
stable arrangement, so that matter exists as molecules, crystals and metals rather than as a
loose gas of separate atoms. Bonding is the reason a mixture of hydrogen and oxygen behaves
nothing like the [[Water|water]] the two elements form, and it is the layer of explanation
that links the arrangement of [[The periodic table|the periodic table]] to the properties of
every substance built from it.

## Why atoms bond

The question only became answerable once [[Atomic theory|atoms]] were treated as real,
countable objects with an internal structure of electrons and nuclei. Atoms combine when the
resulting arrangement has a lower total energy than the separated atoms: nuclei attract
electrons and repel one another, electrons repel one another, and a bond exists wherever the
electrons can redistribute themselves so that the net attraction outweighs the net
repulsion.[^britannica]

The energy difference is the bond's strength, measured as the bond dissociation energy — the
heat needed to pull two bonded atoms apart in the gas phase. Breaking the H–H bond in
molecular hydrogen takes 436 kilojoules per mole; the triple bond in nitrogen takes 945,
which is why atmospheric nitrogen is nearly inert and why fixing it industrially demands
high temperature and pressure; an ordinary carbon–carbon single bond takes about 346.[^nist]
Bonds are also short: the two protons in a hydrogen molecule sit 74 picometres apart.

Chemists sort the strong bonds into three types — ionic, covalent and metallic — with weaker
intermolecular forces layered on top. The categories are idealisations, and most real bonds
sit somewhere between two of them.

## Ionic bonding

When sodium metal reacts with chlorine gas, an electron passes from each sodium atom to a
chlorine atom, leaving positive and negative ions held together by simple electrostatic
attraction. Because that attraction acts in every direction, an ionic compound is not a
molecule but an extended lattice: in sodium chloride each sodium ion is surrounded by six
chloride ions and each chloride by six sodium ions. Dismantling one mole of that lattice
into free gaseous ions costs 787 kilojoules, which is why [[Salt|common salt]] melts only at
801 °C. Ionic solids are brittle rather than malleable, because sliding one plane of the
lattice across another brings like charges face to face, and they conduct electricity only
once molten or dissolved, when the ions are free to move.

## Covalent bonding

In a covalent bond two atoms share a pair of electrons instead of transferring them. G. N.
Lewis set out the idea in 1916, drawing the shared pair as a line or a pair of dots and
noting the tendency of light atoms to complete an outer set of eight electrons.[^lewis1916]
Shared pairs are directional, so covalent substances have definite shapes: water's two O–H
bonds meet at about 104.5 degrees, methane's four C–H bonds point at the corners of a
tetrahedron 109.5 degrees apart. Atoms may share more than one pair, giving the double bond
of oxygen and the triple bond of nitrogen, each shorter and stronger than the single bond it
replaces.

Sharing is rarely equal. Linus Pauling's electronegativity scale ranks how strongly an atom
pulls on shared electrons, running from about 0.8 for caesium to 3.98 for fluorine; oxygen
scores 3.44 against hydrogen's 2.20.[^pauling1960] A difference of that size leaves the bond
polar, with partial negative charge on the more electronegative atom, and a large enough
difference amounts to the outright transfer that defines an ionic bond. Ionic and covalent
bonding are therefore two ends of a single continuum rather than separate phenomena.

The physical account of why a shared pair binds at all came from
[[Quantum mechanics|quantum mechanics]]. Walter Heitler and Fritz London treated the
hydrogen molecule in 1927, and the two frameworks that grew out of that work — valence bond
theory, with its hybridised atomic orbitals, and molecular orbital theory, with electrons
spread over the whole molecule — remain the standard tools for predicting geometry and
reactivity.

## Metallic bonding

In a metal the outermost electrons belong to no particular atom. They occupy states that
extend through the whole crystal, leaving an array of positive ion cores immersed in a mobile
electron sea. That arrangement accounts for the familiar properties: mobile electrons carry
current and heat, they absorb and re-emit light across the visible range to give metallic
lustre, and because the bonding is not directional, planes of atoms can slip past one another
without the structure coming apart. It is why copper can be drawn into wire while a salt
crystal shatters.

## Hydrogen bonds and weaker forces

Molecules attract one another as well. The strongest of these interactions is the hydrogen
bond, defined by IUPAC as an attraction between a hydrogen atom already bonded to an
electronegative atom and a nearby electron-rich site.[^iupac] Individually they are weak —
around 20 kilojoules per mole in water, against 463 for the O–H covalent bond — but there
are a great many of them, and collectively they keep water liquid at temperatures where
comparable molecules are gases.

Hydrogen bonds also carry heredity. In [[Deoxyribonucleic acid|DNA]], adenine pairs with
thymine across two hydrogen bonds and guanine with cytosine across three, the arrangement
James Watson and Francis Crick proposed in 1953.[^watsoncrick] Each pair is weak enough for
the strands to be unzipped and read, while a helix millions of base pairs long is held
together securely. Weaker still are London dispersion forces, which arise from momentary
fluctuations in the distribution of electrons; they are what lets the sheets of graphite
slide over one another and what holds candle wax solid.

## Bond energies in practice

Because bonds store energy, the heat of any reaction is the difference between the bonds
broken and the bonds formed. [[Combustion]] releases heat because the bonds in carbon dioxide
and water are collectively stronger than the carbon–hydrogen, carbon–carbon and
oxygen–oxygen bonds consumed.[^nist] Tabulated bond energies therefore allow a reaction's
heat to be estimated before it is run, and the same tables explain why some compounds are
stable enough to mine and others cannot be kept in a bottle.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Chemical bond",
            "subtitle": "Attraction holding atoms in a stable arrangement",
            "rows": [
                {
                    "kind": "header",
                    "value": "Principal types",
                },
                {
                    "kind": "row",
                    "label": "Ionic",
                    "value": "Electrostatic attraction between oppositely charged ions",
                },
                {
                    "kind": "row",
                    "label": "Covalent",
                    "value": "An electron pair shared between two atoms",
                },
                {
                    "kind": "row",
                    "label": "Metallic",
                    "value": "Positive ion cores in a sea of delocalised electrons",
                },
                {
                    "kind": "row",
                    "label": "Hydrogen bond",
                    "value": "Attraction between a polarised hydrogen and an electron-rich site",
                },
                {
                    "kind": "header",
                    "value": "Representative strengths",
                },
                {
                    "kind": "row",
                    "label": "H–H covalent bond",
                    "value": "436 kJ per mole",
                },
                {
                    "kind": "row",
                    "label": "Nitrogen triple bond",
                    "value": "945 kJ per mole",
                },
                {
                    "kind": "row",
                    "label": "Sodium chloride lattice",
                    "value": "787 kJ per mole",
                },
                {
                    "kind": "row",
                    "label": "Hydrogen bond in water",
                    "value": "about 20 kJ per mole",
                },
                {
                    "kind": "header",
                    "value": "Key ideas",
                },
                {
                    "kind": "row",
                    "label": "Shared electron pair",
                    "value": "G. N. Lewis, 1916",
                },
                {
                    "kind": "row",
                    "label": "Electronegativity scale",
                    "value": "Linus Pauling; fluorine 3.98, oxygen 3.44, hydrogen 2.20",
                },
                {
                    "kind": "row",
                    "label": "Quantum treatment",
                    "value": "Heitler and London on the hydrogen molecule, 1927",
                },
                {
                    "kind": "full",
                    "value": "Bond lengths and strengths are measured by spectroscopy, "
                    "calorimetry and diffraction, and tabulated in thermochemical databases.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "lewis1916",
                "title": "The Atom and the Molecule",
                "url": "https://pubs.acs.org/doi/10.1021/ja02261a002",
                "authors": "Gilbert N. Lewis",
                "publisher": "Journal of the American Chemical Society 38 (4): 762–785",
                "published_on": "1916",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1021/ja02261a002",
                "quote": "",
            },
            {
                "key": "pauling1960",
                "title": "The Nature of the Chemical Bond and the Structure of Molecules and Crystals",
                "url": "https://cornellpress.cornell.edu/book/9780801403330/the-nature-of-the-chemical-bond/",
                "authors": "Linus Pauling",
                "publisher": "Cornell University Press, 3rd edition",
                "published_on": "1960",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-8014-0333-0",
                "quote": "",
            },
            {
                "key": "iupac",
                "title": "Definition of the hydrogen bond (IUPAC Recommendations 2011)",
                "url": "https://publications.iupac.org/pac/pdf/2011/pdf/8308x1637.pdf",
                "authors": "E. Arunan, G. R. Desiraju, R. A. Klein and others",
                "publisher": "Pure and Applied Chemistry 83 (8): 1637–1641",
                "published_on": "2011",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1351/PAC-REC-10-01-02",
                "quote": "",
            },
            {
                "key": "watsoncrick",
                "title": "Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid",
                "url": "https://www.nature.com/articles/171737a0",
                "authors": "James D. Watson, Francis H. C. Crick",
                "publisher": "Nature 171: 737–738",
                "published_on": "25 April 1953",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/171737a0",
                "quote": "",
            },
            {
                "key": "nist",
                "title": "NIST Chemistry WebBook, NIST Standard Reference Database Number 69",
                "url": "https://webbook.nist.gov/chemistry/",
                "authors": "P. J. Linstrom, W. G. Mallard (editors)",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2025",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.18434/T4D303",
                "quote": "",
            },
            {
                "key": "britannica",
                "title": "Chemical bonding",
                "url": "https://www.britannica.com/science/chemical-bonding",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Atomic theory",
            "The periodic table",
            "Quantum mechanics",
            "Water",
            "Deoxyribonucleic acid",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["bonding", "molecular structure", "electronegativity", "physical chemistry"],
    },
    {
        "title": "Water",
        "category": "Chemistry and Materials",
        "categories": ["Earth and Environment"],
        "short_description": "The compound H2O, and the anomalies that set it apart from other liquids",
        "summary": (
            "Water is a compound of two hydrogen atoms and one oxygen atom whose hydrogen "
            "bonding gives it a long list of anomalous properties, among them ice that "
            "floats, an unusually high heat capacity and exceptional solvent power."
        ),
        "content": """**Water** is the chemical compound H2O, a molecule of two hydrogen atoms bonded to
a single oxygen atom, and the only common substance that occurs naturally as solid, liquid
and gas within the range of temperatures found at Earth's surface. It is abundant and
chemically simple, yet nearly every one of its physical properties is anomalous when set
beside molecules of comparable size, and almost all of those anomalies trace back to one
feature: hydrogen bonding.

## The molecule

Each oxygen–hydrogen bond is about 96 picometres long, and the two meet at an angle close to
104.5 degrees — narrower than the 109.5 degrees of a regular tetrahedron, because the two
non-bonding electron pairs on the oxygen atom take up more room than the bonding pairs
do.[^britannica] Oxygen is considerably more electronegative than hydrogen, so each
[[Chemical bond|bond]] is polar, and because the molecule is bent rather than straight the
two bond dipoles do not cancel: the molecule carries a permanent dipole moment of about 1.85
debye. Its relative molecular mass of 18.02 makes water one of the lightest substances that
is liquid at room temperature. Hydrogen sulfide, built to the same pattern but almost twice
as heavy, boils at about −60 °C; water boils at 100 °C.

## Hydrogen bonding

Water has two hydrogen atoms to donate and two lone pairs to accept, so one molecule can
hydrogen bond to as many as four neighbours at once. IUPAC defines such a bond as an
attraction between a hydrogen atom already bonded to an electronegative atom and an
electron-rich region on another molecule.[^iupac] In ordinary hexagonal ice every molecule
takes up all four links, producing an open tetrahedral framework with conspicuous empty
space in it. In the liquid the network survives but is continually breaking and re-forming,
individual bonds lasting only picoseconds. Each is worth roughly 20 kilojoules per mole,
about a twentieth of the covalent O–H bond, but there are enough of them that the network
dominates water's behaviour.

## Anomalous properties

The energy stored in that network appears as unusually large thermal quantities. Water's
specific heat capacity is about 4.18 joules per gram per kelvin, higher than almost any other
liquid, so the oceans take up and give back enormous amounts of heat for small changes of
temperature. Melting ice absorbs 6.01 kilojoules per mole and boiling water 40.65, the latter
equivalent to roughly 2,257 joules for every gram vaporised.[^nist] That last figure is what
makes evaporation such an effective coolant, and it makes [[The water cycle|the water cycle]]
the largest single mover of energy through the atmosphere.

Water also contracts as it cools only down to 3.98 °C; below that it expands again, so its
density peaks just under 1,000 kilograms per cubic metre at that temperature. Ice is about
nine per cent less dense still, close to 917 kilograms per cubic metre, and therefore floats.
A freezing lake consequently develops a lid of ice while the water beneath stays liquid,
which is why freshwater life survives winters at all and why it survived the repeated
advances of each [[Ice age|glaciation]].

Surface tension is about 72 millinewtons per metre at 25 °C, exceptional among liquids that
are not molten metals. Combined with water's strong adhesion to cellulose, it allows
continuous columns of sap to be pulled through the conducting vessels of trees to heights of
more than a hundred metres, under tension rather than pressure.

## Solvent behaviour

A relative permittivity of roughly 78 at 25 °C means water screens electric charge very
effectively, which is why it dissolves ionic solids that few other liquids will touch: a
crystal of [[Salt|sodium chloride]] disperses because each freed ion acquires a shell of
oriented water molecules whose attraction repays the energy of the lattice it left. Water is
a poor solvent for non-polar substances, and that failure matters as much biologically as its
successes, because it is what drives lipids to assemble into the membranes that enclose every
[[The cell|cell]]. Water also reacts slightly with itself, roughly one molecule in five
hundred million donating a proton to another; the resulting balance of hydronium and
hydroxide ions fixes the neutral point of the pH scale at 7 at 25 °C.

## Phases

At the triple point, 273.16 kelvin and 611.657 pascals, ice, liquid and vapour coexist. From
1954 until the revision of the SI base units in 2019 that single point defined the kelvin
exactly; the unit is now fixed instead by assigning an exact value to the Boltzmann
constant.[^bipm] Under pressure the phase diagram becomes elaborate. Around twenty
crystalline forms of ice have been characterised, most of them stable only at pressures far
beyond anything found at the Earth's surface, and new phases are still being reported.[^ice]

## Water on Earth

Water covers about 71 per cent of the planet's surface. The oceans hold some 96.5 per cent of
it; of the 2.5 per cent that is fresh, most is locked in ice sheets and glaciers or held
underground, leaving a small remainder in lakes, rivers, soil and the air.[^usgs] It is a
reactant as well as a medium: in [[Photosynthesis|photosynthesis]] water molecules are split
and their oxygen released as O2, the source of practically all the free oxygen in the
atmosphere. Dissolved carbonate chemistry decides whether a [[Coral reef|coral reef]] can
build limestone faster than the sea removes it. Human settlement has been shaped by the
same properties: [[Venice]] stands on millions of wooden piles driven into a lagoon,
preserved for centuries precisely because timber submerged in oxygen-poor water does not rot.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Water",
            "subtitle": "Chemical compound H2O",
            "rows": [
                {
                    "kind": "header",
                    "value": "Molecule",
                },
                {
                    "kind": "row",
                    "label": "Formula",
                    "value": "H2O",
                },
                {
                    "kind": "row",
                    "label": "Relative molecular mass",
                    "value": "18.02",
                },
                {
                    "kind": "row",
                    "label": "Bond length",
                    "value": "about 96 picometres (O–H)",
                },
                {
                    "kind": "row",
                    "label": "Bond angle",
                    "value": "about 104.5 degrees (H–O–H)",
                },
                {
                    "kind": "header",
                    "value": "Physical properties",
                },
                {
                    "kind": "row",
                    "label": "Melting point",
                    "value": "0 °C at 1 atmosphere",
                },
                {
                    "kind": "row",
                    "label": "Boiling point",
                    "value": "100 °C at 1 atmosphere",
                },
                {
                    "kind": "row",
                    "label": "Density maximum",
                    "value": "just under 1,000 kg per cubic metre at 3.98 °C",
                },
                {
                    "kind": "row",
                    "label": "Density of ice",
                    "value": "about 917 kg per cubic metre at 0 °C",
                },
                {
                    "kind": "row",
                    "label": "Specific heat capacity",
                    "value": "about 4.18 J per gram per kelvin at 25 °C",
                },
                {
                    "kind": "row",
                    "label": "Enthalpy of vaporisation",
                    "value": "40.65 kJ per mole at 100 °C",
                },
                {
                    "kind": "row",
                    "label": "Surface tension",
                    "value": "about 72 millinewtons per metre at 25 °C",
                },
                {
                    "kind": "row",
                    "label": "Triple point",
                    "value": "273.16 kelvin at 611.657 pascals",
                },
                {
                    "kind": "full",
                    "value": "Water covers about 71 per cent of Earth's surface, and about "
                    "96.5 per cent of all of it is held in the oceans.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "nist",
                "title": "NIST Chemistry WebBook, NIST Standard Reference Database Number 69",
                "url": "https://webbook.nist.gov/chemistry/",
                "authors": "P. J. Linstrom, W. G. Mallard (editors)",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2025",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.18434/T4D303",
                "quote": "",
            },
            {
                "key": "iupac",
                "title": "Definition of the hydrogen bond (IUPAC Recommendations 2011)",
                "url": "https://publications.iupac.org/pac/pdf/2011/pdf/8308x1637.pdf",
                "authors": "E. Arunan, G. R. Desiraju, R. A. Klein and others",
                "publisher": "Pure and Applied Chemistry 83 (8): 1637–1641",
                "published_on": "2011",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1351/PAC-REC-10-01-02",
                "quote": "",
            },
            {
                "key": "usgs",
                "title": "How Much Water is There on Earth?",
                "url": "https://www.usgs.gov/water-science-school/science/how-much-water-there-earth",
                "authors": "",
                "publisher": "U.S. Geological Survey, Water Science School",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "ice",
                "title": "The everlasting hunt for new ice phases",
                "url": "https://www.nature.com/articles/s41467-021-23403-6",
                "authors": "Thomas C. Hansen",
                "publisher": "Nature Communications 12: 3161",
                "published_on": "2021",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/s41467-021-23403-6",
                "quote": "",
            },
            {
                "key": "bipm",
                "title": "The International System of Units (SI), 9th edition",
                "url": "https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf",
                "authors": "",
                "publisher": "Bureau International des Poids et Mesures",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica",
                "title": "Water",
                "url": "https://www.britannica.com/science/water",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Chemical bond",
            "The water cycle",
            "Photosynthesis",
            "Ice age",
            "The cell",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["hydrogen bonding", "phases of matter", "solvents", "physical chemistry"],
    },
    {
        "title": "Combustion",
        "category": "Chemistry and Materials",
        "categories": ["Engineering and Technology"],
        "short_description": "The rapid oxidation reaction that produces flame, heat and light",
        "summary": (
            "Combustion is a rapid, self-sustaining oxidation reaction that releases heat and "
            "usually light. Lavoisier's demonstration in the 1770s that burning consumes part "
            "of the air displaced the phlogiston theory and founded modern chemistry."
        ),
        "content": """**Combustion** is a rapid, self-sustaining oxidation reaction in which a fuel
combines with an oxidant — in almost every practical case the oxygen of the air — releasing
heat and, in a flame, light. Complete combustion of a hydrocarbon yields carbon dioxide and
water: one mole of methane burning as CH4 + 2 O2 → CO2 + 2 H2O gives up about 890
kilojoules.[^nist] The energy comes from the [[Chemical bond|chemical bonds]] involved, since
those formed in the products are collectively stronger than those broken in the fuel and in
the oxygen.

## From phlogiston to oxygen

For most of the eighteenth century burning was explained by phlogiston, a fiery principle
supposed to reside in combustible bodies and to escape when they burned, leaving ash as the
residue.[^phlogiston] The theory, sketched by Johann Joachim Becher in the 1660s and
systematised by Georg Ernst Stahl, was coherent and productive, but it could not explain why
a metal heated in air grew heavier rather than lighter.

Antoine Lavoisier settled the question by weighing. In the spring of 1774 he calcined tin and
lead in sealed vessels and found the total mass unchanged: the metal's gain matched the air's
loss, and only about a fifth of the air took any part. Joseph Priestley isolated that active
component in August 1774 and described it to Lavoisier's circle; Lavoisier recognised it as
exactly what his account required, named it oxygène, and in 1783 read "Réflexions sur le
phlogistique" to the Académie royale des sciences as a direct attack on the older theory. His
Traité élémentaire de chimie of 1789 presented the new chemistry together with a table of
simple substances.[^lavoisier] Lavoisier also identified animal respiration as a slow
combustion. He was guillotined in 1794, at fifty.

The oxygen theory marks the point at which chemistry separated decisively from
[[Alchemy|alchemical]] practice, and its insistence on the balance sheet supplied the weights
and ratios that [[The periodic table|the periodic table]] would later organise.

## Flames

A flame is the luminous region in which gas-phase reaction is actually taking place, and
flames fall into two families. In a premixed flame — a Bunsen burner or a gas hob — fuel and
air are combined before ignition, and the reaction front is thin, stable and nearly
colourless. In a diffusion flame — a candle, an oil lamp, a wood fire — fuel and oxidant meet
only where they interdiffuse, and the flame is that boundary.

A candle illustrates the second type completely. Heat from the flame melts the wax, capillary
action draws the liquid up the wick, further heat vaporises it and breaks it into smaller
fragments, and those burn in a thin envelope where they meet incoming air. Michael Faraday
built six Christmas lectures at the Royal Institution around precisely this sequence,
published as The Chemical History of a Candle.[^faraday] The blue at a flame's base is
emission from excited CH and C2 fragments; the yellow above it is thermal radiation from soot
particles hot enough to glow, which is why a sooty flame is bright and a clean one is not. A
stoichiometric methane–air flame reaches roughly 2,000 °C, and the same fuel burned in pure
oxygen runs several hundred degrees hotter, which is what allows an oxy-fuel torch to cut
steel.

## Ignition, chains and limits

Combustion is not one reaction but a branching chain of hundreds, carried by short-lived
radicals: hydrogen and oxygen atoms, hydroxyl, and fragments of the fuel. Chain-branching
steps, such as a hydrogen atom reacting with molecular oxygen to give hydroxyl and an oxygen
atom, turn one radical into two, so the reaction rate can climb explosively once it begins.
Nikolay Semenov and Cyril Hinshelwood established this picture in the 1920s and 1930s and
shared the 1956 Nobel Prize in Chemistry for it.[^nobel]

Because the chain has to outrun its own losses, combustion has limits. A methane–air mixture
will not carry a flame below about 5 per cent or above about 15 per cent methane by volume:
too lean and there is not enough fuel, too rich and not enough oxygen. Fire control follows
the same logic, summarised as the fire triangle of fuel, oxidant and heat — water removes
heat, a blanket removes the oxidant, and certain gaseous agents work instead by scavenging
the radicals that carry the chain.

## Incomplete combustion

Where oxygen is short or mixing poor, carbon leaves the flame only part-oxidised. The
products include soot, unburnt hydrocarbons and carbon monoxide, which binds to haemoglobin
far more tightly than oxygen does and is the principal hazard of fuel-burning appliances
indoors. At the other extreme, very hot flames oxidise the nitrogen of the air itself to
nitric oxide and nitrogen dioxide, the thermal route to the nitrogen oxides behind
photochemical smog.

## Fire, furnaces and engines

Controlled burning is older than the species: burnt bone and ashed plant material in the
Acheulean layers of Wonderwerk Cave in South Africa have been dated to roughly a million
years ago.[^berna] Smelting exploits combustion twice over, because charcoal or coke supplies
both the heat and, as carbon monoxide, the reducing agent that strips oxygen from iron ore.
Abraham Darby's success in smelting with coke at Coalbrookdale in 1709 released English
ironmaking from a dwindling supply of charcoal.

Combustion in a boiler drove the [[Steam engine|steam engine]], where the fire stays outside
the working fluid; the internal combustion engine moved it into the cylinder. Either way, the
fraction of released heat that can be turned into work is capped not by the chemistry but by
[[Thermodynamics|thermodynamics]], through the efficiency limit that binds every
[[Heat engine|heat engine]]. Cheap heat on that scale is what made
[[The Industrial Revolution|the Industrial Revolution]] possible, and its residue is now the
dominant human input to [[The carbon cycle|the carbon cycle]]: fossil fuels and cement
production released about 37.4 billion tonnes of carbon dioxide in 2024, and the atmospheric
concentration reached about 422.5 parts per million, some 52 per cent above its pre-industrial
level.[^gcb]
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Combustion",
            "subtitle": "Exothermic oxidation of a fuel",
            "rows": [
                {
                    "kind": "header",
                    "value": "The reaction",
                },
                {
                    "kind": "row",
                    "label": "Type",
                    "value": "Rapid, self-sustaining oxidation carried by radical chains",
                },
                {
                    "kind": "row",
                    "label": "Usual oxidant",
                    "value": "Atmospheric oxygen, about 21 per cent of air by volume",
                },
                {
                    "kind": "row",
                    "label": "Complete products",
                    "value": "Carbon dioxide and water vapour",
                },
                {
                    "kind": "row",
                    "label": "Incomplete products",
                    "value": "Soot, carbon monoxide, unburnt hydrocarbons",
                },
                {
                    "kind": "header",
                    "value": "Representative figures",
                },
                {
                    "kind": "row",
                    "label": "Methane combustion",
                    "value": "CH4 + 2 O2 → CO2 + 2 H2O, about 890 kJ per mole",
                },
                {
                    "kind": "row",
                    "label": "Methane–air flame",
                    "value": "roughly 2,000 °C at a stoichiometric mixture",
                },
                {
                    "kind": "row",
                    "label": "Flammable range",
                    "value": "about 5 to 15 per cent methane by volume in air",
                },
                {
                    "kind": "header",
                    "value": "History",
                },
                {
                    "kind": "row",
                    "label": "Phlogiston theory",
                    "value": "Johann Joachim Becher and Georg Ernst Stahl",
                },
                {
                    "kind": "row",
                    "label": "Oxygen theory",
                    "value": "Antoine Lavoisier, 1774 to 1789",
                },
                {
                    "kind": "row",
                    "label": "Chain mechanism",
                    "value": "Semenov and Hinshelwood, Nobel Prize in Chemistry 1956",
                },
                {
                    "kind": "full",
                    "value": "Flames are classed as premixed, where fuel and oxidant are "
                    "mixed before ignition, or diffusion, where they meet only at the "
                    "reacting surface.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "lavoisier",
                "title": "Antoine Lavoisier: Oxygen theory of combustion",
                "url": "https://www.britannica.com/biography/Antoine-Lavoisier/Oxygen-theory-of-combustion",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "phlogiston",
                "title": "Phlogiston",
                "url": "https://www.britannica.com/science/phlogiston",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "faraday",
                "title": "The Chemical History of a Candle",
                "url": "https://www.gutenberg.org/ebooks/14474",
                "authors": "Michael Faraday",
                "publisher": "Project Gutenberg",
                "published_on": "1861",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nobel",
                "title": "The Nobel Prize in Chemistry 1956",
                "url": "https://www.nobelprize.org/prizes/chemistry/1956/summary/",
                "authors": "",
                "publisher": "The Nobel Foundation",
                "published_on": "1956",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "for their researches into the mechanism of chemical reactions",
            },
            {
                "key": "berna",
                "title": "Microstratigraphic evidence of in situ fire in the Acheulean strata of Wonderwerk Cave",
                "url": "https://www.pnas.org/doi/10.1073/pnas.1117620109",
                "authors": "Francesco Berna, Paul Goldberg, Liora Kolska Horwitz and others",
                "publisher": "Proceedings of the National Academy of Sciences 109 (20): E1215–E1220",
                "published_on": "2012",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1073/pnas.1117620109",
                "quote": "",
            },
            {
                "key": "gcb",
                "title": "Global Carbon Budget 2024",
                "url": "https://essd.copernicus.org/articles/17/965/2025/",
                "authors": "Pierre Friedlingstein, Michael O'Sullivan, Matthew W. Jones and others",
                "publisher": "Earth System Science Data 17: 965–1039",
                "published_on": "2025",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.5194/essd-17-965-2025",
                "quote": "",
            },
            {
                "key": "nist",
                "title": "NIST Chemistry WebBook, NIST Standard Reference Database Number 69",
                "url": "https://webbook.nist.gov/chemistry/",
                "authors": "P. J. Linstrom, W. G. Mallard (editors)",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2025",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.18434/T4D303",
                "quote": "",
            },
        ],
        "see_also": [
            "Thermodynamics",
            "Heat engine",
            "The carbon cycle",
            "Alchemy",
            "Steam engine",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["oxidation", "fire", "flame chemistry", "history of chemistry"],
    },
]
