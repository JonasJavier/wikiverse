"""Physics — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Thermodynamics",
        "category": "Physics",
        "categories": ["Engineering and Technology"],
        "short_description": "The physics of heat, work and the direction in which processes run",
        "summary": (
            "Thermodynamics relates heat, work, temperature and energy in matter treated in "
            "bulk. Its four laws set the accounting rules for energy and fix the direction of "
            "spontaneous change, constraining engines, reactions, cells and stars alike."
        ),
        "content": """**Thermodynamics** is the branch of physics that relates heat, work, temperature and
energy in matter treated in bulk, and that fixes the direction in which physical and chemical
processes run. Its results follow from four laws stated without reference to atoms, which is why
the same reasoning constrains a steam cylinder, a chemical reaction, a bacterium and a star. It was
assembled in the nineteenth century around practical questions about
[[Steam engine|steam engines]], fuel and muscular work; the explanation of why its laws hold
arrived afterwards, in statistical mechanics.

## Systems, states and equilibrium

An analysis begins by drawing a boundary: the system inside, the surroundings outside, and a
boundary that may or may not let matter and energy through. The system's condition is given by
state variables — pressure, volume, temperature, internal energy, [[Entropy|entropy]] — which
belong to the state itself, so a change in any of them is independent of the route taken. Heat and
work are different in kind: they are quantities transferred along a particular path, which is why
a cycle can return a gas to its starting pressure and volume and still leave net work behind. The
classical results concern equilibrium states and the reversible idealisation — a process slow
enough to be run backwards through the same states — which no real machine achieves but which
marks the limit of the possible.

## The four laws

The **zeroth law** states that thermal equilibrium is transitive: if two bodies are each in
equilibrium with a third, they are in equilibrium with each other. Trivial as it sounds, this is
what makes temperature a single-valued property of a state and thermometry possible. It was
numbered last, after the other three were in use.

The **first law** extends the conservation of energy to include heat, writing the change in a
system's internal energy as the heat added minus the work done. Its experimental basis was the
mechanical equivalent of heat: Julius Robert von Mayer argued for a fixed conversion factor in
1842, and James Prescott Joule measured one in the 1840s by stirring water with a paddle wheel
driven by falling weights, coming within about one per cent of the modern 4.184 joules per
calorie. Any machine that delivers work from nothing violates this law.

The **second law** forbids much of what the first law permits. Rudolf Clausius put it as the
impossibility of heat passing spontaneously from a colder body to a hotter one with no other
change; William Thomson, later Lord Kelvin, put it as the impossibility of a cyclic engine whose
only effect is to turn heat from one reservoir entirely into work. Clausius's restatement of 1865
introduced entropy, a state function whose change along a reversible step is the heat absorbed
divided by the absolute temperature, and the law then reads: the entropy of an isolated system
never decreases.[^clausius1865]

The **third law**, formulated by Walther Nernst in 1906, says that the entropy of a system
approaches a constant as its temperature approaches absolute zero, and that the constant is zero
for a perfect crystal. One consequence is that absolute zero cannot be reached in any finite
number of steps, though cold-atom laboratories now work routinely at a few billionths of a
kelvin.

## Engines and the efficiency ceiling

The founding document of the subject is Sadi Carnot's essay of 1824 on the motive power of fire,
written when the steam engine was transforming industry and its theory did not exist. Carnot argued
that the work obtainable depends on the temperature difference across which heat falls and not on
the working substance, and that the best conceivable engine is a reversible one.[^carnot1824]
Restated with the absolute temperature scale Kelvin proposed in 1848, that gives the ceiling on
every [[Heat engine|heat engine]]: one minus the ratio of sink temperature to source temperature. A
plant taking steam at 600 °C and rejecting heat at 27 °C cannot exceed about 66 per cent however it
is built.[^feynman1963]

The practical gap was enormous, and so was the money in closing it. Thomas Newcomen's atmospheric
engines of the early eighteenth century turned well under one per cent of their fuel's energy into
work, while the best modern combined-cycle gas plants exceed 60 per cent. Because such machines
almost always obtain their temperature difference by [[Combustion|burning fuel]], the ceiling also
fixes the carbon released per unit of useful work. The mines and mills of
[[The Industrial Revolution|the industrial era]] supplied the problems, and thermodynamics told
engineers which improvements were forbidden outright.

## The statistical foundation

