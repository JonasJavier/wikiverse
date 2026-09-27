"""Astronomy and Space — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Voyager program",
        "category": "Astronomy and Space",
        "categories": ["Engineering and Technology"],
        "short_description": "NASA's twin probes to the outer planets, now in interstellar space",
        "summary": (
            "The Voyager program sent two NASA spacecraft to the outer Solar System in 1977. "
            "Between them they surveyed Jupiter, Saturn, Uranus and Neptune, carried a "
            "phonograph record of Earth's sounds and images, and became the first human-made "
            "objects to reach interstellar space."
        ),
        "content": """**The Voyager program** is a NASA mission built around two nearly identical
robotic spacecraft, Voyager 1 and Voyager 2, launched in 1977 to survey the outer planets of
[[The Solar System|the Solar System]]. Between them the probes returned the first close
images of Jupiter, Saturn, Uranus and Neptune and of 48 of their moons.[^nasa_voyage] Both
craft have since passed out of the heliosphere, the bubble of solar wind and magnetic field
that surrounds the Sun, and continue to return measurements from interstellar space nearly
five decades after launch.[^nasa_interstellar]

## Origins

The program began as a trajectory calculation. In 1965 Gary Flandro, working at the Jet
Propulsion Laboratory, noticed that Jupiter, Saturn, Uranus and Neptune would be arranged in
the late 1970s so that a single spacecraft could reach all four in turn, using each planet's
gravity to bend and accelerate its path rather than carrying the propellant to do the same
work. The alignment recurs only about once every 175 years.[^nasa_voyage]

The four-planet "Grand Tour" proposed on the strength of that geometry was cancelled as too
expensive and replaced by a smaller two-planet project, Mariner Jupiter-Saturn 1977, renamed
Voyager shortly before launch. The outer legs were not so much abandoned as left
unadvertised. Voyager 2 was given a trajectory that could still be extended to Uranus and
Neptune, but only if Voyager 1 first completed the close flyby of Saturn's moon Titan that
the mission was required to attempt; had Voyager 1 failed, Voyager 2 would have been
retargeted to Titan and the outer planets forfeited. Voyager 1 succeeded, and Voyager 2 was
released to continue outward.

## Launch and encounters

Voyager 2 lifted off first, on 20 August 1977, followed by Voyager 1 on 5 September. Both
were launched from Cape Canaveral on Titan IIIE-Centaur rockets.[^nssdca] Voyager 1 followed
a shorter, faster path and overtook its twin well before either reached Jupiter.

Voyager 1 passed Jupiter on 5 March 1979 and Saturn on 12 November 1980. Voyager 2 reached
Jupiter on 9 July 1979 and Saturn on 25 August 1981, then went on to Uranus on 24 January
1986 and Neptune on 25 August 1989; it remains the only spacecraft to have visited either
planet.[^nasa_voyage]

The most unexpected result came early. Images taken at Jupiter showed active volcanism on the
moon Io, the first eruptions observed anywhere beyond Earth.[^nasa_voyage] The encounters also
yielded Jupiter's faint ring, the braided appearance of Saturn's narrow F ring, a magnetic
field at Uranus tilted far from that planet's rotation axis, eleven previously unknown Uranian
moons, and nitrogen plumes on Neptune's moon Triton.

Returning that material across the Solar System pushed the engineering of coded transmission.
The signal arriving at Earth is far too weak to be read directly, so the data are wrapped in
error-correcting codes. From the Uranus encounter onward Voyager 2's downlink used a
concatenated scheme drawn from [[Information theory]]: a Reed-Solomon block code was applied
outside the convolutional code already in service, the outer code being well suited to
repairing the bursts of errors the inner one leaves behind.[^costello2007] The flight data
subsystem was also reprogrammed in flight to compress images before transmission, and the two
measures together cut the telemetry rate needed for a given return by more than half against
Saturn practice, with little loss of information.[^urban1987]

## The Golden Record

Each spacecraft carries a 12-inch gold-plated copper phonograph record, its contents chosen
for NASA by a committee chaired by the astronomer Carl Sagan, in case either craft is ever
found. The disc holds 115 images encoded in analogue form, an audio essay of natural sounds,
spoken greetings in 55 languages running from Akkadian to the modern Chinese dialect Wu, and
about 90 minutes of music.[^nasa_record]

The music was assembled to sample traditions rather than to fix a canon. It opens with the
first movement of the Brandenburg Concerto No. 2 by [[Johann Sebastian Bach]] and continues
immediately with "Kinds of Flowers" (Puspawarna), a piece for Javanese court
[[Gamelan|gamelan]]. Three of the selections are by Bach, more than by any other composer,
which gives [[Baroque music]] a conspicuous place beside Navajo night chant, Peruvian
panpipes and Chuck Berry's "Johnny B. Goode".[^nasa_record]

