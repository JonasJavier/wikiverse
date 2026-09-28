"""Everything the seed needs that is not an article.

The taxonomy, the featured rotation, the "Did you know…" hooks and the redirect
table are copied out of ``docs/content-plan.json`` so that seeding needs no file
I/O and no path assumption at runtime. ``docs/content-plan.json`` stays the
editorial source of truth; this module is its Python projection and the two are
kept in step by hand.

Two things here are *not* in the plan file:

* ``ICONS`` / category ``order`` — presentation, which the plan does not carry.
* ``ON_THIS_DAY`` — derived: eight dated events, each one attached to an article
  that actually exists in the corpus, so the front-page panel has real data
  rather than filler. Every entry is a settled, well-documented date.

Nothing here may be used to count the corpus. :data:`REDIRECTS` lists all 52
planned aliases, including those whose target has not been written yet; the seed
creates a :class:`~apps.articles.models.Redirect` only when the target exists,
and the rest become live the day their article is authored.
"""

from __future__ import annotations

__all__ = [
    "CATEGORIES",
    "DID_YOU_KNOW",
    "FEATURED",
    "ON_THIS_DAY",
    "REDIRECTS",
    "VALID_CATEGORY_NAMES",
]

#: ``(name, description, color, icon)`` in display order. ``Category.order`` is
#: the index, so the sidebar reads sciences → humanities rather than
#: alphabetically.
CATEGORIES: list[tuple[str, str, str, str]] = [
    (
        "Mathematics",
        "Number, structure, shape and proof, from the invention of zero to the "
        "mathematics of unpredictability.",
        "#41678f",
        "sigma",
    ),
    (
        "Physics",
        "Matter, energy, motion and the laws that connect a kettle to a black hole.",
        "#55599b",
        "atom",
    ),
    (
        "Astronomy and Space",
        "The contents and history of the sky, and the instruments and probes sent to read it.",
        "#6f5698",
        "telescope",
    ),
    (
        "Chemistry and Materials",
        "Atoms, bonds and reactions, and the long road from alchemy to the periodic table.",
        "#2d7f80",
        "flask-conical",
    ),
    (
        "Life Sciences",
        "Living systems from molecules to reefs, and the evolutionary logic behind them.",
        "#3d8a5a",
        "dna",
    ),
    (
        "Medicine and the Mind",
        "How medical knowledge was established, and how bodies and memory actually work.",
        "#a2555c",
        "stethoscope",
    ),
    (
        "Earth and Environment",
        "The planet as a working machine: crust, water, ice, air and the cycles that link them.",
        "#6f8a3d",
        "globe",
    ),
    (
        "Geography and Places",
        "Specific places on Earth, why they ended up that way, and the craft of mapping them.",
        "#35798f",
        "map",
    ),
    (
        "Computing and Information",
        "Computation, cryptography, networks and information as a measurable quantity.",
        "#4f7d93",
        "cpu",
    ),
    (
        "Engineering and Technology",
        "Machines and instruments, from bronze gearwork to satellites that keep time.",
        "#7b8290",
        "cog",
    ),
    (
        "History",
        "Periods, events and exchange networks that reshaped how people lived and thought.",
        "#8f5f45",
        "scroll",
    ),
    (
        "Philosophy and Religion",
        "Traditions of reasoning, belief and conduct, and the arguments that outlived them.",
        "#8d5590",
        "landmark",
    ),
    (
        "Language and Literature",
        "Writing systems, languages and the works that survived long enough to matter.",
        "#9c5570",
        "book-open",
    ),
    (
        "Visual Arts",
        "Images and image-making: pigment, geometry, printing and paint.",
        "#b07a3c",
        "palette",
    ),
    (
        "Music and Performance",
        "Sound organised on purpose: tuning systems, styles, instruments and ensembles.",
        "#a8604f",
        "music",
    ),
    (
        "Society and Everyday Life",
        "Money, records, trade goods and games, and the ordinary things with extraordinary "
        "histories.",
        "#8a7a4a",
        "users",
    ),
]

#: The 16 names a ``SeedArticle`` may use in ``category`` or ``categories``.
VALID_CATEGORY_NAMES: frozenset[str] = frozenset(name for name, _d, _c, _i in CATEGORIES)


#: The featured rotation, best first. Titles whose article is not written yet are
#: skipped by the seed, which then tops the panel up from the feature tier, so
#: the front page is never half empty while authoring continues.
FEATURED: list[str] = [
    "The Silk Road",
    "Entropy",
    "Natural selection",
    "Alan Turing",
    "Black hole",
    "Leonardo da Vinci",
]


