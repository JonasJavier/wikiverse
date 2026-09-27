"""Astronomy and Space — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Galileo Galilei",
        "category": "Astronomy and Space",
        "categories": ["Physics", "History"],
        "short_description": "Italian astronomer who turned the new telescope on the sky",
        "summary": (
            "Galileo Galilei (1564–1642) was an Italian astronomer, physicist and "
            "mathematician whose telescopic discoveries and experiments on motion helped "
            "dismantle Aristotelian physics, and whose trial by the Roman Inquisition in "
            "1633 became the defining conflict over scientific authority."
        ),
        "content": """**Galileo Galilei** (15 February 1564 – 8 January 1642) was an Italian astronomer,
physicist and mathematician whose telescopic observations supplied the first genuinely new
evidence in the dispute over [[The Copernican Revolution|heliocentrism]], and whose
experiments on falling and rolling bodies began to replace the qualitative physics inherited
from Aristotle with mathematical description. His condemnation by the Roman Inquisition in
1633 made him the emblematic figure of [[The Scientific Revolution]] and the subject of a
four-century argument about what the episode actually demonstrates.

## Early life and career

Galileo was born in Pisa, the eldest child of Vincenzo Galilei, a lutenist and music
theorist who had himself experimented on the relationship between the tension of a string
and its pitch.[^sep] Galileo enrolled at the University of Pisa in 1581 to read medicine,
left without a degree, taught mathematics privately, and was appointed to the chair of
mathematics at Pisa in 1589. In 1592 he moved to the far better paid chair at Padua, in the
mainland territory of the Republic of [[Venice]], where he remained for eighteen years,
lecturing on Euclid and astronomy, running a workshop that sold surveying instruments, and
working privately on the problem of motion.[^britannica]

## The telescope

News of a Dutch spyglass reached Venice in the summer of 1609. Galileo grasped the
arrangement quickly — a weak convex objective at one end of a tube, a strong concave
eyepiece at the other — ground his own lenses, and reached roughly eight times magnification
almost at once, about twenty times by the end of the year, and some thirty times
later.[^museo] In August 1609 he demonstrated the instrument to the Venetian Senate from the
campanile of San Marco, arguing its value for sighting ships hours before they were visible
to the naked eye. The Senate doubled his salary and confirmed his post for life.

What he did next set him apart from the other early telescope makers: he pointed it away
from the harbour. Between November 1609 and March 1610 he established that the line dividing
lunar day from night is ragged rather than smooth, implying mountains and valleys on a body
that Aristotelian cosmology required to be perfectly spherical; that the Milky Way resolves
into individual stars; and, from 7 January 1610, that four small bodies accompany Jupiter and
shift position from night to night. He published all of it within weeks as *Sidereus
Nuncius*, printed in Venice on 13 March 1610, naming the satellites the Medicean Stars after
the ruling family of Tuscany, which promptly appointed him mathematician and philosopher to
the Grand Duke.[^loc] The names now in use — Io, Europa, Ganymede and Callisto — were
proposed by his rival Simon Marius and became standard only in the twentieth century.

## Further observations

Jupiter's satellites mattered because they were a second centre of motion inside
[[The Solar System]]: whatever else was true, not everything circled the Earth. Late in 1610
Galileo found something stronger. Venus runs through a full cycle of phases, from a small
gibbous disc to a large crescent, which is what a body orbiting the Sun must do and what a
body carried on a Ptolemaic epicycle below the Sun cannot. He announced the result as an
anagram before publishing it, a common device for claiming priority without disclosing a
finding. He also followed spots across the solar disc, argued in 1613 that they lay on the
Sun's surface rather than in front of it, and inferred the Sun's rotation from their drift.
His optics could not resolve Saturn's rings, which he described as two attendant bodies that
later inexplicably vanished.

The instrument was understood through an older tradition of optics. The behaviour of
[[Light]] in lenses and the formation of inverted images inside a darkened room, the
[[Camera obscura]], had been analysed centuries before, and Galileo used projection rather
than direct viewing for his solar work.

## The science of motion

Galileo's mechanics, developed at Padua and published only at the end of his life, is the
more durable achievement. Rolling bronze balls down a grooved wooden ramp and timing them by
the flow of water, he established that a uniformly accelerated body covers distances
proportional to the square of the elapsed time, so that in successive equal intervals it
traverses lengths in the ratio 1 : 3 : 5 : 7. He argued that bodies of different weight fall
at the same rate in the absence of air resistance; that a projectile's path is a parabola
compounded of uniform horizontal motion and uniform vertical acceleration; and that a body on
a frictionless horizontal plane would keep moving indefinitely, which is the germ of what
[[Isaac Newton]] later stated as the first law of motion. He also noticed that a pendulum's
period is nearly independent of the width of its swing. His attempt to measure the speed of
light by signalling between two lanterns failed, and he concluded only that propagation was
extremely fast.

