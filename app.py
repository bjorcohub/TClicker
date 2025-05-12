import streamlit as st
import time
import random

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.title("📱 Telenor Clicker")

# Initialisering
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
    st.session_state.router_blocked_until = 0
    st.session_state.has_second_phone = False
    st.session_state.tvilling_click_boost = 1
    st.session_state.tvilling_cooldown = 0
    st.session_state.tvilling_blocked_until = 0
    st.session_state.safe_protection = 0
    st.session_state.testing = False  # intern testflagg

# Test-knapp
if st.button("🧪 +1000 datapakker (test)"):
    st.session_state.data += 1000
    st.session_state.testing = True

# Abonnement
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

# Ekstra
extras = {
    "Nettvern": (150, "+10% auto-inntekt"),
    "Nettvern+": (300, "+20% auto-inntekt"),
    "Safe": (900, "Reduserer sjansen for virus ved boost"),
    "Min Sky": (600, "Dobler klikk-verdi (kun postpaid)"),
    "Se Hvem": (400, "+2/sek auto-inntekt"),
    "Data-sim i ruter": (800, "Aktiverbar boost: Dobler auto-inntekt i 30 sek (risiko for virus)"),
    "Tvilling": (1200, "Dobler datapakker per klikk (krever 2. telefon, risiko for virus)"),
}

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
    ("iPhone 16 Pro Max", 10000, 15),
]

# Oppdater auto inntekt
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income
st.session_state.last_update = now

# Klikk-metrikk
click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0

# Vis statistikk
st.metric("📦 Datapakker", int(st.session_state.data))
st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")
st.metric("🌀 Auto-inntekt/sek", f"{st.session_state.auto_income:.1f}")
st.metric("📲 Datapakker per klikk", f"{st.session_state.click_power * st.session_state.tvilling_click_boost:.1f}")

# Klikk-knapp
if st.button("📲 Klikk for datapakke"):
    st.session_state.data += st.session_state.click_power * st.session_state.tvilling_click_boost
    st.session_state.clicks += 1

# Nåværende abonnement
st.subheader(f"📶 Nåværende abonnement: {st.session_state.subscription_level}")

# Neste abonnement
current_index = next(i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level)
if current_index + 1 < len(subscriptions):
    next_sub = subscriptions[current_index + 1]
    st.info(f"🎯 Neste: {next_sub[0]} ({next_sub[1]} datapakker) – Gir {next_sub[2]} auto-inntekt/sek")
    if st.session_state.data >= next_sub[1]:
        if st.button(f"⬆️ Oppgrader til {next_sub[0]}", help=f"Gir {next_sub[2]} auto-inntekt/sek"):
            st.session_state.data -= next_sub[1]
            st.session_state.subscription_level = next_sub[0]
            st.session_state.auto_income = next_sub[2]
            if "Min Sky" in st.session_state.upgrades and "Fast 2GB" not in next_sub[0]:
                st.session_state.click_power = phones[st.session_state.phone_index][2] * 2
else:
    st.success("🏆 Du har nådd Ubegrenset Maksimal!")

# Nåværende og neste telefon
current_phone = phones[st.session_state.phone_index]
st.subheader(f"📱 Nåværende telefon: {current_phone[0]} – {current_phone[2]} per klikk")

if st.session_state.phone_index + 1 < len(phones):
    next_phone = phones[st.session_state.phone_index + 1]
    st.info(f"📶 Neste: {next_phone[0]} ({next_phone[1]} datapakker) – Gir {next_phone[2]} per klikk")
    if st.session_state.data >= next_phone[1]:
        if st.button(f"Kjøp {next_phone[0]}", help=f"Gir {next_phone[2]} datapakker per klikk"):
            st.session_state.data -= next_phone[1]
            st.session_state.phone_index += 1
            power = phones[st.session_state.phone_index][2]
            st.session_state.click_power = power * (2 if "Min Sky" in st.session_state.upgrades and "Fast 2GB" not in st.session_state.subscription_level else 1)

