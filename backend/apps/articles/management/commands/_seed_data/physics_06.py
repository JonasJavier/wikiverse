"""Physics — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Quantum mechanics",
        "category": "Physics",
        "categories": ["Chemistry and Materials"],
        "short_description": "The physics of matter and energy at atomic and subatomic scales",
        "summary": (
            "Quantum mechanics describes matter and radiation at atomic scales, where energy "
            "comes in discrete quanta and predictions are probabilities rather than "
            "certainties. Assembled between 1900 and 1927, it underpins chemistry, lasers and "
            "semiconductor electronics."
        ),
        "content": """**Quantum mechanics** is the physical theory that describes matter and
radiation at atomic and subatomic scales, where quantities such as energy and angular
momentum occur in discrete units called quanta and where the theory yields probabilities
rather than single definite outcomes. It was assembled between 1900 and 1927 out of
experimental results that classical physics could not accommodate, and it now underlies
atomic and nuclear physics, the whole of chemistry, and the electronics of the semiconductor
industry.

The theory is not a small correction applied to Newtonian mechanics at small scales but a
different account of what a physical state is. A quantum state assigns complex amplitudes to
possible outcomes; the amplitudes for alternative histories add, and can cancel, and the
squared magnitude of the total amplitude gives the probability of each outcome.[^feynman3]
Familiar classical behaviour reappears as an approximation valid whenever the quantities
involved are large compared with the Planck constant, fixed exactly at
6.62607015 × 10⁻³⁴ joule seconds in the 2019 revision of the International System of
Units.[^nist]

## Classical physics and its failures

