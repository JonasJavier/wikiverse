"""Medicine and the Mind — Wikiverse seed corpus.

Part of the CC BY 4.0 licensed article corpus. See __init__.py.
"""

ARTICLES = [
    {
        "title": "Vaccination",
        "category": "Medicine and the Mind",
        "categories": ["Life Sciences", "History"],
        "short_description": "Deliberate priming of the immune system against a later infection",
        "summary": (
            "Vaccination exposes the immune system to a harmless form or fragment of a "
            "pathogen so that a later encounter meets an existing defence. Grown out of "
            "eighteenth-century variolation, it produced the only deliberate eradication "
            "of a human disease."
        ),
        "content": """**Vaccination** is the deliberate administration of a harmless
preparation derived from a pathogen — a weakened or killed organism, one of its molecules, or
instructions for making one — in order to provoke an immune response that protects against a
later natural infection. The word descends from the Latin *vacca*, cow, after the cowpox
material Edward Jenner used against smallpox in 1796.[^jenner1798] Vaccination is the only medical intervention
to have driven a human disease to extinction, and the biological property it exploits,
immunological memory, is the same one that makes most infections a once-in-a-lifetime event.

## Variolation

Smallpox in its severe form, *variola major*, killed roughly three in ten of those it infected
and left many survivors scarred or blind; unlike [[The Black Death|plague]], which arrived
in waves, it was a constant presence in cities. Long before European physicians took an
interest,
practitioners in China, India, west Asia and parts of Africa used variolation: material from a
smallpox pustule was scratched into the skin, or powdered scabs were blown into the nose. The
result was usually a mild case followed by lasting protection.[^cdc_smallpox]

Two episodes in 1721 brought the practice into the English-language record. In London, Lady
Mary Wortley Montagu, who had watched inoculation in Constantinople, had her daughter
variolated. In Boston, during an epidemic, Cotton Mather pressed the case after learning of the
procedure from Onesimus, an enslaved West African man in his household, and the physician
Zabdiel Boylston inoculated some 240 people. Six died, about one in forty, against roughly one
in seven of the 5,700-odd Bostonians who caught smallpox in the ordinary way.[^boylston] The
arithmetic favoured inoculation, but the procedure gave the patient genuine smallpox, which
could kill and could seed an outbreak — an objection no tally of survivors answered.

## Jenner and cowpox

Dairy workers who had caught cowpox, a mild disease of cattle that raises pustules on the
hands, were locally reputed to be safe from smallpox. On 14 May 1796 Edward Jenner, a physician
at Berkeley in Gloucestershire, took matter from a cowpox lesion on the hand of a dairymaid,
Sarah Nelmes, and introduced it into the arm of an eight-year-old boy, James Phipps. In July he
challenged Phipps with smallpox material and no disease followed. Jenner's *Inquiry into the
Causes and Effects of the Variolae Vaccinae* of 1798 set out his case histories and argued that
cowpox conferred protection without the danger of variolation.[^jenner1798] He was not the
first to try — the Dorset farmer Benjamin Jesty had inoculated his family with cowpox in 1774 —
but Jenner published and distributed material, and within a decade vaccination had spread
across Europe and the Americas.

## Attenuation and a general method

Cowpox was a fortunate accident: a mild relative of a lethal disease. Louis Pasteur turned the
accident into a procedure. Cultures of chicken cholera left on the bench through the summer of
1879 had lost their virulence yet still protected birds against fresh cultures. Pasteur called
the process attenuation and, in Jenner's honour, extended the word *vaccine* to any such
preparation. A public trial of an anthrax vaccine on sheep at Pouilly-le-Fort followed in 1881,
and in July 1885 he treated Joseph Meister, a boy bitten by a rabid dog, with injections of
dried spinal cord from infected rabbits.[^pasteur] Attenuation arrived alongside
[[Germ theory of disease|germ theory]], which explained why any of it worked and which later
directed the search for drugs such as [[Penicillin|penicillin]] that attack bacteria directly.

## Immunological memory

A first encounter with an antigen provokes a slow response: one to two weeks pass while
lymphocytes able to recognise it multiply and mature. Some of their descendants persist as
memory B and T [[The cell|cells]] in the lymph nodes, spleen and bone marrow, organs whose
immune role was unknown to the [[Human anatomy|anatomists]] who first described them, and a
second encounter is met within days by antibodies of higher affinity. Vaccination stages that
first encounter under controlled conditions. Durability varies: measles and yellow fever
vaccines protect for decades, tetanus toxoid is boosted every ten years, and influenza
vaccines are reformulated because the virus's surface proteins change under
[[Natural selection|selection]] faster than the [[Memory|memory]] laid down against them
stays useful. Adjuvants — aluminium salts have been
used since the 1920s — raise the response to antigens that are too inert on their own.

## Classes of vaccine

Live attenuated vaccines — measles, oral polio, BCG, yellow fever — use weakened organisms
that replicate briefly and provoke a durable response. Inactivated vaccines, such as injected
polio, use killed organisms, and toxoid vaccines against tetanus and diphtheria use
inactivated toxins rather than the bacteria themselves. Subunit vaccines use a purified
protein or polysaccharide; conjugate vaccines against *Haemophilus influenzae* type b link a
bacterial sugar coat to a carrier protein so that infants respond to it. Viral-vector and
nucleic-acid vaccines supply the gene for one antigen and leave the recipient's cells to make
it.

## The eradication of smallpox

The World Health Organization adopted smallpox eradication as a goal in 1959, but the programme
was underfunded and made slow progress; an Intensified Smallpox Eradication Programme began in
1967, when the disease still killed more than two million people a year.[^who_smallpox] Three
things made the second attempt work: a freeze-dried vaccine that survived tropical transport; a
bifurcated needle, patented in 1965, which held about two microlitres of vaccine between its
tines, needed far less vaccine than earlier instruments and could be boiled and
reused[^si_needle]; and a shift from blanket campaigns to surveillance and containment, in
which each reported case triggered vaccination of the ring of contacts around it. Transmission
ended in South America in 1971, Asia in 1975 and Africa in 1977. The last person infected
naturally with *variola major* was Rahima Banu, a three-year-old in Bangladesh, in 1975; the
last natural case of any kind was Ali Maow Maalin, a hospital cook in Merca, Somalia, who fell
ill in October 1977.[^cdc_smallpox] The World Health Assembly declared the disease eradicated
on 8 May 1980. Rinderpest, a cattle disease, was declared eradicated in 2011; among human
diseases only smallpox has gone, though wild poliovirus types 2 and 3 have been certified
extinct.

## Coverage and reception

Because vaccination interrupts transmission rather than merely protecting the recipient,
sufficient coverage shields those who are not vaccinated; the threshold rises with
transmissibility, and measles, among the most contagious diseases known, requires roughly 95
per cent coverage to stop circulating. Opposition is as old as the practice: Boston mobs
threatened Boylston in 1721, and compulsory vaccination in Victorian Britain produced an
organised anti-vaccination movement. A paper of 1998 proposing a link between the
measles-mumps-rubella vaccine and autism was retracted by *The Lancet* in 2010, and later
studies of millions of children found no such association.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Vaccination",
            "subtitle": "Medical procedure",
            "rows": [
                {
                    "kind": "row",
                    "label": "Purpose",
                    "value": "Induce protective immunity without natural infection",
                },
                {
                    "kind": "row",
                    "label": "Mechanism",
                    "value": "Immunological memory in B and T lymphocytes",
                },
                {"kind": "header", "value": "Chronology"},
                {
                    "kind": "row",
                    "label": "Variolation recorded in Europe",
                    "value": "1721, London and Boston",
                },
                {
                    "kind": "row",
                    "label": "First cowpox vaccination",
                    "value": "14 May 1796, by Edward Jenner",
                },
                {
                    "kind": "row",
                    "label": "Attenuated cultures",
                    "value": "1879-1885, by Louis Pasteur",
                },
                {
                    "kind": "row",
                    "label": "Smallpox eradication declared",
                    "value": "8 May 1980",
                },
                {"kind": "header", "value": "Main classes"},
                {
                    "kind": "row",
                    "label": "Live attenuated",
                    "value": "Measles, oral polio, BCG, yellow fever",
                },
                {
                    "kind": "row",
                    "label": "Inactivated",
                    "value": "Injected polio, hepatitis A, rabies",
                },
                {"kind": "row", "label": "Toxoid", "value": "Tetanus, diphtheria"},
                {
                    "kind": "row",
                    "label": "Subunit and conjugate",
                    "value": "Hepatitis B, *Haemophilus influenzae* type b",
                },
                {
                    "kind": "full",
                    "value": "Etymology: Latin *vacca*, cow, after the cowpox used in 1796",
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/d/d6/The_cow_pock.jpg",
            "alt": (
                "Coloured etching of a crowded vaccination room in which small cows sprout "
                "from the bodies of the newly vaccinated"
            ),
            "caption": (
                "James Gillray's etching of 1802, published six years after Jenner's first "
                "vaccination, showing cows erupting from vaccinated patients."
            ),
            "credit": "James Gillray",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:The_cow_pock.jpg",
        },
        "references": [
            {
                "key": "jenner1798",
                "title": (
                    "An Inquiry into the Causes and Effects of the Variolae Vaccinae, a "
                    "Disease Discovered in Some of the Western Counties of England"
                ),
                "url": "https://www.gutenberg.org/ebooks/29414",
                "authors": "Edward Jenner",
                "publisher": "Sampson Low, London",
                "published_on": "1798",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "cdc_smallpox",
                "title": "History of Smallpox",
                "url": "https://www.cdc.gov/smallpox/about/history.html",
                "authors": "",
                "publisher": "U.S. Centers for Disease Control and Prevention",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "who_smallpox",
                "title": "History of Smallpox Vaccination",
                "url": (
                    "https://www.who.int/news-room/spotlight/history-of-vaccination/"
                    "history-of-smallpox-vaccination"
                ),
                "authors": "",
                "publisher": "World Health Organization",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "boylston",
                "title": "Zabdiel Boylston",
                "url": "https://www.britannica.com/biography/Zabdiel-Boylston",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "pasteur",
                "title": "Louis Pasteur",
                "url": "https://www.britannica.com/biography/Louis-Pasteur",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "si_needle",
                "title": "Bifurcated Needles for Vaccination",
                "url": "https://www.si.edu/object/bifurcated-needles-vaccination:nmah_722803",
                "authors": "",
                "publisher": "Smithsonian National Museum of American History",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Germ theory of disease",
            "Penicillin",
            "The Black Death",
            "Natural selection",
            "Memory",
            "Human anatomy",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["immunisation", "smallpox", "immunology", "public health"],
    },
    {
        "title": "Penicillin",
        "category": "Medicine and the Mind",
        "categories": ["Chemistry and Materials", "Life Sciences"],
        "short_description": "First mass-produced antibiotic, obtained from a Penicillium mould",
        "summary": (
            "Penicillin is a family of beta-lactam antibiotics obtained from Penicillium "
            "moulds. Noticed by Alexander Fleming in 1928 and turned into a usable drug by "
            "an Oxford team from 1939, it was in mass production by 1944."
        ),
        "content": """**Penicillin** is a family of antibiotics built around a four-membered
beta-lactam ring, obtained from moulds of the genus *Penicillium*. It was the first
antibacterial drug that could be given systemically, in quantity, against a wide range of
infections without poisoning the patient, and its arrival in the early 1940s turned conditions
that routinely killed — bacterial meningitis, puerperal fever, wound sepsis, endocarditis —
into treatable illnesses.

## Fleming's plate

In September 1928 Alexander Fleming, a bacteriologist at St Mary's Hospital in Paddington,
London, returned to a stack of culture plates of *Staphylococcus* and found one contaminated by
a mould, with the bacterial colonies nearest the mould dissolved away. He identified the
organism as a *Penicillium* and named the diffusible substance it produced penicillin. His
paper of 1929 recorded that broth from the mould inhibited staphylococci, streptococci and
several other species at great dilution while leaving white blood cells unharmed, and proposed
using it to suppress Gram-positive bacteria when isolating others.[^fleming1929] Antagonism
between moulds and bacteria had been noticed before, by John Tyndall in the 1870s and in Ernest
Duchesne's thesis of 1897, but nobody had isolated an agent. Fleming could not either: the
active material was present in tiny amounts and lost activity quickly, and by the mid-1930s he
had largely set the problem aside.

## The Oxford work

In 1938 Howard Florey and Ernst Chain, at the Sir William Dunn School of Pathology in Oxford,
began a systematic survey of antibacterial substances made by microorganisms, and read
Fleming's paper as one entry in the literature. Norman Heatley devised the extraction that made
the project possible, shuttling penicillin between water and solvent at different acidities,
and a cylinder-plate assay that expressed potency in arbitrary Oxford units. On 25 May 1940 the
team infected eight mice with haemolytic streptococci and gave four of them penicillin; the
four treated mice survived and the untreated four died.[^gaynes2017] Their report appeared in
*The Lancet* that August.

Making enough for a human being was a different scale of problem. The school improvised culture
vessels, settling on ceramic pans, and a team of assistants kept them going. The first patient,
treated in February 1941, was an Oxford police constable with a spreading infection of the face;
he improved markedly, penicillin was recovered from his urine and given back to him, and when
the supply ran out the infection returned and killed him.[^acs_landmark]

## Mass production

With British industry occupied by the war, Florey and Heatley flew to the United States in the
summer of 1941 and were directed to the Northern Regional Research Laboratory at Peoria,
Illinois. Two changes there transformed the yield. Corn steep liquor, a by-product of starch
manufacture, proved a far better growth medium than anything Oxford had used; and a strain of
*Penicillium chrysogenum* recovered from a mouldy cantaloupe in a Peoria market produced several
times more penicillin than Fleming's mould, becoming, after further selection, the ancestor of
industrial strains. Surface culture in flasks gave way to deep-tank fermentation, in which
sterile air is bubbled through a stirred vessel thousands of gallons in volume.[^gaynes2017]

At the end of 1942 the entire American stock was enough for fewer than a hundred patients; by
September 1943 production met the demands of the Allied armed forces, and penicillin was
available in quantity for casualties of the Normandy landings in June 1944.[^sciencemuseum]
Fleming, Chain and Florey shared the 1945 Nobel Prize in Physiology or Medicine.[^nobel1945]

## Structure and mechanism

Every penicillin has the same bicyclic core: a strained four-membered beta-lactam ring fused to
a five-membered thiazolidine ring, with a variable side chain attached to the second. The
strain in the four-membered ring makes it chemically reactive, and that reactivity is the drug.
Bacteria enclose themselves in peptidoglycan, a mesh of sugar chains cross-linked by short
peptides; enzymes called transpeptidases make the cross-links. Penicillin resembles the end of
the peptide those enzymes act on, binds their active site and is not released, so a growing
cell cannot finish its wall and bursts under its own internal pressure. Animal
[[The cell|cells]] have no peptidoglycan and no transpeptidases, which is why a drug that
destroys bacteria leaves the patient almost untouched — the clearest case of the selective
toxicity that [[Germ theory of disease|germ theory]] had made it sensible to look for.
Gram-positive bacteria are the most susceptible; the outer membrane of Gram-negative species
restricts access.

## Resistance

Chain and Edward Abraham described a bacterial enzyme that destroyed penicillin in 1940, before
any patient had been treated. Such beta-lactamases hydrolyse the four-membered ring and render
the drug inert. Penicillin-resistant *Staphylococcus aureus* spread through hospitals within a
decade of the drug's introduction; methicillin, engineered to resist the enzyme, reached use in
1959, and methicillin-resistant strains were reported in Britain in 1961. Resistance is
[[Natural selection|natural selection]] observed on a human timescale, with one complication:
the relevant [[Deoxyribonucleic acid|DNA]] often sits on plasmids and transposons that pass
between strains and even between species, so a resistance gene need not arise afresh in each
lineage. The World Health Organization counts antimicrobial resistance among the largest
threats to global health.[^who_amr]

Chemists answered by modifying the core. Isolation of 6-aminopenicillanic acid in the late
1950s allowed side chains to be attached at will, producing acid-stable oral penicillins and
then ampicillin and amoxicillin, which reach many Gram-negative bacteria; pairing amoxicillin
with a beta-lactamase inhibitor restores activity against enzyme-producing strains. Beta-lactams
remain the most heavily used class of antibiotic, and some organisms, including
*Streptococcus pyogenes*, have never acquired resistance to penicillin itself. Unlike
[[Vaccination|vaccination]], which forestalls infection, penicillin treats it, and the two
strategies place quite different selective pressures on the organisms they target.
""",
        "tier": "standard",
        "kind": "concept",
        "infobox": {
            "title": "Penicillin",
            "subtitle": "Class of beta-lactam antibiotics",
            "rows": [
                {
                    "kind": "row",
                    "label": "Source",
                    "value": "*Penicillium* moulds, chiefly *P. rubens* and *P. chrysogenum*",
                },
                {
                    "kind": "row",
                    "label": "Core",
                    "value": "Fused beta-lactam and thiazolidine rings",
                },
                {
                    "kind": "row",
                    "label": "Target",
                    "value": "Transpeptidases that cross-link bacterial peptidoglycan",
                },
                {
                    "kind": "row",
                    "label": "Spectrum",
                    "value": "Chiefly Gram-positive bacteria and spirochaetes",
                },
                {"kind": "header", "value": "Chronology"},
                {
                    "kind": "row",
                    "label": "Observed",
                    "value": "September 1928, by Alexander Fleming",
                },
                {"kind": "row", "label": "First published", "value": "1929"},
                {"kind": "row", "label": "Mouse protection test", "value": "25 May 1940, Oxford"},
                {"kind": "row", "label": "First patient treated", "value": "February 1941"},
                {
                    "kind": "row",
                    "label": "Nobel Prize",
                    "value": "1945, to Fleming, Chain and Florey",
                },
                {
                    "kind": "full",
                    "value": "Potency was measured in Oxford units before pure material existed",
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Penicillium_notatum.jpg",
            "alt": (
                "A petri dish of agar carrying a blue-green Penicillium colony with a pale "
                "outer fringe"
            ),
            "caption": (
                "A culture of Penicillium chrysogenum, long known as P. notatum, the mould "
                "genus from which penicillin was first obtained."
            ),
            "credit": "Crulina 98",
            "license": "CC BY-SA 3.0",
            "source_url": "https://commons.wikimedia.org/wiki/File:Penicillium_notatum.jpg",
        },
        "references": [
            {
                "key": "fleming1929",
                "title": (
                    "On the Antibacterial Action of Cultures of a Penicillium, with Special "
                    "Reference to Their Use in the Isolation of B. influenzae"
                ),
                "url": "https://pubmed.ncbi.nlm.nih.gov/6994200/",
                "authors": "Alexander Fleming",
                "publisher": "British Journal of Experimental Pathology 10, 226-236",
                "published_on": "1929",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "gaynes2017",
                "title": (
                    "The Discovery of Penicillin — New Insights After More Than 75 Years of "
                    "Clinical Use"
                ),
                "url": "https://wwwnc.cdc.gov/eid/article/23/5/16-1556_article",
                "authors": "Robert Gaynes",
                "publisher": "Emerging Infectious Diseases 23(5), 849-853",
                "published_on": "May 2017",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.3201/eid2305.161556",
                "quote": "",
            },
            {
                "key": "acs_landmark",
                "title": "Alexander Fleming: Discovery and Development of Penicillin",
                "url": (
                    "https://www.acs.org/education/whatischemistry/landmarks/flemingpenicillin.html"
                ),
                "authors": "",
                "publisher": "American Chemical Society, National Historic Chemical Landmarks",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "sciencemuseum",
                "title": "How Was Penicillin Developed?",
                "url": (
                    "https://www.sciencemuseum.org.uk/objects-and-stories/"
                    "how-was-penicillin-developed"
                ),
                "authors": "",
                "publisher": "Science Museum Group, London",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nobel1945",
                "title": "The Nobel Prize in Physiology or Medicine 1945",
                "url": "https://www.nobelprize.org/prizes/medicine/1945/summary/",
                "authors": "",
                "publisher": "Nobel Foundation",
                "published_on": "1945",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "who_amr",
                "title": "Antimicrobial Resistance",
                "url": (
                    "https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance"
                ),
                "authors": "",
                "publisher": "World Health Organization",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Germ theory of disease",
            "Natural selection",
            "Vaccination",
            "The cell",
            "Deoxyribonucleic acid",
        ],
        "aliases": ["Antibiotics"],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["antibiotics", "beta-lactam", "microbiology", "drug discovery"],
    },
    {
        "title": "Human anatomy",
        "category": "Medicine and the Mind",
        "categories": ["Life Sciences", "History"],
        "short_description": "The structure of the human body and the history of describing it",
        "summary": (
            "Human anatomy is the study of the structure of the body and the relations "
            "between its parts. Its modern form dates from sixteenth-century dissection and "
            "printed atlases; imaging since 1895 has opened the living body to inspection."
        ),
        "content": """**Human anatomy** is the study of the structure of the human body and of the
spatial relations between its parts. It divides by scale into gross anatomy, visible to the
unaided eye, and microscopic anatomy or histology; by approach into regional anatomy, which
works through the body area by area, and systemic anatomy, which follows one organ system at a
time. Its history is largely a history of access: what could be seen, on what kind of body,
and whether the result could be checked by anyone else.

## Terms of reference

Anatomical descriptions are relative to a convention called the anatomical position: the body
upright, feet together, arms at the sides, palms facing forward. Against that reference,
superior and inferior mean towards the head and the feet, anterior and posterior towards the
front and back, medial and lateral towards and away from the midline, and proximal and distal
nearer to and further from a limb's attachment. Three standard planes cut the body: sagittal
(left from right), coronal (front from back) and transverse (upper from lower). The convention
matters because ordinary words fail once a body changes posture: the sole of the foot is
inferior whether a person is standing or lying down.

## Levels of organisation

The conventional hierarchy runs from molecules to [[The cell|cells]] — of the order of 37
trillion of them in an adult, by one careful reckoning[^bianconi2013] — then to four basic
tissue types, epithelial, connective, muscular and nervous, then to organs, and then to eleven
organ systems: integumentary, skeletal, muscular, nervous, endocrine, cardiovascular,
lymphatic, respiratory, digestive, urinary and reproductive. An adult skeleton is conventionally
counted as 206 bones, although a newborn has many more separate elements that later fuse, and
more than 600 skeletal muscles move them. The resting heart pushes roughly five litres of blood
a minute; a few hundred million alveoli present a gas-exchange surface of the order of seventy
square metres; and water makes up around 60 per cent of an adult's mass. Such figures describe
a statistical body: arterial patterns in the heart and kidneys vary widely, and about one
person in ten thousand has situs inversus, with the thoracic and abdominal organs mirrored
left to right.

## Antiquity and its inherited errors

[[Aristotle]] dissected animals and founded comparative anatomy, but sustained human dissection
in antiquity was confined to a brief episode at Alexandria in the early third century BCE, where
Herophilus and Erasistratus opened human bodies and described the nerves, the brain's
ventricles and the valves of the heart. Their writings survive only as quotations in later
authors, and the practice lapsed after the first generation of scholars at the
[[The Library of Alexandria|Mouseion]].

Galen, working in the second century CE, produced the anatomy that both Latin Europe and the
Islamic world used for more than a thousand years. Roman custom barred him from human
dissection, so he worked on Barbary macaques, pigs and oxen and transferred what he found. The
result carried animal structures into the human record: he described a *rete mirabile*, a dense
vascular plexus at the base of the brain that exists in hoofed animals but not in people, gave
the liver five lobes, and treated the lower jaw as two bones because it is two in the dog.[^galen]
Galen's authority was not absolute — the thirteenth-century Cairo physician Ibn al-Nafis
rejected his account of blood crossing the wall between the ventricles — but his text was the
framework within which anatomy was taught.

## Dissection and the printed atlas

Public dissection resumed in the Italian universities around 1315, and Mondino de Luzzi's
*Anathomia* of 1316 gave Bologna a dissection manual that was still in use two centuries later.
It followed Galen. [[Leonardo da Vinci]], dissecting in the decades around 1500, produced
several hundred anatomical drawings of great accuracy and wrote of having opened more than
thirty bodies, but never published them; they influenced almost nobody for three centuries.

The break came with Andreas Vesalius, professor at Padua, whose *De humani corporis fabrica
libri septem* was printed at Basel in 1543 by Johannes Oporinus when he was about
twenty-eight.[^nlm_vesalius] Vesalius dissected human bodies himself, corrected Galen at
hundreds of points, and — decisively — commissioned large woodcuts, cut in Venice and often
associated with the workshop of Titian, that were keyed to the text. The
[[The printing press|printing press]] meant identical figures could be set beside a body in any
anatomy theatre in Europe and checked, making anatomical claims contestable as manuscript
description never had been. Everything still depended on a supply of cadavers, which came from
executed criminals and, after Britain's Anatomy Act of 1832, from the unclaimed dead; the
[[The Renaissance|Renaissance]] artists who studied anatomy worked under the same constraint.

## From structure to function

William Harvey's *De motu cordis*, published at Frankfurt in 1628, settled an anatomical
question by measurement: the heart expels far more blood in an hour than the body contains, so
the same blood must circulate, and the one-way valves in the veins show which way it
goes.[^harvey] That replaced the Galenic scheme in which blood was continuously manufactured
and consumed, and made anatomy answerable to quantity. Microscopy extended the same logic
downwards, until structure at cellular scale became inseparable from physiology, and
[[Germ theory of disease|germ theory]] made anatomy practical for surgery. *Anatomy:
Descriptive and Surgical*, which Henry Gray published in 1858 with wood engravings by Henry
Vandyke Carter, fixed the form of the teaching atlas.

## Imaging

X-rays, discovered in November 1895, gave the first view of structure inside a living person.
Computed tomography reconstructs a cross-section from many projections taken at different
angles: the first clinical scan was made on 1 October 1971 at the Atkinson Morley Hospital in
London with a prototype built by Godfrey Hounsfield at EMI, taking several minutes per slice.
Hounsfield shared the 1979 Nobel Prize in Physiology or Medicine with Allan
Cormack.[^nobel1979] Magnetic resonance imaging followed, and with it the ability to relate
function to structure in a living brain, the method behind much of what is now known about
[[Memory|memory]] and the hippocampus. The Visible Human Project at the US National Library of
Medicine released a male body photographed at one-millimetre intervals in 1994 and a female at
0.33 millimetres in 1995.[^nlm_visible]

## Terminology

Anatomical vocabulary is Latin and Greek, standardised so that a structure has one name across
languages. The Basle *Nomina Anatomica* of 1895 began the process; the current standard is
*Terminologia Anatomica*, first issued in 1998, whose second edition was published online in
2019 by the Federative International Programme for Anatomical Terminologies.[^fipat] Eponyms
such as the circle of Willis and the islets of Langerhans survive in clinical use, but the
standard prefers descriptive terms.
""",
        "tier": "standard",
        "kind": "discipline",
        "infobox": {
            "title": "Human anatomy",
            "subtitle": "Branch of the biological sciences",
            "rows": [
                {
                    "kind": "row",
                    "label": "Subject",
                    "value": "Structure of the human body and the relations between its parts",
                },
                {
                    "kind": "row",
                    "label": "Main divisions",
                    "value": "Gross anatomy, histology, embryology, radiological anatomy",
                },
                {
                    "kind": "row",
                    "label": "Standard terminology",
                    "value": "*Terminologia Anatomica* (1998; second edition 2019)",
                },
                {"kind": "header", "value": "Conventional adult figures"},
                {"kind": "row", "label": "Bones", "value": "206"},
                {"kind": "row", "label": "Skeletal muscles", "value": "More than 600"},
                {"kind": "row", "label": "Organ systems", "value": "Eleven"},
                {"kind": "row", "label": "Cells", "value": "Of the order of 37 trillion"},
                {"kind": "header", "value": "Landmark works"},
                {
                    "kind": "row",
                    "label": "Galen",
                    "value": "Anatomical writings, second century CE",
                },
                {
                    "kind": "row",
                    "label": "Vesalius",
                    "value": "*De humani corporis fabrica*, Basel, 1543",
                },
                {
                    "kind": "row",
                    "label": "Harvey",
                    "value": "*De motu cordis*, Frankfurt, 1628",
                },
                {
                    "kind": "row",
                    "label": "Gray",
                    "value": "*Anatomy: Descriptive and Surgical*, London, 1858",
                },
            ],
        },
        "image": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/2/23/Vesalius_Fabrica_p190.jpg",
            "alt": (
                "Woodcut of a flayed human figure standing in a landscape with the muscles of "
                "the trunk and limbs exposed"
            ),
            "caption": (
                "A muscle figure from Vesalius's De humani corporis fabrica of 1543, one of "
                "the plates that made printed anatomy checkable against a body."
            ),
            "credit": "Andreas Vesalius, De humani corporis fabrica (Basel, 1543)",
            "license": "Public domain",
            "source_url": "https://commons.wikimedia.org/wiki/File:Vesalius_Fabrica_p190.jpg",
        },
        "references": [
            {
                "key": "nlm_vesalius",
                "title": "Historical Anatomies on the Web: Andreas Vesalius",
                "url": (
                    "https://www.nlm.nih.gov/exhibition/historicalanatomies/vesalius_home.html"
                ),
                "authors": "",
                "publisher": "U.S. National Library of Medicine",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "galen",
                "title": "Galen",
                "url": "https://www.britannica.com/biography/Galen",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "harvey",
                "title": "William Harvey",
                "url": "https://www.britannica.com/biography/William-Harvey",
                "authors": "",
                "publisher": "Encyclopaedia Britannica",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "bianconi2013",
                "title": "An Estimation of the Number of Cells in the Human Body",
                "url": "https://www.tandfonline.com/doi/abs/10.3109/03014460.2013.807878",
                "authors": "Eva Bianconi, Allison Piovesan, Silvia Canaider and colleagues",
                "publisher": "Annals of Human Biology 40(6), 463-471",
                "published_on": "2013",
                "accessed_on": "2026-09-26",
                "identifier": "doi:10.3109/03014460.2013.807878",
                "quote": "",
            },
            {
                "key": "nobel1979",
                "title": "The Nobel Prize in Physiology or Medicine 1979",
                "url": "https://www.nobelprize.org/prizes/medicine/1979/summary/",
                "authors": "",
                "publisher": "Nobel Foundation",
                "published_on": "1979",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "nlm_visible",
                "title": "The Visible Human Project",
                "url": "https://www.nlm.nih.gov/research/visible/visible_human.html",
                "authors": "",
                "publisher": "U.S. National Library of Medicine",
                "published_on": "",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
            {
                "key": "fipat",
                "title": "Terminologia Anatomica, Second Edition",
                "url": "https://fipat.library.dal.ca/TA2/",
                "authors": "",
                "publisher": (
                    "Federative International Programme for Anatomical Terminologies, "
                    "International Federation of Associations of Anatomists"
                ),
                "published_on": "2019",
                "accessed_on": "2026-09-26",
                "identifier": "",
                "quote": "",
            },
        ],
        "see_also": [
            "Leonardo da Vinci",
            "The cell",
            "Germ theory of disease",
            "Memory",
            "The Renaissance",
            "Aristotle",
        ],
        "aliases": [],
        "is_stub": False,
        "is_disambiguation": False,
        "tags": ["anatomy", "history of medicine", "dissection", "medical imaging"],
    },
]
