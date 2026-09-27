"""Earth and Environment — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Krakatoa",
        "category": "Earth and Environment",
        "categories": [
            "History",
            "Geography and Places",
        ],
        "short_description": "Indonesian volcano whose 1883 eruption was heard thousands of kilometres away",
        "summary": (
            "Krakatoa is a volcanic island group in the Sunda Strait between Java and Sumatra. "
            "Its eruption in August 1883 destroyed most of the island, killed more than 36,000 "
            "people, almost all by tsunami, and left traces in the sky worldwide for years."
        ),
        "content": """**Krakatoa** (Indonesian: *Krakatau*) is a volcanic island group in the
Sunda Strait between Java and Sumatra, Indonesia, and the site of the eruption of August
1883, one of the most destructive and most thoroughly documented volcanic events in recorded
history. Caldera collapse during the climax destroyed the greater part of the island and
killed more than 36,000 people, the overwhelming majority of them drowned by tsunamis.[^gvp]

## Setting

Krakatoa sits on the Sunda Arc, the chain of volcanoes built above the trench where the
Australian Plate descends beneath southeast Asia. Subduction margins of this kind host most
of the world's explosive volcanism and most great [[Earthquake|earthquakes]], and the arc is
a standard illustration of [[Plate tectonics|plate tectonics]] at work. Before 1883 the
island was roughly nine kilometres long and carried three coalesced cones: Rakata in the
south, a little over 800 metres high, with Danan and Perbuwatan to the north.[^verbeek1885]
The strait divides Sumatra from Java, and the villages destroyed in 1883 stood on both
shores, in the Sundanese and Javanese country whose bronze [[Gamelan|gamelan]] ensembles are
among the region's best-known traditions.

## The eruption of 1883

The volcano had last erupted around 1680. Activity resumed on 20 May 1883 with ash columns
and explosions audible in Batavia, and continued intermittently through the following
months.[^verbeek1885] The climactic phase began in the early afternoon of 26 August and
culminated in four great explosions on the morning of 27 August, the largest at about ten
o'clock local time. As the magma chamber emptied, the northern part of the island foundered,
destroying the Danan and Perbuwatan cones and leaving a submarine caldera; only the southern
remnant of Rakata and two small islands were left standing.[^gvp]

Pyroclastic flows swept outwards across the surface of the sea for tens of kilometres and
killed people on the Sumatran coast. The bulk volume of pyroclastic deposits, including the
ash that settled out of the eruption column, has been estimated at 18 to 21 cubic
kilometres, which places the event at 6 on the volcanic explosivity index — very large, but
an order of magnitude smaller than the largest eruptions known from the geological
record.[^selframpino1981]

## Tsunamis

Almost all of the deaths were caused by tsunamis generated in the strait during the
climactic explosions. Waves reported at up to about 30 metres struck the nearest shores,
destroying Anyer and Merak on the Javanese side and Telok Betong on Sumatra; the gunboat
*Berouw* was carried inland up a river valley and left stranded. The Dutch colonial
administration compiled a death toll of 36,417, and modern summaries give a figure of more
than 36,000.[^gvp] Unlike the tsunamis that follow a great [[Earthquake|earthquake]], which
are driven by sudden vertical movement of the sea floor, the 1883 waves are attributed
chiefly to pyroclastic flows entering the water and to the collapse of the volcano itself;
how much each contributed is still argued.[^selframpino1981]

## Sound and the pressure wave

The explosions of 27 August produced what is generally regarded as the loudest
[[Sound|sound]] in the historical record. Reports of gunfire or distant thunder came from
Alice Springs in central Australia and from Rodrigues in the Indian Ocean, some 4,800
kilometres from the volcano, which is close to the practical limit for a sound that remains
audible to the unaided ear.[^britannica] The lower-frequency part of the disturbance
travelled onward as an atmospheric pressure wave, and barographs at meteorological stations
around the world registered it passing repeatedly over the following days. The Royal
Society's Krakatoa Committee gathered those traces together with tide-gauge records and
observers' accounts into a report published in 1888, which remains the largest single body of
evidence on the event.[^symons1888] News reached Europe within a day over submarine telegraph
cables, making the eruption one of the first natural disasters reported around the world
while it was still under way.