The record's aluminium jacket doubles as its instruction manual. Engraved on the cover are a
drawing of the stylus in the groove and the correct playback speed, a key for reconstructing
the images, and a map giving the Sun's position relative to fourteen pulsars identified by
their periods; a plated sample of uranium-238, whose half-life is 4.5 billion years, lets a
finder date the launch from the fraction that has decayed.[^nasa_cover][^murmurs]

## Interstellar mission

Voyager 1 crossed the heliopause, the boundary at which the outward pressure of the solar wind
gives way to the interstellar plasma, on 25 August 2012 at about 122 astronomical units from
the Sun.[^nasa_interstellar] Voyager 2 crossed on 5 November 2018 at about 119 astronomical
units and in the opposite hemisphere. It found a thinner and simpler boundary than Voyager 1
had, together with a magnetic barrier just inside the heliopause that impedes the entry of
cosmic rays.[^burlaga2019]

Both craft are tracked through NASA's Deep Space Network. Their distances are obtained from
the round-trip travel time of a radio signal, the same measurement that the
[[Global Positioning System]] applies in the opposite direction to locate receivers on Earth.
NASA calculated that on 18 November 2026 Voyager 1 would stand one light-day from Earth, about
25.9 billion kilometres.[^nasa_where]

## Power and lifetime

Each spacecraft draws its electricity from three radioisotope thermoelectric generators
fuelled with plutonium-238, which together supplied about 470 watts at launch.[^nssdca] Output
falls by roughly 4 watts a year as the fuel decays and the thermocouples degrade, so
instruments and heaters are switched off one at a time. Engineers turned off Voyager 1's
cosmic ray subsystem on 25 February 2025 and Voyager 2's low-energy charged particle
instrument on 24 March 2025, leaving three working instruments on each craft, under a
conservation plan meant to keep at least one instrument running on each probe into the
2030s.[^jpl_power] The retirements have continued: Voyager 1's own low-energy charged particle
experiment was shut down on 17 April 2026, reducing that craft to a plasma wave receiver and a
magnetometer.[^nasa_v1_lecp]

