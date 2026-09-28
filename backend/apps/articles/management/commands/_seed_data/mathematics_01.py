"""Mathematics — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Zero",
        "category": "Mathematics",
        "categories": [
            "History",
            "Computing and Information",
        ],
        "short_description": "The digit that marks an empty place and the number that means none",
        "summary": (
            "Zero is both the digit that marks an empty position in a place-value numeral "
            "system and the number that represents the absence of quantity. The two roles "
            "were separated by more than a thousand years."
        ),
        "content": """**Zero** is the integer that denotes the absence of quantity,
and the digit that marks an empty position in a place-value numeral system. The two roles are
historically separate: scribes were writing a placeholder for a missing column more than a
thousand years before mathematicians were willing to treat zero as a number that could itself
be added, subtracted and multiplied.[^mactutor]

## Numerals without a zero

Additive numeral systems need no zero. In Roman, Egyptian and Greek alphabetic numerals each
sign carried a fixed value wherever it stood, so an empty column had nothing to record. Such
systems are compact for recording results but poor for calculating with: arithmetic was
usually performed on a counting board or from tables, and only the answer was written down.

Positional systems create the need for a zero, because in them a digit means a different
amount depending on where it sits. They also make written calculation mechanical: once place
value is fixed, addition and long multiplication reduce to a short list of steps that can be
followed without insight, which is why the spread of the decimal digits and the spread of the
word [[Algorithm|algorithm]] belong to the same episode. Positional counting was invented
more than once. The Inca [[Quipu]], a device of knotted cords, recorded numbers in base ten
as clusters of knots at fixed heights, and expressed a zero by leaving a position bare.
Numerals are in this respect a layer of [[Writing systems|writing]] that migrates far more
easily than the languages around it.

## Placeholder marks

Babylonian scribes wrote numbers in base 60 with [[Cuneiform|cuneiform]] wedges and for
centuries simply left a space where a sexagesimal place was empty. By about 400 BCE a sign of
two slanted wedges was in use for that gap.[^mactutor] It appeared inside numbers rather than
at the end, so a reader still had to infer the overall magnitude from context. Greek
astronomers working in the same sexagesimal tradition, Ptolemy in the second century CE among
them, used a small round mark for a vacant place in tables of fractions, and Maya scribes
used a shell-shaped glyph as a zero in the positional Long Count calendar. In none of these
systems was the mark treated as a number in its own right.

## Zero as a number

Indian mathematicians called it shunya, "empty", and wrote it first as a dot and later as a
small circle. The Brahmasphutasiddhanta, completed by Brahmagupta in 628 CE, is the earliest
surviving text to give arithmetic rules for zero and for negative quantities together,
phrased in terms of fortunes and debts: a debt minus zero is a debt, zero minus a debt is a
fortune, and the product of zero with any quantity is zero.[^mactutor] Division was harder.
Brahmagupta set zero divided by zero equal to zero; Mahavira in the ninth century held that a
number divided by zero is left unchanged; Bhaskara II in the twelfth argued that the quotient
is an unbounded quantity, which is closer to the modern treatment by limits, although modern
arithmetic simply leaves division by zero undefined.[^plofker]

The oldest securely dated zero inside a positional numeral is not Indian but Khmer.
Inscription K-127 from Sambor on the Mekong records the Saka year 605, equivalent to 683 CE,
using a dot for the empty tens place.[^aczel] The Indian example usually cited, an inscription
at Gwalior recording the endowment of a garden, is dated 876 CE and uses a small raised circle
much like the modern digit.[^mactutor]

## Transmission westward

The decimal digits reached Arabic-speaking mathematicians by the eighth century. Around 825
al-Khwarizmi, working in Baghdad, wrote a treatise on calculation with the Indian numerals
that became the main channel by which the system travelled; it survives only in Latin
translation, and its author's Latinised name is the origin of the word algorithm.[^mactutor]
Sanskrit shunya was rendered as Arabic sifr, also meaning empty, which produced Latin cifra
and zephirum and, by way of Italian, both zero and cipher. In the western provinces of
[[The Islamic Golden Age|the Islamic world]] the digits took on the ghubar forms that are the
immediate ancestors of the figures in use today.

