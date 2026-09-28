"""Physics — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Light",
        "category": "Physics",
        "categories": ["Astronomy and Space"],
        "short_description": "Electromagnetic radiation the eye can see, and how it travels",
        "summary": (
            "Light is electromagnetic radiation between roughly 380 and 750 nanometres, the band "
            "the human eye detects. It behaves as a ray, a wave and a stream of photons, and "
            "crosses a vacuum at exactly 299,792,458 metres per second."
        ),
        "content": """**Light** is electromagnetic radiation in the band of wavelengths the human eye can
detect, roughly 380 to 750 nanometres, corresponding to frequencies of about 400 to 790
terahertz and photon energies between about 1.6 and 3.3 electronvolts.[^britannica-light]
Physicists often stretch the word to cover the adjacent infrared and ultraviolet, which
obey the same laws but are invisible. Light is the subject of optics, and since the 1860s
it has been understood as one narrow slice of the
[[Electromagnetism|electromagnetic spectrum]].

Three descriptions of light are in routine use, each valid in its own regime. Geometrical
optics treats light as rays that travel in straight lines and bend at surfaces; it accounts
for shadows, mirrors and lenses. Wave optics treats it as an oscillating electromagnetic
field, and is required wherever interference, diffraction or polarisation appear. Quantum
optics treats it as a stream of photons, indivisible packets of energy, and is required for
emission, absorption and detection. Ray optics is the short-wavelength limit of wave optics,
and wave optics is the many-photon limit of the quantum description; none of the three is a
rival to the others.[^feynman-optics]

## Reflection and refraction

At a smooth surface the reflected ray leaves at the same angle to the surface normal as the
incident ray arrives, in the same plane. At a boundary between transparent media part of the
beam reflects and part crosses over with a change of direction given by Snell's law: the
sine of the angle to the normal is inversely proportional to the refractive index of the
medium. That index is the ratio of the vacuum speed of light to the phase speed in the
material, about 1.33 for water, 1.5 for ordinary glass and 2.42 for diamond.

Going from a dense medium towards a rarer one, refraction fails beyond a critical angle and
the beam is reflected entirely. The critical angle is about 49 degrees for water against air
and about 24 degrees for diamond against air; the diamond figure, combined with strong
dispersion, is why a cut stone traps and redirects light so vigorously. The same effect
confines a signal inside an optical fibre.

Refractive index depends slightly on wavelength, an effect called dispersion, which is why a
prism spreads white light into a band of colours and why a rainbow forms an arc about 42
degrees from the point opposite the Sun. All of this follows from a single statement, Fermat's
principle: of the possible paths between two points, light takes one whose travel time is
unchanged by small variations.[^feynman-optics]

## The speed of light

[[Galileo Galilei]] described an attempt to time light between distant lanterns and concluded
in 1638 that its propagation was either instantaneous or extraordinarily fast. The first
evidence of a finite speed came in 1676, when Ole Rømer noticed that eclipses of Jupiter's
moon Io ran early when Earth was near Jupiter and late when it was far, and inferred that
light needed roughly 22 minutes to cross the diameter of Earth's orbit; the modern figure is
about 16.7 minutes. Christiaan Huygens converted Rømer's timing into a speed and obtained
about two-thirds of the correct value. James Bradley's discovery in 1728 of the aberration of
starlight, an annual wobble of some 20 arcseconds caused by Earth's own motion, yielded a
result within roughly one per cent.

Laboratory measurement followed in the nineteenth century. Hippolyte Fizeau sent a beam
through a rapidly spinning toothed wheel to a mirror about 8 kilometres away in 1849 and
obtained 313,000 kilometres per second; Léon Foucault's rotating-mirror version gave 298,000
in 1862. Albert Michelson spent decades refining the figure, reaching 299,796 kilometres per
second in a 1926 measurement between two California mountain tops.

Modern practice reverses the relationship. In 1983 the General Conference on Weights and
Measures defined the metre as the distance light travels in vacuum in 1/299,792,458 of a
second, so the vacuum speed of light is now exactly 299,792,458 metres per second by
definition and any further experiment measures length rather than speed.[^si-brochure][^nist-c]
Sunlight crosses the 150 million kilometres to Earth in about 8 minutes 20 seconds. In matter
the phase speed is smaller by the refractive index, falling to roughly 225,000 kilometres per
second in water.

