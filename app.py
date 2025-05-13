# Full Telenor Clicker Streamlit-app med forbedret boost/virus-logikk

import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")

# Initialiser spilldata
if "datapakker" not in st.session_state:
    st.session_state.datapakker = 0
    st.session_state.click_value = 1
    st.session_state.auto_income = 0
    st.session_state.last_auto_income_time = time.time()
    st.session_state.upgrades = set()
    st.session_state.has_router = False
    st.session_state.has_second_phone = False
    st.session_state.safe_protection = 0
    st.session_state.router_cooldown = 0
    st.session_state.router_boost_end = 0
    st.session_state.router_blocked = False
    st.session_state.original_auto_income = 0
    st.session_state.tvilling_cooldown = 0
    st.session_state.tvilling_boost_end = 0
    st.session_state.tvilling_blocked = False
    st.session_state.tvilling_click_boost = 1
    st.session_state.last_click_time = time.time()
    st.session_state.total_clicks = 0

now = time.time()

# Automatisk inntekt
elapsed = now - st.session_state.last_auto_income_time
if elapsed >= 1:
    income = int(st.session_state.auto_income * elapsed)
    st.session_state.datapakker += income
    st.session_state.last_auto_income_time = now

st.title("📱 Telenor Clicker")

# Klikk for datapakke
if st.button("📦 Klikk for datapakke"):
    st.session_state.total_clicks += 1
    click_value = int(st.session_state.click_value * st.session_state.tvilling_click_boost)
    st.session_state.datapakker += click_value

# Boost-knapper og nedtellinger vises her
# Ruter Boost
if "Data-sim i ruter" in st.session_state.upgrades and st.session_state.has_router:
    cooldown = 60
    duration = 30
    since_activation = now - st.session_state.router_cooldown
    virus_chance = 0.6 if st.session_state.safe_protection == 0 else 0.3

    if st.session_state.router_blocked and since_activation >= cooldown:
        st.session_state.router_blocked = False
        st.session_state.auto_income = st.session_state.original_auto_income  # Reset etter virus

    if st.session_state.router_blocked:
        remaining = int(cooldown - since_activation)
        st.error(f"🚫 Ruter-virus aktiv. Boost låst i {remaining}s.")
    elif since_activation >= cooldown:
        if st.button("📡 Aktiver Ruter Boost (30s dobbel auto-inntekt)"):
            st.session_state.router_cooldown = now
            st.session_state.original_auto_income = st.session_state.auto_income
            if random.random() < virus_chance:
                st.session_state.router_blocked = True
                st.session_state.auto_income = int(st.session_state.auto_income * 0.66)
                if st.session_state.safe_protection == 0:
                    st.info("Tips: Kjøp 'Safe' for å redusere sjansen for virus.")
                st.warning("⚠️ Du fikk virus! Auto-inntekt redusert midlertidig.")
            else:
                st.session_state.auto_income *= 2
                st.session_state.router_boost_end = now + duration
                st.success("🚀 Ruter-boost aktiv!")
    elif now < st.session_state.router_boost_end:
        remaining = int(st.session_state.router_boost_end - now)
        st.success(f"🚀 Ruter-boost aktiv! {remaining}s igjen")
    else:
        remaining = int(cooldown - since_activation)
        st.caption(f"⏳ Ruter nedkjøling: {remaining}s")

# Tvilling Boost
if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    tvilling_cooldown = 60
    tvilling_duration = 30
    since_activation = now - st.session_state.tvilling_cooldown
    virus_chance = 0.6 if st.session_state.safe_protection == 0 else 0.3

    if st.session_state.tvilling_blocked and since_activation >= tvilling_cooldown:
        st.session_state.tvilling_blocked = False
        st.session_state.tvilling_click_boost = 1

    if st.session_state.tvilling_blocked:
        remaining = int(tvilling_cooldown - since_activation)
        st.error(f"🚫 Tvilling-virus aktiv. Boost låst i {remaining}s.")
    elif since_activation >= tvilling_cooldown:
        if st.button("📶 Aktiver Tvilling Boost (30s dobbel klikkverdi)"):
            st.session_state.tvilling_cooldown = now
            if random.random() < virus_chance:
                st.session_state.tvilling_blocked = True
                st.session_state.tvilling_click_boost = 0.66
                if st.session_state.safe_protection == 0:
                    st.info("Tips: Kjøp 'Safe' for å redusere sjansen for virus.")
                st.warning("⚠️ Du fikk virus! Klikkverdi redusert midlertidig.")
            else:
                st.session_state.tvilling_click_boost = 2
                st.session_state.tvilling_boost_end = now + tvilling_duration
                st.success("🚀 Tvilling-boost aktiv!")
    elif now < st.session_state.tvilling_boost_end:
        remaining = int(st.session_state.tvilling_boost_end - now)
        st.success(f"🚀 Tvilling-boost aktiv! {remaining}s igjen")
    else:
        remaining = int(tvilling_cooldown - since_activation)
        st.caption(f"⏳ Tvilling nedkjøling: {remaining}s")

# Statistikk
st.subheader("📊 Statistikk")
st.write(f"Datapakker: {int(st.session_state.datapakker)}")
st.write(f"Klikkverdi: {int(st.session_state.click_value * st.session_state.tvilling_click_boost)}")
st.write(f"Auto-inntekt: {int(st.session_state.auto_income)} /sek")
st.write(f"Totale klikk: {st.session_state.total_clicks}")

# Oppgraderinger
st.subheader("⚙️ Oppgraderinger")
if st.button("Kjøp Abonnement (100 DP)"):
    if st.session_state.datapakker >= 100:
        st.session_state.datapakker -= 100
        st.session_state.click_value += 1
        st.success("📶 Du oppgraderte abonnementet ditt!")

if st.button("Kjøp ny telefon (500 DP)"):
    if st.session_state.datapakker >= 500:
        st.session_state.datapakker -= 500
        st.session_state.has_second_phone = True
        st.session_state.upgrades.add("Tvilling")
        st.success("📱 Du kjøpte en ekstra telefon!")

if st.button("Kjøp Data-sim i ruter (1000 DP)"):
    if st.session_state.datapakker >= 1000:
        st.session_state.datapakker -= 1000
        st.session_state.has_router = True
        st.session_state.auto_income += 1
        st.session_state.upgrades.add("Data-sim i ruter")
        st.success("🌐 Du aktiverte ruter med data-sim!")

if st.button("Kjøp Safe (700 DP)"):
    if st.session_state.datapakker >= 700 and (st.session_state.has_second_phone or st.session_state.has_router):
        st.session_state.datapakker -= 700
        st.session_state.safe_protection = 1
        st.success("🛡️ Du har kjøpt Safe og redusert sjansen for virus!")
    elif not (st.session_state.has_second_phone or st.session_state.has_router):
        st.warning("Du må ha Tvilling eller Data-sim i ruter før du kan kjøpe Safe.")
