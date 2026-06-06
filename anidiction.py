import streamlit as st
st.set_page_config(page_title="Animal Encyclopedia", page_icon="🐾", layout="wide")

import random
import datetime
import urllib.parse
import json

try:
    import requests as _requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ═══════════════════════════════════════════════════════════════════════════════
# ANIMAL DATABASE
# ═══════════════════════════════════════════════════════════════════════════════
ANIMALS = {
    "Lion": {"emoji":"🦁","category":"Mammal","habitat":"Savanna, Grasslands","diet":"Carnivore","lifespan":"10–14 years (wild)","weight":"120–250 kg","conservation":"Vulnerable","conservation_color":"#fb923c","region":"Africa","fun_fact":"A lion's roar can be heard from up to 8 km away.","description":"The lion is the second-largest living cat after the tiger. Known as the 'king of the jungle', lions are highly social and live in groups called prides. Males are distinguished by their impressive manes.","image_query":"lion wild africa savanna"},
    "Blue Whale": {"emoji":"🐋","category":"Mammal","habitat":"Open Ocean","diet":"Filter Feeder (Krill)","lifespan":"80–90 years","weight":"Up to 200,000 kg","conservation":"Endangered","conservation_color":"#ef4444","region":"Worldwide","fun_fact":"The blue whale's heart is the size of a small car and can weigh 400 kg.","description":"The blue whale is the largest animal known to have ever existed. Despite their enormous size, blue whales feed almost exclusively on tiny shrimp-like creatures called krill, consuming up to 4 tonnes per day.","image_query":"blue whale ocean underwater"},
    "Snow Leopard": {"emoji":"🐆","category":"Mammal","habitat":"Mountain Ranges","diet":"Carnivore","lifespan":"10–12 years (wild)","weight":"22–55 kg","conservation":"Vulnerable","conservation_color":"#fb923c","region":"Central Asia","fun_fact":"Snow leopards cannot roar — they make a unique sound called a 'chuff'.","description":"Snow leopards are elusive big cats adapted to life in cold, mountainous environments. Their thick fur, wide paws that act as natural snowshoes, and long tails for balance make them perfectly suited for the Himalayas.","image_query":"snow leopard mountain wild"},
    "Emperor Penguin": {"emoji":"🐧","category":"Bird","habitat":"Antarctica","diet":"Carnivore (Fish, Squid)","lifespan":"15–20 years","weight":"22–45 kg","conservation":"Near Threatened","conservation_color":"#facc15","region":"Antarctica","fun_fact":"Emperor penguins can dive to depths of over 500 metres and hold their breath for 20 minutes.","description":"The emperor penguin is the tallest and heaviest of all penguin species. They breed during the harsh Antarctic winter, with males incubating a single egg on their feet under a brood pouch for up to 65 days.","image_query":"emperor penguin antarctica colony"},
    "Komodo Dragon": {"emoji":"🦎","category":"Reptile","habitat":"Tropical Forest, Savanna","diet":"Carnivore","lifespan":"30 years","weight":"70–90 kg","conservation":"Endangered","conservation_color":"#ef4444","region":"Indonesia","fun_fact":"Komodo dragons can detect carrion from up to 9.5 km away using their forked tongues.","description":"The Komodo dragon is the world's largest living lizard. Found only on a handful of Indonesian islands, these apex predators use venom and bacteria-laden saliva to subdue prey much larger than themselves.","image_query":"komodo dragon indonesia wild"},
    "Bald Eagle": {"emoji":"🦅","category":"Bird","habitat":"Forests, Near Water","diet":"Carnivore (Fish, Small Mammals)","lifespan":"20–30 years","weight":"3–6.3 kg","conservation":"Least Concern","conservation_color":"#34d399","region":"North America","fun_fact":"Bald eagles build the largest bird nests in North America — up to 4 metres deep and 2.5 metres wide.","description":"The bald eagle is the national bird and symbol of the United States. A master fisher, it swoops down at speeds of up to 160 km/h to snatch fish from the water with its powerful talons.","image_query":"bald eagle flying wild nature"},
    "Poison Dart Frog": {"emoji":"🐸","category":"Amphibian","habitat":"Tropical Rainforest","diet":"Insectivore","lifespan":"3–15 years","weight":"< 10 g","conservation":"Varies by Species","conservation_color":"#a78bfa","region":"Central & South America","fun_fact":"The golden poison frog has enough toxin to kill 10 adult humans.","description":"Poison dart frogs are among the most toxic animals on Earth, yet their vivid colours serve as a warning to predators — a phenomenon called aposematism. Their toxins come from their diet of specific insects in the wild.","image_query":"poison dart frog colorful rainforest"},
    "Giant Panda": {"emoji":"🐼","category":"Mammal","habitat":"Temperate Broadleaf Forest","diet":"Herbivore (Bamboo)","lifespan":"20 years (wild)","weight":"70–125 kg","conservation":"Vulnerable","conservation_color":"#fb923c","region":"China","fun_fact":"Giant pandas spend 10–16 hours a day eating bamboo to get enough nutrition.","description":"The giant panda is one of the world's most beloved and recognisable animals. Despite being classified as carnivores, pandas have evolved to eat almost exclusively bamboo, consuming 12–38 kg of it each day.","image_query":"giant panda bamboo China wildlife"},
    "Manta Ray": {"emoji":"🐟","category":"Fish","habitat":"Tropical & Subtropical Ocean","diet":"Filter Feeder (Plankton)","lifespan":"40+ years","weight":"Up to 2,000 kg","conservation":"Vulnerable","conservation_color":"#fb923c","region":"Worldwide","fun_fact":"Manta rays have the largest brain-to-body ratio of any cold-blooded fish.","description":"Manta rays are graceful giants of the ocean, gliding through the water using their large, wing-like pectoral fins. They are highly intelligent and have been observed in what appears to be playful behaviour and self-recognition.","image_query":"manta ray ocean underwater swimming"},
    "Arctic Fox": {"emoji":"🦊","category":"Mammal","habitat":"Arctic Tundra","diet":"Omnivore","lifespan":"3–6 years (wild)","weight":"3–8 kg","conservation":"Least Concern","conservation_color":"#34d399","region":"Arctic","fun_fact":"The Arctic fox can withstand temperatures as low as −70 °C before its metabolism increases.","description":"The Arctic fox is a small, resilient canid perfectly adapted to one of Earth's harshest environments. Its thick, multi-layered fur turns white in winter for camouflage in snow and brown in summer, making it one of nature's best seasonal chameleons.","image_query":"arctic fox white snow tundra wild"},
    "Cheetah": {"emoji":"🐆","category":"Mammal","habitat":"Savanna, Grasslands","diet":"Carnivore","lifespan":"10–12 years (wild)","weight":"21–72 kg","conservation":"Vulnerable","conservation_color":"#fb923c","region":"Africa, Iran","fun_fact":"The cheetah accelerates from 0 to 100 km/h in just 3 seconds — faster than most sports cars.","description":"The cheetah is the fastest land animal on Earth, capable of reaching speeds of up to 120 km/h. Unlike other big cats, cheetahs cannot roar but can purr. They rely on explosive speed and keen eyesight rather than stealth to hunt.","image_query":"cheetah running africa wild savanna"},
    "Octopus": {"emoji":"🐙","category":"Cephalopod","habitat":"Ocean (all depths)","diet":"Carnivore","lifespan":"1–5 years","weight":"3–15 kg","conservation":"Least Concern","conservation_color":"#34d399","region":"Worldwide","fun_fact":"Octopuses have three hearts, blue blood, and nine brains (one central + one per arm).","description":"Octopuses are remarkably intelligent invertebrates capable of problem-solving, tool use, and even short-term memory. They can change colour and texture in milliseconds to camouflage themselves or communicate — all while being completely colourblind.","image_query":"octopus underwater ocean wild"},
}

