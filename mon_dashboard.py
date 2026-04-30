import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Terminal Stratégique v3.0", layout="wide")
st.title("🚀 Terminal d'Analyse : Pépères vs Pépites")

# --- BARRE LATÉRALE : LE COCKPIT ---
st.sidebar.header("🕹️ Configuration du Pilote")

# LISTE MISE À JOUR : IA, ROBOTIQUE & SANTÉ
actifs = {
    "-- SÉCURITÉ (Les Pépères) --": "^FCHI",
    "CAC 40 (France)": "^FCHI",
    "S&P 500 (USA)": "SPY",
    "LVMH (Luxe)": "MC.PA",
    "Air Liquide (Industrie)": "AI.PA",
    "Or (Refuge)": "GC=F",
    "-- TECHNOLOGIE IA (Les Pépites) --": "NVDA",
    "Nvidia (Cerveau IA)": "NVDA",
    "AMD (Challenger IA)": "AMD",
    "Thales (Défense/Drones)": "HO.PA",
    "-- ROBOTIQUE & SANTÉ --": "ISRG",
    "Intuitive Surgical (Robot Médical)": "ISRG",
    "Teradyne (Robotique Industrielle)": "TER",
    "GE HealthCare (Diagnostic IA)": "GEHC",
    "-- ÉNERGIE & SPECULATIF --": "CCJ",
    "Cameco (Uranium)": "CCJ",
    "Bitcoin (Spéculation)": "BTC-USD"
}

choix_nom = st.sidebar.selectbox("Actif à analyser :", list(actifs.keys()))
symbole = actifs[choix_nom]

if "--" in choix_nom:
    st.info("Veuillez sélectionner un actif réel dans le menu déroulant.")
    st.stop()

capital_init = st.sidebar.number_input("Capital de départ (€)", value=1000)

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Réglages de la Méthode")
mm_courte = st.sidebar.slider("Réactivité (Moyenne Courte)", 5, 50, 20)
mm_longue = st.sidebar.slider("Sagesse (Moyenne Longue)", 20, 200, 50)
stop_loss_pct = st.sidebar.slider("Parachute (Stop-Loss %)", 1, 15, 3) / 100

# --- RÉCUPÉRATION DES DONNÉES ---
@st.cache_data(ttl=3600)
def load_data(ticker):
    return yf.download(ticker, period="5y")

df = load_data(symbole)
df['MA_S'] = df['Close'].rolling(mm_courte).mean()
df['MA_L'] = df['Close'].rolling(mm_longue).mean()
df['Returns'] = df['Close'].pct_change()

# --- SIMULATION DE LA STRATÉGIE ---
position, cap_final = 0, capital_init
for i in range(1, len(df)):
    prix = df['Close'].iloc[i].item()
    if position == 0 and df['MA_S'].iloc[i] > df['MA_L'].iloc[i]:
        position = cap_final / prix
    elif position > 0:
        prix_achat = cap_final / position
        if df['MA_S'].iloc[i] < df['MA_L'].iloc[i] or prix < prix_achat * (1 - stop_loss_pct):
            cap_final, position = position * prix, 0

# --- AFFICHAGE DES INDICATEURS ---
prix_act = df['Close'].iloc[-1].item()
var_j = df['Returns'].iloc[-1].item() * 100
signal = "ACHAT (Tendance Hausse)" if df['MA_S'].iloc[-1] > df['MA_L'].iloc[-1] else "VENTE (Tendance Baisse)"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Prix Actuel", f"{prix_act:.2f}", f"{var_j:.2f}%")
c2.metric("Signal Méthode", signal)
c3.metric("Capital Final Simulé", f"{cap_final:.2f}€", f"{((cap_final/capital_init)-1)*100:.2f}%")
c4.metric("Risque (Pire Jour)", f"{df['Returns'].min()*100:.2f}%")

# --- GRAPHIQUE ---
st.markdown("---")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['Close'], color="#bdc3c7", alpha=0.6, label="Prix (Le Bruit)")
ax.plot(df['MA_S'], color="#3498db", label="Moyenne Courte (L'Esprit)")
ax.plot(df['MA_L'], color="#e67e22", linewidth=2, label="Moyenne Longue (La Sagesse)")
ax.fill_between(df.index, df['MA_S'], df['MA_L'], where=(df['MA_S'] >= df['MA_L']), color='green', alpha=0.1)
ax.legend()
st.pyplot(fig)

# --- SECTION INTELLIGENCE & ÉCOUTE ---
st.markdown("---")
st.header("🔍 Intelligence Stratégique & Écoute")
col_news1, col_news2 = st.columns(2)

with col_news1:
    st.subheader("📰 Veille Institutionnelle & Secteur")
    # Requête de recherche optimisée pour inclure la concurrence et les brevets
    search_query = f"https://www.google.com/search?q={choix_nom}+concurrence+brevets+institutionnels+investissements&tbm=nws"
    st.markdown(f"[👉 Lancer la veille sur **{choix_nom}**]({search_query})")
    st.info("Pensez à surveiller les annonces de la FDA pour le médical et les rapports de production pour la robotique.")

with col_news2:
    st.subheader("💡 Carnet de Bord du Pilote")
    st.text_area("Notes de session (2h/jour) :", 
                 placeholder="Ex: 'Intuitive Surgical gagne un brevet, signal haussier confirmé par la moyenne.'")

st.caption("Méthode : Les moyennes filtrent les excès, le parachute protège des chutes, l'écoute anticipe les ruptures.")