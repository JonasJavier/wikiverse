"""Medicine and the Mind — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Memory",
        "category": "Medicine and the Mind",
        "categories": [
            "Life Sciences",
            "Computing and Information",
        ],
        "short_description": "How nervous systems encode, store and retrieve experience",
        "summary": (
            "Memory is the set of processes by which a nervous system encodes information, "
            "retains it and retrieves it later. Work on amnesic patients and on synaptic change "
            "established that it is not one faculty but several, each with its own anatomy."
        ),
        "content": """**Memory** is the set of processes by which a nervous system encodes
information, retains it over time and retrieves it later. Experimental psychology and clinical
neurology converged during the twentieth century on the conclusion that memory is not a single
faculty but several partly independent systems, separable by what they hold, how long they hold it,
and which structures of the brain they require.[^squire2009]

## Measuring retention

Systematic study began with Hermann Ebbinghaus, who in the early 1880s used himself as his only
subject. He learned lists of nonsense syllables, chosen to carry no prior meaning, and measured how
much of the original effort was saved when he relearned a list after intervals from twenty minutes
to a month. The resulting forgetting curve falls steeply within hours and then flattens, and the
savings method he published in 1885 established that retention could be given a number at
all.[^ebbinghaus]

Three later results fixed the modern picture of the short intervals. George Sperling showed in 1960
that a briefly flashed grid of letters leaves a visual trace that is almost complete but decays
within about a second, so an observer cued immediately can report whichever row is asked for while
one cued a second later can report almost nothing.[^sperling1960] George Miller had argued in 1956
that immediate recall is limited to roughly seven items, and that the limit falls on chunks rather
than raw symbols, so recoding digits into dates or letters into words increases the information
carried without increasing the count.[^miller1956] Alan Baddeley and Graham Hitch replaced the
passive short-term store in 1974 with a working memory built from separate subsystems for
speech-based and for visual material, coordinated by a limited attentional executive.[^baddeley1974]

## Systems

Long-term memory is conventionally divided into declarative memory, whose contents can be brought to
mind and stated, and non-declarative or procedural memory, which shows itself only in performance.
Declarative memory divides again into episodic memory for particular events, carrying a time and a
place, and semantic memory for facts detached from the occasion of learning. Non-declarative memory
covers motor and perceptual skills, conditioning and priming, and depends on the basal ganglia,
cerebellum and cortex rather than on the structures that support recollection.[^squire2009]

## The patient H.M.

The separation between these systems was established by a single surgical outcome. In 1953 the
neurosurgeon William Beecher Scoville removed the medial temporal lobes on both sides of the brain
of Henry Molaison, then twenty-seven, to control epilepsy that had not responded to drugs. The
seizures improved. The memory loss was severe and permanent, and the examination Brenda Milner
reported with Scoville in 1957 found intelligence, language, perception and immediate recall
unimpaired while the capacity to form new lasting memories was destroyed.[^scoville1957] Molaison
could hold a conversation and describe his childhood, but never learned the plan of the house he
moved to afterwards, and did not recognise the researchers who tested him for the next five decades.

He was not incapable of all learning. Milner found that his accuracy at tracing a figure seen only
in a mirror improved from session to session although he denied ever having attempted the task — the
first clear demonstration that skill learning proceeds without conscious recollection. Molaison, who
died in 2008, became the most closely studied individual in the history of neuroscience; Suzanne
Corkin, who worked with him from 1962, later set out both the findings and the arrangements made to
protect him.[^corkin2013] His brain was afterwards cut into 2,401 sections seventy micrometres thick
and reassembled as a digital model, which showed that the operation had spared more of the posterior
hippocampus than the 1957 report assumed.[^annese2014]

## Synaptic change

Attempts to localise the physical trace by removing tissue failed; Karl Lashley, who spent decades
excising areas of cortex from trained rats, concluded that no single site held a given memory. The
mechanism accepted now is a change in the strength of connections between neurons rather than
storage in a place. In 1973 Timothy Bliss and Terje Lømo reported that a brief burst of
high-frequency stimulation of the pathway entering the hippocampus of a rabbit left the response to
later single pulses enlarged for half an hour to ten hours. Long-term potentiation of this kind,
since traced to changes in receptor numbers and in the shape of individual synapses, is the standard
cellular model of learning.[^blisslomo1973] Because that machinery sits inside a single
[[The cell|cell]], the physical basis of a memory is continually remade from new protein.

Newly formed memories remain labile before they stabilise, a process called consolidation;
disruption during that window impairs retention, and sleep appears to assist it. On a longer
timescale, memories that begin as hippocampus-dependent become retrievable from the cortex over
months and years, which is why damage to the hippocampus produces a retrograde amnesia graded by
age, sparing the remote past. Retrieval reopens the window: Karim Nader and colleagues showed in
2000 that a reactivated fear memory in rats could be abolished by blocking protein synthesis in the
amygdala, implying that recalling a memory obliges the brain to store it again.[^nader2000]

## Reconstruction and error

Because retrieval rebuilds rather than replays, remembering is systematically editable. Elizabeth
Loftus and John Palmer showed in 1974 that changing a single verb in a question about a filmed
collision — whether the cars "smashed" or "hit" — altered the speeds witnesses estimated and made
them more likely to report broken glass the film did not contain.[^loftus1974] Findings of this kind
reshaped the conduct of police interviews and identity parades, and they give the
[[Ship of Theseus]] problem a concrete form: continuity of self rests on a record revised each time
it is consulted.