## Atmospheric aftermath

Sulfur dioxide injected into the stratosphere formed a veil of sulfate aerosol that spread
around the globe within weeks. For the next two to three years observers recorded unusually
vivid red and orange twilights, a whitish halo around the Sun known as Bishop's ring after
the Honolulu clergyman who first described it, and occasional sightings of a blue or green
Sun; the Royal Society report devoted a long section to these optical effects.[^symons1888]
The aerosol also reflected sunlight, and estimates of the resulting cooling of the northern
hemisphere run to a few tenths of a degree Celsius, lasting a few years. Volcanic cooling of
this kind is brief, decaying as the aerosol falls out of the stratosphere, and it is not
comparable to the slow, orbitally paced swings that drive an [[Ice age]]. Only sustained
volcanism on a far greater scale — the flood basalt provinces, which erupted millions of
cubic kilometres over hundreds of thousands of years — is implicated in mass
[[Extinction]] events.

## Life returns

The surviving fragments were stripped bare and buried in hot ash, which turned them into a
natural experiment in how an ecosystem reassembles. A survey in 1884 found almost nothing
alive, the first animal recorded being a spider. Grasses and ferns arrived within a few
years, casuarina woodland followed, and by the middle of the twentieth century the islands
carried closed forest. The sequence has been monitored ever since and is one of the best
field tests of island biogeography available.[^thornton1996]

## Anak Krakatau

