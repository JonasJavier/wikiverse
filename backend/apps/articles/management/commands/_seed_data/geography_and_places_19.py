"""Geography and Places — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Mount Everest",
        "category": "Geography and Places",
        "categories": ["Earth and Environment"],
        "short_description": "The highest point on Earth, 8,848.86 metres above sea level",
        "summary": (
            "Mount Everest reaches 8,848.86 metres on the Nepal-China border in the "
            "Himalayas. Built by continental collision, its summit is marine limestone, "
            "and the air there holds about a third of the pressure available at sea level."
        ),
        "content": """**Mount Everest** is the highest mountain on Earth measured from
sea level, reaching 8,848.86 metres (29,032 feet) at a point on the frontier
between Nepal and the Tibet
Autonomous Region of China. It stands in the Mahalangur section of the Great Himalayas at
the head of Nepal's Khumbu valley, flanked by Lhotse and Nuptse to the south and falling
away eastward into the Kangshung face. In Nepali the mountain is Sagarmatha; in Tibetan it
is Chomolungma, transcribed Qomolangma in Chinese usage.[^britannica]

## Setting and names

The Great Trigonometrical Survey of India catalogued the peak as Peak XV. In 1856 Andrew
Waugh, then Surveyor General, proposed naming it for his predecessor George Everest, and
the Royal Geographical Society adopted the name in 1865. Everest objected: he had never
seen the mountain, and a name that local people could neither pronounce nor write cut
against the survey's own practice of recording indigenous names.[^keay] Nepal was closed to
foreign surveyors at the time, which is one reason the survey worked from the Indian plains
and why the Nepali and Tibetan names took more than a century to enter general English use.

## Geology

The mountain is a product of continental collision. India drifted north across the Tethys
Ocean and met Asia in a collision that began roughly 50 million years ago and has been
stacking and thrusting sheets of crust ever since. The summit pyramid is Ordovician
limestone, the Qomolangma Formation, laid down as carbonate mud on the Tethyan seafloor and
still carrying fragments of crinoids and other marine animals. A low-angle fault, the
Qomolangma Detachment, separates it from the older rocks beneath, whose uppermost member is
the conspicuous pale Yellow Band of metamorphosed limestone that climbers cross high on
both main routes.[^searle] The [[Plate tectonics|plate motions]] responsible have not
stopped: satellite geodesy shows the range creeping northeast by a few centimetres a year
while rising by a few millimetres.

## Measuring the height

Because the approaches were shut, Peak XV was fixed entirely by theodolite sightings taken
from six stations on the plains of Bihar in 1849 and 1850, at distances of up to about 240
kilometres. Radhanath Sikdar, the survey's chief computer, is generally credited with
reducing the observations in 1852 and concluding that Peak XV was the highest yet measured.
The result came out at almost exactly 29,000 feet, and Waugh published 29,002 feet in 1856
so that the figure would not read as a round guess.[^keay] The hard corrections were for
atmospheric refraction and for the deflection of the plumb line by the mass of the range
itself. As with the longitude problem that the [[Marine chronometer|marine chronometer]]
settled at sea, the difficulty lay less in the measurement than in the reference frame: a
height above sea level taken a thousand kilometres inland depends on a model of where sea
level would lie beneath the rock, which is the same class of choice that governs
[[Cartography|projection and datum]] in map-making. A Survey of India campaign of 1952-54
produced 8,848 metres, the value most atlases carried for half a century. Nepalese
surveyors reached the summit with [[Global Positioning System|satellite positioning]]
receivers in May 2019 and a Chinese team repeated the exercise in May 2020; on 8 December
2020 the two governments announced the agreed figure of 8,848.86 metres, snow cap
included.[^britannica]

## Atmosphere and the death zone