Classical thermodynamics says nothing about atoms, and its laws were established without them.
Statistical mechanics, built by James Clerk Maxwell, Ludwig Boltzmann and Josiah Willard Gibbs
between the 1860s and the 1900s, supplied the missing account: a macroscopic state corresponds to
an enormous number of microscopic arrangements, and entropy measures how many. On that reading the
second law is a statement of overwhelming likelihood rather than logical necessity, which is why
the subject is inseparable from [[Probability theory|probability]] and why measurable departures
appear in systems of a few molecules watched over milliseconds.[^wang2002][^sepstatmech] The link
is built into the unit system: since 2019 the kelvin has been defined by fixing the Boltzmann
constant at exactly 1.380649 × 10⁻²³ joules per kelvin.[^si2019][^nistk] Because entropy also
measures missing information, the same mathematics reappears in
[[Information theory|information theory]], counting bits instead of joules per kelvin.

## Free energy, chemistry and biology

Most laboratory and biological processes occur at constant temperature and pressure rather than in
isolation, and for these the governing quantity is the Gibbs free energy: enthalpy minus temperature
times entropy. A process runs spontaneously when it lowers the free energy, so a reaction may absorb
heat and still proceed if it generates enough entropy. The same differences set equilibrium
constants, cell voltages and the direction of metabolic reactions.

## Reach and limits

The framework has been extended to magnetic materials, to radiation, to electrochemistry and,
unexpectedly, to gravitation, where the event horizon of a black hole carries both entropy and a
temperature. Its silences matter too: it says nothing about rates, so a reaction can be favourable
and immeasurably slow, and its classical form assumes equilibrium, so steady flows, living cells and
weather need the machinery of non-equilibrium thermodynamics built by Lars Onsager and others. The
reasoning can also outrun its evidence: Kelvin, calculating how long the Earth would take to cool,
put its age at between 20 and 400 million years in 1862, and the thermodynamics was sound while the
answer was badly wrong, because radioactive heating inside the planet had not yet been discovered.
""",
        "tier": "standard",
        "kind": "discipline",
        "infobox": {
            "title": "Thermodynamics",
            "subtitle": "Branch of physics",
            "rows": [
                {"kind": "header", "value": "The four laws"},
                {
                    "kind": "row",
                    "label": "Zeroth",
                    "value": "Thermal equilibrium is transitive, so temperature is well defined",
                },
                {
                    "kind": "row",
                    "label": "First",
                    "value": "Energy is conserved once heat is counted as a form of transfer",
                },
                {
                    "kind": "row",
                    "label": "Second",
                    "value": "The entropy of an isolated system never decreases",
                },
                {
                    "kind": "row",
                    "label": "Third",
                    "value": "Entropy tends to a constant as temperature tends to absolute zero",
                },
                {"kind": "header", "value": "Quantities"},
                {
                    "kind": "row",
                    "label": "State functions",
                    "value": "Internal energy, [[Entropy|entropy]], enthalpy, free energy",
                },
                {"kind": "row", "label": "Path quantities", "value": "Heat and work"},
                {
                    "kind": "row",
                    "label": "Defining constant",
                    "value": "Boltzmann constant, exactly 1.380649 × 10⁻²³ J/K",
                },
                {"kind": "header", "value": "Formative work"},
                {
                    "kind": "row",
                    "label": "Classical",
                    "value": "Carnot (1824), Kelvin (1848), Clausius (1850, 1865), Nernst (1906)",
                },
                {
                    "kind": "row",
                    "label": "Statistical",
                    "value": "Maxwell, Boltzmann and Gibbs, 1860s to 1900s",
                },
                {
                    "kind": "full",
                    "value": "No engine working between two temperatures can beat the efficiency "
                    "of a reversible one operating between the same two.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "carnot1824",
                "title": "Reflections on the Motive Power of Heat",
                "url": "https://en.wikisource.org/wiki/Reflections_on_the_Motive_Power_of_Heat",
                "authors": "Sadi Carnot, translated by Robert H. Thurston",
                "publisher": "Wikisource (from the Thurston translation)",
                "published_on": "1824",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "The motive power of heat is independent of the agents employed to "
                "realize it",
            },
            {
                "key": "clausius1865",
                "title": "Ueber verschiedene für die Anwendung bequeme Formen der "
                "Hauptgleichungen der mechanischen Wärmetheorie",
                "url": "https://doi.org/10.1002/andp.18652010702",
                "authors": "Rudolf Clausius",
                "publisher": "Annalen der Physik",
                "published_on": "1865",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1002/andp.18652010702",
                "quote": "Die Entropie der Welt strebt einem Maximum zu.",
            },
            {
                "key": "feynman1963",
                "title": "The Feynman Lectures on Physics, Volume I, Chapter 44: The Laws of "
                "Thermodynamics",
                "url": "https://www.feynmanlectures.caltech.edu/I_44.html",
                "authors": "Richard P. Feynman, Robert B. Leighton and Matthew Sands",
                "publisher": "California Institute of Technology",
                "published_on": "1963",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "wang2002",
                "title": "Experimental Demonstration of Violations of the Second Law of "
                "Thermodynamics for Small Systems and Short Time Scales",
                "url": "https://doi.org/10.1103/PhysRevLett.89.050601",
                "authors": "G. M. Wang, E. M. Sevick, E. Mittag, D. J. Searles and D. J. Evans",
                "publisher": "Physical Review Letters 89, 050601",
                "published_on": "2002",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevLett.89.050601",
                "quote": "",
            },
            {
                "key": "sepstatmech",
                "title": "Philosophy of Statistical Mechanics",
                "url": "https://plato.stanford.edu/entries/statphys-statmech/",
                "authors": "",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2023",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "si2019",
                "title": "The International System of Units (SI), 9th edition",
                "url": "https://www.bipm.org/en/publications/si-brochure",
                "authors": "",
                "publisher": "Bureau International des Poids et Mesures",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nistk",
                "title": "Boltzmann constant: CODATA recommended value",
                "url": "https://physics.nist.gov/cgi-bin/cuu/Value?k",
                "authors": "",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2022 CODATA adjustment",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Entropy",
            "Heat engine",
            "Steam engine",
            "Combustion",
            "Information theory",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["thermodynamics", "heat", "energy", "statistical mechanics"],
    },
    {
        "title": "Entropy",
        "category": "Physics",
        "categories": ["Computing and Information"],
        "short_description": "A count of microscopic arrangements that gives change a direction",
        "summary": (
            "Entropy measures how many microscopic arrangements are consistent with a system's "
            "observable state. It is the quantity that never decreases in an isolated system, "
            "Boltzmann's count of microstates, and Shannon's measure of missing information."
        ),
        "content": """**Entropy** is a measure of how many microscopic arrangements are consistent with what
