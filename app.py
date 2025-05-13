import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.title("📱 Telenor Clicker")

# === INIT ===
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

# === DEFINITIONS ===

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
    "Data-sim i ruter": (800, "Aktiverbar boost: Dobler auto-inntekt i 30 sek (virus mulig)"),
    "Tvilling": (1200, "Krever 2. telefon – Dobler klikk midlertidig (virus mulig)")
}

# === INCOME CALCULATION ===
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income
st.session_state.last_update = now

# === CLICK PER MINUTE ===
click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0

# === METRICS ===
st.metric("📦 Datapakker", int(st.session_state.data))
st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")
#st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")
st.metric("🌀 Auto-inntekt per sekund", f"{st.session_state.auto_income:.1f}")
st.metric("📲 Datapakker per klikk", f"{st.session_state.click_power:.1f}")

# === CLICK BUTTON ===
if st.button("📲 Klikk for datapakke"):
    st.session_state.data += st.session_state.click_power
    st.session_state.clicks += 1

# === BOOST + VIRUS LOGIC (TVILLING + RUTER) ===
def handle_boost(name):
    if name == "router":
        cooldown = 60
        duration = 30
        chance = 0.7 if st.session_state.safe_protection == 0 else 0.35
        elapsed = now - st.session_state.router_cooldown

        if st.session_state.router_blocked:
            remaining = int(cooldown - elapsed)
            st.error(f"🚫 Boost deaktivert pga virus! ({remaining}s igjen)")
            st.error(f"🚫 Ruter deaktivert pga virus! ({remaining}s igjen)")
        elif elapsed >= cooldown:
            if st.button("📡 Aktiver Ruter Boost"):
                st.session_state.router_cooldown = now
                st.session_state.router_boost_time = now
                if random.random() < chance:
                    st.session_state.router_blocked = True
                    st.session_state.router_virus_active = True
                    st.session_state.auto_income = st.session_state.base_auto_income * 0.66
                    if st.session_state.safe_protection == 0:
                        st.info("💡 Tips: Kjøp Safe for lavere risiko for virus.")
                else:
                    st.session_state.auto_income = st.session_state.base_auto_income * 2
        elif now - st.session_state.router_boost_time < duration:
            remaining = int(duration - (now - st.session_state.router_boost_time))
            st.success(f"🚀 Ruter-boost aktiv ({remaining}s igjen)")
        elif st.session_state.router_virus_active:
            st.session_state.auto_income = st.session_state.base_auto_income
            st.session_state.router_virus_active = False
        else:
            st.session_state.auto_income = st.session_state.base_auto_income

    elif name == "tvilling":
        cooldown = 60
        duration = 30
        chance = 0.7 if st.session_state.safe_protection == 0 else 0.35
        elapsed = now - st.session_state.tvilling_cooldown

        if st.session_state.tvilling_blocked:
            remaining = int(cooldown - elapsed)
            st.error(f"🚫 Tvilling-boost låst pga virus! ({remaining}s igjen)")
        elif elapsed >= cooldown:
            if st.button("📶 Aktiver Tvilling Boost"):
                st.session_state.tvilling_cooldown = now
                st.session_state.tvilling_boost_time = now
                if random.random() < chance:
                    st.session_state.tvilling_blocked = True
                    st.session_state.tvilling_virus_active = True
                    st.session_state.click_power = st.session_state.base_click_power * 0.66
                    if st.session_state.safe_protection == 0:
                        st.info("💡 Tips: Kjøp Safe for lavere risiko for virus.")
                else:
                    st.session_state.click_power = st.session_state.base_click_power * 2
        elif now - st.session_state.tvilling_boost_time < duration:
            remaining = int(duration - (now - st.session_state.tvilling_boost_time))
            st.success(f"🚀 Tvilling-boost aktiv ({remaining}s igjen)")
        elif st.session_state.tvilling_virus_active:
            st.session_state.click_power = st.session_state.base_click_power
            st.session_state.tvilling_virus_active = False
        else:
            st.session_state.click_power = st.session_state.base_click_power

# === BOOST KNAPPER UNDER KLIKK ===
if "Data-sim i ruter" in st.session_state.upgrades and st.session_state.has_router:
    handle_boost("router")

if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    handle_boost("tvilling")

# === SUBSCRIPTION ===
st.subheader(f"📶 Nåværende abonnement: {st.session_state.subscription_level}")
current_index = next(i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level)
if current_index + 1 < len(subscriptions):
    next_sub = subscriptions[current_index + 1]
    st.info(f"🎯 Neste: {next_sub[0]} ({next_sub[1]} datapakker) – Gir {next_sub[2]}/sek")
    if st.session_state.data >= next_sub[1]:
        if st.button(f"⬆️ Oppgrader til {next_sub[0]} ({next_sub[1]})"):
            st.session_state.data -= next_sub[1]
            st.session_state.subscription_level = next_sub[0]
            st.session_state.auto_income = next_sub[2]
            st.session_state.base_auto_income = next_sub[2]
            if "Min Sky" in st.session_state.upgrades and "Fast 2GB" not in next_sub[0]:
                st.session_state.click_power = st.session_state.base_click_power * 2

# === PHONES ===
current_phone = phones[st.session_state.phone_index]
st.subheader(f"📱 Nåværende telefon: {current_phone[0]} – {current_phone[2]} per klikk")

if st.session_state.phone_index + 1 < len(phones):
    next_phone = phones[st.session_state.phone_index + 1]
    st.info(f"📶 Neste: {next_phone[0]} ({next_phone[1]}) – {next_phone[2]} per klikk")
    if st.session_state.data >= next_phone[1]:
        if st.button(f"Kjøp {next_phone[0]} ({next_phone[1]})"):
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
    else:
        st.warning(f"Du trenger {phone2_price} datapakker")

# === EXTRAS ===
st.subheader("🔧 Ekstrautstyr")
for name, (cost, desc) in extras.items():
    if name not in st.session_state.upgrades:
        if (name == "Safe") and ("Tvilling" not in st.session_state.upgrades and "Data-sim i ruter" not in st.session_state.upgrades):
            continue
        if st.session_state.data >= cost:
            if st.button(f"Kjøp {name} ({cost})", help=desc):
                st.session_state.data -= cost
                st.session_state.upgrades.add(name)
                if name == "Nettvern":
                    st.session_state.auto_income *= 1.10
                    st.session_state.base_auto_income = st.session_state.auto_income
                elif name == "Nettvern+":
                    st.session_state.auto_income *= 1.20
                    st.session_state.base_auto_income = st.session_state.auto_income
                elif name == "Safe":
                    st.session_state.safe_protection = 0.5
                elif name == "Min Sky":
                    st.session_state.click_power *= 2
                elif name == "Se Hvem":
                    st.session_state.auto_income += 2
                    st.session_state.base_auto_income = st.session_state.auto_income
                elif name == "Data-sim i ruter":
                    st.session_state.has_router = True

# === TESTBUTTON (valgfritt)
if st.button("💾 Test: +1000 datapakker"):
    st.session_state.data += 1000
#if st.button("💾 Test: +1000 datapakker"):
    #st.session_state.data += 1000

st.caption("Laget av deg – Telenor Clicker")