Barometers carried to the summit by the 1981 American Medical Research Expedition recorded
a mean pressure of about 253 torr, near 337 hectopascals — roughly a third of the
sea-level value, and higher than the standard atmosphere predicts for that altitude
because the tropical tropopause bulges upward.[^west] The partial pressure of oxygen in
inspired air is correspondingly low, and the summit lies very close to the ceiling an
acclimatised human can reach breathing ambient air at all. Reinhold Messner and Peter
Habeler first did so in May 1978. Above roughly 8,000 metres, the belt climbers call the
death zone, acclimatisation no longer offsets deterioration and time spent is paid for in
tissue damage. The jet stream crosses the summit for much of the year, so almost all
ascents fall in short windows before and after the monsoon, chiefly in May.

## Exploration and ascent

British reconnaissance from the Tibetan side began in 1921. On 8 June 1924 George Mallory
and Andrew Irvine disappeared high on the northeast ridge, leaving an argument about how
far they reached that has never been settled. The first confirmed ascent was made on 29 May
1953 by Edmund Hillary and Tenzing Norgay, by the South Col and southeast ridge, on a
British expedition led by John Hunt; a Chinese party summited from the north in May 1960.
Commercial guiding on the standard routes expanded sharply from the 1990s. The Himalayan
Database, the standard register of Nepalese Himalayan climbing, logged more than 800
summits in the 2024 season alone.[^himdb]

## Sherpa labour and risk

The Sherpa, a Tibetan-speaking people of Solukhumbu, supply most of the high-altitude
workforce: fixing rope and ladders through the shifting Khumbu Icefall, carrying loads,
stocking camps and increasingly guiding clients. The exposure is not shared evenly, because
the dangerous ground is crossed many more times by the people who prepare it than by those
who use it once. The first deaths on the mountain were seven porters killed by an avalanche
on the 1922 expedition. On 18 April 2014 a block of ice fell into the icefall and killed
sixteen Nepali workers, then the deadliest single day on Everest. Just over a year later,
on 25 April 2015, the magnitude 7.8 Gorkha [[Earthquake|earthquake]] shook an avalanche off
neighbouring Pumori into Base Camp, killing at least 19 people.[^gorkha] Climbing from
Nepal was abandoned in both seasons.

## The mountain today