## Colour and the spectrum

Isaac Newton's prism experiments, begun in the 1660s and set out in Opticks in 1704,
established that white light is a mixture: a prism separates it into a spectrum, and a second
prism recombines the spectrum into white. Colour as experienced, however, belongs to the
visual system as much as to the radiation. Human colour vision rests on three classes of cone
cell with broad, overlapping sensitivities peaking near 420, 530 and 560 nanometres, so wholly
different spectra can look identical. Colour printing and every display screen exploit that
ambiguity, and some perceived colours, magenta among them, correspond to no single wavelength
at all.

Splitting light by wavelength is mathematically the same operation as taking the
[[Fourier transform]] of the field's variation in time. Joseph von Fraunhofer catalogued
hundreds of dark lines in the solar spectrum from 1814, and around 1860 Gustav Kirchhoff and
Robert Bunsen showed that each chemical element imprints a characteristic pattern of lines.
Spectroscopy thereby turned light into a chemical assay usable at any distance: caesium and
rubidium were both identified by their spectra, and helium was found in sunlight decades
before it was isolated on Earth, filling in [[The periodic table|the periodic table]] from
across space.

## Interference, diffraction and polarisation

Thomas Young's demonstration around 1801 that two overlapping beams from narrow slits produce
alternating bright and dark fringes could not be explained by rays, and revived the wave
account. Augustin-Jean Fresnel supplied the mathematics; in 1818 Siméon Poisson objected that
the theory absurdly required a bright spot at the very centre of a circular object's shadow,
and the spot was promptly observed. Diffraction also sets a hard limit on image detail: a
circular aperture of diameter D cannot separate features closer than about 1.22 times the
wavelength divided by D, which is why telescopes are built large and microscopes reach for
short wavelengths.[^born-wolf] Polarisation, the fact that the oscillation has a direction
across the line of travel, confirms that light waves are transverse, and is put to work in
sunglasses, stress analysis and liquid-crystal displays.

## An electromagnetic wave

In the 1860s James Clerk Maxwell showed that his equations for the coupled electric and
magnetic fields permit transverse waves whose speed is fixed by two constants measurable in an
electrical laboratory, and that this speed matched the measured speed of light. Light was
therefore electromagnetic radiation, a conclusion reinforced when Heinrich Hertz generated and
detected radio waves in 1887 and 1888.[^britannica-light] The medium those waves were assumed
to need proved undetectable, and the resolution was [[Special relativity|special relativity]],
in which the vacuum speed of light is the same for every inertial observer and no medium is
required.

## Photons

The spectrum of radiation from a hot body resisted every classical explanation until Max
Planck, in 1900, obtained the right formula by allowing energy to be exchanged only in
discrete amounts proportional to frequency. In 1905 Albert Einstein went further and treated
light itself as arriving in quanta, which explained why electrons ejected from an illuminated
metal gain energy according to the frequency of the light rather than its brightness; the 1921
Nobel Prize in Physics was awarded for that work.[^nobel1921] Arthur Compton's X-ray
scattering experiments of 1923 showed that these quanta also carry momentum. A photon of green
light at 500 nanometres carries about 2.5 electronvolts. Sent one at a time through a two-slit
apparatus, individual photons still build up an interference pattern, a result that
[[Quantum mechanics]] describes precisely without making it intuitive.

## Images and instruments

A small hole in the wall of a darkened room throws an inverted image of the scene outside, the
effect exploited by the [[Camera obscura]]. Ibn al-Haytham, working in Cairo in the early
eleventh century, used such observations to argue that vision occurs because light travels
from objects into the eye, overturning the Greek doctrine that the eye emits rays, and treated
the eye as an optical instrument to be analysed.[^alhazen] A converging lens gathers parallel
rays to a focus one focal length away; combinations of lenses gave Europe spectacles from the
late thirteenth century, the telescope Galileo turned on Jupiter in 1610, the compound
microscope, and the camera.

## Light in nature and in art