can be observed about a system, and equivalently of how much of a system's energy is unavailable
for doing work. It was introduced in 1865 as a bookkeeping device for the waste heat of engines,
given a microscopic meaning in the 1870s as a count of molecular arrangements, and carried over
in 1948 into [[Information theory|information theory]] as a measure of uncertainty. These are
not three analogies but one quantity expressed in different units: joules per kelvin in
thermodynamics, bits in communication. Because entropy is the one familiar quantity with a
built-in direction of increase, it also underwrites the physical distinction between past and
future.

## Thermodynamic entropy

Rudolf Clausius introduced entropy to make precise something the older theory of heat could only
gesture at, namely that energy transferred as heat is progressively degraded. Along a reversible
step the change in entropy equals the heat absorbed divided by the absolute temperature at which
it is absorbed; for any real, irreversible process the change is larger than that. Clausius took
the word from the Greek for transformation and shaped it deliberately to echo *energy*, and he
closed his 1865 paper with a pair of claims: the energy of the universe is constant, and its
entropy tends towards a maximum.[^clausius1865]

Entropy in this sense is measured in joules per kelvin, is a property of a state rather than of
a process, and is extensive, so two litres of [[Water|water]] at a given temperature carry twice
the entropy of one. The numbers are ordinary. Melting a kilogram of ice at 0 °C absorbs about
334 kilojoules and therefore raises the entropy of the sample by roughly 1.2 kilojoules per
kelvin. Tabulated standard molar entropies show the same pattern from the other direction:
liquid water is listed near 70 joules per mole per kelvin at 25 °C and water vapour near 189,
because a molecule in a gas has vastly more ways of being arranged than one in a liquid.

## The second law

Three classical statements of the second law of [[Thermodynamics|thermodynamics]] turn out to be
equivalent. Clausius's version forbids heat from passing spontaneously from a colder to a hotter
body with no other change. The Kelvin–Planck version forbids a cyclic engine whose sole effect
is to convert heat from a single reservoir entirely into work. The entropy version states that
the total entropy of an isolated system never decreases, and strictly increases in any
irreversible process.

The practical consequence is a hard ceiling on every [[Heat engine|heat engine]]: none working
between two temperatures can exceed the efficiency of a reversible engine between the same two,
which is one minus their ratio. A [[Steam engine|steam plant]] with a 600 °C boiler and
near-ambient cooling water is capped near two thirds before a single real loss is
counted.[^feynman1963] The same law explains why no perpetual-motion machine of the second kind
has ever survived examination, and why patent offices treat such applications with standing
scepticism.

## Counting microstates

Ludwig Boltzmann supplied the microscopic reading in the 1870s: the entropy of a macroscopic
state is proportional to the number of microscopic configurations that realise it, with the
Boltzmann constant — 1.380649 × 10⁻²³ joules per kelvin — as the proportionality factor and a
logarithm to keep entropy additive.[^nistk] The
resulting formula, *S = k log W*, is carved on his gravestone in Vienna. Josiah Willard Gibbs
generalised it to cases where the configurations are not equally likely, giving an expression
that sums each probability multiplied by its own logarithm.