Everest is now among the most closely monitored mountains anywhere, and among the most
heavily used. The Khumbu Glacier draining its southern cirque has thinned and is
increasingly pitted with meltwater ponds, part of a Himalaya-wide retreat from the extents
the ranges held during the last [[Ice age|glaciation]]. Congestion on the fixed ropes near
the summit on good days, abandoned equipment and human waste at the high camps, and the
permit revenue on which Nepal's mountaineering economy depends are all recurring subjects
of regulation.[^britannica]
""",
        "tier": "standard",
        "kind": "place",
        "infobox": {
            "title": "Mount Everest",
            "subtitle": "Sagarmatha; Chomolungma",
            "rows": [
                {
                    "kind": "header",
                    "value": "Geography",
                },
                {
                    "kind": "row",
                    "label": "Elevation",
                    "value": "8,848.86 m (29,032 ft)",
                },
                {
                    "kind": "row",
                    "label": "Range",
                    "value": "Mahalangur Himal, Great Himalayas",
                },
                {
                    "kind": "row",
                    "label": "Location",
                    "value": "Nepal and Tibet Autonomous Region of China",
                },
                {
                    "kind": "row",
                    "label": "Prominence",
                    "value": "8,848.86 m — the highest point on Earth",
                },
                {
                    "kind": "header",
                    "value": "Geology",
                },
                {
                    "kind": "row",
                    "label": "Summit rock",
                    "value": "Ordovician limestone, Qomolangma Formation",
                },
                {
                    "kind": "row",
                    "label": "Origin",
                    "value": "India-Asia continental collision, from about 50 Ma",
                },
                {
                    "kind": "header",
                    "value": "Climbing",
                },
                {
                    "kind": "row",
                    "label": "First ascent",
                    "value": "29 May 1953, Edmund Hillary and Tenzing Norgay",
                },
                {
                    "kind": "row",
                    "label": "Standard routes",
                    "value": "South Col from Nepal; northeast ridge from Tibet",
                },
                {
                    "kind": "full",
                    "value": (
                        "Summit air pressure averages about 253 torr, near a third of the "
                        "sea-level value."
                    ),
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "britannica",
                "title": "Mount Everest",
                "url": "https://www.britannica.com/place/Mount-Everest",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "keay",
                "title": (
                    "The Great Arc: The Dramatic Tale of How India Was Mapped and Everest Was Named"
                ),
                "url": "https://archive.org/details/dli.pahar.3721",
                "authors": "John Keay",
                "publisher": "HarperCollins",
                "published_on": "2000",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-00-653123-4",
                "quote": "",
            },
            {
                "key": "searle",
                "title": (
                    "Colliding Continents: A Geological Exploration of the Himalaya, "
                    "Karakoram, and Tibet"
                ),
                "url": (
                    "https://global.oup.com/academic/product/colliding-continents-9780199653003"
                ),
                "authors": "Mike Searle",
                "publisher": "Oxford University Press",
                "published_on": "2013",
                "accessed_on": "2026-09-26",
                "identifier": "ISBN 978-0-19-965300-3",
                "quote": "",
            },
            {
                "key": "west",
                "title": (
                    "Barometric pressures at extreme altitudes on Mt. Everest: "
                    "physiological significance"
                ),
                "url": "https://journals.physiology.org/doi/abs/10.1152/jappl.1983.54.5.1188",
                "authors": (
                    "John B. West, Sukhamay Lahiri, Karl H. Maret, Richard M. Peters, "
                    "Christopher J. Pizzo"
                ),
                "publisher": "Journal of Applied Physiology",
                "published_on": "1983",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1152/jappl.1983.54.5.1188",
                "quote": "",
            },
            {
                "key": "himdb",
                "title": "The Himalayan Database",
                "url": "https://www.himalayandatabase.com/",
                "authors": "",
                "publisher": "The Himalayan Database",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "gorkha",
                "title": "Nepal earthquake of 2015",
                "url": "https://www.britannica.com/topic/Nepal-earthquake-of-2015",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Plate tectonics",
            "Earthquake",
            "Cartography",
            "Global Positioning System",
            "Ice age",
        ],
        "aliases": ["Everest"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["himalayas", "mountaineering", "geodesy", "plate tectonics"],
    },
    {
        "title": "The Nile",
        "category": "Geography and Places",
        "categories": ["Earth and Environment", "History"],
        "short_description": "The north-flowing river of northeast Africa and the spine of Egypt",
        "summary": (
            "The Nile drains close to three million square kilometres of northeast Africa "
            "and flows north to the Mediterranean. Its White and Blue branches meet at "
            "Khartoum, and an annual flood sustained Egypt until the Aswan High Dam."
        ),
        "content": """**The Nile** is the principal river of northeast Africa, running
north from the equatorial lakes and the Ethiopian highlands to a delta on the
Mediterranean. Its basin covers close
to three million square kilometres across eleven countries, and for most of its lower
course it crosses desert that contributes nothing to its flow.[^nile]

## Course

The river has two great branches. The White Nile leaves Lake Victoria at Ripon Falls —
submerged since the 1950s behind the Owen Falls dam — and runs on through Lake Kyoga and
Lake Albert; traced further upstream it reaches the Kagera system in the highlands of
Rwanda and Burundi. The Blue Nile, the Abay, flows out of Lake Tana in the Ethiopian
highlands, whose chief feeder rises at the spring of Gish Abay. The two meet at Khartoum.
The Atbara, the last tributary of any size, joins about 300 kilometres downstream, and for
the remaining two and a half thousand kilometres to the sea no perennial water enters the
channel at all. Six cataracts, bars of harder basement rock numbered upstream from Aswan,
break the Sudanese and southern Egyptian reaches and long restricted navigation. Below
Cairo the river splits into the Rosetta and Damietta branches across a delta fronting some
240 kilometres of coastline; ancient geographers counted as many as seven mouths.[^nile]

The Nile's length is usually given as about 6,650 kilometres, which makes it the longest or
second-longest river in the world depending on how the Amazon is traced. The number is not
a fixed quantity: it depends on which headstream is treated as the source and how closely
the channel is followed, and satellite-based remeasurements have produced longer values.

