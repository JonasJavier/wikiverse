"""Mathematics — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Chaos theory",
        "category": "Mathematics",
        "categories": ["Physics", "Earth and Environment"],
        "short_description": "Deterministic systems whose long-run behaviour resists prediction",
        "summary": (
            "Chaos theory studies deterministic systems in which arbitrarily small "
            "differences in the starting state grow exponentially, so that long-term "
            "behaviour becomes unpredictable in practice while remaining bounded and "
            "statistically describable."
        ),
        "content": """**Chaos theory** is the study of deterministic systems whose
long-term behaviour cannot be predicted in practice, because arbitrarily small differences
between two starting states grow exponentially as the systems evolve. A chaotic system
contains no randomness: its
equations fix its entire future from any given instant. What it lacks is stability with respect
to measurement error, and because every physical measurement has finite precision, that lack is
enough to place the distant future beyond reach.

Chaotic behaviour is common rather than exotic. It has been identified in dripping taps, stirred
fluids, driven pendulums, electrical circuits, insect populations, the tumbling of small moons
and the orbits of the planets. Its discovery did not overturn the deterministic mechanics of
[[Isaac Newton]]; it clarified what determinism does and does not buy. Pierre-Simon Laplace's
claim of 1814 — that an intellect knowing every particle's position and velocity could compute
the whole future — remains formally correct and practically void, because "knowing" would have
to mean knowing exactly. The word *chaos* entered mathematics in its technical sense with a 1975
paper by Tien-Yien Li and James Yorke on iterated maps of an interval.[^liyorke]

## Sensitive dependence on initial conditions

The defining property is sensitive dependence on initial conditions. Two trajectories separated
at the start by a small distance `d0` diverge on average like `d0 · e^(λt)`, where `λ` is the
largest Lyapunov exponent; chaos requires `λ > 0`. Its reciprocal, the Lyapunov time, is the
interval over which an error grows by a factor of about 2.7.

Because the growth is exponential rather than proportional to elapsed time, refinements in the
initial data pay poorly. Reducing the initial error by a factor of a thousand extends the usable
forecast by only about seven Lyapunov times, and reducing it by a further factor of a thousand
buys the same modest extension again. Improved instruments push the horizon outward at a
logarithmic crawl.

Sensitive dependence alone is not sufficient. A trajectory that simply flies apart also
amplifies error without being chaotic. The definition that became standard, set out by Robert L.
Devaney, requires in addition that the motion be topologically transitive — any region of the
accessible state space is eventually carried into any other — and that periodic orbits be dense
within it.[^strogatz] Chaos is therefore local instability combined with global confinement:
trajectories are pulled back again and again into the same bounded region while being stretched
apart inside it.

## Poincaré and the three-body problem

[[Calculus]] gave Newton an exact solution for two gravitating bodies. Three resisted. In 1885 a
prize competition was announced under the patronage of Oscar II of Sweden, one of whose
questions concerned the stability of the Solar System, and Henri Poincaré's memoir on the
three-body problem took the prize in 1889. While the text was in press the editor Lars Edvard
Phragmén queried a passage; Poincaré's attempt to repair it showed that curves he had assumed to
close smoothly instead crossed one another in an infinitely intricate web. He had the printed
sheets destroyed and paid for the reprinting himself, at more than the value of the prize, and
the corrected memoir appeared in *Acta Mathematica* in 1890.[^barrowgreen]

Poincaré also drew the practical moral. In *Science et méthode* (1908) he observed that a tenth
of a degree more or less at some point could decide where a cyclone would form, and that a
forecaster who could not measure that tenth of a degree would appear simply to have failed.

## Lorenz and the convection model

Edward Lorenz (1917–2008), a meteorologist at the Massachusetts Institute of Technology, met the
phenomenon by accident. In 1961, running a twelve-equation model of the atmosphere on a Royal
McBee LGP-30, he restarted a computation from an intermediate state copied off a printout,
entering 0.506 where the machine's internal value had been 0.506127. The re-run tracked the
original for a while and then diverged from it entirely.[^gleick]

In 1963 Lorenz published "Deterministic nonperiodic flow", reducing a seven-equation model of
Rayleigh–Bénard convection studied by Barry Saltzman to three ordinary differential equations:

```
dx/dt = σ(y − x)
dy/dt = x(ρ − z) − y
dz/dt = xy − βz
```