A new cone, Anak Krakatau ("child of Krakatoa"), began to build inside the 1883 caldera and
first rose above sea level in 1927; it has erupted frequently since.[^gvp] On 22 December
2018 part of its flank slid into the sea, generating a tsunami that reached the shores of the
Sunda Strait without warning and killed more than 400 people — a reminder that the hazard at
Krakatoa does not require an eruption on the scale of 1883.[^britannica]
""",
        "tier": "standard",
        "kind": "period",
        "infobox": {
            "title": "Krakatoa",
            "subtitle": "Volcanic island group, Sunda Strait, Indonesia",
            "rows": [
                {
                    "kind": "row",
                    "label": "Location",
                    "value": "Sunda Strait, between Java and Sumatra",
                },
                {
                    "kind": "row",
                    "label": "Tectonic setting",
                    "value": "Sunda Arc, above the subducting Australian Plate",
                },
                {"kind": "row", "label": "Type", "value": "Caldera with post-collapse cone"},
                {"kind": "header", "value": "The 1883 eruption"},
                {"kind": "row", "label": "Climax", "value": "26–27 August 1883"},
                {"kind": "row", "label": "Explosivity", "value": "Volcanic explosivity index 6"},
                {
                    "kind": "row",
                    "label": "Erupted volume",
                    "value": "About 18–21 cubic kilometres of pyroclastic deposits, bulk",
                },
                {
                    "kind": "row",
                    "label": "Recorded deaths",
                    "value": "More than 36,000, almost all of them from tsunamis",
                },
                {
                    "kind": "row",
                    "label": "Audible at",
                    "value": "Rodrigues, about 4,800 km away in the Indian Ocean",
                },
                {"kind": "header", "value": "Afterwards"},
                {
                    "kind": "row",
                    "label": "Present cone",
                    "value": "Anak Krakatau, first above sea level in 1927",
                },
                {
                    "kind": "row",
                    "label": "Later disaster",
                    "value": "Flank collapse and tsunami, 22 December 2018",
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/4/49/Krakatoa_eruption_lithograph.jpg",
            "alt": "Nineteenth-century lithograph of a towering eruption column rising from an island",
            "caption": (
                "The 1883 eruption as reconstructed in a lithograph published as the first plate "
                "of the Royal Society's 1888 report"
            ),
            "credit": "Lithograph by Parker & Coward, Britain",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Krakatoa_eruption_lithograph.jpg",
        },
        "references": [
            {
                "key": "gvp",
                "title": "Krakatau (262000)",
                "url": "https://volcano.si.edu/volcano.cfm?vn=262000",
                "authors": "",
                "publisher": "Global Volcanism Program, Smithsonian Institution",
                "published_on": "n.d.",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": (
                    "Caldera collapse during the catastrophic 1883 eruption destroyed Danan and "
                    "Perbuwatan cones, causing more than 36,000 fatalities, most as a result of "
                    "tsunamis."
                ),
            },
            {
                "key": "selframpino1981",
                "title": "The 1883 eruption of Krakatau",
                "url": "https://doi.org/10.1038/294699a0",
                "authors": "Stephen Self and Michael R. Rampino",
                "publisher": "Nature 294, 699–704",
                "published_on": "1981",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1038/294699a0",
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
                "publisher": "Trübner & Co., London",
                "published_on": "1888",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "verbeek1885",
                "title": "Krakatau",
                "url": "",
                "authors": "Rogier D. M. Verbeek",
                "publisher": "Imprimerie de l'État, Batavia",
                "published_on": "1885",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "thornton1996",
                "title": "Krakatau: The Destruction and Reassembly of an Island Ecosystem",
                "url": "",
                "authors": "Ian W. B. Thornton",
                "publisher": "Harvard University Press",
                "published_on": "1996",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "britannica",
                "title": "Krakatoa",
                "url": "https://www.britannica.com/place/Krakatoa",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "n.d.",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Plate tectonics",
            "Earthquake",
            "Extinction",
            "Ice age",
            "Sound",
            "Gamelan",
        ],
        "aliases": [
            "Krakatau",
        ],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "volcanoes",
            "1883 eruption",
            "indonesia",
            "tsunami",
            "sunda strait",
        ],
    },
    {
        "title": "Ice age",
        "category": "Earth and Environment",
        "categories": [
            "Geography and Places",
            "Life Sciences",
        ],
        "short_description": "Long cold intervals when ice sheets spread far beyond the poles",
        "summary": (
            "An ice age is a prolonged cold interval in which ice sheets and glaciers cover much "
            "of the land. Earth is in one now: the Quaternary glaciation, whose glacial and "
            "interglacial swings are paced by slow changes in the planet's orbit and tilt."
        ),
        "content": """**An ice age** is a prolonged interval of Earth's history during which ice
sheets and glaciers cover a large part of the land surface and global temperatures sit well
below the long-term average. By that definition the planet is in an ice age now: ice has
covered Antarctica for tens of millions of years and Greenland for millions, and the current
cold epoch, the Quaternary glaciation, began about 2.6 million years ago.

## Ice ages and glacials

A distinction matters here. An ice age in the geological sense lasts millions of years.
Within it the climate swings between glacial periods, when ice sheets push far into the
mid-latitudes, and interglacials, when they retreat to roughly their present extent. Popular
usage inverts the terms: "the Ice Age" normally means the most recent glacial period, which
ended between about 19,000 and 11,700 years ago. The present interglacial, the Holocene, is
dated from about 11,700 years ago in Greenland ice cores. The Little Ice Age, a cool interval
in parts of the world between roughly 1300 and 1850, amounted to a fraction of a degree and
was not an ice age in either sense.

## Earlier glaciations

