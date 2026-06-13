import streamlit as st
st.set_page_config(page_title="Animal Encyclopedia", page_icon="🐾", layout="wide", initial_sidebar_state="expanded")

import random, datetime, urllib.parse, json, math, re

try:
    import requests as _req
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ══════════════════════════════════════════════════════════════
# ANIMALS DATABASE  (expanded with scientific + stats fields)
# ══════════════════════════════════════════════════════════════
ANIMALS = {
    "Lion": {
        "emoji":"🦁","category":"Mammal","habitat":"Savanna, Grasslands","diet":"Carnivore",
        "lifespan_years":12,"weight_kg":185,"speed_kmh":80,"conservation":"Vulnerable",
        "conservation_color":"#fb923c","region":"Africa","continent":"Africa",
        "scientific_name":"Panthera leo","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Carnivora","family":"Felidae","genus":"Panthera",
        "fun_fact":"A lion's roar can be heard from up to 8 km away.",
        "description":"The lion is the second-largest living cat after the tiger. Known as the 'king of the jungle', lions are highly social and live in groups called prides. Males are distinguished by their impressive manes.",
        "related":["Cheetah","Snow Leopard","Tiger"],
        "image_query":"lion wild africa savanna",
    },
    "Blue Whale": {
        "emoji":"🐋","category":"Mammal","habitat":"Open Ocean","diet":"Filter Feeder",
        "lifespan_years":85,"weight_kg":150000,"speed_kmh":46,"conservation":"Endangered",
        "conservation_color":"#ef4444","region":"Worldwide","continent":"Worldwide",
        "scientific_name":"Balaenoptera musculus","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Artiodactyla","family":"Balaenopteridae","genus":"Balaenoptera",
        "fun_fact":"The blue whale's heart is the size of a small car and can weigh 400 kg.",
        "description":"The blue whale is the largest animal known to have ever existed. Despite their enormous size, blue whales feed almost exclusively on tiny shrimp-like creatures called krill, consuming up to 4 tonnes per day.",
        "related":["Manta Ray","Humpback Whale","Orca"],
        "image_query":"blue whale ocean underwater",
    },
    "Snow Leopard": {
        "emoji":"🐆","category":"Mammal","habitat":"Mountain Ranges","diet":"Carnivore",
        "lifespan_years":11,"weight_kg":38,"speed_kmh":64,"conservation":"Vulnerable",
        "conservation_color":"#fb923c","region":"Central Asia","continent":"Asia",
        "scientific_name":"Panthera uncia","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Carnivora","family":"Felidae","genus":"Panthera",
        "fun_fact":"Snow leopards cannot roar — they make a unique sound called a 'chuff'.",
        "description":"Snow leopards are elusive big cats adapted to life in cold, mountainous environments. Their thick fur, wide paws that act as natural snowshoes, and long tails for balance make them perfectly suited for the Himalayas.",
        "related":["Lion","Cheetah","Tiger"],
        "image_query":"snow leopard mountain wild",
    },
    "Emperor Penguin": {
        "emoji":"🐧","category":"Bird","habitat":"Antarctica","diet":"Carnivore",
        "lifespan_years":17,"weight_kg":34,"speed_kmh":9,"conservation":"Near Threatened",
        "conservation_color":"#facc15","region":"Antarctica","continent":"Antarctica",
        "scientific_name":"Aptenodytes forsteri","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Aves","order":"Sphenisciformes","family":"Spheniscidae","genus":"Aptenodytes",
        "fun_fact":"Emperor penguins can dive to depths of over 500 metres and hold their breath for 20 minutes.",
        "description":"The emperor penguin is the tallest and heaviest of all penguin species. They breed during the harsh Antarctic winter, with males incubating a single egg on their feet under a brood pouch for up to 65 days.",
        "related":["Bald Eagle","Albatross"],
        "image_query":"emperor penguin antarctica colony",
    },
    "Komodo Dragon": {
        "emoji":"🦎","category":"Reptile","habitat":"Tropical Forest","diet":"Carnivore",
        "lifespan_years":30,"weight_kg":80,"speed_kmh":20,"conservation":"Endangered",
        "conservation_color":"#ef4444","region":"Indonesia","continent":"Asia",
        "scientific_name":"Varanus komodoensis","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Reptilia","order":"Squamata","family":"Varanidae","genus":"Varanus",
        "fun_fact":"Komodo dragons can detect carrion from up to 9.5 km away using their forked tongues.",
        "description":"The Komodo dragon is the world's largest living lizard. Found only on a handful of Indonesian islands, these apex predators use venom and bacteria-laden saliva to subdue prey much larger than themselves.",
        "related":["Poison Dart Frog","Saltwater Crocodile"],
        "image_query":"komodo dragon indonesia wild",
    },
    "Bald Eagle": {
        "emoji":"🦅","category":"Bird","habitat":"Forests, Near Water","diet":"Carnivore",
        "lifespan_years":25,"weight_kg":5,"speed_kmh":160,"conservation":"Least Concern",
        "conservation_color":"#34d399","region":"North America","continent":"North America",
        "scientific_name":"Haliaeetus leucocephalus","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Aves","order":"Accipitriformes","family":"Accipitridae","genus":"Haliaeetus",
        "fun_fact":"Bald eagles build the largest bird nests in North America — up to 4 metres deep and 2.5 metres wide.",
        "description":"The bald eagle is the national bird and symbol of the United States. A master fisher, it swoops down at speeds of up to 160 km/h to snatch fish from the water with its powerful talons.",
        "related":["Emperor Penguin","Peregrine Falcon"],
        "image_query":"bald eagle flying wild nature",
    },
    "Poison Dart Frog": {
        "emoji":"🐸","category":"Amphibian","habitat":"Tropical Rainforest","diet":"Insectivore",
        "lifespan_years":9,"weight_kg":0.003,"speed_kmh":3,"conservation":"Varies by Species",
        "conservation_color":"#a78bfa","region":"Central & South America","continent":"South America",
        "scientific_name":"Dendrobatidae (family)","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Amphibia","order":"Anura","family":"Dendrobatidae","genus":"Dendrobates",
        "fun_fact":"The golden poison frog has enough toxin to kill 10 adult humans.",
        "description":"Poison dart frogs are among the most toxic animals on Earth, yet their vivid colours serve as a warning to predators — a phenomenon called aposematism. Their toxins come from their diet of specific insects in the wild.",
        "related":["Komodo Dragon","Axolotl"],
        "image_query":"poison dart frog colorful rainforest",
    },
    "Giant Panda": {
        "emoji":"🐼","category":"Mammal","habitat":"Temperate Broadleaf Forest","diet":"Herbivore",
        "lifespan_years":20,"weight_kg":100,"speed_kmh":32,"conservation":"Vulnerable",
        "conservation_color":"#fb923c","region":"China","continent":"Asia",
        "scientific_name":"Ailuropoda melanoleuca","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Carnivora","family":"Ursidae","genus":"Ailuropoda",
        "fun_fact":"Giant pandas spend 10–16 hours a day eating bamboo to get enough nutrition.",
        "description":"The giant panda is one of the world's most beloved and recognisable animals. Despite being classified as carnivores, pandas have evolved to eat almost exclusively bamboo, consuming 12–38 kg of it each day.",
        "related":["Arctic Fox","Snow Leopard"],
        "image_query":"giant panda bamboo China wildlife",
    },
    "Manta Ray": {
        "emoji":"🐟","category":"Fish","habitat":"Tropical Ocean","diet":"Filter Feeder",
        "lifespan_years":40,"weight_kg":1400,"speed_kmh":35,"conservation":"Vulnerable",
        "conservation_color":"#fb923c","region":"Worldwide","continent":"Worldwide",
        "scientific_name":"Mobula birostris","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Chondrichthyes","order":"Myliobatiformes","family":"Mobulidae","genus":"Mobula",
        "fun_fact":"Manta rays have the largest brain-to-body ratio of any cold-blooded fish.",
        "description":"Manta rays are graceful giants of the ocean, gliding through the water using their large, wing-like pectoral fins. They are highly intelligent and have been observed in what appears to be playful behaviour and self-recognition.",
        "related":["Blue Whale","Octopus"],
        "image_query":"manta ray ocean underwater swimming",
    },
    "Arctic Fox": {
        "emoji":"🦊","category":"Mammal","habitat":"Arctic Tundra","diet":"Omnivore",
        "lifespan_years":4,"weight_kg":5,"speed_kmh":50,"conservation":"Least Concern",
        "conservation_color":"#34d399","region":"Arctic","continent":"Arctic",
        "scientific_name":"Vulpes lagopus","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Carnivora","family":"Canidae","genus":"Vulpes",
        "fun_fact":"The Arctic fox can withstand temperatures as low as −70 °C before its metabolism increases.",
        "description":"The Arctic fox is a small, resilient canid perfectly adapted to one of Earth's harshest environments. Its thick, multi-layered fur turns white in winter for camouflage in snow and brown in summer.",
        "related":["Giant Panda","Lion"],
        "image_query":"arctic fox white snow tundra wild",
    },
    "Cheetah": {
        "emoji":"🐆","category":"Mammal","habitat":"Savanna, Grasslands","diet":"Carnivore",
        "lifespan_years":11,"weight_kg":50,"speed_kmh":120,"conservation":"Vulnerable",
        "conservation_color":"#fb923c","region":"Africa, Iran","continent":"Africa",
        "scientific_name":"Acinonyx jubatus","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Carnivora","family":"Felidae","genus":"Acinonyx",
        "fun_fact":"The cheetah accelerates from 0 to 100 km/h in just 3 seconds — faster than most sports cars.",
        "description":"The cheetah is the fastest land animal on Earth, capable of reaching speeds of up to 120 km/h. Unlike other big cats, cheetahs cannot roar but can purr.",
        "related":["Lion","Snow Leopard","Bald Eagle"],
        "image_query":"cheetah running africa wild savanna",
    },
    "Octopus": {
        "emoji":"🐙","category":"Cephalopod","habitat":"Ocean (all depths)","diet":"Carnivore",
        "lifespan_years":3,"weight_kg":10,"speed_kmh":40,"conservation":"Least Concern",
        "conservation_color":"#34d399","region":"Worldwide","continent":"Worldwide",
        "scientific_name":"Octopus vulgaris","kingdom":"Animalia","phylum":"Mollusca",
        "class_":"Cephalopoda","order":"Octopoda","family":"Octopodidae","genus":"Octopus",
        "fun_fact":"Octopuses have three hearts, blue blood, and nine brains (one central + one per arm).",
        "description":"Octopuses are remarkably intelligent invertebrates capable of problem-solving, tool use, and even short-term memory. They can change colour and texture in milliseconds to camouflage themselves.",
        "related":["Manta Ray","Blue Whale"],
        "image_query":"octopus underwater ocean wild",
    },
    "Tiger": {
        "emoji":"🐯","category":"Mammal","habitat":"Tropical Forest, Grasslands","diet":"Carnivore",
        "lifespan_years":12,"weight_kg":220,"speed_kmh":65,"conservation":"Endangered",
        "conservation_color":"#ef4444","region":"Asia","continent":"Asia",
        "scientific_name":"Panthera tigris","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Carnivora","family":"Felidae","genus":"Panthera",
        "fun_fact":"No two tigers have the same stripe pattern — like human fingerprints.",
        "description":"The tiger is the largest wild cat species. A solitary apex predator, it primarily hunts deer and wild boar. Tigers are strong swimmers and cool off in pools and streams.",
        "related":["Lion","Snow Leopard","Cheetah"],
        "image_query":"tiger wild jungle asia",
    },
    "Gorilla": {
        "emoji":"🦍","category":"Mammal","habitat":"Tropical Rainforest","diet":"Herbivore",
        "lifespan_years":35,"weight_kg":160,"speed_kmh":40,"conservation":"Endangered",
        "conservation_color":"#ef4444","region":"Central Africa","continent":"Africa",
        "scientific_name":"Gorilla gorilla","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Primates","family":"Hominidae","genus":"Gorilla",
        "fun_fact":"Gorillas share about 98.3% of their DNA with humans.",
        "description":"Gorillas are the largest living primates. They are highly social and live in family groups led by a dominant silverback male. Despite their fearsome reputation, gorillas are gentle herbivores.",
        "related":["Lion","Giant Panda"],
        "image_query":"gorilla wild africa rainforest",
    },
    "Elephant": {
        "emoji":"🐘","category":"Mammal","habitat":"Savanna, Forest","diet":"Herbivore",
        "lifespan_years":65,"weight_kg":5000,"speed_kmh":40,"conservation":"Vulnerable",
        "conservation_color":"#fb923c","region":"Africa, Asia","continent":"Africa",
        "scientific_name":"Loxodonta africana","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Proboscidea","family":"Elephantidae","genus":"Loxodonta",
        "fun_fact":"Elephants are the only animals that can't jump — but they can swim for miles.",
        "description":"African elephants are the largest land animals on Earth. Highly intelligent and deeply social, they live in matriarchal herds and are known to mourn their dead and communicate via infrasound.",
        "related":["Gorilla","Lion","Blue Whale"],
        "image_query":"elephant wild africa savanna",
    },
    "Polar Bear": {
        "emoji":"🐻‍❄️","category":"Mammal","habitat":"Arctic Ice","diet":"Carnivore",
        "lifespan_years":25,"weight_kg":450,"speed_kmh":40,"conservation":"Vulnerable",
        "conservation_color":"#fb923c","region":"Arctic","continent":"Arctic",
        "scientific_name":"Ursus maritimus","kingdom":"Animalia","phylum":"Chordata",
        "class_":"Mammalia","order":"Carnivora","family":"Ursidae","genus":"Ursus",
        "fun_fact":"Polar bears have black skin and translucent fur that appears white — it reflects light.",
        "description":"Polar bears are the world's largest land carnivores. They are excellent swimmers, using their large front paws to paddle through icy Arctic waters in search of seals.",
        "related":["Arctic Fox","Giant Panda"],
        "image_query":"polar bear arctic ice wild",
    },
}