Here `x` measures the intensity of convective overturning while `y` and `z` measure horizontal
and vertical temperature variation. With `σ = 10`, `ρ = 28` and `β = 8/3` the solution never
repeats, never settles and never leaves a bounded region. Plotted in three dimensions it winds
around two lobes, switching between them in no repeating order — the set now called the Lorenz
attractor, whose Hausdorff dimension has been estimated at about 2.06.[^lorenz]

Lorenz's paper reported a colleague's remark that if the theory held, a single flap of a sea
gull's wings would be enough to change the weather permanently.[^lorenz] The sea gull became a
butterfly in December 1972, when Lorenz addressed the 139th meeting of the American Association
for the Advancement of Science under a title proposed by Philip Merilees, asking whether the flap
of a butterfly's wings in Brazil could set off a tornado in Texas.[^gleick]

## The logistic map and universality

Chaos needs neither many variables nor continuous time. The logistic map,
`x(n+1) = r · x(n) · (1 − x(n))`, is a single line of arithmetic modelling a population limited
by its own crowding. For `r` below 1 the population dies out; between 1 and 3 it settles on a
single value; at `r = 3` that value loses stability and the sequence alternates between two.
Further doublings follow at `r = 1 + √6 ≈ 3.4495`, then near 3.5441, then in ever-shorter
intervals accumulating at about 3.5699. Above that point orbits are aperiodic for most parameter
values, interrupted by narrow windows of periodic behaviour.

Robert May's 1976 review in *Nature* put this before a large biological readership with the
warning that erratic field data need not indicate a noisy environment: the simplest plausible
model of a seasonally breeding population generates erratic series on its own.[^may]

Mitchell Feigenbaum, working at Los Alamos from 1975, found that the parameter intervals between
successive doublings shrink by a constant factor `δ = 4.669201609…`, and that the same constant,
together with a scaling ratio `α = 2.502907875…`, governs every map with a single smooth
quadratic maximum whatever its algebraic form.[^feigenbaum] That universality gives chaos
quantitative predictions of its own, and the ratios have since been measured in convecting
fluids, oscillating chemical reactions and driven electronic circuits.

## Strange attractors

David Ruelle and Floris Takens named the *strange attractor* in a 1971 paper arguing that fluid
turbulence arises when a system's trajectories settle onto such a set, rather than through the
accumulation of independent oscillation modes.[^ruelletakens] An attractor is a set that nearby
trajectories approach; a strange attractor is one with fractal structure, so that magnifying a
small piece reveals further layering at every scale.

The geometry follows from the arithmetic. A dissipative chaotic system shrinks volumes in state
space overall while stretching them along at least one direction, so the stretched sheet must be
folded back into the bounded region — the operation Stephen Smale formalised as the horseshoe
map. Repeated stretching and folding produces an infinitely laminated object of non-integer
dimension. One practical consequence is that a chaotic signal has a broad continuous power
spectrum rather than the discrete lines of a periodic one, which is how chaos is often first
identified in laboratory data through the [[Fourier transform]].

## Measuring and describing chaos

Because individual trajectories are not reproducible, chaotic systems are described
statistically, which makes [[Probability theory]] a working tool rather than a concession. A
chaotic attractor typically carries an invariant measure — a stable long-run distribution of the
time the trajectory spends in each region — and averages taken against that measure are
repeatable even though the path is not.

The rate at which a chaotic system destroys information about its own past is the
Kolmogorov–Sinai entropy, which for a broad class of systems equals the sum of the positive
Lyapunov exponents. The quantity connects dynamics directly to [[Entropy]] in the statistical
sense and to the coding arguments of [[Information theory]]: a chaotic system can be read as a
source emitting a fixed number of bits of new information per unit time, and no forecast can
outrun that rate.

Lyapunov times vary enormously with the system. Errors in atmospheric forecasts double in a
matter of days; the orbits of the inner planets have a Lyapunov time of a few million years; the
orbit of Pluto has one of roughly twenty million.

## Predictability in practice

The response in weather forecasting has been to abandon the single best forecast. Operational
centres run ensembles: the same model started from many slightly different initial states chosen
to sample the uncertainty in the observations. Where the members stay together the forecast is
confident; where they fan out it is not, and the spread itself is part of the product. Lorenz's
own estimate that mid-latitude weather has a deterministic prediction limit of about two weeks
has proved durable.