At least five long glacial epochs are recognised in the rock record. The Huronian, about 2.4
to 2.1 billion years ago, followed the first rise of atmospheric oxygen. The Cryogenian,
about 720 to 635 million years ago, left glacial deposits at low palaeolatitudes and is the
basis of the snowball Earth hypothesis. A short, severe Late Ordovician glaciation about 445
million years ago coincides with one of the great mass [[Extinction]] events. The late
Palaeozoic ice age, roughly 360 to 260 million years ago, left matching glacial deposits and
striated pavements in South America, Africa, India and Australia; their distribution makes no
sense on the modern map, and it formed part of the evidence Alfred Wegener assembled for
continental drift, now understood through [[Plate tectonics|plate tectonics]]. Long-term
cooling is itself partly tectonic, since the opening of ocean passages and the uplift and
weathering of young mountain belts alter both heat transport and the slow drawdown of carbon
dioxide.

## Orbital pacing

Within the Quaternary, glacials and interglacials recur with a regularity that points to
astronomy. Three slow changes in Earth's orbit and spin modulate the sunlight reaching high
northern latitudes in summer, which decides whether winter snow survives the year: the
eccentricity of the orbit, with a period near 100,000 years; the tilt of the axis, which
varies between about 22.1 and 24.5 degrees over 41,000 years; and the precession of the axis,
with periods of about 19,000 to 23,000 years. Milutin Milanković worked out the insolation
consequences in the 1920s and 1930s, but the idea only won general acceptance once deep-sea
sediment cores had been analysed: in 1976 Hays, Imbrie and Shackleton showed that the climate
signal of the previous 450,000 years was concentrated in spectral peaks near 23,000, 42,000
and 100,000 years, matching the orbital periods.[^hays1976]

Orbital forcing alone is far too weak to produce the observed temperature range, so feedbacks
do most of the work. Snow and ice reflect sunlight and reinforce cooling, dust and vegetation
shift, and the ocean takes up and releases carbon dioxide. Air trapped in ice cores holds
about 180 to 190 parts per million of carbon dioxide at glacial maxima against roughly 280 in
interglacials, which makes [[The carbon cycle|the carbon cycle]] an amplifier of the orbital
signal rather than its cause. Why the 100,000-year rhythm has dominated the past million
years, when eccentricity is the weakest of the three forcings, remains unsettled; before
about a million years ago the 41,000-year beat prevailed.

## Reading the record

Nineteenth-century field geologists established glaciation from landforms. Erratic boulders
far from any outcrop of their own rock, polished and striated bedrock, and ridges of unsorted
debris are produced by ice and by very little else. Louis Agassiz assembled the argument in
*Études sur les glaciers* in 1840, extending the local observations of Jean-Pierre Perraudin,
Ignace Venetz and Jean de Charpentier into the claim that a great ice sheet had once covered
northern Europe.[^agassiz1840] Resistance was considerable. [[Charles Darwin]] read the
horizontal parallel roads of Glen Roy in Scotland as marine beaches in a paper of 1839, and
only later accepted that they are the shorelines of a lake dammed by glacier ice; he came to
regard the paper as one of his worst mistakes.[^darwin1839]

Two continuous records now underpin the chronology. Oxygen isotopes in the shells of
deep-sea foraminifera track global ice volume, because ice sheets preferentially store the
lighter isotope and leave the ocean enriched in the heavier one, and stacked records of this
kind span the whole Quaternary. Ice cores give a more direct reading: the EPICA core from
Dome C in East Antarctica recovered a sequence of eight glacial cycles, and later work on
Antarctic ice extended the record of trapped air to about 800,000 years.[^epica2004] Because
the bubbles hold samples of the atmosphere itself, cores fix past carbon dioxide and methane
concentrations by measurement rather than inference.

## The last glacial maximum

Ice sheets grew to their maximum positions between about 33,000 and 26,500 years ago, and
most began to retreat around 20,000 to 19,000 years ago.[^clark2009] The Laurentide sheet
covered Canada and the northern United States and was several kilometres thick; the
Fennoscandian sheet covered Scandinavia, the Baltic and much of northern Europe; the
Cordilleran, Patagonian and enlarged Antarctic and Greenland sheets completed the inventory.
Something like a quarter of the land surface carried ice, against roughly a tenth today.