The imaging system was retired much earlier. On 14 February 1990, from about 6 billion
kilometres out, Voyager 1 turned its cameras back toward the inner Solar System and recorded a
mosaic in which Earth occupies less than a single pixel, published as "Pale Blue
Dot".[^nasa_pbd] The cameras were shut down soon afterwards to save power and computer memory.
""",
        "tier": "standard",
        "kind": "work",
        "infobox": {
            "title": "Voyager program",
            "subtitle": "NASA outer-planets and interstellar mission",
            "rows": [
                {"kind": "header", "value": "Overview"},
                {"kind": "row", "label": "Operator", "value": "NASA / Jet Propulsion Laboratory"},
                {"kind": "row", "label": "Spacecraft", "value": "Voyager 1 and Voyager 2"},
                {"kind": "row", "label": "Launch vehicle", "value": "Titan IIIE-Centaur"},
                {"kind": "row", "label": "Voyager 2 launch", "value": "20 August 1977"},
                {"kind": "row", "label": "Voyager 1 launch", "value": "5 September 1977"},
                {"kind": "header", "value": "Planetary encounters"},
                {
                    "kind": "row",
                    "label": "Jupiter",
                    "value": "5 March 1979 (Voyager 1); 9 July 1979 (Voyager 2)",
                },
                {
                    "kind": "row",
                    "label": "Saturn",
                    "value": "12 November 1980 (Voyager 1); 25 August 1981 (Voyager 2)",
                },
                {"kind": "row", "label": "Uranus", "value": "24 January 1986 (Voyager 2 only)"},
                {"kind": "row", "label": "Neptune", "value": "25 August 1989 (Voyager 2 only)"},
                {"kind": "header", "value": "Interstellar phase"},
                {
                    "kind": "row",
                    "label": "Heliopause crossed",
                    "value": "25 August 2012 (Voyager 1); 5 November 2018 (Voyager 2)",
                },
                {
                    "kind": "row",
                    "label": "Power",
                    "value": "Three radioisotope thermoelectric generators, about 470 W at launch",
                },
                {
                    "kind": "full",
                    "value": (
                        "Each craft carries a gold-plated copper phonograph record of images, "
                        "greetings and music, with playback instructions engraved on its cover."
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/5/56/"
                "The_Sounds_of_Earth_Record_Cover_-_GPN-2000-001978.jpg"
            ),
            "alt": (
                "Gold-coloured aluminium record jacket engraved with diagrams of a stylus, "
                "a wave pattern and a radial pulsar map"
            ),
            "caption": (
                "The gold anodised aluminium cover that protects each Voyager record. Its "
                "engraved diagrams show how to play the disc and where the Sun lies relative "
                "to fourteen pulsars."
            ),
            "credit": "NASA/JPL",
            "license": "Public domain",
            "source_url": (
                "https://commons.wikimedia.org/wiki/"
                "File:The_Sounds_of_Earth_Record_Cover_-_GPN-2000-001978.jpg"
            ),
        },
        "references": [
            {
                "key": "nasa_voyage",
                "title": "The Planetary Voyage",
                "url": "https://science.nasa.gov/mission/voyager/planetary-voyage/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "Discovery of active volcanism on the satellite Io was probably the "
                    "greatest surprise."
                ),
            },
            {
                "key": "nasa_interstellar",
                "title": "Voyager: Interstellar Mission",
                "url": "https://science.nasa.gov/mission/voyager/interstellar-mission/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nssdca",
                "title": "Voyager 1 spacecraft record (1977-084A)",
                "url": "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1977-084A",
                "authors": "",
                "publisher": "NASA Space Science Data Coordinated Archive",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "approximately 470 W of 30 V DC power at launch",
            },
            {
                "key": "nasa_record",
                "title": "Golden Record Contents",
                "url": "https://science.nasa.gov/mission/voyager/golden-record-contents/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "murmurs",
                "title": "Murmurs of Earth: The Voyager Interstellar Record",
                "url": "https://archive.org/details/murmursofearthvo00saga",
                "authors": (
                    "Carl Sagan, F. D. Drake, Ann Druyan, Timothy Ferris, Jon Lomberg and "
                    "Linda Salzman Sagan"
                ),
                "publisher": "Ballantine Books",
                "published_on": "1979; first published by Random House in 1978",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa_cover",
                "title": "The Golden Record Cover",
                "url": "https://science.nasa.gov/mission/voyager/golden-record-cover/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "shows the location of the solar system with respect to 14 pulsars, whose "
                    "precise periods are given"
                ),
            },
            {
                "key": "burlaga2019",
                "title": (
                    "Magnetic field and particle measurements made by Voyager 2 at and near "
                    "the heliopause"
                ),
                "url": "https://www.nature.com/articles/s41550-019-0920-y",
                "authors": "L. F. Burlaga and others",
                "publisher": "Nature Astronomy",
                "published_on": "November 2019",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/s41550-019-0920-y",
                "quote": "",
            },
            {
                "key": "costello2007",
                "title": "Channel Coding: The Road to Channel Capacity",
                "url": "https://arxiv.org/abs/cs/0611112",
                "authors": "Daniel J. Costello Jr. and G. David Forney Jr.",
                "publisher": "Proceedings of the IEEE",
                "published_on": "2007",
                "accessed_on": "2026-09-26",
                "identifier": "arXiv:cs/0611112",
                "quote": "",
            },
            {
                "key": "urban1987",
                "title": "Voyager image data compression and block encoding",
                "url": "https://ntrs.nasa.gov/citations/19880046413",
                "authors": "Michael G. Urban",
                "publisher": "Jet Propulsion Laboratory; ITC/USA '87, San Diego",
                "published_on": "October 1987",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "reduce telemetry transmission rates by over 50 percent compared to those "
                    "used at Saturn, with negligible loss in information return"
                ),
            },
            {
                "key": "jpl_power",
                "title": "NASA Turns Off 2 Voyager Science Instruments to Extend Mission",
                "url": (
                    "https://www.jpl.nasa.gov/news/"
                    "nasa-turns-off-two-voyager-science-instruments-to-extend-mission/"
                ),
                "authors": "",
                "publisher": "NASA Jet Propulsion Laboratory",
                "published_on": "5 March 2025",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa_v1_lecp",
                "title": "NASA Shuts Off Instrument on Voyager 1 to Keep Spacecraft Operating",
                "url": (
                    "https://science.nasa.gov/blogs/voyager/2026/04/17/"
                    "nasa-shuts-off-instrument-on-voyager-1-to-keep-spacecraft-operating/"
                ),
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "17 April 2026",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "Voyager 1 still has two remaining operating science instruments - one "
                    "that listens to plasma waves and one that measures magnetic fields."
                ),
            },
            {
                "key": "nasa_where",
                "title": "Where Are Voyager 1 and Voyager 2 Now?",
                "url": (
                    "https://science.nasa.gov/mission/voyager/"
                    "where-are-voyager-1-and-voyager-2-now/"
                ),
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa_pbd",
                "title": "The Pale Blue Dot",
                "url": "https://science.nasa.gov/resource/voyager-pale-blue-dot-download/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "The Solar System",
            "Global Positioning System",
            "Information theory",
            "Gamelan",
            "Johann Sebastian Bach",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "spaceflight",
            "outer planets",
            "gravity assist",
            "Golden Record",
            "interstellar space",
        ],
    },
    {
        "title": "The periodic table",
        "category": "Chemistry and Materials",
        "categories": ["Physics"],
        "short_description": "The elements ordered by atomic number into periods and groups",
        "summary": (
            "The periodic table arranges the chemical elements by atomic number so that "
            "elements with similar behaviour fall into the same column. Built from atomic "
            "weights in the 1860s and later explained by electron structure, it now holds "
            "118 elements."
        ),
        "content": """**The periodic table** is a tabular arrangement of the chemical elements in