# Kjøp 2. telefon for Tvilling
if "Tvilling" in st.session_state.upgrades and not st.session_state.has_second_phone:
    phone2_price = 2000
    if st.session_state.data >= phone2_price:
        if st.button(f"📱 Kjøp 2. telefon for Tvilling ({phone2_price})", help="Nødvendig for å aktivere Tvilling – dobler klikk"):
            st.session_state.data -= phone2_price
            st.session_state.has_second_phone = True
            st.session_state.tvilling_click_boost = 2
            st.success("Tvilling aktivert – dobbel datapakke per klikk!")

# Ekstrautstyr
st.subheader("🔧 Ekstrautstyr")
upcoming = []
for name, (cost, desc) in extras.items():
    if name not in st.session_state.upgrades:
        if name == "Safe" and "Tvilling" not in st.session_state.upgrades and "Data-sim i ruter" not in st.session_state.upgrades:
            continue
        if st.session_state.data >= cost:
            if st.button(f"Kjøp {name} ({cost})", help=desc):
                st.session_state.data -= cost
                st.session_state.upgrades.add(name)
                if name == "Nettvern":
                    st.session_state.auto_income *= 1.10
                elif name == "Nettvern+":
                    st.session_state.auto_income *= 1.20
                elif name == "Safe":
                    st.session_state.safe_protection = 0.8
                elif name == "Min Sky" and "Fast 2GB" not in st.session_state.subscription_level:
                    st.session_state.click_power *= 2
                elif name == "Se Hvem":
                    st.session_state.auto_income += 2
                elif name == "Data-sim i ruter":
                    st.session_state.has_router = True
        else:
            upcoming.append((name, cost, desc))

if upcoming:
    st.subheader("🔜 Kommer snart:")
    for name, cost, desc in sorted(upcoming, key=lambda x: x[1]):
        st.text(f"{name} ({cost}) – {desc}")

# Ruter boost
if "Data-sim i ruter" in st.session_state.upgrades and st.session_state.has_router:
    virus_chance = 0.4 * (1 - st.session_state.safe_protection)
    cooldown = 60
    active = 30
    since = now - st.session_state.router_cooldown
    blocked = now < st.session_state.router_blocked_until

    if blocked:
        time_left = int(st.session_state.router_blocked_until - now)
        st.error(f"🚫 Ruter låst pga virus! Vent {time_left} sekunder.")
    elif since >= cooldown:
        if st.button("📡 Aktiver Ruter Boost (30 sek)"):
            st.session_state.router_cooldown = now
            if random.random() < virus_chance:
                st.session_state.router_blocked_until = now + 60
                st.warning("⚠️ Du fikk virus! Boost mislyktes og må vente 60 sek.")
                if "Safe" not in st.session_state.upgrades:
                    st.info("💡 Tips: Kjøp Safe for å redusere risikoen for virus.")
            else:
                st.success("🚀 Ruter boost aktiv!")
                st.session_state.auto_income *= 2
    elif since < active:
        st.success("🚀 Ruter boost aktiv!")
    else:
        st.caption(f"⏳ Ruter nedkjøling: {int(cooldown - since)} sek")

# Tvilling boost
if "Tvilling" in st.session_state.upgrades and st.session_state.has_second_phone:
    virus_chance = 0.4 * (1 - st.session_state.safe_protection)
    cooldown = 60
    since = now - st.session_state.tvilling_cooldown
    blocked = now < st.session_state.tvilling_blocked_until

    if blocked:
        time_left = int(st.session_state.tvilling_blocked_until - now)
        st.error(f"🚫 Tvilling låst pga virus! Vent {time_left} sekunder.")
    elif since >= cooldown:
        if st.button("📳 Aktiver Tvilling Boost (30 sek dobbel klikk)"):
            st.session_state.tvilling_cooldown = now
            if random.random() < virus_chance:
                st.session_state.tvilling_blocked_until = now + 60
                st.warning("⚠️ Du fikk virus! Boost mislyktes og må vente 60 sek.")
                if "Safe" not in st.session_state.upgrades:
                    st.info("💡 Tips: Kjøp Safe for å redusere risikoen for virus.")
            else:
                st.success("🚀 Tvilling boost aktiv!")
                st.session_state.tvilling_click_boost = 4
    elif since < 30:
        st.success("🚀 Tvilling boost aktiv!")
    else:
        st.session_state.tvilling_click_boost = 2
        st.caption(f"⏳ Tvilling nedkjøling: {int(cooldown - since)} sek")

st.caption("Laget av deg – Telenor Clicker")
