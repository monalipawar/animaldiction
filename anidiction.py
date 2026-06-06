import streamlit as st

st.set_page_config(page_title="Animal Dictionary", page_icon="🐾", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# ANIMAL DATABASE
# ═══════════════════════════════════════════════════════════════════════════════
ANIMALS = {
    "Lion": {
        "emoji": "🦁",
        "category": "Mammal",
        "habitat": "Savanna, Grasslands",
        "diet": "Carnivore",
        "lifespan": "10–14 years (wild)",
        "weight": "120–250 kg",
        "conservation": "Vulnerable",
        "conservation_color": "#fb923c",
        "region": "Africa",
        "fun_fact": "A lion's roar can be heard from up to 8 km away.",
        "description": "The lion is the second-largest living cat after the tiger. Known as the 'king of the jungle', lions are highly social and live in groups called prides. Males are distinguished by their impressive manes.",
        "image_query": "lion wild africa savanna"
    },
    "Blue Whale": {
        "emoji": "🐋",
        "category": "Mammal",
        "habitat": "Open Ocean",
        "diet": "Filter Feeder (Krill)",
        "lifespan": "80–90 years",
        "weight": "Up to 200,000 kg",
        "conservation": "Endangered",
        "conservation_color": "#ef4444",
        "region": "Worldwide",
        "fun_fact": "The blue whale's heart is the size of a small car and can weigh 400 kg.",
        "description": "The blue whale is the largest animal known to have ever existed. Despite their enormous size, blue whales feed almost exclusively on tiny shrimp-like creatures called krill, consuming up to 4 tonnes per day.",
        "image_query": "blue whale ocean underwater"
    },
    "Snow Leopard": {
        "emoji": "🐆",
        "category": "Mammal",
        "habitat": "Mountain Ranges",
        "diet": "Carnivore",
        "lifespan": "10–12 years (wild)",
        "weight": "22–55 kg",
        "conservation": "Vulnerable",
        "conservation_color": "#fb923c",
        "region": "Central Asia",
        "fun_fact": "Snow leopards cannot roar — they make a unique sound called a 'chuff'.",
        "description": "Snow leopards are elusive big cats adapted to life in cold, mountainous environments. Their thick fur, wide paws that act as natural snowshoes, and long tails for balance make them perfectly suited for the Himalayas.",
        "image_query": "snow leopard mountain wild"
    },
    "Emperor Penguin": {
        "emoji": "🐧",
        "category": "Bird",
        "habitat": "Antarctica",
        "diet": "Carnivore (Fish, Squid)",
        "lifespan": "15–20 years",
        "weight": "22–45 kg",
        "conservation": "Near Threatened",
        "conservation_color": "#facc15",
        "region": "Antarctica",
        "fun_fact": "Emperor penguins can dive to depths of over 500 metres and hold their breath for 20 minutes.",
        "description": "The emperor penguin is the tallest and heaviest of all penguin species. They breed during the harsh Antarctic winter, with males incubating a single egg on their feet under a brood pouch for up to 65 days.",
        "image_query": "emperor penguin antarctica colony"
    },
    "Komodo Dragon": {
        "emoji": "🦎",
        "category": "Reptile",
        "habitat": "Tropical Forest, Savanna",
        "diet": "Carnivore",
        "lifespan": "30 years",
        "weight": "70–90 kg",
        "conservation": "Endangered",
        "conservation_color": "#ef4444",
        "region": "Indonesia",
        "fun_fact": "Komodo dragons can detect carrion from up to 9.5 km away using their forked tongues.",
        "description": "The Komodo dragon is the world's largest living lizard. Found only on a handful of Indonesian islands, these apex predators use venom and bacteria-laden saliva to subdue prey much larger than themselves.",
        "image_query": "komodo dragon indonesia wild"
    },
    "Bald Eagle": {
        "emoji": "🦅",
        "category": "Bird",
        "habitat": "Forests, Near Water",
        "diet": "Carnivore (Fish, Small Mammals)",
        "lifespan": "20–30 years",
        "weight": "3–6.3 kg",
        "conservation": "Least Concern",
        "conservation_color": "#34d399",
        "region": "North America",
        "fun_fact": "Bald eagles build the largest bird nests in North America — up to 4 metres deep and 2.5 metres wide.",
        "description": "The bald eagle is the national bird and symbol of the United States. A master fisher, it swoops down at speeds of up to 160 km/h to snatch fish from the water with its powerful talons.",
        "image_query": "bald eagle flying wild nature"
    },
    "Poison Dart Frog": {
        "emoji": "🐸",
        "category": "Amphibian",
        "habitat": "Tropical Rainforest",
        "diet": "Insectivore",
        "lifespan": "3–15 years",
        "weight": "< 10 g",
        "conservation": "Varies by Species",
        "conservation_color": "#a78bfa",
        "region": "Central & South America",
        "fun_fact": "The golden poison frog has enough toxin to kill 10 adult humans.",
        "description": "Poison dart frogs are among the most toxic animals on Earth, yet their vivid colours serve as a warning to predators — a phenomenon called aposematism. Their toxins come from their diet of specific insects in the wild.",
        "image_query": "poison dart frog colorful rainforest"
    },
    "Giant Panda": {
        "emoji": "🐼",
        "category": "Mammal",
        "habitat": "Temperate Broadleaf Forest",
        "diet": "Herbivore (Bamboo)",
        "lifespan": "20 years (wild)",
        "weight": "70–125 kg",
        "conservation": "Vulnerable",
        "conservation_color": "#fb923c",
        "region": "China",
        "fun_fact": "Giant pandas spend 10–16 hours a day eating bamboo to get enough nutrition.",
        "description": "The giant panda is one of the world's most beloved and recognisable animals. Despite being classified as carnivores, pandas have evolved to eat almost exclusively bamboo, consuming 12–38 kg of it each day.",
        "image_query": "giant panda bamboo China wildlife"
    },
    "Manta Ray": {
        "emoji": "🐟",
        "category": "Fish",
        "habitat": "Tropical & Subtropical Ocean",
        "diet": "Filter Feeder (Plankton)",
        "lifespan": "40+ years",
        "weight": "Up to 2,000 kg",
        "conservation": "Vulnerable",
        "conservation_color": "#fb923c",
        "region": "Worldwide",
        "fun_fact": "Manta rays have the largest brain-to-body ratio of any cold-blooded fish.",
        "description": "Manta rays are graceful giants of the ocean, gliding through the water using their large, wing-like pectoral fins. They are highly intelligent and have been observed in what appears to be playful behaviour and self-recognition.",
        "image_query": "manta ray ocean underwater swimming"
    },
    "Arctic Fox": {
        "emoji": "🦊",
        "category": "Mammal",
        "habitat": "Arctic Tundra",
        "diet": "Omnivore",
        "lifespan": "3–6 years (wild)",
        "weight": "3–8 kg",
        "conservation": "Least Concern",
        "conservation_color": "#34d399",
        "region": "Arctic",
        "fun_fact": "The Arctic fox can withstand temperatures as low as −70 °C before its metabolism increases.",
        "description": "The Arctic fox is a small, resilient canid perfectly adapted to one of Earth's harshest environments. Its thick, multi-layered fur turns white in winter for camouflage in snow and brown in summer, making it one of nature's best seasonal chameleons.",
        "image_query": "arctic fox white snow tundra wild"
    },
    "Cheetah": {
        "emoji": "🐆",
        "category": "Mammal",
        "habitat": "Savanna, Grasslands",
        "diet": "Carnivore",
        "lifespan": "10–12 years (wild)",
        "weight": "21–72 kg",
        "conservation": "Vulnerable",
        "conservation_color": "#fb923c",
        "region": "Africa, Iran",
        "fun_fact": "The cheetah accelerates from 0 to 100 km/h in just 3 seconds — faster than most sports cars.",
        "description": "The cheetah is the fastest land animal on Earth, capable of reaching speeds of up to 120 km/h. Unlike other big cats, cheetahs cannot roar but can purr. They rely on explosive speed and keen eyesight rather than stealth to hunt.",
        "image_query": "cheetah running africa wild savanna"
    },
    "Octopus": {
        "emoji": "🐙",
        "category": "Cephalopod",
        "habitat": "Ocean (all depths)",
        "diet": "Carnivore",
        "lifespan": "1–5 years",
        "weight": "3–15 kg",
        "conservation": "Least Concern",
        "conservation_color": "#34d399",
        "region": "Worldwide",
        "fun_fact": "Octopuses have three hearts, blue blood, and nine brains (one central + one per arm).",
        "description": "Octopuses are remarkably intelligent invertebrates capable of problem-solving, tool use, and even short-term memory. They can change colour and texture in milliseconds to camouflage themselves or communicate — all while being completely colourblind.",
        "image_query": "octopus underwater ocean wild"
    },
}

CATEGORIES = ["All"] + sorted(set(a["category"] for a in ANIMALS.values()))
REGIONS = ["All"] + sorted(set(a["region"] for a in ANIMALS.values()))

CONSERVATION_ORDER = {
    "Least Concern": 0,
    "Near Threatened": 1,
    "Vulnerable": 2,
    "Endangered": 3,
    "Varies by Species": 4,
}

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
if "selected_animal" not in st.session_state:
    st.session_state.selected_animal = None

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(160deg, #020617, #0a1628, #1a0a28) !important;
    min-height: 100vh;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: rgba(5,10,25,0.85) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(20px);
}
#MainMenu, footer, header { visibility: hidden; }

.stars-bg {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.star {
    position: absolute; border-radius: 50%; background: white;
    animation: twinkle var(--dur, 3s) ease-in-out infinite alternate;
    opacity: 0;
}
@keyframes twinkle {
    0%   { opacity: 0.1; transform: scale(0.8); }
    100% { opacity: 0.85; transform: scale(1.2); }
}

.page-wrap { position: relative; z-index: 1; padding: 2rem 1.5rem 4rem; }

.page-header { text-align: center; margin-bottom: 2.5rem; padding-top: 1rem; }
.page-header h1 {
    font-family: 'Outfit', sans-serif; font-weight: 800;
    font-size: clamp(2rem, 5vw, 3.2rem); letter-spacing: -0.02em;
    background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 60%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 0.4rem; line-height: 1.15;
}
.page-header p {
    font-family: 'Outfit', sans-serif; font-size: 1rem;
    color: rgba(148,163,184,0.75); font-weight: 300; letter-spacing: 0.04em; margin: 0;
}

.animal-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 1.2rem;
}

.animal-card {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px; padding: 1.5rem 1.3rem 1.3rem;
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    cursor: pointer; transition: transform 0.25s cubic-bezier(.22,.68,0,1.2), border-color 0.25s ease, box-shadow 0.25s ease;
    text-align: center;
}
.animal-card:hover {
    transform: translateY(-5px) scale(1.02);
    border-color: rgba(167,139,250,0.4);
    box-shadow: 0 0 0 1px rgba(167,139,250,0.3), 0 16px 50px -8px rgba(167,139,250,0.2), 0 6px 20px rgba(0,0,0,0.4);
}
.animal-card .emoji { font-size: 2.8rem; margin-bottom: 0.6rem; display: block; }
.animal-card .name {
    font-family: 'Outfit', sans-serif; font-weight: 700;
    font-size: 1.05rem; color: #f1f5f9; margin: 0 0 0.3rem;
}
.animal-card .cat-badge {
    display: inline-block; font-size: 0.65rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    background: rgba(167,139,250,0.12); border: 1px solid rgba(167,139,250,0.2);
    color: #a78bfa; padding: 2px 9px; border-radius: 20px;
}
.animal-card .region {
    font-size: 0.78rem; color: rgba(148,163,184,0.6); margin-top: 0.4rem;
    font-weight: 300;
}

/* DETAIL PANEL */
.detail-wrap {
    background: rgba(10,18,40,0.7);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px; padding: 2.5rem;
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    position: relative; overflow: hidden;
    margin-bottom: 2rem;
}
.detail-glow {
    position: absolute; top: -60px; right: -60px;
    width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle, rgba(167,139,250,0.2) 0%, transparent 70%);
    pointer-events: none;
}
.detail-name {
    font-family: 'Outfit', sans-serif; font-weight: 800;
    font-size: 2.4rem; color: #f1f5f9; letter-spacing: -0.02em;
    margin: 0 0 0.3rem;
}
.detail-desc {
    font-family: 'Outfit', sans-serif; font-size: 0.95rem;
    color: rgba(148,163,184,0.85); line-height: 1.7; font-weight: 300;
    margin: 1rem 0 1.5rem;
}
.detail-fun-fact {
    background: rgba(167,139,250,0.1);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 12px; padding: 1rem 1.2rem;
    margin-bottom: 1.5rem;
}
.detail-fun-fact .label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #a78bfa; margin-bottom: 0.3rem;
}
.detail-fun-fact .text {
    font-size: 0.92rem; color: #e2e8f0; line-height: 1.6; font-weight: 400;
}
.stats-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.9rem; margin-top: 1rem;
}
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 0.85rem 0.9rem;
}
.stat-label {
    font-size: 0.67rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: rgba(148,163,184,0.55); margin-bottom: 0.25rem;
}
.stat-value { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; }

