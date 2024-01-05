import streamlit as st
from functions import scrape_data
import csv

favicon_path = "favicon.ico"

st.set_page_config(
    page_title="KaliHub",
    page_icon=favicon_path
)
st.title("Bienvenue sur KaliHub ")
st.sidebar.header("Créé par")
st.sidebar.text("Richard Kali")

# Variables pour stocker les données scrapées
scraped_data = []

# Vérifie si le bouton "Démarrer la collecte avec cet URL" a été cliqué
if st.button("Démarrer la collecte avec cet URL"):
    st.write("La collecte est en cours...")

    # Afficher une barre de progression pendant le chargement
    progress_bar = st.progress(0)

    # Appel de la fonction scrape_data seulement si l'URL est valide
    scraped_data = scrape_data(25, 1, progress_bar)

    if not scraped_data:
        st.write("Aucune donnée n'a été récupérée.")
    #else:
        # with open('produits.csv', mode='w', newline='', encoding='utf-8') as file:
        #     writer = csv.writer(file)
        #     # Écrire les en-têtes
        #     writer.writerow(['ID','Titres', 'Prix', 'Liens', 'Images'])

        #     for data in scraped_data:
        #         writer.writerow([data['id_article'],data['title'], data['price'], data['link'], data['image']])
        #         # st.write(f"Titre : {data['title']}")
        #         # st.write(f"Prix : {data['price']}")
        #         # if data['image'] is not None:
        #         #     st.image(data['image'], caption='Image', use_column_width=True)
        #         # else:
        #         #     st.write("Aucune image disponible")

st.write("je vais remplir plus tard")