Holding that much water on land lowered the sea by about 125 metres. Continental shelves
emerged: Beringia joined Siberia to Alaska, Doggerland joined Britain to the continent, and
Sundaland linked the islands of southeast Asia. [[The water cycle|The water cycle]] itself
ran slower, because colder air carries less moisture; deserts expanded and windblown dust in
ice and ocean cores increased, while large pluvial lakes formed in some mid-latitude basins.
[[The Sahara]] was drier and dustier than it is today, and only after the ice withdrew,
between roughly 11,000 and 5,000 years ago, did a strengthened monsoon turn much of it into
grassland and lakes.

The ice left durable landforms: the basins of the Great Lakes and the Finger Lakes, the
fjords of Norway and Chile, the moraine ridge that underlies Long Island, and the scoured
channels of eastern Washington cut by outburst floods from an ice-dammed lake. The crust is
still recovering, and Scandinavia and the land around Hudson Bay, pressed down by kilometres
of ice, are rising by up to about a centimetre a year. Human history sits inside this record:
the painted chambers at [[Lascaux cave paintings|Lascaux]] were decorated roughly 17,000
years ago, in the late glacial, when reindeer and horse ranged across a cold and open
southwestern France.

## The present interglacial

Quaternary interglacials have typically lasted on the order of ten thousand years, and the
Holocene has been unusually stable, which is part of why it serves as the reference state for
the agricultural and urban record. The end of the last glacial also coincides with the loss
of much of the world's large-mammal fauna, and how much weight to give climate change as
against human hunting in those [[Extinction|extinctions]] is still debated. By the geological
definition the planet has not left its ice age: the Greenland and Antarctic ice sheets are
still there.
""",
        "tier": "standard",
        "kind": "period",
        "infobox": {
            "title": "Ice age",
            "subtitle": "Prolonged cold interval with extensive land ice",
            "rows": [
                {"kind": "header", "value": "The current ice age"},
                {"kind": "row", "label": "Name", "value": "Quaternary glaciation"},
                {"kind": "row", "label": "Began", "value": "About 2.6 million years ago"},
                {
                    "kind": "row",
                    "label": "Present interval",
                    "value": "Holocene interglacial, from about 11,700 years ago",
                },
                {"kind": "header", "value": "Last glacial maximum"},
                {
                    "kind": "row",
                    "label": "Maximum ice",
                    "value": "About 33,000 to 26,500 years ago",
                },
                {"kind": "row", "label": "Sea level", "value": "About 125 metres below present"},
                {
                    "kind": "row",
                    "label": "Land ice",
                    "value": "Roughly a quarter of the land surface",
                },
                {"kind": "header", "value": "Orbital pacing"},
                {"kind": "row", "label": "Eccentricity", "value": "Period near 100,000 years"},
                {
                    "kind": "row",
                    "label": "Axial tilt",
                    "value": "22.1 to 24.5 degrees over 41,000 years",
                },
                {"kind": "row", "label": "Precession", "value": "About 19,000 to 23,000 years"},
                {
                    "kind": "full",
                    "value": (
                        "Earlier glacial epochs: Huronian, Cryogenian, Late Ordovician and late "
                        "Palaeozoic."
                    ),
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Ice_age_fauna_of_northern_Spain_-_Mauricio_Ant%C3%B3n.jpg",
            "alt": "Painted reconstruction of mammoths, woolly rhinoceros, horses and lions in a cold landscape",
            "caption": (
                "A reconstruction of ice-age northern Spain, with woolly mammoth, woolly "
                "rhinoceros, horses and cave lions"
            ),
            "credit": "Mauricio Antón, in Sedwick C. (2008), PLoS Biology 6(4): e99",
            "license": "CC BY 2.5",
            "source_url": "https://commons.wikimedia.org/wiki/File:Ice_age_fauna_of_northern_Spain_-_Mauricio_Ant%C3%B3n.jpg",
        },
        "references": [
            {
                "key": "hays1976",
                "title": "Variations in the Earth's Orbit: Pacemaker of the Ice Ages",
                "url": "https://doi.org/10.1126/science.194.4270.1121",
                "authors": "J. D. Hays, John Imbrie and N. J. Shackleton",
                "publisher": "Science 194, 1121–1132",
                "published_on": "1976",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.194.4270.1121",
                "quote": "",
            },
            {
                "key": "clark2009",
                "title": "The Last Glacial Maximum",
                "url": "https://doi.org/10.1126/science.1172873",
                "authors": "Peter U. Clark and others",
                "publisher": "Science 325, 710–714",
                "published_on": "2009",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1126/science.1172873",
                "quote": (
                    "Growth of the ice sheets to their maximum positions occurred between 33.0 "
                    "and 26.5 ka."
                ),
            },
            {
                "key": "epica2004",
                "title": "Eight glacial cycles from an Antarctic ice core",
                "url": "",
                "authors": "EPICA community members",
                "publisher": "Nature 429",
                "published_on": "2004",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "agassiz1840",
                "title": "Études sur les glaciers",
                "url": "",
                "authors": "Louis Agassiz",
                "publisher": "Jent & Gassmann, Neuchâtel",
                "published_on": "1840",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "darwin1839",
                "title": "Observations on the parallel roads of Glen Roy",
                "url": "",
                "authors": "Charles Darwin",
                "publisher": "Philosophical Transactions of the Royal Society of London",
                "published_on": "1839",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Plate tectonics",
            "The carbon cycle",
            "The water cycle",
            "Extinction",
            "Lascaux cave paintings",
            "The Sahara",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "glaciation",
            "quaternary",
            "palaeoclimate",
            "milankovitch cycles",
            "ice cores",
        ],
    },
    {
        "title": "The water cycle",
        "category": "Earth and Environment",
        "categories": [
            "Geography and Places",
            "Life Sciences",
        ],
        "short_description": "The continual movement of water between ocean, air, ice, land and life",
        "summary": (
            "The water cycle is the continual movement of water between the ocean, the "
            "atmosphere, ice, the land and living things, driven by solar heating and gravity. "
            "Most of it is ocean evaporation returning as rain; a small residue runs off as rivers."
        ),
        "content": """**The water cycle**, also called the hydrologic cycle, is the continual
