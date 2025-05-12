import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.title("📱 Telenor Clicker")

# --- INIT STATE ---
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
    st.session_state.tvilling_cooldown = 0
    st.session_state.tvilling_blocked = False
    st.session_state.safe_protection = 0

# Testknapp for å få 1000 datapakker
if st.button("🐞 Gi meg 1000 datapakker (TEST)"):
    st.session_state.data += 1000

# Subscriptions, phones og upgrades definisjoner (kortet her for plass)
subscriptions = [("Kontantkort", 0, 1), ("Fast 2GB", 50, 1), ("Fast 5GB", 200, 3), ("Fast 10GB", 500, 6),
                 ("Ubegrenset Enkel", 1000, 10), ("Ubegrenset Normal", 2500, 15),
                 ("Ubegrenset Optimal", 5000, 22), ("Ubegrenset Maksimal", 10000, 35)]
phones = [("Doro Phone", 0, 1), ("iPhone 7", 300, 2), ("iPhone 8", 600, 3), ("iPhone X", 900, 4),
          ("iPhone 11", 1300, 5), ("iPhone 12", 1800, 6), ("iPhone 13", 2500, 7), ("iPhone 14", 3200, 8),
          ("iPhone 15", 4000, 9), ("iPhone 16", 5000, 10), ("iPhone 16 Pro", 7000, 12), ("iPhone 16 Pro Max", 10000, 15)]
extras = {
    "Nettvern": (150, "+10% auto-inntekt"),
    "Nettvern+": (300, "+20% auto-inntekt"),
    "Safe": (900, "Reduserer sjansen for virus ved boost"),
    "Min Sky": (600, "Dobler klikk-verdi (kun postpaid)"),
    "Se Hvem": (400, "+2/sek auto-inntekt"),
    "Data-sim i ruter": (800, "Aktiverbar boost: Dobler auto-inntekt i 30 sek (krever ruter, virus kan oppstå)"),
    "Tvilling": (1200, "Krever 2. telefon – Dobler datapakker per klikk, men risikerer virus ved boost")
}

# Virusmekanikk
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income
st.session_state.last_update = now

click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0

# --- VISUALS ---
st.metric("📦 Datapakker", int(st.session_state.data))
st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")
st.metric("🌀 Auto-inntekt per sekund", f"{st.session_state.auto_income:.1f}")
st.metric("📲 Datapakker per klikk", f"{st.session_state.click_power * st.session_state.tvilling_click_boost:.1f}")

# --- KLIKK ---
if st.button("📲 Klikk for datapakke"):
    st.session_state.data += st.session_state.click_power * st.session_state.tvilling_click_boost
    st.session_state.clicks += 1

# --- TVILLING BOOST ---
if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    cooldown = 60
    duration = 30
    since_activation = now - st.session_state.tvilling_cooldown
    virus_chance = 0.4 * (1 - st.session_state.safe_protection)
    if st.session_state.tvilling_blocked:
        st.error("🤒 Tvilling-boost blokkert pga virus. Vent til cooldown er over.")
        if since_activation >= cooldown:
            st.session_state.tvilling_blocked = False
    elif since_activation >= cooldown:
        if st.button("📱 Aktiver Tvilling Boost (30 sek dobbel klikkverdi)"):
            st.session_state.tvilling_cooldown = now
            st.session_state.tvilling_click_boost = 2
            if random.random() < virus_chance:
                st.session_state.tvilling_blocked = True
                st.warning("⚠️ Du fikk virus! Tvilling er blokkert i 60 sekunder.")
                if st.session_state.safe_protection == 0:
                    st.info("💡 Tips: Kjøp 'Safe' for å redusere sjansen for virus.")
            else:
                st.success("🚀 Tvilling-boost aktiv!")
            st.experimental_rerun()
    elif since_activation < duration:
        st.success("🚀 Tvilling-boost aktiv!")
    else:
        st.session_state.tvilling_click_boost = 1
        remaining = int(cooldown - since_activation)
        st.caption(f"⏳ Tvilling nedkjøling: {remaining} sek")
