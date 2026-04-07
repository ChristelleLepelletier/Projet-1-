import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import io
import os
st.write(os.listdir())

st.title("📊 Dashboard interactif des ventes")




# charger ton fichier CSV dans ton app avec pandas
#chemin = r"C:\Users\chris\Documents\PYTHON\exercices_a_faire\Chatgpt\intermediaire\ventes.csv"
df = pd.read_csv("ventes.csv")

df["total"] = df["prix"] * df["quantite"]
df["date"] = pd.to_datetime(df["date"])

# --- SIDEBAR ---
st.sidebar.markdown("## ⚙️ Paramètres du dashboard")
st.sidebar.markdown("---")

# Section Filtres
st.sidebar.markdown("### 🎯 Filtres principaux")

ville = st.sidebar.selectbox(
    "🏙️ Ville",
    ["Toutes"] + list(df["ville"].unique())
)

produit = st.sidebar.selectbox(
    "📦 Produit",
    ["Tous"] + list(df["produit"].unique())
)

date_selection = st.sidebar.date_input(
    "📅 Date",
    value=df["date"].min()
)

st.sidebar.markdown("---")

# Section Informations
st.sidebar.markdown("### ℹ️ Informations")
st.sidebar.info(
    "Utilisez les filtres ci-dessus pour ajuster les données affichées dans le dashboard."
)

st.sidebar.markdown("---")

# Section Export
st.sidebar.markdown("### 📤 Export des données")


# 🔹 Filtres
ville = st.selectbox("Choisir une ville", ["Toutes"] + list(df["ville"].unique()))
produit = st.selectbox("Choisir un produit", ["Tous"] + list(df["produit"].unique()))

df_filtre = df.copy()

if ville != "Toutes":
    df_filtre = df_filtre[df_filtre["ville"] == ville]

if produit != "Tous":
    df_filtre = df_filtre[df_filtre["produit"] == produit]

# 🔹 Tableau
st.subheader("📋 Données filtrées")
st.dataframe(df_filtre)

# 🔹 Graphique 1
# 1. un graphique en ligne
st.subheader("📈 Ventes par date")
ventes_date = df_filtre.groupby("date")["total"].sum().reset_index()
fig1 = px.line(ventes_date, x="date", y="total", markers=True)
st.plotly_chart(fig1)

# 🔹 Graphique 2
st.subheader("📊 Ventes par produit")
ventes_prod = df_filtre.groupby("produit")["total"].sum().reset_index()
st.write(ventes_prod)
fig2 = px.bar(ventes_prod, x="produit", y="total", color="produit")
st.plotly_chart(fig2)

# Quelle opération pandas permet de calculer le chiffre d’affaires total à partir de la colonne "total" ?
chiffre_affaires = df_filtre["total"].sum()

# Comment calculer le panier moyen à partir de df_filtre ?
panier_moyen = df_filtre["total"].mean()

# Comment calculer le nombre de commandes à partir de df_filtre ?
nombre_commandes = df_filtre.shape[0]

# Comment afficher 3 KPI sur la même ligne avec Streamlit ?
col1, col2, col3 = st.columns(3)
col1.metric("Chiffre d'affaires", f"{chiffre_affaires:,.2f} €")
col2.metric("Panier moyen", f"{panier_moyen:,.2f} €")
col3.metric("Nombre de commandes", f"{nombre_commandes}")

# Quelle fonction Streamlit permet de sélectionner une date ?
date_selection = st.date_input("Sélectionner une date", value=df_filtre["date"].min())

# Comment filtrer df_filtre pour ne garder que : les lignes avec une date égale à date_selection ?
df_filtre_date = df_filtre[df_filtre["date"] == pd.to_datetime(date_selection)]

# Comment calculer le total des ventes par produit à partir de df_filtre_date ?
ventes_prod_date = df_filtre_date.groupby("produit")["total"].sum().reset_index()

# Comment trouver le produit qui a généré le plus de chiffre d’affaires à partir de ventes_prod_date ?
produit_top = ventes_prod_date.loc[ventes_prod_date["total"].idxmax()]["produit"]
# Comment afficher le produit top dans Streamlit ?
st.write(f"Le produit qui a généré le plus de chiffre d'affaires le {date_selection} est : **{produit_top}**")
# Comment afficher le produit top dans Streamlit ?
st.metric("Produit le plus vendu", produit_top)

####################################################################################################################
# ÉTAPE 1 — Top 3 produits
# À partir de ventes_prod_date, comment :
# trier par "total" décroissant
ventes_prod_date_trie = ventes_prod_date.sort_values(by="total", ascending=False)
# garder les 3 premières lignes
top3_produits = ventes_prod_date_trie.head(3)

# ÉTAPE 2 — Classement clients
# Comment calculer le total des ventes par client à partir de df_filtre ?
ventes_client = df_filtre.groupby("client")["total"].sum().reset_index()
# Comment trier ventes_client du plus gros au plus petit chiffre d’affaires ?
ventes_client_trie = ventes_client.sort_values(by="total", ascending = False)

# ÉTAPE 3 — Export Excel
# Quelle fonction pandas permet d’exporter un DataFrame en fichier Excel ?
df_filtre.to_excel("ventes_filtre.xlsx", index=False)
# Dans Streamlit, quelle fonction permet de créer un bouton pour télécharger un fichier ?
with open("ventes_filtre.xlsx", "rb") as f:
    st.download_button("Télécharger les données filtrées", data=f, file_name="ventes_filtre.xlsx")

#buffer = io.BytesIO()
#df_filtre.to_excel(buffer, index=False)
#buffer.seek(0)

#st.download_button("Télécharger", data=buffer, file_name="ventes_filtre.xlsx")

# DERNIÈRE ÉTAPE — Mise en ligne
