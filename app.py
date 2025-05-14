import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.title("📱 Telenor Clicker")

# === SESSION INIT ===
if "data" not in st.session_state:
    st.session_state.update({
        "data": 0,
        "clicks": 0,
        "click_power": 1,
        "base_click_power": 1,
        "auto_income": 0,
        "base_auto_income": 0,
        "subscription_level": "Kontantkort",
        "upgrades": set(),
        "last_update": time.time(),
        "click_start_time": time.time(),
        "phone_index": 0,
        "has_router": False,
        "router_cooldown": 0,
        "router_boost_start": 0,
        "router_blocked": False,
        "router_virus": False,
        "has_second_phone": False,
        "tvilling_cooldown": 0,
        "tvilling_boost_start": 0,
        "tvilling_blocked": False,
        "tvilling_virus": False,
        "safe_protection": 0
    })

# === CONSTANTS ===
subscriptions = [
    ("Kontantkort", 0, 1),
    ("Fast 2GB", 50, 1),
    ("Fast 5GB", 200, 3),
    ("Fast 10GB", 500, 6),
    ("Ubegrenset Enkel", 1000, 10),
    ("Ubegrenset SPLITT", 2500, 15),
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
    "Safe": (900, "Reduserer sjanse for virus"),
    "Min Sky": (600, "Dobler klikkverdi (kun postpaid)"),
    "Se Hvem": (400, "+2/sek auto-inntekt"),
    "Data-sim i ruter": (800, "Aktiver boost: Dobler auto-inntekt midlertidig"),
    "Tvilling": (1200, "Krever 2. telefon – Dobler klikk midlertidig"),
}

# === TIME UPDATE ===
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income
st.session_state.last_update = now

# === METRICS ===
clicks_per_minute = (
    (st.session_state.clicks / (now - st.session_state.click_start_time)) * 60
    if now - st.session_state.click_start_time > 0
    else 0
)

col1, col2, col3 = st.columns(3)
col1.metric("📦 Datapakker", int(st.session_state.data))
col2.metric("🖱️ Klikk/min", f"{clicks_per_minute:.1f}")
col3.metric("⚡ Auto-inntekt", f"{st.session_state.auto_income:.1f}/s")

# === CLICK ===
if st.button("📲 Klikk for datapakke", use_container_width=True):
    st.session_state.data += st.session_state.click_power
    st.session_state.clicks += 1

st.caption(f"Per klikk: {st.session_state.click_power:.1f}")

# === BOOST SYSTEM ===
def boost_logic(name, cooldown, duration, boost_factor, virus_factor):
    now = time.time()
    if name == "router":
        cooldown_start = st.session_state.router_cooldown
        boost_start = st.session_state.router_boost_start
        virus_active = st.session_state.router_virus
        blocked = st.session_state.router_blocked
        base = st.session_state.base_auto_income
        value_key = "auto_income"
        virus_flag = "router_virus"
    else:
        cooldown_start = st.session_state.tvilling_cooldown
        boost_start = st.session_state.tvilling_boost_start
        virus_active = st.session_state.tvilling_virus
        blocked = st.session_state.tvilling_blocked
        base = st.session_state.base_click_power
        value_key = "click_power"
        virus_flag = "tvilling_virus"

    chance = 0.7 if st.session_state.safe_protection == 0 else 0.35

    if now < boost_start + duration:
        remaining = int(boost_start + duration - now)
        st.success(f"🚀 {name.capitalize()} boost aktiv ({remaining}s igjen)")
    elif virus_active:
        setattr(st.session_state, value_key, base)
        setattr(st.session_state, virus_flag, False)
    elif now < cooldown_start + cooldown:
        remaining = int(cooldown_start + cooldown - now)
        st.warning(f"⏳ {name.capitalize()} tilgjengelig om {remaining}s")
    else:
        if st.button(f"⚡ Aktiver {name.capitalize()} Boost"):
            setattr(st.session_state, f"{name}_cooldown", now)
            setattr(st.session_state, f"{name}_boost_start", now)
            if random.random() < chance:
                setattr(st.session_state, f"{name}_blocked", True)
                setattr(st.session_state, virus_flag, True)
                setattr(st.session_state, value_key, base * virus_factor)
                st.error(f"💀 Virus! {name.capitalize()} gir nå bare 2/3 effekt!")
            else:
                setattr(st.session_state, value_key, base * boost_factor)

# === BOOST BUTTONS ===
if "Data-sim i ruter" in st.session_state.upgrades and st.session_state.has_router:
    boost_logic("router", cooldown=60, duration=30, boost_factor=2, virus_factor=0.66)

if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    boost_logic("tvilling", cooldown=60, duration=30, boost_factor=2, virus_factor=0.66)

# === UPGRADE SECTION ===
st.subheader("📶 Abonnement")
current_sub = next(i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level)
if current_sub + 1 < len(subscriptions):
    name, cost, income = subscriptions[current_sub + 1]
    st.info(f"Neste: {name} ({cost} datapakker) – {income}/sek")
    if st.session_state.data >= cost:
        if st.button(f"🔼 Oppgrader til {name}"):
            st.session_state.data -= cost
            st.session_state.subscription_level = name
            st.session_state.auto_income = income
            st.session_state.base_auto_income = income
            if "Min Sky" in st.session_state.upgrades:
                st.session_state.click_power = st.session_state.base_click_power * 2

# === PHONE SECTION ===
st.subheader("📱 Telefon")
phone_name, phone_cost, phone_power = phones[st.session_state.phone_index]
st.write(f"Nåværende: {phone_name} – {phone_power}/klikk")
if st.session_state.phone_index + 1 < len(phones):
    name, cost, power = phones[st.session_state.phone_index + 1]
    st.info(f"Neste: {name} ({cost} datapakker) – {power}/klikk")
    if st.session_state.data >= cost:
        if st.button(f"📲 Kjøp {name}"):
            st.session_state.data -= cost
            st.session_state.phone_index += 1
            st.session_state.base_click_power = power
            st.session_state.click_power = power

# === SECOND PHONE FOR TVILLING ===
if "Tvilling" in st.session_state.upgrades and not st.session_state.has_second_phone:
    if st.session_state.data >= 2000:
        if st.button("📱 Kjøp 2. telefon for Tvilling (2000)"):
            st.session_state.data -= 2000
            st.session_state.has_second_phone = True
            st.success("✅ Tvilling aktivert!")
    else:
        st.warning("Du trenger 2000 datapakker for 2. telefon")

# === EXTRAS ===
st.subheader("🧩 Ekstrautstyr")
for name, (price, desc) in extras.items():
    if name not in st.session_state.upgrades:
        if (name == "Safe") and not (
            "Tvilling" in st.session_state.upgrades or "Data-sim i ruter" in st.session_state.upgrades
        ):
            continue
        if st.session_state.data >= price:
            if st.button(f"Kjøp {name} ({price})", help=desc):
                st.session_state.data -= price
                st.session_state.upgrades.add(name)
                if name == "Nettvern":
                    st.session_state.base_auto_income *= 1.1
                elif name == "Nettvern+":
                    st.session_state.base_auto_income *= 1.2
                elif name == "Safe":
                    st.session_state.safe_protection = 0.5
                elif name == "Min Sky":
                    st.session_state.click_power *= 2
                elif name == "Se Hvem":
                    st.session_state.base_auto_income += 2
                elif name == "Data-sim i ruter":
                    st.session_state.has_router = True

# === TESTING BUTTON ===
if st.button("💾 Test: +1000 datapakker"):
    st.session_state.data += 1000

st.caption("Laget av deg – Telenor Clicker")