The distinction between weather and climate follows from the same structure. The shape and
statistics of an attractor can be stable and computable even when no trajectory on it is
predictable, so long-run averages of temperature, rainfall and circulation — the quantities that
organise [[The water cycle]] — are a different and more tractable question than next month's
weather.

Chaos also sets the horizon for celestial mechanics. Numerical integrations show that the orbits
of the inner planets of [[The Solar System]] are chaotic. In 2009 Jacques Laskar and Mickaël
Gastineau integrated 2,501 slightly differing solutions forward five billion years and found
that about one per cent produced an increase in Mercury's eccentricity large enough to permit a
collision with Venus or the Sun.[^laskar] The system is stable in the sense that it has held
together for some 4.5 billion years, and unpredictable in the sense that its detailed
configuration a hundred million years hence cannot be computed.

Convection is the same mathematics Lorenz truncated, and models of the mantle flow that drives
[[Plate tectonics]] show comparable sensitivity, which is one reason such models are run as
families of possibilities rather than as single predictions.

## Common misreadings

Chaos is not randomness. A chaotic sequence is produced by a fixed rule and repeats exactly if
its initial state is repeated exactly; the unpredictability lies in the impossibility of
specifying that state exactly, not in the rule.

Chaos is not disorder. A chaotic system's state is tightly constrained: it stays on its
attractor, and the attractor has a definite geometry, a definite dimension and definite
statistics.

The butterfly effect is not a claim about causation. It compares two histories differing by one
flap and notes that the difference between them grows without bound. It does not say the flap
caused the tornado, and in an atmosphere containing countless such perturbations the contribution
of any single one is not separable.

Chaos is not universal among nonlinear systems. The Kolmogorov–Arnold–Moser theorem shows that
under a small enough perturbation most of the regular orbits of an integrable system survive, so
regular and chaotic motion coexist in the same system at different energies and
parameters.[^strogatz]