## Two rivers

The branches behave differently, and the difference shaped Egyptian life. The White Nile
arrives steady, its flow buffered first by Lake Victoria and then by the Sudd, an immense
papyrus and sedge wetland in South Sudan where roughly half the water is lost to
evaporation and transpiration before the river emerges. The Blue Nile is violently
seasonal, fed by the summer monsoon over the Ethiopian highlands, and it carries most of
the sediment. Measured at Aswan, a little over half the annual flow comes down the Blue
Nile, about a third down the White Nile and the remainder from the Atbara; at the height of
the flood the Ethiopian tributaries supply the overwhelming majority.[^nile] The river is a
compact demonstration of how [[The water cycle|the water cycle]] couples distant places:
rain falling on Ethiopia in July reaches Egypt weeks later, having crossed a large part of
[[The Sahara]] without gaining a drop.

## The flood

Before the twentieth century the Nile at Aswan began to rise in late June, peaked in
September and fell through the winter, spreading water and fine silt across the floodplain.
[[Ancient Egypt|Egyptian]] administration was built on that rhythm. The civil calendar had
three seasons — akhet, the inundation; peret, the emergence of the fields; and shemu, the
harvest and low water — of four thirty-day months each, plus five additional days.
Officials read the height of the rise on nilometers, graduated wells and stairways at
Elephantine, at Roda Island in Cairo and elsewhere, because the height forecast the harvest
and therefore the tax assessment; the Roda structure standing today dates in its present
form from 861. A low flood meant shortage, and a very high one destroyed embankments and
villages.[^nile] Silt was the other gift: a fresh layer each year renewed soil fertility
without manuring, which is one reason the valley supported dense population for three
millennia. The same landscape supplied natron, a naturally occurring soda [[Salt|salt]]
gathered from lake beds west of the delta, which Egyptian embalmers used to dry bodies.

## Searching for the source

Classical geographers knew the lower river intimately and its head not at all. Ptolemy
placed the origin in snowy "Mountains of the Moon", later identified with the Rwenzori
range. The roughly north-south alignment of Alexandria and Syene, near modern Aswan, gave
Eratosthenes at [[The Library of Alexandria|the Mouseion]] the baseline for his estimate of
the Earth's circumference. The modern search was an exercise in competitive
[[Cartography|mapping]]. John Hanning Speke, travelling with Richard Burton, struck north
alone and reached the great lake on 30 July 1858, naming it for Queen Victoria; he returned
in 1862 and on 28 July identified its outlet, which he called Ripon Falls. Burton rejected
the claim, and Speke was killed by his own gun in September 1864, the day before the two
were to debate the question in public. Henry Morton Stanley's circumnavigation of the lake
in 1875 effectively settled it.[^speke]

## Damming the river

Perennial irrigation had been extended through the nineteenth century by barrages and
canals, and the Aswan Low Dam, completed in 1902 and twice raised, stored part of the
flood. The Aswan High Dam, built between 1960 and 1970 a few kilometres upstream, ended the
flood outright. Its reservoir, Lake Nasser, holds on the order of 130 cubic kilometres,
more than a year's flow, which converts a wildly variable river into a managed supply,
allows several crops a year and generates hydroelectricity. The costs were equally
concrete: Lower Nubia was drowned, tens of thousands of people were resettled, and
monuments including the temples at Abu Simbel were cut apart and rebuilt on higher
ground.[^aswan]

## The delta now