CATEGORIES = ["All"] + sorted(set(a["category"] for a in ANIMALS.values()))
CONTINENTS = ["All"] + sorted(set(a["continent"] for a in ANIMALS.values()))
DIETS      = ["All"] + sorted(set(a["diet"] for a in ANIMALS.values()))
CONSERVATION_STATUSES = ["All","Least Concern","Near Threatened","Vulnerable","Endangered","Critically Endangered"]
CONSERVATION_ORDER    = {"Least Concern":0,"Near Threatened":1,"Vulnerable":2,"Endangered":3,"Critically Endangered":4,"Varies by Species":5}
CONSERVATION_COLORS   = {"Least Concern":"#34d399","Near Threatened":"#facc15","Vulnerable":"#fb923c","Endangered":"#ef4444","Critically Endangered":"#dc2626","Unknown":"#64748b","Varies by Species":"#a78bfa"}

WIKI_HEADERS = {"User-Agent":"AnimalEncyclopedia/4.0 (educational)"}

# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
DEFAULTS = {
    "page": "home",           # home | detail | quiz | guess | conservation | habitat | stats | explorer
    "selected": None,
    "wiki_cache": {},
    "favorites": [],
    "history": [],
    "free_results": [],
    "free_query": "",
    # quiz
    "quiz_q": 0,
    "quiz_score": 0,
    "quiz_questions": [],
    "quiz_answered": False,
    "quiz_selected": None,
    # guess game
    "guess_animal": None,
    "guess_revealed": [],
    "guess_done": False,
    "guess_wrong": 0,
    "guess_won": False,
    # explorer filters
    "exp_continent": "All",
    "exp_diet": "All",
    "exp_conservation": "All",
    "exp_weight_max": 200000,
    "exp_speed_max": 200,
    "exp_lifespan_max": 100,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════
# API HELPERS
# ══════════════════════════════════════════════════════════════
def _get(url, params=None, timeout=6):
    if not HAS_REQUESTS:
        return None
    try:
        r = _req.get(url, params=params, headers=WIKI_HEADERS, timeout=timeout)
        return r if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def wiki_search(q):
    """
    Multi-strategy Wikipedia search that finds virtually any animal.
    Strategy 1: direct page lookup (handles exact names like 'Betta fish', 'Tardigrade')
    Strategy 2: opensearch autocomplete (catches common names)
    Strategy 3: full-text search (catches obscure/scientific names)
    """
    BAD = ["film","movie","album","band","song","footballer","politician","actor",
           "singer","book","novel","video game","television","series","disambiguation",
           "hurricane","typhoon","operation","character","episode","list of",
           "municipality","city","town","village","county","district","province"]

    results = []
    seen = set()

    def add(title, snippet=""):
        if title in seen: return
        combined = (title + " " + snippet).lower()
        if any(b in combined for b in BAD): return
        seen.add(title)
        results.append(title)

    # Strategy 1: Direct page lookup — works perfectly for "Betta fish", "Tardigrade", etc.
    r1 = _get("https://en.wikipedia.org/w/api.php", {
        "action": "query", "titles": q,
        "prop": "info|extracts", "exintro": "1", "exsentences": "1",
        "redirects": "1", "format": "json"})
    if r1:
        pages = r1.json().get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid != "-1":  # -1 means not found
                add(page.get("title", q))

    # Strategy 2: OpenSearch autocomplete — great for common names
    r2 = _get("https://en.wikipedia.org/w/api.php", {
        "action": "opensearch", "search": q,
        "limit": "8", "namespace": "0", "format": "json"})
    if r2:
        titles = r2.json()[1] if len(r2.json()) > 1 else []
        for t in titles:
            add(t)

    # Strategy 3: Full-text search — catches scientific names and rare species
    r3 = _get("https://en.wikipedia.org/w/api.php", {
        "action": "query", "list": "search",
        "srsearch": q, "srnamespace": "0",
        "srlimit": "10", "srprop": "snippet", "format": "json"})
    if r3:
        for item in r3.json().get("query", {}).get("search", []):
            add(item["title"], item.get("snippet", ""))

    # Filter to likely animal articles using Wikipedia's description field
    final = []
    ANIMAL_HINTS = ["animal","species","fish","bird","mammal","reptile","amphibian",
                    "insect","invertebrate","arthropod","mollus","crustacean","arachnid",
                    "worm","cnidarian","echinoderm","bacterium","protist","fungus",
                    "genus","family","order","class","phylum","organism","creature",
                    "fauna","wildlife","predator","prey","herbivore","carnivore",
                    "parasite","microorganism","tardigrade","microscopic"]
    NOT_ANIMAL = ["film","album","song","band","footballer","actor","singer",
                  "municipality","city","town","village","novel","video game",
                  "television","hurricane","politician","person","athlete"]

    for title in results:
        tl = title.lower()
        # immediately reject obvious non-animals
        if any(b in tl for b in NOT_ANIMAL): continue
        # check the Wikipedia description field quickly
        safe = urllib.parse.quote(title.replace(" ", "_"))
        rd = _get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe}")
        if rd:
            d = rd.json()
            desc_field = d.get("description", "").lower()
            extract    = d.get("extract", "")[:300].lower()
            combined   = desc_field + " " + extract
            # accept if any animal hint found, or no NOT_ANIMAL flag
            is_animal = any(h in combined for h in ANIMAL_HINTS)
            is_not    = any(b in desc_field for b in NOT_ANIMAL)
            if is_animal and not is_not:
                final.append(title)
            elif not is_not and title not in [r["title"] if isinstance(r,dict) else r for r in final]:
                # ambiguous — include anyway, user can decide
                final.append(title)
        else:
            final.append(title)  # network error — include optimistically
        if len(final) >= 9:
            break

    return final[:9]


@st.cache_data(ttl=3600, show_spinner=False)
def wiki_summary(title):
    safe = urllib.parse.quote(title.replace(" ","_"))
    r = _get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe}")
    return r.json() if r else {}

@st.cache_data(ttl=3600, show_spinner=False)
def wiki_images(title):
    r = _get("https://en.wikipedia.org/w/api.php", {
        "action":"query","titles":title,"prop":"images","imlimit":"30","format":"json"})
    if not r: return []
    BAD = ["flag","icon","logo","map","symbol","blank","commons","wikimedia","edit",
           "question","sound","audio","silhouette","range","distribution","coa","coat"]
    out = []
    for p in r.json().get("query",{}).get("pages",{}).values():
        for img in p.get("images",[]):
            nm = img["title"].lower()
            if any(b in nm for b in BAD): continue
            if nm.endswith((".svg",".ogg",".ogv",".webm",".pdf")): continue
            out.append(img["title"])
    return out[:8]