## Adoption in Europe

Leonardo of Pisa, known as Fibonacci, opened his Liber Abaci of 1202 with the nine Indian
figures together with the sign 0, and filled the book with commercial problems, currency
conversions and interest calculations aimed at merchants rather than scholars.[^sigler]
Adoption still took three centuries. Reckoning on ruled boards and reckoning with pen and
figures coexisted, and one practical objection to the new digits was that a written figure is
easier to alter than a sum spelled out in words: the money-changers' guild of Florence forbade
its members to use them in their books in 1299. The familiar claim that medieval Europe feared
the zero as something diabolical is, by contrast, a modern invention, traceable through
nineteenth- and twentieth-century popular writing.[^nothaft] What settled the question was
commercial. [[Double-entry bookkeeping]], described in print by Luca Pacioli in 1494, depends
on columns that add up and on a symbol for an account that balances to nothing.

## Mathematical status

Zero is the additive identity: adding it changes nothing, and it is the only number with that
property. It is even, it is neither positive nor negative, and it is neither a
[[Prime number|prime]] nor a composite number, since it is divisible by every positive
integer. Multiplication by zero always yields zero, which is why division by zero is excluded:
no number multiplied by zero gives a non-zero result, and every number multiplied by zero
gives zero, so the quotient is in one case impossible and in the other not unique. Several
conventions follow from treating zero as the empty case
rather than as a special one: the empty set has cardinality zero, an empty sum is zero, an
empty product is one, and zero factorial is one. Whether the natural numbers are taken to
begin at zero or at one remains a divided convention.

## Zero in computing