#: Full hook *sentences*, not titles — they are rendered verbatim under
#: "Did you know…". Each one leads with the traditional "... that".
DID_YOU_KNOW: list[str] = [
    "... that the word algorithm comes from the name of the ninth-century scholar "
    "al-Khwarizmi, whose book on al-jabr also gave us the word algebra?",
    "... that a corroded lump of bronze raised from a Roman-era shipwreck turned out to be "
    "a geared machine that predicted eclipses and tracked the four-year Olympiad cycle?",
    "... that the 1883 eruption of Krakatoa was heard thousands of kilometres away and its "
    "pressure wave circled the globe several times?",
    "... that the atomic clocks aboard GPS satellites must be corrected by about 38 "
    "microseconds a day, because both special and general relativity are pulling on them?",
    "... that Hokusai's Great Wave is not a tsunami but an offshore swell, and that its "
    "striking blue came from Prussian blue pigment newly imported into Japan?",
    "... that a honey bee's waggle dance encodes both the direction of a food source and "
    "how far away it is?",
    "... that the Sahara was green grassland dotted with lakes as recently as about 6,000 "
    "years ago, and that rock art there shows cattle and swimmers?",
    "... that ultramarine was ground from lapis lazuli hauled out of Afghanistan and cost "
    "Renaissance painters more than gold, which is why it was saved for the Virgin's robe?",
]


#: ``(year, month, day, body_markdown)``, newest last. Derived rather than
#: copied: each body links to an article that exists in the corpus today, so the
#: panel is live on first boot. ``body_markdown`` goes through the ordinary
#: article renderer, so ``[[wikilinks]]`` resolve.
ON_THIS_DAY: list[tuple[int, int, int, str]] = [
    (
        1610,
        1,
        7,
        "**1610** — [[Galileo Galilei]] turned a telescope on Jupiter and recorded three "
        "small stars beside it. Within a week he had found a fourth and realised they were "
        "moons in orbit, not fixed stars.",
    ),
    (
        1687,
        7,
        5,
        "**1687** — [[Isaac Newton]]'s *Philosophiae Naturalis Principia Mathematica* was "
        "published by the Royal Society, setting out the laws of motion and universal "
        "gravitation.",
    ),
    (
        1796,
        5,
        14,
        "**1796** — Edward Jenner inoculated the eight-year-old James Phipps with material "
        "from a cowpox sore, the experiment that gave [[Vaccination|vaccination]] its name "
        "and its method.",
    ),
    (
        1859,
        11,
        24,
        "**1859** — *On the Origin of Species* went on sale in London, laying out "
        "[[Charles Darwin]]'s argument for [[Natural selection|natural selection]].",
    ),
    (
        1883,
        8,
        27,
        "**1883** — The final explosions of [[Krakatoa]] destroyed most of the island. The "
        "sound was reported thousands of kilometres away and the pressure wave was traced "
        "around the world on barometers.",
    ),
    (
        1919,
        5,
        29,
        "**1919** — Two British expeditions photographed a total [[Solar eclipse|solar "
        "eclipse]] to measure the deflection of starlight by the Sun, and reported a result "
        "favouring [[General relativity|general relativity]].",
    ),
    (
        1953,
        4,
        25,
        "**1953** — *Nature* published the one-page paper proposing a double-helix structure "
        "for [[Deoxyribonucleic acid|DNA]], alongside the X-ray diffraction papers it "
        "depended on.",
    ),
    (
        1977,
        9,
        5,
        "**1977** — Voyager 1 left Earth, sixteen days after Voyager 2. Both probes of the "
        "[[Voyager program]] are still transmitting from interstellar space.",
    ),
]