The counting makes the second law intuitive. Consider a box of gas with every molecule
momentarily in the left half. Nothing in the laws of motion forbids that arrangement; the
objection is arithmetic. For a sample of 10²² molecules the fraction of arrangements with this
property is two raised to the power of minus 10²², a number so small that no observation has
ever caught a gas doing it. What the second law says, on this reading, is that systems drift
towards macroscopic states with overwhelmingly more microscopic realisations and, having arrived,
stay. Two nineteenth-century objections — Loschmidt's, that reversing every molecular velocity
would reverse the process, and Zermelo's, that a finite system must eventually return
arbitrarily close to any earlier state — are both correct and both irrelevant at laboratory
scale, because the recurrence times involved dwarf the age of the universe. In genuinely small
systems the fluctuations are visible: a micron-sized bead dragged through water by optical
tweezers has been watched, over intervals of a fraction of a second, to take up heat and move
against the applied force, at rates matching the fluctuation theorems that generalise the second
law.[^wang2002] Entropy increase is therefore a statement about probability, not about logical
impossibility, which is why the subject leans on [[Probability theory|probability theory]] at
every step.

## Chemistry, life and open systems

At constant temperature and pressure the quantity that decides whether a change proceeds is the
Gibbs free energy, enthalpy minus temperature times entropy. A reaction may absorb heat and
still run, provided it generates enough entropy; conversely, a process may look tidy and still
be entropy-driven. Oil separates from water largely because water molecules forced to arrange
themselves around a non-polar surface are released when the oil droplets merge, and colloidal
spheres will crystallise into an ordered lattice for no reason other than that the ordered
arrangement leaves each sphere more room to rattle. Living things do not evade any of this. An
organism keeps its own entropy low by exporting more to its surroundings, and the planet as a
whole is not an isolated system: Earth receives energy as visible light from a 5,800 K surface
and returns it as infrared at around 255 K, radiating away roughly twenty times as much entropy
as arrives with it. [[Photosynthesis|Photosynthesis]] taps that one-way flow.

## Information entropy

Claude Shannon defined the entropy of a probability distribution in 1948 as the negative sum of
each probability times its logarithm, taking base two so that the unit is the bit.[^shannon1948]
A fair coin carries exactly one bit per toss, a biased coin less, a certain outcome none.
Shannon's source-coding theorem turns this into an engineering limit: no lossless compression
scheme can represent output from a source in fewer bits per symbol, on average, than the
source's entropy. Printed English, on his own later estimate, carries on the order of one bit
per letter once ordinary redundancy is taken into account, far below the 4.7 bits that 26
equiprobable letters would require.[^shannon1951] The shared name is not decoration: for a
distribution over microstates, Shannon's expression and Gibbs's differ only by the Boltzmann
constant. The choice of word is usually traced to a suggestion from John von Neumann, reported
second-hand many years later.

## Maxwell's demon and the cost of erasure

James Clerk Maxwell proposed in 1867 a creature small enough to watch individual molecules and
open a shutter only for the fast ones, apparently building a temperature difference from nothing.
Leó Szilárd sharpened the puzzle in 1929 with a single-molecule engine that seemed to convert
information into work. The resolution rests on Rolf Landauer's argument of 1961 that logically
irreversible operations carry a thermodynamic price: erasing one bit in surroundings at
temperature *T* must dissipate at least *kT* ln 2, about 2.9 × 10⁻²¹ joules at room
temperature.[^landauer1961] Charles Bennett showed in 1982 that computation itself can in
principle be carried out reversibly, so the demon's unavoidable cost lies not in measuring but
in clearing its memory before the next cycle.[^bennett1982] The bound was tested in 2012 with a
single colloidal particle in a double-well optical trap, whose measured dissipation on erasure
approached the Landauer limit.[^berut2012] Thermodynamics and information are joined by
measurement, not merely by metaphor.

## The arrow of time

The underlying equations of motion run equally well in either direction, so the observed
asymmetry of the world cannot come from the dynamics alone. The standard account locates it in
the initial condition: the universe began in a state of extraordinarily low entropy, and
everything that distinguishes past from future — that eggs break rather than assemble, that
records exist of yesterday and not tomorrow — follows from the resulting one-way drift towards
more probable states.[^septimethermo] [[Chaos theory|Chaotic]] dynamics accelerate the process by
spreading any coarse-grained description over the available configurations very quickly, but
sensitivity to initial conditions is not itself the source of the asymmetry.