The vertebrate arrangement is not the only one available. The [[Octopus]], whose neurons are mostly
distributed through its arms rather than gathered into the kind of central organ described by
[[Human anatomy]], learns visual and tactile discriminations and retains them for weeks without any
structure equivalent to a hippocampus.

## Memory outside the body

Societies have offloaded memory onto durable objects for at least five thousand years.
[[Cuneiform]] tablets began as administrative records, fixing quantities no scribe then needed to
hold in mind; the Andean [[Quipu]] encoded numbers and categories in knotted and coloured cords;
indexes, archives and catalogues followed. [[Plato]] has Socrates object in the *Phaedrus* that
writing would weaken the memories of those who relied on it, an argument made again about every
later storage technology. The word itself was carried into engineering, where the addressable stores
of a computer are called memory, and the borrowing runs both ways: systems in
[[Artificial intelligence]] are described as consolidating and forgetting, while theories of human
memory took their vocabulary of encoding, storage and retrieval from information processing.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Memory",
            "subtitle": "Encoding, storage and retrieval in nervous systems",
            "rows": [
                {"kind": "header", "value": "Main divisions"},
                {
                    "kind": "row",
                    "label": "Declarative",
                    "value": "Episodic (events) and semantic (facts)",
                },
                {
                    "kind": "row",
                    "label": "Non-declarative",
                    "value": "Skills, conditioning, priming",
                },
                {
                    "kind": "row",
                    "label": "Working memory",
                    "value": "Seconds-long; a few chunks at a time",
                },
                {"kind": "header", "value": "Structures involved"},
                {
                    "kind": "row",
                    "label": "Hippocampus",
                    "value": "Formation of new declarative memories",
                },
                {"kind": "row", "label": "Amygdala", "value": "Emotional and fear memory"},
                {
                    "kind": "row",
                    "label": "Basal ganglia, cerebellum",
                    "value": "Habits and motor skills",
                },
                {"kind": "header", "value": "Landmark evidence"},
                {
                    "kind": "row",
                    "label": "1885",
                    "value": "Ebbinghaus measures the forgetting curve[^ebbinghaus]",
                },
                {
                    "kind": "row",
                    "label": "1957",
                    "value": "Scoville and Milner report patient H.M.[^scoville1957]",
                },
                {
                    "kind": "row",
                    "label": "1973",
                    "value": "Bliss and Lømo describe long-term potentiation",
                },
                {
                    "kind": "full",
                    "value": "Memory is several partly independent systems, not one faculty.",
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/5/5b/"
                "Hippocampus_and_seahorse_cropped.JPG"
            ),
            "alt": "A dissected human hippocampus and fornix beside a preserved seahorse",
            "caption": (
                "A human hippocampus and fornix beside a seahorse, the animal that gave the "
                "structure its name"
            ),
            "credit": "Professor Laszlo Seress",
            "license": "CC BY-SA 3.0",
            "source_url": (
                "https://commons.wikimedia.org/wiki/File:"
                "Hippocampus_and_seahorse_cropped.JPG"
            ),
        },
        "references": [
            {
                "key": "squire2009",
                "title": "The Legacy of Patient H.M. for Neuroscience",
                "url": "https://doi.org/10.1016/j.neuron.2008.12.023",
                "authors": "Larry R. Squire",
                "publisher": "Neuron 61(1), 6-9",
                "published_on": "January 2009",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1016/j.neuron.2008.12.023",
                "quote": "",
            },
            {
                "key": "ebbinghaus",
                "title": "Memory: A Contribution to Experimental Psychology",
                "url": "https://psychclassics.yorku.ca/Ebbinghaus/index.htm",
                "authors": "Hermann Ebbinghaus, translated by H. A. Ruger and C. E. Bussenius",
                "publisher": "Teachers College, Columbia University",
                "published_on": "1913 (German original 1885)",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sperling1960",
                "title": "The information available in brief visual presentations",
                "url": "https://doi.org/10.1037/h0093759",
                "authors": "George Sperling",
                "publisher": "Psychological Monographs 74(11), 1-29",
                "published_on": "1960",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1037/h0093759",
                "quote": "",
            },
            {
                "key": "miller1956",
                "title": (
                    "The magical number seven, plus or minus two: some limits on our capacity "
                    "for processing information"
                ),
                "url": "https://doi.org/10.1037/h0043158",
                "authors": "George A. Miller",
                "publisher": "Psychological Review 63(2), 81-97",
                "published_on": "1956",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1037/h0043158",
                "quote": "",
            },
            {
                "key": "baddeley1974",
                "title": "Working Memory",
                "url": "https://doi.org/10.1016/S0079-7421(08)60452-1",
                "authors": "Alan D. Baddeley and Graham Hitch",
                "publisher": "Psychology of Learning and Motivation 8, 47-89",
                "published_on": "1974",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1016/S0079-7421(08)60452-1",
                "quote": "",
            },
            {
                "key": "scoville1957",
                "title": "Loss of recent memory after bilateral hippocampal lesions",
                "url": "https://doi.org/10.1136/jnnp.20.1.11",
                "authors": "William Beecher Scoville and Brenda Milner",
                "publisher": "Journal of Neurology, Neurosurgery and Psychiatry 20(1), 11-21",
                "published_on": "February 1957",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1136/jnnp.20.1.11",
                "quote": "",
            },
            {
                "key": "corkin2013",
                "title": (
                    "Permanent Present Tense: The Unforgettable Life of the Amnesic Patient, H.M."
                ),
                "url": "https://openlibrary.org/isbn/9780465031597",
                "authors": "Suzanne Corkin",
                "publisher": "Basic Books",
                "published_on": "2013",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-465-03159-7",
                "quote": "",
            },
            {
                "key": "annese2014",
                "title": (
                    "Postmortem examination of patient H.M.'s brain based on histological "
                    "sectioning and digital 3D reconstruction"
                ),
                "url": "https://doi.org/10.1038/ncomms4122",
                "authors": "Jacopo Annese and colleagues",
                "publisher": "Nature Communications 5, 3122",
                "published_on": "28 January 2014",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/ncomms4122",
                "quote": "",
            },
            {
                "key": "blisslomo1973",
                "title": (
                    "Long-lasting potentiation of synaptic transmission in the dentate area of "
                    "the anaesthetized rabbit following stimulation of the perforant path"
                ),
                "url": "https://doi.org/10.1113/jphysiol.1973.sp010273",
                "authors": "Timothy V. P. Bliss and Terje Lømo",
                "publisher": "The Journal of Physiology 232(2), 331-356",
                "published_on": "1973",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1113/jphysiol.1973.sp010273",
                "quote": "",
            },
            {
                "key": "nader2000",
                "title": (
                    "Fear memories require protein synthesis in the amygdala for reconsolidation "
                    "after retrieval"
                ),
                "url": "https://doi.org/10.1038/35021052",
                "authors": "Karim Nader, Glenn E. Schafe and Joseph E. LeDoux",
                "publisher": "Nature 406, 722-726",
                "published_on": "17 August 2000",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/35021052",
                "quote": "",
            },
            {
                "key": "loftus1974",
                "title": (
                    "Reconstruction of automobile destruction: an example of the interaction "
                    "between language and memory"
                ),
                "url": "https://doi.org/10.1016/S0022-5371(74)80011-3",
                "authors": "Elizabeth F. Loftus and John C. Palmer",
                "publisher": "Journal of Verbal Learning and Verbal Behavior 13(5), 585-589",
                "published_on": "October 1974",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1016/S0022-5371(74)80011-3",
                "quote": "",
            },
        ],
        "see_also": [
            "Human anatomy",
            "Ship of Theseus",
            "Artificial intelligence",
            "Octopus",
            "Quipu",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "neuroscience",
            "cognitive psychology",
            "hippocampus",
            "amnesia",
            "learning",
        ],
    },
    {
        "title": "Plate tectonics",
        "category": "Earth and Environment",
        "categories": [
            "Geography and Places",
            "History",
        ],
        "short_description": "The theory that Earth's outer shell is broken into moving plates",
        "summary": (
            "Plate tectonics is the theory that Earth's rigid outer shell is divided into moving "
            "plates whose interactions build mountains and ocean basins. Dismissed as continental "
            "drift before 1960, it was established by magnetic evidence from the sea floor."
        ),
        "content": """**Plate tectonics** is the theory that Earth's rigid outer shell is
divided into a small number of large plates which move over the hotter, weaker rock beneath, and
that almost all mountain building, volcanism and seismic activity occurs where those plates meet.
Proposed in recognisable form in 1912 and dismissed for half a century afterwards, it was
established between 1963 and 1968 by magnetic and seismic evidence gathered from the ocean floor,
and it now supplies the organising framework for the whole of the solid-earth sciences.[^usgs]

## The theory in outline

The outermost part of Earth that behaves rigidly on geological timescales is the lithosphere: the
crust together with the uppermost mantle, ranging from a few kilometres thick at mid-ocean ridges
to about 100 kilometres beneath old ocean basins and 200 kilometres or more beneath ancient
continental shields. It rests on the asthenosphere, mantle rock close enough to its melting point
to flow over millions of years. The lithosphere is broken into seven or eight major plates — the
Pacific, North American, South American, Eurasian, African, Antarctic and Indo-Australian — and
dozens of smaller ones. Each moves as a nearly rigid cap on a sphere, so its motion can be
described completely as a rotation about an axis, and speeds range from a few millimetres to about
ten centimetres a year.[^usgs]

Plates are created and destroyed rather than permanent. New oceanic lithosphere forms at mid-ocean
ridges and is consumed at subduction zones, so the sea floor is young: the oldest ocean crust still
in place, in the western Pacific, is Jurassic, on the order of 180 million years old, while
continental rocks older than four billion years survive because continental crust is too buoyant to
be dragged down.[^muller2008] Roughly half of the present ocean floor has formed in the last 65
million years.

## Continental drift and its rejection

The fit between the coasts of Africa and South America had been remarked on since the sixteenth
century, and Antonio Snider-Pellegrini published maps of a joined and then separated Atlantic in
1858. The first sustained argument came from Alfred Wegener, a German meteorologist, who set out
continental displacement in lectures in January 1912 and then in *Die Entstehung der Kontinente und
Ozeane*, first published in 1915 and revised through a fourth edition in 1929. Wegener assembled
matching coastlines with matching geological provinces across the Atlantic, identical late
Palaeozoic fossil floras on southern continents now separated by oceans, and glacial deposits in
India, Africa, Australia and South America that made sense only if those landmasses had once sat
together near the pole as the single supercontinent he named Pangaea.[^wegener1929]

The evidence was strong; the mechanism was not. Wegener proposed that continents ploughed through
the ocean floor, driven by tidal forces and by a poleward flight force, and geophysicists
calculated correctly that such forces were orders of magnitude too small and that the sea floor was
far too strong to be furrowed. A symposium of the American Association of Petroleum Geologists in
1926 was overwhelmingly hostile, and outside South Africa and a scattering of sympathisers drift
remained a fringe position for a generation. Wegener died in November 1930 on the Greenland ice
sheet during his fourth expedition, shortly after his fiftieth birthday. Arthur Holmes suggested in
1931 that convection in a mantle heated by radioactive decay could carry continents as passengers
and destroy ocean floor at the trailing edge, which is close to the modern answer, but the idea
stayed speculative for thirty years.[^oreskes2003]

## Evidence from the sea floor

Wartime and post-war surveying transformed the problem by mapping the two-thirds of the planet that
had been inaccessible. Marie Tharp, working from echo-sounding profiles at Columbia University,
identified a continuous rift valley running down the axis of the Mid-Atlantic Ridge in the early
1950s, and the physiographic maps she made with Bruce Heezen showed a ridge system encircling the
globe for some 60,000 kilometres. Heat flow was high along the ridges, sediment was thin at the
crest and thickened away from it, and earthquakes fell in narrow bands along ridge axes and
trenches rather than being scattered.

Harry Hess drew these facts together in a paper circulated from 1960 and published in 1962: mantle
rising beneath a ridge generates new sea floor that spreads outward and is eventually returned to
the mantle at a trench, so ocean basins are conveyor belts rather than permanent holes.[^hess1962]
Robert Dietz named the process sea-floor spreading in 1961. The decisive test came from magnetism.
Basalt erupted at a ridge cools through its Curie point and locks in the direction of the
[[Electromagnetism|magnetic field]] prevailing at the time, and the geomagnetic field reverses
polarity at irregular intervals of tens of thousands to millions of years. If Hess was right, a
ridge should therefore be flanked by stripes of alternately magnetised crust, symmetrical about the
axis and matching the reversal timescale already known from lavas on land. Fred Vine and Drummond
Matthews proposed exactly that in *Nature* in September 1963; Lawrence Morley had reached the same
conclusion independently in a paper that was rejected.[^vine1963] Magnetic profiles collected by
the research vessel *Eltanin* across the Pacific-Antarctic Ridge in 1966 displayed the predicted
symmetry with unmistakable clarity, and drilling by the *Glomar Challenger* from 1968 confirmed
that the sediment lying directly on basement grows older away from the ridge at the rate spreading
requires.

## The plate model, 1965 to 1968

What remained was the geometry. J. Tuzo Wilson showed in 1965 that the fractures offsetting ridge
segments are a new class of fault, which he called transform faults, ending abruptly where they
meet a ridge or a trench because they transfer motion from one kind of boundary to another; his
prediction about the direction of slip on them was confirmed by earthquake first-motion studies
within two years.[^wilson1965] Dan McKenzie and Robert Parker demonstrated in 1967 that the motions
of the northern Pacific could be treated as the rotation of a rigid cap on a sphere, and in 1968
W. Jason Morgan and Xavier Le Pichon extended the treatment to the whole planet, Le Pichon fitting
the global pattern of spreading rates with six large plates.[^morgan1968][^lepichon1968] Within
about three years the subject had acquired its name, its mathematics and near-universal assent —
one of the fastest reversals of consensus in the history of the physical sciences.

## Boundaries

Three kinds of boundary account for nearly all tectonic activity.

Divergent boundaries are where plates separate and new lithosphere is created. Most lie on the
ocean floor, where full spreading rates run from about two centimetres a year on the Mid-Atlantic
Ridge to around fifteen on parts of the East Pacific Rise; a few, such as the East African Rift,
cut continents. Iceland is the rare place where a ridge stands above sea level.

Convergent boundaries consume lithosphere. Where the descending plate is oceanic it bends down into
a trench and sinks, carrying water and sediment with it; the water lowers the melting point of the
overlying mantle and feeds a chain of explosive volcanoes 100 to 200 kilometres behind the trench.
The Sunda Arc that produced [[Krakatoa]] and the Andes above the Nazca Plate are of this kind, and
earthquakes can be traced down a sinking slab to depths of about 700 kilometres. The Mariana Trench,
nearly eleven kilometres deep, is the lowest point on the sea floor. Where both plates carry
continental crust neither sinks readily and the margin thickens instead: the collision of India with
Asia, which began roughly 50 million years ago and continues at four to five centimetres a year, has
raised the Himalaya and [[Mount Everest]] and roughly doubled the crustal thickness beneath Tibet.

Transform boundaries are where plates slide past one another without creating or destroying
lithosphere. The San Andreas fault in California and the Alpine fault in New Zealand are continental
examples, and they generate large shallow [[Earthquake|earthquakes]] without volcanism.

Volcanism also occurs far from any boundary, above long-lived upwellings in the mantle. As a plate
travels over one, a chain of volcanoes is built and then carried away, ageing progressively along
its length; the Hawaiian-Emperor seamounts and the hotspot beneath [[The Galápagos Islands]] are the
standard examples.

## Driving forces

Plate motion is ultimately powered by Earth's internal heat, from radioactive decay and from heat
left over from accretion, but the immediate forces act on the plates themselves. Oceanic lithosphere
cools and thickens as it ages until it is denser than the mantle beneath it, so a slab that has
begun to sink pulls the rest of its plate after it. This slab pull is generally judged the dominant
term, which is consistent with the observation that plates with long subducting margins — the
Pacific, Nazca and Cocos plates — move fastest, while plates with none, such as the African and
Antarctic, are slow. Ridge push, the gravitational sliding of lithosphere off the elevated ridge,
and drag from mantle flow beneath the plate contribute less.

## The supercontinent cycle

Because ocean basins open and close, continents are repeatedly assembled and dispersed. Wilson
recognised that an ocean can close along the lines on which it opened, and a complete opening and
closing is now called a Wilson cycle. Pangaea came together about 320 million years ago and began to
break apart around 200 million years ago; Rodinia preceded it, assembled roughly 1.1 billion years
ago, and earlier assemblies are inferred at average intervals of the order of 400 million years.

The consequences reach well beyond geology. The position and elevation of continents govern ocean
circulation and the exposure of fresh rock to weathering, and so the long-term regulation of
atmospheric carbon dioxide, which is why the opening of the Southern Ocean and the rise of the
Himalaya are both implicated in the cooling that led to the most recent [[Ice age]]. Rearranged
coastlines and shallow seas alter the distribution of habitats, and several of the mass
[[Extinction]] events in the fossil record coincide with continental reorganisation and with the
flood basalt eruptions that accompany it. The limestone platforms built by a [[Coral reef]] record
the slow vertical motion of the sea floor that [[Charles Darwin]] inferred from Pacific atolls long
before subsidence had any explanation.

## Measurement today

Plate velocities derived from magnetic stripes are averages over millions of years. Since the 1980s
the same motions have been measured directly by space geodesy — very long baseline interferometry,
satellite laser ranging and permanent receivers of the [[Global Positioning System]] — and the two
kinds of estimate agree closely, while the geodetic networks additionally resolve strain
accumulating across individual faults at the millimetre level.[^argus2011] Global models now
describe the motion of dozens of plates rather than six.

Earth remains the only body in [[The Solar System]] known to have plate tectonics. Venus, of nearly
the same size and internal heat budget, has a volcanically resurfaced crust with no plates and no
spreading ridges, while Mars and the Moon are single rigid shells. Why the difference exists is
unsettled, and Earth's liquid water — which weakens rock, lubricates faults and allows the dense
minerals that make a slab sink — is the requirement most often proposed, which would make plate
tectonics a statement about an unusual planetary state rather than a general rule.[^oreskes2003]
""",
        "tier": "feature",
        "kind": "concept",
        "infobox": {
            "title": "Plate tectonics",
            "subtitle": "Unifying theory of Earth's rigid outer shell",
            "rows": [
                {"kind": "header", "value": "The moving layer"},
                {
                    "kind": "row",
                    "label": "Lithosphere",
                    "value": "Crust plus uppermost mantle; a few km to over 200 km thick",
                },
                {
                    "kind": "row",
                    "label": "Rests on",
                    "value": "Asthenosphere, mantle rock that flows over millions of years",
                },
                {
                    "kind": "row",
                    "label": "Major plates",
                    "value": "Seven or eight, with dozens of smaller ones",
                },
                {
                    "kind": "row",
                    "label": "Speeds",
                    "value": "A few millimetres to about 10 cm per year",
                },
                {"kind": "header", "value": "Boundary types"},
                {
                    "kind": "row",
                    "label": "Divergent",
                    "value": "Ridges and rifts; new lithosphere created",
                },
                {
                    "kind": "row",
                    "label": "Convergent",
                    "value": "Trenches and collision belts; lithosphere consumed",
                },
                {
                    "kind": "row",
                    "label": "Transform",
                    "value": "Plates slide past one another; no volcanism",
                },
                {"kind": "header", "value": "How it was established"},
                {
                    "kind": "row",
                    "label": "1915",
                    "value": "Wegener publishes continental displacement[^wegener1929]",
                },
                {
                    "kind": "row",
                    "label": "1962",
                    "value": "Hess proposes sea-floor spreading[^hess1962]",
                },
                {
                    "kind": "row",
                    "label": "1963",
                    "value": "Vine and Matthews explain magnetic stripes[^vine1963]",
                },
                {
                    "kind": "row",
                    "label": "1965-1968",
                    "value": "Transform faults and rigid plates on a sphere[^wilson1965]",
                },
                {
                    "kind": "full",
                    "value": (
                        "Earth is the only body in the Solar System known to have plate tectonics."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Plates_tect2_en.svg",
            "alt": "World map showing the major tectonic plates and the boundaries between them",
            "caption": (
                "The major tectonic plates and their boundaries, after a map published by the "
                "United States Geological Survey"
            ),
            "credit": "United States Geological Survey, vectorised for Wikimedia Commons",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Plates_tect2_en.svg",
        },
        "references": [
            {
                "key": "usgs",
                "title": "This Dynamic Earth: The Story of Plate Tectonics",
                "url": "https://pubs.usgs.gov/gip/dynamic/dynamic.html",
                "authors": "W. Jacquelyne Kious and Robert I. Tilling",
                "publisher": "United States Geological Survey",
                "published_on": "1996",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "muller2008",
                "title": (
                    "Age, spreading rates, and spreading asymmetry of the world's ocean crust"
                ),
                "url": "https://doi.org/10.1029/2007GC001743",
                "authors": "R. Dietmar Müller, Maria Sdrolias, Carmen Gaina and Walter R. Roest",
                "publisher": "Geochemistry, Geophysics, Geosystems 9(4), Q04006",
                "published_on": "April 2008",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1029/2007GC001743",
                "quote": "",
            },
            {
                "key": "wegener1929",
                "title": "The Origin of Continents and Oceans",
                "url": "https://openlibrary.org/isbn/9780486617084",
                "authors": "Alfred Wegener, translated by John Biram",
                "publisher": "Dover Publications (translation of the fourth German edition)",
                "published_on": "1966 (original 1929)",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-486-61708-4",
                "quote": "",
            },
            {
                "key": "oreskes2003",
                "title": (
                    "Plate Tectonics: An Insider's History of the Modern Theory of the Earth"
                ),
                "url": "https://openlibrary.org/isbn/9780813341323",
                "authors": "Naomi Oreskes (editor)",
                "publisher": "Westview Press",
                "published_on": "2003",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-8133-4132-3",
                "quote": "",
            },
            {
                "key": "hess1962",
                "title": "History of Ocean Basins",
                "url": "https://doi.org/10.1130/Petrologic.1962.599",
                "authors": "Harry H. Hess",
                "publisher": (
                    "Petrologic Studies: A Volume in Honor of A. F. Buddington, "
                    "Geological Society of America"
                ),
                "published_on": "1962",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1130/Petrologic.1962.599",
                "quote": "",
            },
            {
                "key": "vine1963",
                "title": "Magnetic Anomalies Over Oceanic Ridges",
                "url": "https://doi.org/10.1038/199947a0",
                "authors": "Frederick J. Vine and Drummond H. Matthews",
                "publisher": "Nature 199, 947-949",
                "published_on": "September 1963",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/199947a0",
                "quote": "",
            },
            {
                "key": "wilson1965",
                "title": "A New Class of Faults and their Bearing on Continental Drift",
                "url": "https://doi.org/10.1038/207343a0",
                "authors": "J. Tuzo Wilson",
                "publisher": "Nature 207, 343-347",
                "published_on": "July 1965",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/207343a0",
                "quote": "",
            },
            {
                "key": "morgan1968",
                "title": "Rises, trenches, great faults, and crustal blocks",
                "url": "https://doi.org/10.1029/JB073i006p01959",
                "authors": "W. Jason Morgan",
                "publisher": "Journal of Geophysical Research 73(6), 1959-1982",
                "published_on": "15 March 1968",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1029/JB073i006p01959",
                "quote": "",
            },
            {
                "key": "lepichon1968",
                "title": "Sea-floor spreading and continental drift",
                "url": "https://doi.org/10.1029/JB073i012p03661",
                "authors": "Xavier Le Pichon",
                "publisher": "Journal of Geophysical Research 73(12), 3661-3697",
                "published_on": "15 June 1968",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1029/JB073i012p03661",
                "quote": "",
            },
            {
                "key": "argus2011",
                "title": (
                    "Geologically current motion of 56 plates relative to the no-net-rotation "
                    "reference frame"
                ),
                "url": "https://doi.org/10.1029/2011GC003751",
                "authors": "Donald F. Argus, Richard G. Gordon and Charles DeMets",
                "publisher": "Geochemistry, Geophysics, Geosystems 12(11), Q11001",
                "published_on": "November 2011",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1029/2011GC003751",
                "quote": "",
            },
        ],
        "see_also": [
            "Earthquake",
            "Mount Everest",
            "Krakatoa",
            "Extinction",
            "Ice age",
            "The Galápagos Islands",
        ],
        "aliases": [
            "Continental drift",
        ],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "geology",
            "geophysics",
            "sea-floor spreading",
            "subduction",
            "history of science",
        ],
    },
    {
        "title": "Earthquake",
        "category": "Earth and Environment",
        "categories": [
            "Engineering and Technology",
            "Geography and Places",
        ],
        "short_description": "Ground shaking from sudden slip on a fault, and the waves it sends out",
        "summary": (
            "An earthquake is the shaking produced when rock slips along a fault and releases "
            "stored elastic strain as seismic waves. The size of the source and the shaking felt "
            "at any one place are measured on separate scales."
        ),
        "content": """**An earthquake** is the shaking of the ground produced when rock slips
along a fault and releases the elastic strain that has accumulated in it, part of the stored energy
radiating away as seismic waves. Nearly all large earthquakes occur at the boundaries between the
plates of [[Plate tectonics]], and the belt around the rim of the Pacific accounts for most of them.

## Faults and rupture

The modern account of the mechanism dates from the San Francisco earthquake of 18 April 1906, after
which Harry Fielding Reid compared survey measurements made across the San Andreas fault before and
after the event and found that the ground on either side had been progressively deformed for decades
and had then snapped back. In Reid's elastic rebound model, strain builds in rock adjoining a locked
fault, friction holds the two surfaces until the shear stress across them exceeds it, and the rock
on each side then springs towards a less strained shape, sliding past its neighbour in seconds.
Friction recovers after slip, so the cycle repeats; this stick-slip behaviour is why earthquakes
recur on the same structures.[^scholz2019]

Rupture begins at a point, the hypocentre, and spreads across the fault surface at one to three
kilometres a second. The area that slips and the amount of slip together set the size of the event:
a magnitude 6 rupture may be ten kilometres long with about a metre of slip, while the magnitude 9.1
Sumatra-Andaman earthquake of 26 December 2004 tore roughly 1,300 kilometres of plate boundary with
displacements locally over 20 metres.[^usgs2004] The largest earthquakes of all are thrust events on
subduction interfaces, because those gently inclined surfaces offer the greatest contact area
available to rupture at once.

## Seismic waves

Two kinds of wave travel through the body of the planet. P waves are compressional, alternately
squeezing and stretching the rock along the direction of travel, and are the fastest — about six
kilometres a second in the upper crust — so they arrive first. S waves are shear waves, in which
material moves across the direction of travel; they travel at roughly three and a half kilometres a
second and cannot pass through liquid at all, and the shadow they cast on the far side of the planet
was the evidence that Earth's outer core is molten. Slower surface waves, named after Rayleigh and
Love, run along the ground and usually do most of the damage at distance.

The interval between the P and S arrivals gives the distance to the source, so records from three or
more stations locate it. Frequencies in a strong-motion record run from below a tenth of a hertz to
tens of hertz, overlapping the lowest [[Sound]] a person can hear, and resolving that record with
the [[Fourier transform]] yields the spectrum engineers compare against the natural periods of a
structure.

## Measuring size and effect

Charles Richter's scale of 1935 assigned a local magnitude from the largest amplitude recorded on a
standard seismograph, corrected for distance, on a base-ten logarithmic scale.[^richter1935] It
saturates for very large events, so modern catalogues use moment magnitude, developed by Hiroo
Kanamori, Thomas Hanks and others, which is computed from the seismic moment — the product of fault
area, average slip and rock rigidity — and is therefore tied to the energy actually
released.[^hanks1979] The scales agree over the middle of their range, where one unit of magnitude
is a factor of ten in wave amplitude and about thirty-two in radiated energy. The largest
instrumentally recorded earthquake is the Valdivia event in Chile on 22 May 1960, at moment
magnitude 9.5, and numbers fall off with size about tenfold for each unit of magnitude, which works
out globally at ten to twenty earthquakes of magnitude 7 or above each year.[^usgsmag]

Magnitude describes the source; intensity describes the shaking at a place. The Modified Mercalli
scale runs from I, not felt, to XII, total destruction, and is assigned from observed effects, so a
single earthquake has one magnitude but many intensities. Aftershocks decay in number roughly as the
reciprocal of elapsed time, a regularity published by Fusakichi Omori in 1894 and still the basis of
aftershock forecasts.[^utsu1995]

## Tsunamis

An earthquake that displaces the sea floor vertically displaces the water above it, and the
resulting wave train travels at a speed set by the water depth: in four kilometres of ocean about
200 metres a second, or some 700 kilometres an hour. In the open sea such a wave may be less than a
metre high with a wavelength of hundreds of kilometres and pass unnoticed beneath a ship, but on
reaching the continental shelf it slows, shortens and rises. The 2004 Indian Ocean tsunami killed
more than 230,000 people in fourteen countries, most of whom had no warning at all.[^usgs2004] The
Tohoku earthquake of 11 March 2011, catalogued by the United States Geological Survey at moment
magnitude 9.1, moved the coast of Honshu about 2.4 metres eastward and sent waves over sea walls
built for a smaller event, killing close to twenty thousand people.[^usgs2011]

Not every destructive sea wave is seismic. The waves that caused almost all the deaths at
[[Krakatoa]] in 1883 came from volcanic collapse and from pyroclastic flows entering the water, and
the breaker in [[The Great Wave off Kanagawa]], frequently described as a tsunami, is identified in
its own Japanese title as a wave in the offing rather than one driven ashore.

## Building for shaking

Most deaths in earthquakes are caused by collapsing structures rather than by ground motion itself,
so the response has been regulatory as much as technical: California's Field Act of 1933, passed
after the Long Beach earthquake wrecked school buildings, imposed state review of school design.
Engineering practice concentrates on ductility, so that a frame deforms without losing its ability
to carry load, on avoiding weak storeys and irregular plans, and on base isolation, in which a
building rests on bearings that let the ground move beneath it.

Local ground conditions matter as much as distance from the source. Loose water-saturated sand can
lose its strength entirely and behave as a liquid, a process called liquefaction that tipped
buildings over intact at Niigata in 1964 and in Christchurch in 2011. Soft basin sediments amplify
shaking at particular periods: the magnitude 8.0 earthquake of 19 September 1985 had its epicentre
some 350 kilometres from Mexico City, but the old lake bed beneath the city resonated at around two
seconds and destroyed mid-rise buildings whose own natural period matched it, while shorter and
taller buildings largely survived.

## Forecasting and warning

Individual earthquakes cannot be predicted in the sense of naming a place, a time and a size in
advance, and claimed precursors have not survived systematic testing. What is possible is
probabilistic hazard assessment, which combines fault slip rates, historical catalogues and
trenching of prehistoric ruptures into an estimate of the shaking expected at a site over the design
life of a building, and early warning, which exploits the fact that electronic signals outrun
seismic waves. Networks in Japan, Mexico, Taiwan and the western United States detect the first
arrivals near the source and issue alerts seconds to tens of seconds before strong shaking reaches a
city, enough time to stop trains, close valves and halt surgery. The reach of the hazard is wide:
the Gorkha earthquake of 25 April 2015, on a thrust fault beneath Nepal, killed close to nine
thousand people and shook loose an avalanche that swept the base camp on [[Mount Everest]], roughly
220 kilometres from the epicentre.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Earthquake",
            "subtitle": "Sudden fault slip and the seismic waves it radiates",
            "rows": [
                {"kind": "header", "value": "Mechanism"},
                {
                    "kind": "row",
                    "label": "Cause",
                    "value": "Elastic rebound: stored strain released by slip on a fault",
                },
                {
                    "kind": "row",
                    "label": "Rupture speed",
                    "value": "1-3 km per second across the fault surface",
                },
                {"kind": "header", "value": "Waves"},
                {
                    "kind": "row",
                    "label": "P wave",
                    "value": "Compressional; about 6 km/s in the upper crust; arrives first",
                },
                {
                    "kind": "row",
                    "label": "S wave",
                    "value": "Shear; about 3.5 km/s; cannot travel through liquid",
                },
                {
                    "kind": "row",
                    "label": "Surface waves",
                    "value": "Rayleigh and Love; slowest and often most damaging",
                },
                {"kind": "header", "value": "Scales"},
                {
                    "kind": "row",
                    "label": "Magnitude",
                    "value": "One value per earthquake; moment magnitude is standard[^hanks1979]",
                },
                {
                    "kind": "row",
                    "label": "Intensity",
                    "value": "Modified Mercalli I to XII; one value per place",
                },
                {
                    "kind": "row",
                    "label": "Largest recorded",
                    "value": "Valdivia, Chile, 22 May 1960, moment magnitude 9.5",
                },
                {
                    "kind": "full",
                    "value": (
                        "Magnitude measures the source; intensity measures the shaking at a place."
                    ),
                },
            ],
        },
        "image": {
            "url": (
                "https://upload.wikimedia.org/wikipedia/commons/d/db/Quake_epicenters_1963-98.png"
            ),
            "alt": "World map with earthquake epicentres forming narrow lines around the Pacific",
            "caption": (
                "Epicentres of earthquakes recorded between 1963 and 1998, tracing the boundaries "
                "between tectonic plates"
            ),
            "credit": "NASA, DTAM project team",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Quake_epicenters_1963-98.png",
        },
        "references": [
            {
                "key": "scholz2019",
                "title": "The Mechanics of Earthquakes and Faulting",
                "url": "https://openlibrary.org/isbn/9781107163485",
                "authors": "Christopher H. Scholz",
                "publisher": "Cambridge University Press (third edition)",
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-1-107-16348-5",
                "quote": "",
            },
            {
                "key": "usgs2004",
                "title": "M 9.1 - 2004 Sumatra - Andaman Islands Earthquake",
                "url": (
                    "https://earthquake.usgs.gov/earthquakes/eventpage/"
                    "official20041226005853450_30/executive"
                ),
                "authors": "",
                "publisher": "United States Geological Survey, Earthquake Hazards Program",
                "published_on": "26 December 2004",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "usgs2011",
                "title": "M 9.1 - 2011 Great Tohoku Earthquake, Japan",
                "url": (
                    "https://earthquake.usgs.gov/earthquakes/eventpage/"
                    "official20110311054624120_30/executive"
                ),
                "authors": "",
                "publisher": "United States Geological Survey, Earthquake Hazards Program",
                "published_on": "11 March 2011",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "richter1935",
                "title": "An instrumental earthquake magnitude scale",
                "url": "https://doi.org/10.1785/BSSA0250010001",
                "authors": "Charles F. Richter",
                "publisher": "Bulletin of the Seismological Society of America 25(1), 1-32",
                "published_on": "January 1935",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1785/BSSA0250010001",
                "quote": "",
            },
            {
                "key": "hanks1979",
                "title": "A moment magnitude scale",
                "url": "https://doi.org/10.1029/JB084iB05p02348",
                "authors": "Thomas C. Hanks and Hiroo Kanamori",
                "publisher": "Journal of Geophysical Research 84(B5), 2348-2350",
                "published_on": "10 May 1979",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1029/JB084iB05p02348",
                "quote": "",
            },
            {
                "key": "usgsmag",
                "title": "Earthquake Magnitude, Energy Release, and Shaking Intensity",
                "url": (
                    "https://www.usgs.gov/programs/earthquake-hazards/"
                    "earthquake-magnitude-energy-release-and-shaking-intensity"
                ),
                "authors": "",
                "publisher": "United States Geological Survey",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "utsu1995",
                "title": (
                    "The Centenary of the Omori Formula for a Decay Law of Aftershock Activity"
                ),
                "url": "https://doi.org/10.4294/jpe1952.43.1",
                "authors": "Tokuji Utsu, Yosihiko Ogata and Ritsuko S. Matsu'ura",
                "publisher": "Journal of Physics of the Earth 43(1), 1-33",
                "published_on": "1995",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.4294/jpe1952.43.1",
                "quote": "",
            },
        ],
        "see_also": [
            "Plate tectonics",
            "Krakatoa",
            "Mount Everest",
            "Sound",
            "Fourier transform",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "seismology",
            "faults",
            "tsunami",
            "earthquake engineering",
            "hazard",
        ],
    },
]
