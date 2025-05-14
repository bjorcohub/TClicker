import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.markdown("<h1 style='text-align: center;'>📱 Telenor Clicker</h1>", unsafe_allow_html=True)

# === INITIALIZE ===
if 'data' not in st.session_state:
    st.session_state.data = 0
    st.session_state.auto_income = 0
    st.session_state.base_auto_income = 0
    st.session_state.click_power = 1
    st.session_state.base_click_power = 1
    st.session_state.subscription_level = "Kontantkort"
    st.session_state.upgrades = set()
    st.session_state.last_update = time.time()
    st.session_state.clicks = 0
    st.session_state.click_start_time = time.time()
    st.session_state.phone_index = 0
    st.session_state.has_router = False
    st.session_state.router_cooldown = 0
    st.session_state.router_boost_time = 0
    st.session_state.router_blocked = False
    st.session_state.router_virus_active = False
    st.session_state.has_second_phone = False
    st.session_state.tvilling_click_boost = 1
    st.session_state.tvilling_cooldown = 0
    st.session_state.tvilling_boost_time = 0
    st.session_state.tvilling_blocked = False
    st.session_state.tvilling_virus_active = False
    st.session_state.safe_protection = 0

# === CONSTANTS ===
subscriptions = [
    ("Kontantkort", 0, 1),
    ("Fast 2GB", 50, 1),
    ("Fast 5GB", 200, 3),
    ("Fast 10GB", 500, 6),
    ("Ubegrenset Enkel", 1000, 10),
    ("Ubegrenset Normal", 2500, 15),
    ("Ubegrenset Optimal", 5000, 22),
    ("Ubegrenset Maksimal", 10000, 35),
]

phones = [
    ("Doro Phone", 0, 1),
    ("iPhone 7", 300, 2),
    ("iPhone 8", 600, 3),
    ("iPhone X", 900, 4),
    ("iPhone 11", 1300, 5),
    ("iPhone 12", 1800, 6),
    ("iPhone 13", 2500, 7),
    ("iPhone 14", 3200, 8),
    ("iPhone 15", 4000, 9),
    ("iPhone 16", 5000, 10),
    ("iPhone 16 Pro", 7000, 12),
    ("iPhone 16 Pro Max", 10000, 15)
]

extras = {
    "Nettvern": (150, "+10% auto-inntekt"),
    "Nettvern+": (300, "+20% auto-inntekt"),
    "Safe": (900, "Reduserer sjansen for virus"),
    "Min Sky": (600, "Dobler klikk-verdi (kun postpaid)"),
    "Se Hvem": (400, "+2/sek auto-inntekt"),
    "Data-sim i ruter": (800, "Boost: Dobler auto-inntekt i 30 sek (virus mulig)"),
    "Tvilling": (1200, "Krever 2. telefon – Dobler klikk i 30 sek (virus mulig)"),
    "SPLITT": (2500, "Gir 5% mer auto-inntekt permanent")
}

# === LOGIC ===
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income
st.session_state.last_update = now

click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0

# === METRICS ===
col1, col2, col3 = st.columns(3)
col1.metric("📦 Datapakker", int(st.session_state.data))
col2.metric("🖱️ Klikk/min", f"{clicks_per_minute:.1f}")
col3.metric("🌀 Auto/s", f"{st.session_state.auto_income:.1f}")

st.markdown(
    f"<h2 style='text-align:center; color:#2E86AB;'>📲 {st.session_state.click_power:.1f} datapakker per klikk</h2>",
    unsafe_allow_html=True
)

# === CLICK ===
click_btn = st.button("📲 Klikk for datapakke", key="click_button")
if click_btn:
    st.session_state.data += st.session_state.click_power
    st.session_state.clicks += 1
    st.balloons()