movement of water among the ocean, the atmosphere, the land surface, the subsurface and living
organisms. It is powered by solar energy, which evaporates water, and by gravity, which brings
it back down and moves it downhill. The total inventory of water on Earth barely changes, so
the cycle is a matter of redistribution rather than of creation or loss.

## Reservoirs

Earth holds roughly 1.39 billion cubic kilometres of water, and about 96.5 per cent of it is
in the ocean.[^usgswater] Of the small freshwater remainder, the largest share is locked in
ice sheets and glaciers, with groundwater next; lakes, rivers, soil moisture and living
tissue together account for a fraction of a per cent. The atmosphere is the smallest of the
major reservoirs, holding on the order of 13,000 cubic kilometres at any moment — a layer
only about 25 millimetres deep if spread evenly over the globe — and yet every drop of
precipitation passes through it. The anomalies of the [[Water|water molecule]], in particular
the hydrogen bonding that gives it a high heat of vaporisation, set the terms on which the
whole cycle operates.

## Fluxes and residence times

The fluxes are large in comparison with the atmospheric store. Estimates of the global
budget put evaporation from the ocean at about 413,000 cubic kilometres a year against about
373,000 falling back on it as precipitation; land receives about 113,000, returns about
73,000 by evaporation and transpiration, and discharges the difference, some 40,000 cubic
kilometres, to the sea as runoff.[^trenberth2007] That residue is the water available to
rivers, and it is what makes river flow a sensitive measure of a basin's climate.