.conservation-badge {
    display: inline-block; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 4px 12px; border-radius: 20px;
    border: 1px solid;
}

.back-btn {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 600;
    color: rgba(148,163,184,0.7);
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px; padding: 6px 14px;
    cursor: pointer; transition: all 0.2s;
    text-decoration: none;
}
.back-btn:hover { color: #e2e8f0; background: rgba(255,255,255,0.09); }

/* sidebar overrides */
[data-testid="stSidebar"] * { font-family: 'Outfit', sans-serif !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(15,23,42,0.7) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}
[data-testid="stSidebar"] label { color: rgba(148,163,184,0.65) !important; font-size: 0.8rem !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(15,23,42,0.7) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stSidebar"] h2 {
    color: #f1f5f9 !important; font-weight: 700 !important; font-size: 1.1rem !important;
}
[data-testid="stSidebar"] p {
    color: rgba(148,163,184,0.7) !important; font-size: 0.82rem !important;
}
.stButton > button {
    background: rgba(167,139,250,0.15) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    color: #a78bfa !important; border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important; font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(167,139,250,0.25) !important;
    border-color: #a78bfa !important;
}
</style>

<div class="stars-bg" id="starsContainer"></div>
<script>
(function() {
    var c = document.getElementById('starsContainer');
    if (!c) return;
    for (var i = 0; i < 100; i++) {
        var s = document.createElement('div');
        s.className = 'star';
        var size = Math.random() * 2.5 + 0.5;
        s.style.cssText = 'width:'+size+'px;height:'+size+'px;left:'+(Math.random()*100)+'%;top:'+(Math.random()*100)+'%;--dur:'+(Math.random()*3+2)+'s;animation-delay:'+(Math.random()*4)+'s';
        c.appendChild(s);
    }
})();
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🐾 Animal Dictionary")
    st.markdown("Explore the animal kingdom with facts, stats & more.")
    st.markdown("---")

    search = st.text_input("🔍  Search animals", placeholder="e.g. Lion, Eagle...")

    cat_filter = st.selectbox("Category", CATEGORIES)
    region_filter = st.selectbox("Region", REGIONS)

    sort_by = st.selectbox("Sort by", ["Name (A–Z)", "Conservation Status"])

    st.markdown("---")
    st.markdown(f"**{len(ANIMALS)} animals** in the database")

    if st.session_state.selected_animal:
        if st.button("← Back to all animals"):
            st.session_state.selected_animal = None
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# FILTER + SORT
# ═══════════════════════════════════════════════════════════════════════════════
def filter_animals():
    result = dict(ANIMALS)
    if search:
        result = {k: v for k, v in result.items() if search.lower() in k.lower() or search.lower() in v["description"].lower()}
    if cat_filter != "All":
        result = {k: v for k, v in result.items() if v["category"] == cat_filter}
    if region_filter != "All":
        result = {k: v for k, v in result.items() if v["region"] == region_filter}
    if sort_by == "Name (A–Z)":
        result = dict(sorted(result.items()))
    elif sort_by == "Conservation Status":
        result = dict(sorted(result.items(), key=lambda x: CONSERVATION_ORDER.get(x[1]["conservation"], 99)))
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL VIEW
# ═══════════════════════════════════════════════════════════════════════════════
def show_detail(name, data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    con_color = data["conservation_color"]

    st.markdown(f"""
    <div class="detail-wrap">
        <div class="detail-glow"></div>
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">
            <span style="font-size:3.5rem;line-height:1;">{data['emoji']}</span>
            <div>
                <div class="detail-name">{name}</div>
                <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
                    <span style="font-size:0.75rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:rgba(148,163,184,0.6);">{data['category']} · {data['region']}</span>
                    <span class="conservation-badge" style="color:{con_color};border-color:{con_color}33;background:{con_color}15;">{data['conservation']}</span>
                </div>
            </div>
        </div>
        <p class="detail-desc">{data['description']}</p>
        <div class="detail-fun-fact">
            <div class="label">✦ Did you know?</div>
            <div class="text">{data['fun_fact']}</div>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-label">Habitat</div><div class="stat-value">{data['habitat']}</div></div>
            <div class="stat-card"><div class="stat-label">Diet</div><div class="stat-value">{data['diet']}</div></div>
            <div class="stat-card"><div class="stat-label">Lifespan</div><div class="stat-value">{data['lifespan']}</div></div>
            <div class="stat-card"><div class="stat-label">Weight</div><div class="stat-value">{data['weight']}</div></div>
            <div class="stat-card"><div class="stat-label">Region</div><div class="stat-value">{data['region']}</div></div>
            <div class="stat-card"><div class="stat-label">Conservation</div><div class="stat-value" style="color:{con_color};">{data['conservation']}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Image search
    st.markdown("### 📸 Photos")
    try:
        import requests
        from PIL import Image
        from io import BytesIO

        DDG_URL = f"https://duckduckgo.com/?q={data['image_query'].replace(' ', '+')}&iax=images&ia=images"
        st.markdown(
            f'<a href="{DDG_URL}" target="_blank" style="display:inline-block;margin-bottom:1rem;font-family:Outfit,sans-serif;font-size:0.85rem;color:#a78bfa;text-decoration:none;background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.2);padding:6px 14px;border-radius:10px;">🔍 Search {name} images on DuckDuckGo ↗</a>',
            unsafe_allow_html=True
        )
    except Exception:
        pass

    # Wikimedia image attempt
    try:
        import urllib.parse, urllib.request, json as _json
        query = urllib.parse.quote(name)
        wiki_api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        req = urllib.request.Request(wiki_api, headers={"User-Agent": "AnimalDictApp/1.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            wiki_data = _json.loads(resp.read().decode())
        if "thumbnail" in wiki_data:
            img_url = wiki_data["thumbnail"]["source"].replace("/200px-", "/500px-")
            st.markdown(
                f'<img src="{img_url}" style="width:100%;max-width:520px;border-radius:16px;border:1px solid rgba(255,255,255,0.1);display:block;margin-bottom:1rem;" alt="{name}">',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<p style="font-size:0.75rem;color:rgba(148,163,184,0.4);font-family:Outfit,sans-serif;">Image via Wikipedia</p>',
                unsafe_allow_html=True
            )
    except Exception:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:3rem;text-align:center;color:rgba(148,163,184,0.4);font-family:Outfit,sans-serif;font-size:0.9rem;">{data["emoji"]} Image not available offline — search online above</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRID VIEW
# ═══════════════════════════════════════════════════════════════════════════════
def show_grid(animals):
    st.markdown("""
    <div class="page-wrap">
      <div class="page-header">
        <h1>🐾 Animal Dictionary</h1>
        <p>Discover facts, habitats & stats about the animal kingdom</p>
      </div>
    """, unsafe_allow_html=True)

    if not animals:
        st.markdown('<p style="text-align:center;color:rgba(148,163,184,0.5);font-family:Outfit,sans-serif;padding:4rem;">No animals found matching your filters.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Build grid HTML
    cards_html = '<div class="animal-grid">'
    for name in animals:
        d = animals[name]
        cards_html += f"""
        <div class="animal-card" onclick="void(0)">
            <span class="emoji">{d['emoji']}</span>
            <div class="name">{name}</div>
            <div class="cat-badge">{d['category']}</div>
            <div class="region">📍 {d['region']}</div>
        </div>
        """
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # Streamlit buttons for click (below grid, in columns)
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, name in enumerate(animals):
        with cols[i % 4]:
            if st.button(f"{animals[name]['emoji']} {name}", key=f"btn_{name}"):
                st.session_state.selected_animal = name
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.selected_animal:
    name = st.session_state.selected_animal
    show_detail(name, ANIMALS[name])
else:
    filtered = filter_animals()
    show_grid(filtered)
