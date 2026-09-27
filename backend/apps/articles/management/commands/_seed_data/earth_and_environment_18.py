"""Earth and Environment — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "The carbon cycle",
        "category": "Earth and Environment",
        "categories": ["Life Sciences", "Chemistry and Materials"],
        "short_description": "How carbon moves between air, ocean, life and rock, over years or aeons",
        "summary": (
            "The carbon cycle is the set of exchanges that move carbon between the atmosphere, "
            "the ocean, living things and rock. A fast biological loop turns over in years to "
            "centuries; a slow geological loop takes hundreds of thousands of years."
        ),
        "content": """**The carbon cycle** is the set of exchanges that move carbon among the atmosphere, the
ocean, living organisms, soils and rock. Carbon is the framework element of organic chemistry
and, as carbon dioxide and methane, an infrared-absorbing gas, so its distribution among these
reservoirs governs both the chemistry of life and the temperature of the surface. Geochemists
divide the system into a fast biological loop that turns over in years to centuries and a slow
geological loop whose steps take hundreds of thousands to hundreds of millions of
years.[^nasa_carbon]

## Reservoirs

Stocks are quoted in gigatonnes of carbon (Gt C). The atmosphere is the smallest mobile reservoir
and the best measured: at a global mean of 419.31 parts per million of carbon dioxide in 2023 it
held about 890 Gt C, since one part per million corresponds to roughly 2.12 Gt C.[^gcb2024] Land
plants hold on the order of 450 Gt C and soils several times more. The ocean is much larger, with
some 38,000 Gt C dissolved in it, about nine-tenths as bicarbonate ion rather than as dissolved
gas. Sedimentary rock dwarfs all of them, holding tens of millions of gigatonnes, mostly as
limestone and dolomite.[^ipcc_ar6_ch5] Because the atmospheric pool is the smallest, modest
imbalances in the fluxes crossing it change its concentration quickly.

## The fast biological loop

[[Photosynthesis]] on land fixes roughly 120 Gt C a year, of which plants respire about half
straight back, and marine phytoplankton fix a further 50 Gt C or so. Respiration by animals
and microbes, the decay of litter and [[Combustion|combustion]] in wildfires return almost exactly
as much, which is why the pre-industrial atmosphere held near 280 parts per million for thousands
of years.

The balance is not perfect month to month. Charles David Keeling began continuous carbon dioxide
measurements at Mauna Loa in 1958, at about 315 parts per million, and found a sawtooth
superimposed on a rise: concentration falls through the northern growing season and recovers over
the northern winter, peaking in May and bottoming out in late September or October.[^keeling] The
amplitude is about six parts per million at Mauna Loa, larger at high northern latitudes where
there is more land, and small in the Southern Hemisphere.[^noaa_trends]

## Ocean chemistry and the two pumps

Carbon dioxide dissolves in [[Water|water]], and in seawater it does more than dissolve: it
reacts, forming carbonic acid, which gives up hydrogen ions to leave bicarbonate and carbonate.
The resulting buffer lets the ocean hold roughly fifty times as much carbon as the atmosphere,
and it means that uptake acidifies. Surface seawater has become about 0.1 pH unit more acidic
since the eighteenth century, lowering the carbonate saturation that calcifying organisms such
as those building a [[Coral reef|coral reef]] depend on.[^ipcc_ar6_ch5]

Two mechanisms carry carbon into the deep: a solubility pump, because cold high-latitude water
dissolves more gas and then sinks out of contact with the air, and a biological pump, because a
fraction of the organic matter made by plankton sinks as particles before it is respired. Both are
limited by how fast the deep ocean is renewed, which is why ocean uptake of an emission pulse
takes centuries. Rivers, the return arm of [[The water cycle|the water cycle]], deliver on the
order of half a gigatonne of carbon a year to the sea.

## The slow geological loop

Beyond a hundred thousand years the biological loop nets out and the geological one governs.
Rainwater carrying dissolved carbon dioxide is a weak acid that attacks silicate
minerals, releasing calcium, magnesium and bicarbonate ions; rivers carry these to the ocean,
where organisms and chemical precipitation lock them into calcium carbonate, so the sequence
buries one molecule of atmospheric carbon dioxide for each calcium ion delivered. Carbonate rock
returns to the interior at subduction zones, a consequence of
[[Plate tectonics|plate tectonics]], and the carbon comes back through volcanic and metamorphic
degassing at roughly 0.1 Gt C a year.[^ipcc_ar6_ch5]