Dividing a reservoir by its throughput gives a residence time, and the values span nine
orders of magnitude. Water spends about nine days in the atmosphere, weeks to months in
rivers and soil, years to decades in lakes, years to millennia in groundwater, of the order
of 3,000 years in the ocean, and tens of thousands of years in the Antarctic ice
sheet.[^usgscycle] The brevity of the atmospheric step is why weather responds within days
to changes at the surface, while an alteration in groundwater or ice may take millennia to
work through.

The cycle is also an energy conveyor. Evaporating a kilogram of water absorbs roughly 2.5
megajoules, which is released again when the vapour condenses. That latent heat drives
thunderstorms and tropical cyclones and carries a substantial part of the heat that moves
from the tropics towards the poles.

## Processes

Water leaves the surface by evaporation from open water and soil, by transpiration through
the stomata of plants, and by sublimation directly from snow and ice; the combined land term
is usually treated as evapotranspiration. Vapour is carried by the wind, cools as it rises,
and condenses on aerosol particles to form cloud droplets or ice crystals, which grow by
collision and by the transfer of vapour from droplets to crystals until they fall as
precipitation. What lands is intercepted by vegetation, infiltrates the soil, percolates to
the water table and travels slowly as groundwater, or runs off over the surface into streams.
How much vapour the air can hold is set by temperature: the saturation vapour pressure rises
by about seven per cent for each degree Celsius of warming, which is the single most
important constraint on the cycle's response to a change in climate.[^ipcc]

## The geography of rain

The large-scale circulation decides where the water falls. Air rises near the equator,
cools and rains, then descends near 20 to 30 degrees of latitude as dry, warming air; that
descending branch is why the great subtropical deserts, [[The Sahara]] among them, sit where
they do. Monsoons arise from the seasonal reversal of the temperature contrast between land
and ocean, and mountains force air upward to produce heavy rain on the windward flank and a
rain shadow behind.

Rivers integrate the surplus of whole basins and carry it across regions that have none.
[[The Nile]] gathers most of its water from summer monsoon rain on the Ethiopian highlands
and delivers it through a desert that adds almost nothing, which is why its flood was
seasonal and predictable. Moisture can also be recycled several times over a continent: in
[[The Amazon rainforest]] transpiration returns a large share of the rain to the atmosphere,
where low-level flows carry it westward and southward, so the forest contributes materially
to its own rainfall.

## Coupling to other cycles

The cycle is tied to [[The carbon cycle|the carbon cycle]] at the scale of a single leaf,
because stomata opened to admit carbon dioxide inevitably lose water, and at the scale of
continents, because the chemical weathering of silicate rock that slowly removes carbon
dioxide from the air requires water to proceed. Climate changes the cycle in turn. During
glacial periods more water is held as land ice, sea level falls, and a colder atmosphere
carries less moisture, so the whole circulation runs cooler and drier; at the last glacial
maximum of the current [[Ice age]] the sea stood about 125 metres lower than today.

## Measuring the cycle