#: ``(from_title, to_title)`` for every planned alias. The seed skips a row whose
#: target article does not exist yet; ``SeedArticle.aliases`` is the other half of
#: the same table and the two agree for every written article.
REDIRECTS: list[tuple[str, str]] = [
    ("DNA", "Deoxyribonucleic acid"),
    ("Evolution", "Natural selection"),
    ("Survival of the fittest", "Natural selection"),
    ("Cell theory", "The cell"),
    ("Antibiotics", "Penicillin"),
    ("Germ theory", "Germ theory of disease"),
    ("Plague", "The Black Death"),
    ("JS", "JavaScript"),
    ("ECMAScript", "JavaScript"),
    ("AI", "Artificial intelligence"),
    ("Machine learning", "Artificial intelligence"),
    ("Neural network", "Artificial intelligence"),
    ("Turing test", "Artificial intelligence"),
    ("WWW", "World Wide Web"),
    ("The Web", "World Wide Web"),
    ("GPS", "Global Positioning System"),
    ("RSA", "Public-key cryptography"),
    ("UTF-8", "Unicode"),
    ("Bletchley Park", "Alan Turing"),
    ("Shannon entropy", "Information theory"),
    ("Second law of thermodynamics", "Entropy"),
    ("Carnot cycle", "Heat engine"),
    ("E=mc2", "Special relativity"),
    ("Butterfly effect", "Chaos theory"),
    ("Fourier series", "Fourier transform"),
    ("Heliocentrism", "The Copernican Revolution"),
    ("Newton", "Isaac Newton"),
    ("Quicksilver", "Mercury (element)"),
    ("Hg", "Mercury (element)"),
    ("Continental drift", "Plate tectonics"),
    ("Krakatau", "Krakatoa"),
    ("Northern lights", "Aurora"),
    ("Hydrologic cycle", "The water cycle"),
    ("Everest", "Mount Everest"),
    ("Nile River", "The Nile"),
    ("Sahara Desert", "The Sahara"),
    ("Galapagos", "The Galápagos Islands"),
    ("Silk Route", "The Silk Road"),
    ("Renaissance", "The Renaissance"),
    ("Movable type", "The printing press"),
    ("Longitude problem", "Marine chronometer"),
    ("Gilgamesh", "The Epic of Gilgamesh"),
    ("Arabian Nights", "One Thousand and One Nights"),
    ("Khipu", "Quipu"),
    ("Shakespeare", "William Shakespeare"),
    ("Da Vinci", "Leonardo da Vinci"),
    ("Mona Lisa", "Leonardo da Vinci"),
    ("Bach", "Johann Sebastian Bach"),
    ("Hokusai", "The Great Wave off Kanagawa"),
    ("Perspective", "Linear perspective"),
    ("Lapis lazuli", "Ultramarine"),
    ("Waggle dance", "Honey bee"),
]