@st.cache_data(ttl=3600, show_spinner=False)
def resolve_img(ft):
    r = _get("https://en.wikipedia.org/w/api.php", {
        "action":"query","titles":ft,"prop":"imageinfo",
        "iiprop":"url|dimensions","iiurlwidth":"500","format":"json"})
    if not r: return None
    for p in r.json().get("query",{}).get("pages",{}).values():
        info = p.get("imageinfo",[])
        if info: return info[0].get("thumburl") or info[0].get("url")
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def gbif_lookup(name):
    """
    GBIF lookup — tries the exact name first, then falls back to a fuzzy match.
    Works with common names ('Betta fish'), scientific names ('Betta splendens'),
    and everything in between.
    """
    # Try exact match first
    r = _get("https://api.gbif.org/v1/species/match", {
        "name": name, "verbose": "false"})
    d = r.json() if r else {}

    # If no match, try without 'fish'/'bird' suffix words
    if not d or d.get("matchType") == "NONE":
        clean = re.sub(r'\b(fish|bird|snake|frog|worm|spider|beetle|fly|bee|ant|shark|whale|bear|cat|dog|wolf|fox)\b', '', name, flags=re.I).strip()
        if clean and clean != name:
            r2 = _get("https://api.gbif.org/v1/species/match", {
                "name": clean, "verbose": "false"})
            if r2: d = r2.json()

    if not d or d.get("matchType") == "NONE":
        return {}

    key = d.get("usageKey")
    if not key:
        return {}

    # Fetch occurrence count
    r3 = _get("https://api.gbif.org/v1/occurrence/search", {"taxonKey": key, "limit": "0"})
    occ_count = r3.json().get("count", 0) if r3 else 0

    return {
        "gbif_key": key,
        "kingdom": d.get("kingdom", ""),
        "phylum":  d.get("phylum", ""),
        "class_":  d.get("clazz", ""),
        "order":   d.get("order", ""),
        "family":  d.get("family", ""),
        "genus":   d.get("genus", ""),
        "species": d.get("species", ""),
        "status":  d.get("status", ""),
        "occurrence_count": occ_count,
        "gbif_url": f"https://www.gbif.org/species/{key}",
    }

def _parse_extract(text):
    """
    Scan the Wikipedia extract for diet, habitat, conservation, lifespan,
    weight, speed and a fun-fact sentence. Returns a dict of found values.
    All values remain as display strings (no numeric coercion needed here).
    """
    t = text.lower()
    result = {}

    # ── Diet ─────────────────────────────────────────────────────────────────
    diet_map = [
        (r'\b(carnivore|carnivorous|feeds? on (?:meat|fish|mammals?|birds?|insects?|invertebrates?|prey|other animals))\b', "Carnivore"),
        (r'\b(herbivore|herbivorous|feeds? on (?:plants?|leaves?|grass|vegetation|bamboo|algae|seagrass))\b', "Herbivore"),
        (r'\b(omnivore|omnivorous|feeds? on (?:both|variety of|plants? and|animals? and))\b', "Omnivore"),
        (r'\b(insectivore|insectivorous|feeds? on insects?)\b', "Insectivore"),
        (r'\b(filter.feed|suspension.feed)\b', "Filter Feeder"),
        (r'\b(feeds? on (?:plankton|krill|zooplankton|phytoplankton))\b', "Filter Feeder"),
        (r'\b(piscivore|piscivorous|feeds? (?:mainly |primarily )?on fish)\b', "Piscivore"),
        (r'\b(frugivore|frugivorous|fruit.eating|feeds? on fruit)\b', "Frugivore"),
        (r'\b(detritivore|detritivorous|feeds? on (?:decaying|detritus|dead matter))\b', "Detritivore"),
        (r'\b(nectarivore|feeds? on nectar)\b', "Nectarivore"),
        (r'\b(granivore|feeds? on seeds?|seed.eating)\b', "Granivore"),
        (r'\b(parasite|parasitic|feeds? on (?:host|blood|tissue))\b', "Parasite"),
        (r'\b(scavenger|scavenges?|feeds? on carrion)\b', "Scavenger"),
        (r'\b(feeds? on|eats?|diet (?:consists?|is|includes?))\b', "Omnivore"),  # generic fallback
    ]
    for pat, label in diet_map:
        if re.search(pat, t):
            result["diet"] = label
            break

    # ── Conservation ─────────────────────────────────────────────────────────
    con_map = [
        (r'critically endangered', "Critically Endangered", "#dc2626"),
        (r'\bendangered\b', "Endangered", "#ef4444"),
        (r'vulnerable', "Vulnerable", "#fb923c"),
        (r'near threatened', "Near Threatened", "#facc15"),
        (r'least concern', "Least Concern", "#34d399"),
        (r'data deficient', "Data Deficient", "#64748b"),
        (r'iucn red list', "See IUCN Red List", "#a78bfa"),
    ]
    for pat, label, color in con_map:
        if re.search(pat, t):
            result["conservation"] = label
            result["conservation_color"] = color
            break

    # ── Habitat — expanded to catch real Wikipedia phrasing ───────────────────
    hab_map = [
        (r'\b(coral reef|reef)\b', "Coral Reef"),
        (r'\b(deep.?sea|deep ocean|abyssal|hadal)\b', "Deep Ocean"),
        (r'\b(ocean|marine|sea|pelagic|open water)\b', "Ocean"),
        (r'\b(tropical rainforest|jungle)\b', "Tropical Rainforest"),
        (r'\b(freshwater|river|lake|pond|stream|creek|canal)\b', "Freshwater"),
        (r'\b(tundra|arctic|polar|permafrost)\b', "Arctic / Tundra"),
        (r'\b(desert|arid|xeric)\b', "Desert"),
        (r'\b(savann|grassland|prairie|steppe)\b', "Savanna / Grassland"),
        (r'\b(mountain|alpine|himalay|high.?altitude)\b', "Mountain"),
        (r'\b(rainforest|tropical forest|tropical)\b', "Tropical Forest"),
        (r'\b(forest|woodland|taiga|boreal|temperate)\b', "Forest"),
        (r'\b(wetland|marsh|swamp|mangrove|estuar)\b', "Wetland"),
        (r'\b(cave|subterranean|underground)\b', "Cave / Underground"),
        (r'\b(moss|lichen|soil|leaf litter|bark)\b', "Terrestrial / Soil"),
        (r'\b(ubiquitous|every habitat|all environment|worldwide habitat|found everywhere)\b', "Widespread"),
        (r'\b(parasit|host|endoparasit|ectoparasit)\b', "Parasitic"),
        (r'\b(xochimilco|mexico city lake)\b', "Freshwater Lake"),
        (r'\b(aquatic|water)\b', "Aquatic"),
        (r'\b(terrestrial|land)\b', "Terrestrial"),
    ]
    for pat, label in hab_map:
        if re.search(pat, t):
            result["habitat"] = label
            break

    # ── Region / Continent ───────────────────────────────────────────────────
    region_map = [
        (r'\b(africa)\b', "Africa", "Africa"),
        (r'\b(south america|amazon|brazil|peru|colombia)\b', "South America", "South America"),
        (r'\b(north america|united states|canada|mexico)\b', "North America", "North America"),
        (r'\b(australia|oceania|new zealand)\b', "Australia / Oceania", "Australia"),
        (r'\b(europe)\b', "Europe", "Europe"),
        (r'\b(southeast asia|indonesia|philippines|borneo)\b', "Southeast Asia", "Asia"),
        (r'\b(china|japan|korea)\b', "East Asia", "Asia"),
        (r'\b(india|south asia)\b', "South Asia", "Asia"),
        (r'\b(arctic|antarct)\b', "Polar Regions", "Arctic"),
        (r'\b(worldwide|global|cosmopolitan|throughout the world|all ocean)\b', "Worldwide", "Worldwide"),
    ]
    for pat, region, cont in region_map:
        if re.search(pat, t):
            result["region"] = region
            result["continent"] = cont
            break

    # ── Lifespan ─────────────────────────────────────────────────────────────
    ls = re.search(r'(?:live|lifespan|live up to|lives? (?:for )?(?:up to )?)([\d]+)(?:\s*(?:to|–|-)\s*([\d]+))?\s*years', t)
    if ls:
        lo, hi = ls.group(1), ls.group(2)
        result["lifespan_display"] = f"{lo}–{hi} years" if hi else f"~{lo} years"
        result["lifespan_years"] = int(hi or lo)

    # ── Weight ───────────────────────────────────────────────────────────────
    wt = re.search(r'weigh(?:s|ing|t)?\s+(?:up to\s+)?([\d,\.]+)\s*(kg|g|lb|ton)', t)
    if wt:
        val_str = wt.group(1).replace(",","")
        unit = wt.group(2)
        try:
            val = float(val_str)
            if unit == "g":   val /= 1000
            elif unit == "lb": val *= 0.453592
            elif unit == "ton": val *= 1000
            result["weight_kg"] = round(val, 3) if val < 1 else round(val)
            result["weight_display"] = f"{wt.group(1)} {unit}"
        except ValueError:
            pass

    # ── Speed ────────────────────────────────────────────────────────────────
    sp = re.search(r'([\d]+)\s*(?:km/h|kilometres? per hour|mph)', t)
    if sp:
        try:
            spd = float(sp.group(1))
            if "mph" in t[sp.start():sp.end()+3]:
                spd = round(spd * 1.60934)
            result["speed_kmh"] = int(spd)
        except ValueError:
            pass

    # ── Fun fact — pick the most interesting sentence ─────────────────────────
    sentences = [s.strip() for s in text.replace("\n"," ").split(". ") if len(s.strip()) > 40]
    fact_keywords = ["largest","smallest","fastest","only","unique","never","always",
                     "can","million","thousand","record","world","known","first","last"]
    best = None
    for s in sentences[1:]:   # skip the first (usually the definition)
        if any(k in s.lower() for k in fact_keywords):
            best = s.strip()
            if not best.endswith("."): best += "."
            break
    if best:
        result["fun_fact"] = best

    return result


def _emoji_for_category(cat):
    m = {
        "Fish":"🐟","Mammal":"🦁","Bird":"🐦","Reptile":"🦎",
        "Amphibian":"🐸","Insect":"🦋","Spider":"🕷️","Crustacean":"🦀",
        "Mollusca":"🐌","Cephalopod":"🐙","Worm":"🪱","Cnidarian":"🪸",
        "Invertebrate":"🦗",
    }
    for k,v in m.items():
        if k.lower() in cat.lower(): return v
    return "🐾"