The question of whether rainfall is sufficient to feed rivers and springs was settled by
measurement. Pierre Perrault gauged precipitation in the upper Seine basin and compared it
with the river's discharge in *De l'origine des fontaines* of 1674, showing a large surplus;
Edmond Halley followed with experiments on evaporation rates that closed the other side of
the account.[^perrault1674] Modern monitoring combines rain gauges and river gauging stations
with satellites: precipitation radar and microwave instruments measure rainfall over the
oceans, and pairs of satellites detect month-to-month changes in groundwater and ice by
sensing tiny variations in Earth's gravity field.[^nasagpm] Stable isotopes of hydrogen and
oxygen act as a fingerprint, recording the temperature and route by which a given sample of
water travelled.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "The water cycle",
            "subtitle": "Movement of water through Earth's reservoirs",
            "rows": [
                {
                    "kind": "full",
                    "value": (
                        "Also called the hydrologic cycle. Driven by solar heating and gravity; "
                        "the planet's total water inventory is effectively fixed."
                    ),
                },
                {"kind": "header", "value": "Global inventory"},
                {
                    "kind": "row",
                    "label": "Total water",
                    "value": "About 1.39 billion cubic kilometres",
                },
                {"kind": "row", "label": "Ocean", "value": "About 96.5 per cent of the total"},
                {
                    "kind": "row",
                    "label": "Largest fresh store",
                    "value": "Ice sheets and glaciers",
                },
                {
                    "kind": "row",
                    "label": "Atmosphere",
                    "value": "Order of 13,000 cubic kilometres, about 25 mm spread over the globe",
                },
                {"kind": "header", "value": "Annual fluxes"},
                {
                    "kind": "row",
                    "label": "Ocean evaporation",
                    "value": "About 413,000 cubic kilometres",
                },
                {
                    "kind": "row",
                    "label": "Precipitation on land",
                    "value": "About 113,000 cubic kilometres",
                },
                {
                    "kind": "row",
                    "label": "Runoff to the sea",
                    "value": "About 40,000 cubic kilometres",
                },
                {"kind": "header", "value": "Residence times"},
                {"kind": "row", "label": "Atmosphere", "value": "About nine days"},
                {"kind": "row", "label": "Rivers and soil", "value": "Weeks to months"},
                {"kind": "row", "label": "Ocean", "value": "Of the order of 3,000 years"},
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/9/94/Water_cycle.png",
            "alt": "Labelled diagram of the water cycle showing evaporation, condensation, precipitation and runoff",
            "caption": "A schematic of the water cycle published by the United States Geological Survey",
            "credit": "United States Geological Survey",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Water_cycle.png",
        },
        "references": [
            {
                "key": "usgscycle",
                "title": "The Water Cycle",
                "url": "https://www.usgs.gov/special-topics/water-science-school/science/water-cycle",
                "authors": "",
                "publisher": "Water Science School, United States Geological Survey",
                "published_on": "n.d.",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "usgswater",
                "title": "Where is Earth's Water?",
                "url": "https://www.usgs.gov/special-topics/water-science-school/science/where-earths-water",
                "authors": "",
                "publisher": "Water Science School, United States Geological Survey",
                "published_on": "n.d.",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "trenberth2007",
                "title": (
                    "Estimates of the Global Water Budget and Its Annual Cycle Using "
                    "Observational and Model Data"
                ),
                "url": "",
                "authors": "Kevin E. Trenberth, Lesley Smith, Taotao Qian, Aiguo Dai and John Fasullo",
                "publisher": "Journal of Hydrometeorology 8, 758–769",
                "published_on": "2007",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "ipcc",
                "title": "Water Cycle Changes",
                "url": "https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-8/",
                "authors": "Hervé Douville, Krishnan Raghavan and others",
                "publisher": (
                    "Chapter 8 of Climate Change 2021: The Physical Science Basis, "
                    "Intergovernmental Panel on Climate Change"
                ),
                "published_on": "2021",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "perrault1674",
                "title": "De l'origine des fontaines",
                "url": "",
                "authors": "Pierre Perrault",
                "publisher": "",
                "published_on": "1674",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasagpm",
                "title": "Global Precipitation Measurement mission",
                "url": "https://gpm.nasa.gov/",
                "authors": "",
                "publisher": "National Aeronautics and Space Administration",
                "published_on": "n.d.",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Water",
            "Ice age",
            "The carbon cycle",
            "The Nile",
            "The Sahara",
            "The Amazon rainforest",
        ],
        "aliases": [
            "Hydrologic cycle",
        ],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": [
            "hydrology",
            "evaporation",
            "precipitation",
            "groundwater",
            "climate",
        ],
    },
]