#: ``(title, category)`` for all 120 planned articles — **the link universe**
#: (DECISIONS §19). A ``[[wikilink]]`` or ``see_also`` entry naming a title in
#: here is valid; one naming a title outside it is a build failure. A planned
#: title that has not been written yet becomes a red link, which is why this list
#: is longer than the corpus and must stay that way.
#:
#: Copied from ``docs/content-plan.json`` rather than read from it: the Docker
#: image contains ``backend/`` only, so a runtime file read would make the
#: validator work in a checkout and fail in production.
PLANNED_ARTICLES: list[tuple[str, str]] = [
    ("Zero", "Mathematics"),
    ("Prime number", "Mathematics"),
    ("Euclid's Elements", "Mathematics"),
    ("Calculus", "Mathematics"),
    ("Fourier transform", "Mathematics"),
    ("Probability theory", "Mathematics"),
    ("Chaos theory", "Mathematics"),
    ("Möbius strip", "Mathematics"),
    ("Isaac Newton", "Physics"),
    ("Thermodynamics", "Physics"),
    ("Entropy", "Physics"),
    ("Electromagnetism", "Physics"),
    ("Light", "Physics"),
    ("Special relativity", "Physics"),
    ("General relativity", "Physics"),
    ("Quantum mechanics", "Physics"),
    ("Sound", "Physics"),
    ("The Solar System", "Astronomy and Space"),
    ("Mercury (planet)", "Astronomy and Space"),
    ("Mercury", "Astronomy and Space"),
    ("The Copernican Revolution", "Astronomy and Space"),
    ("Galileo Galilei", "Astronomy and Space"),
    ("Black hole", "Astronomy and Space"),
    ("Solar eclipse", "Astronomy and Space"),
    ("Voyager program", "Astronomy and Space"),
    ("The periodic table", "Chemistry and Materials"),
    ("Atomic theory", "Chemistry and Materials"),
    ("Chemical bond", "Chemistry and Materials"),
    ("Water", "Chemistry and Materials"),
    ("Combustion", "Chemistry and Materials"),
    ("Alchemy", "Chemistry and Materials"),
    ("Mercury (element)", "Chemistry and Materials"),
    ("Marie Curie", "Chemistry and Materials"),
    ("Photosynthesis", "Life Sciences"),
    ("Natural selection", "Life Sciences"),
    ("Charles Darwin", "Life Sciences"),
    ("Deoxyribonucleic acid", "Life Sciences"),
    ("The cell", "Life Sciences"),
    ("Coral reef", "Life Sciences"),
    ("Octopus", "Life Sciences"),
    ("Honey bee", "Life Sciences"),
    ("Germ theory of disease", "Medicine and the Mind"),
    ("Vaccination", "Medicine and the Mind"),
    ("Penicillin", "Medicine and the Mind"),
    ("Human anatomy", "Medicine and the Mind"),
    ("Memory", "Medicine and the Mind"),
    ("Plate tectonics", "Earth and Environment"),
    ("Earthquake", "Earth and Environment"),
    ("Krakatoa", "Earth and Environment"),
    ("Ice age", "Earth and Environment"),
    ("The water cycle", "Earth and Environment"),
    ("The carbon cycle", "Earth and Environment"),
    ("Aurora", "Earth and Environment"),
    ("Extinction", "Earth and Environment"),
    ("Mount Everest", "Geography and Places"),
    ("The Nile", "Geography and Places"),
    ("The Sahara", "Geography and Places"),
    ("Venice", "Geography and Places"),
    ("Timbuktu", "Geography and Places"),
    ("Cartography", "Geography and Places"),
    ("The Amazon rainforest", "Geography and Places"),
    ("The Galápagos Islands", "Geography and Places"),
    ("Algorithm", "Computing and Information"),
    ("Alan Turing", "Computing and Information"),
    ("Information theory", "Computing and Information"),
    ("Public-key cryptography", "Computing and Information"),
    ("The Internet", "Computing and Information"),
    ("World Wide Web", "Computing and Information"),
    ("Artificial intelligence", "Computing and Information"),
    ("JavaScript", "Computing and Information"),
    ("Unicode", "Computing and Information"),
    ("Steam engine", "Engineering and Technology"),
    ("Heat engine", "Engineering and Technology"),
    ("The printing press", "Engineering and Technology"),
    ("The transistor", "Engineering and Technology"),
    ("The Antikythera mechanism", "Engineering and Technology"),
    ("Marine chronometer", "Engineering and Technology"),
    ("Global Positioning System", "Engineering and Technology"),
    ("Astrolabe", "Engineering and Technology"),
    ("The Silk Road", "History"),
    ("The Roman Empire", "History"),
    ("The Islamic Golden Age", "History"),
    ("The Library of Alexandria", "History"),
    ("Ancient Egypt", "History"),
    ("The Black Death", "History"),
    ("The Renaissance", "History"),
    ("The Scientific Revolution", "History"),
    ("The Industrial Revolution", "History"),
    ("Revolution", "History"),
    ("Plato", "Philosophy and Religion"),
    ("Aristotle", "Philosophy and Religion"),
    ("Logic", "Philosophy and Religion"),
    ("Stoicism", "Philosophy and Religion"),
    ("Buddhism", "Philosophy and Religion"),
    ("Confucius", "Philosophy and Religion"),
    ("Ship of Theseus", "Philosophy and Religion"),
    ("Writing systems", "Language and Literature"),
    ("Cuneiform", "Language and Literature"),
    ("The Epic of Gilgamesh", "Language and Literature"),
    ("William Shakespeare", "Language and Literature"),
    ("One Thousand and One Nights", "Language and Literature"),
    ("Quipu", "Language and Literature"),
    ("Leonardo da Vinci", "Visual Arts"),
    ("Linear perspective", "Visual Arts"),
    ("Impressionism", "Visual Arts"),
    ("The Great Wave off Kanagawa", "Visual Arts"),
    ("Camera obscura", "Visual Arts"),
    ("Lascaux cave paintings", "Visual Arts"),
    ("Ultramarine", "Visual Arts"),
    ("Baroque music", "Music and Performance"),
    ("Johann Sebastian Bach", "Music and Performance"),
    ("Equal temperament", "Music and Performance"),
    ("Jazz", "Music and Performance"),
    ("Gamelan", "Music and Performance"),
    ("Bass", "Music and Performance"),
    ("Money", "Society and Everyday Life"),
    ("Double-entry bookkeeping", "Society and Everyday Life"),
    ("Salt", "Society and Everyday Life"),
    ("Chess", "Society and Everyday Life"),
    ("Game theory", "Society and Everyday Life"),
]

#: Just the titles, for membership tests.
PLANNED_TITLES: frozenset[str] = frozenset(title for title, _category in PLANNED_ARTICLES)
