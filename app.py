import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.title("📱 Telenor Clicker")

# Init session state
if 'data' not in st.session_state:
    st.session_state.data = 0
    st.session_state.auto_income_base = 0
    st.session_state.auto_income_current = 0
    st.session_state.click_power_base = 1
    st.session_state.click_power_current = 1
    st.session_state.subscription_level = "Kontantkort"
    st.session_state.upgrades = set()
    st.session_state.last_update = time.time()
    st.session_state.clicks = 0
    st.session_state.click_start_time = time.time()
    st.session_state.phone_index = 0
    st.session_state.has_router = False
    st.session_state.router_boost_until = 0
    st.session_state.router_locked_until = 0
    st.session_state.has_second_phone = False
    st.session_state.tvilling_click_boost = 1
    st.session_state.tvilling_boost_until = 0
    st.session_state.tvilling_locked_until = 0
    st.session_state.safe_protection = 0
    st.session_state.virus_risk = 0.7  # default

# Data
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
    ("iPhone 16 Pro Max", 10000, 15),
]

extras = {
    "Nettvern": (150, "+10% auto-inntekt"),
    "Nettvern+": (300, "+20% auto-inntekt"),
    "Safe": (900, "Reduserer sjansen for virus"),
    "Min Sky": (600, "Dobler klikk-verdi (kun postpaid)"),
    "Se Hvem": (400, "+2/sek auto-inntekt"),
    "Data-sim i ruter": (800, "Dobler auto-inntekt i 30 sek (kan gi virus)"),
    "Tvilling": (1200, "Dobler klikk i 30 sek (kan gi virus)"),
}

# Helper
def update_income():
    click_boost = 2 if "Min Sky" in st.session_state.upgrades and "Fast" not in st.session_state.subscription_level else 1
    phone_power = phones[st.session_state.phone_index][2]
    base_click = phone_power * click_boost
    st.session_state.click_power_base = base_click

    auto_income = subscriptions[[i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level][0]][2]

    if "Nettvern" in st.session_state.upgrades:
        auto_income *= 1.10
    if "Nettvern+" in st.session_state.upgrades:
        auto_income *= 1.20
    if "Se Hvem" in st.session_state.upgrades:
        auto_income += 2

    st.session_state.auto_income_base = auto_income

update_income()

# Virus debuff
now = time.time()
router_boost_active = now < st.session_state.router_boost_until
tvilling_boost_active = now < st.session_state.tvilling_boost_until
router_locked = now < st.session_state.router_locked_until
tvilling_locked = now < st.session_state.tvilling_locked_until

# Apply virus effects
router_debuff = 2/3 if router_locked else 1
tvilling_debuff = 2/3 if tvilling_locked else 1

st.session_state.auto_income_current = st.session_state.auto_income_base * (2 if router_boost_active else 1) * router_debuff
st.session_state.click_power_current = st.session_state.click_power_base * (2 if tvilling_boost_active else 1) * tvilling_debuff

# Passive income
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income_current
st.session_state.last_update = now

# Metrics
click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0
st.metric("📦 Datapakker", int(st.session_state.data))
st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")
st.metric("🌀 Auto-inntekt per sekund", f"{st.session_state.auto_income_current:.1f}")
st.metric("📲 Datapakker per klikk", f"{st.session_state.click_power_current:.1f}")

# Klikkeknapp
if st.button("📲 Klikk for datapakke"):
    st.session_state.data += st.session_state.click_power_current
    st.session_state.clicks += 1

# --- BOOST-knapper vises her ---
if st.session_state.has_router:
    if router_locked:
        left = int(st.session_state.router_locked_until - now)
        st.error(f"🛑 Ruter-virus aktiv: {left}s igjen")
    elif router_boost_active:
        left = int(st.session_state.router_boost_until - now)
        st.success(f"🚀 Ruter-boost aktiv i {left}s")
    else:
        if st.button("📡 Aktiver Ruter Boost (30s dobbel auto-inntekt)"):
            st.session_state.router_boost_until = now + 30
            chance = 0.4 if "Safe" in st.session_state.upgrades else 0.7
            if random.random() < chance:
                st.session_state.router_locked_until = now + 60
                if "Safe" not in st.session_state.upgrades:
                    st.warning("⚠️ Du fikk virus! Kjøp Safe for lavere risiko.")
                else:
                    st.warning("⚠️ Du fikk virus, men Safe reduserte risikoen.")
            else:
                st.success("✅ Boost aktivert uten virus!")