order of atomic number, laid out so that elements with similar chemical behaviour fall into
the same vertical column. It is the organising diagram of chemistry: an element's position
encodes, in compressed form, the size of its atoms, how tightly it holds its outermost
electrons, the formulas of the compounds it forms and roughly how vigorously it reacts. The
table now contains 118 elements, of which 94 occur naturally on Earth. The four heaviest were
named only in 2016, completing its seventh row.[^iupac2016]

## How the table is read

Horizontal rows are called periods and vertical columns are called groups. The International
Union of Pure and Applied Chemistry (IUPAC) numbers the groups 1 to 18 from left to right and
the periods 1 to 7 from top to bottom.[^iupac_pt] Each step to the right adds one proton to
the nucleus and one electron to the neutral atom; each new row begins the filling of a new
outermost shell, which is why the pattern of chemical behaviour repeats rather than drifting.

The table divides into blocks named after the kind of orbital its outer electrons occupy. The
two columns on the far left and the six on the right form the s and p blocks, the main-group
elements, whose chemistry is the most regular. Between them sit the ten columns of the d
block, the transition metals. Two further series of fourteen elements each, the lanthanides
and the actinides, make up the f block; they are conventionally cut out and printed beneath
the main body, which would otherwise be 32 columns wide.

Several groups carry long-standing names. Group 1, the alkali metals, are soft, reactive
metals that form singly charged positive ions. Group 17, the halogens, are reactive non-metals
that form singly charged negative ions. Group 18, the noble gases, have filled outer shells
and were for decades thought to form no compounds at all; the first xenon compound was not
prepared until 1962.

## Precursors

An ordered table required a trustworthy list of elements and trustworthy atomic weights, and
neither existed before the late eighteenth century. Antoine Lavoisier's *Traité élémentaire de
chimie* of 1789 offered the first credible inventory, some thirty-three substances that had
resisted further decomposition, and its authority rested on his demonstration that
[[Combustion|combustion]] is combination with oxygen rather than the loss of a principle
called phlogiston. The list still contained errors: light and "caloric" appear on it as
elements. What it displaced was largely the scheme inherited from [[Alchemy|alchemy]], which
paired seven metals with the seven classical planets.

Through the middle of the nineteenth century several chemists noticed periodicity without
producing a usable table. From 1817 Johann Wolfgang Döbereiner identified "triads" such as
calcium, strontium and barium, in which the middle element's atomic weight is close to the
average of the other two. In 1862 Alexandre-Émile Béguyer de Chancourtois wound the elements
in weight order around a cylinder and found related elements falling on the same vertical
line, but his paper was printed without its diagram and attracted little attention. John
Newlands stated a "law of octaves" in 1865, and Julius Lothar Meyer plotted atomic volume
against atomic weight to obtain a curve with clear repeating maxima.[^scerri2020]

## Mendeleev's table

Dmitri Mendeleev's version, drafted in February 1869 and read to the Russian Chemical Society
the following month, was not the first but was the one that took hold, for two reasons. He
treated the gaps in his arrangement as claims rather than embarrassments, and he was willing
to trust chemical resemblance over a measured atomic weight when the two conflicted, placing
tellurium before iodine although tellurium is the heavier of the two.[^scerri2020]

In 1871 Mendeleev published detailed predictions for three missing elements, which he named
eka-boron, eka-aluminium and eka-silicon after the elements immediately above each gap. All
three were found within fifteen years: gallium by Paul-Émile Lecoq de Boisbaudran in 1875,
scandium by Lars Fredrik Nilson in 1879 and germanium by Clemens Winkler in 1886. The
agreement between prediction and measurement was close enough to convert most of the
profession.[^scerri2020]

| Property | Predicted for eka-silicon, 1871 | Measured for germanium, 1886 |
| --- | --- | --- |
| Atomic weight | 72 | 72.6 |
| Density | 5.5 g/cm3 | 5.35 g/cm3 |
| Oxide | EsO2, density 4.7 g/cm3 | GeO2, density 4.70 g/cm3 |
| Chloride | EsCl4, boiling below 100 °C | GeCl4, boiling at 86 °C |

Mendeleev's record was not unblemished. He also predicted elements lighter than hydrogen to
populate the ether, and he resisted the noble gases when they appeared, because his table had
no column for them. Argon was isolated by Lord Rayleigh and William Ramsay in 1894, and
helium, identified in 1868 by its emission [[Light|lines]] in the solar spectrum, was not
obtained on Earth until 1895. A new group accommodated the whole family without disturbing the
rest of the arrangement, which counted in the scheme's favour.[^britannica_pt]

## Ordering by atomic number