Because silicate weathering runs faster in warm, wet conditions it acts as a negative feedback:
a warmer planet weathers faster, draws carbon dioxide down faster and cools. Walker, Hays and
Kasting set it out in 1981; it is the standard explanation for how surface temperatures stayed
habitable for billions of years under a brightening Sun.

A second slow path buries organic carbon rather than carbonate. Where sediment accumulates fast
or bottom water is short of oxygen, a small percentage of organic matter escapes decay; the
Carboniferous coal measures, laid down between about 359 and 299 million years ago, and the
marine source rocks of most petroleum are the result. Burning them, which began in earnest with
[[The Industrial Revolution|the Industrial Revolution]], short-circuits a loop that took millions
of years to close.

## Reading the record

Air trapped in polar ice gives direct samples of past atmospheres. The EPICA core from Dome C
in Antarctica extends the carbon dioxide record to 800,000 years and shows it oscillating between
roughly 180 parts per million at glacial maxima and 280 to 300 during interglacials, closely
tracking Antarctic temperature through eight [[Ice age|glacial cycles]].[^luthi2008] Accounting for
those swings, which require the ocean to have absorbed the missing glacial carbon, remains a
central problem.

Isotopes identify the source of added carbon. Photosynthesis discriminates against the heavier
stable isotope carbon-13, so plant matter and the fossil fuels derived from it are depleted in it,
and as that carbon enters the air the atmosphere's carbon-13 ratio falls. Further back, sharp
negative excursions in the carbon-13 content of marine carbonate mark episodes when large amounts
of light carbon entered the system quickly; one accompanies the end-Permian
[[Extinction|extinction]], another the warming at the Palaeocene-Eocene boundary.

## The human perturbation

In 2023 fossil fuel use and cement production released 10.1 gigatonnes of carbon and land-use
change, chiefly deforestation, about 1.0. Of the 11.1 Gt C total, the ocean took up 2.9 Gt C and
land ecosystems 2.3 Gt C, while the atmosphere gained 5.9 Gt C, equivalent to 2.79 parts per
million.[^gcb2024] Roughly half of each year's emissions therefore stays in the air, and the
anthropogenic flux is about a hundred times the volcanic and metamorphic one it competes with.

