"""Computing and Information — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "JavaScript",
        "category": "Computing and Information",
        "categories": ["Engineering and Technology"],
        "short_description": "The programming language that every web browser runs",
        "summary": (
            "JavaScript is the programming language that supplies the interactive layer "
            "of the web. Written at Netscape in 1995 and standardised as ECMAScript, it "
            "is the only language all major browsers execute directly."
        ),
        "content": """**JavaScript** is a high-level programming language, standardised under the name
ECMAScript, that supplies the interactive layer of the [[World Wide Web]]. It is the only
programming language that all major web browsers execute directly, and it has since spread to
servers, build tools, database query layers and embedded runtimes. The language is dynamically
typed, treats functions as ordinary values, and organises inheritance around prototype objects
rather than classes.

## Origins

JavaScript was written at Netscape Communications in 1995 by Brendan Eich, who produced a
working prototype in about ten days in May of that year.[^hopl] Netscape wanted a small
scripting language that page authors rather than systems programmers could embed in documents,
and it had separately agreed with Sun Microsystems to promote Java in the browser. The new
language was accordingly renamed from Mocha to LiveScript and finally to JavaScript, a
marketing decision that has produced lasting confusion, since the two languages share little
beyond some surface syntax. It appeared in a beta release of Netscape Navigator 2.0 in 1995
and in the shipped browser the following year. Microsoft wrote a compatible implementation,
JScript, for Internet Explorer 3.0 in 1996.

Divergence between the two implementations made portable scripting difficult, and Netscape
submitted the language to Ecma International for standardisation in November 1996. The first
edition of ECMA-262 was published in June 1997.[^ecma262] Because Java was a Sun trademark,
the standard took the name ECMAScript, which survives in the title of the specification and in
the numbering of its editions while JavaScript remains the name in ordinary use.

## Standardisation

The third edition, in 1999, added regular expressions, exception handling and stricter string
semantics, after which the standard stalled: an ambitious fourth edition was abandoned in 2008
when the committee could not agree on it. The fifth edition, published in 2009, introduced
strict mode, native JSON support and property descriptors. ECMAScript 2015, the sixth edition,
was the largest single revision, adding block-scoped `let` and `const` declarations, arrow
functions, classes as syntax over the existing prototype semantics, iterators and generators,
promises, and a module system.

Since 2015 the standard has been republished annually. Ecma's Technical Committee 39, which
maintains it, works through a published five-stage proposal process in which a feature
advances to the standard only once specification text, conformance tests and independent
implementations exist.[^tc39] The language therefore now changes in small yearly increments
rather than in decade-long jumps.

## Language design

Every value is either a primitive — number, string, boolean, `null`, `undefined`, symbol or
big integer — or an object. Ordinary numbers are IEEE 754 double-precision floating point, so
integers are represented exactly only up to 9,007,199,254,740,991; the separate `BigInt` type,
added in ECMAScript 2020, covers larger ones. Strings are sequences of 16-bit code units
interpreted as UTF-16, which means that characters outside the Basic Multilingual Plane of
[[Unicode]] occupy two units, and that indexing a string by position can split a character in
half.[^mdn]

Inheritance works by delegation rather than by copying. Every object holds an internal
reference to a prototype object, and a property lookup that fails on the object itself walks
that chain. Functions are values, can be nested, and capture the variables of the scope in
which they were created, so closures are the usual tool for encapsulation and for expressing
higher-order [[Algorithm|algorithms]]. The class syntax added in 2015 is a notation over this
model, not a second object system beside it.

## The browser environment

The language defines no input or output of its own. In a browser it is handed the Document
Object Model, an object tree mirroring the parsed HTML document, which scripts read and mutate
to change what is displayed. Early browsers exposed incompatible models; the World Wide Web
Consortium published DOM Level 1 in 1998, and the DOM is now maintained as a continuously
revised standard alongside HTML. Asynchronous requests — first through the XMLHTTP object
Microsoft shipped with Internet Explorer 5 in 1999, later through the standard fetch
interface — let a page retrieve data over [[The Internet|the Internet]] without reloading, the
technique popularised from 2005 under the name Ajax.