CATEGORIES = ["All"] + sorted(set(a["category"] for a in ANIMALS.values()))
REGIONS    = ["All"] + sorted(set(a["region"]    for a in ANIMALS.values()))
CONSERVATION_ORDER = {"Least Concern":0,"Near Threatened":1,"Vulnerable":2,"Endangered":3,"Varies by Species":4}

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
defaults = {
    "selected_animal": None,
    "wiki_cache": {},          # title -> built data dict
    "favorites": [],
    "search_history": [],
    "free_results": [],        # list of Wikipedia page titles from last search
    "free_query": "",
    "view_mode": "browse",     # "browse" | "wiki"
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════════════════
# WIKIPEDIA HELPERS  (graceful degradation if network fails)
# ═══════════════════════════════════════════════════════════════════════════════
WIKI_HEADERS = {"User-Agent": "AnimalEncyclopedia/2.0 (https://github.com/example; educational)"}

def _get(url, params=None, timeout=6):
    """Safe GET — returns response object or None."""
    if not HAS_REQUESTS:
        return None
    try:
        r = _requests.get(url, params=params, headers=WIKI_HEADERS, timeout=timeout)
        if r.status_code == 200:
            return r
    except Exception:
        pass
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def wiki_search(query: str):
    """Return list of matching Wikipedia article titles for an animal query."""
    r = _get("https://en.wikipedia.org/w/api.php", params={
        "action": "query", "list": "search",
        "srsearch": query + " animal species",
        "srnamespace": "0", "srlimit": "15",
        "srprop": "snippet|titlesnippet", "format": "json",
    })
    if not r:
        return []
    items = r.json().get("query", {}).get("search", [])
    BAD = ["film","movie","album","band","song","footballer","politician",
           "actor","singer","book","novel","video game","television",
           "TV series","disambiguation","hurricane","typhoon","operation"]
    out = []
    for item in items:
        title   = item["title"]
        snippet = item.get("snippet", "")
        combined = (title + " " + snippet).lower()
        if any(b in combined for b in BAD):
            continue
        out.append(title)
        if len(out) >= 8:
            break
    return out

@st.cache_data(ttl=3600, show_spinner=False)
def wiki_summary(title: str):
    """Fetch Wikipedia REST summary for a page title."""
    safe = urllib.parse.quote(title.replace(" ", "_"))
    r = _get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe}")
    if r:
        return r.json()
    return {}