Most programming languages number the elements of an array from zero, so that an index is an
offset from the start of a block rather than an ordinal. Binary floating-point arithmetic as
standardised in IEEE 754 goes further and provides two zeros, +0 and -0, which compare as
equal but are distinguishable in division, where one divided by +0 and one divided by -0 yield
infinities of opposite sign.[^ieee754] Text encodings keep their own zeros: [[Unicode]]
assigns the digit 0 the code point U+0030 and encodes separate zero digits for dozens of other
scripts, alongside a null control character that is not a digit at all.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Zero",
            "subtitle": "0, integer and numerical digit",
            "rows": [
                {"kind": "header", "value": "As a number"},
                {
                    "kind": "row",
                    "label": "Symbol",
                    "value": "0",
                },
                {
                    "kind": "row",
                    "label": "Properties",
                    "value": "Even; additive identity; neither prime nor composite",
                },
                {
                    "kind": "row",
                    "label": "Division",
                    "value": "Division by zero is undefined",
                },
                {"kind": "header", "value": "History"},
                {
                    "kind": "row",
                    "label": "Earliest placeholder",
                    "value": "Babylonian sexagesimal notation, by c. 400 BCE",
                },
                {
                    "kind": "row",
                    "label": "Earliest rules",
                    "value": "Brahmagupta, Brahmasphutasiddhanta, 628 CE",
                },
                {
                    "kind": "row",
                    "label": "Oldest dated numeral",
                    "value": "Inscription K-127, Sambor, Cambodia, 683 CE",
                },
                {
                    "kind": "row",
                    "label": "Into Latin Europe",
                    "value": "Fibonacci, Liber Abaci, 1202",
                },
                {
                    "kind": "row",
                    "label": "Name",
                    "value": "Sanskrit *shunya* to Arabic *sifr* to Latin *zephirum*",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "mactutor",
                "title": "A history of Zero",
                "url": "https://mathshistory.st-andrews.ac.uk/HistTopics/Zero/",
                "authors": "J J O'Connor and E F Robertson",
                "publisher": "MacTutor History of Mathematics Archive, University of St Andrews",
                "published_on": "November 2000",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "plofker",
                "title": "Mathematics in India",
                "url": "",
                "authors": "Kim Plofker",
                "publisher": "Princeton University Press",
                "published_on": "2009",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "aczel",
                "title": "Finding Zero",
                "url": "",
                "authors": "Amir D. Aczel",
                "publisher": "St. Martin's Press",
                "published_on": "2015",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sigler",
                "title": "Fibonacci's Liber Abaci: A Translation into Modern English",
                "url": "",
                "authors": "Laurence E. Sigler (translator)",
                "publisher": "Springer",
                "published_on": "2002",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nothaft",
                "title": "Medieval Europe's satanic ciphers: on the genesis of a modern myth",
                "url": "https://ora.ox.ac.uk/objects/uuid:71f4c8ca-2b6a-4393-94dc-8d81096985bc",
                "authors": "C. Philipp E. Nothaft",
                "publisher": "British Journal for the History of Mathematics",
                "published_on": "2020",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1080/26375451.2020.1726050",
                "quote": "",
            },
            {
                "key": "ieee754",
                "title": "IEEE Standard for Floating-Point Arithmetic (IEEE 754-2019)",
                "url": "",
                "authors": "",
                "publisher": "Institute of Electrical and Electronics Engineers",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Prime number",
            "Algorithm",
            "Cuneiform",
            "Writing systems",
            "Double-entry bookkeeping",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "number theory",
            "numerals",
            "place value",
            "history of mathematics",
        ],
    },
    {
        "title": "Prime number",
        "category": "Mathematics",
        "categories": [
            "Computing and Information",
        ],
        "short_description": "An integer greater than 1 whose only divisors are 1 and itself",
        "summary": (
            "A prime number has no positive divisors other than 1 and itself. Primes are the "
            "multiplicative building blocks of the integers, and the difficulty of finding "
            "them inside a large number underpins modern cryptography."
        ),
        "content": """**A prime number** is an integer greater than 1 whose only positive
divisors are 1 and itself. The sequence begins 2, 3, 5, 7, 11, 13, 17, 19, 23, 29; there are
25 primes below 100 and 50,847,534 below one billion.[^oeis] Every larger integer that is not
prime is composite, and can be broken into primes in exactly one way, which makes the primes
the multiplicative building blocks of arithmetic. The difficulty of performing that breaking on
a large number is what most contemporary [[Public-key cryptography]] rests on.

## Definition and unique factorisation

Neither 1 nor [[Zero|zero]] counts as prime. Excluding 1 is a convention with a purpose: if 1
were prime, 12 could be written as 2 × 2 × 3, as 1 × 2 × 2 × 3, and so on without end, and
factorisations would no longer be unique. Zero is excluded because it is divisible by every
positive integer. Two is the only even prime, so every other prime is odd, and that asymmetry
accounts for a great many special cases in number theory.

The fundamental theorem of arithmetic states that every integer greater than 1 is a product of
primes, uniquely apart from the order of the factors. Its essential ingredient appears in
[[Euclid's Elements]] as Book VII, Proposition 30 — if a prime divides a product, it divides
one of the factors — but the theorem was first stated and proved in full generality by Carl
Friedrich Gauss in the Disquisitiones Arithmeticae of 1801.[^hardywright]

## Sieving

The oldest method for listing primes is the sieve of Eratosthenes. Write out the integers from
2 to n, then repeatedly take the smallest number not yet struck out, keep it, and strike out
all of its multiples; the process can stop as soon as that number exceeds the square root of
n, because any composite below n has a factor no larger than its own square root. The method
is named for Eratosthenes of Cyrene, who directed [[The Library of Alexandria|the library at
Alexandria]] in the third century BCE, although the earliest surviving description of it is in
the Introduction to Arithmetic of Nicomachus, written around 100 CE.[^mactutor_primes] For
listing every prime up to a bound it remains the standard tool.

## There is no largest prime

Book IX, Proposition 20 of the Elements proves that "prime numbers are more than any assigned
multitude of prime numbers", in Thomas Heath's translation.[^heath] The argument is short:
given any finite collection of primes, multiply them together and add 1. The result leaves a
remainder of 1 when divided by each prime in the collection, so whatever primes divide it are
not in the collection, and therefore no finite collection can be complete.

## Distribution

The prime-counting function, written pi(x), gives the number of primes not exceeding x. Primes
thin out as they grow: pi(100) is 25 and pi(1,000,000) is 78,498. Gauss as a teenager and
Adrien-Marie Legendre in 1798 both noticed that pi(x) is close to x divided by the natural
logarithm of x, a statement finally proved in 1896, independently by Jacques Hadamard and
Charles-Jean de la Vallee Poussin, using the analytic properties of Riemann's zeta function.
The prime number theorem is often restated as a density: an integer near n behaves like a
prime with likelihood roughly one in log n, and heuristics built on that reading, borrowed
from [[Probability theory]], predict a great deal of observed prime behaviour
correctly.[^hardywright]

Regularity and irregularity sit side by side. Pafnuty Chebyshev proved in 1852 that there is
always a prime between n and 2n for n greater than 1, yet arbitrarily long runs containing no
primes also exist, since none of the numbers from n! + 2 up to n! + n can be prime. Bernhard
Riemann's memoir of 1859 tied the fluctuations of pi(x) to the zeros of the zeta function. The
Riemann hypothesis, which asserts that all the non-trivial zeros have real part one half,
would pin down the error in the prime number theorem as tightly as possible; it remains
unproved, and is one of the seven Millennium Prize Problems of the Clay Mathematics Institute.

## Open problems

Some of the plainest questions about primes are unanswered. The twin prime conjecture, that
infinitely many pairs of primes differ by 2, is open, but in 2013 Yitang Zhang proved that
infinitely many pairs differ by at most 70 million, the first finite bound of its
kind.[^zhang] Later collaborative work by James Maynard, Terence Tao and the Polymath project
reduced that bound to 246 within about a year. Goldbach's conjecture, proposed in a letter to
Leonhard Euler in 1742, holds that every even number greater than 2 is a sum of two primes; it
has been verified by computer beyond 4 × 10^18 and proved in general for no case at all. In
2004 Ben Green and Terence Tao showed that the primes contain arithmetic progressions of every
finite length.

## Mersenne primes and records

Numbers of the form 2^p − 1 can be prime only when p is itself prime, and those that are prime
are called Mersenne primes. The Euclid-Euler theorem pairs them one for one with the even
perfect numbers. Because the Lucas-Lehmer test makes such candidates unusually cheap to check,
nearly every record-holding prime since 1952 has had this form. The largest known prime is
2^136,279,841 − 1, a number of 41,024,320 decimal digits and the 52nd known Mersenne prime,
found on 12 October 2024 on cloud hardware volunteered to the Great Internet Mersenne Prime
Search by Luke Durant.[^gimps]

## Testing versus factoring

Deciding whether a number is prime turns out to be far easier than finding its factors.
Fermat's little theorem supplies a fast test that composites almost always fail; the
Miller-Rabin test, repeated with several bases, drives the chance of misclassifying a composite
below any desired threshold; and in 2002 Manindra Agrawal, Neeraj Kayal and Nitin Saxena
exhibited an [[Algorithm|algorithm]] showing that primality testing can be done in polynomial
time. Nothing comparable is known for factorisation: the best general method, the number field
sieve, still runs in sub-exponential time.[^crandall] Factoring RSA-250, a 250-digit challenge
number, took roughly 2,700 core-years of computer time when it was completed in 2020. That gap
between the two problems is what RSA encryption and digital signatures depend on, and it is
why Peter Shor's quantum factoring algorithm of 1994 prompted a long search for replacements.
The United States National Institute of Standards and Technology published its first
post-quantum cryptography standards in August 2024.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Prime number",
            "subtitle": "Number theory",
            "rows": [
                {"kind": "header", "value": "Definition"},
                {
                    "kind": "row",
                    "label": "Statement",
                    "value": "An integer above 1 with no divisors but 1 and itself",
                },
                {
                    "kind": "row",
                    "label": "First members",
                    "value": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29",
                },
                {
                    "kind": "row",
                    "label": "Below 100",
                    "value": "25 primes",
                },
                {
                    "kind": "row",
                    "label": "Below one billion",
                    "value": "50,847,534 primes",
                },
                {"kind": "header", "value": "Landmarks"},
                {
                    "kind": "row",
                    "label": "Infinitude proved",
                    "value": "[[Euclid's Elements]], Book IX, Proposition 20",
                },
                {
                    "kind": "row",
                    "label": "Prime number theorem",
                    "value": "Conjectured 1790s, proved 1896",
                },
                {
                    "kind": "row",
                    "label": "Largest known",
                    "value": "2^136,279,841 − 1, of 41,024,320 digits (2024)",
                },
                {
                    "kind": "row",
                    "label": "Sequence",
                    "value": "OEIS A000040",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "oeis",
                "title": "A000040: The prime numbers",
                "url": "https://oeis.org/A000040",
                "authors": "",
                "publisher": "The On-Line Encyclopedia of Integer Sequences, OEIS Foundation",
                "published_on": "continuously updated",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "hardywright",
                "title": "An Introduction to the Theory of Numbers",
                "url": "",
                "authors": "G. H. Hardy and E. M. Wright",
                "publisher": "Oxford University Press",
                "published_on": "2008 (6th edition)",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "mactutor_primes",
                "title": "Prime numbers",
                "url": "https://mathshistory.st-andrews.ac.uk/HistTopics/Prime_numbers/",
                "authors": "J J O'Connor and E F Robertson",
                "publisher": "MacTutor History of Mathematics Archive, University of St Andrews",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "heath",
                "title": "The Thirteen Books of Euclid's Elements",
                "url": "",
                "authors": "Thomas L. Heath (translator and editor)",
                "publisher": "Cambridge University Press",
                "published_on": "1908",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "Prime numbers are more than any assigned multitude of prime numbers.",
            },
            {
                "key": "zhang",
                "title": "Bounded gaps between primes",
                "url": "https://doi.org/10.4007/annals.2014.179.3.7",
                "authors": "Yitang Zhang",
                "publisher": "Annals of Mathematics 179, pages 1121-1174",
                "published_on": "2014",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.4007/annals.2014.179.3.7",
                "quote": "",
            },
            {
                "key": "gimps",
                "title": "Mersenne Prime Discovery: 2^136279841-1 is Prime!",
                "url": "https://www.mersenne.org/primes/?press=M136279841",
                "authors": "",
                "publisher": "Great Internet Mersenne Prime Search",
                "published_on": "October 2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "crandall",
                "title": "Prime Numbers: A Computational Perspective",
                "url": "",
                "authors": "Richard Crandall and Carl Pomerance",
                "publisher": "Springer",
                "published_on": "2005 (2nd edition)",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Zero",
            "Euclid's Elements",
            "Public-key cryptography",
            "Algorithm",
            "Probability theory",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "number theory",
            "primes",
            "factorisation",
            "cryptography",
        ],
    },
    {
        "title": "Euclid's Elements",
        "category": "Mathematics",
        "categories": [
            "History",
            "Philosophy and Religion",
        ],
        "short_description": "The geometry textbook that taught the West what a proof looks like",
        "summary": (
            "Compiled at Alexandria about 300 BCE, Euclid's Elements derives 465 propositions "
            "of geometry and number theory from a short list of definitions and postulates. It "
            "was the standard geometry textbook for two thousand years."
        ),
        "content": """**Euclid's Elements** is a treatise on geometry and number theory
in thirteen books, compiled at Alexandria about 300 BCE. It arranges most of the mathematics
known to the Greek world into a single deductive chain of 465 propositions, each derived from a
short list of definitions, postulates and common notions together with the propositions already
proved.[^heath] For more than two millennia it was the geometry textbook of the Mediterranean
world and then of Europe, and over a thousand editions have appeared since it was first printed
in 1482.[^boyer]

## Euclid

Almost nothing is known about the compiler. He worked at Alexandria, probably during the reign
of Ptolemy I between 305 and 282 BCE, and may have taught at the institution attached to
[[The Library of Alexandria|the library there]]. The main biographical source is the commentary
on Book I written by Proclus some 750 years later, which preserves the reply Euclid is said to
have given Ptolemy: that there is no royal road to geometry.[^mactutor_euclid] Little in the
Elements is original to him. Results came from Hippocrates of Chios, Theaetetus, and above all
Eudoxus of Cnidus, whose theory of proportion and method of exhaustion fill Books V and XII.
Euclid's achievement was the arrangement — the choice of starting points, and the ordering of
everything else so that no proposition depends on anything not already established.

## Contents

Book I opens with 23 definitions, five postulates and five common notions, then proves 48
propositions, ending with the theorem of Pythagoras and its converse. Books II to IV treat
areas, circles, and figures inscribed in and circumscribed about circles. Book V presents
Eudoxus's theory of proportion, which holds for incommensurable magnitudes and is the most
demanding part of the work; Book VI applies it to similar figures. Books VII to IX are
arithmetic: the Euclidean algorithm for the greatest common divisor, the proof that there is no
largest [[Prime number|prime]] at IX.20, and the criterion for even perfect numbers at IX.36.
Book X, the longest at 115 propositions, classifies certain incommensurable magnitudes. Books
XI to XIII turn to solid geometry, measure the cone and the pyramid by exhaustion, and close by
constructing the five regular solids, the figures [[Plato]] had assigned to the elements of
matter. The Books XIV and XV found in many manuscripts and early printed editions are later
additions, by Hypsicles and others.

## The axiomatic method

The form of the work mattered as much as its content. Assumptions are declared in advance,
nothing else is assumed, and each proposition follows a fixed pattern: statement, setting-out,
construction, demonstration, conclusion. That is a working realisation of the demonstrative
science [[Aristotle]] had described in the Posterior Analytics, and it became the model for
what a rigorous argument should look like far outside mathematics. Spinoza cast his Ethics in
numbered propositions and proofs, and [[Isaac Newton]] wrote the Principia in a deliberately
Euclidean style two thousand years after the original.

## Transmission

The oldest surviving physical trace is a fragment of papyrus from Oxyrhynchus, P.Oxy. I 29, of
about 100 CE, carrying the statement and the diagram of Book II, Proposition 5.[^oxy] Most
Greek manuscripts descend from the recension made by Theon of Alexandria in the fourth century;
a Vatican manuscript preserving an earlier state of the text was identified by François Peyrard
early in the nineteenth century. The oldest complete Greek copy is Bodleian MS. D'Orville 301,
finished at Constantinople in September 888 by the scribe Stephen the Clerk for Arethas of
Patras, who recorded paying fourteen gold coins for it.[^bodleian]

Arabic versions were made at Baghdad in the ninth century by al-Hajjaj ibn Yusuf ibn Matar and
by Ishaq ibn Hunayn, the latter revised by Thabit ibn Qurra, and mathematicians of
[[The Islamic Golden Age]] wrote extensively on the work, with Ibn al-Haytham, Omar Khayyam and
Nasir al-Din al-Tusi all attacking the parallel postulate in particular. Latin Europe received
the Elements from Arabic rather than Greek: Adelard of Bath translated it about 1120, and the
edition prepared by Campanus of Novara around 1259 became the standard medieval text.[^boyer]

## Printing and teaching

Erhard Ratdolt printed Campanus's Latin text at Venice on 25 May 1482, the first printed
edition of the Elements and one of the first substantial printed books to carry geometrical
diagrams.[^boyer] The Greek text followed at Basel in 1533. Henry Billingsley's English
translation of 1570 appeared with a long preface by John Dee; Christopher Clavius's Latin
edition of 1574 became the Jesuit teaching text, and from it Matteo Ricci and Xu Guangqi
translated the first six books into Chinese in 1607. Oliver Byrne's edition of 1847 replaced
the lettering of the diagrams with coloured shapes. Through [[The Renaissance]] and long after,
the Elements was where painters, architects and surveyors learned their geometry; the theory of
similar figures in Book VI is the geometrical core of [[Linear perspective]].

## The parallel postulate

The fifth postulate, which amounts to the claim that through a point beside a line exactly one
parallel can be drawn, is longer and less self-evident than the other four, and Euclid himself
put off using it until Proposition 29. Attempts to derive it from the remaining assumptions
went on for two thousand years. Girolamo Saccheri in 1733 deduced a long series of consequences
from its denial in the hope of reaching a contradiction, and reached none. Nikolai Lobachevsky
in 1829 and Janos Bolyai in 1832 published consistent geometries in which the postulate fails,
conclusions Gauss had reached privately and left unpublished, and in 1868 Eugenio Beltrami
produced a model establishing that such a geometry is exactly as consistent as Euclid's.
Bernhard Riemann's lecture of 1854 generalised the subject to curved spaces of any dimension
and supplied the mathematics on which [[General relativity]] was later built. The same century
produced surfaces with no counterpart in Euclid's plane at all, among them the one-sided
[[Möbius strip]], described independently by August Möbius and Johann Listing in 1858.

## Rigour reconsidered

Closer nineteenth-century reading showed the Elements to be less complete than its reputation.
Its very first proposition assumes that two constructed circles meet, which no postulate
guarantees, and the diagrams quietly supply facts about order and betweenness that are never
stated. David Hilbert's Grundlagen der Geometrie of 1899 answered this with a full axiom
system, grouped under incidence, order, congruence, parallels and continuity, from which
Euclidean geometry follows with no appeal to a figure.[^hilbert] The Elements is therefore now
read as the first sustained axiomatic system rather than a flawless one, which leaves its
historical standing intact: the habit of deriving consequences from stated assumptions reached
modern mathematics largely through this book.
""",
        "tier": "standard",
        "kind": "work",
        "infobox": {
            "title": "Euclid's Elements",
            "subtitle": "Stoicheia (Στοιχεῖα)",
            "rows": [
                {"kind": "header", "value": "The work"},
                {
                    "kind": "row",
                    "label": "Author",
                    "value": "Euclid of Alexandria",
                },
                {
                    "kind": "row",
                    "label": "Language",
                    "value": "Ancient Greek",
                },
                {
                    "kind": "row",
                    "label": "Compiled",
                    "value": "c. 300 BCE",
                },
                {
                    "kind": "row",
                    "label": "Books",
                    "value": "13, with two later additions",
                },
                {
                    "kind": "row",
                    "label": "Propositions",
                    "value": "465",
                },
                {"kind": "header", "value": "Transmission"},
                {
                    "kind": "row",
                    "label": "Oldest fragment",
                    "value": "Papyrus Oxyrhynchus I 29, c. 100 CE",
                },
                {
                    "kind": "row",
                    "label": "Oldest full copy",
                    "value": "Bodleian MS. D'Orville 301, copied 888",
                },
                {
                    "kind": "row",
                    "label": "First printed",
                    "value": "Venice, 25 May 1482, by Erhard Ratdolt",
                },
                {
                    "kind": "row",
                    "label": "First in English",
                    "value": "Henry Billingsley, 1570",
                },
                {
                    "kind": "full",
                    "value": "Superseded as a school text only in the twentieth century.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "heath",
                "title": "The Thirteen Books of Euclid's Elements",
                "url": "",
                "authors": "Thomas L. Heath (translator and editor)",
                "publisher": "Cambridge University Press",
                "published_on": "1908",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "boyer",
                "title": "A History of Mathematics",
                "url": "",
                "authors": "Carl B. Boyer and Uta C. Merzbach",
                "publisher": "John Wiley & Sons",
                "published_on": "2011 (3rd edition)",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "mactutor_euclid",
                "title": "Euclid of Alexandria",
                "url": "https://mathshistory.st-andrews.ac.uk/Biographies/Euclid/",
                "authors": "J J O'Connor and E F Robertson",
                "publisher": "MacTutor History of Mathematics Archive, University of St Andrews",
                "published_on": "January 1999",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "oxy",
                "title": "The Oxyrhynchus Papyri, Part I",
                "url": "",
                "authors": "Bernard P. Grenfell and Arthur S. Hunt",
                "publisher": "Egypt Exploration Fund, London",
                "published_on": "1898",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "Papyrus 29: a fragment of Euclid, Elements, Book II, Proposition 5.",
            },
            {
                "key": "bodleian",
                "title": "MS. D'Orville 301",
                "url": "https://medieval.bodleian.ox.ac.uk/catalog/manuscript_4146",
                "authors": "",
                "publisher": "Bodleian Libraries, University of Oxford",
                "published_on": "manuscript copied 888",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "hilbert",
                "title": "Grundlagen der Geometrie",
                "url": "",
                "authors": "David Hilbert",
                "publisher": "B. G. Teubner, Leipzig",
                "published_on": "1899",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Prime number",
            "Plato",
            "Aristotle",
            "Linear perspective",
            "The Library of Alexandria",
            "Möbius strip",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "geometry",
            "axiomatic method",
            "ancient greek mathematics",
            "history of mathematics",
        ],
    },
]