The celebrated demonstration of dropping unequal weights from the leaning campanile at Pisa
is reported only by his late disciple Vincenzo Viviani and is generally treated as
unverified.

## The trial

Galileo's Copernicanism became a theological problem in 1615 and 1616. A Roman commission
judged the doctrine of a moving Earth formally heretical, Cardinal Bellarmine warned him in
person, and the work of Copernicus was suspended pending correction. Galileo stayed publicly
quiet on the question for sixteen years. In 1632 he published the *Dialogue Concerning the
Two Chief World Systems*, a conversation among three speakers that ostensibly weighed the
Ptolemaic and Copernican systems and in practice demolished the first. Its central physical
argument, which derived the Earth's motion from the tides, was wrong.

He was summoned to Rome, tried, and on 22 June 1633 found "vehemently suspect of heresy". He
abjured, the *Dialogue* was banned, and a sentence of imprisonment was commuted to house
arrest, served from December 1633 at his villa at Arcetri outside Florence.[^finocchiaro] The
muttered *eppur si muove* appears in no contemporary record.

## Later years and reputation

Blind by 1638 and still confined, Galileo completed the *Discourses and Mathematical
Demonstrations Relating to Two New Sciences*, which sets out his work on the strength of
materials and on motion. The manuscript was carried out of Italy and printed at Leiden by the
Elzevirs in 1638, beyond the reach of the Roman censors. He died at Arcetri in January 1642.
The *Dialogue* stayed on the Index of Prohibited Books until 1835. A study commission
appointed by John Paul II in 1981 reported eleven years later, and in an address to the
Pontifical Academy of Sciences on 31 October 1992 he accepted that Galileo's theological
judges had erred in treating a question of physical cosmology as settled by
scripture.[^vatican]
""",
        "tier": "standard",
        "kind": "person",
        "infobox": {
            "title": "Galileo Galilei",
            "subtitle": "Italian astronomer, physicist and mathematician",
            "rows": [
                {
                    "kind": "row",
                    "label": "Born",
                    "value": "15 February 1564, Pisa, Duchy of Florence",
                },
                {"kind": "row", "label": "Died", "value": "8 January 1642, Arcetri, near Florence"},
                {"kind": "row", "label": "Fields", "value": "Astronomy, mechanics, mathematics"},
                {"kind": "header", "value": "Academic posts"},
                {"kind": "row", "label": "Pisa", "value": "Chair of mathematics, 1589–1592"},
                {"kind": "row", "label": "Padua", "value": "Chair of mathematics, 1592–1610"},
                {
                    "kind": "row",
                    "label": "Florence",
                    "value": "Mathematician and philosopher to the Grand Duke of Tuscany, from 1610",
                },
                {"kind": "header", "value": "Principal works"},
                {"kind": "row", "label": "1610", "value": "*Sidereus Nuncius*"},
                {
                    "kind": "row",
                    "label": "1632",
                    "value": "*Dialogue Concerning the Two Chief World Systems*",
                },
                {"kind": "row", "label": "1638", "value": "*Two New Sciences*"},
                {
                    "kind": "full",
                    "value": (
                        "Condemned by the Roman Inquisition on 22 June 1633 and held under "
                        "house arrest until his death"
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/d/d4/"
                "Justus_Sustermans_-_Portrait_of_Galileo_Galilei%2C_1636.jpg"
            ),
            "alt": "Oil portrait of an elderly bearded man in a dark robe, facing slightly left",
            "caption": "Galileo in 1636, painted by Justus Sustermans during the years of house arrest.",
            "credit": "Justus Sustermans; Royal Museums Greenwich",
            "license": "Public domain",
            "source_url": (
                "https://commons.wikimedia.org/wiki/"
                "File:Justus_Sustermans_-_Portrait_of_Galileo_Galilei,_1636.jpg"
            ),
        },
        "references": [
            {
                "key": "sep",
                "title": "Galileo Galilei",
                "url": "https://plato.stanford.edu/entries/galileo/",
                "authors": "Peter Machamer and David Marshall Miller",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2021",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica",
                "title": "Galileo",
                "url": "https://www.britannica.com/biography/Galileo-Galilei",
                "authors": "Albert Van Helden and Stillman Drake",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "museo",
                "title": "Museo Galileo, Institute and Museum of the History of Science",
                "url": "https://www.museogalileo.it/en/",
                "authors": "",
                "publisher": "Museo Galileo, Florence",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "loc",
                "title": "Starry Messenger: Galileo's Rapidly Published Findings",
                "url": (
                    "https://www.loc.gov/static/collections/"
                    "finding-our-place-in-the-cosmos-with-carl-sagan/articles-and-essays/"
                    "modeling-the-cosmos/galileo-and-the-telescope.html"
                ),
                "authors": "",
                "publisher": "Library of Congress",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "finocchiaro",
                "title": "The Galileo Affair: A Documentary History",
                "url": "https://www.ucpress.edu/books/the-galileo-affair/paper",
                "authors": "Maurice A. Finocchiaro (editor and translator)",
                "publisher": "University of California Press",
                "published_on": "1989",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "vatican",
                "title": (
                    "Address to the Participants in the Plenary Session of the Pontifical "
                    "Academy of Sciences"
                ),
                "url": (
                    "https://www.vatican.va/content/john-paul-ii/en/speeches/1992/october/"
                    "documents/hf_jp-ii_spe_19921031_accademia-scienze.html"
                ),
                "authors": "John Paul II",
                "publisher": "Holy See",
                "published_on": "31 October 1992",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "The Copernican Revolution",
            "The Scientific Revolution",
            "Isaac Newton",
            "The Solar System",
            "Camera obscura",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["telescope", "heliocentrism", "mechanics", "history of astronomy"],
    },
    {
        "title": "Black hole",
        "category": "Astronomy and Space",
        "categories": ["Physics"],
        "short_description": "A region of spacetime whose gravity lets nothing, not even light, escape",
        "summary": (
            "A black hole is a region of spacetime curved so steeply by concentrated mass that "
            "nothing inside its event horizon can escape. Once a theoretical curiosity, black "
            "holes are now observed through X-rays, stellar orbits, gravitational waves and "
            "direct imaging."
        ),
        "content": """**Black holes** are regions of spacetime in which gravity is so strong that no
