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
    "Data-sim": (350, "+1 klikk hvert 5. sek"),
    "Tvilling": (1000, "Dobler auto-inntekt midlertidig")
}

# Update auto income over time
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.data += elapsed * st.session_state.auto_income
st.session_state.last_update = now

# Calculate clicks per minute
click_elapsed = now - st.session_state.click_start_time
clicks_per_minute = (st.session_state.clicks / click_elapsed * 60) if click_elapsed > 0 else 0

# UI Layout
st.metric("📦 Datapakker", int(st.session_state.data))
st.metric("🖱️ Klikk per minutt", f"{clicks_per_minute:.1f}")

if st.button("📲 Klikk for datapakke"):
    st.session_state.data += st.session_state.click_power
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
                st.session_state.click_power = 2

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
                    st.session_state.click_power = 2
                elif name == "Se Hvem":
                    st.session_state.auto_income += 2
                # Data-sim og Tvilling kan implementeres senere
        else:
            upcoming_upgrades.append((name, cost, desc))

if upcoming_upgrades:
    st.subheader("🔜 Neste ekstrautstyr du kan spare til:")
    for name, cost, desc in sorted(upcoming_upgrades, key=lambda x: x[1]):
        st.text(f"{name} ({cost}) - {desc}")

st.caption("Laget av deg – Telenor Clicker")