The reservoir also traps the silt. On the order of a hundred million tonnes a year now
settles behind the dam instead of reaching the fields and the coast, so Egyptian farming
depends on manufactured fertiliser, and the delta shoreline, no longer resupplied, is
eroding — locally by tens of metres a year — while subsidence and seawater intrusion
compound the loss. The promontories at the Rosetta and Damietta mouths have retreated
markedly since 1970.[^aswan]
""",
        "tier": "standard",
        "kind": "place",
        "infobox": {
            "title": "The Nile",
            "subtitle": "River of northeast Africa",
            "rows": [
                {
                    "kind": "header",
                    "value": "Course",
                },
                {
                    "kind": "row",
                    "label": "Length",
                    "value": "About 6,650 km; estimates vary with method",
                },
                {
                    "kind": "row",
                    "label": "Branches",
                    "value": "White Nile from Lake Victoria; Blue Nile from Lake Tana",
                },
                {
                    "kind": "row",
                    "label": "Confluence",
                    "value": "Khartoum, Sudan",
                },
                {
                    "kind": "row",
                    "label": "Mouth",
                    "value": "Mediterranean Sea, by the Rosetta and Damietta branches",
                },
                {
                    "kind": "header",
                    "value": "Basin",
                },
                {
                    "kind": "row",
                    "label": "Drainage area",
                    "value": "Close to 3 million km2",
                },
                {
                    "kind": "row",
                    "label": "Basin states",
                    "value": "Eleven",
                },
                {
                    "kind": "row",
                    "label": "Discharge at Aswan",
                    "value": "About 2,800 cubic metres per second",
                },
                {
                    "kind": "header",
                    "value": "Regulation",
                },
                {
                    "kind": "row",
                    "label": "Aswan Low Dam",
                    "value": "Completed 1902, raised twice",
                },
                {
                    "kind": "row",
                    "label": "Aswan High Dam",
                    "value": "Built 1960-1970; reservoir Lake Nasser",
                },
                {
                    "kind": "full",
                    "value": (
                        "The annual flood ended in 1970; the silt it carried now settles "
                        "in Lake Nasser."
                    ),
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "nile",
                "title": "Nile River",
                "url": "https://www.britannica.com/place/Nile-River",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "aswan",
                "title": "Nile River: Dams and reservoirs",
                "url": "https://www.britannica.com/place/Nile-River/Dams-and-reservoirs",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "speke",
                "title": "John Hanning Speke",
                "url": "https://www.britannica.com/biography/John-Hanning-Speke",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Ancient Egypt",
            "The Sahara",
            "The water cycle",
            "Cartography",
            "Salt",
        ],
        "aliases": ["Nile River"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["rivers", "hydrology", "egypt", "dams"],
    },
    {
        "title": "The Sahara",
        "category": "Geography and Places",
        "categories": ["Earth and Environment", "History"],
        "short_description": "The world's largest hot desert, about nine million square kilometres",
        "summary": (
            "The Sahara spans North Africa from the Atlantic to the Red Sea, covering "
            "roughly nine million square kilometres. Sand seas make up about a quarter of "
            "it, it was green savanna 6,000 years ago, and its dust fertilises the Amazon."
        ),
        "content": """**The Sahara** is the largest hot desert on Earth, a belt of arid
land stretching across northern Africa from the Atlantic coast to the Red Sea
and from the Mediterranean and the
Atlas ranges south to the semi-arid Sahel. Published areas range from about 8.6 to 9.2
million square kilometres depending on where the southern boundary is drawn, which places
it on the same scale as China or the United States. The name comes from the Arabic
sahra, meaning desert.[^britannica]

## Extent and surfaces

Dunes are the popular image and the minority case. Sand seas, or ergs — among them the
Grand Erg Oriental, the Grand Erg Occidental and the Libyan Sand Sea — cover perhaps a
quarter of the surface. The rest is hamada, bare rock plateau scoured clean of fines; reg,
gravel plains armoured with a pavement of coarse stones; dry valleys, or wadis, cut when
the climate was wetter; salt flats; and mountain massifs that rise high enough to be cool
and comparatively damp. The Ahaggar in Algeria and the Tibesti in Chad are volcanic
uplands, and the Tibesti carries the desert's high point at Emi Koussi, 3,415 metres. Its
lowest point is the Qattara Depression in Egypt, 133 metres below sea level.[^britannica]
Temperatures are extreme but not unbounded: the World Meteorological Organization struck
out the celebrated 58 °C reading from El Azizia in Libya, dated 13 September 1922, after a
2012 review found the instrument, the observer and the site all unreliable.[^wmo]