matter and no signal, including [[Light|light itself]], can escape to the outside. The
boundary of such a region is its event horizon, a one-way surface rather than a physical
membrane: an object crossing it can still send signals inward but never outward again. Black
holes are a prediction of [[General relativity]], and over roughly half a century they moved
from a mathematical oddity that most physicists expected nature to forbid to objects that are
routinely weighed, timed and, since 2019, photographed.

## Dark stars before relativity

The idea is older than relativity. In 1783 the English clergyman and natural philosopher John
Michell sent the Royal Society a paper reasoning that if light consisted of corpuscles
subject to gravity in the manner described by [[Isaac Newton]], then a star sufficiently
large and dense would have an escape velocity exceeding the speed of light, so that its light
would fall back and the star would be invisible; he suggested such bodies might be detected
by their gravitational effect on visible companions.[^michell] Pierre-Simon Laplace published
a similar argument in 1796 and dropped it from later editions. The notion lapsed once the wave
theory of light displaced the corpuscular one, because a wave has no obvious reason to be
slowed by gravity.

## The Schwarzschild radius

Within months of the publication of general relativity, Karl Schwarzschild found the exact
solution of the field equations for the empty space around a spherical, non-rotating mass.
The solution misbehaves at a characteristic distance from the centre, the Schwarzschild
radius, equal to 2GM/c². It works out to about 2.95 kilometres for each solar mass, so the
Sun would have to be compressed inside a sphere roughly 6 kilometres across, and the Earth
inside a sphere about 18 millimetres across, to become a black hole. For decades this surface
was read as a genuine singularity in the theory. It is not: it is an artefact of the
coordinates, and nothing physically infinite happens there. What is real about it is its
causal structure. Because [[Special relativity|no signal outruns light]], every future-directed
path from inside the horizon leads inward.

## Gravitational collapse

The astrophysical question was whether anything actually collapses that far. Subrahmanyan
Chandrasekhar showed in 1931 that electron degeneracy pressure cannot support a white dwarf
heavier than about 1.4 solar masses. Neutron stars have a comparable ceiling, currently
estimated at roughly two to three solar masses. In 1939 J. Robert Oppenheimer and Hartland
Snyder worked out the collapse of a spherical dust cloud in general relativity and found that
it proceeds without limit: to a distant observer the surface appears to freeze at the horizon
and redden away, while to an observer falling with it the horizon is crossed in finite time
and the centre is reached shortly after.[^oppenheimer]

The obvious objection was that real stars are not perfect spheres, and that any asymmetry
might halt the collapse. Roger Penrose settled it in 1965 with a topological argument showing
that once a trapped surface forms, a singularity follows generically, without any assumption
of symmetry.[^penrose] He shared the 2020 Nobel Prize in Physics for that result, alongside
Reinhard Genzel and Andrea Ghez for the observational case at the centre of the Milky
Way.[^nobel] The term "black hole" itself appeared in print in a 1964 conference report and
was popularised by John Archibald Wheeler from 1967, replacing the earlier phrase
"gravitationally completely collapsed object".

