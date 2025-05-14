# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App config
st.set_page_config(page_title="Clôture Avril 2025", layout="wide")

# CSS for custom style
st.markdown("""
    <style>
        .big-font {font-size:24px !important;}
        .metric-box {
            padding: 1rem; border-radius: 1rem;
            background-color: #f0f4f8; text-align: center;
            box-shadow: 1px 1px 10px rgba(0,0,0,0.05);
        }
        .section-title {
            font-size: 20px;
            margin-top: 2rem;
            color: #1f4e79;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='big-font'><b>👋 Bienvenue Kheiriddine !</b> — Clôture Avril 2025</div>", unsafe_allow_html=True)

# KPIs
st.markdown("<div class='section-title'>📊 Indicateurs clés</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='metric-box'><h5>⏳ Jours restants</h5><h3>3</h3></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-box'><h5>🔍 Anomalies</h5><h3>12</h3></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='metric-box'><h5>📈 Progression</h5><h3>80%</h3></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='metric-box'><h5>💶 Ajustements</h5><h3>25.4k€</h3></div>", unsafe_allow_html=True)

# Quick actions
st.markdown("<div class='section-title'>⚡ Accès rapides</div>", unsafe_allow_html=True)
cols = st.columns(6)
actions = ["Importer mes pièces", "Configurer les règles", "Configurer alertes", "Assignation tâches", "Éditer les rapports", "Partager les résultats"]
for i in range(6):
    cols[i].button(actions[i])

# Planning
st.markdown("<div class='section-title'>🗓️ Planning de clôture</div>", unsafe_allow_html=True)
tasks = {
    "Rapprochement bancaire": 90,
    "Comptes clients": 80,
    "Provisions": 40,
    "Consolidation": 20
}
for task, val in tasks.items():
    st.text(task)
    st.progress(val)

# Top anomalies
st.markdown("<div class='section-title'>🔴 Top anomalies à traiter</div>", unsafe_allow_html=True)
anomalies_df = pd.DataFrame({
    "Anomalie": ["Écart banque SG", "Provision client Durand", "Facture Martin", "TVA déductible"],
    "Montant (€)": [6240, 12750, 3820, 2430],
    "Statut": ["Urgent", "En attente", "Manquante", "Erronée"]
})
st.dataframe(anomalies_df, use_container_width=True)

# Documents chart
st.markdown("<div class='section-title'>📄 Documents téléchargés</div>", unsafe_allow_html=True)
doc_data = pd.Series([3, 2, 1, 1], index=["Termes SIREC", "Bilan 2024", "Grand Livre", "Balance clients"])
fig, ax = plt.subplots()
doc_data.plot(kind='bar', ax=ax, color='#4a90e2')
st.pyplot(fig)

# Invoices
st.markdown("<div class='section-title'>📁 Suivi factures</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("À traiter", "34")
c2.metric("Validées", "0")
c3.metric("Refusées", "0")

# Ajustements
st.markdown("<div class='section-title'>✅ Ajustements</div>", unsafe_allow_html=True)
st.progress(0.72)
st.caption("138 / 190 utilisateurs traités")

# Optional upload
st.markdown("### 📤 Import de fichiers")
uploaded = st.file_uploader("Importer un document")
if uploaded:
    st.success(f"✅ Fichier {uploaded.name} importé avec succès.")