Atmospheric carbon dioxide is now more than 50 per cent above its pre-industrial value of about
278 parts per million, higher than anywhere in the ice-core record.[^gcb2024] Such a perturbation
is long-lived because of the structure of the cycle itself: ocean mixing removes the excess over
centuries, sea-floor carbonate dissolution over roughly ten thousand years, and silicate
weathering only over hundreds of thousands. A substantial fraction of a large release therefore
stays in the atmosphere and ocean for millennia.[^ipcc_ar6_ch5]
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "The carbon cycle",
            "subtitle": "Global biogeochemical cycle",
            "rows": [
                {"kind": "header", "value": "Major reservoirs"},
                {"kind": "row", "label": "Atmosphere", "value": "About 890 Gt C at 420 ppm CO2"},
                {"kind": "row", "label": "Ocean, dissolved", "value": "About 38,000 Gt C"},
                {"kind": "row", "label": "Soils", "value": "Roughly 1,500 to 2,400 Gt C"},
                {"kind": "row", "label": "Vegetation", "value": "About 450 Gt C"},
                {
                    "kind": "row",
                    "label": "Sedimentary rock",
                    "value": "Tens of millions of Gt C",
                },
                {"kind": "header", "value": "Principal fluxes"},
                {
                    "kind": "row",
                    "label": "Land photosynthesis",
                    "value": "About 120 Gt C per year, gross",
                },
                {
                    "kind": "row",
                    "label": "Ocean and air exchange",
                    "value": "About 80 Gt C per year each way",
                },
                {
                    "kind": "row",
                    "label": "Fossil fuel and cement",
                    "value": "10.1 Gt C in 2023",
                },
                {
                    "kind": "row",
                    "label": "Volcanic and metamorphic",
                    "value": "Roughly 0.1 Gt C per year",
                },
                {"kind": "header", "value": "Turnover"},
                {"kind": "row", "label": "Fast biological loop", "value": "Years to centuries"},
                {
                    "kind": "row",
                    "label": "Slow geological loop",
                    "value": "Hundreds of thousands to hundreds of millions of years",
                },
                {
                    "kind": "full",
                    "value": "One part per million of atmospheric CO2 corresponds to about "
                    "2.12 gigatonnes of carbon.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "nasa_carbon",
                "title": "The Carbon Cycle",
                "url": "https://earthobservatory.nasa.gov/features/CarbonCycle",
                "authors": "Holli Riebeek",
                "publisher": "NASA Earth Observatory",
                "published_on": "2011",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "gcb2024",
                "title": "Global Carbon Budget 2024",
                "url": "https://essd.copernicus.org/articles/17/965/2025/",
                "authors": "Pierre Friedlingstein and others",
                "publisher": "Earth System Science Data",
                "published_on": "March 2025",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.5194/essd-17-965-2025",
                "quote": "",
            },
            {
                "key": "noaa_trends",
                "title": "Trends in Atmospheric Carbon Dioxide",
                "url": "https://gml.noaa.gov/ccgg/trends/",
                "authors": "",
                "publisher": "NOAA Global Monitoring Laboratory",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "keeling",
                "title": "The Keeling Curve",
                "url": "https://keelingcurve.ucsd.edu/",
                "authors": "",
                "publisher": "Scripps Institution of Oceanography",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "luthi2008",
                "title": (
                    "High-resolution carbon dioxide concentration record 650,000-800,000 years "
                    "before present"
                ),
                "url": "https://www.nature.com/articles/nature06949",
                "authors": "Dieter Lüthi and others",
                "publisher": "Nature",
                "published_on": "May 2008",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature06949",
                "quote": "",
            },
            {
                "key": "ipcc_ar6_ch5",
                "title": "Global Carbon and other Biogeochemical Cycles and Feedbacks",
                "url": "https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-5/",
                "authors": "",
                "publisher": "IPCC Sixth Assessment Report, Working Group I",
                "published_on": "2021",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Photosynthesis",
            "Combustion",
            "Ice age",
            "The water cycle",
            "Extinction",
            "The Industrial Revolution",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["biogeochemistry", "carbon dioxide", "climate", "geochemistry"],
    },
    {
        "title": "Aurora",
        "category": "Earth and Environment",
        "categories": ["Physics", "Astronomy and Space"],
        "short_description": "Light high in the atmosphere where particles from space strike it",
        "summary": (
            "An aurora is the glow produced when charged particles guided by a planet's magnetic "
            "field collide with atoms and molecules in the upper atmosphere. On Earth the "
            "displays ring the magnetic poles and brighten during geomagnetic storms."
        ),
        "content": """**An aurora** is light emitted by atoms and molecules in the upper atmosphere after they
have been struck by charged particles funnelled down along a planet's magnetic field. On Earth
the displays are called the aurora borealis in the northern hemisphere and the aurora australis
in the southern, and they occur mainly in two ovals encircling the magnetic poles, at altitudes
between about 90 and 150 kilometres.[^swpc_aurora]

## The chain from Sun to sky

The energy comes from the solar wind, a plasma streaming out of the Sun's corona at 300 to 800
kilometres a second and carrying the Sun's magnetic field with it. Where that interplanetary
field has a southward component it reconnects with Earth's field on the dayside; magnetic flux
is then dragged over the poles into the long magnetotail, where it accumulates until a second
reconnection releases it and hurls plasma back towards the planet. Electrons from that plasma
are accelerated to energies of a few thousand electronvolts in a region some thousands of
kilometres above the atmosphere, guided by field lines into the polar upper atmosphere, and
stopped by collisions there.[^swpc_storms]

The circuit closes through currents flowing along the field lines. Kristian Birkeland inferred
them from magnetic measurements on expeditions in northern Norway and from laboratory
experiments with a magnetised sphere in the early 1900s; satellite magnetometers confirmed them
some six decades later, and they are now called Birkeland currents. The whole coupling is a
problem in [[Electromagnetism|electromagnetism]] on a planetary scale.

## Why the colours are what they are

Auroral light is not thermal. Each colour is the relaxation of a particular excited state, so
the spectrum is a set of discrete lines and molecular bands rather than a continuum, the same
distinction that separates a glowing filament from a discharge lamp in the physics of
[[Light|light]].

The dominant green at 557.7 nanometres comes from atomic oxygen moving between two states that
a selection rule forbids. The transition is slow, with a lifetime of about 0.7 seconds, long
enough that the emitting atom must sit in air thin enough to escape a de-exciting collision
first. That condition is met above roughly 100 kilometres, and the green layer is
correspondingly sharp.[^angeo2023] Atomic oxygen also produces red light at 630.0 nanometres
from a still more strongly forbidden transition, with a lifetime near 110 seconds; lower down,
collisions quench it long before it can radiate, so red appears only high in tall displays.
Ionised molecular nitrogen supplies a blue-violet band at 427.8 nanometres, and neutral
nitrogen a crimson fringe along the lower edge of the most intense forms, where fast electrons
penetrate below 100 kilometres. Human colour vision is poor at low light levels, so a faint
aurora looks grey-white to the eye while a camera records it as green.

## The auroral oval and the substorm

Aurorae are not scattered at random through the polar regions. They occupy an oval centred on
each geomagnetic pole, some hundreds of kilometres wide, typically crossing 65 to 70 degrees
magnetic latitude when activity is low and expanding towards the equator as it rises. The oval
is fixed with respect to the Sun rather than rotating with the Earth, so a given town passes
beneath its most active part in the hours around magnetic midnight.[^swpc_tutorial]

Activity arrives in substorms lasting one to three hours: a quiet growth phase in which arcs
drift equatorward, an explosive expansion in which the lowest arc brightens, surges poleward
and breaks into rays, curls and patches, and a slow recovery. Geomagnetic conditions are
summarised by the three-hourly Kp index on a scale of 0 to 9, and storms by a five-step scale
running from G1 to G5.[^swpc_storms] During a G5 storm on 10 and 11 May 2024, displays were
reported far outside the usual zone across Europe, North America and Asia.

## Records and effects

Candidate accounts of aurorae appear in Assyrian astrological reports written in
[[Cuneiform|cuneiform]] in the seventh century BC and in Chinese, Greek and Roman sources. The
Latin name aurora borealis came into use in the seventeenth century and is conventionally
credited to [[Galileo Galilei]].

The strongest geomagnetic storm on record occurred on 1 and 2 September 1859, after Richard
Carrington and Richard Hodgson independently observed a flare in visible light on the Sun's
disc. Aurorae were reported from Cuba, Hawaii and Colombia in the north and from Santiago in
the south; telegraph lines threw sparks and shocked operators, in some accounts set message
paper alight, and in a few cases carried traffic with their batteries disconnected
altogether.[^green2006]

Those effects are induction: a fluctuating magnetic field drives currents in long conductors.
The modern equivalents are power grids and pipelines. A geomagnetic storm on 13 March 1989
collapsed the Hydro-Québec network in well under two minutes and left about six million people
without electricity for some nine hours. Auroral-zone ionisation also disrupts high-frequency
radio and adds ranging error to satellite navigation, including the
[[Global Positioning System]], while heating of the thermosphere raises drag on low-orbiting
satellites.[^swpc_storms]

Aurorae are not confined to Earth. Any magnetised planet with an atmosphere can have them, and
most of [[The Solar System|the Solar System]] does. Jupiter's are permanent and vastly more
powerful, driven largely by the planet's rapid rotation and by sulphur and oxygen supplied from
volcanic Io rather than by the solar wind; Saturn, Uranus and Neptune have them too; and Mars,
which lacks a global field, shows patchy aurorae over magnetised crust as well as diffuse and
proton varieties.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Aurora",
            "subtitle": "Upper-atmosphere optical phenomenon",
            "rows": [
                {
                    "kind": "row",
                    "label": "Also called",
                    "value": "Aurora borealis in the north, aurora australis in the south",
                },
                {
                    "kind": "row",
                    "label": "Typical altitude",
                    "value": "About 90 to 150 km; red emission higher",
                },
                {
                    "kind": "row",
                    "label": "Energy source",
                    "value": "Solar wind coupled to Earth's magnetosphere",
                },
                {"kind": "header", "value": "Principal emissions"},
                {
                    "kind": "row",
                    "label": "Green, 557.7 nm",
                    "value": "Atomic oxygen; excited state lasts about 0.7 s",
                },
                {
                    "kind": "row",
                    "label": "Red, 630.0 nm",
                    "value": "Atomic oxygen; excited state lasts about 110 s",
                },
                {
                    "kind": "row",
                    "label": "Blue-violet, 427.8 nm",
                    "value": "Ionised molecular nitrogen",
                },
                {"kind": "header", "value": "Geography and timing"},
                {
                    "kind": "row",
                    "label": "Auroral oval",
                    "value": "Roughly 65 to 70 degrees magnetic latitude when quiet",
                },
                {
                    "kind": "row",
                    "label": "Activity indices",
                    "value": "Kp 0 to 9; geomagnetic storm scale G1 to G5",
                },
                {
                    "kind": "full",
                    "value": "The strongest recorded geomagnetic storm, on 1 and 2 September "
                    "1859, pushed aurorae as far as Cuba and Hawaii.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "swpc_aurora",
                "title": "Aurora",
                "url": "https://www.swpc.noaa.gov/phenomena/aurora",
                "authors": "",
                "publisher": "NOAA Space Weather Prediction Center",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "swpc_tutorial",
                "title": "Aurora Tutorial",
                "url": "https://www.swpc.noaa.gov/content/aurora-tutorial",
                "authors": "",
                "publisher": "NOAA Space Weather Prediction Center",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "swpc_storms",
                "title": "Geomagnetic Storms",
                "url": "https://www.swpc.noaa.gov/phenomena/geomagnetic-storms",
                "authors": "",
                "publisher": "NOAA Space Weather Prediction Center",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "angeo2023",
                "title": "The altitude of green OI 557.7 nm and blue N2+ 427.8 nm aurora",
                "url": "https://angeo.copernicus.org/articles/41/1/2023/",
                "authors": "",
                "publisher": "Annales Geophysicae",
                "published_on": "2023",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "green2006",
                "title": "Duration and extent of the great auroral storm of 1859",
                "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5215858/",
                "authors": "James L. Green and Scott Boardsen",
                "publisher": "Advances in Space Research",
                "published_on": "2006",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Electromagnetism",
            "The Solar System",
            "Light",
            "Global Positioning System",
            "Cuneiform",
        ],
        "aliases": ["Northern lights"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["space weather", "magnetosphere", "atmosphere", "solar wind"],
    },
    {
        "title": "Extinction",
        "category": "Earth and Environment",
        "categories": ["Life Sciences"],
        "short_description": "The end of a lineage, and the events in which many ended at once",
        "summary": (
            "Extinction is the death of the last member of a species or larger group. It runs at "
            "a low background rate punctuated by mass extinctions, five of which stand out in "
            "the marine fossil record of the past 540 million years."
        ),
        "content": """**Extinction** is the end of a lineage: the death of the last individual of a species, or
the disappearance of a whole genus, family or larger group. It is the normal fate of species,
since the overwhelming majority of those that have ever lived are gone, and for most of
geological time it proceeds at a low background rate, interrupted by brief intervals in which a
large share of the world's species vanished together.

## Establishing that species end

That species could end was not obvious: fossils of unfamiliar animals were long read as remains of
creatures still living somewhere unexplored. Georges Cuvier settled the question in 1796 by
comparing fossil elephant teeth and jaws from Siberia and North America with those of living
elephants, showing that the mammoth and the mastodon were distinct species with no living
counterparts. Extinction thereafter needed explaining, and
[[Charles Darwin]] supplied an explanation: if varieties better suited to local conditions
replace their rivals, extinction is the other half of [[Natural selection|natural selection]]
rather than an anomaly.

## Background and mass extinction

Average species durations in the marine fossil record run to a few million years, which implies
a background rate of roughly 0.1 to 1 extinctions per million species-years. Mass extinctions
are the intervals that exceed this by a wide margin; the working definition is the loss of about
three-quarters of species in a geologically short time.[^barnosky2011]

David Raup and Jack Sepkoski put the distinction on a statistical footing in 1982 with a
compilation of marine families. Four events, late in the Ordovician, Permian, Triassic and
Cretaceous, stood out as statistically distinct; a fifth, in the Devonian, was elevated but not
significant in that dataset.[^raup1982] The
set became known as the big five; later work has confirmed the events and shown the Devonian
crisis to be a long series of pulses rather than one catastrophe.

## The five great events

The end-Ordovician event, about 444 million years ago, came in two pulses framing a short, severe
glaciation: falling sea level drained the shallow shelves where most marine life lived, and the
return of warm, oxygen-poor water finished the job, culling brachiopods, trilobites, graptolites
and conodonts.

The Late Devonian crisis, centred about 372 million years ago, fell hardest on reefs. The great
stromatoporoid and tabulate-coral structures of the period collapsed and nothing comparable was
built for tens of millions of years, a turning point in the history of the [[Coral reef|reef]] as
an ecosystem.

The end-Permian event, 252 million years ago, was the largest. Subtracting the background losses
scattered through the interval puts it at roughly 81 per cent of marine species rather than the
90 to 96 per cent once quoted.[^stanley2016] Uranium-lead dates from ash beds at Meishan in
China place the main extinction between 251.941 and 251.880 million years ago, an interval of
about 60,000 years, and show that a sharp negative swing in [[The carbon cycle|carbon-cycle]]
chemistry began just before it.[^burgess2014] Eruption of the Siberian Traps, among the largest
flood-basalt provinces known, is the leading cause, acting through warming, anoxia and
acidification.

The end-Triassic event, about 201 million years ago, coincided with the Central Atlantic Magmatic
Province, the volcanism that accompanied the opening of the Atlantic, and left the dinosaurs
dominant on land.

The end-Cretaceous event, 66 million years ago, is the best understood. In 1980 Luis and Walter
Alvarez, with Frank Asaro and Helen Michel, reported iridium enrichments of 20 to 160 times
background in boundary clays from Italy, Denmark and New Zealand, and argued for the impact of a
body about 10 kilometres across.[^alvarez1980] The Chicxulub structure beneath the Yucatán
peninsula, some 180 kilometres wide, was later matched to that layer, and a 2010 review of the
global stratigraphy concluded that the impact triggered the extinction, with Deccan Traps
volcanism as an accompanying stress rather than the trigger.[^schulte2010] Non-avian dinosaurs,
ammonites, most planktonic foraminifera and the large marine reptiles went; birds, mammals,
teleost fish and flowering plants came through.

## Patterns and causes

The recurring ingredients are flood-basalt volcanism, bolide impact, rapid climate change, ocean
anoxia and large, fast disturbances to the carbon cycle, often several at once and on a stage set
by the arrangement of continents and shelves that [[Plate tectonics|plate tectonics]] provides. Extinction is not random with respect to biology:
large-bodied, specialised and geographically restricted groups fare worse than small generalists
with wide ranges, and organisms that build carbonate skeletons or depend on a steady supply of
food from [[Photosynthesis|photosynthesis]] are especially exposed. Diversity typically needs five
to ten million years to rebuild, and the groups that expand afterwards are rarely those that
dominated before.

## Reconstructing an extinction

An extinction is inferred from a species' last appearance in the rock, and that inference is
fragile. Sampling is incomplete, so a lineage's true end is later than its last known fossil;
where the shortfall is uneven between groups, an abrupt event is smeared into an apparent gradual
decline, a bias named the Signor-Lipps effect. Palaeontologists therefore combine several lines of
evidence: isotope excursions in carbonate, pollen and spore counts, microfossil abundance, impact
ejecta and radiometric dates from interbedded ash. A spike in fern spores just above the
Cretaceous-Palaeogene boundary in North America, for instance, records the recolonisation of
devastated ground. Local disappearance must also be distinguished from global loss: the 1883
eruption of [[Krakatoa]] sterilised the surviving islands, but plants and animals returned from
Java and Sumatra within decades, and nothing was extinguished.

## The documentary record

Extinctions since about 1500 are recorded in writing. The dodo of Mauritius was last credibly
reported in 1662, Steller's sea cow was hunted out within 27 years of its description in 1741, the
great auk ended in 1844, the last passenger pigeon died in the Cincinnati Zoo on 1 September 1914,
and the last captive thylacine died in 1936. Islands are over-represented: endemic species with
small populations and no experience of introduced predators are the most vulnerable, and
archipelagos such as [[The Galápagos Islands]] have lost forms including the Pinta Island
tortoise, whose last individual died in 2012. The IUCN Red List records several hundred species as
Extinct, certainly an undercount, since most species have never been described and a last
occurrence is rarely witnessed.[^iucn]

A 2011 review concluded that current losses, although unusually rapid, had not reached the
three-quarters threshold, but that losing the species then listed as critically endangered would
cross it within a few centuries.[^barnosky2011] Pleistocene losses sit between the two records:
most large mammal genera of the Americas and Australia disappeared during and after the last
[[Ice age]], with climate change and human arrival both implicated, and the woolly mammoth
survived on Wrangel Island until roughly 4,000 years ago.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Extinction",
            "subtitle": "Loss of a species or lineage",
            "rows": [
                {"kind": "header", "value": "The big five mass extinctions"},
                {
                    "kind": "row",
                    "label": "End-Ordovician",
                    "value": "About 444 million years ago",
                },
                {
                    "kind": "row",
                    "label": "Late Devonian",
                    "value": "About 372 million years ago",
                },
                {"kind": "row", "label": "End-Permian", "value": "About 252 million years ago"},
                {"kind": "row", "label": "End-Triassic", "value": "About 201 million years ago"},
                {"kind": "row", "label": "End-Cretaceous", "value": "66 million years ago"},
                {"kind": "header", "value": "Measures"},
                {
                    "kind": "row",
                    "label": "Background rate",
                    "value": "Roughly 0.1 to 1 extinctions per million species-years",
                },
                {
                    "kind": "row",
                    "label": "Mass extinction",
                    "value": "Conventionally the loss of about 75 per cent of species",
                },
                {
                    "kind": "row",
                    "label": "Largest known loss",
                    "value": "About 81 per cent of marine species, end-Permian",
                },
                {"kind": "header", "value": "Evidence"},
                {
                    "kind": "full",
                    "value": "Last appearances in rock, carbon-isotope excursions, pollen and "
                    "spore counts, impact ejecta and dated volcanic ash beds.",
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "raup1982",
                "title": "Mass Extinctions in the Marine Fossil Record",
                "url": "https://www.science.org/doi/10.1126/science.215.4539.1501",
                "authors": "David M. Raup and J. John Sepkoski Jr.",
                "publisher": "Science",
                "published_on": "March 1982",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.215.4539.1501",
                "quote": "",
            },
            {
                "key": "stanley2016",
                "title": "Estimates of the magnitudes of major marine mass extinctions in earth "
                "history",
                "url": "https://www.pnas.org/doi/10.1073/pnas.1613094113",
                "authors": "Steven M. Stanley",
                "publisher": "Proceedings of the National Academy of Sciences",
                "published_on": "2016",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1073/pnas.1613094113",
                "quote": "",
            },
            {
                "key": "burgess2014",
                "title": "High-precision timeline for Earth's most severe extinction",
                "url": "https://www.pnas.org/doi/10.1073/pnas.1317692111",
                "authors": "Seth D. Burgess, Samuel Bowring and Shu-zhong Shen",
                "publisher": "Proceedings of the National Academy of Sciences",
                "published_on": "2014",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1073/pnas.1317692111",
                "quote": "",
            },
            {
                "key": "alvarez1980",
                "title": "Extraterrestrial Cause for the Cretaceous-Tertiary Extinction",
                "url": "https://www.science.org/doi/10.1126/science.208.4448.1095",
                "authors": "Luis W. Alvarez, Walter Alvarez, Frank Asaro and Helen V. Michel",
                "publisher": "Science",
                "published_on": "June 1980",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.208.4448.1095",
                "quote": "",
            },
            {
                "key": "schulte2010",
                "title": "The Chicxulub Asteroid Impact and Mass Extinction at the "
                "Cretaceous-Paleogene Boundary",
                "url": "https://www.science.org/doi/10.1126/science.1177265",
                "authors": "Peter Schulte and others",
                "publisher": "Science",
                "published_on": "March 2010",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.1177265",
                "quote": "",
            },
            {
                "key": "barnosky2011",
                "title": "Has the Earth's sixth mass extinction already arrived?",
                "url": "https://www.nature.com/articles/nature09678",
                "authors": "Anthony D. Barnosky and others",
                "publisher": "Nature",
                "published_on": "March 2011",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/nature09678",
                "quote": "",
            },
            {
                "key": "iucn",
                "title": "Summary Statistics",
                "url": "https://www.iucnredlist.org/resources/summary-statistics",
                "authors": "",
                "publisher": "IUCN Red List of Threatened Species",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Natural selection",
            "Ice age",
            "Plate tectonics",
            "Krakatoa",
            "The Galápagos Islands",
            "Charles Darwin",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["palaeontology", "mass extinction", "biodiversity", "stratigraphy"],
    },
]