## Anatomy

A stationary black hole is described by exactly three numbers: mass, angular momentum and
electric charge. Every other property of the collapsing matter — its composition, its
magnetic field, its shape — is erased, a result summarised as the no-hair theorem. Roy Kerr
found the solution for a rotating black hole in 1963, and astrophysical black holes are
expected to be Kerr black holes with negligible charge.

Outside the horizon of a non-rotating black hole lie two further landmarks. The photon sphere
sits at 1.5 times the Schwarzschild radius, the radius at which light can circle in an
unstable orbit. The innermost stable circular orbit for matter lies at 3 times the
Schwarzschild radius; inside it, orbiting material spirals in. Together these produce the
observable signature of a black hole: a dark central region, the shadow, whose apparent size
is set by the strong bending of light rays and is noticeably larger than the horizon
itself.[^nasa]

## Tidal forces

Tidal stretching scales as the mass divided by the cube of the distance, so it grows more
severe for smaller black holes. At the horizon of a black hole of a few solar masses the
difference in gravitational pull across a human body would be lethal long before the horizon
was reached. At the horizon of a supermassive black hole of billions of solar masses the
tidal gradient is mild, and an infalling observer would cross without local discomfort while
being causally sealed off nonetheless. A whole star passing close enough to a supermassive
black hole is still torn apart well outside the horizon, producing a months-long flare known
as a tidal disruption event.

## Classes and formation

Stellar-mass black holes, of roughly 3 to 100 solar masses, are the collapse remnants of
stars that began life above about twenty solar masses. Supermassive black holes, between
about a hundred thousand and tens of billions of solar masses, sit at the centres of most
large galaxies; how they grew so large so early remains unsettled. Intermediate-mass black
holes, between those ranges, are sparsely evidenced. Primordial black holes formed by density
fluctuations in the early universe are hypothetical and, in some mass ranges, heavily
constrained by observation.

Scale is easy to misjudge. Sagittarius A*, at the centre of the Milky Way, has a mass of
about 4.3 million suns and therefore a horizon radius near 12.7 million kilometres — under a
tenth of the Earth–Sun distance, and dwarfed by [[The Solar System]] it would sit inside. The
black hole at the centre of the galaxy M87 is roughly 6.5 billion solar masses, giving a
horizon radius of some 120 astronomical units, about four times the radius of Neptune's orbit.

## Accretion and radiation

Black holes themselves emit nothing, but matter falling towards one does. Gas with angular
momentum settles into an accretion disc, where viscous friction converts orbital energy into
heat and X-rays. The efficiency is remarkable: around 6 per cent of the rest mass energy of
the infalling matter can be radiated for a non-rotating black hole, and up to about 40 per
cent for a rapidly spinning one, against 0.7 per cent for hydrogen fusion. Accreting
supermassive black holes power quasars and radio jets, which is why the brightest persistent
objects in the universe are driven by the darkest.

## Observational evidence

Four independent lines of evidence now converge.

X-ray binaries supplied the first candidates. Cygnus X-1, detected by a sounding rocket in
1964, pairs a bright supergiant with an unseen companion too massive to be a neutron star.
Dozens of similar systems are now catalogued.

Stellar orbits established the Galactic centre case. Over three decades, infrared astronomers
tracked individual stars looping around an invisible mass at the centre of the Milky Way; one
of them completes an orbit in about sixteen years. Interferometric astrometry of several such
orbits gives a mass of 4.297 million solar masses concentrated within a region far smaller
than the orbits themselves.[^gravity]

Gravitational waves gave direct evidence of horizons in motion. On 14 September 2015 the two
LIGO detectors recorded a signal, announced the following February, from the merger of black
holes of about 36 and 29 solar masses into one of about 62. Roughly three solar masses were
converted into gravitational radiation in a fraction of a second, from a source about 410
megaparsecs away.[^ligo] Scores of mergers have since been catalogued.

Imaging came last. The Event Horizon Telescope combined eight radio observatories into an
Earth-sized interferometer at a wavelength of 1.3 millimetres. On 10 April 2019 it released an
image of the galaxy M87's central black hole: an asymmetric bright ring 42 microarcseconds
across, surrounding a dark depression, at a distance of some 55 million
light-years.[^eht2019i] The ring's diameter yields a mass near 6.5 billion suns, matching
estimates from stellar motions.[^eht2019vi] A comparable image of Sagittarius A*, about 27,000
light-years away and far more variable, followed on 12 May 2022.[^eht2022]

## Thermodynamics and Hawking radiation