@st.cache_data(ttl=3600, show_spinner=False)
def wiki_images(title: str):
    """Return list of image File: titles from a Wikipedia article."""
    r = _get("https://en.wikipedia.org/w/api.php", params={
        "action": "query", "titles": title,
        "prop": "images", "imlimit": "30", "format": "json",
    })
    if not r:
        return []
    pages = r.json().get("query", {}).get("pages", {})
    BAD = ["flag","icon","logo","map","symbol","blank","commons","wikimedia",
           "edit","question","sound","audio","silhouette","range","distribution"]
    out = []
    for p in pages.values():
        for img in p.get("images", []):
            nm = img["title"].lower()
            if any(b in nm for b in BAD):
                continue
            if nm.endswith((".svg", ".ogg", ".ogv", ".webm", ".pdf")):
                continue
            out.append(img["title"])
    return out[:8]

@st.cache_data(ttl=3600, show_spinner=False)
def resolve_img(file_title: str):
    """Resolve File:xxx → actual HTTPS image URL (500px thumb)."""
    r = _get("https://en.wikipedia.org/w/api.php", params={
        "action": "query", "titles": file_title,
        "prop": "imageinfo", "iiprop": "url|dimensions",
        "iiurlwidth": "500", "format": "json",
    })
    if not r:
        return None
    pages = r.json().get("query", {}).get("pages", {})
    for p in pages.values():
        info = p.get("imageinfo", [])
        if info:
            return info[0].get("thumburl") or info[0].get("url")
    return None

def build_wiki_entry(title: str, summary: dict) -> dict:
    """Convert Wikipedia summary → animal data dict."""
    desc = summary.get("extract", "No description available.")
    sentences = [s.strip() for s in desc.replace("\n", " ").split(". ") if s.strip()]
    short = ". ".join(sentences[:4])
    if short and not short.endswith("."):
        short += "."

    thumb = None
    if "thumbnail" in summary:
        raw = summary["thumbnail"].get("source", "")
        for old, new in [("/200px-","/600px-"), ("/320px-","/600px-"), ("/400px-","/600px-")]:
            if old in raw:
                raw = raw.replace(old, new)
                break
        thumb = raw

    wiki_url = summary.get("content_urls", {}).get("desktop", {}).get("page", "")
    return {
        "emoji": "🐾",
        "category": summary.get("description", "Animal").split(",")[0].strip().title() or "Animal",
        "habitat": "—", "diet": "—", "lifespan": "—", "weight": "—",
        "conservation": "Unknown", "conservation_color": "#64748b",
        "region": "—",
        "fun_fact": "Visit the Wikipedia article for more fascinating facts!",
        "description": short or "No description available.",
        "image_query": urllib.parse.quote(title.lower()),
        "wiki_url": wiki_url,
        "wiki_thumb": thumb,
        "wiki_title": title,
        "_from_wiki": True,
    }

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{
  background:linear-gradient(160deg,#020617,#0a1628,#1a0a28)!important;
  min-height:100vh;font-family:'Outfit',sans-serif!important;
}
[data-testid="stAppViewContainer"]>.main{background:transparent!important;}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stSidebar"]{
  background:rgba(5,10,25,0.88)!important;
  border-right:1px solid rgba(255,255,255,0.07)!important;
  backdrop-filter:blur(20px);
}
#MainMenu,footer,header{visibility:hidden;}

