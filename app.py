import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.title("📱 Telenor Clicker")

# Init session state
if 'data' not in st.session_state:
    st.session_state.data = 0
    st.session_state.auto_income = 0
    st.session_state.click_power = 1
    st.session_state.subscription_level = "Kontantkort"
    st.session_state.upgrades = set()
    st.session_state.last_update = time.time()
    st.session_state.clicks = 0
    st.session_state.click_start_time = time.time()
    st.session_state.phone_index = 0
    st.session_state.has_router = False
    st.session_state.router_cooldown = 0
    st.session_state.router_blocked = False
    st.session_state.has_second_phone = False
    st.session_state.tvilling_click_boost = 1
    st.session_state.safe_protection = 0
    st.session_state.tvilling_blocked = False
    st.session_state.tvilling_cooldown = 0

# TESTKNAPP – gir 1000 datapakker
if st.button("🧪 Gi 1000 datapakker (TEST)"):
    st.session_state.data += 1000

# Abonnementer
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

# Telefoner
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

# Ekstrautstyr
extras = {
    "Nettvern": (150, "+10% auto-inntekt"),
    "Nettvern+": (300, "+20% auto-inntekt"),
    "Safe": (900, "Reduserer sjansen for virus ved boost"),
    "Min Sky": (600, "Dobler klikk-verdi (kun postpaid)"),
    "Se Hvem": (400, "+2/sek auto-inntekt"),
    "Data-sim i ruter": (800, "Boost: Dobler auto-inntekt i 30 sek"),
    "Tvilling": (1200, "Krever 2. telefon – Dobler datapakker per klikk")
}

# Oppdater auto-inntekt
now = time.time()
elapsed = now - st.session_state.last_update
income_multiplier = 2 if "Ruter Boost" in st.session_state else 1
virus_multiplier = 2/3 if st.session_state.router_blocked else 1
st.session_state.data += elapsed * st.session_state.auto_income * income_multiplier * virus_multiplier
st.session_state.last_update = now

# Statistikk
click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0
effective_click_power = st.session_state.click_power * st.session_state.tvilling_click_boost
if st.session_state.tvilling_blocked:
    effective_click_power *= 2/3

st.metric("📦 Datapakker", int(st.session_state.data))
st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")
st.metric("🌀 Auto-inntekt/sek", f"{st.session_state.auto_income:.1f}")
st.metric("📲 Per klikk", f"{effective_click_power:.1f}")

# Klikk-knapp
if st.button("📲 Klikk for datapakke"):
    st.session_state.data += effective_click_power
    st.session_state.clicks += 1

# Abonnement
st.subheader(f"📶 Nåværende abonnement: {st.session_state.subscription_level}")
curr_idx = next(i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level)
if curr_idx + 1 < len(subscriptions):
    next_sub = subscriptions[curr_idx + 1]
    st.info(f"🎯 Neste: {next_sub[0]} ({next_sub[1]} datapakker) – {next_sub[2]} auto-inntekt/sek")
    if st.session_state.data >= next_sub[1] and st.button(f"⬆️ Oppgrader til {next_sub[0]}", help=f"Gir {next_sub[2]} auto-inntekt/sek"):
        st.session_state.data -= next_sub[1]
        st.session_state.subscription_level = next_sub[0]
        st.session_state.auto_income = next_sub[2]
        if "Min Sky" in st.session_state.upgrades and "Fast 2GB" not in next_sub[0]:
            st.session_state.click_power = phones[st.session_state.phone_index][2] * 2

# Telefon
curr_phone = phones[st.session_state.phone_index]
st.subheader(f"📱 Nåværende telefon: {curr_phone[0]} – {curr_phone[2]} per klikk")
if st.session_state.phone_index + 1 < len(phones):
    next_phone = phones[st.session_state.phone_index + 1]
    st.info(f"📶 Neste: {next_phone[0]} ({next_phone[1]} datapakker) – {next_phone[2]} per klikk")
    if st.session_state.data >= next_phone[1] and st.button(f"Kjøp {next_phone[0]}", help=f"Gir {next_phone[2]} per klikk"):
        st.session_state.data -= next_phone[1]
        st.session_state.phone_index += 1
        new_power = phones[st.session_state.phone_index][2]
        st.session_state.click_power = new_power * 2 if "Min Sky" in st.session_state.upgrades and "Fast 2GB" not in st.session_state.subscription_level else new_power