By 1890 Newtonian mechanics, [[Electromagnetism|Maxwell's electromagnetism]] and
thermodynamics between them accounted for nearly everything that had been measured. Three
results did not fit, and each of them forced a quantum.

The first was the spectrum of thermal radiation. A heated cavity emits [[Light|light]] with a
characteristic distribution across wavelengths. Classical statistical mechanics, applied to
the electromagnetic modes inside the cavity, predicted that the radiated power should grow
without limit at short wavelengths, a conclusion later nicknamed the ultraviolet catastrophe.
On 14 December 1900 Max Planck presented to the German Physical Society a formula that fitted
the measurements across the whole range, obtained by assuming that the cavity's oscillators
could exchange energy only in whole multiples of *hν*, where *ν* is the frequency. Planck
regarded the assumption as a formal device and spent years trying to remove it; he received
the 1918 Nobel Prize in Physics for the discovery of energy quanta.[^planck_nobel]

The second was the photoelectric effect. Light falling on a metal surface ejects electrons,
but below a threshold frequency none are released however bright the beam, and above it the
maximum electron energy depends on frequency rather than intensity. In 1905 Albert Einstein
proposed that light is absorbed in localised quanta of energy *hν*, later called photons. It
was this paper, rather than relativity, that the Nobel committee cited when it awarded him the
1921 prize.[^einstein_nobel]

The third was the atom itself. Ernest Rutherford's scattering experiments established in 1911
that atomic mass and positive charge sit in a tiny central nucleus, a result that reshaped
[[Atomic theory]]. But an electron orbiting such a nucleus should radiate continuously and
spiral inward within a fraction of a nanosecond, and atoms in fact emit only sharp, reproducible
spectral lines.

## The old quantum theory

Niels Bohr's model of 1913 imposed quantisation by hand: the electron was allowed only certain
orbits, identified by an integer, and radiated only when jumping between them. The scheme
reproduced the observed hydrogen lines exactly, with a ground-state binding energy of 13.6
electronvolts, but it could not be extended to helium, said nothing about line intensities and
offered no reason why the rule should hold.

Two experiments pushed further. In 1922 Otto Stern and Walther Gerlach sent a beam of silver
atoms through a strongly non-uniform magnetic field and found that it split into two distinct
beams rather than spreading into a band: the magnetic moment could take only two orientations.
In 1924 Louis de Broglie proposed that matter, like light, has a wavelength, equal to the Planck
constant divided by momentum. Clinton Davisson and Lester Germer confirmed it in 1927 by
diffracting electrons from a nickel crystal, and George Paget Thomson did so independently with
thin foils; the two shared the 1937 Nobel Prize. In 1961 Claus Jönsson carried out the
two-slit experiment with electrons directly, and the interference fringes appeared as predicted.

## The formalism of 1925 to 1927

Werner Heisenberg, recovering from hay fever on the island of Helgoland in June 1925, wrote down
a scheme in which observable quantities are represented by arrays that do not commute; Max Born
and Pascual Jordan recognised these as matrices and developed the result into matrix mechanics.
Early in 1926 Erwin Schrödinger published a wave equation for the electron that gave the same
hydrogen spectrum by very different means, and the two formulations were soon shown to be
equivalent. Born supplied the missing physical reading later in 1926: the squared magnitude of
the wave function is a probability density, a step that put probability into the foundations of the
theory and earned him the 1954 Nobel Prize.

In February 1927 Heisenberg derived the relation that bears his name, in which the product of
the uncertainties in a particle's position and momentum cannot fall below the Planck constant
divided by 4π.[^aip_uncertainty] The limit is not a statement about clumsy instruments; it
follows from the wave description itself, in the same way that a pulse confined to a short time
must contain a broad band of frequencies, which is a fact about the
[[Fourier transform]]. Wolfgang Pauli's exclusion principle of 1925 completed the core: no two
electrons may share the same quantum state. Paul Dirac's relativistic electron equation of 1928
then predicted antimatter, and Carl Anderson identified the positron in cosmic-ray tracks in
1932.

## Measurement and interpretation

The formalism is not in dispute; what it means has been argued over ever since. Between
measurements a state evolves smoothly and reversibly under the Schrödinger equation. A
measurement, in the textbook account, yields one of a set of allowed values with the
probabilities given by the Born rule, and the state afterwards reflects the value obtained.
Where exactly the first description gives way to the second is the measurement problem.

The Copenhagen view associated with Bohr and Heisenberg treats the quantum state as a device for
predicting the results of classically described experiments. Erwin Schrödinger's 1935 thought
experiment, in which a cat's fate is entangled with a decaying atom, was intended to show how
uncomfortable that position becomes when it is scaled up. Later alternatives include Hugh
Everett's 1957 relative-state or many-worlds formulation, the pilot-wave theory of de Broglie and
David Bohm, and explicit collapse models. All of them reproduce the standard predictions, which
is why the debate is philosophical in the strict sense rather than experimental.[^sep_qm] The
theory of decoherence, developed from the 1970s, explains why interference between macroscopically
distinct states becomes unobservable so quickly, without by itself settling the question.

## Entanglement and Bell tests

In 1935 Einstein, Boris Podolsky and Nathan Rosen argued that quantum mechanics must be
incomplete, because measuring one member of a correlated pair appears to fix the state of the
other instantly. Schrödinger named the phenomenon entanglement in the same year. In 1964 John
Stewart Bell showed that the argument could be settled in a laboratory: any theory in which the
outcomes are fixed by local properties carried by the particles obeys an inequality that quantum
mechanics violates.

Stuart Freedman and John Clauser reported a violation in 1972, and Alain Aspect's group at Orsay
tightened the test in 1981 and 1982. Remaining loopholes, in which a hidden signal or a biased
sample could mimic the result, were closed in 2015 by experiments that separated the detectors
far enough for light-speed signalling to be excluded while recording every event; one used
electron spins in diamond 1.3 kilometres apart.[^hensen2015] The 2022 Nobel Prize in Physics went
to Aspect, Clauser and Anton Zeilinger for this line of work.[^nobel2022] Entanglement is now a
resource rather than a puzzle, underlying quantum key distribution and quantum computing.

## What the theory explains

Quantum mechanics is the reason chemistry has the shape it does. Electron shells and the exclusion
principle account for the periods and groups of [[The periodic table|the periodic table]], and for
why the noble gases are inert while the alkali metals are violent. The [[Chemical bond]] is
explained as the sharing or transfer of electrons between overlapping orbitals, first calculated
for the hydrogen molecule by Walter Heitler and Fritz London in 1927. Relativistic corrections to
the quantum description explain specific oddities, including why [[Mercury (element)|mercury]] is
liquid at room temperature: its outermost electron shell is contracted and held tightly, so the
metallic bonding between atoms is unusually weak.

In solids the same mathematics produces energy bands, and the size of the gap between them
separates conductors from insulators and semiconductors. That understanding made
[[The transistor|the transistor]] possible in 1947 and everything built from it since. Tunnelling
through a barrier, forbidden classically, explains alpha decay, a problem the discovery of
radioactivity had opened and George Gamow, Ronald Gurney and Edward Condon solved in 1928; it also
drives hydrogen fusion in stars and is the operating principle of the scanning tunnelling
microscope built by Gerd Binnig and Heinrich Rohrer in 1981. Stimulated emission, which Einstein
identified in 1917, gave the laser in 1960. Counting quantum states also fixed the absolute scale
of [[Entropy|entropy]], which classical thermodynamics could only define up to a constant.

## Scope and limits

Extended to fields, the theory became quantum electrodynamics, for which Richard Feynman, Julian
Schwinger and Sin-Itiro Tomonaga shared the 1965 Nobel Prize; its prediction of the electron's
magnetic moment agrees with measurement to better than one part in a billion, making it the most
precisely tested theory in physics.[^britannica_qm] The same framework, extended to the strong and
weak interactions, produces the Standard Model of particle physics.

Gravity remains outside it. [[General relativity]] describes spacetime as a smooth classical
geometry, and no experimentally tested theory combines the two. The clearest place where the
conflict bites is the [[Black hole|black hole]], where quantum arguments assign a temperature and
an entropy to a purely geometrical horizon.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Quantum mechanics",
            "subtitle": "Physical theory of matter and energy at small scales",
            "rows": [
                {"kind": "header", "value": "Overview"},
                {"kind": "row", "label": "Field", "value": "Physics"},
                {
                    "kind": "row",
                    "label": "Domain",
                    "value": "Atoms, molecules, photons, nuclei, condensed matter",
                },
                {
                    "kind": "row",
                    "label": "Defining constant",
                    "value": "Planck constant, 6.62607015 × 10⁻³⁴ joule seconds (exact)",
                },
                {"kind": "header", "value": "Development"},
                {
                    "kind": "row",
                    "label": "First step",
                    "value": "Planck's quantum hypothesis, 14 December 1900",
                },
                {
                    "kind": "row",
                    "label": "Formalised",
                    "value": "1925–1927 by Heisenberg, Born, Jordan, Schrödinger and Dirac",
                },
                {
                    "kind": "row",
                    "label": "Central equation",
                    "value": "Schrödinger equation, 1926",
                },
                {
                    "kind": "row",
                    "label": "Statistical rule",
                    "value": "Born rule: probability is the squared magnitude of the amplitude",
                },
                {"kind": "header", "value": "Reach"},
                {
                    "kind": "full",
                    "value": (
                        "Explains [[The periodic table|the periodic table]], the "
                        "[[Chemical bond|chemical bond]], lasers, nuclear decay and "
                        "[[The transistor|semiconductor electronics]]."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Hydrogen_Density_Plots.png",
            "alt": (
                "Grid of greyscale plots showing ring-shaped and lobed probability clouds for "
                "an electron in a hydrogen atom"
            ),
            "caption": (
                "Probability densities for the electron in a hydrogen atom across a range of "
                "quantum numbers; brighter regions are where the electron is more likely to be "
                "found."
            ),
            "credit": "PoorLeno, via Wikimedia Commons",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Hydrogen_Density_Plots.png",
        },
        "references": [
            {
                "key": "nist",
                "title": "Planck constant — CODATA recommended value",
                "url": "https://physics.nist.gov/cgi-bin/cuu/Value?h",
                "authors": "",
                "publisher": "National Institute of Standards and Technology",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "planck_nobel",
                "title": "The Nobel Prize in Physics 1918",
                "url": "https://www.nobelprize.org/prizes/physics/1918/summary/",
                "authors": "",
                "publisher": "The Nobel Foundation",
                "published_on": "1918",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "einstein_nobel",
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
                "key": "aip_uncertainty",
                "title": "The Uncertainty Principle (Heisenberg web exhibit)",
                "url": "https://history.aip.org/exhibits/heisenberg/uncertainty-principle.html",
                "authors": "",
                "publisher": "American Institute of Physics, Center for History of Physics",
                "published_on": "1998",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "feynman3",
                "title": "The Feynman Lectures on Physics, Volume III, Chapter 1: Quantum Behavior",
                "url": "https://www.feynmanlectures.caltech.edu/III_01.html",
                "authors": "Richard P. Feynman, Robert B. Leighton, Matthew Sands",
                "publisher": "California Institute of Technology",
                "published_on": "1965",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sep_qm",
                "title": "Quantum Mechanics",
                "url": "https://plato.stanford.edu/entries/qm/",
                "authors": "",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "revised 2021",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "hensen2015",
                "title": (
                    "Loophole-free Bell inequality violation using electron spins separated by "
                    "1.3 kilometres"
                ),
                "url": "https://www.nature.com/articles/nature15759",
                "authors": "B. Hensen and others",
                "publisher": "Nature, volume 526, pages 682–686",
                "published_on": "October 2015",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature15759",
                "quote": "",
            },
            {
                "key": "nobel2022",
                "title": "The Nobel Prize in Physics 2022",
                "url": "https://www.nobelprize.org/prizes/physics/2022/summary/",
                "authors": "",
                "publisher": "The Nobel Foundation",
                "published_on": "2022",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica_qm",
                "title": "Quantum mechanics",
                "url": "https://www.britannica.com/science/quantum-mechanics-physics",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Light",
            "Atomic theory",
            "The periodic table",
            "Chemical bond",
            "The transistor",
            "Electromagnetism",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "quantum physics",
            "wave-particle duality",
            "uncertainty principle",
            "entanglement",
            "history of physics",
        ],
    },
    {
        "title": "Sound",
        "category": "Physics",
        "categories": ["Music and Performance"],
        "short_description": "Mechanical pressure waves in matter, and how they are heard",
        "summary": (
            "Sound is a mechanical wave of pressure variation travelling through a solid, liquid "
            "or gas. Its frequency is heard as pitch, its amplitude as loudness and its harmonic "
            "content as timbre; in air at 20 °C it travels at 343 metres per second."
        ),
        "content": """**Sound** is a mechanical wave consisting of small variations in pressure
that travel through a solid, liquid or gas by displacing the material itself. Because it needs
matter to carry it, sound does not propagate through a vacuum, a point Robert Boyle demonstrated
in 1660 when a bell rung inside an evacuated glass receiver became almost inaudible.[^britannica]
In air the wave is longitudinal: the particles oscillate along the direction of travel, producing
alternating compressions and rarefactions rather than the side-to-side displacement of a wave on a
string.

The pressure changes involved are tiny. Ordinary conversation a metre away corresponds to a
pressure amplitude of roughly two hundredths of a pascal, against an atmospheric pressure of about
101,000 pascals. The quietest sound a healthy young ear can detect is smaller still, near 20
micropascals, which is the reference value from which the decibel scale is defined.

## Speed and medium

In dry air at 20 °C sound travels at 343 metres per second. For an ideal gas the speed depends on
temperature and on the gas's composition but not on pressure, and it rises with the square root of
absolute temperature, so the figure falls to about 331 metres per second at 0 °C. Stiffer media
carry sound faster: roughly 1,480 metres per second in fresh water and about 5,000 metres per
second in steel.[^feynman47] The ratio of an object's speed to the local speed of sound is its Mach
number; past Mach 1 the pressure disturbances can no longer move ahead of the object and pile up
into the shock front heard on the ground as a sonic boom.

## Pitch, loudness and timbre

Frequency is perceived as pitch. A doubling of frequency is an octave, a ratio of exactly two to
one, and the division of that interval into a usable scale is the problem addressed by
[[Equal temperament]]. Modern concert pitch places the A above middle C at 440 hertz.

Loudness is reported in decibels, a logarithmic measure: an increase of 10 decibels is a tenfold
increase in sound intensity, and is usually perceived as roughly a doubling of loudness. The ear
is not equally sensitive across the spectrum, being most responsive between about 2 and 5
kilohertz, so measured level and perceived loudness diverge at the extremes of the audible range.

Timbre is what distinguishes a clarinet from a violin playing the same note at the same level. It
comes from the relative strengths of the harmonics above the fundamental and from how those
strengths change during the attack and decay of the note. Decomposing a waveform into its
component frequencies is exactly the operation performed by the [[Fourier transform]], which is
why that piece of mathematics is central to audio recording, synthesis and compression. Register
matters as much as timbre: the lowest string of an orchestral double bass sounds near 41 hertz,
and the word [[Bass|bass]] covers both that region of the spectrum and the instruments that fill
it. In [[Jazz]] the recorded attack and decay of a plucked bass note carry as much of the
instrument's identity as its pitch.

## Standing waves and resonance

When a wave is confined, reflections from the boundaries interfere with the outgoing wave and only
certain frequencies survive. A string of length *L* fixed at both ends supports a fundamental at
half the wave speed divided by *L*, plus harmonics at whole-number multiples of it; a pipe open at
both ends behaves similarly, while a pipe closed at one end sounds an octave lower for the same
length. Almost every musical instrument is a device for selecting such modes and coupling them to
the air.

Driving a system at one of its natural frequencies produces resonance, in which a small repeated
input builds a large amplitude. Two tones of slightly different frequency produce beats at the
difference frequency, an effect used deliberately in the bronze ensembles of Java and Bali, where
paired instruments of a [[Gamelan]] are tuned a few hertz apart so that each struck note shimmers.

## Hearing and its limits

Human hearing conventionally spans 20 hertz to 20 kilohertz, though the upper limit falls steadily
with age and after noise exposure. Pressure waves below that range are called infrasound and are
produced by volcanic eruptions, large storms and the ground motion of an [[Earthquake]]; elephants
and some whales communicate there. Above it lies ultrasound, used by bats echolocating at well
over 100 kilohertz and by medical scanners working in the megahertz range. The cochlea sorts
incoming frequencies by position along the basilar membrane, so the ear performs a rough
mechanical frequency analysis before the signal reaches the brain.

## In the Earth and the ocean

Seismology treats the Earth as a sounding body. Compressional P waves are longitudinal, like
sound in air, while shear S waves are transverse and cannot pass through a liquid at all; it was
the shadow that S waves cast across the planet that revealed the liquid outer core.[^usgs] In the
ocean a layer of minimum sound speed about a kilometre down acts as a waveguide, trapping low
frequencies so that they travel thousands of kilometres.

## The loudest recorded events

The eruption of [[Krakatoa]] on 27 August 1883 produced the loudest sound in the instrumental
record. It was reported as a distinct noise on Rodrigues Island, some 4,800 kilometres away. A
barograph at the Batavia gasworks, about 160 kilometres from the volcano, registered a pressure
jump of more than 8.5 kilopascals, which corresponds to a sound pressure level of about 172
decibels at that distance.[^symons1888] The atmospheric pulse was picked up by more than fifty
recording stations worldwide and passed some barographs seven times, having travelled around the
globe roughly three and a half times.[^royalsociety]

There is a ceiling on how loud an ordinary sound wave in air can be. Since the rarefaction half of
the cycle cannot reduce the pressure below vacuum, the amplitude of an undistorted wave at sea
level cannot exceed atmospheric pressure, which caps the level at roughly 190 decibels. Anything
more energetic propagates as a shock wave, with a sharp front and a different set of physical
rules.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Sound",
            "subtitle": "Mechanical waves in a material medium",
            "rows": [
                {"kind": "header", "value": "Physical character"},
                {"kind": "row", "label": "Wave type", "value": "Longitudinal pressure wave"},
                {"kind": "row", "label": "Speed in air at 20 °C", "value": "343 metres per second"},
                {
                    "kind": "row",
                    "label": "Speed in fresh water",
                    "value": "About 1,480 metres per second",
                },
                {
                    "kind": "row",
                    "label": "Speed in steel",
                    "value": "About 5,000 metres per second",
                },
                {"kind": "header", "value": "Perception"},
                {"kind": "row", "label": "Audible range", "value": "Roughly 20 Hz to 20 kHz"},
                {
                    "kind": "row",
                    "label": "Decibel reference",
                    "value": "20 micropascals, defined as 0 decibels",
                },
                {
                    "kind": "row",
                    "label": "Concert pitch",
                    "value": "The A above middle C at 440 hertz",
                },
                {
                    "kind": "full",
                    "value": (
                        "Frequency is heard as pitch, amplitude as loudness, and harmonic content "
                        "as timbre."
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                "CPT-sound-physical-manifestation.svg"
            ),
            "alt": (
                "Diagram of a loudspeaker sending bands of compressed and rarefied air towards a "
                "human ear"
            ),
            "caption": (
                "A sound wave travelling through air as alternating compressions and rarefactions, "
                "from a loudspeaker to a listener's ear."
            ),
            "credit": "Pluke, via Wikimedia Commons",
            "license": "CC0 1.0",
            "source_url": (
                "https://commons.wikimedia.org/wiki/File:CPT-sound-physical-manifestation.svg"
            ),
        },
        "references": [
            {
                "key": "britannica",
                "title": "Sound (physics)",
                "url": "https://www.britannica.com/science/sound-physics",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "feynman47",
                "title": (
                    "The Feynman Lectures on Physics, Volume I, Chapter 47: Sound. The wave "
                    "equation"
                ),
                "url": "https://www.feynmanlectures.caltech.edu/I_47.html",
                "authors": "Richard P. Feynman, Robert B. Leighton, Matthew Sands",
                "publisher": "California Institute of Technology",
                "published_on": "1963",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "usgs",
                "title": "The Science of Earthquakes",
                "url": "https://www.usgs.gov/programs/earthquake-hazards/science-earthquakes",
                "authors": "",
                "publisher": "United States Geological Survey",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "symons1888",
                "title": (
                    "The Eruption of Krakatoa, and Subsequent Phenomena: Report of the Krakatoa "
                    "Committee of the Royal Society"
                ),
                "url": "",
                "authors": "G. J. Symons (editor)",
                "publisher": "Trübner and Co., London",
                "published_on": "1888",
                "accessed_on": "",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "royalsociety",
                "title": "Crowdsourcing Krakatoa",
                "url": "https://royalsociety.org/blog/2024/01/crowdsourcing-krakatoa/",
                "authors": "",
                "publisher": "The Royal Society",
                "published_on": "January 2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Fourier transform",
            "Equal temperament",
            "Earthquake",
            "Krakatoa",
            "Gamelan",
            "Bass",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["acoustics", "waves", "hearing", "pitch", "resonance"],
    },
    {
        "title": "The Solar System",
        "category": "Astronomy and Space",
        "categories": ["Physics"],
        "short_description": "The Sun and everything gravitationally bound to it",
        "summary": (
            "The Solar System is the Sun together with the eight planets, their moons and the "
            "small bodies bound to it by gravity. It condensed from a disc of gas and dust about "
            "4.6 billion years ago and spans thousands of astronomical units."
        ),
        "content": """**The Solar System** is the Sun together with everything held in orbit
around it: eight planets, five recognised dwarf planets, hundreds of moons, and an uncounted
population of asteroids, comets and dust. It condensed from a rotating disc of gas and dust about
4.6 billion years ago, and its gravitational reach extends outward for tens of thousands of times
the Earth–Sun distance.

## The Sun

The Sun holds about 99.8 per cent of the mass of the system and supplies effectively all of its
light and heat.[^nasa_sun] It is an unremarkable main-sequence star of spectral type G2, with a
radius near 700,000 kilometres and a mass equal to more than 330,000 Earths. Its visible surface,
the photosphere, has a temperature near 5,500 °C, while the core reaches roughly 15 million °C,
hot enough to fuse hydrogen into helium.[^nasa_sun] The resulting output of about
3.8 × 10²⁶ watts corresponds to converting some four million tonnes of matter into energy every
second. Light from the photosphere takes 8 minutes and 20 seconds to reach Earth.

Because the Sun dominates the mass so completely, every other body moves, to a good first
approximation, on a conic section around it. That this follows from a single inverse-square law of
gravitation was the central demonstration of [[Isaac Newton|Newton]]'s *Principia* of 1687.

## What counts as a planet

The word planet had no formal definition until the International Astronomical Union adopted
Resolution B5 on 24 August 2006. A planet must orbit the Sun, must be massive enough for its own
gravity to pull it into a nearly round shape, and must have cleared the neighbourhood around its
orbit. Bodies meeting the first two conditions but not the third became dwarf planets, a category
that includes Ceres in the asteroid belt and Pluto, Haumea, Makemake and Eris beyond
Neptune.[^iau_b5] The decision was contested, but it followed directly from the discovery of
Pluto-sized objects in the outer system.

## The inner planets

The four inner planets are rock-and-metal bodies with thin atmospheres or none.
[[Mercury (planet)|Mercury]], only 4,879 kilometres across, is the smallest, retains almost no
atmosphere, and is locked in a three-to-two resonance between its spin and its orbit; its surface
swings between roughly 430 °C in daylight and −180 °C at night. Venus is nearly Earth's twin in
size but
carries a carbon dioxide atmosphere that presses down at about 92 times Earth's sea-level pressure
and holds its surface near 465 °C. Earth is the only body known to have liquid [[Water|water]] on
its surface and active [[Plate tectonics|plate tectonics]]. Mars, half Earth's diameter, has the
system's largest volcano, Olympus Mons, standing some 22 kilometres above the surrounding plains.

Earth's Moon, 3,475 kilometres across, is unusually large relative to its planet. By coincidence
its angular diameter in the sky is very nearly that of the Sun, which is the only reason total
[[Solar eclipse|solar eclipses]] occur at all.

## The giant planets

Jupiter contains 318 Earth masses, more than twice as much material as everything else in orbit
around the Sun combined, and is composed mostly of hydrogen and helium with no solid surface. Its
Great Red Spot is a storm that has been observed for well over a century. Saturn is less dense
than water and is encircled by a ring system some 280,000 kilometres across but in most places
only tens of metres thick, made overwhelmingly of water ice.[^nssdc]

Uranus and Neptune, often distinguished as ice giants, contain proportionally more water, ammonia
and methane. Uranus is tipped on its side, with an axial tilt near 98 degrees. Neptune was found
by prediction rather than by survey: discrepancies in Uranus's motion led Urbain Le Verrier to
compute a position, and Johann Gottfried Galle observed the planet within a degree of it on 23
September 1846. At 30 astronomical units from the Sun, Neptune takes 165 years to complete one
orbit.

## Moons

Jupiter and Saturn each have scores of confirmed satellites, and the tallies keep climbing as
surveys reach smaller objects; one announcement in 2025 added more than a hundred small moons to
Saturn's list alone. A handful are worlds in their own right. Ganymede, at 5,268 kilometres, is
larger than Mercury. Titan has a nitrogen atmosphere denser than Earth's at the surface, with
rivers and lakes of liquid methane and ethane; the Huygens probe landed there on 14 January 2005.
Io is the most volcanically active body in the system, kneaded by tidal forces from Jupiter.
Europa and Enceladus both appear to hold liquid water beneath an ice shell, and the Cassini
orbiter flew directly through plumes erupting from Enceladus's south polar fractures.

## Small bodies and the outer reaches

Most asteroids occupy a belt between Mars and Jupiter, roughly 2 to 3.3 astronomical units out.
Despite their number, their combined mass is only a few per cent of the Moon's, and Ceres alone,
about 940 kilometres across, accounts for a large share of it. Fragments that survive the fall to
Earth as meteorites are the only hand samples of the early system apart from lunar and Martian
rock. Comets are bodies of ice and dust that grow a coma and a tail when solar heating drives off
their volatiles; those on short orbits are steadily eroded, while long-period comets arrive from
far outside the planetary region.

Beyond Neptune lies the Kuiper belt, a flattened population of icy bodies from about 30 to 50
astronomical units, of which Pluto — 2,377 kilometres in diameter, as measured by New Horizons
during its flyby on 14 July 2015 — is the best studied.[^nasa_nh] Further out, the Oort cloud is
inferred rather than observed: a roughly spherical reservoir of comet nuclei, thousands of
astronomical units away, whose existence explains the orbits of long-period comets.

The solar wind carves a bubble in the interstellar medium called the heliosphere. Its outer
boundary, the heliopause, was crossed by Voyager 1 on 25 August 2012 at about 122 astronomical
units and by Voyager 2 on 5 November 2018; the [[Voyager program]] remains the only source of
direct measurements from beyond it.[^nasa_voyager]

## Formation

The modern account descends from the nebular hypothesis of Immanuel Kant in 1755 and Pierre-Simon
Laplace in 1796. A fragment of a cold molecular cloud collapsed under its own gravity; conservation
of angular momentum flattened the infalling material into a disc, with most of the mass settling
into the growing Sun. Within the disc, dust grains stuck together and grew into kilometre-scale
planetesimals, which collided and merged. Inside the frost line only rock and metal could condense,
producing small dense planets; beyond it ices were available as well, so the growing cores were
large enough to capture hydrogen and helium directly from the disc.

The timing is read from meteorites: the oldest solids in primitive chondrites, calcium- and
aluminium-rich inclusions, date to about 4.567 billion years ago. Models of the giant planets'
subsequent migration are used to explain the structure of the asteroid belt and the Kuiper belt.
The process is no longer purely theoretical. In 2014 the ALMA array imaged concentric rings and
gaps in the disc around the young star HL Tauri, apparently carved by forming planets.[^eso_hltau]
More than 5,000 planets around other stars had been confirmed by March 2022, and the diversity of
those systems has made the Solar System's own arrangement look like one outcome among many rather
than a template.[^exo_archive]

## The scale of it

The astronomical unit, defined since 2012 as exactly 149,597,870.7 kilometres, is the working ruler
for the system.[^nasa_ss] The distances it measures resist intuition. Shrink the Sun to a sphere one
metre across and the Earth becomes a bead nine millimetres wide, 108 metres away; Neptune sits 3.2
kilometres out. On that same scale the nearest star, Proxima Centauri, would be about 29,000
kilometres distant, roughly three-quarters of the way around the Earth.

## Reading the system

Predicting where the planets would be mattered long before anyone knew what they were. The
[[The Antikythera mechanism|Antikythera mechanism]], built in the second or first century BC, used
bronze gearwork to model the motions of the Sun and Moon and to predict eclipses. Ptolemaic
astronomy placed the Earth at the centre and accounted for the observations with nested circles;
the shift to a Sun-centred arrangement, traced in [[The Copernican Revolution]], took more than a
century and required [[Galileo Galilei|Galileo]]'s telescopic evidence and Kepler's elliptical
orbits before Newton supplied the underlying dynamics.

One residual discrepancy outlasted Newton. Mercury's perihelion advances by about 43 arcseconds
per century more than Newtonian gravitation predicts, a mismatch that was explained only when
[[General relativity]] recast gravity as the curvature of spacetime. Systematic exploration by
spacecraft began in 1959, and every planet has now been visited at least once.[^nasa_ss]
""",
        "tier": "feature",
        "kind": "place",
        "infobox": {
            "title": "The Solar System",
            "subtitle": "The Sun and the bodies bound to it by gravity",
            "rows": [
                {"kind": "header", "value": "Overview"},
                {
                    "kind": "row",
                    "label": "Central star",
                    "value": "The Sun, a G2 main-sequence star holding about 99.8% of the mass",
                },
                {"kind": "row", "label": "Age", "value": "About 4.6 billion years"},
                {
                    "kind": "row",
                    "label": "Planets",
                    "value": "Eight, under the IAU definition adopted in 2006",
                },
                {
                    "kind": "row",
                    "label": "Dwarf planets",
                    "value": "Five recognised: Ceres, Pluto, Haumea, Makemake and Eris",
                },
                {"kind": "header", "value": "Dimensions"},
                {
                    "kind": "row",
                    "label": "Astronomical unit",
                    "value": "149,597,870.7 km, exactly, by definition since 2012",
                },
                {
                    "kind": "row",
                    "label": "Neptune's orbit",
                    "value": "About 30 astronomical units, one circuit in 165 years",
                },
                {
                    "kind": "row",
                    "label": "Heliopause",
                    "value": "Crossed by Voyager 1 at about 122 astronomical units",
                },
                {
                    "kind": "row",
                    "label": "Nearest star",
                    "value": "Proxima Centauri, about 4.25 light-years away",
                },
                {"kind": "header", "value": "Exploration"},
                {
                    "kind": "full",
                    "value": (
                        "Visited by robotic spacecraft since 1959; both probes of the "
                        "[[Voyager program]] are now beyond the heliopause."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Planets2013.svg",
            "alt": (
                "The eight planets arranged in a row, drawn at their relative sizes, with the "
                "giant planets dwarfing the rocky ones"
            ),
            "caption": (
                "The eight planets shown at their relative sizes. Distances and positions are not "
                "to scale."
            ),
            "credit": "WP and PlanetUser, via Wikimedia Commons",
            "license": "CC BY-SA 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:Planets2013.svg",
        },
        "references": [
            {
                "key": "nasa_ss",
                "title": "Solar System",
                "url": "https://science.nasa.gov/solar-system/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa_sun",
                "title": "Sun: Facts",
                "url": "https://science.nasa.gov/sun/facts/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "The Sun accounts for 99.8% of our solar system's mass.",
            },
            {
                "key": "nssdc",
                "title": "Planetary Fact Sheet",
                "url": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/",
                "authors": "",
                "publisher": "NASA Space Science Data Coordinated Archive",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "iau_b5",
                "title": "Resolution B5: Definition of a Planet in the Solar System",
                "url": "https://iauarchive.eso.org/static/resolutions/Resolution_GA26-5-6.pdf",
                "authors": "",
                "publisher": "International Astronomical Union, 26th General Assembly",
                "published_on": "24 August 2006",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa_voyager",
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
                "key": "nasa_nh",
                "title": "New Horizons",
                "url": "https://science.nasa.gov/mission/new-horizons/",
                "authors": "",
                "publisher": "NASA Science",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "eso_hltau",
                "title": "Revolutionary ALMA Image Reveals Planetary Genesis",
                "url": "https://www.eso.org/public/news/eso1436/",
                "authors": "",
                "publisher": "European Southern Observatory, release eso1436",
                "published_on": "6 November 2014",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "exo_archive",
                "title": "NASA Exoplanet Archive",
                "url": "https://exoplanetarchive.ipac.caltech.edu/",
                "authors": "",
                "publisher": "NASA Exoplanet Science Institute, Caltech",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Mercury (planet)",
            "The Copernican Revolution",
            "Voyager program",
            "Solar eclipse",
            "General relativity",
            "The Antikythera mechanism",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "solar system",
            "planets",
            "the Sun",
            "planetary formation",
            "space exploration",
        ],
    },
]