Mendeleev ordered the elements by atomic weight, which mostly works but produces a handful of
inversions. The rule was corrected in 1913 and 1914 by Henry Moseley, who bombarded elemental
targets with electrons and measured the frequencies of the X-rays they emitted. The square
root of the frequency of a characteristic line varies linearly with the element's place in the
table, and Moseley identified that place with the electric charge on the nucleus: the atomic
number, Z. Ordering by Z removes the inversions, fixes exactly how many elements can lie
between any two known ones, and showed that four elements lighter than gold were still
missing.[^egdell2020] Moseley was killed at Gallipoli in 1915, aged 27.

## Why the pattern exists

Periodicity follows from how electrons occupy the space around a nucleus, which is described
by [[Quantum mechanics|quantum mechanics]] and sketched in [[Atomic theory]]. Niels Bohr's
model of 1913 introduced quantised shells; Wolfgang Pauli's exclusion principle of 1925, which
forbids two electrons in an atom from sharing all four quantum numbers, fixed how many
electrons each shell can hold. An s orbital accommodates 2 electrons, a set of p orbitals 6,
d orbitals 10 and f orbitals 14 — exactly the widths of the four blocks.

The order in which orbitals fill explains the table's shape and not merely its column count.
The 4s level lies below 3d in energy for a neutral atom, so period 4 opens with potassium and
calcium in the s block before the first transition series begins at scandium, and the period
runs to 18 elements instead of 8. Elements in one group share an outer-shell configuration,
which is why they form the same kinds of bond, as described in
[[Chemical bond|chemical bonding]]: the noble gases are unreactive because their outer shells
are complete, and the alkali metals are reactive because each carries a single loosely held
electron outside a closed shell.

## Periodic trends

Several properties vary smoothly enough across the table to be estimated from position alone.
Atomic radius contracts from left to right along a period, as the growing nuclear charge draws
the electron cloud inward, and expands down a group as shells are added. First ionisation
energy runs the other way, rising across a period and falling down a group; helium's is the
highest of any element. Electronegativity, the tendency of an atom to pull shared electrons
toward itself, peaks at fluorine, assigned 3.98 on the Pauling scale, and is lowest among the
heavy alkali metals, caesium being 0.79. Metallic character increases toward the bottom left
of the table.

The regularity fails in instructive places. In the heaviest atoms the innermost electrons move
fast enough that relativistic corrections alter chemistry measurably: contraction of the 6s
orbital is why gold is yellow rather than silver-white, and why [[Mercury (element)|mercury]]
is the only metal that is liquid at room temperature.

## Where the elements came from

The table is also a record of nuclear history. Hydrogen, most helium and a trace of lithium
were made in the first minutes after the Big Bang. Elements up to iron and nickel are built by
fusion inside stars, and the sequence stops there because the binding energy per nucleon peaks
around that mass, so fusing still heavier nuclei absorbs energy instead of releasing it. Most
elements beyond iron are assembled by neutron capture — a slow process in the interiors of
evolved low-mass stars and a rapid one in explosive environments, the latter confirmed as a
source when the merger of two neutron stars observed in 2017 was seen to manufacture heavy
elements. Lithium, beryllium and boron are the anomalies, made mainly when cosmic rays break
up heavier nuclei in interstellar space.[^johnson2019]

## Filling and extending the table

Two of Mendeleev's gaps were closed only by synthesis: technetium, element 43, was first
produced by bombardment in 1937, and promethium, element 61, in 1945. Beyond uranium every
element has been made artificially. Placing them correctly required Glenn Seaborg's proposal
of 1944 that the elements from actinium onward form a second f-block series, the actinides,
parallel to the lanthanides rather than continuing the transition metals; rearranged on that
basis, the new elements fell into consistent groups.[^scerri2020]

Radioactivity had already complicated what a place in the table means. The work of
[[Marie Curie]] and her collaborators added polonium and radium to it and established that
atoms of one element turn into atoms of another, so an element's position is a statement about
nuclear charge rather than about permanence.

The heaviest elements exist only as a few atoms at a time and survive for fractions of a
second. All four of those that completed period 7 — nihonium, moscovium, tennessine and
oganesson, with atomic numbers 113, 115, 117 and 118 — had their names approved by IUPAC in
November 2016.[^iupac2016] Attempts on elements 119 and 120 continue, and theory suggests an
island of longer-lived superheavy nuclei somewhere beyond, but no experiment has reached it.
Because the heaviest elements have no stable isotopes and no settled terrestrial abundance,
the standard atomic weights that IUPAC's commission publishes for ordinary elements cannot be
quoted for them at all.[^ciaaw]

## What the table does not settle