# Tvilling – andre telefon
if "Tvilling" in st.session_state.upgrades and not st.session_state.has_second_phone:
    if st.session_state.data >= 2000 and st.button("📱 Kjøp 2. telefon for Tvilling (2000)", help="Kreves for å aktivere boost"):
        st.session_state.data -= 2000
        st.session_state.has_second_phone = True
        st.session_state.tvilling_click_boost = 2

# Ekstrautstyr
st.subheader("🔧 Ekstrautstyr")
for name, (cost, desc) in extras.items():
    if name not in st.session_state.upgrades:
        if name == "Safe" and "Data-sim i ruter" not in st.session_state.upgrades and "Tvilling" not in st.session_state.upgrades:
            continue
        if st.session_state.data >= cost and st.button(f"Kjøp {name} ({cost})", help=desc):
            st.session_state.data -= cost
            st.session_state.upgrades.add(name)
            if name == "Nettvern":
                st.session_state.auto_income *= 1.10
            elif name == "Nettvern+":
                st.session_state.auto_income *= 1.20
            elif name == "Safe":
                st.session_state.safe_protection = 0.65
            elif name == "Min Sky" and "Fast 2GB" not in st.session_state.subscription_level:
                st.session_state.click_power *= 2
            elif name == "Se Hvem":
                st.session_state.auto_income += 2
            elif name == "Data-sim i ruter":
                st.session_state.has_router = True

# Ruter-boost
cooldown = 60
boost_duration = 30
now = time.time()
virus_chance = 0.65 * (1 - st.session_state.safe_protection)

# --- Ruter BOOST ---
since_ruter = now - st.session_state.router_cooldown
boost_active = 0 <= since_ruter <= boost_duration

if "Data-sim i ruter" in st.session_state.upgrades and st.session_state.has_router:
    if st.session_state.router_blocked:
        remaining = int(cooldown - since_ruter)
        st.error(f"🚫 Ruter-boost deaktivert pga virus. Tid igjen: {remaining} sek")
        if remaining <= 0:
            st.session_state.router_blocked = False
    elif boost_active:
        remaining = int(boost_duration - since_ruter)
        st.success(f"🚀 Ruter-boost aktiv! Tid igjen: {remaining} sek")
    elif since_ruter >= cooldown:
        if st.button("📡 Aktiver Ruter Boost"):
            st.session_state.router_cooldown = now
            if random.random() < virus_chance:
                st.session_state.router_blocked = True
                st.warning("⚠️ Du fikk virus ved aktivering! Boost blokkert i 60 sek.")
                if "Safe" not in st.session_state.upgrades:
                    st.info("💡 Kjøp 'Safe' for lavere virus-sjanse.")
            else:
                st.success("✅ Ruter-boost aktiv i 30 sek")

# --- Tvilling BOOST ---
since_tvilling = now - st.session_state.tvilling_cooldown
tvilling_boost_active = 0 <= since_tvilling <= boost_duration

if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    if st.session_state.tvilling_blocked:
        remaining = int(cooldown - since_tvilling)
        st.error(f"📴 Tvilling-boost deaktivert pga virus. Tid igjen: {remaining} sek")
        if remaining <= 0:
            st.session_state.tvilling_blocked = False
    elif tvilling_boost_active:
        remaining = int(boost_duration - since_tvilling)
        st.success(f"📶 Tvilling-boost aktiv! Tid igjen: {remaining} sek")
    elif since_tvilling >= cooldown:
        if st.button("📲 Aktiver Tvilling Boost"):
            st.session_state.tvilling_cooldown = now
            if random.random() < virus_chance:
                st.session_state.tvilling_blocked = True
                st.warning("⚠️ Tvilling boost mislyktes – virus!")
                if "Safe" not in st.session_state.upgrades:
                    st.info("💡 Tips: Kjøp 'Safe' for lavere risiko.")
            else:
                st.success("✅ Tvilling boost aktiv i 30 sek")