## Horizons and the entropy of the universe

Entropy reappears in gravitation in a form nobody expected. Jacob Bekenstein argued in 1973 that
a [[Black hole|black hole]] must carry entropy proportional to the area of its event horizon, on
pain of letting matter be thrown in to destroy entropy and break the second law.[^bekenstein1973]
Stephen Hawking fixed the constant two years later by showing that a black hole radiates with a
definite temperature, so that the entropy equals a quarter of the horizon area measured in Planck
units.[^hawking1975] The consequences are startling: a black hole of one solar mass carries some
10⁷⁷ times the Boltzmann constant, around twenty orders of magnitude more entropy than an
ordinary star of the same mass, while its Hawking temperature is only about 60 nanokelvin. The
generalised second law asserts that ordinary entropy plus horizon entropy never decreases, and
this coupling of [[General relativity|gravity]] to thermodynamics remains one of the strongest
constraints on attempts to quantise gravity. On the largest scale, a 2010 audit of the entropy
budget put the observable universe at roughly 3 × 10¹⁰⁴ times the Boltzmann constant, dominated
overwhelmingly by supermassive black holes.[^egan2010]

## What entropy is not

The textbook gloss of entropy as disorder is a rough mnemonic that fails often enough to be
worth dropping. Freezing water and crystallising colloids both become more ordered to the eye
while the total entropy rises, and the tidiness of a room has no thermodynamic content at all.
Entropy is not a measure of complexity, nor of usefulness, and the claim that life or evolution
violates the second law confuses an open system with an isolated one. The reliable statement is
narrower and stronger: entropy counts the microscopic arrangements compatible with a
macroscopic description, and isolated systems move towards descriptions that admit more of
them.[^sepstatmech]
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Entropy",
            "subtitle": "Thermodynamic and information-theoretic quantity",
            "rows": [
                {"kind": "header", "value": "Thermodynamics"},
                {"kind": "row", "label": "SI unit", "value": "joule per kelvin (J/K)"},
                {
                    "kind": "row",
                    "label": "Defining relation",
                    "value": "Heat absorbed divided by absolute temperature, on a reversible step",
                },
                {"kind": "row", "label": "Named by", "value": "Rudolf Clausius, 1865"},
                {
                    "kind": "row",
                    "label": "Character",
                    "value": "State function; extensive; never decreases in an isolated system",
                },
                {"kind": "header", "value": "Statistical mechanics"},
                {
                    "kind": "row",
                    "label": "Microscopic form",
                    "value": "*S = k log W*, the count of microstates (Boltzmann, 1870s)",
                },
                {
                    "kind": "row",
                    "label": "Boltzmann constant",
                    "value": "Exactly 1.380649 × 10⁻²³ J/K since the 2019 revision of the SI",
                },
                {"kind": "header", "value": "Information theory"},
                {
                    "kind": "row",
                    "label": "Measure",
                    "value": "Expected surprise of a distribution, in bits",
                },
                {"kind": "row", "label": "Introduced by", "value": "Claude Shannon, 1948"},
                {"kind": "header", "value": "Gravitation"},
                {
                    "kind": "row",
                    "label": "Black hole entropy",
                    "value": "A quarter of the horizon area in Planck units "
                    "(Bekenstein 1973, Hawking 1975)",
                },
                {
                    "kind": "full",
                    "value": "The second law of thermodynamics states that the entropy of an "
                    "isolated system never decreases.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "clausius1865",
                "title": "Ueber verschiedene für die Anwendung bequeme Formen der "
                "Hauptgleichungen der mechanischen Wärmetheorie",
                "url": "https://doi.org/10.1002/andp.18652010702",
                "authors": "Rudolf Clausius",
                "publisher": "Annalen der Physik",
                "published_on": "1865",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1002/andp.18652010702",
                "quote": "Die Entropie der Welt strebt einem Maximum zu.",
            },
            {
                "key": "feynman1963",
                "title": "The Feynman Lectures on Physics, Volume I, Chapter 44: The Laws of "
                "Thermodynamics",
                "url": "https://www.feynmanlectures.caltech.edu/I_44.html",
                "authors": "Richard P. Feynman, Robert B. Leighton and Matthew Sands",
                "publisher": "California Institute of Technology",
                "published_on": "1963",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "wang2002",
                "title": "Experimental Demonstration of Violations of the Second Law of "
                "Thermodynamics for Small Systems and Short Time Scales",
                "url": "https://doi.org/10.1103/PhysRevLett.89.050601",
                "authors": "G. M. Wang, E. M. Sevick, E. Mittag, D. J. Searles and D. J. Evans",
                "publisher": "Physical Review Letters 89, 050601",
                "published_on": "2002",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevLett.89.050601",
                "quote": "",
            },
            {
                "key": "shannon1948",
                "title": "A Mathematical Theory of Communication",
                "url": "https://doi.org/10.1002/j.1538-7305.1948.tb01338.x",
                "authors": "Claude E. Shannon",
                "publisher": "Bell System Technical Journal 27, 379–423",
                "published_on": "July 1948",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1002/j.1538-7305.1948.tb01338.x",
                "quote": "",
            },
            {
                "key": "shannon1951",
                "title": "Prediction and Entropy of Printed English",
                "url": "https://doi.org/10.1002/j.1538-7305.1951.tb01366.x",
                "authors": "Claude E. Shannon",
                "publisher": "Bell System Technical Journal 30, 50–64",
                "published_on": "1951",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1002/j.1538-7305.1951.tb01366.x",
                "quote": "",
            },
            {
                "key": "landauer1961",
                "title": "Irreversibility and Heat Generation in the Computing Process",
                "url": "https://doi.org/10.1147/rd.53.0183",
                "authors": "Rolf Landauer",
                "publisher": "IBM Journal of Research and Development 5, 183–191",
                "published_on": "1961",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1147/rd.53.0183",
                "quote": "",
            },
            {
                "key": "bennett1982",
                "title": "The thermodynamics of computation — a review",
                "url": "https://doi.org/10.1007/BF02084158",
                "authors": "Charles H. Bennett",
                "publisher": "International Journal of Theoretical Physics 21, 905–940",
                "published_on": "1982",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1007/BF02084158",
                "quote": "",
            },
            {
                "key": "berut2012",
                "title": "Experimental verification of Landauer's principle linking information "
                "and thermodynamics",
                "url": "https://doi.org/10.1038/nature10872",
                "authors": "Antoine Bérut, Artak Arakelyan, Artyom Petrosyan, Sergio Ciliberto, "
                "Raoul Dillenschneider and Eric Lutz",
                "publisher": "Nature 483, 187–189",
                "published_on": "March 2012",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature10872",
                "quote": "",
            },
            {
                "key": "bekenstein1973",
                "title": "Black Holes and Entropy",
                "url": "https://doi.org/10.1103/PhysRevD.7.2333",
                "authors": "Jacob D. Bekenstein",
                "publisher": "Physical Review D 7, 2333–2346",
                "published_on": "1973",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevD.7.2333",
                "quote": "",
            },
            {
                "key": "hawking1975",
                "title": "Particle creation by black holes",
                "url": "https://doi.org/10.1007/BF02345020",
                "authors": "Stephen W. Hawking",
                "publisher": "Communications in Mathematical Physics 43, 199–220",
                "published_on": "1975",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1007/BF02345020",
                "quote": "",
            },
            {
                "key": "egan2010",
                "title": "A Larger Estimate of the Entropy of the Universe",
                "url": "https://doi.org/10.1088/0004-637X/710/2/1825",
                "authors": "Chas A. Egan and Charles H. Lineweaver",
                "publisher": "The Astrophysical Journal 710, 1825–1834",
                "published_on": "2010",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1088/0004-637X/710/2/1825",
                "quote": "",
            },
            {
                "key": "septimethermo",
                "title": "Thermodynamic Asymmetry in Time",
                "url": "https://plato.stanford.edu/entries/time-thermo/",
                "authors": "Craig Callender",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2001, revised 2026",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sepstatmech",
                "title": "Philosophy of Statistical Mechanics",
                "url": "https://plato.stanford.edu/entries/statphys-statmech/",
                "authors": "",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2023",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nistk",
                "title": "Boltzmann constant: CODATA recommended value",
                "url": "https://physics.nist.gov/cgi-bin/cuu/Value?k",
                "authors": "",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2022 CODATA adjustment",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Thermodynamics",
            "Heat engine",
            "Information theory",
            "Black hole",
            "Chaos theory",
            "Probability theory",
        ],
        "aliases": ["Second law of thermodynamics"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "thermodynamics",
            "statistical mechanics",
            "second law",
            "information theory",
            "arrow of time",
        ],
    },
    {
        "title": "Electromagnetism",
        "category": "Physics",
        "categories": ["Engineering and Technology"],
        "short_description": "The single interaction behind electricity, magnetism and light",
        "summary": (
            "Electromagnetism is the interaction between electric charges, currents and fields. "
            "Unified in the nineteenth century by Faraday's fields and Maxwell's equations, it "
            "also revealed that light is an electromagnetic wave."
        ),
        "content": """**Electromagnetism** is the interaction between electrically charged matter and the
electric and magnetic fields it produces, and one of the four known fundamental interactions. It
binds electrons to nuclei and atoms to one another, so it underlies all of chemistry, and it
accounts for essentially every everyday force other than gravity: friction, tension, contact and
the solidity of a floor are electromagnetic at bottom. Its unification during the nineteenth
century — the demonstration that electricity, magnetism and [[Light|light]] are three aspects of
one thing — is among the most consequential results in physics, both for what it explained and
for the technologies that followed from it.

## Charges, currents and fields

Electric charge comes in two signs, like charges repel and unlike attract, and the force between
two small charges falls off as the inverse square of their separation, a relation Charles-Augustin
de Coulomb established with a torsion balance in 1785. The modern description is indirect: a
charge sets up an electric field throughout space, and any other charge responds to the field at
its own location. A charge in motion responds to a magnetic field as well, at right angles both
to its velocity and to the field, and the combination is the Lorentz force.

Magnetism has no independent source. Every magnetic field traces back to moving charge, whether
as a current in a wire or as the intrinsic spin and orbital motion of electrons in a magnetised
solid, and no isolated magnetic pole has ever been found despite repeated searches. Field
strengths in ordinary experience span a wide range: the Earth's field is between about 25 and 65
microtesla at the surface, a refrigerator magnet a few millitesla, and a clinical imaging magnet
1.5 to 3 tesla.

## From two subjects to one

Electricity and magnetism were studied separately until 1820, when Hans Christian Ørsted noticed
that a compass needle turned when a nearby circuit was closed. Within months André-Marie Ampère
had shown that two parallel currents attract or repel each other and had begun the quantitative
theory of the force between them. The converse effect took another decade: on 29 August 1831
Michael Faraday wound two coils on an iron ring and saw a transient current appear in the second
whenever the current in the first was switched, establishing electromagnetic
induction.[^faraday1832] Faraday, who had little mathematics, thought in terms of lines of force
filling space, and in 1845 found that a magnetic field could rotate the plane of polarisation of
light passing through glass — the first hint that light and magnetism were related.

## Maxwell's equations

James Clerk Maxwell gave Faraday's picture mathematical form. Between 1861 and 1865 he assembled
the laws of electricity and magnetism into one system, adding a term now called the displacement
current so that a changing electric field produces a magnetic field just as a changing magnetic
field produces an electric one.[^maxwell1865] His *Treatise on Electricity and Magnetism* of 1873
set out the theory at length, and in the 1880s Oliver Heaviside and Josiah Willard Gibbs recast
his many component equations into the four vector equations taught today.[^feynmanem] In words:
electric charge is a source of electric field; magnetic field lines have no ends; a changing
magnetic field drives an electric field; and currents together with changing electric fields
drive a magnetic field.

## Light as an electromagnetic wave

The equations have solutions in which electric and magnetic fields sustain each other and travel
through empty space, at a speed fixed entirely by two constants measurable in a laboratory with
batteries and coils. When Wilhelm Weber and Rudolf Kohlrausch determined the relevant ratio in
1856 they obtained about 3.1 × 10⁸ metres per second, within a few per cent of contemporary
measurements of the speed of light, and Maxwell drew the conclusion that light simply is such a
wave. Heinrich Hertz confirmed it experimentally in 1887 and 1888 by generating waves a few tens
of centimetres long with a spark gap and showing that they reflect, refract, polarise and form
standing waves exactly as light does.

Visible light occupies a narrow band of a continuous spectrum, roughly 380 to 700 nanometres in
wavelength, with radio waves, microwaves and infrared on one side and ultraviolet, X-rays and
gamma rays on the other. All travel in vacuum at 299,792,458 metres per second, a figure that is
now exact by definition: since 1983 the metre has been defined in terms of the second and that
speed.[^si2019] The 2019 revision of the SI made the vacuum magnetic permeability a measured
quantity rather than an exact one, its value now 1.25663706127 × 10⁻⁶ newtons per ampere squared
with a relative uncertainty of 1.6 × 10⁻¹⁰.[^nistmu0]

## Relativity and the quantum

Electromagnetism forced both of the twentieth century's revolutions in physics. Einstein's 1905
paper on [[Special relativity|special relativity]] opens by noting that the theory gave two
different accounts of one experiment depending on whether the magnet or the conductor was said to
move, though the observable current was the same; relativity resolved the asymmetry by making the
electric and magnetic fields components of a single object whose split depends on the observer. In
quantum electrodynamics the field is quantised and its excitations are photons, and the strength of
the interaction is set by the fine-structure constant, whose inverse is measured as
137.035999177.[^nistalpha] It is among the most severely tested theories in science: the magnetic
moment of the electron has been calculated and measured in agreement to better than one part in a
billion. Electromagnetic behaviour in matter, worked out through
[[Quantum mechanics|quantum mechanics]], explains chemical bonding, the optical properties of
materials and the controlled conduction inside [[The transistor|transistors]]. At accelerator
energies, electromagnetism and the weak nuclear force merge into a single electroweak interaction,
confirmed by the discovery of the W and Z bosons at CERN in 1983.

## Consequences

Induction is the basis of electrical power. A conductor moved in a magnetic field generates a
current, which makes generators and motors two aspects of one machine, and transformers exploit
the fact that only a changing flux induces a voltage, which is why transmission grids run on
alternating current. Radio, television, radar and the satellite links of the
[[Global Positioning System|Global Positioning System]] all send information as electromagnetic
waves, and a loudspeaker converts a varying current into [[Sound|sound]] by driving a coil in a
magnetic field. Natural electromagnetic phenomena are equally visible: lightning, the magnetic
minerals in cooling lava that record reversals of the Earth's field, and the deflection of the
solar wind by the magnetosphere, which funnels charged particles towards the poles to produce the
[[Aurora|aurora]].
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Electromagnetism",
            "subtitle": "Fundamental interaction",
            "rows": [
                {"kind": "header", "value": "Character"},
                {
                    "kind": "row",
                    "label": "Acts on",
                    "value": "Electric charge, currents and magnetic moments",
                },
                {
                    "kind": "row",
                    "label": "Carried by",
                    "value": "The electromagnetic field; in quantum theory, the photon",
                },
                {
                    "kind": "row",
                    "label": "Range",
                    "value": "Unlimited; between point charges the force falls as 1/r²",
                },
                {
                    "kind": "row",
                    "label": "Strength",
                    "value": "Set by the fine-structure constant, close to 1/137",
                },
                {"kind": "header", "value": "Laws"},
                {
                    "kind": "row",
                    "label": "Field equations",
                    "value": "Maxwell's equations (1865; vector form from the 1880s)",
                },
                {
                    "kind": "row",
                    "label": "Force law",
                    "value": "Lorentz force, on a charge from the electric and magnetic fields",
                },
                {"kind": "header", "value": "Constants"},
                {
                    "kind": "row",
                    "label": "Speed in vacuum",
                    "value": "299,792,458 m/s, exact by the 1983 definition of the metre",
                },
                {
                    "kind": "row",
                    "label": "Vacuum permeability",
                    "value": "1.25663706127 × 10⁻⁶ N/A², measured since 2019",
                },
                {
                    "kind": "full",
                    "value": "Merges with the weak nuclear force at high energy in the "
                    "electroweak theory, confirmed by the W and Z bosons in 1983.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "faraday1832",
                "title": "Experimental Researches in Electricity",
                "url": "https://doi.org/10.1098/rstl.1832.0006",
                "authors": "Michael Faraday",
                "publisher": "Philosophical Transactions of the Royal Society of London 122, "
                "125–162",
                "published_on": "1832",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rstl.1832.0006",
                "quote": "",
            },
            {
                "key": "maxwell1865",
                "title": "A Dynamical Theory of the Electromagnetic Field",
                "url": "https://doi.org/10.1098/rstl.1865.0008",
                "authors": "James Clerk Maxwell",
                "publisher": "Philosophical Transactions of the Royal Society of London 155, "
                "459–512",
                "published_on": "1865",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rstl.1865.0008",
                "quote": "",
            },
            {
                "key": "feynmanem",
                "title": "The Feynman Lectures on Physics, Volume II, Chapter 18: The Maxwell "
                "Equations",
                "url": "https://www.feynmanlectures.caltech.edu/II_18.html",
                "authors": "Richard P. Feynman, Robert B. Leighton and Matthew Sands",
                "publisher": "California Institute of Technology",
                "published_on": "1964",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "si2019",
                "title": "The International System of Units (SI), 9th edition",
                "url": "https://www.bipm.org/en/publications/si-brochure",
                "authors": "",
                "publisher": "Bureau International des Poids et Mesures",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nistmu0",
                "title": "Vacuum magnetic permeability: CODATA recommended value",
                "url": "https://physics.nist.gov/cgi-bin/cuu/Value?mu0",
                "authors": "",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2022 CODATA adjustment",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nistalpha",
                "title": "Inverse fine-structure constant: CODATA recommended value",
                "url": "https://physics.nist.gov/cgi-bin/cuu/Value?alphinv",
                "authors": "",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2022 CODATA adjustment",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Light",
            "Special relativity",
            "Quantum mechanics",
            "The transistor",
            "Aurora",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["electricity", "magnetism", "Maxwell's equations", "fields", "optics"],
    },
]