if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    if tvilling_locked:
        left = int(st.session_state.tvilling_locked_until - now)
        st.error(f"🛑 Tvilling-virus aktiv: {left}s igjen")
    elif tvilling_boost_active:
        left = int(st.session_state.tvilling_boost_until - now)
        st.success(f"🚀 Tvilling-boost aktiv i {left}s")
    else:
        if st.button("📡 Aktiver Tvilling Boost (30s dobbel klikk)"):
            st.session_state.tvilling_boost_until = now + 30
            chance = 0.4 if "Safe" in st.session_state.upgrades else 0.7
            if random.random() < chance:
                st.session_state.tvilling_locked_until = now + 60
                if "Safe" not in st.session_state.upgrades:
                    st.warning("⚠️ Du fikk virus! Kjøp Safe for lavere risiko.")
                else:
                    st.warning("⚠️ Du fikk virus, men Safe reduserte risikoen.")
            else:
                st.success("✅ Tvilling-boost aktivert uten virus!")

# Abonnement
st.subheader(f"📶 Nåværende abonnement: {st.session_state.subscription_level}")
current_index = next(i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level)
if current_index + 1 < len(subscriptions):
    next_sub = subscriptions[current_index + 1]
    st.info(f"🎯 Neste: {next_sub[0]} ({next_sub[1]} datapakker) – Gir {next_sub[2]} auto-inntekt/sek")
    if st.session_state.data >= next_sub[1]:
        if st.button(f"⬆️ Oppgrader til {next_sub[0]} ({next_sub[1]})"):
            st.session_state.data -= next_sub[1]
            st.session_state.subscription_level = next_sub[0]
            update_income()

# Telefon
current_phone = phones[st.session_state.phone_index]
st.subheader(f"📱 Nåværende telefon: {current_phone[0]} – {current_phone[2]} per klikk")
if st.session_state.phone_index + 1 < len(phones):
    next_phone = phones[st.session_state.phone_index + 1]
    st.info(f"📶 Neste: {next_phone[0]} ({next_phone[1]} datapakker) – Gir {next_phone[2]} per klikk")
    if st.session_state.data >= next_phone[1]:
        if st.button(f"Kjøp {next_phone[0]} ({next_phone[1]})"):
            st.session_state.data -= next_phone[1]
            st.session_state.phone_index += 1
            update_income()

# Tvilling – 2. telefon
if "Tvilling" in st.session_state.upgrades and not st.session_state.has_second_phone:
    price = 2000
    if st.session_state.data >= price:
        if st.button(f"📱 Kjøp 2. telefon ({price})"):
            st.session_state.data -= price
            st.session_state.has_second_phone = True
            st.success("2. telefon kjøpt – Tvilling aktivert!")

# Ekstrautstyr
st.subheader("🔧 Ekstrautstyr")
for name, (cost, desc) in extras.items():
    if name in st.session_state.upgrades:
        continue
    if name == "Safe" and "Tvilling" not in st.session_state.upgrades and "Data-sim i ruter" not in st.session_state.upgrades:
        continue
    if st.session_state.data >= cost:
        if st.button(f"Kjøp {name} ({cost})", help=desc):
            st.session_state.data -= cost
            st.session_state.upgrades.add(name)
            if name == "Data-sim i ruter":
                st.session_state.has_router = True
            update_income()

# Testknapp (kan fjernes senere)
if st.button("💰 Få 1000 datapakker (testing)"):
    st.session_state.data += 1000

st.caption("Laget av deg – Telenor Clicker")