def build_wiki_entry(title, summary, gbif_data=None):
    """Build a full animal data dict from Wikipedia summary + optional GBIF data."""
    desc = summary.get("extract", "")
    sentences = [s.strip() for s in desc.replace("\n"," ").split(". ") if s.strip()]
    short = ". ".join(sentences[:4])
    if short and not short.endswith("."): short += "."

    thumb = None
    if "thumbnail" in summary:
        raw = summary["thumbnail"].get("source","")
        for o,n in [("/200px-","/600px-"),("/320px-","/600px-"),("/400px-","/600px-")]:
            if o in raw: raw = raw.replace(o,n); break
        thumb = raw

    wiki_url = summary.get("content_urls",{}).get("desktop",{}).get("page","")

    # Category from Wikipedia description field e.g. "species of fish"
    wiki_desc_field = summary.get("description","")
    cat = "Animal"
    for token in ["fish","mammal","bird","reptile","amphibian","insect","spider",
                  "crustacean","mollusc","worm","cnidarian","invertebrate","cephalopod"]:
        if token in wiki_desc_field.lower() or token in desc[:200].lower():
            cat = token.title()
            break

    # Parse extract for stats
    parsed = _parse_extract(desc)

    # Taxonomy — prefer GBIF, fall back to parsed or "—"
    g = gbif_data or {}
    kingdom  = g.get("kingdom") or "Animalia"
    phylum   = g.get("phylum")  or "—"
    class_   = g.get("class_") or g.get("clazz") or "—"
    order    = g.get("order")   or "—"
    family   = g.get("family")  or "—"
    genus    = g.get("genus")   or "—"
    sci_name = g.get("species") or title  # GBIF "species" field = "Genus species"

    # Override category with GBIF class if available
    if class_ and class_ != "—":
        class_lower = class_.lower()
        class_map = {
            "mammalia":"Mammal","aves":"Bird","reptilia":"Reptile",
            "amphibia":"Amphibian","actinopterygii":"Fish","chondrichthyes":"Fish",
            "insecta":"Insect","arachnida":"Spider","malacostraca":"Crustacean",
            "cephalopoda":"Cephalopod","gastropoda":"Mollusca",
        }
        for k,v in class_map.items():
            if k in class_lower:
                cat = v; break

    emoji = _emoji_for_category(cat)

    lifespan_years   = parsed.get("lifespan_years", 0)
    lifespan_display = parsed.get("lifespan_display", "—")
    weight_kg        = parsed.get("weight_kg", 0)
    weight_display   = parsed.get("weight_display", "—")
    speed_kmh        = parsed.get("speed_kmh", 0)

    conservation       = parsed.get("conservation", "Unknown")
    conservation_color = parsed.get("conservation_color", "#64748b")
    habitat  = parsed.get("habitat", "—")
    diet     = parsed.get("diet", "—")
    region   = parsed.get("region", "—")
    continent= parsed.get("continent", "—")
    fun_fact = parsed.get("fun_fact", f"{title} is a fascinating species — explore Wikipedia for more details.")

    return {
        "emoji": emoji,
        "category": cat,
        "habitat": habitat,
        "diet": diet,
        "lifespan_years": lifespan_years,
        "lifespan_display": lifespan_display,
        "weight_kg": weight_kg,
        "weight_display": weight_display,
        "speed_kmh": speed_kmh,
        "conservation": conservation,
        "conservation_color": conservation_color,
        "region": region,
        "continent": continent,
        "scientific_name": sci_name,
        "kingdom": kingdom,
        "phylum": phylum,
        "class_": class_,
        "order": order,
        "family": family,
        "genus": genus,
        "fun_fact": fun_fact,
        "description": short or "No description available.",
        "related": [],
        "image_query": urllib.parse.quote(title.lower()),
        "wiki_url": wiki_url,
        "wiki_thumb": thumb,
        "wiki_title": title,
        "_from_wiki": True,
    }


def _is_stale(entry):
    if not entry: return True
    if entry.get("fun_fact","").startswith("Search Wikipedia or GBIF"): return True
    if entry.get("habitat","—") == "—" and entry.get("diet","—") == "—" and entry.get("region","—") == "—": return True
    return False

def load_wiki(title):
    cached = st.session_state.wiki_cache.get(title)
    if cached and not _is_stale(cached):
        return cached
    s = wiki_summary(title)
    if not s: return None
    # Try GBIF with Wikipedia's canonical title first (often the scientific name),
    # then fall back to the common name the user typed
    sci_hint = s.get("title", title)
    gbif_data = gbif_lookup(sci_hint)
    if not gbif_data:
        gbif_data = gbif_lookup(title)
    e = build_wiki_entry(title, s, gbif_data)
    st.session_state.wiki_cache[title] = e
    return e

def get_data(name):
    if name in ANIMALS: return ANIMALS[name]
    return st.session_state.wiki_cache.get(name)

def add_history(q):
    h=st.session_state.history
    if q and q not in h: h.insert(0,q)
    st.session_state.history=h[:20]

def toggle_fav(name):
    f=st.session_state.favorites
    if name in f: f.remove(name)
    else: f.insert(0,name)
    st.session_state.favorites=f[:30]