The environment also constrains what a script may do. The same-origin policy prevents a
document from reading another site's documents or responses, scripts run without direct access
to the file system or to other processes, and cryptographic work is delegated to a vetted
browser interface exposing hashing, symmetric ciphers and
[[Public-key cryptography|public-key]] signature operations rather than left to be
reimplemented in the language.

## Concurrency and the event loop

A JavaScript program runs on one thread, and each task runs to completion: nothing interrupts a
function part-way through. Work that must wait — a timer, a network response, a user gesture —
is registered with a callback and resumes only after the current task ends and the runtime
takes the next entry from its task queues.[^whatwg] Promises, standardised in 2015, gave the
model a composable value representing a result that has not arrived yet, and the `async` and
`await` keywords of ECMAScript 2017 allow waiting code to be written in ordinary sequential
form while still yielding control. Genuine parallelism requires separate workers, which
communicate by copying or transferring messages instead of sharing memory.

## Engines

Early interpreters were slow enough that scripting was reserved for small decorative effects.
Modern engines compile the language just in time: they begin by interpreting bytecode, observe
which functions run hot and what shapes their objects take, emit optimised machine code that
assumes those shapes, and fall back to the interpreter when an assumption is violated. Hidden
classes and inline caches, which convert repeated property lookups into fixed memory offsets,
are the central technique. Google's V8, released with the Chrome browser in 2008, made the
approach widely visible; Mozilla's SpiderMonkey and Apple's JavaScriptCore use comparable
designs.

## Beyond the browser