The deepest surprises are thermodynamic. In 1972 Jacob Bekenstein argued that a black hole
must carry an entropy proportional to the area of its horizon rather than to its volume,
because otherwise dropping matter into one would let an observer violate the second law of
[[Thermodynamics]].[^bekenstein] Two years later Stephen Hawking showed that applying
[[Quantum mechanics]] to fields near a horizon makes the black hole radiate with a genuine
thermal spectrum, fixing the constant in Bekenstein's formula.[^hawking] The entropy equals
one quarter of the horizon area in Planck units.

The numbers are extreme in both directions. The [[Entropy]] of a solar-mass black hole is
around 10⁷⁷ times Boltzmann's constant, close to twenty orders of magnitude greater than the
thermodynamic entropy of the star that made it; horizons are by a wide margin the most
entropic objects known. The temperature, by contrast, is minute — about 62 nanokelvin for one
solar mass, and inversely proportional to mass, so a stellar-mass black hole absorbs far more
from the 2.7-kelvin cosmic microwave background than it emits. Left alone in an empty
universe, such a black hole would take of order 10⁶⁷ years to evaporate, ending in a brief,
violent burst.

## The information problem

Hawking radiation is thermal, which means it appears to carry no record of what fell in. If
that is exactly true, then a black hole destroys quantum information, contradicting the
reversibility that underlies quantum theory. Framed in the language of [[Information theory]],
the question is whether the correlations between the emitted radiation and the collapsed
matter survive. The problem has driven decades of work on holography, on the pattern of
entanglement entropy over a black hole's lifetime, and on what a horizon looks like from the
inside. No consensus resolution has been established.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Black hole",
            "subtitle": "Gravitationally collapsed region of spacetime",
            "rows": [
                {
                    "kind": "row",
                    "label": "Predicted by",
                    "value": "[[General relativity]]; Schwarzschild solution, 1916",
                },
                {
                    "kind": "row",
                    "label": "Defining feature",
                    "value": "An event horizon, a one-way causal boundary",
                },
                {
                    "kind": "row",
                    "label": "Schwarzschild radius",
                    "value": "2GM/c², about 2.95 km per solar mass",
                },
                {
                    "kind": "row",
                    "label": "Fully described by",
                    "value": "Mass, angular momentum and electric charge",
                },
                {"kind": "header", "value": "Observed classes"},
                {
                    "kind": "row",
                    "label": "Stellar-mass",
                    "value": "About 3 to 100 solar masses; remnants of massive stars",
                },
                {
                    "kind": "row",
                    "label": "Supermassive",
                    "value": "100,000 to tens of billions of solar masses; galactic centres",
                },
                {"kind": "header", "value": "Landmark observations"},
                {
                    "kind": "row",
                    "label": "2015",
                    "value": "GW150914, first gravitational-wave detection of a merger",
                },
                {
                    "kind": "row",
                    "label": "2019",
                    "value": "First horizon-scale image, of M87's black hole",
                },
                {"kind": "row", "label": "2022", "value": "Horizon-scale image of Sagittarius A*"},
                {
                    "kind": "full",
                    "value": (
                        "Horizon entropy scales with area, not volume — the result that opened "
                        "black-hole thermodynamics"
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/4/4f/"
                "Black_hole_-_Messier_87_crop_max_res.jpg"
            ),
            "alt": "An asymmetric glowing orange ring surrounding a dark circular region",
            "caption": (
                "The Event Horizon Telescope image of the black hole at the centre of M87, "
                "released on 10 April 2019: a ring of emission 42 microarcseconds across "
                "around the shadow."
            ),
            "credit": "Event Horizon Telescope Collaboration / ESO",
            "license": "CC BY 4.0",
            "source_url": (
                "https://commons.wikimedia.org/wiki/File:Black_hole_-_Messier_87_crop_max_res.jpg"
            ),
        },
        "references": [
            {
                "key": "michell",
                "title": (
                    "On the Means of Discovering the Distance, Magnitude, etc. of the Fixed "
                    "Stars, in Consequence of the Diminution of the Velocity of Their Light"
                ),
                "url": "https://doi.org/10.1098/rstl.1784.0008",
                "authors": "John Michell",
                "publisher": "Philosophical Transactions of the Royal Society of London",
                "published_on": "1784",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rstl.1784.0008",
                "quote": "",
            },
            {
                "key": "oppenheimer",
                "title": "On Continued Gravitational Contraction",
                "url": "https://doi.org/10.1103/PhysRev.56.455",
                "authors": "J. R. Oppenheimer and H. Snyder",
                "publisher": "Physical Review",
                "published_on": "1939",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRev.56.455",
                "quote": "",
            },
            {
                "key": "penrose",
                "title": "Gravitational Collapse and Space-Time Singularities",
                "url": "https://doi.org/10.1103/PhysRevLett.14.57",
                "authors": "Roger Penrose",
                "publisher": "Physical Review Letters",
                "published_on": "1965",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevLett.14.57",
                "quote": "",
            },
            {
                "key": "nobel",
                "title": "The Nobel Prize in Physics 2020",
                "url": "https://www.nobelprize.org/prizes/physics/2020/summary/",
                "authors": "",
                "publisher": "Nobel Prize Outreach",
                "published_on": "2020",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa",
                "title": "Black Holes",
                "url": "https://imagine.gsfc.nasa.gov/science/objects/black_holes1.html",
                "authors": "",
                "publisher": "NASA Goddard Space Flight Center, Imagine the Universe",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "gravity",
                "title": (
                    "Mass Distribution in the Galactic Center Based on Interferometric "
                    "Astrometry of Multiple Stellar Orbits"
                ),
                "url": "https://doi.org/10.1051/0004-6361/202142465",
                "authors": "GRAVITY Collaboration",
                "publisher": "Astronomy & Astrophysics",
                "published_on": "2022",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1051/0004-6361/202142465",
                "quote": "",
            },
            {
                "key": "ligo",
                "title": "Observation of Gravitational Waves from a Binary Black Hole Merger",
                "url": "https://doi.org/10.1103/PhysRevLett.116.061102",
                "authors": "B. P. Abbott et al. (LIGO Scientific Collaboration and Virgo Collaboration)",
                "publisher": "Physical Review Letters",
                "published_on": "11 February 2016",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevLett.116.061102",
                "quote": "",
            },
            {
                "key": "eht2019i",
                "title": (
                    "First M87 Event Horizon Telescope Results. I. The Shadow of the "
                    "Supermassive Black Hole"
                ),
                "url": "https://doi.org/10.3847/2041-8213/ab0ec7",
                "authors": "Event Horizon Telescope Collaboration",
                "publisher": "The Astrophysical Journal Letters",
                "published_on": "10 April 2019",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.3847/2041-8213/ab0ec7",
                "quote": "",
            },
            {
                "key": "eht2019vi",
                "title": (
                    "First M87 Event Horizon Telescope Results. VI. The Shadow and Mass of "
                    "the Central Black Hole"
                ),
                "url": "https://doi.org/10.3847/2041-8213/ab1141",
                "authors": "Event Horizon Telescope Collaboration",
                "publisher": "The Astrophysical Journal Letters",
                "published_on": "10 April 2019",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.3847/2041-8213/ab1141",
                "quote": "",
            },
            {
                "key": "eht2022",
                "title": (
                    "First Sagittarius A* Event Horizon Telescope Results. I. The Shadow of "
                    "the Supermassive Black Hole in the Center of the Milky Way"
                ),
                "url": "https://doi.org/10.3847/2041-8213/ac6674",
                "authors": "Event Horizon Telescope Collaboration",
                "publisher": "The Astrophysical Journal Letters",
                "published_on": "12 May 2022",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.3847/2041-8213/ac6674",
                "quote": "",
            },
            {
                "key": "bekenstein",
                "title": "Black Holes and Entropy",
                "url": "https://doi.org/10.1103/PhysRevD.7.2333",
                "authors": "Jacob D. Bekenstein",
                "publisher": "Physical Review D",
                "published_on": "1973",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevD.7.2333",
                "quote": "",
            },
            {
                "key": "hawking",
                "title": "Black hole explosions?",
                "url": "https://doi.org/10.1038/248030a0",
                "authors": "S. W. Hawking",
                "publisher": "Nature",
                "published_on": "1 March 1974",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/248030a0",
                "quote": "",
            },
        ],
        "see_also": [
            "General relativity",
            "Special relativity",
            "Entropy",
            "Information theory",
            "Quantum mechanics",
            "The Solar System",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "gravitation",
            "event horizon",
            "Hawking radiation",
            "gravitational waves",
            "astrophysics",
        ],
    },
    {
        "title": "Solar eclipse",
        "category": "Astronomy and Space",
        "categories": ["Physics"],
        "short_description": "The Moon passing between Earth and the Sun and blocking its light",
        "summary": (
            "A solar eclipse occurs when the Moon passes between Earth and the Sun and casts "
            "its shadow on the surface. Because the two discs appear almost the same size, "
            "totality lasts only minutes and briefly exposes the Sun's corona."
        ),
        "content": """**Solar eclipses** occur when the Moon passes between the Earth and the Sun and
casts its shadow across part of the Earth's surface. They depend on a coincidence with no
physical cause: the Sun is roughly 400 times the diameter of the Moon and also roughly 390
times as far away, so the two discs appear almost exactly the same size from the ground. A
slightly smaller Moon would never produce totality; a slightly larger one would hide the
Sun's outer atmosphere along with the disc.

## Geometry

The Moon's orbit is tilted about five degrees to the plane of the Earth's orbit, so most new
moons pass above or below the Sun. An eclipse requires the new moon to fall near one of the
two nodes where the orbital planes cross, which happens during eclipse seasons about 173 days
apart. Both orbits are elliptical, so the apparent diameters vary: the Moon's between roughly
29.4 and 33.5 arcminutes, the Sun's between about 31.6 and 32.7. Whether a given central
eclipse is total or annular depends on where in that range the two discs happen to fall.

The shadow has two parts. Within the umbra the solar disc is entirely covered; within the
surrounding penumbra it is partly covered. The umbra traces a narrow track, at most a few
hundred kilometres wide, that sweeps eastward as the Moon moves and the Earth turns beneath
it. The track crosses the ground at roughly 1,700 kilometres per hour near the equator and far
faster at high latitudes, which is why totality is always brief.

## Types

Four cases are distinguished. A **total** eclipse occurs when the umbra reaches the surface.
An **annular** eclipse occurs when the Moon is near the far point of its orbit and its disc is
too small to cover the Sun, leaving a bright ring; the sky stays daylit. A **partial** eclipse
is seen from inside the penumbra only. A **hybrid** eclipse is annular at the ends of its
track and total in the middle, because the surface curves closer to the Moon at mid-track.

Totality at a given point lasts from a fraction of a second to a theoretical maximum of 7
minutes 32 seconds; the annular phase of an annular eclipse can run as long as 12 minutes 29
seconds.[^glossary] Long totalities occur when the Moon is near its closest approach and the
Earth near its farthest point from the Sun.

## Frequency and the saros

Between two and five solar eclipses occur each year, of which a total eclipse happens
somewhere on Earth roughly every eighteen months; any particular location waits centuries on
average. Eclipses repeat in families called saros series. One saros is 223 synodic months, or
6,585.32 days — about 18 years, 11 days and 8 hours — after which the Sun, Moon and node
return to nearly the same relative positions and a very similar eclipse follows.[^saros]

The awkward extra third of a day matters. Because the Earth has turned a further 120 degrees,
each eclipse in a series falls about a third of the way westward around the globe from its
predecessor. Three saroses, a period of 54 years and 34 days called the exeligmos, restore
the longitude as well. A saros series runs for 1,226 to 1,550 years and contains 69 to 87
eclipses, drifting from pole to pole as it goes; roughly forty series are in progress at any
time.[^saros] Modern catalogues tabulate every eclipse across five millennia on this
basis.[^canon]

## What totality looks like

The last minutes before totality are distinctive. Light turns metallic, the temperature drops
several degrees, and the ragged edge of the Moon breaks the vanishing sliver of Sun into
points of light called Baily's beads, the last of which forms the diamond ring. Bands of faint
shadow may ripple across pale surfaces. Then the corona appears: the Sun's outer atmosphere,
a million or more degrees hot but a millionth the brightness of the disc, invisible at any
other time without specialised instruments. Bright stars and planets become visible, among
them [[Mercury (planet)|Mercury]], which never strays far from the Sun and is normally lost in
its glare.

## Eclipses and the history of astronomy

Eclipse prediction is among the oldest quantitative achievements in astronomy. Babylonian
scribes recorded lunar and solar eclipses on clay tablets in [[Cuneiform]] over centuries and
used the saros to anticipate when an eclipse was possible, though not where it would be
visible. The [[The Antikythera mechanism|Antikythera mechanism]], a Greek geared device of
the second or first century BC, encodes the same cycle mechanically: a spiral dial of 223
months carries glyphs marking predicted eclipses, and a subsidiary four-turn dial handles the
exeligmos correction.[^freeth]

Totality also made the Sun's atmosphere available for study. During the eclipse of 18 August
1868 observers recorded a bright yellow line in the spectrum of a solar prominence that
matched no known element; the element was named helium, and was not found on Earth until
1895.[^helium] Other unexplained coronal lines, once attributed to a hypothetical element
"coronium", were identified in the early 1940s as emission from extremely highly ionised iron,
which is what first revealed how hot the corona is.

The most consequential eclipse observation was made on 29 May 1919, when British expeditions
to Sobral in Brazil and to the island of Príncipe photographed stars near the eclipsed Sun to
test whether [[General relativity]] correctly predicted the bending of starlight. Einstein's
value for a ray grazing the solar limb was 1.75 arcseconds, twice the Newtonian figure. The
Sobral plates gave 1.98 arcseconds and the Príncipe plates 1.61; the results were announced
in London that November.[^dyson]

## Observing methods

Because the Sun's brightness is undiminished during partial and annular phases, indirect
methods have always been used to watch them. Projection through a small aperture onto a screen
is the oldest: the [[Camera obscura]] was used for eclipse observation in the medieval Islamic
world and by European astronomers from the sixteenth century, and pinhole projection remains
the standard classroom demonstration.[^nasa] Only during total eclipse, when the disc is fully
covered, is the corona bright enough and the disc dark enough to be looked at directly.

## The far future

Lunar laser ranging shows the Moon receding from the Earth by about 3.8 centimetres a year, a
consequence of tidal interaction. Its apparent diameter is therefore shrinking. In something
of the order of 600 million years the Moon will no longer be able to cover the solar disc from
anywhere on Earth, and total eclipses will cease; annular eclipses will continue. On the scale
of [[The Solar System]], the present era of totality is a brief accident of timing.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Solar eclipse",
            "subtitle": "Alignment of Sun, Moon and Earth at new moon",
            "rows": [
                {"kind": "row", "label": "Types", "value": "Total, annular, partial and hybrid"},
                {
                    "kind": "row",
                    "label": "Frequency",
                    "value": "Two to five each year; a total eclipse somewhere about every 18 months",
                },
                {"kind": "row", "label": "Maximum totality", "value": "7 minutes 32 seconds"},
                {
                    "kind": "row",
                    "label": "Shadow speed",
                    "value": "About 1,700 km/h near the equator, faster at high latitudes",
                },
                {"kind": "header", "value": "The saros cycle"},
                {
                    "kind": "row",
                    "label": "Length",
                    "value": "223 synodic months, or 6,585.32 days — 18 years, 11 days and 8 hours",
                },
                {
                    "kind": "row",
                    "label": "Longitude shift",
                    "value": "Each successive eclipse falls about 120° further west",
                },
                {
                    "kind": "row",
                    "label": "Series lifetime",
                    "value": "1,226 to 1,550 years, containing 69 to 87 eclipses",
                },
                {
                    "kind": "full",
                    "value": (
                        "Predicted from cuneiform records in the first millennium BC and by the "
                        "geared saros dial of [[The Antikythera mechanism]]"
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Solar_eclipse_1999_4.jpg",
            "alt": "A black lunar disc ringed by the pale, streaming white light of the solar corona",
            "caption": (
                "The corona during the total solar eclipse of 11 August 1999, photographed "
                "from France."
            ),
            "credit": "Luc Viatour, www.lucnix.be",
            "license": "CC BY-SA 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:Solar_eclipse_1999_4.jpg",
        },
        "references": [
            {
                "key": "glossary",
                "title": "Eclipse Glossary",
                "url": "https://eclipse.gsfc.nasa.gov/SEhelp/SEglossary.html",
                "authors": "Fred Espenak",
                "publisher": "NASA Goddard Space Flight Center",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "saros",
                "title": "Eclipses and the Saros",
                "url": "https://eclipse.gsfc.nasa.gov/SEsaros/SEsaros.html",
                "authors": "Fred Espenak",
                "publisher": "NASA Goddard Space Flight Center",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "canon",
                "title": "Five Millennium Canon of Solar Eclipses: -1999 to +3000",
                "url": "https://eclipse.gsfc.nasa.gov/SEpubs/5MCSE.html",
                "authors": "Fred Espenak and Jean Meeus",
                "publisher": "NASA Technical Publication TP-2006-214141",
                "published_on": "2006",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "freeth",
                "title": (
                    "Calendars with Olympiad display and eclipse prediction on the Antikythera "
                    "Mechanism"
                ),
                "url": "https://doi.org/10.1038/nature07130",
                "authors": "Tony Freeth, Alexander Jones, John M. Steele and Yanis Bitsakis",
                "publisher": "Nature",
                "published_on": "July 2008",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature07130",
                "quote": "",
            },
            {
                "key": "dyson",
                "title": (
                    "A Determination of the Deflection of Light by the Sun's Gravitational "
                    "Field, from Observations Made at the Total Eclipse of May 29, 1919"
                ),
                "url": "https://doi.org/10.1098/rsta.1920.0009",
                "authors": "F. W. Dyson, A. S. Eddington and C. Davidson",
                "publisher": "Philosophical Transactions of the Royal Society A",
                "published_on": "1920",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rsta.1920.0009",
                "quote": "",
            },
            {
                "key": "helium",
                "title": "Helium",
                "url": "https://periodic-table.rsc.org/element/2/helium",
                "authors": "",
                "publisher": "Royal Society of Chemistry, Periodic Table",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa",
                "title": "Eclipses",
                "url": "https://science.nasa.gov/eclipses/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "The Antikythera mechanism",
            "General relativity",
            "The Solar System",
            "Mercury (planet)",
            "Cuneiform",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["eclipse", "saros", "corona", "celestial mechanics"],
    },
]
