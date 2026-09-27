"""Mathematics — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Calculus",
        "category": "Mathematics",
        "categories": ["Physics"],
        "short_description": "The mathematics of continuous change: derivatives and integrals",
        "summary": (
            "Calculus is the mathematics of continuous change, built on the limit and on two "
            "inverse operations: differentiation, which measures instantaneous rates, and "
            "integration, which accumulates them. Newton and Leibniz devised it independently."
        ),
        "content": """**Calculus** is the branch of mathematics that describes continuous change. It
rests on two operations that turn out to be inverses of one another: differentiation,
which extracts the instantaneous rate at which a quantity varies, and integration, which
accumulates a varying quantity across an interval. Both are defined by means of the limit,
a device for assigning an exact value to the outcome of an endless refinement. Worked out
independently by [[Isaac Newton]] in the mid-1660s and by Gottfried Wilhelm Leibniz a
decade later, calculus became the language in which physical law is ordinarily written,
and the quarrel over who had invented it separated British from Continental mathematics
for a century.

## The derivative

For a function f, the quotient (f(x + h) − f(x)) / h gives the average rate of change of f
across an interval of width h. The derivative at x, written f′(x) or dy/dx, is the single
value that this quotient approaches as h shrinks toward zero; where no such value exists,
the function is not differentiable at that point. Geometrically the derivative is the slope
of the tangent line to the graph. Kinematically, if the function gives position against
time, its derivative is velocity and the derivative of velocity is acceleration — the
reading from which the subject grew.

The same operation carries a different meaning in every field that uses it.

| Quantity described by the function | Its derivative |
| --- | --- |
| Position against time | Velocity |
| Velocity against time | Acceleration |
| Electric charge against time | Current |
| Total cost against output | Marginal cost |
| Population against time | Growth rate |

What makes differentiation a *calculus* — a system of routine computation rather than a
collection of one-off constructions — is that a handful of rules cover almost every
expression. The derivative of a power, a product, a quotient and a composition can each be
written down from the derivatives of the parts, the last of these being the chain rule.
Once the basic cases are established, no further appeal to limits is needed. Three
notations survive side by side: Leibniz's dy/dx, Newton's dotted letters, and the prime of
Joseph-Louis Lagrange, introduced in his *Théorie des fonctions analytiques* of 1797.

## The integral

The definite integral of f between a and b is built by cutting the interval into small
pieces, multiplying a value of f on each piece by that piece's width, adding the products,
and taking the limit as the subdivision is refined without bound. Where f is positive the
result is the area under its graph, but the construction is indifferent to that reading:
the same sum gives arc length, volume, the work done by a variable force, a centre of
mass, and the chance that a continuous quantity falls in a given range, which is how
[[Probability theory]] handles distributions.

## The fundamental theorem

The two halves of the subject are joined by the fundamental theorem of calculus, which has
two statements. Differentiating the function that accumulates f from a fixed starting
point returns f. And the definite integral of f′ across an interval equals the difference
in f between the endpoints. The second converts the computation of an area from a limit
process into an algebraic one: find any antiderivative, evaluate it twice, subtract.
Geometric versions of the relation were known to Isaac Barrow and James Gregory in the
1660s; recognising it as general, and as the organising principle of a whole subject, was
the step that Newton and Leibniz each took.[^boyer]

## Anticipations