def go(page,animal=None):
    st.session_state.page=page
    if animal is not None:
        st.session_state.selected=animal
    st.rerun()

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
*{box-sizing:border-box;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{
  background:linear-gradient(160deg,#020617,#0a1628,#1a0a28)!important;
  min-height:100vh;font-family:'Outfit',sans-serif!important;
}
[data-testid="stAppViewContainer"]>.main{background:transparent!important;}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stSidebar"]{
  background:rgba(4,9,22,0.92)!important;
  border-right:1px solid rgba(255,255,255,0.06)!important;
  backdrop-filter:blur(24px);
}
#MainMenu,footer,header{visibility:hidden;}
.stars-bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;}
.star{position:absolute;border-radius:50%;background:white;animation:twinkle var(--dur,3s) ease-in-out infinite alternate;opacity:0;}
@keyframes twinkle{0%{opacity:0.08;transform:scale(0.8)}100%{opacity:0.9;transform:scale(1.3)}}
.pg{position:relative;z-index:1;padding:1.8rem 1.4rem 4rem;}
/* Page header */
.ph{text-align:center;margin-bottom:1.8rem;}
.ph h1{font-weight:800;font-size:clamp(1.8rem,4vw,3rem);letter-spacing:-.02em;
  background:linear-gradient(135deg,#e2e8f0 0%,#94a3b8 55%,#a78bfa 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  margin:0 0 .35rem;line-height:1.15;}
.ph p{font-size:.95rem;color:rgba(148,163,184,.72);font-weight:300;letter-spacing:.04em;margin:0;}
/* Glass card base */
.gc{background:rgba(13,20,40,.68);border:1px solid rgba(255,255,255,.08);
  border-radius:18px;backdrop-filter:blur(18px);}
/* Animal cards */
.ag{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:1.1rem;}
.ac{background:rgba(13,20,40,.65);border:1px solid rgba(255,255,255,.08);
  border-radius:18px;padding:1.4rem 1.1rem 1.2rem;
  backdrop-filter:blur(18px);text-align:center;
  transition:transform .22s cubic-bezier(.22,.68,0,1.2),border-color .2s,box-shadow .2s;}
.ac:hover{transform:translateY(-5px) scale(1.02);border-color:rgba(167,139,250,.42);
  box-shadow:0 0 0 1px rgba(167,139,250,.28),0 14px 44px -8px rgba(167,139,250,.22);}
.ac .em{font-size:2.6rem;margin-bottom:.55rem;display:block;}
.ac .nm{font-weight:700;font-size:1rem;color:#f1f5f9;margin:0 0 .3rem;}
.ac .cb{display:inline-block;font-size:.62rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
  background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.22);
  color:#a78bfa;padding:2px 9px;border-radius:20px;}
.ac .rg{font-size:.75rem;color:rgba(148,163,184,.55);margin-top:.4rem;font-weight:300;}
/* Detail panel */
.dw{background:rgba(9,16,38,.74);border:1px solid rgba(255,255,255,.1);
  border-radius:24px;padding:2.2rem;
  backdrop-filter:blur(24px);position:relative;overflow:hidden;margin-bottom:1.8rem;}
.dg{position:absolute;top:-50px;right:-50px;width:200px;height:200px;border-radius:50%;
  background:radial-gradient(circle,rgba(167,139,250,.22) 0%,transparent 70%);pointer-events:none;}
.dn{font-weight:800;font-size:2.2rem;color:#f1f5f9;letter-spacing:-.02em;margin:0 0 .3rem;}
.dd{font-size:.92rem;color:rgba(148,163,184,.85);line-height:1.72;font-weight:300;margin:.9rem 0 1.3rem;}
.ff{background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.22);
  border-radius:12px;padding:.9rem 1.1rem;margin-bottom:1.3rem;}
.ff .lb{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#a78bfa;margin-bottom:.25rem;}
.ff .tx{font-size:.9rem;color:#e2e8f0;line-height:1.6;}
.sg{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;margin-top:.8rem;}
.sc{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:.8rem .85rem;}
.sl{font-size:.65rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:rgba(148,163,184,.52);margin-bottom:.22rem;}
.sv{font-size:.88rem;font-weight:600;color:#e2e8f0;}
.conbadge{display:inline-block;font-size:.7rem;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;padding:3px 11px;border-radius:20px;border:1px solid;}
/* Classification table */
.clf{background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.15);
  border-radius:14px;padding:1rem 1.2rem;margin-top:1rem;}
.clf table{width:100%;border-collapse:collapse;}
.clf td{padding:.32rem .5rem;font-size:.84rem;border-bottom:1px solid rgba(255,255,255,.04);}
.clf td:first-child{color:rgba(148,163,184,.55);font-weight:600;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;width:38%;}
.clf td:last-child{color:#e2e8f0;font-style:italic;}
/* GBIF panel */
.gbif{background:rgba(52,211,153,.06);border:1px solid rgba(52,211,153,.2);
  border-radius:14px;padding:1rem 1.2rem;margin-top:1rem;}
.gbif h4{font-size:.82rem;font-weight:700;color:#34d399;letter-spacing:.08em;text-transform:uppercase;margin:0 0 .5rem;}
.gbif p{font-size:.82rem;color:rgba(148,163,184,.8);margin:0;}
/* Photo grid */
.slbl{font-weight:700;font-size:1.05rem;color:#e2e8f0;margin:1.5rem 0 .65rem;display:flex;align-items:center;gap:.4rem;}
/* Related species chips */
.rc{display:inline-block;background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.22);
  border-radius:20px;padding:4px 14px;font-size:.8rem;color:#a78bfa;
  margin:3px;cursor:pointer;transition:background .2s;}
.rc:hover{background:rgba(167,139,250,.22);}
/* Wiki banner */
.wb{background:rgba(56,189,248,.07);border:1px solid rgba(56,189,248,.2);
  border-radius:12px;padding:.7rem 1rem;margin-bottom:.9rem;font-size:.8rem;color:rgba(147,210,250,.85);}
/* Free search box */
.fsb{background:rgba(13,20,40,.72);border:1px solid rgba(167,139,250,.26);
  border-radius:20px;padding:1.3rem 1.5rem .9rem;
  backdrop-filter:blur(20px);margin-bottom:1.4rem;}
.fsb h3{font-weight:700;font-size:1rem;color:#e2e8f0;margin:0 0 .65rem;}
/* Quiz & Game */
.qcard{background:rgba(13,20,40,.72);border:1px solid rgba(167,139,250,.2);
  border-radius:20px;padding:1.8rem;backdrop-filter:blur(18px);margin-bottom:1.2rem;}
.qcard h2{font-weight:800;font-size:1.5rem;color:#f1f5f9;margin:0 0 .6rem;}
.qcard p{color:rgba(148,163,184,.8);font-size:.9rem;margin:0 0 1.2rem;}
.ans-btn{width:100%;background:rgba(255,255,255,.05)!important;
  border:1px solid rgba(255,255,255,.12)!important;
  color:#e2e8f0!important;border-radius:12px!important;
  font-family:'Outfit',sans-serif!important;font-size:.9rem!important;
  padding:.6rem!important;margin:.3rem 0!important;
  transition:all .18s!important;text-align:left!important;}
.ans-btn:hover{background:rgba(167,139,250,.18)!important;border-color:rgba(167,139,250,.4)!important;}
.correct{background:rgba(52,211,153,.18)!important;border-color:#34d399!important;color:#34d399!important;}
.wrong{background:rgba(239,68,68,.15)!important;border-color:#ef4444!important;color:#ef4444!important;}
/* Stat bars */
.bar-wrap{margin:.5rem 0;}
.bar-bg{background:rgba(255,255,255,.07);border-radius:20px;height:8px;overflow:hidden;margin-top:.25rem;}
.bar-fill{height:100%;border-radius:20px;background:linear-gradient(90deg,#a78bfa,#60a5fa);transition:width .6s ease;}
/* Guess game hints */
.hint-card{background:rgba(13,20,40,.65);border:1px solid rgba(255,255,255,.08);
  border-radius:14px;padding:.9rem 1.1rem;margin:.4rem 0;font-size:.9rem;color:#e2e8f0;}
.hint-hidden{filter:blur(8px);user-select:none;color:rgba(148,163,184,.4);}
/* Conservation explorer */
.con-bar{display:flex;align-items:center;gap:.8rem;margin:.5rem 0;}
.con-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0;}
/* Sidebar nav */
[data-testid="stSidebar"] *{font-family:'Outfit',sans-serif!important;}
[data-testid="stSidebar"] h2{color:#f1f5f9!important;font-weight:700!important;font-size:1.05rem!important;}
[data-testid="stSidebar"] p{color:rgba(148,163,184,.7)!important;font-size:.8rem!important;}
[data-testid="stSidebar"] label{color:rgba(148,163,184,.6)!important;font-size:.78rem!important;text-transform:uppercase!important;letter-spacing:.06em!important;}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox>div>div{
  background:rgba(13,20,40,.75)!important;border:1px solid rgba(255,255,255,.1)!important;
  border-radius:10px!important;color:#e2e8f0!important;font-family:'Outfit',sans-serif!important;}
.stButton>button{
  background:rgba(167,139,250,.14)!important;border:1px solid rgba(167,139,250,.28)!important;
  color:#a78bfa!important;border-radius:10px!important;
  font-family:'Outfit',sans-serif!important;font-weight:600!important;transition:all .18s!important;}
.stButton>button:hover{background:rgba(167,139,250,.26)!important;border-color:#a78bfa!important;}
div[data-testid="column"] .stButton>button{width:100%;}
.stTabs [data-baseweb="tab"]{font-family:'Outfit',sans-serif!important;color:rgba(148,163,184,.65)!important;}
.stTabs [aria-selected="true"]{color:#a78bfa!important;}
.stTabs [data-baseweb="tab-highlight"]{background:#a78bfa!important;}
hr{border-color:rgba(255,255,255,.06)!important;}
</style>
<div class="stars-bg" id="sc"></div>
<script>
(function(){
  var c=document.getElementById('sc');if(!c)return;
  for(var i=0;i<140;i++){
    var s=document.createElement('div');s.className='star';
    var sz=Math.random()*2.4+0.4;
    s.style.cssText='width:'+sz+'px;height:'+sz+'px;left:'+(Math.random()*100)+'%;top:'+(Math.random()*100)+'%;--dur:'+(Math.random()*3+2)+'s;animation-delay:'+(Math.random()*5)+'s';
    c.appendChild(s);
  }
})();
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🐾 Animal Encyclopedia")
    st.markdown("The ultimate guide to Earth's wildlife.")
    st.markdown("---")
    # Navigation
    st.markdown("### 🗺️ Navigation")
    nav_items = [
        ("🏠 Home",          "home"),
        ("🔭 Explorer",      "explorer"),
        ("🌿 Habitat Map",   "habitat"),
        ("🛡️ Conservation",  "conservation"),
        ("📊 Statistics",    "stats"),
        ("🎓 Animal Quiz",   "quiz"),
        ("🕵️ Guess the Animal","guess"),
    ]
    for label, page_key in nav_items:
        if st.button(label, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.session_state.selected = None
            st.rerun()

    st.markdown("---")
    # AOTD
    rng=random.Random(int(datetime.date.today().strftime("%Y%m%d")))
    AOTD=rng.choice(list(ANIMALS.keys()))
    st.markdown(f"### 🏆 Animal of the Day")
    st.markdown(f"**{ANIMALS[AOTD]['emoji']} {AOTD}**")
    if st.button("View →", key="aotd"):
        st.session_state.selected=AOTD; st.session_state.page="detail"; st.rerun()

    st.markdown("---")
    if st.button("🎲 Random Animal", key="rand"):
        st.session_state.selected=random.choice(list(ANIMALS.keys()))
        st.session_state.page="detail"; st.rerun()

    st.markdown("---")
    st.markdown("### ⭐ Favorites")
    if st.session_state.favorites:
        for fav in st.session_state.favorites[:8]:
            em = ANIMALS.get(fav,{}).get("emoji","🐾")
            if st.button(f"{em} {fav}", key=f"fav_{fav}"):
                st.session_state.selected=fav; st.session_state.page="detail"; st.rerun()
    else:
        st.markdown('<p style="color:rgba(148,163,184,0.38);font-size:.78rem;">No favorites yet.</p>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🕐 Recent")
    for h in st.session_state.history[:5]:
        st.markdown(f'<span style="font-size:.76rem;color:rgba(148,163,184,.42);">• {h}</span>', unsafe_allow_html=True)

    if st.session_state.page not in ("home","explorer","habitat","conservation","stats","quiz","guess"):
        st.markdown("---")
        if st.button("← Back", key="back_sb"):
            st.session_state.page="home"; st.session_state.selected=None; st.rerun()

# ══════════════════════════════════════════════════════════════
# PAGE: DETAIL
# ══════════════════════════════════════════════════════════════
def page_detail():
    name=st.session_state.selected
    if not name:
        go("home"); return
    data=get_data(name)
    if data is None:
        with st.spinner(f"Loading {name}…"):
            data=load_wiki(name)
    if not data:
        st.error(f"Could not load '{name}'. Please go back.")
        if st.button("← Home"): go("home")
        return

    st.markdown('<div class="pg">', unsafe_allow_html=True)
    from_wiki=data.get("_from_wiki",False)
    con_color=data.get("conservation_color","#64748b")
    is_fav=name in st.session_state.favorites

    if from_wiki:
        wu=data.get("wiki_url","")
        lnk=f'<a href="{wu}" target="_blank" style="color:#38bdf8;text-decoration:none;">Read on Wikipedia ↗</a>' if wu else ""
        st.markdown(f'<div class="wb">📖 Live data from Wikipedia. {lnk}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dw">
      <div class="dg"></div>
      <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;margin-bottom:.4rem;">
        <span style="font-size:3.2rem;line-height:1;">{data['emoji']}</span>
        <div>
          <div class="dn">{name}</div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
            <span style="font-size:.72rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:rgba(148,163,184,.55);">{data['category']} · {data.get('region','—')}</span>
            <span class="conbadge" style="color:{con_color};border-color:{con_color}44;background:{con_color}14;">{data['conservation']}</span>
          </div>
          <div style="font-size:.82rem;color:rgba(148,163,184,.5);font-style:italic;margin-top:.25rem;">{data.get('scientific_name','—')}</div>
        </div>
      </div>
      <p class="dd">{data['description']}</p>
      <div class="ff"><div class="lb">✦ Did you know?</div><div class="tx">{data['fun_fact']}</div></div>
      <div class="sg">
        <div class="sc"><div class="sl">Habitat</div><div class="sv">{data.get('habitat') or '—'}</div></div>
        <div class="sc"><div class="sl">Diet</div><div class="sv">{data.get('diet') or '—'}</div></div>
        <div class="sc"><div class="sl">Lifespan</div><div class="sv">{data.get('lifespan_display') or (str(data['lifespan_years'])+' yrs' if data.get('lifespan_years') else '—')}</div></div>
        <div class="sc"><div class="sl">Weight</div><div class="sv">{data.get('weight_display') or (str(data['weight_kg'])+' kg' if data.get('weight_kg') else '—')}</div></div>
        <div class="sc"><div class="sl">Top Speed</div><div class="sv">{str(data['speed_kmh'])+' km/h' if data.get('speed_kmh') else '—'}</div></div>
        <div class="sc"><div class="sl">Region</div><div class="sv">{data.get('region') or '—'}</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons
    c1,c2,c3=st.columns([1,1,2])
    with c1:
        if st.button("★ Unfav" if is_fav else "☆ Favorite", key="fav_btn"):
            toggle_fav(name); st.rerun()
    with c2:
        if st.button("🏠 Home", key="home_btn"):
            go("home")

    # ── Tabs ──────────────────────────────────────────────────
    tabs=st.tabs(["📸 Photos","🧬 Classification","🌐 GBIF Data","🔗 Related Species"])

    with tabs[0]:
        wiki_title=data.get("wiki_title",name)
        thumb=data.get("wiki_thumb")
        if not thumb:
            s2=wiki_summary(wiki_title)
            if "thumbnail" in s2:
                raw=s2["thumbnail"].get("source","")
                for o,n in [("/200px-","/600px-"),("/320px-","/600px-")]:
                    if o in raw: raw=raw.replace(o,n); break
                thumb=raw
        if thumb:
            st.markdown(f'<img src="{thumb}" style="width:100%;max-width:560px;border-radius:16px;border:1px solid rgba(255,255,255,.1);display:block;margin-bottom:.5rem;" alt="{name}">', unsafe_allow_html=True)
            st.markdown('<p style="font-size:.7rem;color:rgba(148,163,184,.32);margin-bottom:.8rem;">📷 via Wikipedia</p>', unsafe_allow_html=True)
        imgs=wiki_images(wiki_title)
        resolved=[]
        for ft in imgs:
            u=resolve_img(ft)
            if u and any(u.lower().endswith(x) for x in (".jpg",".jpeg",".png",".webp")):
                resolved.append(u)
            if len(resolved)>=3: break
        if resolved:
            cols=st.columns(len(resolved))
            for i,u in enumerate(resolved):
                with cols[i]:
                    st.markdown(f'<img src="{u}" style="width:100%;border-radius:10px;border:1px solid rgba(255,255,255,.07);" alt="photo">', unsafe_allow_html=True)
        ddg=f"https://duckduckgo.com/?q={urllib.parse.quote(name+' animal')}&iax=images&ia=images"
        st.markdown(f'<a href="{ddg}" target="_blank" style="display:inline-block;margin-top:.8rem;font-size:.83rem;color:#a78bfa;text-decoration:none;background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);padding:5px 13px;border-radius:10px;">🔍 More {name} photos ↗</a>', unsafe_allow_html=True)

    with tabs[1]:
        sci=data.get("scientific_name","—")
        st.markdown(f"""
        <div class="clf">
          <table>
            <tr><td>Kingdom</td><td>{data.get('kingdom','Animalia')}</td></tr>
            <tr><td>Phylum</td><td>{data.get('phylum','—')}</td></tr>
            <tr><td>Class</td><td>{data.get('class_','—')}</td></tr>
            <tr><td>Order</td><td>{data.get('order','—')}</td></tr>
            <tr><td>Family</td><td>{data.get('family','—')}</td></tr>
            <tr><td>Genus</td><td>{data.get('genus','—')}</td></tr>
            <tr><td>Scientific Name</td><td>{sci}</td></tr>
          </table>
        </div>""", unsafe_allow_html=True)

    with tabs[2]:
        sci_name=data.get("scientific_name","")
        if sci_name and sci_name not in ("—","Dendrobatidae (family)"):
            with st.spinner("Fetching GBIF data…"):
                gbif=gbif_lookup(sci_name)
            if gbif:
                occ=gbif.get("occurrence_count",0)
                occ_str=f"{occ:,}" if occ else "Unknown"
                st.markdown(f"""
                <div class="gbif">
                  <h4>🌐 GBIF — Global Biodiversity Information Facility</h4>
                  <p><b>Recorded observations:</b> {occ_str} occurrences worldwide</p>
                  <p><b>GBIF Status:</b> {gbif.get('status','—')}</p>
                  <p style="margin-top:.5rem;"><a href="{gbif.get('gbif_url','')}" target="_blank" style="color:#34d399;text-decoration:none;">View on GBIF ↗</a></p>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="gbif"><h4>🌐 GBIF</h4><p>No GBIF data found for this species.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="gbif"><h4>🌐 GBIF</h4><p>Scientific name required for GBIF lookup. Not available for this entry.</p></div>', unsafe_allow_html=True)

    with tabs[3]:
        related=data.get("related",[])
        if related:
            st.markdown('<div style="margin:.4rem 0 .8rem;">', unsafe_allow_html=True)
            cols=st.columns(min(len(related),3))
            for i,rel in enumerate(related):
                if rel in ANIMALS:
                    rd=ANIMALS[rel]
                    with cols[i%3]:
                        if st.button(f"{rd['emoji']} {rel}", key=f"rel_{rel}_{name}"):
                            st.session_state.selected=rel; add_history(rel); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:rgba(148,163,184,.45);font-size:.85rem;">No related species data available.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════
def page_home():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown("""
    <div class="ph">
      <h1>🐾 Animal Encyclopedia</h1>
      <p>Search any animal on Earth — powered by Wikipedia & GBIF</p>
    </div>""", unsafe_allow_html=True)

    # Free search
    st.markdown('<div class="fsb"><h3>🔎 Search Any Animal</h3></div>', unsafe_allow_html=True)
    ci,cb=st.columns([5,1])
    with ci:
        q=st.text_input("fs","",label_visibility="collapsed",
            placeholder="Axolotl, Tardigrade, Narwhal, Pangolin, Quokka, Platypus…",key="fs_inp")
    with cb:
        do_s=st.button("Search →",key="fs_go")
    if do_s and q.strip():
        sq=q.strip(); st.session_state.free_query=sq; add_history(sq)
        with st.spinner(f"Searching for '{sq}'…"):
            st.session_state.free_results=wiki_search(sq)

    if st.session_state.free_results:
        res=st.session_state.free_results
        st.markdown(f'<p style="font-size:.82rem;color:rgba(148,163,184,.55);margin:.3rem 0 .5rem;">Found <b style="color:#a78bfa;">{len(res)}</b> results for "{st.session_state.free_query}"</p>', unsafe_allow_html=True)
        nc=min(len(res),4); cols=st.columns(nc)
        for i,title in enumerate(res):
            with cols[i%nc]:
                if st.button(f"🐾 {title}",key=f"wr{i}"):
                    with st.spinner(f"Loading {title}…"):
                        e=load_wiki(title)
                    if e:
                        st.session_state.selected=title; st.session_state.page="detail"; add_history(title); st.rerun()
                    else:
                        st.error(f"Could not load '{title}'.")
        if st.button("✕ Clear",key="clr"):
            st.session_state.free_results=[]; st.session_state.free_query=""; st.rerun()

    # Sidebar browse filters
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:.8rem;color:rgba(148,163,184,.42);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.8rem;">📚 Curated Collection</p>', unsafe_allow_html=True)

    fc1,fc2,fc3,fc4=st.columns(4)
    with fc1: cat_f=st.selectbox("Category",CATEGORIES,key="hcat")
    with fc2: cont_f=st.selectbox("Continent",CONTINENTS,key="hcont")
    with fc3: diet_f=st.selectbox("Diet",DIETS,key="hdiet")
    with fc4: sort_f=st.selectbox("Sort",["Name A–Z","Conservation","Fastest","Heaviest"],key="hsort")

    animals=dict(ANIMALS)
    if cat_f!="All":  animals={k:v for k,v in animals.items() if v["category"]==cat_f}
    if cont_f!="All": animals={k:v for k,v in animals.items() if v["continent"]==cont_f}
    if diet_f!="All": animals={k:v for k,v in animals.items() if v["diet"]==diet_f}
    if sort_f=="Name A–Z":    animals=dict(sorted(animals.items()))
    elif sort_f=="Conservation": animals=dict(sorted(animals.items(),key=lambda x:CONSERVATION_ORDER.get(x[1]["conservation"],9)))
    elif sort_f=="Fastest":   animals=dict(sorted(animals.items(),key=lambda x:-x[1].get("speed_kmh",0)))
    elif sort_f=="Heaviest":  animals=dict(sorted(animals.items(),key=lambda x:-x[1].get("weight_kg",0)))

    if not animals:
        st.markdown('<p style="text-align:center;color:rgba(148,163,184,.4);padding:3rem;">No animals match.</p>', unsafe_allow_html=True)
    else:
        cards='<div class="ag">'
        for n,d in animals.items():
            cc=d.get("conservation_color","#64748b")
            cards+=f'<div class="ac"><span class="em">{d["emoji"]}</span><div class="nm">{n}</div><div class="cb">{d["category"]}</div><div class="rg">📍 {d["region"]}</div><div style="margin-top:.4rem;"><span style="font-size:.65rem;font-weight:700;color:{cc};background:{cc}18;border:1px solid {cc}44;padding:2px 8px;border-radius:12px;">{d["conservation"]}</span></div></div>'
        cards+='</div>'
        st.markdown(cards,unsafe_allow_html=True)
        st.markdown("<div style='margin-top:.9rem;'></div>",unsafe_allow_html=True)
        bcols=st.columns(4)
        for i,(n,d) in enumerate(animals.items()):
            with bcols[i%4]:
                if st.button(f"{d['emoji']} {n}",key=f"g_{n}"):
                    st.session_state.selected=n; st.session_state.page="detail"; add_history(n); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: EXPLORER (multi-filter)
# ══════════════════════════════════════════════════════════════
def page_explorer():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><h1>🔭 Animal Explorer</h1><p>Filter by continent, diet, size, speed, lifespan & conservation</p></div>', unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)
    with c1:
        cont=st.selectbox("Continent",CONTINENTS,key="ex_cont")
        diet=st.selectbox("Diet",DIETS,key="ex_diet")
    with c2:
        cons=st.selectbox("Conservation",CONSERVATION_STATUSES,key="ex_cons")
        cat_=st.selectbox("Category",CATEGORIES,key="ex_cat")
    with c3:
        max_w=st.slider("Max Weight (kg)",10,200000,200000,step=1000,key="ex_w")
        max_s=st.slider("Max Speed (km/h)",1,200,200,key="ex_s")
    max_l=st.slider("Max Lifespan (years)",1,100,100,key="ex_l")

    filtered={k:v for k,v in ANIMALS.items()
              if (cont=="All" or v["continent"]==cont)
              and (diet=="All" or v["diet"]==diet)
              and (cons=="All" or v["conservation"]==cons)
              and (cat_=="All" or v["category"]==cat_)
              and v.get("weight_kg",0)<=max_w
              and v.get("speed_kmh",0)<=max_s
              and v.get("lifespan_years",0)<=max_l}

    st.markdown(f'<p style="font-size:.84rem;color:rgba(148,163,184,.55);margin:.3rem 0 .8rem;"><b style="color:#a78bfa;">{len(filtered)}</b> animals match your filters</p>', unsafe_allow_html=True)

    if not filtered:
        st.markdown('<p style="text-align:center;color:rgba(148,163,184,.4);padding:2rem;">No animals match. Try relaxing the filters.</p>', unsafe_allow_html=True)
    else:
        cards='<div class="ag">'
        for n,d in filtered.items():
            cc=d.get("conservation_color","#64748b")
            cards+=f'<div class="ac"><span class="em">{d["emoji"]}</span><div class="nm">{n}</div><div class="cb">{d["category"]}</div><div class="rg">📍 {d["region"]}</div><div style="margin-top:.4rem;font-size:.72rem;color:rgba(148,163,184,.6);">⚡ {d.get("speed_kmh","?")} km/h · {d.get("weight_kg","?")} kg</div></div>'
        cards+='</div>'
        st.markdown(cards,unsafe_allow_html=True)
        st.markdown("<div style='margin-top:.9rem;'></div>",unsafe_allow_html=True)
        bc=st.columns(4)
        for i,(n,d) in enumerate(filtered.items()):
            with bc[i%4]:
                if st.button(f"{d['emoji']} {n}",key=f"ex_{n}"):
                    st.session_state.selected=n; st.session_state.page="detail"; add_history(n); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: HABITAT EXPLORER
# ══════════════════════════════════════════════════════════════
def page_habitat():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><h1>🌿 Habitat Explorer</h1><p>Discover animals by where they live</p></div>', unsafe_allow_html=True)

    habitats={
        "🌊 Ocean": ["Blue Whale","Manta Ray","Octopus"],
        "🌿 Rainforest": ["Poison Dart Frog","Gorilla"],
        "🏔️ Mountains": ["Snow Leopard"],
        "🌾 Savanna": ["Lion","Cheetah","Elephant"],
        "❄️ Arctic / Antarctic": ["Arctic Fox","Emperor Penguin","Polar Bear"],
        "🌲 Forest": ["Bald Eagle","Tiger","Giant Panda"],
        "🏝️ Islands": ["Komodo Dragon"],
    }
    habitat_descs={
        "🌊 Ocean": "Covering 71% of Earth's surface, oceans are home to the largest and most diverse array of life.",
        "🌿 Rainforest": "Tropical rainforests cover just 6% of land but host over 50% of species.",
        "🏔️ Mountains": "Harsh, high-altitude environments demand extreme adaptations from their residents.",
        "🌾 Savanna": "Wide grasslands with seasonal rains, supporting iconic African and Asian megafauna.",
        "❄️ Arctic / Antarctic": "Polar regions demand supreme cold-tolerance; few species thrive, but those that do are extraordinary.",
        "🌲 Forest": "Temperate and boreal forests provide rich ecosystems for predators and prey alike.",
        "🏝️ Islands": "Island isolation drives unique evolution, often producing species found nowhere else.",
    }

    for hab, members in habitats.items():
        with st.expander(f"{hab}  —  {len(members)} animals", expanded=False):
            st.markdown(f'<p style="font-size:.85rem;color:rgba(148,163,184,.7);margin-bottom:.8rem;">{habitat_descs.get(hab,"")}</p>', unsafe_allow_html=True)
            if members:
                hcols=st.columns(min(len(members),4))
                for i,m in enumerate(members):
                    if m in ANIMALS:
                        d=ANIMALS[m]
                        with hcols[i%4]:
                            st.markdown(f'<div class="ac" style="padding:1rem;"><span class="em">{d["emoji"]}</span><div class="nm">{m}</div><div class="cb">{d["category"]}</div></div>', unsafe_allow_html=True)
                            if st.button(f"View {m}",key=f"hab_{hab}_{m}"):
                                st.session_state.selected=m; st.session_state.page="detail"; add_history(m); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: CONSERVATION EXPLORER
# ══════════════════════════════════════════════════════════════
def page_conservation():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><h1>🛡️ Conservation Status Explorer</h1><p>Understand the IUCN Red List and what it means for wildlife</p></div>', unsafe_allow_html=True)

    status_info={
        "Least Concern":      ("#34d399","LC","Species evaluated and found to be at low risk."),
        "Near Threatened":    ("#facc15","NT","Close to qualifying as threatened in the near future."),
        "Vulnerable":         ("#fb923c","VU","Facing high risk of extinction in the wild."),
        "Endangered":         ("#ef4444","EN","Facing a very high risk of extinction in the wild."),
        "Critically Endangered":("#dc2626","CR","Facing an extremely high risk of extinction."),
    }
    for status,(color,code,desc) in status_info.items():
        members=[n for n,d in ANIMALS.items() if d["conservation"]==status]
        st.markdown(f"""
        <div class="gc" style="padding:1.2rem 1.4rem;margin-bottom:1rem;">
          <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.5rem;">
            <span style="width:14px;height:14px;border-radius:50%;background:{color};display:inline-block;flex-shrink:0;"></span>
            <span style="font-weight:700;font-size:1rem;color:{color};">{status}</span>
            <span style="font-size:.72rem;font-weight:700;letter-spacing:.1em;color:{color};background:{color}18;border:1px solid {color}44;padding:2px 9px;border-radius:12px;">{code}</span>
            <span style="font-size:.78rem;color:rgba(148,163,184,.55);margin-left:auto;">{len(members)} in our database</span>
          </div>
          <p style="font-size:.84rem;color:rgba(148,163,184,.7);margin:0 0 .6rem;">{desc}</p>
        </div>""", unsafe_allow_html=True)
        if members:
            bc=st.columns(min(len(members),4))
            for i,m in enumerate(members):
                with bc[i%4]:
                    em=ANIMALS[m]["emoji"]
                    if st.button(f"{em} {m}",key=f"con_{status}_{m}"):
                        st.session_state.selected=m; st.session_state.page="detail"; add_history(m); st.rerun()

    st.markdown("""
    <div class="gc" style="padding:1.2rem 1.4rem;margin-top:1rem;">
      <p style="font-size:.83rem;color:rgba(148,163,184,.6);margin:0;">
      ℹ️ Data based on the <b style="color:#e2e8f0;">IUCN Red List of Threatened Species</b>.
      Statuses are approximate and may not reflect the most recent assessment.
      Visit <a href="https://www.iucnredlist.org" target="_blank" style="color:#a78bfa;">iucnredlist.org</a> for authoritative data.
      </p>
    </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: STATISTICS DASHBOARD
# ══════════════════════════════════════════════════════════════
def page_stats():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><h1>📊 Statistics Dashboard</h1><p>Insights and records from our animal database</p></div>', unsafe_allow_html=True)

    animals=ANIMALS

    # Summary cards
    total=len(animals)
    endangered_count=sum(1 for a in animals.values() if a["conservation"] in ("Endangered","Critically Endangered"))
    categories=len(set(a["category"] for a in animals.values()))
    heaviest=max(animals,key=lambda k:animals[k].get("weight_kg",0))
    fastest=max(animals,key=lambda k:animals[k].get("speed_kmh",0))
    oldest=max(animals,key=lambda k:animals[k].get("lifespan_years",0))

    c1,c2,c3,c4=st.columns(4)
    for col,icon,val,lbl in [(c1,"🐾",total,"Total Animals"),(c2,"🚨",endangered_count,"Endangered / CR"),(c3,"🧬",categories,"Categories"),(c4,"🌍",len(set(a["continent"] for a in animals.values())),"Continents")]:
        with col:
            st.markdown(f"""
            <div class="gc" style="padding:1.1rem;text-align:center;margin-bottom:1rem;">
              <div style="font-size:1.8rem;">{icon}</div>
              <div style="font-size:2rem;font-weight:800;color:#f1f5f9;">{val}</div>
              <div style="font-size:.75rem;color:rgba(148,163,184,.55);text-transform:uppercase;letter-spacing:.08em;">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # Records
    st.markdown('<div class="slbl">🏆 Records</div>', unsafe_allow_html=True)
    rc1,rc2,rc3=st.columns(3)
    for col,icon,lbl,name,val in [
        (rc1,"⚡","Fastest",fastest,f"{animals[fastest]['speed_kmh']} km/h"),
        (rc2,"⚖️","Heaviest",heaviest,f"{animals[heaviest]['weight_kg']:,} kg"),
        (rc3,"⏳","Longest Lived",oldest,f"{animals[oldest]['lifespan_years']} years"),
    ]:
        with col:
            d=animals[name]
            st.markdown(f"""
            <div class="gc" style="padding:1.1rem;text-align:center;margin-bottom:1rem;">
              <div style="font-size:.72rem;color:rgba(148,163,184,.5);text-transform:uppercase;letter-spacing:.08em;margin-bottom:.3rem;">{icon} {lbl}</div>
              <div style="font-size:2rem;">{d['emoji']}</div>
              <div style="font-weight:700;color:#f1f5f9;">{name}</div>
              <div style="font-size:.85rem;color:#a78bfa;font-weight:600;">{val}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"View {name}",key=f"rec_{name}"):
                st.session_state.selected=name; st.session_state.page="detail"; add_history(name); st.rerun()

    # Speed comparison bar chart
    st.markdown('<div class="slbl">⚡ Speed Comparison</div>', unsafe_allow_html=True)
    by_speed=sorted(animals.items(),key=lambda x:-x[1].get("speed_kmh",0))
    max_spd=by_speed[0][1]["speed_kmh"]
    st.markdown('<div class="gc" style="padding:1.2rem 1.5rem;">', unsafe_allow_html=True)
    for n,d in by_speed:
        spd=d.get("speed_kmh",0); pct=int(spd/max_spd*100) if max_spd else 0
        st.markdown(f"""
        <div class="bar-wrap">
          <div style="display:flex;justify-content:space-between;font-size:.82rem;">
            <span style="color:#e2e8f0;">{d['emoji']} {n}</span>
            <span style="color:#a78bfa;font-weight:600;">{spd} km/h</span>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;"></div></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Weight comparison
    st.markdown('<div class="slbl">⚖️ Weight Comparison (log scale)</div>', unsafe_allow_html=True)
    by_weight=sorted(animals.items(),key=lambda x:-x[1].get("weight_kg",0))
    max_log=math.log10(max(d.get("weight_kg",1) for d in animals.values())+1)
    st.markdown('<div class="gc" style="padding:1.2rem 1.5rem;">', unsafe_allow_html=True)
    for n,d in by_weight:
        wt=d.get("weight_kg",0); pct=int(math.log10(wt+1)/max_log*100) if wt else 1
        wt_str=f"{wt:,} kg" if wt>=1 else f"{wt*1000:.0f} g"
        st.markdown(f"""
        <div class="bar-wrap">
          <div style="display:flex;justify-content:space-between;font-size:.82rem;">
            <span style="color:#e2e8f0;">{d['emoji']} {n}</span>
            <span style="color:#60a5fa;font-weight:600;">{wt_str}</span>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#60a5fa,#34d399);"></div></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Category breakdown
    st.markdown('<div class="slbl">🧬 Category Breakdown</div>', unsafe_allow_html=True)
    cat_counts={}
    for d in animals.values():
        cat_counts[d["category"]]=cat_counts.get(d["category"],0)+1
    cat_counts=dict(sorted(cat_counts.items(),key=lambda x:-x[1]))
    max_c=max(cat_counts.values())
    st.markdown('<div class="gc" style="padding:1.2rem 1.5rem;">', unsafe_allow_html=True)
    for cat,count in cat_counts.items():
        pct=int(count/max_c*100)
        st.markdown(f"""
        <div class="bar-wrap">
          <div style="display:flex;justify-content:space-between;font-size:.82rem;">
            <span style="color:#e2e8f0;">{cat}</span>
            <span style="color:#a78bfa;font-weight:600;">{count}</span>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#a78bfa,#f472b6);"></div></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: QUIZ
# ══════════════════════════════════════════════════════════════
QUIZ_QUESTIONS_POOL = [
    {"q":"Which animal has the largest brain-to-body ratio of any cold-blooded fish?","a":"Manta Ray","opts":["Manta Ray","Octopus","Blue Whale","Bald Eagle"]},
    {"q":"What is the fastest land animal on Earth?","a":"Cheetah","opts":["Cheetah","Lion","Bald Eagle","Tiger"]},
    {"q":"Which animal's heart can weigh up to 400 kg?","a":"Blue Whale","opts":["Blue Whale","Elephant","Polar Bear","Gorilla"]},
    {"q":"What unique sound does a snow leopard make instead of roaring?","a":"A 'chuff'","opts":["A 'chuff'","A bark","A hiss","A chirp"]},
    {"q":"How many hearts does an octopus have?","a":"Three","opts":["One","Two","Three","Four"]},
    {"q":"Which penguin species incubates its egg through the Antarctic winter?","a":"Emperor Penguin","opts":["Emperor Penguin","King Penguin","Rockhopper Penguin","Chinstrap Penguin"]},
    {"q":"What percentage of DNA do gorillas share with humans?","a":"98.3%","opts":["85%","92%","98.3%","99.9%"]},
    {"q":"What is the scientific name of the lion?","a":"Panthera leo","opts":["Panthera leo","Acinonyx jubatus","Panthera tigris","Panthera uncia"]},
    {"q":"How far can a lion's roar be heard?","a":"8 km","opts":["2 km","5 km","8 km","15 km"]},
    {"q":"Which animal can withstand temperatures as low as −70°C?","a":"Arctic Fox","opts":["Arctic Fox","Polar Bear","Emperor Penguin","Snow Leopard"]},
    {"q":"What does the Komodo dragon use to detect prey from 9.5 km away?","a":"Its forked tongue","opts":["Its forked tongue","Its eyes","Its ears","Heat pits"]},
    {"q":"How many kg of bamboo does a giant panda eat per day?","a":"12–38 kg","opts":["1–5 kg","12–38 kg","50–70 kg","5–10 kg"]},
    {"q":"What is the top speed of a cheetah?","a":"120 km/h","opts":["80 km/h","100 km/h","120 km/h","150 km/h"]},
    {"q":"Which animal has nine brains?","a":"Octopus","opts":["Octopus","Manta Ray","Komodo Dragon","Blue Whale"]},
    {"q":"The bald eagle is the national bird of which country?","a":"United States","opts":["United States","Canada","Mexico","Australia"]},
]

def generate_quiz():
    qs=random.sample(QUIZ_QUESTIONS_POOL, min(10, len(QUIZ_QUESTIONS_POOL)))
    for q in qs: random.shuffle(q["opts"])
    return qs

def page_quiz():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><h1>🎓 Animal Quiz</h1><p>Test your wildlife knowledge — 10 questions</p></div>', unsafe_allow_html=True)

    if not st.session_state.quiz_questions:
        st.markdown("""
        <div class="qcard" style="text-align:center;">
          <h2>Ready to test your knowledge?</h2>
          <p>10 randomised questions about the animal kingdom. Good luck!</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Start Quiz", key="start_quiz"):
            st.session_state.quiz_questions=generate_quiz()
            st.session_state.quiz_q=0; st.session_state.quiz_score=0
            st.session_state.quiz_answered=False; st.session_state.quiz_selected=None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    qs=st.session_state.quiz_questions
    qi=st.session_state.quiz_q

    # Finished
    if qi>=len(qs):
        score=st.session_state.quiz_score; total=len(qs)
        pct=int(score/total*100)
        medal="🥇" if pct>=90 else "🥈" if pct>=70 else "🥉" if pct>=50 else "😅"
        st.markdown(f"""
        <div class="qcard" style="text-align:center;">
          <div style="font-size:4rem;">{medal}</div>
          <h2>Quiz Complete!</h2>
          <p>You scored <b style="color:#a78bfa;font-size:1.3rem;">{score}/{total}</b> ({pct}%)</p>
          <p>{'Outstanding! You\'re an animal expert!' if pct>=90 else 'Great job! Keep exploring!' if pct>=70 else 'Good effort — keep learning!' if pct>=50 else 'Time to browse the encyclopedia!'}</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 Play Again", key="quiz_again"):
            st.session_state.quiz_questions=[]; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    q=qs[qi]
    progress=qi/len(qs)
    st.progress(progress, text=f"Question {qi+1} of {len(qs)}  ·  Score: {st.session_state.quiz_score}")

    st.markdown(f"""
    <div class="qcard">
      <h2>Q{qi+1}. {q['q']}</h2>
    </div>""", unsafe_allow_html=True)

    answered=st.session_state.quiz_answered
    selected=st.session_state.quiz_selected

    for opt in q["opts"]:
        if answered:
            if opt==q["a"]:    btn_class="correct"
            elif opt==selected: btn_class="wrong"
            else:               btn_class=""
            st.markdown(f'<div class="ans-btn {btn_class}" style="padding:.65rem 1rem;border-radius:12px;margin:.3rem 0;">{("✅ " if opt==q["a"] else "❌ " if opt==selected else "")}{opt}</div>', unsafe_allow_html=True)
        else:
            if st.button(opt, key=f"qopt_{qi}_{opt}"):
                st.session_state.quiz_answered=True
                st.session_state.quiz_selected=opt
                if opt==q["a"]: st.session_state.quiz_score+=1
                st.rerun()

    if answered:
        if selected==q["a"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ The answer was: **{q['a']}**")
        if st.button("Next Question →", key="quiz_next"):
            st.session_state.quiz_q+=1; st.session_state.quiz_answered=False; st.session_state.quiz_selected=None; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: GUESS THE ANIMAL
# ══════════════════════════════════════════════════════════════
def page_guess():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><h1>🕵️ Guess the Animal</h1><p>Clues are revealed one by one — guess with as few as possible!</p></div>', unsafe_allow_html=True)

    def new_game():
        a=random.choice(list(ANIMALS.keys()))
        st.session_state.guess_animal=a
        st.session_state.guess_revealed=[0]  # start with 1 hint visible
        st.session_state.guess_done=False
        st.session_state.guess_wrong=0
        st.session_state.guess_won=False

    if st.session_state.guess_animal is None:
        new_game()

    name=st.session_state.guess_animal
    d=ANIMALS[name]
    revealed=st.session_state.guess_revealed
    done=st.session_state.guess_done

    HINTS=[
        ("🌍 Continent",    d["continent"]),
        ("🍽️ Diet",         d["diet"]),
        ("🏡 Habitat",      d["habitat"]),
        ("⚖️ Weight",       f"{d['weight_kg']} kg"),
        ("⚡ Top Speed",    f"{d['speed_kmh']} km/h"),
        ("🧬 Category",     d["category"]),
        ("🛡️ Conservation", d["conservation"]),
        ("⏳ Lifespan",     f"~{d['lifespan_years']} years"),
        ("🔬 Family",       d["family"]),
        ("💡 Fun Fact",     d["fun_fact"]),
    ]

    st.markdown(f'<p style="font-size:.85rem;color:rgba(148,163,184,.55);margin-bottom:.8rem;">Hints revealed: <b style="color:#a78bfa;">{len(revealed)}</b> / {len(HINTS)}  ·  Wrong guesses: <b style="color:#ef4444;">{st.session_state.guess_wrong}</b></p>', unsafe_allow_html=True)

    for i,(label,val) in enumerate(HINTS):
        if i in revealed:
            st.markdown(f'<div class="hint-card"><b style="color:rgba(148,163,184,.55);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;">{label}</b><br>{val}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="hint-card hint-hidden"><b>{label}</b><br>???</div>', unsafe_allow_html=True)

    if not done:
        c1,c2=st.columns([3,1])
        with c1:
            guess_opts=["— select —"]+sorted(ANIMALS.keys())
            guess=st.selectbox("Your guess:",guess_opts,key="guess_pick")
        with c2:
            st.markdown("<br>",unsafe_allow_html=True)
            if st.button("Submit →",key="guess_submit") and guess!="— select —":
                if guess==name:
                    st.session_state.guess_done=True; st.session_state.guess_won=True; st.rerun()
                else:
                    st.session_state.guess_wrong+=1
                    # reveal next hint
                    next_i=max(revealed)+1
                    if next_i<len(HINTS):
                        st.session_state.guess_revealed.append(next_i)
                    st.rerun()

        if st.button("👁️ Reveal Next Hint",key="next_hint"):
            next_i=max(revealed)+1
            if next_i<len(HINTS):
                st.session_state.guess_revealed.append(next_i)
                st.rerun()

        if st.button("🏳️ Give Up",key="give_up"):
            st.session_state.guess_done=True; st.rerun()
    else:
        if st.session_state.guess_won:
            hints_used=len(revealed)
            st.success(f"🎉 Correct! It was **{d['emoji']} {name}** — guessed with {hints_used} hint(s) visible!")
        else:
            st.error(f"The animal was **{d['emoji']} {name}**!")
        c1,c2=st.columns(2)
        with c1:
            if st.button("🔄 New Game",key="guess_new"):
                new_game(); st.rerun()
        with c2:
            if st.button(f"View {d['emoji']} {name}",key="guess_view"):
                st.session_state.selected=name; st.session_state.page="detail"; add_history(name); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════
page=st.session_state.page

if page=="detail" or (page=="home" and st.session_state.selected):
    if st.session_state.selected:
        st.session_state.page="detail"
        page_detail()
    else:
        st.session_state.page="home"
        page_home()
elif page=="explorer":    page_explorer()
elif page=="habitat":     page_habitat()
elif page=="conservation":page_conservation()
elif page=="stats":       page_stats()
elif page=="quiz":        page_quiz()
elif page=="guess":       page_guess()
else:
    page_home()