/* Stars */
.stars-bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;}
.star{position:absolute;border-radius:50%;background:white;animation:twinkle var(--dur,3s) ease-in-out infinite alternate;opacity:0;}
@keyframes twinkle{0%{opacity:0.1;transform:scale(0.8)}100%{opacity:0.85;transform:scale(1.2)}}

/* Layout */
.page-wrap{position:relative;z-index:1;padding:2rem 1.5rem 4rem;}
.page-header{text-align:center;margin-bottom:2rem;padding-top:1rem;}
.page-header h1{
  font-weight:800;font-size:clamp(2rem,5vw,3.2rem);letter-spacing:-0.02em;
  background:linear-gradient(135deg,#e2e8f0 0%,#94a3b8 55%,#a78bfa 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  margin:0 0 0.4rem;line-height:1.15;
}
.page-header p{font-size:1rem;color:rgba(148,163,184,0.75);font-weight:300;letter-spacing:0.04em;margin:0;}

/* Free search box */
.fsearch-box{
  background:rgba(15,23,42,0.72);border:1px solid rgba(167,139,250,0.28);
  border-radius:20px;padding:1.4rem 1.6rem 1rem;
  backdrop-filter:blur(20px);margin-bottom:1.5rem;
  box-shadow:0 0 50px rgba(167,139,250,0.07);
}
.fsearch-box h3{font-weight:700;font-size:1.05rem;color:#e2e8f0;margin:0 0 0.7rem;}

/* Search result chips */
.sr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:0.8rem;margin-top:0.9rem;}
.sr-card{
  background:rgba(15,23,42,0.65);border:1px solid rgba(255,255,255,0.07);
  border-radius:14px;padding:0.9rem 0.8rem;backdrop-filter:blur(18px);
  text-align:center;transition:transform .2s,border-color .2s,box-shadow .2s;
}
.sr-card:hover{transform:translateY(-3px);border-color:rgba(167,139,250,0.4);box-shadow:0 8px 28px rgba(167,139,250,0.14);}
.sr-name{font-weight:700;font-size:0.9rem;color:#f1f5f9;margin-bottom:0.2rem;}
.sr-sub{font-size:0.7rem;color:rgba(148,163,184,0.5);}

/* Animal grid */
.animal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(205px,1fr));gap:1.2rem;}
.animal-card{
  background:rgba(15,23,42,0.6);border:1px solid rgba(255,255,255,0.08);
  border-radius:18px;padding:1.5rem 1.3rem 1.3rem;
  backdrop-filter:blur(18px);cursor:pointer;
  transition:transform .25s cubic-bezier(.22,.68,0,1.2),border-color .25s,box-shadow .25s;
  text-align:center;
}
.animal-card:hover{
  transform:translateY(-5px) scale(1.02);border-color:rgba(167,139,250,0.4);
  box-shadow:0 0 0 1px rgba(167,139,250,0.3),0 16px 50px -8px rgba(167,139,250,0.2),0 6px 20px rgba(0,0,0,0.4);
}
.animal-card .emoji{font-size:2.8rem;margin-bottom:0.6rem;display:block;}
.animal-card .name{font-weight:700;font-size:1.05rem;color:#f1f5f9;margin:0 0 0.3rem;}
.animal-card .cat-badge{
  display:inline-block;font-size:0.65rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
  background:rgba(167,139,250,0.12);border:1px solid rgba(167,139,250,0.2);
  color:#a78bfa;padding:2px 9px;border-radius:20px;
}
.animal-card .region{font-size:0.78rem;color:rgba(148,163,184,0.6);margin-top:0.4rem;font-weight:300;}

/* Detail panel */
.detail-wrap{
  background:rgba(10,18,40,0.72);border:1px solid rgba(255,255,255,0.1);
  border-radius:24px;padding:2.5rem;
  backdrop-filter:blur(24px);position:relative;overflow:hidden;margin-bottom:2rem;
}
.detail-glow{
  position:absolute;top:-60px;right:-60px;width:220px;height:220px;border-radius:50%;
  background:radial-gradient(circle,rgba(167,139,250,0.2) 0%,transparent 70%);pointer-events:none;
}
.detail-name{font-weight:800;font-size:2.4rem;color:#f1f5f9;letter-spacing:-0.02em;margin:0 0 0.3rem;}
.detail-desc{font-size:0.95rem;color:rgba(148,163,184,0.85);line-height:1.7;font-weight:300;margin:1rem 0 1.5rem;}
.fun-fact{
  background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.2);
  border-radius:12px;padding:1rem 1.2rem;margin-bottom:1.5rem;
}
.fun-fact .lbl{font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#a78bfa;margin-bottom:.3rem;}
.fun-fact .txt{font-size:.92rem;color:#e2e8f0;line-height:1.6;}
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem;margin-top:1rem;}
.stat-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:.85rem .9rem;}
.stat-lbl{font-size:.67rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:rgba(148,163,184,.55);margin-bottom:.25rem;}
.stat-val{font-size:.9rem;font-weight:600;color:#e2e8f0;}
.con-badge{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:4px 12px;border-radius:20px;border:1px solid;}

/* Wiki banner */
.wiki-banner{
  background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.22);
  border-radius:12px;padding:.75rem 1.1rem;margin-bottom:1rem;
  font-size:.82rem;color:rgba(147,210,250,.85);
}

/* Photo section */
.section-lbl{
  font-weight:700;font-size:1.1rem;color:#e2e8f0;
  margin:1.6rem 0 .7rem;display:flex;align-items:center;gap:.45rem;
}

/* Sidebar overrides */
[data-testid="stSidebar"] *{font-family:'Outfit',sans-serif!important;}
[data-testid="stSidebar"] .stSelectbox>div>div{
  background:rgba(15,23,42,.7)!important;border:1px solid rgba(255,255,255,.1)!important;
  border-radius:10px!important;color:#e2e8f0!important;
}
[data-testid="stSidebar"] label{color:rgba(148,163,184,.65)!important;font-size:.8rem!important;letter-spacing:.06em!important;text-transform:uppercase!important;}
[data-testid="stSidebar"] .stTextInput input{
  background:rgba(15,23,42,.7)!important;border:1px solid rgba(255,255,255,.1)!important;
  border-radius:10px!important;color:#e2e8f0!important;font-family:'Outfit',sans-serif!important;
}
[data-testid="stSidebar"] h2{color:#f1f5f9!important;font-weight:700!important;font-size:1.1rem!important;}
[data-testid="stSidebar"] p{color:rgba(148,163,184,.7)!important;font-size:.82rem!important;}
.stButton>button{
  background:rgba(167,139,250,.15)!important;border:1px solid rgba(167,139,250,.3)!important;
  color:#a78bfa!important;border-radius:10px!important;
  font-family:'Outfit',sans-serif!important;font-weight:600!important;transition:all .2s!important;
}
.stButton>button:hover{background:rgba(167,139,250,.25)!important;border-color:#a78bfa!important;}
div[data-testid="column"] .stButton>button{width:100%;}
</style>

<div class="stars-bg" id="starsContainer"></div>
<script>
(function(){
  var c=document.getElementById('starsContainer');if(!c)return;
  for(var i=0;i<130;i++){
    var s=document.createElement('div');s.className='star';
    var sz=Math.random()*2.5+0.5;
    s.style.cssText='width:'+sz+'px;height:'+sz+'px;left:'+(Math.random()*100)+'%;top:'+(Math.random()*100)+'%;--dur:'+(Math.random()*3+2)+'s;animation-delay:'+(Math.random()*5)+'s';
    c.appendChild(s);
  }
})();
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def add_history(q):
    h = st.session_state.search_history
    if q and q not in h:
        h.insert(0, q)
    st.session_state.search_history = h[:20]

def toggle_fav(name):
    favs = st.session_state.favorites
    if name in favs:
        favs.remove(name)
    else:
        favs.insert(0, name)
    st.session_state.favorites = favs[:30]

def filter_animals():
    r = dict(ANIMALS)
    if sidebar_search:
        r = {k:v for k,v in r.items()
             if sidebar_search.lower() in k.lower() or sidebar_search.lower() in v["description"].lower()}
    if cat_filter != "All":
        r = {k:v for k,v in r.items() if v["category"] == cat_filter}
    if region_filter != "All":
        r = {k:v for k,v in r.items() if v["region"] == region_filter}
    if sort_by == "Name (A–Z)":
        r = dict(sorted(r.items()))
    elif sort_by == "Conservation Status":
        r = dict(sorted(r.items(), key=lambda x: CONSERVATION_ORDER.get(x[1]["conservation"], 99)))
    return r

def get_animal_data(name):
    """Return data dict for a name — from local DB, wiki cache, or None."""
    if name in ANIMALS:
        return ANIMALS[name]
    return st.session_state.wiki_cache.get(name)

def load_wiki_animal(title):
    """Fetch Wikipedia data and store in cache. Return data dict or None."""
    if title in st.session_state.wiki_cache:
        return st.session_state.wiki_cache[title]
    summary = wiki_summary(title)
    if not summary:
        return None
    entry = build_wiki_entry(title, summary)
    st.session_state.wiki_cache[title] = entry
    return entry

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🐾 Animal Encyclopedia")
    st.markdown("Search **any animal on Earth** via Wikipedia, or browse our curated collection.")
    st.markdown("---")
    sidebar_search = st.text_input("🔍 Filter curated list", placeholder="e.g. Lion, Eagle...")
    cat_filter    = st.selectbox("Category", CATEGORIES)
    region_filter = st.selectbox("Region", REGIONS)
    sort_by       = st.selectbox("Sort by", ["Name (A–Z)", "Conservation Status"])
    st.markdown("---")

    # Animal of the Day
    rng  = random.Random(int(datetime.date.today().strftime("%Y%m%d")))
    AOTD = rng.choice(list(ANIMALS.keys()))
    st.markdown(f"### 🏆 Animal of the Day")
    st.markdown(f"**{ANIMALS[AOTD]['emoji']} {AOTD}**")
    if st.button("View Animal of the Day", key="aotd_btn"):
        st.session_state.selected_animal = AOTD
        st.session_state.view_mode = "browse"
        st.rerun()

    st.markdown("---")
    if st.button("🎲 Random Animal", key="rand_btn"):
        st.session_state.selected_animal = random.choice(list(ANIMALS.keys()))
        st.session_state.view_mode = "browse"
        st.rerun()

    st.markdown("---")
    st.markdown("### ⭐ Favorites")
    if st.session_state.favorites:
        for fav in st.session_state.favorites[:10]:
            if st.button(f"⭐ {fav}", key=f"fav_{fav}"):
                st.session_state.selected_animal = fav
                st.session_state.view_mode = "browse" if fav in ANIMALS else "wiki"
                st.rerun()
    else:
        st.markdown('<p style="color:rgba(148,163,184,0.4);font-size:0.8rem;">No favorites yet.</p>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🕐 Recent Searches")
    if st.session_state.search_history:
        for h in st.session_state.search_history[:6]:
            st.markdown(f'<span style="font-size:0.78rem;color:rgba(148,163,184,0.45);">• {h}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:rgba(148,163,184,0.4);font-size:0.8rem;">No searches yet.</p>', unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.selected_animal:
        if st.button("← Back to All Animals", key="back_btn"):
            st.session_state.selected_animal = None
            st.session_state.view_mode = "browse"
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL VIEW
# ═══════════════════════════════════════════════════════════════════════════════
def show_detail(name, data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    con_color  = data.get("conservation_color", "#64748b")
    is_fav     = name in st.session_state.favorites
    from_wiki  = data.get("_from_wiki", False)

    if from_wiki:
        wiki_url = data.get("wiki_url", "")
        link_html = (f'<a href="{wiki_url}" target="_blank" style="color:#38bdf8;text-decoration:none;">Read on Wikipedia ↗</a>'
                     if wiki_url else "")
        st.markdown(f'<div class="wiki-banner">📖 Live data from Wikipedia. {link_html}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="detail-wrap">
      <div class="detail-glow"></div>
      <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;flex-wrap:wrap;">
        <span style="font-size:3.5rem;line-height:1;">{data['emoji']}</span>
        <div>
          <div class="detail-name">{name}</div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
            <span style="font-size:0.75rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:rgba(148,163,184,0.6);">{data['category']} · {data['region']}</span>
            <span class="con-badge" style="color:{con_color};border-color:{con_color}33;background:{con_color}15;">{data['conservation']}</span>
          </div>
        </div>
      </div>
      <p class="detail-desc">{data['description']}</p>
      <div class="fun-fact">
        <div class="lbl">✦ Did you know?</div>
        <div class="txt">{data['fun_fact']}</div>
      </div>
      <div class="stats-grid">
        <div class="stat-card"><div class="stat-lbl">Habitat</div><div class="stat-val">{data['habitat']}</div></div>
        <div class="stat-card"><div class="stat-lbl">Diet</div><div class="stat-val">{data['diet']}</div></div>
        <div class="stat-card"><div class="stat-lbl">Lifespan</div><div class="stat-val">{data['lifespan']}</div></div>
        <div class="stat-card"><div class="stat-lbl">Weight</div><div class="stat-val">{data['weight']}</div></div>
        <div class="stat-card"><div class="stat-lbl">Region</div><div class="stat-val">{data['region']}</div></div>
        <div class="stat-card"><div class="stat-lbl">Conservation</div><div class="stat-val" style="color:{con_color};">{data['conservation']}</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_fav, col_back = st.columns([1, 3])
    with col_fav:
        fav_lbl = "★ Unfavorite" if is_fav else "☆ Favorite"
        if st.button(fav_lbl, key="fav_toggle"):
            toggle_fav(name)
            st.rerun()

    # ── PHOTOS ────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-lbl">📸 Photos</div>', unsafe_allow_html=True)

    wiki_title = data.get("wiki_title", name)
    photos_shown = 0

    # Primary thumbnail
    thumb = data.get("wiki_thumb")
    if not thumb:
        smry = wiki_summary(wiki_title)
        if "thumbnail" in smry:
            raw = smry["thumbnail"].get("source", "")
            for old, new in [("/200px-","/600px-"),("/320px-","/600px-"),("/400px-","/600px-")]:
                if old in raw:
                    raw = raw.replace(old, new)
                    break
            thumb = raw

    if thumb:
        st.markdown(
            f'<img src="{thumb}" style="width:100%;max-width:560px;border-radius:16px;'
            f'border:1px solid rgba(255,255,255,0.1);display:block;margin-bottom:0.5rem;" alt="{name}">',
            unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.72rem;color:rgba(148,163,184,0.35);margin-bottom:1rem;">📷 via Wikipedia</p>', unsafe_allow_html=True)
        photos_shown += 1

    # Extra article images
    img_files = wiki_images(wiki_title)
    if img_files:
        cols = st.columns(3)
        shown = 0
        for ft in img_files:
            if shown >= 3:
                break
            url = resolve_img(ft)
            if url and any(url.lower().endswith(ext) for ext in (".jpg",".jpeg",".png",".webp")):
                with cols[shown % 3]:
                    st.markdown(
                        f'<img src="{url}" style="width:100%;border-radius:10px;'
                        f'border:1px solid rgba(255,255,255,0.07);margin-bottom:0.5rem;" alt="{ft}">',
                        unsafe_allow_html=True)
                shown += 1
                photos_shown += 1

    if photos_shown == 0:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);'
            f'border-radius:14px;padding:2.5rem;text-align:center;color:rgba(148,163,184,0.4);font-size:0.9rem;">'
            f'{data["emoji"]} Photos unavailable — search online below</div>',
            unsafe_allow_html=True)

    ddg = f"https://duckduckgo.com/?q={urllib.parse.quote(name + ' animal')}&iax=images&ia=images"
    st.markdown(
        f'<a href="{ddg}" target="_blank" style="display:inline-block;margin-top:.8rem;'
        f'font-size:.85rem;color:#a78bfa;text-decoration:none;'
        f'background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);'
        f'padding:6px 14px;border-radius:10px;font-family:Outfit,sans-serif;">🔍 More {name} photos ↗</a>',
        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRID / HOME VIEW
# ═══════════════════════════════════════════════════════════════════════════════
def show_grid(animals):
    st.markdown("""
    <div class="page-wrap">
      <div class="page-header">
        <h1>🐾 Animal Encyclopedia</h1>
        <p>Search any animal on Earth, or browse our curated collection</p>
      </div>
    """, unsafe_allow_html=True)

    # ── FREE SEARCH ───────────────────────────────────────────────────────────
    st.markdown('<div class="fsearch-box"><h3>🔎 Search Any Animal</h3></div>', unsafe_allow_html=True)

    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        query = st.text_input(
            "fs_inp", label_visibility="collapsed",
            placeholder="Any animal — Axolotl, Tardigrade, Narwhal, Pangolin, Quokka…",
            value=st.session_state.free_query,
            key="fs_field")
    with col_btn:
        do_search = st.button("Search →", key="fs_btn")

    if do_search and query.strip():
        q = query.strip()
        st.session_state.free_query = q
        add_history(q)
        with st.spinner(f"Searching Wikipedia for '{q}'…"):
            results = wiki_search(q)
        st.session_state.free_results = results

    # Results
    if st.session_state.free_results:
        results = st.session_state.free_results
        q_display = st.session_state.free_query
        st.markdown(
            f'<p style="font-size:.84rem;color:rgba(148,163,184,.6);font-family:Outfit,sans-serif;margin:.4rem 0 .6rem;">'
            f'Found <b style="color:#a78bfa;">{len(results)}</b> results for "{q_display}" — click to open</p>',
            unsafe_allow_html=True)

        n_cols = min(len(results), 4)
        cols = st.columns(n_cols)
        for i, title in enumerate(results):
            with cols[i % n_cols]:
                if st.button(f"🐾 {title}", key=f"wr_{i}"):
                    with st.spinner(f"Loading {title}…"):
                        entry = load_wiki_animal(title)
                    if entry:
                        st.session_state.selected_animal = title
                        st.session_state.view_mode = "wiki"
                        add_history(title)
                        st.rerun()
                    else:
                        st.error(f"Could not load '{title}'. Try another result.")

        if st.button("✕ Clear", key="clear_res"):
            st.session_state.free_results = []
            st.session_state.free_query   = ""
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.05);margin:1.5rem 0;'>", unsafe_allow_html=True)

    # ── CURATED GRID ──────────────────────────────────────────────────────────
    st.markdown(
        '<p style="font-family:Outfit,sans-serif;font-size:.82rem;color:rgba(148,163,184,.45);'
        'margin-bottom:1rem;text-transform:uppercase;letter-spacing:.1em;">📚 Curated Collection</p>',
        unsafe_allow_html=True)

    if not animals:
        st.markdown('<p style="text-align:center;color:rgba(148,163,184,.45);padding:3rem;">No animals match your filters.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Visual HTML cards
    cards = '<div class="animal-grid">'
    for name, d in animals.items():
        cards += f"""
        <div class="animal-card">
          <span class="emoji">{d['emoji']}</span>
          <div class="name">{name}</div>
          <div class="cat-badge">{d['category']}</div>
          <div class="region">📍 {d['region']}</div>
        </div>"""
    cards += '</div>'
    st.markdown(cards, unsafe_allow_html=True)

    # Functional buttons under the grid
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    btn_cols = st.columns(4)
    for i, (name, d) in enumerate(animals.items()):
        with btn_cols[i % 4]:
            if st.button(f"{d['emoji']} {name}", key=f"grid_{name}"):
                st.session_state.selected_animal = name
                st.session_state.view_mode = "browse"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
sel = st.session_state.selected_animal

if sel:
    data = get_animal_data(sel)
    if data is None:
        # Try to load from Wikipedia on-the-fly
        with st.spinner(f"Loading {sel}…"):
            data = load_wiki_animal(sel)
    if data:
        show_detail(sel, data)
    else:
        st.error(f"Could not load data for '{sel}'. Please go back and try another.")
        if st.button("← Back"):
            st.session_state.selected_animal = None
            st.rerun()
else:
    show_grid(filter_animals())