Archimedes of Syracuse (c. 287–212 BC) obtained the area of a parabolic segment by the
method of exhaustion, trapping a region between inscribed and circumscribed figures whose
difference could be made as small as desired. The reasoning has the logic of a limit
without any general machinery, and it belongs to the deductive geometry codified in
[[Euclid's Elements]]. Archimedes also described, in a work addressed to Eratosthenes, the
mechanical weighing of figures by which he actually found such results; that text survives
only through a palimpsest identified in 1906.

In Kerala, Madhava of Sangamagrama (c. 1340 – c. 1425) and the school that followed him
obtained infinite series for the sine, cosine and arctangent, including the series that
yields π, with the reasoning set down in the Malayalam *Yuktibhāṣā* around 1530. In Europe
the immediate precursors arrived in quick succession: Johannes Kepler's 1615 treatise on
the volumes of wine casks, Bonaventura Cavalieri's *Geometria indivisibilibus continuorum*
of 1635, which treated an area as a sum of line-like indivisibles, Pierre de Fermat's
methods for maxima, minima and tangents in the 1630s, and John Wallis's *Arithmetica
infinitorum* of 1656. What all of them lacked was a uniform notation and an explicit
statement that the two operations undo each other.[^boyer]

## Newton's fluxions

Newton developed his version in 1665 and 1666, much of it at Woolsthorpe while plague
closed Cambridge. He took quantities to flow with time: a *fluent* and its rate of change,
the *fluxion*, marked with a dot above the letter. His tract of October 1666 was never
printed. *De analysi per aequationes numero terminorum infinitas*, written in 1669,
circulated in manuscript among British mathematicians and was published only in 1711, and
the fuller *Method of Fluxions*, written in 1671, appeared in English in 1736, nine years
after his death.[^mactutor] When Newton presented his results on motion and gravitation in
the *Principia* of 1687, he cast them in classical geometry rather than in the new
calculus, which has kept that book difficult ever since.

## Leibniz's differentials

Leibniz reached the subject in Paris between 1673 and 1676, coming from sequences of finite
differences to infinitely small ones. On 29 October 1675 he wrote the integral sign, an
elongated *s* for *summa*, and the *d* for a difference; both are still in use. His paper
"Nova methodus pro maximis et minimis", in the Leipzig journal *Acta Eruditorum* for
October 1684, was the first published account of the differential calculus, and a paper on
integration followed in 1686.[^mactutor] Leibniz's symbolism made substitution and the
chain rule look like ordinary algebra carried out on differentials, which is the main
reason his notation, and not Newton's, is the one taught today. Jacob Bernoulli proposed
the name "integral calculus" in 1690.

## The priority dispute

The modern verdict is that both men had the subject independently, Newton first in time and
Leibniz first in print. That was not the eighteenth-century view. Insinuations of
plagiarism circulated from the 1690s, and in 1712 the Royal Society, with Newton as its
president, appointed a committee to settle the question. Its report, the *Commercium
epistolicum*, found for Newton and implied that Leibniz had taken his ideas from material
seen in England. Surviving drafts show that Newton chose the committee and wrote much of
the report himself, and that he afterwards published an anonymous review of it in the
Society's own *Philosophical Transactions*.[^cudl] Leibniz died in 1716 with nothing
resolved. The lasting cost fell on Britain, where attachment to fluxion notation left
mathematicians cut off from Continental analysis until the Analytical Society, founded at
Cambridge in 1812 by Charles Babbage, John Herschel and George Peacock, campaigned to
adopt Leibniz's symbols.

## Making it rigorous

For roughly 150 years calculus produced correct answers while resting on quantities that
were treated as non-zero during a calculation and as zero at the end of it. George Berkeley
pressed the objection in *The Analyst* of 1734, asking of these vanishing increments
whether one might not "call them the ghosts of departed quantities".[^berkeley] Leonhard
Euler's *Institutiones calculi differentialis* of 1755 extended the subject enormously
without settling the difficulty.

The repair came in the nineteenth century. Bernard Bolzano in 1817 and Augustin-Louis
Cauchy, in his *Cours d'analyse* of 1821 and his lectures of 1823, redefined continuity,
the derivative and the integral in terms of limits alone, with no infinitely small
quantities anywhere. Karl Weierstrass's Berlin lectures turned the limit into the
epsilon–delta formulation still taught and supplied the cautionary examples, among them a
function that is continuous everywhere and differentiable nowhere. Richard Dedekind and
Georg Cantor then constructed the real numbers themselves in 1872, and Henri Lebesgue's
integral of 1902 extended integration to functions beyond the reach of the Riemann
definition, becoming the foundation of modern probability. Infinitesimals were eventually
given a consistent form of their own in Abraham Robinson's non-standard analysis in the
1960s, long after limits had taken over the teaching of the subject.[^sep]

## A general-purpose language

Calculus spread because the laws of nature turned out to be statements about derivatives.
Newton's second law is a differential equation; so are the equations of electromagnetism,
of fluid flow and of heat conduction. [[Thermodynamics]] is written in partial derivatives
and exact differentials. Joseph Fourier's attack on the heat equation produced the
[[Fourier transform]]. The wave equation governs the propagation of [[Light]] and of
sound, and the variational form of the subject — finding the function that makes an
integral smallest — states optics and mechanics in one sentence each.
[[General relativity]] recasts gravity as the differential geometry of curved spacetime,
and [[Chaos theory]] studies ordinary differential equations whose nearby solutions
separate exponentially. Outside physics, marginal quantities in economics are derivatives, and
ecological and epidemiological models are systems of differential equations solved
numerically. Roughly three centuries after it was assembled, the machinery is settled,
uncontroversial, and used by nearly every quantitative science.
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Calculus",
            "subtitle": "Branch of mathematical analysis",
            "rows": [
                {
                    "kind": "full",
                    "value": "The study of change and accumulation, joined by one theorem",
                },
                {
                    "kind": "header",
                    "value": "Core notions",
                },
                {
                    "kind": "row",
                    "label": "Operations",
                    "value": "Differentiation, integration",
                },
                {
                    "kind": "row",
                    "label": "Joined by",
                    "value": "The fundamental theorem of calculus",
                },
                {
                    "kind": "row",
                    "label": "Defined through",
                    "value": "The limit",
                },
                {
                    "kind": "header",
                    "value": "Origins",
                },
                {
                    "kind": "row",
                    "label": "Independent founders",
                    "value": "[[Isaac Newton]] (1665–1666); G. W. Leibniz (1673–1676)",
                },
                {
                    "kind": "row",
                    "label": "First publication",
                    "value": "Leibniz, *Acta Eruditorum*, October 1684",
                },
                {
                    "kind": "row",
                    "label": "Surviving notation",
                    "value": "Leibniz's dy/dx and integral sign; Lagrange's f′",
                },
                {
                    "kind": "header",
                    "value": "Foundations",
                },
                {
                    "kind": "row",
                    "label": "Chief critique",
                    "value": "George Berkeley, *The Analyst* (1734)",
                },
                {
                    "kind": "row",
                    "label": "Made rigorous by",
                    "value": "Cauchy (1821–1823), Weierstrass, Dedekind and Cantor",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "boyer",
                "title": "The History of the Calculus and Its Conceptual Development",
                "url": "https://archive.org/details/historyofcalculu00boye",
                "authors": "Carl B. Boyer",
                "publisher": "Dover Publications",
                "published_on": "1959",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-486-60509-8",
                "quote": "",
            },
            {
                "key": "mactutor",
                "title": "A history of the calculus",
                "url": "https://mathshistory.st-andrews.ac.uk/HistTopics/The_rise_of_calculus/",
                "authors": "J. J. O'Connor and E. F. Robertson",
                "publisher": "MacTutor History of Mathematics Archive, University of St Andrews",
                "published_on": "1996",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "berkeley",
                "title": "The Analyst; or, a Discourse Addressed to an Infidel Mathematician",
                "url": "https://www.maths.tcd.ie/pub/HistMath/People/Berkeley/Analyst/",
                "authors": "George Berkeley",
                "publisher": "J. Tonson, London",
                "published_on": "1734",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "May we not call them the ghosts of departed quantities?",
            },
            {
                "key": "cudl",
                "title": "Papers relating to the dispute respecting the invention of fluxions",
                "url": "https://cudl.lib.cam.ac.uk/view/MS-ADD-03968",
                "authors": "Isaac Newton and others",
                "publisher": "Cambridge Digital Library, Cambridge University Library",
                "published_on": "1712",
                "accessed_on": "2026-09-26",
                "identifier": "MS Add. 3968",
                "quote": "",
            },
            {
                "key": "sep",
                "title": "Continuity and Infinitesimals",
                "url": "https://plato.stanford.edu/entries/continuity/",
                "authors": "John L. Bell",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2005; revised 2022",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Isaac Newton",
            "Fourier transform",
            "Probability theory",
            "General relativity",
            "Chaos theory",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["analysis", "limits", "derivatives", "integrals", "history of mathematics"],
    },
    {
        "title": "Fourier transform",
        "category": "Mathematics",
        "categories": ["Physics", "Computing and Information"],
        "short_description": "A signal rewritten as a sum of pure waves of each frequency",
        "summary": (
            "The Fourier transform rewrites a function of time or space as a combination of pure "
            "sinusoids, exchanging one domain for the other. Devised by Joseph Fourier to solve "
            "the heat equation, it now underlies audio, imaging and spectroscopy."
        ),
        "content": """The **Fourier transform** is a mathematical operation that re-expresses a
function of time or space as a function of frequency, listing the sinusoidal components the
original contains together with the strength and timing of each. Nothing is discarded: an
inverse transform reconstructs the original exactly, so the two descriptions hold the same
information in different coordinates. Problems that are awkward in one description are
often trivial in the other, and that exchange is why the transform turns up throughout
physics, engineering and data analysis.

## Two descriptions of the same thing

A periodic function is expanded as a Fourier series, a sum over a discrete set of
harmonics, each with an amplitude and a phase. A function that does not repeat needs a
continuous range of frequencies, and the sum becomes an integral: the Fourier transform
proper. Both rest on orthogonality. The integral of the product of two sinusoids of
different frequency over a full period is zero, so integrating a signal against one chosen
sinusoid isolates exactly that component and rejects the rest. The formulas for the
coefficients are therefore definite integrals, which makes the whole subject an
application of [[Calculus]].

The effect is easiest to see in [[Sound]]. A struck chord, recorded as pressure against
time, is a complicated wiggle; the same chord in the frequency description is a handful of
sharp peaks at the pitches sounded, and the relative strengths of the upper peaks account
for the difference in timbre between two instruments playing the same note. The whole-number
frequency ratios of that harmonic series are the physical facts that tuning systems such as
[[Equal temperament]] are built to compromise with.

## Fourier's heat problem

Joseph Fourier (1768–1830) introduced the method for heat rather than for signals. In
December 1807 he submitted a memoir on the conduction of heat in solids to the Institut de
France, solving the heat equation by writing an arbitrary initial temperature distribution
as a sum of sines and cosines and then following each term as it decayed at its own rate.
Lagrange blocked publication, denying that an arbitrary function could be represented by
such a series. A revised memoir won the Academy's prize in 1811, with a formal reservation
about its rigour attached, and Fourier eventually published the argument as *Théorie
analytique de la chaleur* in 1822.[^fourier1822][^mactutor]

Lagrange's objection was not idle. Establishing which functions a trigonometric series
represents, and in what sense the series converges, took another century, and the effort
reshaped analysis: Bernhard Riemann's redefinition of the integral and Georg Cantor's first
work on infinite sets both came out of this question. One visible residue is the Gibbs
phenomenon. Near a jump in the function, a truncated series overshoots by about nine per
cent of the jump, and that overshoot does not shrink as more terms are added — it only
moves closer to the discontinuity.

## What the transform does to operations

| Operation on the signal | Effect on its spectrum |
| --- | --- |
| Differentiation | Multiplication by frequency |
| Convolution with another signal | Multiplication, frequency by frequency |
| Shift in time | Change of phase, magnitudes unaltered |
| Compression in time | Stretching in frequency |

The convolution row is the basis of filtering. Blurring, sharpening, echo and tone controls
are all convolutions, and each becomes an ordinary multiplication once both signals are
transformed. The last row states a trade-off that has no exceptions: a signal confined to a
brief interval must occupy a wide band of frequencies, and a pure tone must last a long
time. In [[Quantum mechanics]] the position and momentum descriptions of a particle are
Fourier transforms of each other, which makes Heisenberg's uncertainty relation an instance
of this same inequality rather than a separate physical postulate.

## Discrete data and the fast algorithm

Measurements are sampled, so practical work uses the discrete Fourier transform, which
turns N samples into N coefficients. Computed directly that costs on the order of N²
multiplications, which becomes prohibitive for long records. The fast Fourier transform
brings the cost down to the order of N log N by splitting the sum recursively into
transforms of the even- and odd-numbered samples, whose partial results can be reused. For
a record of a million samples the saving is roughly fifty thousandfold, which is the
difference between an overnight computation and an interactive one.

The algorithm was published by James Cooley and John Tukey in 1965.[^cooley1965] The same
decomposition had been written down by Carl Friedrich Gauss around 1805, in a note on
interpolating the orbits of asteroids that appeared only in his posthumous collected works,
and it was rediscovered piecemeal at least half a dozen times in between.[^gaussfft]

## Uses

The transform is standard equipment wherever a signal or an image is analysed. Audio and
vibration work is done on spectra, and lossy compression discards the spectral components
least likely to be noticed: JPEG images use the closely related discrete cosine transform
and MP3 audio a modified form of it. Magnetic resonance imaging does not measure a picture at all — it
measures spatial frequencies, and the image is produced by inverting the transform. X-ray
crystallography works the same way, the diffraction pattern being the transform of the
electron density in the crystal. Fourier-transform infrared spectrometers recover an
absorption spectrum by transforming an interferogram, so identifying a substance from the
[[Light]] it absorbs is a transform of a measurement. In seismology the spectrum of a
recorded ground motion helps separate the character of the source from the response of the
ground under the instrument, routine work in [[Earthquake]] studies and in petroleum
prospecting. [[Information theory]] rests in part on a result of the same family: a signal
containing no frequency above B is fully determined by samples taken at a rate of 2B, which
is why digital audio at 44,100 samples a second can carry everything the ear detects.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Fourier transform",
            "subtitle": "Integral transform in mathematical analysis",
            "rows": [
                {
                    "kind": "row",
                    "label": "Named after",
                    "value": "Joseph Fourier (1768–1830)",
                },
                {
                    "kind": "row",
                    "label": "Introduced",
                    "value": "Memoir on heat conduction, 1807; published 1822",
                },
                {
                    "kind": "row",
                    "label": "Input",
                    "value": "A function of time or space",
                },
                {
                    "kind": "row",
                    "label": "Output",
                    "value": "Amplitude and phase at each frequency",
                },
                {
                    "kind": "row",
                    "label": "Reversible",
                    "value": "Yes; the inverse transform recovers the original",
                },
                {
                    "kind": "header",
                    "value": "Discrete form",
                },
                {
                    "kind": "row",
                    "label": "Direct cost",
                    "value": "Order N² operations for N samples",
                },
                {
                    "kind": "row",
                    "label": "Fast algorithm",
                    "value": "Order N log N; Cooley and Tukey, 1965",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "fourier1822",
                "title": "Théorie analytique de la chaleur",
                "url": "https://archive.org/details/bub_gb_TDQJAAAAIAAJ",
                "authors": "Joseph Fourier",
                "publisher": "Firmin Didot, Paris",
                "published_on": "1822",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "mactutor",
                "title": "Jean Baptiste Joseph Fourier",
                "url": "https://mathshistory.st-andrews.ac.uk/Biographies/Fourier/",
                "authors": "J. J. O'Connor and E. F. Robertson",
                "publisher": "MacTutor History of Mathematics Archive, University of St Andrews",
                "published_on": "1997",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "cooley1965",
                "title": "An algorithm for the machine calculation of complex Fourier series",
                "url": "https://doi.org/10.1090/S0025-5718-1965-0178586-1",
                "authors": "James W. Cooley and John W. Tukey",
                "publisher": "Mathematics of Computation 19 (90), 297–301",
                "published_on": "April 1965",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1090/S0025-5718-1965-0178586-1",
                "quote": "",
            },
            {
                "key": "gaussfft",
                "title": "Gauss and the history of the fast Fourier transform",
                "url": "https://doi.org/10.1109/MASSP.1984.1162257",
                "authors": "M. T. Heideman, D. H. Johnson and C. S. Burrus",
                "publisher": "IEEE ASSP Magazine 1 (4), 14–21",
                "published_on": "October 1984",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1109/MASSP.1984.1162257",
                "quote": "",
            },
        ],
        "see_also": [
            "Calculus",
            "Sound",
            "Quantum mechanics",
            "Information theory",
            "Earthquake",
        ],
        "aliases": ["Fourier series"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["harmonic analysis", "signal processing", "frequency domain", "FFT"],
    },
    {
        "title": "Probability theory",
        "category": "Mathematics",
        "categories": ["Computing and Information"],
        "short_description": "The mathematics of uncertainty, from dice to Kolmogorov",
        "summary": (
            "Probability theory is the mathematics of uncertainty, from seventeenth-century "
            "gambling problems to Kolmogorov's 1933 axioms, which define probability as a "
            "measure. It is the language of statistical physics, genetics and information theory."
        ),
        "content": """**Probability theory** is the branch of mathematics that measures
uncertainty. It assigns numbers between 0 and 1 to events, states rules for combining
them, and derives from those rules the behaviour of long runs of repeated trials. Its
technical core is short — a handful of axioms and a few limit theorems — but it is the
common language of statistical physics, genetics, signal processing, insurance and error
analysis, and the only mathematics available for describing systems whose detail cannot be
tracked.

## Origins in gambling

Games of chance are far older than any mathematics of them. Gerolamo Cardano, a physician
and compulsive gambler, wrote a treatise on dice odds around 1564 that was not printed
until 1663, by which time its results had been found again. The subject is conventionally
dated instead to a correspondence in 1654 between Blaise Pascal and Pierre de Fermat about
the problem of points: if a match of several rounds is broken off early, how should the
stakes be divided? The question had been put to Pascal by Antoine Gombaud, the chevalier de
Méré. Their answer — divide the stakes according to each player's chance of winning had
play continued — established the working method of enumerating equally likely outcomes and
counting the favourable ones. Christiaan Huygens turned the exchange into the first printed
treatise on the subject, *De ratiociniis in ludo aleae* of 1657, organised not around
probability but around expectation, the average return of a gamble.[^hacking]

## Expectation and the law of large numbers

Jacob Bernoulli's *Ars Conjectandi*, published in 1713, eight years after his death, proved
the first version of the law of large numbers: as independent trials accumulate, the
observed proportion of successes converges on the underlying probability, and Bernoulli
supplied explicit bounds on how many trials are needed for a stated degree of confidence.
That theorem is what connects probability to data, and so to every later use of statistics.
Abraham de Moivre's *The Doctrine of Chances* of 1718 and his work of 1733 on approximating
the binomial distribution produced the normal curve as a limiting shape long before it
acquired that name.[^stigler]

## Inverse probability

Those results run forward, from a known chance mechanism to the data it would produce. The
reverse direction — what observed data implies about an unknown mechanism — was addressed
in an essay by Thomas Bayes, published in 1763 by Richard Price two years after Bayes's
death.[^bayes] Pierre-Simon Laplace developed the same idea independently and far further,
applying it in the *Théorie analytique des probabilités* of 1812 to astronomy, jurisprudence
and population records. Bayes's theorem states how an initial probability is revised in the
light of evidence, and its practical force lies in the weight it gives to base rates: a
test that is 99 per cent accurate in both directions, applied to a condition present in one
person in a thousand, returns a positive result that is correct only about nine per cent of
the time, because the very large unaffected group contributes many more false positives
than the small affected group contributes true ones.

## Axioms

Through the nineteenth century probability was applied with confidence — to measurement
error, to annuities, to the kinetic theory of gases — while resting on a definition,
probability as the ratio of favourable to equally likely cases, that says nothing useful
about continuous quantities. Joseph Bertrand showed in 1889 that a chord drawn "at random"
in a circle can be given three different and equally defensible probabilities of exceeding
a given length, depending on what is taken to be uniformly distributed. David Hilbert
included the axiomatisation of probability in his list of open problems in 1900.

The settlement came in 1933, when Andrey Kolmogorov identified probability with measure: a
sample space of possible outcomes, a collection of subsets of it closed under complement
and countable union, and a function assigning each of those subsets a number that is never
negative, equals 1 on the whole space, and adds across disjoint sets.[^kolmogorov] Random
variables became measurable functions and expectation became an integral in Lebesgue's
sense, which placed the subject inside existing analysis, and so inside [[Calculus]],
rather than beside it. On that footing the classical results were sharpened into the strong
law of large numbers and the central limit theorem, which explains why a sum of many small
independent contributions of finite variance approaches the normal distribution whatever
the individual contributions look like. Markov chains, martingales and Brownian motion
became standard objects of study.

## What probability means

The mathematics is settled; the interpretation is not. On the frequency reading a
probability is the limiting relative frequency of an outcome in a long run of repeatable
trials, which leaves single unrepeatable events awkward to discuss. On the subjective or
Bayesian reading it is a degree of belief, required only to be internally coherent; Frank
Ramsey and Bruno de Finetti showed that anyone whose degrees of belief violate the axioms
can be offered a set of bets that loses in every possible case. Propensity accounts locate
probability in the physical arrangement itself.[^sep] All three schools use the same
theorems and disagree only about what the numbers refer to.

## Why the sciences cannot avoid it

[[Entropy]] in statistical mechanics is a count of the microscopic arrangements compatible
with a macroscopic state, which makes thermodynamics a probabilistic argument about very
large numbers. Quantum mechanics predicts probabilities for outcomes and nothing finer. The
mathematical account of [[Natural selection]] built in the 1920s and 1930s treats gene
frequencies as random variables subject to drift as well as to selection, so population
genetics is probability theory applied to heredity. [[Information theory]] defines the
information content of a message from the probability distribution over the messages that
might have been sent. [[Game theory]] needs randomised strategies, and the minimax theorem
that founds it concerns probability distributions over moves; rating systems in [[Chess]]
are probability models, the Elo system predicting a chance of victory from a difference in
ratings and adjusting both numbers by the gap between prediction and result. And
[[Chaos theory]] shows that chance is not merely a confession of ignorance about the rules:
systems with entirely deterministic rules can have long-run behaviour that admits no
description other than a statistical one.
""",
        "tier": "standard",
        "kind": "discipline",
        "infobox": {
            "title": "Probability theory",
            "subtitle": "Mathematical study of uncertainty",
            "rows": [
                {
                    "kind": "row",
                    "label": "Field",
                    "value": "Mathematics; measure theory",
                },
                {
                    "kind": "row",
                    "label": "Conventional origin",
                    "value": "Pascal–Fermat correspondence, 1654",
                },
                {
                    "kind": "row",
                    "label": "First printed treatise",
                    "value": "Huygens, *De ratiociniis in ludo aleae* (1657)",
                },
                {
                    "kind": "row",
                    "label": "Axiomatised by",
                    "value": "Andrey Kolmogorov, 1933",
                },
                {
                    "kind": "header",
                    "value": "Central results",
                },
                {
                    "kind": "row",
                    "label": "Law of large numbers",
                    "value": "Jacob Bernoulli, *Ars Conjectandi* (1713)",
                },
                {
                    "kind": "row",
                    "label": "Normal approximation",
                    "value": "Abraham de Moivre (1733)",
                },
                {
                    "kind": "row",
                    "label": "Inverse probability",
                    "value": "Thomas Bayes (1763); Pierre-Simon Laplace (1812)",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "hacking",
                "title": "The Emergence of Probability",
                "url": "https://archive.org/details/emergenceofproba00hack",
                "authors": "Ian Hacking",
                "publisher": "Cambridge University Press",
                "published_on": "2nd edition, 2006",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-521-68557-3",
                "quote": "",
            },
            {
                "key": "stigler",
                "title": "The History of Statistics: The Measurement of Uncertainty before 1900",
                "url": "",
                "authors": "Stephen M. Stigler",
                "publisher": "Belknap Press of Harvard University Press",
                "published_on": "1986",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-674-40341-3",
                "quote": "",
            },
            {
                "key": "bayes",
                "title": "An essay towards solving a problem in the doctrine of chances",
                "url": "https://doi.org/10.1098/rstl.1763.0053",
                "authors": "Thomas Bayes, communicated by Richard Price",
                "publisher": "Philosophical Transactions of the Royal Society 53, 370–418",
                "published_on": "1763",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1098/rstl.1763.0053",
                "quote": "",
            },
            {
                "key": "kolmogorov",
                "title": "Grundbegriffe der Wahrscheinlichkeitsrechnung",
                "url": "",
                "authors": "Andrey N. Kolmogorov",
                "publisher": "Julius Springer, Berlin",
                "published_on": "1933",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sep",
                "title": "Interpretations of Probability",
                "url": "https://plato.stanford.edu/entries/probability-interpret/",
                "authors": "Alan Hájek",
                "publisher": "Stanford Encyclopedia of Philosophy",
                "published_on": "2002; revised 2023",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Calculus",
            "Entropy",
            "Information theory",
            "Game theory",
            "Chaos theory",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["probability", "measure theory", "statistics", "randomness", "Bayes' theorem"],
    },
]