# === BOOST ===
def handle_boost(name):
    cooldown = 60
    duration = 30
    chance = 0.7 if st.session_state.safe_protection == 0 else 0.35
    now = time.time()

    if name == "router":
        elapsed = now - st.session_state.router_cooldown
        active = now - st.session_state.router_boost_time < duration

        if active:
            remaining = int(duration - (now - st.session_state.router_boost_time))
            st.success(f"🚀 Ruter aktiv ({remaining}s igjen)")
        elif elapsed < cooldown:
            remaining = int(cooldown - elapsed)
            st.info(f"⏳ Ruter klar om {remaining}s")
        else:
            if st.button("📡 Aktiver Ruter Boost"):
                st.session_state.router_cooldown = now
                st.session_state.router_boost_time = now
                if random.random() < chance:
                    st.session_state.auto_income = st.session_state.base_auto_income * 0.66
                    st.warning("☣️ Virus! Auto-inntekt redusert")
                else:
                    st.session_state.auto_income = st.session_state.base_auto_income * 2
    elif name == "tvilling":
        elapsed = now - st.session_state.tvilling_cooldown
        active = now - st.session_state.tvilling_boost_time < duration

        if active:
            remaining = int(duration - (now - st.session_state.tvilling_boost_time))
            st.success(f"🚀 Tvilling aktiv ({remaining}s igjen)")
        elif elapsed < cooldown:
            remaining = int(cooldown - elapsed)
            st.info(f"⏳ Tvilling klar om {remaining}s")
        else:
            if st.button("📶 Aktiver Tvilling Boost"):
                st.session_state.tvilling_cooldown = now
                st.session_state.tvilling_boost_time = now
                if random.random() < chance:
                    st.session_state.click_power = st.session_state.base_click_power * 0.66
                    st.warning("☣️ Virus! Klikk redusert")
                else:
                    st.session_state.click_power = st.session_state.base_click_power * 2

if "Data-sim i ruter" in st.session_state.upgrades and st.session_state.has_router:
    handle_boost("router")
if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    handle_boost("tvilling")

# === SUBSCRIPTION ===
st.subheader("📶 Abonnement")
current_index = next(i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level)
if current_index + 1 < len(subscriptions):
    next_sub = subscriptions[current_index + 1]
    st.info(f"🎯 Neste: {next_sub[0]} ({next_sub[1]}) – Gir {next_sub[2]}/sek")
    if st.session_state.data >= next_sub[1]:
        if st.button(f"⬆️ Oppgrader til {next_sub[0]} ({next_sub[1]})"):
            st.session_state.data -= next_sub[1]
            st.session_state.subscription_level = next_sub[0]
            st.session_state.auto_income = next_sub[2]
            st.session_state.base_auto_income = next_sub[2]

# === PHONES ===
st.subheader("📱 Telefon")
current_phone = phones[st.session_state.phone_index]
st.info(f"Nåværende: {current_phone[0]} – {current_phone[2]}/klikk")

if st.session_state.phone_index + 1 < len(phones):
    next_phone = phones[st.session_state.phone_index + 1]
    if st.session_state.data >= next_phone[1]:
        if st.button(f"📲 Kjøp {next_phone[0]} ({next_phone[1]})"):
            st.session_state.data -= next_phone[1]
            st.session_state.phone_index += 1
            new_power = phones[st.session_state.phone_index][2]
            st.session_state.base_click_power = new_power
            st.session_state.click_power = new_power

# === SECOND PHONE FOR TVILLING ===
if "Tvilling" in st.session_state.upgrades and not st.session_state.has_second_phone:
    phone2_price = 2000
    if st.session_state.data >= phone2_price:
        if st.button(f"📱 Kjøp 2. telefon for Tvilling ({phone2_price})"):
            st.session_state.data -= phone2_price
            st.session_state.has_second_phone = True
            st.success("Tvilling aktivert!")

# === EXTRAS ===
st.subheader("🔧 Ekstrautstyr")
for name, (cost, desc) in extras.items():
    if name in st.session_state.upgrades:
        st.markdown(f"<div style='color:green;'>✅ {name}</div>", unsafe_allow_html=True)
    elif (name == "Safe") and ("Tvilling" not in st.session_state.upgrades and "Data-sim i ruter" not in st.session_state.upgrades):
        continue
    elif st.session_state.data >= cost:
        if st.button(f"💎 Kjøp {name} ({cost})", help=desc):
            st.session_state.data -= cost
            st.session_state.upgrades.add(name)
            if name == "Nettvern":
                st.session_state.auto_income *= 1.10
            elif name == "Nettvern+":
                st.session_state.auto_income *= 1.20
            elif name == "Safe":
                st.session_state.safe_protection = 0.5
            elif name == "Min Sky":
                st.session_state.click_power *= 2
            elif name == "Se Hvem":
                st.session_state.auto_income += 2
            elif name == "Data-sim i ruter":
                st.session_state.has_router = True
            elif name == "SPLITT":
                st.session_state.auto_income *= 1.05

# === DEBUG ===
if st.button("🧪 +1000 datapakker"):
    st.session_state.data += 1000

st.caption("Laget av deg – Telenor Clicker")
