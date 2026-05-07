import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Mon premier dashboard")

# Exemple de données
data = pd.DataFrame({
    "Produit": ["A", "B", "C"],
    "Ventes": [100, 150, 90]
})

# Affiche le tableau
st.write("Tableau des ventes :", data)

# Graphique
fig, ax = plt.subplots()
ax.bar(data["Produit"], data["Ventes"])
st.pyplot(fig)

# Sélection interactive
produit_sel = st.selectbox("Choisir un produit :", data["Produit"])
st.write(f"Ventes pour {produit_sel} :", data[data["Produit"] == produit_sel]["Ventes"].values[0])