## Why it is dry

The Sahara sits under the descending branch of the Hadley circulation, where air that rose
over the tropics returns to the surface warming and drying as it sinks. That subsiding air
suppresses cloud formation and holds a belt of high pressure across the subtropics on both
sides of the equator, which is why the world's great deserts line up near 25 degrees of
latitude. Much of the central Sahara receives less than 25 millimetres of rain a year, and
some stations go several years without a measurable fall. What rain there is arrives from
the north in winter along the Mediterranean margin and from the West African monsoon in
summer along the southern edge, so the desert's own contribution to [[The water cycle|the
water cycle]] is mostly evaporation and dust.

## The green Sahara

The present desert is recent. Through the early Holocene, and during comparable intervals
earlier in the [[Ice age|Quaternary]], the Sahara held lakes, rivers, grassland and
woodland. This African Humid Period ran from roughly 11,000 to 5,000 years ago and was
paced by precession, the slow wobble of Earth's axis that shifts the seasonal distribution
of sunlight; stronger northern summer insolation drove the West African monsoon much
further north. Marine sediment cores off Mauritania show that both the onset and the end
were abrupt, taking centuries rather than millennia, which points to vegetation and ocean
feedbacks amplifying a gradual orbital push.[^demenocal] Lake Mega-Chad, the ancestor of
Lake Chad, may have been among the largest lakes on the planet.

The evidence is also painted on the rock. Tassili n'Ajjer in southeastern Algeria holds
more than 15,000 drawings and engravings spanning roughly 6000 BCE to the early centuries
CE, recording elephants, giraffes, hippopotamuses and cattle herding in a landscape that
now supports almost nothing.[^unesco] Similar galleries survive in the Messak in Libya and
the Gilf Kebir on the Egyptian-Libyan frontier. Drying populations concentrated along
permanent water, a movement that is part of the background to the rise of
[[Ancient Egypt|Egyptian]] civilisation along [[The Nile]].

## Water in the desert

Much of that vanished rainfall is still underground. The Nubian Sandstone Aquifer System,
spread beneath more than two million square kilometres of Egypt, Libya, Sudan and Chad,
holds on the order of 150,000 cubic kilometres of fossil water recharged mainly during
humid phases, and it is not meaningfully replenished today.[^nasa] Where the water table
meets the surface, or where wells reach it, oases such as Siwa, Kufra, Ghadames and the
Tuat form; they sustained date cultivation and, more importantly, made crossing possible.

## Crossing it

The desert was a barrier and a corridor at once. Camel caravans, from about the first
centuries CE, linked the Mediterranean and the Sahel on routes as demanding as the Central
Asian legs of [[The Silk Road]]. Northbound the trade carried gold, ivory, enslaved people
and later manuscripts; southbound it carried [[Salt]], quarried in slabs at desert mines
such as Taghaza and, after Taghaza was abandoned near the end of the sixteenth century, at
Taoudenni. Salt was scarce in the savanna and gold was scarce in the Mediterranean world,
and the exchange of the two built the Saharan trading cities, [[Timbuktu]] among them.
Azalai caravans still run the Taoudenni route.

## Dust and the Atlantic