Node.js, released in 2009, paired V8 with an event-driven input and output library and a module
system, allowing server software to be written in the same language as the pages it served;
the npm registry that grew around it became one of the largest collections of reusable software
packages in any language. TypeScript, published by Microsoft in 2012, adds a static type system
that is checked at build time and erased before execution, and has become the usual way large
JavaScript codebases are written. WebAssembly, shipped by the major browsers in 2017 and made
a World Wide Web Consortium recommendation in 2019, provides a second and lower-level
compilation target for languages such as C++ and Rust, but it reaches the document and most
browser interfaces through JavaScript. JavaScript has been reported as the most commonly used
programming language in Stack Overflow's annual developer survey for more than a
decade.[^sosurvey]
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "JavaScript",
            "subtitle": "Programming language",
            "rows": [
                {"kind": "header", "value": "Design"},
                {
                    "kind": "row",
                    "label": "Paradigms",
                    "value": "Multi-paradigm: event-driven, functional, prototype-based",
                },
                {"kind": "row", "label": "Typing", "value": "Dynamic, weak"},
                {"kind": "row", "label": "First appeared", "value": "1995"},
                {"kind": "row", "label": "Designer", "value": "Brendan Eich, at Netscape"},
                {
                    "kind": "row",
                    "label": "Influenced by",
                    "value": "Scheme, Self, Java, AWK",
                },
                {"kind": "header", "value": "Standard"},
                {
                    "kind": "row",
                    "label": "Specification",
                    "value": "ECMA-262 (ECMAScript), Ecma International",
                },
                {"kind": "row", "label": "First edition", "value": "June 1997"},
                {"kind": "row", "label": "Revision cycle", "value": "Annual since 2015"},
                {"kind": "row", "label": "Committee", "value": "Ecma Technical Committee 39"},
                {"kind": "header", "value": "Implementation"},
                {
                    "kind": "row",
                    "label": "Major engines",
                    "value": "V8, SpiderMonkey, JavaScriptCore",
                },
                {"kind": "row", "label": "File extensions", "value": ".js, .mjs, .cjs"},
                {
                    "kind": "full",
                    "value": (
                        "Strings are sequences of UTF-16 code units, so a single "
                        "[[Unicode]] character may occupy two positions."
                    ),
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "hopl",
                "title": "JavaScript: the first 20 years",
                "url": "https://dl.acm.org/doi/10.1145/3386327",
                "authors": "Allen Wirfs-Brock and Brendan Eich",
                "publisher": "Proceedings of the ACM on Programming Languages",
                "published_on": "June 2020",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1145/3386327",
                "quote": "",
            },
            {
                "key": "ecma262",
                "title": "ECMA-262: ECMAScript Language Specification",
                "url": "https://ecma-international.org/publications-and-standards/standards/ecma-262/",
                "authors": "Ecma Technical Committee 39",
                "publisher": "Ecma International",
                "published_on": "First edition June 1997",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "tc39",
                "title": "The TC39 Process",
                "url": "https://tc39.es/process-document/",
                "authors": "",
                "publisher": "Ecma Technical Committee 39",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "mdn",
                "title": "JavaScript reference and guide",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
                "authors": "",
                "publisher": "MDN Web Docs, Mozilla",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "whatwg",
                "title": "HTML Living Standard: event loops",
                "url": "https://html.spec.whatwg.org/multipage/webappapis.html#event-loops",
                "authors": "",
                "publisher": "WHATWG",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sosurvey",
                "title": "2024 Developer Survey: Technology",
                "url": "https://survey.stackoverflow.co/2024/technology",
                "authors": "",
                "publisher": "Stack Overflow",
                "published_on": "2024",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "World Wide Web",
            "The Internet",
            "Unicode",
            "Algorithm",
            "Public-key cryptography",
        ],
        "aliases": ["JS", "ECMAScript"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["programming languages", "ecmascript", "web browsers", "software"],
    },
    {
        "title": "Unicode",
        "category": "Computing and Information",
        "categories": ["Language and Literature"],
        "short_description": "One number for every character in every script, and the encodings that carry them",
        "summary": (
            "Unicode assigns a unique code point to every character in the writing "
            "systems it covers, replacing dozens of incompatible byte encodings. Its "
            "UTF-8 form now carries the great majority of the world's digital text."
        ),
        "content": """**Unicode** is a character encoding standard that assigns a unique number, called a
code point, to every character in the writing systems it covers, together with the property
data and algorithms that describe how those characters behave. It replaced a patchwork of
mutually incompatible national and vendor encodings, and it underlies text handling in current
operating systems and on the [[World Wide Web]].

## The code-page era

Early computer text used single-byte encodings. ASCII, standardised in the 1960s, defined 128
code points: enough for unaccented English, digits, punctuation and a set of control codes.
The upper 128 values available in an eight-bit byte were then claimed repeatedly. The ISO/IEC
8859 series filled them with Western European, Cyrillic, Greek, Hebrew and other repertoires;
hardware and software vendors shipped incompatible variants of their own; and East Asian
scripts, whose repertoires run to tens of thousands of characters, needed multi-byte schemes
such as Shift JIS, EUC and Big5.

Nothing in a stream of bytes recorded which scheme had produced it. A file opened under the
wrong assumption yielded the scrambled output known in Japanese as mojibake, and a single
document could not hold Greek, Hebrew and Japanese together at all. Software that had to serve
several markets carried conversion tables between dozens of encodings, and every conversion
was a chance to lose characters that the target encoding did not contain.

## One code space

The Unicode Consortium was incorporated in 1991 and published the first volume of the standard
in the same year. Its founding idea was a single code space large enough for every script, in
which a character is identified by number independently of font, language or byte encoding.
The original design was fixed-width and sixteen bits, allowing 65,536 characters. That proved
too small, and the second edition, in 1996, introduced the surrogate mechanism, extending the
space to 1,114,112 code points written from U+0000 to U+10FFFF and organised as seventeen
planes of 65,536 each.[^unicode] The first plane, the Basic Multilingual Plane, holds the
scripts in everyday modern use; the supplementary planes carry historic scripts, rarer
ideographs, mathematical alphabets, musical notation and emoji.

The standard distinguishes a character from its rendered shape. A code point stands for an
abstract character with a name and a set of properties; which glyph appears on the page is a
font's business. This is the same separation that divides a letter of the alphabet from the
piece of metal type that prints it, a distinction as old as
[[The printing press|printing with movable type]]. Unicode also commits to stability: once
assigned, a code point is never reused and its name is never altered, so text encoded decades
ago still decodes to the same characters.

## Encoding forms

A code point is an integer, and turning integers into bytes requires an encoding form. UTF-32
stores each code point in four bytes, which is simple and wasteful. UTF-16 stores most
characters in two bytes and supplementary-plane characters in a surrogate pair of two more; it
is the internal string representation of several widely used programming environments, which
is why their string lengths are measured in code units rather than characters.

UTF-8, devised in 1992 by Ken Thompson and Rob Pike, won on the wire and in files. It encodes
a code point in one to four bytes, and the 128 ASCII characters keep their original
single-byte values, so existing English-language text, file formats and protocols remained
valid without conversion.[^rfc3629] Its structure is self-synchronising: a leading byte
announces the length of the sequence and continuation bytes are drawn from a disjoint range,
so a decoder that starts in the middle of a stream, or meets corruption, can find the next
character boundary rather than losing the remainder of the text. That deliberate redundancy is
the kind of trade-off [[Information theory]] makes precise — a few extra bits bought in
exchange for resilience. UTF-8 is now reported on more than 98 per cent of surveyed
websites.[^w3techs]

## Normalisation and segmentation

Because Unicode encodes both precomposed characters and combining marks, the same text can
have more than one representation: the letter é exists as a single code point and also as a
plain e followed by a combining acute accent. The standard defines four normalisation forms —
canonical decomposition and composition, plus two compatibility variants that additionally
fold distinctions such as a typographic ligature into its component letters — so that software
can compare and index strings meaningfully.[^uax15]

A separate specification defines where one user-perceived character ends and the next begins,
because that boundary rarely coincides with a code point. A base letter with several marks, a
pair of regional indicators forming a flag, and a sequence of characters joined by a
zero-width joiner are each a single grapheme cluster made of several code points, and text
editors, cursors and character counts are expected to respect the clusters rather than the
units.[^uax29]

## Scripts and unification

By the mid-2020s the standard defined more than 150,000 characters across more than 160
scripts, many of them no longer written. [[Cuneiform]] was encoded in 2006 and Egyptian
hieroglyphs in 2009, which let scholars exchange original and transliterated text in ordinary
files instead of in proprietary fonts. The typology worked out in the study of
[[Writing systems]] — logographic, syllabic, alphabetic, abugida — supplies the categories
that the standard's script divisions follow. Recording systems that do not represent language
as discrete written signs, such as the knotted cords of the Andean [[Quipu|quipu]], fall
outside what a character encoding can represent at all.

The most contested technical decision was Han unification, which treats ideographs of common
origin and meaning used in Chinese, Japanese and Korean as a single character despite regional
differences in shape, on the ground that those differences are typographic. Critics in East
Asia argued that the differences are not always merely typographic, and variation selectors
together with a registry of documented variant forms were added later as a partial remedy.

## Adding a character

Encoding a new character is a committee process. A proposal goes to the Unicode Technical
Committee and in parallel to the international working group responsible for ISO/IEC 10646,
the standard with which Unicode has been kept character-for-character identical, and it must
document actual use rather than an aspiration.[^proposals] Proposals for historic and
minority scripts are typically prepared by specialists in collaboration with user communities,
and a script can take years to move from proposal to publication.

Emoji arrived by a different route. Japanese mobile operators had shipped incompatible
pictograph sets from the late 1990s, and encoding them became necessary for messages to
survive being passed between carriers and onto other platforms. A large block was added in
2010, and the repertoire has since grown as much by composition as by new code points: skin
tone modifiers were introduced in 2015, and zero-width joiner sequences let several existing
characters be presented as one image where a font supports it.[^uts51] Because emoji proposals
attract public attention in a way that script proposals do not, they have made the committee's
ordinary work unusually visible.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Unicode",
            "subtitle": "Character encoding standard",
            "rows": [
                {"kind": "header", "value": "Standard"},
                {"kind": "row", "label": "Developer", "value": "Unicode Consortium"},
                {"kind": "row", "label": "First published", "value": "1991"},
                {
                    "kind": "row",
                    "label": "Companion standard",
                    "value": "ISO/IEC 10646 (Universal Coded Character Set)",
                },
                {
                    "kind": "row",
                    "label": "Governing body",
                    "value": "Unicode Technical Committee",
                },
                {"kind": "header", "value": "Code space"},
                {"kind": "row", "label": "Range", "value": "U+0000 to U+10FFFF"},
                {
                    "kind": "row",
                    "label": "Capacity",
                    "value": "1,114,112 code points in 17 planes of 65,536",
                },
                {
                    "kind": "row",
                    "label": "Encoding forms",
                    "value": "UTF-8, UTF-16, UTF-32",
                },
                {
                    "kind": "full",
                    "value": (
                        "Once assigned, a code point is never reused and its name is "
                        "never changed."
                    ),
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "unicode",
                "title": "The Unicode Standard",
                "url": "https://www.unicode.org/versions/latest/",
                "authors": "",
                "publisher": "Unicode Consortium",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "rfc3629",
                "title": "RFC 3629: UTF-8, a transformation format of ISO 10646",
                "url": "https://www.rfc-editor.org/rfc/rfc3629",
                "authors": "F. Yergeau",
                "publisher": "Internet Engineering Task Force",
                "published_on": "November 2003",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "w3techs",
                "title": "Usage statistics of character encodings for websites",
                "url": "https://w3techs.com/technologies/overview/character_encoding",
                "authors": "",
                "publisher": "W3Techs",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "uax15",
                "title": "Unicode Standard Annex #15: Unicode Normalization Forms",
                "url": "https://www.unicode.org/reports/tr15/",
                "authors": "",
                "publisher": "Unicode Consortium",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "uax29",
                "title": "Unicode Standard Annex #29: Unicode Text Segmentation",
                "url": "https://www.unicode.org/reports/tr29/",
                "authors": "",
                "publisher": "Unicode Consortium",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "uts51",
                "title": "Unicode Technical Standard #51: Unicode Emoji",
                "url": "https://www.unicode.org/reports/tr51/",
                "authors": "",
                "publisher": "Unicode Consortium",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "proposals",
                "title": "Submitting character proposals",
                "url": "https://www.unicode.org/pending/proposals.html",
                "authors": "",
                "publisher": "Unicode Consortium",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Writing systems",
            "Cuneiform",
            "Quipu",
            "The printing press",
            "Information theory",
            "World Wide Web",
        ],
        "aliases": ["UTF-8"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["character encoding", "utf-8", "writing systems", "standards"],
    },
    {
        "title": "Steam engine",
        "category": "Engineering and Technology",
        "categories": ["History", "Physics"],
        "short_description": "The engine that turned heat into work and made mechanical power portable",
        "summary": (
            "Steam engines produce work from the heat of steam. From Newcomen's "
            "atmospheric pump of 1712 through Watt's separate condenser to "
            "high-pressure locomotives, they gave industry its first portable power."
        ),
        "content": """**Steam engines** are heat engines that produce mechanical work from the thermal
energy of steam. Water is boiled in a vessel heated from outside, the steam is admitted to a
cylinder or to a turbine, and either its pressure or its condensation drives a piston or a set
of blades. Because the fuel burns outside the working space, a steam engine can be fired with
anything that makes heat. It was the first source of mechanical power independent of muscle,
wind and falling water, and its spread through the eighteenth and nineteenth centuries
reorganised mining, manufacturing and travel.[^britannica-steam]

## Principle of operation

Two properties of [[Water|water]] make the machine possible. Boiling expands a given mass
enormously — at atmospheric pressure steam occupies roughly 1,600 times the volume of the
liquid it came from — so a modest quantity of fuel can fill a large cylinder. Condensation
reverses the change just as sharply: cooling steam back to water leaves a near vacuum behind
it, so the weight of the surrounding atmosphere can be used as the working force. The earliest
successful engines exploited the second effect; later ones exploited the first.

Any such machine is bound by the limit [[Heat engine|common to all heat engines]]. Work can be
extracted only from heat passing from a hotter body to a colder one, and the fraction
recoverable is set by the two temperatures. A steam engine therefore needs a boiler and a cold
sink, and its efficiency rises as boiler pressure and temperature rise. None of this was
understood when the first engines were built. It was deduced from them afterwards.

## Precursors

Hero of Alexandria described, in the first century, an aeolipile: a sphere mounted on bearings
with two bent nozzles, spun by steam from a boiler beneath it. It converted heat into rotation
and did no useful work, and nothing in the surviving Greek or Roman record connects it with
machinery. The practical line begins in the seventeenth century, when the weight of the
atmosphere was first being measured. Denis Papin, who had built a pressure vessel with a
safety valve in 1679, showed in 1690 that steam condensed inside a cylinder would draw a
piston down against atmospheric pressure — the operating principle of nearly every engine
built for the following century, demonstrated at model scale.

Thomas Savery patented a working pump in 1698. It had no piston at all: steam filled a closed
vessel, cold water poured over the outside condensed it, and the resulting vacuum drew mine
water up a pipe, after which admitting steam again forced that water higher. Savery advertised
the device in 1702 as the miner's friend, but its lift was small, its fuel consumption
enormous and its soldered vessels liable to burst. His patent, extended by Act of Parliament
to 1733, was drawn broadly enough to cover any engine raising water by fire, so his successors
worked under licence from it.

## The atmospheric engine

Thomas Newcomen, an ironmonger of Dartmouth, assembled the working machine. In his engine a
boiler fed steam into a large open-topped cylinder beneath a piston; a jet of cold water was
then sprayed into the cylinder, the steam condensed, and atmospheric pressure forced the
piston down. The piston hung by chains from one end of a great rocking beam whose other end
lifted the rods of a pit pump. The first installation recorded at work stood at a colliery
near Dudley, in Staffordshire, in 1712.[^britannica-newcomen]

The design was self-regulating and nearly indestructible, and it did something no other
machine could: it drained coal and tin workings faster than water seeped in, which allowed
mines to be sunk deeper than had ever been possible. It was also extravagantly wasteful,
because each stroke chilled the whole cylinder and the next charge of steam had to reheat the
metal before it could do any work. Thermal efficiency was well under one per cent. At a
pit-head, where unsaleable small coal was effectively free, that scarcely mattered, and
hundreds of Newcomen engines were built in Britain and on the Continent during the eighteenth
century. Away from the coalfields — in the Cornish copper and tin mines, where fuel arrived by
sea — the fuel bill was the entire problem.[^hills]

## Watt's separate condenser

James Watt, an instrument maker working for the University of Glasgow, was asked in 1763 to
repair a model Newcomen engine and found that it could not be kept running. Measuring the heat
absorbed in boiling water, he located the loss: the cylinder was being alternately heated and
chilled, and most of the fuel went into reheating metal rather than into work. In 1765 he saw
the remedy — condense the steam in a separate vessel kept permanently cold and connected to
the cylinder through a valve, so that the cylinder itself never has to cool. He patented it in
1769 and, after years of failing to have large cylinders bored accurately enough, went into
partnership with the Birmingham manufacturer Matthew Boulton in 1775. The patent was extended
by Act of Parliament to 1800.[^britannica-watt]

The separate condenser, together with a steam jacket around the cylinder and a closed top
admitting steam rather than air above the piston, cut fuel consumption to roughly a quarter or
a third of that of a Newcomen engine of the same power. Boulton and Watt sold the saving
itself: instead of charging a price for the engine, they took an annual royalty calculated from
the coal the customer no longer burned. Several hundred engines were supplied before the patent
lapsed, and Watt's vigorous defence of it in the courts is generally reckoned to have delayed
rival improvements for a generation.

## Rotary motion and control

A pumping engine only had to rock a beam. Driving machinery required continuous rotation, and
Watt's firm delivered it from 1782, using a sun-and-planet gear because the obvious solution,
a crank and flywheel, had already been patented by a rival. Three further inventions turned the
engine into a general prime mover. The double-acting cylinder, admitting steam alternately
above and below the piston, doubled the work per stroke, but it required the piston rod to push
as well as pull; Watt's parallel motion linkage of 1784 guided a rigid rod in a straight line
from the arc of a swinging beam. The centrifugal governor, adopted at the end of the 1780s,
hung two weights from a spindle geared to the output shaft: as speed rose the weights swung
outward and closed a throttle valve, holding the engine near a set speed without an attendant.
It is among the earliest feedback controllers in general industrial use, and it became a
standard worked example when the mathematics of control was developed in the following century.

Watt and his assistant John Southern also devised the indicator, a small gauge that traced
pressure against piston position on a card while the engine ran. The closed loop it drew showed
at a glance where work was being lost, and it let engines be compared honestly. The firm kept
it a trade secret for years. It survives as the pressure–volume diagram on which the analysis
of every thermodynamic cycle is still drawn.

Once rotation was available, power became portable in a way that water power never had been. A
mill no longer had to stand beside a river with sufficient fall, and works could be built where
coal, labour and transport were, which is a substantial part of why
[[The Industrial Revolution|industrialisation]] concentrated where it did.

## High pressure and mobility

Watt worked barely above atmospheric pressure and opposed anything higher as lethal. Once his
patent expired the obvious economy became available: steam well above atmospheric pressure does
useful work simply by expanding, so a high-pressure engine can dispense with the condenser
altogether and exhaust to the air, which makes it far smaller and lighter for a given output.
Richard Trevithick in Cornwall and Oliver Evans in Philadelphia arrived at such engines
independently from about 1800.[^britannica-trevithick] Trevithick ran a steam carriage on a
road at Camborne in 1801, and on 21 February 1804 a locomotive of his hauled ten tons of iron
in five wagons, together with a crowd of passengers, along the Penydarren tramroad in south
Wales — the first recorded journey of a steam locomotive on rails.

Higher pressure also meant boiler explosions, which killed in numbers through the nineteenth
century and drove the development of safety valves, fusible plugs, better plate and riveting,
and eventually statutory inspection. In Cornwall the same high-pressure steam was pushed for
economy rather than compactness. The monthly publication of each mine's engine duty — the work
done per bushel of coal consumed — turned fuel efficiency into a public competition between
engineers, and Cornish engines working steam expansively improved several-fold on the best
Watt engines.[^hills]

## Railways and ships

Applied to transport, the steam engine broke a constraint older than written history: the speed
of land travel had always been the speed of a horse. Colliery lines were using locomotives in
the 1810s, and the Stockton and Darlington Railway of 1825 carried public traffic. The Rainhill
trials of 1829, held to choose motive power for the line between Liverpool and Manchester, were
won by the locomotive Rocket, which combined a multi-tubular boiler — many small flues giving a
large heating surface in a short barrel — with exhaust steam directed up the chimney, so that
the fire was drawn harder the faster the engine worked. Those two features defined the
locomotive boiler for the next century. The Liverpool and Manchester Railway opened in 1830 as
the first intercity line worked entirely by locomotives.

At sea the difficulty was that a ship had to carry its own fuel, which limited range. The answer
was compounding. Instead of expanding steam once, a compound engine passes it through a small
high-pressure cylinder and then a larger low-pressure one, and a triple-expansion engine
through three, which reduces the temperature swing in each cylinder and extracts more work from
the same steam. Combined with surface condensers, which returned distilled feed water to the
boiler and so permitted higher pressures without salt scaling, triple-expansion engines from
the 1880s made long ocean routes commercially practical and remained standard in cargo ships
for decades.

## Theory after practice

The science of heat was largely assembled by studying these machines rather than the reverse. In
1824 Sadi Carnot asked what limited their performance and answered that the maximum efficiency
of any engine depends only on the temperatures between which it works and not at all on the
working substance — a conclusion he reached while heat was still generally thought to be a
conserved fluid.[^britannica-carnot] Carnot's argument, restated by Clausius and by Kelvin
around 1850, became the second law, and the quantity Clausius named [[Entropy|entropy]] made
the limit quantitative. [[Thermodynamics]] thus began as an audit of steam plant and ended as a
constraint on stars and living cells. The traffic ran both ways: engineers received the
idealised cycle against which real engines are measured, and a clear reason to raise boiler
temperature and pressure.

The chemistry of [[Combustion]] set the other practical ceiling, through the temperature a
firebox could reach and the materials that could contain it. The resulting record is stark. A
Newcomen engine recovered well under one per cent of the energy in its coal; a good Watt engine
a few per cent; a late triple-expansion marine engine roughly ten; a modern supercritical steam
plant approaches forty-five. Every gain came either from raising the top temperature and
pressure or from cutting losses to the surroundings.

## Turbines and decline

The reciprocating engine's ceiling was speed: masses that stop and reverse twice per revolution
cannot be driven fast without destroying themselves. The steam turbine, demonstrated by Charles
Parsons in 1884, removed the reversal by passing steam through successive rings of blades and
turning a shaft directly at thousands of revolutions per minute.[^britannica-turbine] Turbines
scale to enormous power in a small volume, and within a generation they had displaced piston
engines in electricity generation and in large ships. On land, electric motors fed from central
stations replaced the line shafting that stationary engines had driven, and the
internal-combustion engine took over road transport. Main-line steam locomotives ended regular
service on British railways in 1968.

## Legacy

As a piston machine the steam engine is obsolete. As a principle it is not. Most of the world's
electricity is still produced by boiling water and passing the steam through a turbine, whether
the heat comes from coal, gas, nuclear fission or concentrated sunlight, and the cycle being
analysed is the one Watt's indicator first traced on a card.[^britannica-turbine] The engine
also left a measurable mark on the atmosphere, because it made large-scale coal burning
economically rational and so began the transfer of long-buried fossil carbon back into the air
that now dominates the [[The carbon cycle|carbon cycle]].
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Steam engine",
            "subtitle": "External-combustion heat engine",
            "rows": [
                {"kind": "header", "value": "Characteristics"},
                {"kind": "row", "label": "Working fluid", "value": "Water and steam"},
                {
                    "kind": "row",
                    "label": "Combustion",
                    "value": "External, so almost any heat source will serve",
                },
                {
                    "kind": "row",
                    "label": "Output motion",
                    "value": "Reciprocating (piston) or rotary (turbine)",
                },
                {"kind": "header", "value": "Key developments"},
                {"kind": "row", "label": "1698", "value": "Savery patents a pistonless pump"},
                {
                    "kind": "row",
                    "label": "1712",
                    "value": "Newcomen's atmospheric beam engine at work near Dudley",
                },
                {
                    "kind": "row",
                    "label": "1769",
                    "value": "Watt patents the separate condenser",
                },
                {
                    "kind": "row",
                    "label": "1804",
                    "value": "Trevithick's high-pressure locomotive runs on rails",
                },
                {
                    "kind": "row",
                    "label": "1884",
                    "value": "Parsons demonstrates the steam turbine",
                },
                {"kind": "header", "value": "Thermal efficiency"},
                {"kind": "row", "label": "Newcomen engine", "value": "Under 1 per cent"},
                {
                    "kind": "row",
                    "label": "Triple-expansion marine engine",
                    "value": "About 10 per cent",
                },
                {
                    "kind": "row",
                    "label": "Modern supercritical plant",
                    "value": "Approaching 45 per cent",
                },
                {
                    "kind": "full",
                    "value": (
                        "Watt defined one horsepower as 33,000 foot-pounds per minute; "
                        "the SI unit of power is named after him."
                    ),
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "britannica-steam",
                "title": "Steam engine",
                "url": "https://www.britannica.com/technology/steam-engine",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica-newcomen",
                "title": "Thomas Newcomen",
                "url": "https://www.britannica.com/biography/Thomas-Newcomen",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica-watt",
                "title": "James Watt",
                "url": "https://www.britannica.com/biography/James-Watt",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica-trevithick",
                "title": "Richard Trevithick",
                "url": "https://www.britannica.com/biography/Richard-Trevithick",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica-carnot",
                "title": "Carnot cycle",
                "url": "https://www.britannica.com/science/Carnot-cycle",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica-turbine",
                "title": "Steam turbine",
                "url": "https://www.britannica.com/technology/steam-turbine",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "hills",
                "title": "Power from Steam: A History of the Stationary Steam Engine",
                "url": "",
                "authors": "Richard L. Hills",
                "publisher": "Cambridge University Press",
                "published_on": "1989",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Heat engine",
            "Thermodynamics",
            "Entropy",
            "Combustion",
            "The Industrial Revolution",
            "The carbon cycle",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["steam power", "industrial revolution", "thermodynamics", "locomotives"],
    },
]
