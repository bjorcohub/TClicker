import streamlit as st
import time

st.set_page_config(page_title="Telenor Clicker", layout="centered")
st.title("📱 Telenor Clicker")

# Initialize session state
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
    st.session_state.has_second_phone = False
    st.session_state.tvilling_click_boost = 1

# Subscription tiers
subscriptions = [
    ("Kontantkort", 0, 1),
    ("Fast 2GB", 50, 1),
    ("Fast 5GB", 200, 2),
    ("Fast 10GB", 500, 4),
    ("Ubegrenset Enkel", 1000, 6),
    ("Ubegrenset Normal", 2500, 9),
    ("Ubegrenset Optimal", 5000, 13),
    ("Ubegrenset Maksimal", 10000, 20),
]

# Extra upgrades
extras = {
    "Nettvern": (150, "+10% auto-inntekt"),
    "Nettvern+": (300, "+20% auto-inntekt"),
    "Safe": (500, "+1/sek og beskyttelse"),
    "Min Sky": (600, "Dobler klikk-verdi (kun postpaid)"),
    "Se Hvem": (400, "+2/sek auto-inntekt"),
    "Data-sim i ruter": (800, "Aktiverbar boost: Dobler auto-inntekt i 30 sek (krever ruter)"),
    "Tvilling": (1200, "Krever 2. telefon – Dobler datapakker per klikk")
}

# Phones to buy
phones = [
    ("Doro Phone", 0, 1),
    ("iPhone 7", 300, 1.2),
    ("iPhone 8", 600, 1.4),
    ("iPhone X", 900, 1.6),
    ("iPhone 11", 1300, 1.8),
    ("iPhone 12", 1800, 2.0),
    ("iPhone 13", 2500, 2.2),
    ("iPhone 14", 3200, 2.5),
    ("iPhone 15", 4000, 2.8),
    ("iPhone 16", 5000, 3.0),
    ("iPhone 16 Pro", 7000, 3.5),
    ("iPhone 16 Pro Max", 10000, 4.0)
]

# Update auto income over time
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income
st.session_state.last_update = now

# Calculate clicks per minute
click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0

# Show metrics
st.metric("📦 Datapakker", int(st.session_state.data))
st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")
st.metric("🔘 Datapakker per klikk", f"{st.session_state.click_power * st.session_state.tvilling_click_boost:.1f}")

# Clicking button
if st.button("📲 Klikk for datapakke"):
    st.session_state.data += st.session_state.click_power * st.session_state.tvilling_click_boost
    st.session_state.clicks += 1

# Show next subscription goal
current_index = next(i for i, s in enumerate(subscriptions) if s[0] == st.session_state.subscription_level)
if current_index + 1 < len(subscriptions):
    next_sub = subscriptions[current_index + 1]
    st.info(f"🎯 Neste abonnement: {next_sub[0]} ({next_sub[1]} datapakker)")
else:
    st.success("🏆 Du har nådd Ubegrenset Maksimal!")

# Upgrade subscription
if current_index + 1 < len(subscriptions):
    next_sub = subscriptions[current_index + 1]
    if st.session_state.data >= next_sub[1]:
        if st.button(f"⬆️ Oppgrader til {next_sub[0]} ({next_sub[1]} datapakker)"):
            st.session_state.data -= next_sub[1]
            st.session_state.subscription_level = next_sub[0]
            st.session_state.auto_income = next_sub[2]
            if "Min Sky" in st.session_state.upgrades and "Fast 2GB" not in next_sub[0]:
                st.session_state.click_power = phones[st.session_state.phone_index][2] * 2

# Buy phones
st.subheader("📱 Telefoner")
if not st.session_state.has_second_phone:
    if st.session_state.phone_index + 1 < len(phones):
        next_phone = phones[st.session_state.phone_index + 1]
        st.info(f"📶 Neste telefon: {next_phone[0]} ({next_phone[1]} datapakker)")
        if st.session_state.data >= next_phone[1]:
            if st.button(f"Kjøp {next_phone[0]} ({next_phone[1]})"):
                st.session_state.data -= next_phone[1]
                st.session_state.phone_index += 1
                new_power = phones[st.session_state.phone_index][2]
                if "Min Sky" in st.session_state.upgrades and "Fast 2GB" not in st.session_state.subscription_level:
                    st.session_state.click_power = new_power * 2
                else:
                    st.session_state.click_power = new_power
else:
    st.caption("📱 Du har allerede to telefoner!")

# Second phone for Tvilling
if "Tvilling" in st.session_state.upgrades and not st.session_state.has_second_phone:
    phone2_price = 2000
    if st.session_state.data >= phone2_price:
        if st.button(f"📱 Kjøp 2. telefon for Tvilling ({phone2_price})"):
            st.session_state.data -= phone2_price
            st.session_state.has_second_phone = True
            st.session_state.tvilling_click_boost = 2
            st.success("Tvilling aktivert – dobbel datapakke per klikk!")
    else:
        st.warning(f"Du trenger {phone2_price} datapakker til 2. telefon for å aktivere Tvilling")

# Extra upgrades
st.subheader("🔧 Ekstrautstyr")
upcoming_upgrades = []
for name, (cost, desc) in extras.items():
    if name not in st.session_state.upgrades:
        if st.session_state.data >= cost:
            if st.button(f"Kjøp {name} ({cost}) - {desc}"):
                st.session_state.data -= cost
                st.session_state.upgrades.add(name)
                if name == "Nettvern":
                    st.session_state.auto_income *= 1.10
                elif name == "Nettvern+":
                    st.session_state.auto_income *= 1.20
                elif name == "Safe":
                    st.session_state.auto_income += 1
                elif name == "Min Sky" and "Fast 2GB" not in st.session_state.subscription_level:
                    st.session_state.click_power *= 2
                elif name == "Se Hvem":
                    st.session_state.auto_income += 2
                elif name == "Data-sim i ruter":
                    st.session_state.has_router = True
                elif name == "Tvilling" and st.session_state.has_second_phone:
                    st.session_state.tvilling_click_boost = 2
        else:
            upcoming_upgrades.append((name, cost, desc))

if upcoming_upgrades:
    st.subheader("🔜 Neste ekstrautstyr du kan spare til:")
    for name, cost, desc in sorted(upcoming_upgrades, key=lambda x: x[1]):
        st.text(f"{name} ({cost}) - {desc}")

# Data-sim boost button
if "Data-sim i ruter" in st.session_state.upgrades and st.session_state.has_router:
    cooldown = 60  # sekunder
    active_duration = 30
    since_activation = now - st.session_state.router_cooldown
    if since_activation >= cooldown:
        if st.button("📡 Aktiver Ruter Boost (30 sek dobbel auto-inntekt)"):
            st.session_state.router_cooldown = now
            st.session_state.auto_income *= 2
            st.experimental_rerun()
    elif since_activation < active_duration:
        st.success("🚀 Ruter-boost aktiv!")
    else:
        remaining = int(cooldown - since_activation)
        st.caption(f"⏳ Ruter nedkjøling: {remaining} sek")

# Show current phone
st.caption(f"📱 Nåværende telefon: {phones[st.session_state.phone_index][0]}")
st.caption("Laget av deg – Telenor Clicker")