The Sahara is the largest single source of mineral dust in the atmosphere. Satellite lidar
measurements put the quantity leaving the western edge of the desert at roughly 182 million
tonnes a year, of which about 27.7 million tonnes settle over the Amazon basin after
crossing some 5,000 kilometres of ocean. Much of it originates in the Bodélé Depression in
Chad, the dried bed of a former arm of Lake Mega-Chad, whose diatom-rich sediments are rich
in phosphorus. The deposited dust delivers roughly 22,000 tonnes of phosphorus a year,
close to the amount that [[The Amazon rainforest]] loses through rainfall runoff and
flooding, so one desert's erosion partly underwrites another continent's forest.[^yu]
Saharan dust also darkens Caribbean skies, fertilises the Atlantic, and suppresses tropical
cyclone formation by drying and stabilising the air ahead of developing storms.
""",
        "tier": "standard",
        "kind": "place",
        "infobox": {
            "title": "The Sahara",
            "subtitle": "The largest hot desert on Earth",
            "rows": [
                {
                    "kind": "header",
                    "value": "Extent",
                },
                {
                    "kind": "row",
                    "label": "Area",
                    "value": "Roughly 9 million km2; published figures 8.6-9.2 million",
                },
                {
                    "kind": "row",
                    "label": "Span",
                    "value": "Atlantic to the Red Sea, across eleven countries and territories",
                },
                {
                    "kind": "row",
                    "label": "Highest point",
                    "value": "Emi Koussi, 3,415 m, Tibesti Mountains, Chad",
                },
                {
                    "kind": "row",
                    "label": "Lowest point",
                    "value": "Qattara Depression, 133 m below sea level, Egypt",
                },
                {
                    "kind": "header",
                    "value": "Surfaces",
                },
                {
                    "kind": "row",
                    "label": "Sand seas",
                    "value": "About a quarter of the area, as ergs",
                },
                {
                    "kind": "row",
                    "label": "Other terrain",
                    "value": "Hamada plateaus, reg gravel plains, wadis, massifs, oases",
                },
                {
                    "kind": "header",
                    "value": "Climate history",
                },
                {
                    "kind": "row",
                    "label": "African Humid Period",
                    "value": "Roughly 11,000 to 5,000 years ago",
                },
                {
                    "kind": "row",
                    "label": "Driver",
                    "value": "Precession-paced strengthening of the West African monsoon",
                },
                {
                    "kind": "full",
                    "value": (
                        "Dust from the Bodele Depression in Chad supplies phosphorus to "
                        "the Amazon basin."
                    ),
                },
            ],
        },
        "image": None,
        "references": [
            {
                "key": "britannica",
                "title": "Sahara",
                "url": "https://www.britannica.com/place/Sahara-desert-Africa",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "wmo",
                "title": (
                    "World Meteorological Organization Assessment of the Purported World "
                    "Record 58 C Temperature Extreme at El Azizia, Libya (13 September 1922)"
                ),
                "url": (
                    "https://journals.ametsoc.org/view/journals/bams/94/2/bams-d-12-00093.1.xml"
                ),
                "authors": "Khalid I. El Fadli and others",
                "publisher": "Bulletin of the American Meteorological Society",
                "published_on": "2013",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1175/BAMS-D-12-00093.1",
                "quote": "",
            },
            {
                "key": "demenocal",
                "title": (
                    "Abrupt onset and termination of the African Humid Period: rapid "
                    "climate responses to gradual insolation forcing"
                ),
                "url": "https://www.sciencedirect.com/science/article/pii/S0277379199000815",
                "authors": "Peter deMenocal and others",
                "publisher": "Quaternary Science Reviews",
                "published_on": "2000",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1016/S0277-3791(99)00081-5",
                "quote": "",
            },
            {
                "key": "unesco",
                "title": "Tassili n'Ajjer",
                "url": "https://whc.unesco.org/en/list/179",
                "authors": "",
                "publisher": "UNESCO World Heritage Centre",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nasa",
                "title": "Nubian Sandstone Aquifer, Egypt",
                "url": "https://science.nasa.gov/photojournal/nubian-sandstone-aquifer-egypt/",
                "authors": "",
                "publisher": "NASA",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "yu",
                "title": (
                    "The fertilizing role of African dust in the Amazon rainforest: a "
                    "first multiyear assessment based on data from CALIPSO"
                ),
                "url": "https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2015GL063040",
                "authors": "Hongbin Yu and others",
                "publisher": "Geophysical Research Letters",
                "published_on": "2015",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.1002/2015GL063040",
                "quote": "",
            },
        ],
        "see_also": [
            "The Nile",
            "Timbuktu",
            "The water cycle",
            "Ice age",
            "The Amazon rainforest",
            "Salt",
        ],
        "aliases": ["Sahara Desert"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["deserts", "palaeoclimate", "north africa", "mineral dust"],
    },
]