Plants drive [[Photosynthesis]] with the 400-to-700-nanometre band, almost exactly the visible
range; chlorophyll absorbs strongly in the blue and the red and reflects the green between
them. The solar power reaching the top of Earth's atmosphere averages about 1,361 watts per
square metre.[^kopp-lean] Because scattering by air molecules grows roughly as the inverse
fourth power of wavelength, the daytime sky is blue and the low Sun is red. Painters have
pursued such effects deliberately: the artists of [[Impressionism]] worked outdoors with new
portable pigments to record light and weather, setting unmixed strokes side by side and
leaving the mixing to the eye. The twentieth century added the laser, the optical fibre and
the light-emitting diode, none of which can be designed from the ray or wave pictures alone.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Light",
            "subtitle": "Electromagnetic radiation visible to the human eye",
            "rows": [
                {
                    "kind": "header",
                    "value": "Physical description",
                },
                {
                    "kind": "row",
                    "label": "Character",
                    "value": "Transverse electromagnetic wave, quantised as photons",
                },
                {
                    "kind": "row",
                    "label": "Visible wavelengths",
                    "value": "about 380–750 nanometres",
                },
                {
                    "kind": "row",
                    "label": "Visible frequencies",
                    "value": "about 400–790 terahertz",
                },
                {
                    "kind": "row",
                    "label": "Photon energy",
                    "value": "about 1.6–3.3 electronvolts",
                },
                {
                    "kind": "row",
                    "label": "Speed in vacuum",
                    "value": "299,792,458 metres per second, exact by definition since 1983",
                },
                {
                    "kind": "row",
                    "label": "Speed in water",
                    "value": "about 225,000 kilometres per second",
                },
                {
                    "kind": "header",
                    "value": "Study",
                },
                {
                    "kind": "row",
                    "label": "Field",
                    "value": "Optics, a branch of [[Electromagnetism|electromagnetic theory]]",
                },
                {
                    "kind": "row",
                    "label": "Landmark texts",
                    "value": "Ibn al-Haytham, *Book of Optics* (c. 1021); Newton, *Opticks* (1704)",
                },
                {
                    "kind": "full",
                    "value": "Light carries nearly all the information astronomy has",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "britannica-light",
                "title": "Light",
                "url": "https://www.britannica.com/science/light",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "feynman-optics",
                "title": "Optics: The Principle of Least Time",
                "url": "https://www.feynmanlectures.caltech.edu/I_26.html",
                "authors": "Richard P. Feynman, Robert B. Leighton, Matthew Sands",
                "publisher": "The Feynman Lectures on Physics, Volume I",
                "published_on": "1963",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "si-brochure",
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
                "key": "nist-c",
                "title": "Speed of light in vacuum: CODATA fundamental physical constants",
                "url": "https://physics.nist.gov/cgi-bin/cuu/Value?c",
                "authors": "",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "born-wolf",
                "title": "Principles of Optics, 7th edition",
                "url": "",
                "authors": "Max Born, Emil Wolf",
                "publisher": "Cambridge University Press",
                "published_on": "1999",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-521-64222-4",
                "quote": "",
            },
            {
                "key": "nobel1921",
                "title": "The Nobel Prize in Physics 1921",
                "url": "https://www.nobelprize.org/prizes/physics/1921/summary/",
                "authors": "",
                "publisher": "The Nobel Foundation",
                "published_on": "1921",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "alhazen",
                "title": "Ibn al-Haytham",
                "url": "https://www.britannica.com/biography/Ibn-al-Haytham",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "kopp-lean",
                "title": (
                    "A new, lower value of total solar irradiance: "
                    "Evidence and climate significance"
                ),
                "url": "https://doi.org/10.1029/2010GL045777",
                "authors": "Greg Kopp, Judith L. Lean",
                "publisher": "Geophysical Research Letters 38, L01706",
                "published_on": "2011",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1029/2010GL045777",
                "quote": "",
            },
        ],
        "see_also": [
            "Electromagnetism",
            "Quantum mechanics",
            "Special relativity",
            "Camera obscura",
            "Impressionism",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["optics", "electromagnetic radiation", "photon", "speed of light", "colour"],
    },
    {
        "title": "Special relativity",
        "category": "Physics",
        "categories": ["Mathematics"],
        "short_description": "Einstein's 1905 theory of space, time and motion in inertial frames",
        "summary": (
            "Special relativity, published by Albert Einstein in 1905, derives the behaviour of "
            "space, time and motion from two postulates: that physical laws hold equally in all "
            "inertial frames, and that light has one vacuum speed for every observer."
        ),
        "content": """**Special relativity** is the theory of space, time and motion that follows from two
postulates about inertial observers, published by Albert Einstein in 1905. It discards the
Newtonian assumption of a single universal time shared by all observers. The theory is
special only in the sense of being restricted: it holds where gravity can be neglected, and
was extended to gravitating systems a decade later by [[General relativity]].

## The two postulates

The first postulate, the principle of relativity, holds that the laws of physics take the
same form in every inertial frame, meaning every frame moving uniformly, without acceleration
or rotation.[^sep-iframes] Something like it was already present in the mechanics of
[[Isaac Newton]]: no experiment performed below deck reveals the steady motion of the ship.
The second postulate holds that the speed of light in vacuum has the same value for every
inertial observer, whatever the motion of the source or of the observer.[^einstein1905]

Separately each postulate is unremarkable; together they are incompatible with the everyday
rule that velocities simply add. [[Electromagnetism|Maxwell's equations]] had already singled
out one speed for electromagnetic waves, which implied a preferred frame — the luminiferous
ether — that the Michelson–Morley interferometer experiment of 1887 failed to
detect.[^mm1887] Einstein's response was not to repair the ether but to abandon absolute
time.

## Simultaneity, time and length

The first casualty is simultaneity. Two events that one inertial observer judges to happen at
the same moment in different places are not simultaneous for an observer moving relative to
the first, and which one came first depends on the frame. Only events close enough to be
linked by a signal travelling at or below the speed of light have a frame-independent order,
which is what protects cause and effect.

Everything quantitative follows from the Lorentz factor, the reciprocal of the square root of
one minus the squared ratio of speed to the speed of light. At half the speed of light it is
about 1.15, at nine-tenths about 2.29, and at 0.99 of light speed about 7.09. A clock moving
relative to an observer runs slow by that factor, an effect called time dilation, and a moving
object's extent along its direction of travel is measured as shorter by the same factor. The
relation is symmetrical: each of two observers in relative motion finds the other's clock
slow, and no contradiction arises because they also disagree about which readings are
simultaneous. Velocities combine by a rule under which no sequence of boosts ever reaches the
speed of light.[^feynman-sr]

## Spacetime

In 1908 Hermann Minkowski recast the theory geometrically. Space and time form a single
four-dimensional structure that different observers slice in different ways, and what all of
them agree on is the interval between two events, built from the squared time separation minus
the squared spatial separation. The interval plays the part that distance plays in ordinary
geometry, and the Lorentz transformations are its rotations. Stated this way the content of the
theory is compact: physics is invariant under those transformations.

## Mass and energy

A second paper of 1905 drew out the consequence that a body's energy content contributes to
its inertia, the relation usually written as energy equal to mass times the square of the
speed of light. Because that square is about 9 × 10^16 in SI units, a small mass corresponds
to an enormous energy. The Sun radiates roughly 3.8 × 10^26 watts, which amounts to converting
some four million tonnes of mass into energy every second, and the same bookkeeping accounts
for the energy released in nuclear fission and fusion. In relativistic mechanics energy and
momentum form one four-component quantity; for a massless particle such as a photon it reduces
to energy equal to momentum times the speed of light.

## Evidence

Special relativity is among the most heavily tested theories in physics. Cosmic-ray muons,
whose mean lifetime at rest is 2.2 microseconds, ought to decay within about 660 metres even
at nearly light speed, yet large numbers of them reach sea level from an altitude of some 15
kilometres, because their internal clocks run slow in the frame of the ground; the effect was
measured in 1941 by Bruno Rossi and David Hall.[^rossi-hall] Accelerator physics assumes the
theory throughout, since the beam energy needed to reach a given speed follows the relativistic
formula rather than the Newtonian one.

The most routine confirmation is navigational. The atomic clocks of the
[[Global Positioning System]] orbit at about 3.9 kilometres per second, which makes them lose
roughly 7 microseconds a day to time dilation, while their weaker gravitational potential makes
them gain about 45 microseconds a day for reasons belonging to general relativity. The net gain
of some 38 microseconds a day would ruin positioning within hours, so the satellite oscillators
are deliberately offset before launch.[^ashby2003]

## Scope

Because it treats only inertial frames and ignores gravity, special relativity is a limiting
case rather than a complete account of motion, but it is exact in that limit and is built into
quantum field theory. Newtonian mechanics remains an excellent approximation whenever speeds
are small compared with light: at Earth's orbital speed of about 30 kilometres per second the
Lorentz factor differs from one by roughly five parts in a thousand million. The theory also
fixes the standing of [[Light|light]] itself, whose vacuum speed is not merely the speed of one
kind of wave but the conversion factor between distance and time, and the limit for any signal.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Special relativity",
            "subtitle": "Theory of space and time for inertial observers",
            "rows": [
                {
                    "kind": "row",
                    "label": "Formulated",
                    "value": "1905, by Albert Einstein",
                },
                {
                    "kind": "row",
                    "label": "Founding paper",
                    "value": "On the Electrodynamics of Moving Bodies (*Annalen der Physik* 1905)",
                },
                {
                    "kind": "row",
                    "label": "First postulate",
                    "value": "Physical laws take the same form in every inertial frame",
                },
                {
                    "kind": "row",
                    "label": "Second postulate",
                    "value": "The vacuum speed of light is the same for every inertial observer",
                },
                {
                    "kind": "row",
                    "label": "Main predictions",
                    "value": "Loss of absolute simultaneity, time dilation, length contraction",
                },
                {
                    "kind": "row",
                    "label": "Mass and energy",
                    "value": "Energy equals mass times the square of the speed of light",
                },
                {
                    "kind": "row",
                    "label": "Geometric form",
                    "value": "Minkowski spacetime, 1908",
                },
                {
                    "kind": "row",
                    "label": "Extended by",
                    "value": "[[General relativity]], which adds gravity",
                },
                {
                    "kind": "full",
                    "value": "Satellite navigation must correct for the theory to stay accurate.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "einstein1905",
                "title": "On the Electrodynamics of Moving Bodies",
                "url": "https://www.fourmilab.ch/etexts/einstein/specrel/www/",
                "authors": "Albert Einstein",
                "publisher": "Annalen der Physik 17, 891–921 (English translation)",
                "published_on": "1905",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sep-iframes",
                "title": "Space and Time: Inertial Frames",
                "url": "https://plato.stanford.edu/entries/spacetime-iframes/",
                "authors": "Robert DiSalle",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2020",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "mm1887",
                "title": "Michelson–Morley experiment",
                "url": "https://www.britannica.com/science/Michelson-Morley-experiment",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "feynman-sr",
                "title": "The Special Theory of Relativity",
                "url": "https://www.feynmanlectures.caltech.edu/I_15.html",
                "authors": "Richard P. Feynman, Robert B. Leighton, Matthew Sands",
                "publisher": "The Feynman Lectures on Physics, Volume I",
                "published_on": "1963",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "rossi-hall",
                "title": "Variation of the Rate of Decay of Mesotrons with Momentum",
                "url": "https://doi.org/10.1103/PhysRev.59.223",
                "authors": "Bruno Rossi, David B. Hall",
                "publisher": "Physical Review 59, 223",
                "published_on": "1941",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRev.59.223",
                "quote": "",
            },
            {
                "key": "ashby2003",
                "title": "Relativity in the Global Positioning System",
                "url": "https://doi.org/10.12942/lrr-2003-1",
                "authors": "Neil Ashby",
                "publisher": "Living Reviews in Relativity 6, 1",
                "published_on": "2003",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.12942/lrr-2003-1",
                "quote": "",
            },
        ],
        "see_also": [
            "Light",
            "General relativity",
            "Electromagnetism",
            "Global Positioning System",
            "Isaac Newton",
        ],
        "aliases": ["E=mc2"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["relativity", "spacetime", "Lorentz transformation", "mass-energy equivalence"],
    },
    {
        "title": "General relativity",
        "category": "Physics",
        "categories": ["Astronomy and Space"],
        "short_description": "Einstein's 1915 theory of gravity as the curvature of spacetime",
        "summary": (
            "General relativity, completed by Albert Einstein in 1915, treats gravity not as a "
            "force but as the curvature of spacetime produced by mass and energy. Its predictions "
            "have been confirmed from Mercury's orbit to gravitational waves."
        ),
        "content": """**General relativity** is Albert Einstein's theory of gravitation, completed in 1915, in
which gravity is not a force reaching across space but a manifestation of the curvature of
spacetime produced by mass and energy. It contains [[Special relativity]] as the case in which
gravity is absent, and reproduces Newtonian gravitation wherever fields are weak and motions
slow, while differing measurably in strong fields and at high precision.

## From special relativity to gravity

Special relativity applies only to inertial frames, which left gravity outside it. Einstein's
way in was the observation, which he later called the happiest thought of his life, that a
person in free fall does not feel their own weight. Generalised, this becomes the equivalence
principle: within a small enough region, free fall cannot be distinguished from inertial
motion in the absence of gravity, and a uniformly accelerating frame cannot be distinguished
from a uniform gravitational field. The principle has immediate consequences. A light beam
crossing an accelerating cabin follows a curved path relative to the cabin, so gravity must
bend light; and a clock lower in a gravitational potential must run slow compared with one
higher up.

Making this quantitative took eight years and the differential geometry of Bernhard Riemann,
in which curvature is expressed by tensors and the variational [[Calculus|calculus]] picks out
the straightest available paths. Einstein presented the final field equations to the Prussian
Academy of Sciences in Berlin on 25 November 1915 and published the complete theory the
following year.[^einstein1916]

## The field equations

The field equations relate a measure of curvature at each point of spacetime to the density and
flow of energy and momentum there. The constant of proportionality contains Newton's
gravitational constant divided by the fourth power of the speed of light, which is why even
enormous masses produce only slight curvature. Matter tells spacetime how to curve, and curved
spacetime tells matter how to move, because free bodies follow geodesics, the straightest paths
the geometry allows. A planet is not pulled off a straight line by a force; it follows the
straightest available track through a geometry shaped by the Sun.[^feynman-curved]

The equations are non-linear and couple ten independent quantities, so exact solutions are rare
and valuable. Karl Schwarzschild found the first within weeks, describing the spacetime outside
a static spherical mass. It contains a critical radius, about 3 kilometres for the mass of the
Sun and 9 millimetres for the mass of Earth, later understood as the event horizon of a
[[Black hole|black hole]].

## The classic tests

Three predictions distinguished the theory at once. First, the perihelion of
[[Mercury (planet)|Mercury]] advances about 43 arcseconds per century more than Newtonian
gravity allows, a discrepancy known since the 1850s; Einstein's calculation supplied exactly
the missing amount with no adjustable parameter. Second, starlight grazing the Sun was
predicted to be deflected by 1.75 arcseconds, twice what a naive Newtonian argument gives.
Expeditions to Brazil and to the island of Príncipe photographed the star field around the
darkened Sun during the total [[Solar eclipse]] of 29 May 1919, and the results announced in
London that November favoured the relativistic value.[^eddington1920] Third, clocks deeper in a
gravitational potential were predicted to run slow, an effect confirmed in 1960 by Robert Pound
and Glen Rebka, who measured the frequency shift of gamma rays sent up a 22.5-metre tower at
Harvard.[^pound-rebka]

## Later confirmations

Testing has continued for a century, and the theory has passed every check within experimental
error.[^will2014] Radio signals passing close to the Sun are delayed by the curvature along
their path, an effect predicted in 1964 and now measured to a few parts in a hundred thousand
with spacecraft telemetry. The binary pulsar PSR B1913+16, discovered in 1974, loses orbital
energy at the rate expected if the system radiates gravitational waves. In 2015 the LIGO
detectors recorded the waveform of two merging black holes of roughly 36 and 29 solar masses,
matching the predicted signal.[^ligo2016] In 2019 the Event Horizon Telescope collaboration
published an image of the bright ring around the supermassive black hole at the centre of the
galaxy M87, of the size and shape the theory requires.[^eht2019]

## Consequences

General relativity is the framework in which most of modern astronomy and cosmology is stated.
Gravitational lensing by galaxies and clusters is used routinely to weigh them and to magnify
objects behind them. Applied to a universe filled evenly with matter, the equations admit no
stable static solution, and the expanding models worked out in the 1920s became the basis of
Big Bang cosmology. Within the [[The Solar System|Solar System]] the corrections are small but
not negligible: the orbits of the inner planets are computed relativistically, and satellite
navigation would drift without them.

The theory also marks its own boundary. Its equations produce singularities, points where
curvature grows without limit and the description fails, at the centres of black holes and at
the beginning of the expanding universe. Reconciling it with quantum theory remains unfinished,
and no experiment has yet reached the regime where a quantum theory of gravity would be needed.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "General relativity",
            "subtitle": "Geometric theory of gravitation",
            "rows": [
                {
                    "kind": "row",
                    "label": "Developed",
                    "value": "1907–1915, by Albert Einstein",
                },
                {
                    "kind": "row",
                    "label": "Field equations presented",
                    "value": "25 November 1915, Prussian Academy of Sciences, Berlin",
                },
                {
                    "kind": "row",
                    "label": "Core idea",
                    "value": "Mass and energy curve spacetime; free bodies follow its geodesics",
                },
                {
                    "kind": "row",
                    "label": "Mathematics",
                    "value": "Riemannian geometry and tensor [[Calculus|calculus]]",
                },
                {
                    "kind": "row",
                    "label": "First tests",
                    "value": "Mercury's perihelion advance; 1.75 arcsecond deflection of starlight",
                },
                {
                    "kind": "row",
                    "label": "Further predictions",
                    "value": "Gravitational redshift and lensing, black holes, gravitational waves",
                },
                {
                    "kind": "row",
                    "label": "Newtonian limit",
                    "value": "Recovers [[Isaac Newton|Newtonian]] gravity in weak fields",
                },
                {
                    "kind": "full",
                    "value": "Still the working theory of gravity for astronomy and cosmology.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "einstein1916",
                "title": "The Foundation of the General Theory of Relativity",
                "url": "https://einsteinpapers.press.princeton.edu/",
                "authors": "Albert Einstein",
                "publisher": "Annalen der Physik 49, 769–822; Collected Papers of Einstein",
                "published_on": "1916",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "feynman-curved",
                "title": "Curved Space",
                "url": "https://www.feynmanlectures.caltech.edu/II_42.html",
                "authors": "Richard P. Feynman, Robert B. Leighton, Matthew Sands",
                "publisher": "The Feynman Lectures on Physics, Volume II",
                "published_on": "1964",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "eddington1920",
                "title": (
                    "A Determination of the Deflection of Light by the Sun's Gravitational Field"
                ),
                "url": "https://doi.org/10.1098/rsta.1920.0009",
                "authors": "Frank W. Dyson, Arthur S. Eddington, Charles Davidson",
                "publisher": "Philosophical Transactions of the Royal Society A 220, 291–333",
                "published_on": "1920",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rsta.1920.0009",
                "quote": "",
            },
            {
                "key": "pound-rebka",
                "title": "Apparent Weight of Photons",
                "url": "https://doi.org/10.1103/PhysRevLett.4.337",
                "authors": "Robert V. Pound, Glen A. Rebka Jr.",
                "publisher": "Physical Review Letters 4, 337",
                "published_on": "1960",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevLett.4.337",
                "quote": "",
            },
            {
                "key": "will2014",
                "title": "The Confrontation between General Relativity and Experiment",
                "url": "https://doi.org/10.12942/lrr-2014-4",
                "authors": "Clifford M. Will",
                "publisher": "Living Reviews in Relativity 17, 4",
                "published_on": "2014",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.12942/lrr-2014-4",
                "quote": "",
            },
            {
                "key": "ligo2016",
                "title": "Observation of Gravitational Waves from a Binary Black Hole Merger",
                "url": "https://doi.org/10.1103/PhysRevLett.116.061102",
                "authors": "LIGO Scientific Collaboration and Virgo Collaboration",
                "publisher": "Physical Review Letters 116, 061102",
                "published_on": "2016",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1103/PhysRevLett.116.061102",
                "quote": "",
            },
            {
                "key": "eht2019",
                "title": "Astronomers Capture First Image of a Black Hole",
                "url": "https://www.eso.org/public/news/eso1907/",
                "authors": "Event Horizon Telescope Collaboration",
                "publisher": "European Southern Observatory",
                "published_on": "April 2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Special relativity",
            "Black hole",
            "The Solar System",
            "Mercury (planet)",
            "Solar eclipse",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["gravitation", "spacetime curvature", "relativity", "cosmology"],
    },
]