Chemists still argue over placements that look purely cosmetic. Whether hydrogen belongs above
lithium or above fluorine, whether helium belongs above beryllium, and whether group 3
contains scandium, yttrium, lanthanum and actinium or scandium, yttrium, lutetium and
lawrencium are live questions, because the table is asked to do two jobs at once: reflect
electron configuration and reflect chemical resemblance. Those two criteria do not always
agree, and no single diagram satisfies both.[^scerri2020]
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Periodic table of the elements",
            "subtitle": "Classification scheme of chemistry",
            "rows": [
                {"kind": "row", "label": "First published", "value": "1869, by Dmitri Mendeleev"},
                {
                    "kind": "row",
                    "label": "Ordering principle",
                    "value": "Atomic number, the electric charge on the nucleus",
                },
                {
                    "kind": "row",
                    "label": "Elements",
                    "value": "118, of which 94 occur naturally on Earth",
                },
                {"kind": "row", "label": "Rows", "value": "7 periods"},
                {
                    "kind": "row",
                    "label": "Columns",
                    "value": "18 groups, numbered 1 to 18 by IUPAC",
                },
                {
                    "kind": "row",
                    "label": "Blocks",
                    "value": "s, p, d and f, named after electron orbitals",
                },
                {"kind": "header", "value": "Extremes"},
                {"kind": "row", "label": "Lightest element", "value": "Hydrogen, Z = 1"},
                {"kind": "row", "label": "Heaviest named", "value": "Oganesson, Z = 118, in 2016"},
                {
                    "kind": "row",
                    "label": "Most electronegative",
                    "value": "Fluorine, 3.98 on the Pauling scale",
                },
                {
                    "kind": "full",
                    "value": (
                        "The lanthanides and actinides are normally printed below the main "
                        "body; set in place, the table is 32 columns wide."
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/b/bb/"
                "Mendeleev%27s_1869_periodic_table.png"
            ),
            "alt": (
                "Facsimile of an 1869 table of element symbols and atomic weights arranged in "
                "columns, with question marks standing in for undiscovered elements"
            ),
            "caption": (
                "Facsimile of the table Dmitri Mendeleev published in 1869. Question marks "
                "occupy the places he left for elements not yet discovered."
            ),
            "credit": "Dmitri Mendeleev",
            "license": "Public domain",
            "source_url": (
                "https://commons.wikimedia.org/wiki/File:Mendeleev%27s_1869_periodic_table.png"
            ),
        },
        "references": [
            {
                "key": "iupac2016",
                "title": "IUPAC announces the names of the elements 113, 115, 117, and 118",
                "url": (
                    "https://iupac.org/"
                    "iupac-announces-the-names-of-the-elements-113-115-117-and-118/"
                ),
                "authors": "",
                "publisher": "International Union of Pure and Applied Chemistry",
                "published_on": "30 November 2016",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "For now, we can all cherish our periodic table completed down to the "
                    "seventh row."
                ),
            },
            {
                "key": "iupac_pt",
                "title": "Periodic Table of Elements",
                "url": "https://iupac.org/what-we-do/periodic-table-of-elements/",
                "authors": "",
                "publisher": "International Union of Pure and Applied Chemistry",
                "published_on": "4 May 2022",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "scerri2020",
                "title": "The Periodic Table: Its Story and Its Significance",
                "url": "https://global.oup.com/academic/product/the-periodic-table-9780190914363",
                "authors": "Eric Scerri",
                "publisher": "Oxford University Press",
                "published_on": "2020, 2nd edition",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-19-091436-3",
                "quote": "",
            },
            {
                "key": "egdell2020",
                "title": "Henry Moseley, X-ray spectroscopy and the periodic table",
                "url": "https://royalsocietypublishing.org/doi/10.1098/rsta.2019.0302",
                "authors": "Russell G. Egdell and Elizabeth Bruton",
                "publisher": "Philosophical Transactions of the Royal Society A",
                "published_on": "2020",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rsta.2019.0302",
                "quote": "",
            },
            {
                "key": "johnson2019",
                "title": "Populating the periodic table: Nucleosynthesis of the elements",
                "url": "https://www.science.org/doi/10.1126/science.aau9540",
                "authors": "Jennifer A. Johnson",
                "publisher": "Science",
                "published_on": "1 February 2019",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.aau9540",
                "quote": "",
            },
            {
                "key": "ciaaw",
                "title": "Standard atomic weights",
                "url": "https://www.ciaaw.org/atomic-weights.htm",
                "authors": "",
                "publisher": "IUPAC Commission on Isotopic Abundances and Atomic Weights",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica_pt",
                "title": "Periodic table",
                "url": "https://www.britannica.com/science/periodic-table",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Atomic theory",
            "Chemical bond",
            "Quantum mechanics",
            "Mercury (element)",
            "Alchemy",
            "Marie Curie",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "chemical elements",
            "periodicity",
            "Mendeleev",
            "atomic number",
            "nucleosynthesis",
        ],
    },
    {
        "title": "Atomic theory",
        "category": "Chemistry and Materials",
        "categories": ["Physics"],
        "short_description": "How matter came to be understood as made of discrete atoms",
        "summary": (
            "Atomic theory holds that matter consists of discrete particles rather than being "
            "continuously divisible. Revived quantitatively by John Dalton after 1803, it was "
            "established by measurement a century later and then rebuilt around the nucleus "
            "and the electron."
        ),
        "content": """**Atomic theory** is the proposition that matter is made of discrete
particles rather than being continuously divisible, together with the body of evidence that
turned that proposition from a philosophical position into a measured physical fact. Its
modern form dates from the first decade of the nineteenth century; the decisive experimental
confirmations arrived a century later, and in the process the theory was rebuilt twice — once
when the atom turned out to have parts, and again when those parts turned out to obey
[[Quantum mechanics|quantum]] rules.

## Ancient atomism

The idea appears in Greek natural philosophy in the fifth century BC with Leucippus and
Democritus, who held that matter consists of indivisible bodies — *atomos*, "uncut" — moving
in a void, and that observable qualities arise from their shapes and arrangements. Epicurus
adopted the doctrine and Lucretius set it out in verse in *De rerum natura*. It was a
metaphysical commitment rather than a scientific hypothesis: no observation available to its
proponents, or to Aristotle, who rejected both atoms and the void, could distinguish discrete
from continuous matter.[^sep_atomism] The laboratory tradition of [[Alchemy]] worked with a
different ontology altogether, organising substances around qualities and principles such as
sulphur and mercury.

## Chemical atomism

John Dalton gave the theory quantitative content. Between 1803 and 1808 he proposed that each
element consists of atoms identical in mass, that compounds contain fixed ratios of small
whole numbers of atoms, and that chemical reactions rearrange atoms without creating or
destroying them.[^britannica_dalton] The proposal earned its keep by explaining the law of
multiple proportions: where two elements form more than one compound, the masses of the second
that combine with a fixed mass of the first stand in simple ratios, as in the two oxides of
carbon, whose oxygen masses are as 1 to 2. Dalton also published a table of relative atomic
weights, taking hydrogen as 1.

He had no way to determine how many atoms a molecule contained, and assigned several formulas
incorrectly, water among them. Joseph Louis Gay-Lussac's measurements of combining gas volumes
in 1808 and Amedeo Avogadro's hypothesis of 1811 — that equal volumes of gases at the same
temperature and pressure contain equal numbers of particles — supplied the missing rule, but
Avogadro's proposal was largely ignored until Stanislao Cannizzaro revived it in 1858.
Consistent atomic weights followed, and with them [[The periodic table]].

Even then many chemists treated atoms as a convenient accounting device rather than as
objects. Wilhelm Ostwald and Ernst Mach were still declining to grant them physical reality in
the early 1900s.[^sep_atomism]

## Counting atoms

The resistance ended with measurement. In 1827 the botanist Robert Brown had described the
ceaseless irregular motion of tiny particles suspended in water. Albert Einstein's paper of
1905 treated that motion as the statistical result of molecular collisions and showed that the
mean square displacement of a suspended particle grows in proportion to elapsed time, with a
coefficient set by temperature, viscosity, particle size and the number of molecules in a
mole.[^einstein1905] Watching the jitter therefore counts molecules. Jean Perrin carried out
the observations, obtained a value for that number close to the accepted one, and received the
1926 Nobel Prize in Physics for his work on the discontinuous structure of
matter.[^nobel_perrin]

## The atom acquires parts

By then the atom had already ceased to be indivisible. In 1897 J. J. Thomson showed that
cathode rays are deflected by both electric and magnetic fields and measured the ratio of
charge to mass of the particles carrying them, later named electrons, finding it far larger
than for any known ion. In 1904 he proposed a model in which electrons sit embedded in a
diffuse sphere of positive charge.

That model was tested at Manchester. In 1909 Hans Geiger and Ernest Marsden directed alpha
particles at thin metal foils and found that a small minority — of the order of one in a few
thousand — were deflected through more than 90 degrees, which a diffuse charge could not
accomplish. Ernest Rutherford's analysis, published in 1911, concluded that the positive
charge and almost all the mass must be concentrated in a region minute compared with the atom
as a whole.[^aps_rutherford] A nucleus is of the order of ten femtometres across against about
a hundred picometres for the whole atom, some ten thousand times smaller in diameter, so
ordinary matter is very nearly empty space held apart by electrons.

## Nuclei, isotopes and neutrons

The nuclear picture was filled in over the following two decades. Frederick Soddy introduced
the term isotope in 1913 for atoms of one element differing in mass, and Francis Aston's mass
spectrograph separated them. Henry Moseley's X-ray measurements of 1913 and 1914 identified an
element's place in [[The periodic table]] with its nuclear charge. Rutherford knocked protons
out of nitrogen nuclei in 1919, and in 1932 James Chadwick identified the neutron, which
accounted for the gap between an element's atomic number and its atomic mass; he received the
1935 Nobel Prize in Physics for the discovery.[^nobel_chadwick] The radioactivity studied by
[[Marie Curie]] and others had meanwhile shown that nuclei change identity spontaneously, so
atoms are neither indivisible nor permanent.

## The quantum atom

A nucleus orbited by electrons is unstable under classical electrodynamics, because a
circulating charge radiates away its energy. Niels Bohr's model of 1913 evaded the problem by
postulating allowed orbits, and reproduced the observed spectral [[Light|lines]] of hydrogen.
Erwin Schrödinger's wave equation of 1926 replaced orbits with orbitals: standing-wave
distributions giving the probability of finding an electron in a given region. Together with
the Pauli exclusion principle, this account explains shell structure, the periodicity of
[[The periodic table]] and the formation of the [[Chemical bond]]. It also carries small
relativistic corrections that become chemically significant in the heaviest atoms and are the
reason [[Mercury (element)|mercury]] is liquid at room temperature.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Atomic theory",
            "subtitle": "Development of the modern account of the atom",
            "rows": [
                {"kind": "header", "value": "Milestones"},
                {"kind": "row", "label": "5th century BC", "value": "Leucippus and Democritus"},
                {
                    "kind": "row",
                    "label": "1803-1808",
                    "value": "Dalton's chemical atomism and atomic weights",
                },
                {"kind": "row", "label": "1897", "value": "Thomson identifies the electron"},
                {
                    "kind": "row",
                    "label": "1905-1913",
                    "value": "Einstein and Perrin measure molecular numbers",
                },
                {"kind": "row", "label": "1911", "value": "Rutherford infers a compact nucleus"},
                {
                    "kind": "row",
                    "label": "1913",
                    "value": "Bohr's quantised shells; Soddy names isotopes",
                },
                {"kind": "row", "label": "1932", "value": "Chadwick identifies the neutron"},
                {
                    "kind": "full",
                    "value": (
                        "Atomic radii are of order 100 picometres; nuclear radii are some ten "
                        "thousand times smaller."
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/9/9b/"
                "Gold_foil_experiment_conclusions.svg"
            ),
            "alt": (
                "Diagram contrasting the small deflections expected from a diffuse positive "
                "charge with the rare large-angle deflections actually observed"
            ),
            "caption": (
                "Conclusions drawn from the alpha-particle scattering experiments: only a "
                "compact, highly charged nucleus can turn a projectile through a large angle."
            ),
            "credit": "Kurzon",
            "license": "Public domain",
            "source_url": (
                "https://commons.wikimedia.org/wiki/File:Gold_foil_experiment_conclusions.svg"
            ),
        },
        "references": [
            {
                "key": "sep_atomism",
                "title": "Atomism from the 17th to the 20th Century",
                "url": "https://plato.stanford.edu/entries/atomism-modern/",
                "authors": "Alan Chalmers and Klodian Coko",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "first published 2005",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica_dalton",
                "title": "John Dalton",
                "url": "https://www.britannica.com/biography/John-Dalton",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "einstein1905",
                "title": (
                    "Über die von der molekularkinetischen Theorie der Wärme geforderte "
                    "Bewegung von in ruhenden Flüssigkeiten suspendierten Teilchen"
                ),
                "url": "https://onlinelibrary.wiley.com/doi/10.1002/andp.19053220806",
                "authors": "Albert Einstein",
                "publisher": "Annalen der Physik",
                "published_on": "1905",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1002/andp.19053220806",
                "quote": "",
            },
            {
                "key": "nobel_perrin",
                "title": "The Nobel Prize in Physics 1926",
                "url": "https://www.nobelprize.org/prizes/physics/1926/summary/",
                "authors": "",
                "publisher": "The Nobel Foundation",
                "published_on": "1926",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "for his work on the discontinuous structure of matter",
            },
            {
                "key": "aps_rutherford",
                "title": "May, 1911: Rutherford and the Discovery of the Atomic Nucleus",
                "url": "https://www.aps.org/apsnews/2006/05/rutherford-discovery-atomic-nucleus",
                "authors": "",
                "publisher": "American Physical Society",
                "published_on": "May 2006",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "the alpha particles were being scattered by a large amount of positive "
                    "charge concentrated in a very small space at the center of the gold atom"
                ),
            },
            {
                "key": "nobel_chadwick",
                "title": "The Nobel Prize in Physics 1935",
                "url": "https://www.nobelprize.org/prizes/physics/1935/summary/",
                "authors": "",
                "publisher": "The Nobel Foundation",
                "published_on": "1935",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "for the discovery of the neutron",
            },
        ],
        "see_also": [
            "The periodic table",
            "Chemical bond",
            "Quantum mechanics",
            "Marie Curie",
            "Alchemy",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "atoms",
            "Dalton",
            "Rutherford",
            "Brownian motion",
            "nucleus",
        ],
    },
]