Finally, unpredictability has a scale. Chaotic forecasts degrade progressively rather than
failing all at once, and they degrade differently for different quantities: the tenth day's
temperature may be out of reach while the season's mean, and the physical bounds on both, remain
secure.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Chaos theory",
            "subtitle": "Branch of nonlinear dynamics",
            "rows": [
                {"kind": "row", "label": "Field", "value": "Dynamical systems; nonlinear dynamics"},
                {
                    "kind": "row",
                    "label": "Defining property",
                    "value": (
                        "Sensitive dependence on initial conditions in a bounded, "
                        "mixing, deterministic system"
                    ),
                },
                {
                    "kind": "row",
                    "label": "Key measure",
                    "value": "Largest Lyapunov exponent; a positive value indicates chaos",
                },
                {"kind": "header", "value": "Landmarks"},
                {
                    "kind": "row",
                    "label": "1890",
                    "value": "Poincaré's revised three-body memoir describes tangled orbits",
                },
                {
                    "kind": "row",
                    "label": "1963",
                    "value": "Lorenz publishes a convection model with no periodic solution",
                },
                {
                    "kind": "row",
                    "label": "1971",
                    "value": "Ruelle and Takens name the *strange attractor*",
                },
                {
                    "kind": "row",
                    "label": "1975",
                    "value": "Li and Yorke introduce *chaos* as a technical term",
                },
                {
                    "kind": "row",
                    "label": "1978",
                    "value": "Feigenbaum publishes the universal period-doubling ratio δ ≈ 4.6692",
                },
                {"kind": "header", "value": "Characteristic quantities"},
                {
                    "kind": "row",
                    "label": "Lorenz attractor",
                    "value": "Hausdorff dimension estimated near 2.06",
                },
                {
                    "kind": "row",
                    "label": "Logistic map",
                    "value": "Aperiodic behaviour above r ≈ 3.5699",
                },
                {
                    "kind": "full",
                    "value": (
                        "Predictability horizons range from days for mid-latitude weather to a "
                        "few million years for the inner planets of [[The Solar System]]."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Lorenz_attractor_yb.svg",
            "alt": "A two-lobed looping curve resembling a pair of butterfly wings",
            "caption": "The Lorenz attractor, plotted for σ = 10, ρ = 28 and β = 8/3",
            "credit": "Wikimol and Dschwen",
            "license": "CC BY-SA 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:Lorenz_attractor_yb.svg",
        },
        "references": [
            {
                "key": "lorenz",
                "title": "Deterministic Nonperiodic Flow",
                "url": "https://doi.org/10.1175/1520-0469(1963)020%3C0130%3ADNF%3E2.0.CO;2",
                "authors": "Edward N. Lorenz",
                "publisher": "Journal of the Atmospheric Sciences, vol. 20, pp. 130–141",
                "published_on": "1963",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "liyorke",
                "title": "Period Three Implies Chaos",
                "url": "https://www.jstor.org/stable/2318254",
                "authors": "Tien-Yien Li and James A. Yorke",
                "publisher": "The American Mathematical Monthly, vol. 82, pp. 985–992",
                "published_on": "1975",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "may",
                "title": "Simple mathematical models with very complicated dynamics",
                "url": "https://doi.org/10.1038/261459a0",
                "authors": "Robert M. May",
                "publisher": "Nature, vol. 261, pp. 459–467",
                "published_on": "1976",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/261459a0",
                "quote": "",
            },
            {
                "key": "ruelletakens",
                "title": "On the nature of turbulence",
                "url": "https://doi.org/10.1007/BF01646553",
                "authors": "David Ruelle and Floris Takens",
                "publisher": "Communications in Mathematical Physics, vol. 20, pp. 167–192",
                "published_on": "1971",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1007/BF01646553",
                "quote": "",
            },
            {
                "key": "feigenbaum",
                "title": "Quantitative universality for a class of nonlinear transformations",
                "url": "https://doi.org/10.1007/BF01020332",
                "authors": "Mitchell J. Feigenbaum",
                "publisher": "Journal of Statistical Physics, vol. 19, pp. 25–52",
                "published_on": "1978",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1007/BF01020332",
                "quote": "",
            },
            {
                "key": "laskar",
                "title": (
                    "Existence of collisional trajectories of Mercury, Mars and Venus "
                    "with the Earth"
                ),
                "url": "https://doi.org/10.1038/nature08096",
                "authors": "Jacques Laskar and Mickaël Gastineau",
                "publisher": "Nature, vol. 459, pp. 817–819",
                "published_on": "June 2009",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature08096",
                "quote": "",
            },
            {
                "key": "barrowgreen",
                "title": "Poincaré and the Three Body Problem",
                "url": "",
                "authors": "June Barrow-Green",
                "publisher": "American Mathematical Society",
                "published_on": "1997",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-8218-0367-7",
                "quote": "",
            },
            {
                "key": "strogatz",
                "title": "Nonlinear Dynamics and Chaos, 2nd edition",
                "url": "",
                "authors": "Steven H. Strogatz",
                "publisher": "Westview Press",
                "published_on": "2015",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-8133-4910-7",
                "quote": "",
            },
            {
                "key": "gleick",
                "title": "Chaos: Making a New Science",
                "url": "",
                "authors": "James Gleick",
                "publisher": "Penguin Books",
                "published_on": "1987",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-14-009250-9",
                "quote": "",
            },
        ],
        "see_also": [
            "Probability theory",
            "Entropy",
            "Calculus",
            "The Solar System",
            "Plate tectonics",
            "Möbius strip",
        ],
        "aliases": ["Butterfly effect"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "dynamical systems",
            "nonlinear dynamics",
            "Lorenz attractor",
            "predictability",
            "fractals",
        ],
    },
    {
        "title": "Möbius strip",
        "category": "Mathematics",
        "categories": [],
        "short_description": "A surface with one side and one edge",
        "summary": (
            "The Möbius strip is a surface with a single side and a single boundary curve, "
            "made by joining the ends of a rectangle after a half-twist. It is the standard "
            "example of a non-orientable surface."
        ),
        "content": """**The Möbius strip** is a surface with only one side and only one edge,
obtained by giving a long rectangle a half-twist and joining its ends. A line drawn down the
middle returns to its starting point having covered what would be both faces of an untwisted
band, and the rim forms a single closed boundary curve. Its Euler characteristic is zero.

It is the standard example of a non-orientable surface, one on which no consistent choice of
"clockwise" can be made everywhere, so that a shape slid once around the band comes back as its
own mirror image. Orientability belongs to topology rather than to the metric geometry of
[[Euclid's Elements]]: it survives any bending or stretching, and the same global question arises
for the spacetime models of [[General relativity]]. August Ferdinand Möbius and Johann Benedict
Listing described the surface independently in 1858; Listing published first, in 1861, while
Möbius's account appeared only after his death.[^mactutor]

Cutting the strip along its centre line does not separate it: the result is one longer two-sided
band carrying four half-twists. A cut a third of the way in yields two interlocked loops, the
narrower of them another Möbius strip.[^mathworld]
""",
        "tier": "stub",
        "kind": "concept",
        "infobox": None,
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/d/d9/M%C3%B6bius_strip.jpg",
            "alt": "A loop of green paper given a half-twist before its ends were joined",
            "caption": "A paper Möbius strip, about 28 cm long",
            "credit": "David Benbennick",
            "license": "CC BY-SA 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:M%C3%B6bius_strip.jpg",
        },
        "references": [
            {
                "key": "mactutor",
                "title": "August Ferdinand Möbius",
                "url": "https://mathshistory.st-andrews.ac.uk/Biographies/Mobius/",
                "authors": "J. J. O'Connor and E. F. Robertson",
                "publisher": "MacTutor History of Mathematics Archive, University of St Andrews",
                "published_on": "1997",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "mathworld",
                "title": "Möbius Strip",
                "url": "https://mathworld.wolfram.com/MoebiusStrip.html",
                "authors": "Eric W. Weisstein",
                "publisher": "Wolfram MathWorld",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": ["Euclid's Elements", "Chaos theory", "General relativity"],
        "aliases": [],
        "is_stub": True,
        "is_disambiguation": False,
        "tags": ["topology", "surfaces", "orientability"],
    },
    {
        "title": "Isaac Newton",
        "category": "Physics",
        "categories": ["Mathematics", "History"],
        "short_description": "English mathematician who unified terrestrial and celestial motion",
        "summary": (
            "Isaac Newton (1642–1727) set out the laws of motion and universal gravitation in "
            "the Principia of 1687, founded modern optics, invented a calculus independently of "
            "Leibniz, and spent decades on alchemy, theology and the Royal Mint."
        ),
        "content": """**Isaac Newton** (25 December 1642 – 20 March 1727, Old Style) was an
English mathematician, physicist and astronomer whose *Philosophiæ Naturalis Principia
Mathematica* of 1687 established that terrestrial and celestial motion obey the same small set
of laws. He also founded the modern study of colour, invented a calculus independently of
Gottfried Wilhelm Leibniz, ran the Royal Mint for nearly three decades, and left a larger body
of unpublished writing on alchemy, prophecy and ancient chronology than on physics.

## Early life and Cambridge

Newton was born prematurely at Woolsthorpe Manor in Lincolnshire on Christmas Day 1642 by the
Julian calendar then used in England, which corresponds to 4 January 1643 in the Gregorian
reckoning. His father, also Isaac, had died three months earlier. When his mother Hannah
remarried she left the boy with his grandmother, a separation his later biographers treat as
formative.[^westfall] After grammar school at Grantham he was admitted to Trinity College,
Cambridge, in June 1661 as a subsizar, paying part of his way by service, and took the degree of
Bachelor of Arts in August 1665.

## The plague years

Cambridge dispersed in 1665 because of plague, and Newton spent much of 1665–1667 at Woolsthorpe.
In those months he generalised the binomial theorem to fractional and negative exponents,
developed the method of fluxions and its inverse, began the experiments on colour, and first
compared the Moon's acceleration in its orbit with the acceleration of a falling body. He later
called the period the prime of his age for invention.[^westfall]

The apple story comes from William Stukeley, who recorded a conversation in Newton's garden at
Kensington in April 1726 in which Newton said the notion of gravitation had been occasioned by
the fall of an apple. It is therefore Newton's own late recollection rather than a posthumous
legend, and no version by him involves a blow to the head.[^westfall] He was elected a fellow of
Trinity in 1667 and appointed Lucasian Professor of Mathematics in 1669, succeeding Isaac Barrow.

## Optics

Newton ground his own mirrors and built a reflecting telescope in late 1668, replacing the
objective lens with a curved mirror and so avoiding the coloured fringing that lenses produce. An
improved instrument shown to the Royal Society in 1671 led to his election as a fellow the
following year.

His first publication, a letter in the *Philosophical Transactions* in 1672, reported the prism
experiments. Newton argued that white [[Light]] is not modified by the prism but separated: each
colour is refracted through its own fixed angle, and once isolated it cannot be altered further.
His *experimentum crucis* passed a single separated colour through a second prism and showed it
emerged unchanged, which made colour a property of light itself rather than of the glass or the
eye. *Opticks* (1704) gathered this work with his studies of thin-film colours, diffraction and
the corpuscular account of light as a stream of small particles — a view suited to rectilinear
propagation and reflection, displaced by the wave theory in the nineteenth century, and partly
restored on quite different grounds by quantum theory.

## Fluxions and the calculus dispute

Newton's method of fluxions treats quantities as flowing with time and computes their rates of
change; it is [[Calculus]] in all but notation. He had it by 1666 and circulated *De analysi*
among a few correspondents in 1669, but published almost none of it for decades. Leibniz, working
independently from about 1674, published the differential calculus in 1684 and the integral in
1686, using the d and ∫ notation still standard today.

The two men had exchanged civil letters in the 1670s. Open conflict began in 1699 and hardened in
1710, when John Keill accused Leibniz in the *Philosophical Transactions* of plagiarism. Leibniz
asked the Royal Society for redress; the Society, with Newton as its president, appointed a
committee whose 1712 report found entirely for Newton. Newton had drafted the report himself and
published an anonymous review of it in 1715.[^smith] Modern scholarship accepts independent
invention, giving Newton priority of discovery and Leibniz priority of publication together with
the better notation.

## The Principia

In August 1684 Edmond Halley asked Newton what curve a planet would describe under an
inverse-square attraction. Newton answered that it was an ellipse and that he had calculated it,
but could not find the paper. The tract he wrote instead, *De motu corporum in gyrum*, grew over
two years into the *Principia*. The Royal Society had voted to print the book but had exhausted
its printing budget on the lavishly illustrated *De Historia Piscium*, so Halley financed it
himself and was later paid part of his own salary in unsold copies of the fish
book.[^rsprincipia]

The *Principia* appeared in Latin in 1687, with a second edition in 1713 and a third in
1726.[^cudl] It states three laws of motion — a body persists in uniform motion unless acted on
by a force; change of motion is proportional to the impressed force; action and reaction are
equal and opposite — and then the law of universal gravitation: any two bodies attract along the
line joining them with a force proportional to the product of their masses and inversely
proportional to the square of their separation. From these Newton derived Kepler's three
planetary laws, the tides as the differential attraction of Moon and Sun, the precession of the
equinoxes, the flattening of a rotating Earth at its poles, and the conic-section paths of
comets. The demonstration that one law governs a falling stone, the Moon and every body in
[[The Solar System]] is why the *Principia* is usually treated as the culmination of
[[The Scientific Revolution]], and Newton acknowledged his debts to the work of
[[Galileo Galilei]] on falling bodies and to Kepler's planetary laws.

Newton could not solve the mutual perturbations of three or more bodies exactly, and suspected
the Solar System might need occasional correction to remain stable — a suggestion Leibniz
mocked.[^smith] His theory also treated gravity as instantaneous action at a distance and
offered no mechanism, a gap he declined to fill. Where its predictions eventually failed — the
residual precession of Mercury's perihelion, the deflection of starlight, the rate of clocks in a
gravitational field — [[General relativity]] replaced the force with the curvature of spacetime,
and reduces to Newton's law for weak fields and slow motion.

## The Royal Mint

Newton left Cambridge for London in 1696 as Warden of the Mint during the Great Recoinage, and
became Master in 1699, holding the post until his death. The Warden's duties included
prosecuting coiners: Newton took depositions in taverns and prisons, ran informers, and secured
the conviction of the counterfeiter William Chaloner, who was hanged at Tyburn on 22 March
1699.[^royalmint]

His most consequential act as Master was a report to the Treasury dated 21 September 1717 on the
relative values of gold and silver coin, followed within months by a royal proclamation capping
the guinea at 21 shillings.[^mint1717] The ratio Newton recommended slightly favoured gold;
silver coin was accordingly melted and exported, and Britain drifted onto a de facto gold
standard that lasted, with interruptions, for two centuries. It is one of the clearest cases of a
technical decision about [[Money]] outliving the reasoning that produced it.

Newton also sat as member of parliament for the University of Cambridge in 1689–1690 and
1701–1702, resigning his Lucasian chair and Trinity fellowship in 1701. Queen Anne knighted him
at Trinity College on 16 April 1705, during a royal visit arranged partly to assist his
parliamentary candidacy; he lost the election.[^westfall] In 1714 he advised the parliamentary
committee whose work produced the Longitude Act, setting out the known methods for finding
longitude at sea and their weaknesses — the competition that the [[Marine chronometer]] would
eventually win.[^westfall]

## Alchemy, theology and chronology

Newton left far more manuscript than print. His [[Alchemy|alchemical]] papers — recipes, reading
notes and records of furnace work — form a substantial part of his surviving writing and are now
edited online.[^chymistry] He read the alchemical corpus as a corrupted record of ancient
knowledge and pursued the transmutation of metals with the patience he brought to optics;
[[Mercury (element)|mercury]] and its compounds recur throughout. Analyses of preserved samples
of his hair reported in 1979 found elevated mercury and lead, which has been proposed as a
contributing cause of the episode of insomnia, memory loss and suspicion he suffered in 1693,
though the diagnosis remains conjectural.[^spargo]

His theological writing is larger still. He concluded that the doctrine of the Trinity was a
fourth-century corruption of Christianity, a position that would have cost him his fellowship and
chair had it become known, and he worked for decades on biblical prophecy and on a revised
chronology of ancient kingdoms published posthumously in 1728.[^newtonproject]

Most of this material was unavailable until part of it was auctioned at Sotheby's in 1936. John
Maynard Keynes bought much of the alchemical collection and told the Royal Society's tercentenary
meeting that Newton was not the first of the age of reason but "the last of the
magicians".[^keynes]

## Later years and reputation

Newton was president of the Royal Society from 1703 until his death and used the office against
his opponents. He had quarrelled with Robert Hooke over both the theory of colour and the
priority of the inverse-square law, and in 1712 he arranged the printing of John Flamsteed's
incomplete star catalogue over the Astronomer Royal's objection; Flamsteed burned most of the
copies he could recover. Newton never married, kept a household in London with his half-niece
Catherine Barton, and died at Kensington in March 1727. He lay in state in Westminster Abbey and
was buried there, an honour not previously given in England to a natural philosopher.

Andrew Motte's English translation of the *Principia* appeared in 1729, and Newtonian mechanics
became the model of what a physical theory should look like for the next two centuries. It
remains the working description of motion for almost every engineering purpose and for
spacecraft navigation. The modern assessment separates two figures who were the same man: the
author of a mathematical physics of extraordinary reach, and a secretive investigator of
alchemy, prophecy and chronology who regarded those studies as no less serious.[^smith]
""",
        "tier": "feature",
        "kind": "person",
        "infobox": {
            "title": "Isaac Newton",
            "subtitle": "English mathematician and natural philosopher",
            "rows": [
                {"kind": "header", "value": "Life"},
                {
                    "kind": "row",
                    "label": "Born",
                    "value": (
                        "25 December 1642 (Old Style; 4 January 1643 New Style), "
                        "Woolsthorpe, Lincolnshire"
                    ),
                },
                {
                    "kind": "row",
                    "label": "Died",
                    "value": (
                        "20 March 1727 (Old Style; 31 March 1727 New Style), "
                        "Kensington, London, aged 84"
                    ),
                },
                {"kind": "row", "label": "Resting place", "value": "Westminster Abbey, London"},
                {"kind": "header", "value": "Career"},
                {
                    "kind": "row",
                    "label": "Education",
                    "value": "Trinity College, Cambridge (admitted 1661; BA 1665)",
                },
                {
                    "kind": "row",
                    "label": "Chair",
                    "value": "Lucasian Professor of Mathematics, 1669–1701",
                },
                {
                    "kind": "row",
                    "label": "Royal Mint",
                    "value": "Warden 1696–1699; Master 1699–1727",
                },
                {
                    "kind": "row",
                    "label": "Royal Society",
                    "value": "Fellow from 1672; president 1703–1727",
                },
                {
                    "kind": "row",
                    "label": "Knighted",
                    "value": "By Queen Anne at Trinity College, Cambridge, 16 April 1705",
                },
                {"kind": "header", "value": "Principal works"},
                {
                    "kind": "row",
                    "label": "Principia",
                    "value": (
                        "*Philosophiæ Naturalis Principia Mathematica* "
                        "(1687; 2nd ed. 1713; 3rd ed. 1726)"
                    ),
                },
                {"kind": "row", "label": "Optics", "value": "*Opticks* (1704)"},
                {
                    "kind": "full",
                    "value": (
                        "Also left a large body of unpublished writing on [[Alchemy|alchemy]], "
                        "biblical prophecy and ancient chronology, most of it unread until the "
                        "twentieth century."
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/3/3b/"
                "Portrait_of_Sir_Isaac_Newton%2C_1689.jpg"
            ),
            "alt": "Oil portrait of a long-haired man in dark robes holding a paper",
            "caption": "Newton in 1689, aged 46, painted by Godfrey Kneller",
            "credit": "Godfrey Kneller, 1689",
            "license": "Public domain",
            "source_url": (
                "https://commons.wikimedia.org/wiki/File:Portrait_of_Sir_Isaac_Newton,_1689.jpg"
            ),
        },
        "references": [
            {
                "key": "westfall",
                "title": "Never at Rest: A Biography of Isaac Newton",
                "url": "",
                "authors": "Richard S. Westfall",
                "publisher": "Cambridge University Press",
                "published_on": "1980",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-521-27435-7",
                "quote": "",
            },
            {
                "key": "smith",
                "title": "Isaac Newton",
                "url": "https://plato.stanford.edu/entries/newton/",
                "authors": "George E. Smith",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2007",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "cudl",
                "title": "Newton's own annotated copy of the Principia (Adv.b.39.1)",
                "url": "https://cudl.lib.cam.ac.uk/view/PR-ADV-B-00039-00001/",
                "authors": "Isaac Newton",
                "publisher": "Cambridge Digital Library, Cambridge University Library",
                "published_on": "1687",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "rsprincipia",
                "title": "Principia",
                "url": "https://royalsociety.org/blog/2014/07/principia/",
                "authors": "The Royal Society",
                "publisher": "The Royal Society",
                "published_on": "July 2014",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "royalmint",
                "title": "Isaac Newton, Warden and Master of the Royal Mint 1696–1727",
                "url": "https://www.royalmintmuseum.org.uk/journal/people/isaac-newton/",
                "authors": "Royal Mint Museum",
                "publisher": "Royal Mint Museum",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "mint1717",
                "title": "Letter concerning the state of the gold and silver coins",
                "url": "https://www.newtonproject.ox.ac.uk/view/texts/normalized/MINT01000",
                "authors": "Isaac Newton",
                "publisher": "The Newton Project, University of Oxford",
                "published_on": "21 September 1717",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "newtonproject",
                "title": "The Newton Project",
                "url": "https://www.newtonproject.ox.ac.uk/",
                "authors": "Rob Iliffe and others",
                "publisher": "Faculty of History, University of Oxford",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "chymistry",
                "title": "The Chymistry of Isaac Newton",
                "url": "https://webapp1.dlib.indiana.edu/newton/",
                "authors": "William R. Newman (editor)",
                "publisher": "Indiana University",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "spargo",
                "title": "Newton's 'derangement of the intellect': new light on an old problem",
                "url": "https://doi.org/10.1098/rsnr.1979.0002",
                "authors": "P. E. Spargo and C. A. Pounds",
                "publisher": "Notes and Records of the Royal Society of London, vol. 34, pp. 11–32",
                "published_on": "1979",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rsnr.1979.0002",
                "quote": "",
            },
            {
                "key": "keynes",
                "title": "Newton, the Man",
                "url": "https://mathshistory.st-andrews.ac.uk/Extras/Keynes_Newton/",
                "authors": "John Maynard Keynes",
                "publisher": "Royal Society Newton Tercentenary Celebrations",
                "published_on": "1947",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "the last of the magicians",
            },
        ],
        "see_also": [
            "Calculus",
            "Light",
            "The Solar System",
            "General relativity",
            "Alchemy",
            "Chaos theory",
        ],
        "aliases": ["Newton"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "classical mechanics",
            "gravitation",
            "optics",
            "calculus",
            "Royal Mint",
            "alchemy",
        ],
    },
]
