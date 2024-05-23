import streamlit as st
import pandas as pd
import base64
from tmdb_API import *
from mod_function import *


def background()->None:
    """
    Définit une image de fond personnalisée pour l'application Streamlit.
    """

    @st.cache_data
    def get_img_as_base64(file)->str:
        """
        Lit un fichier image et l'encode en une chaîne base64.

        Args:
            file (str): Chemin vers le fichier image.

        Returns:
            str: Chaîne encodée en base64 de l'image.
        """
        # Ouvre le fichier et lit les données
        with open(file, "rb") as f:
            data = f.read()
        # Encode les données en base64 et les retourne sous forme de chaîne
        return base64.b64encode(data).decode()

    # Convertit le fichier image en une chaîne base64
    img = get_img_as_base64(r"img/Wallpaper.JPG")

    # Définit le style CSS pour l'image de fond et d'autres éléments de l'interface utilisateur
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: 130%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    # Applique les styles CSS à l'application Streamlit
    st.markdown(page_bg_img, unsafe_allow_html=True)



def menu_navigation()->None:
    """
    Configure un menu de navigation dans la barre latérale de l'application Streamlit.
    """
    
    # Ajoute un sous-titre "Menu" à la barre latérale
    st.sidebar.subheader("Menu")

    # Ajoute un lien vers la page "index.py" dans la barre latérale avec une étiquette et une icône
    st.sidebar.page_link("index.py", label="Recommandation", icon="🏠")
    
    # Ajoute un lien vers la page "pages/nouvelle_page.py" dans la barre latérale avec une étiquette et une icône
    st.sidebar.page_link("pages/nouvelle_page.py", label="Détails Film", icon="1️⃣")
    
    # Ajoute un lien vers la page "pages/FlixCreuse.py" dans la barre latérale avec une étiquette et une icône
    st.sidebar.page_link("pages/FlixCreuse.py", label="Dashboard", icon="2️⃣")



def menu_select_genres(df_film:pd.DataFrame)->tuple[pd.DataFrame, list]:
    """
    Affiche un menu de sélection de genres dans la barre latérale de l'application Streamlit
    et filtre les films en fonction des genres sélectionnés.

    Args:
        df_film (pd.DataFrame): DataFrame contenant les informations sur les films.

    Returns:
        tuple: Un tuple contenant le DataFrame filtré et la liste des genres sélectionnés.
    """

    #extraction des différents genres
    genre_films = df_film['genres'].explode().unique()

    # Affichage d'une boîte de sélection multiple pour les genres dans la barre latérale
    options_genre_film = st.sidebar.multiselect(
        "Selection du genre",
        genre_films, 
        [])

    def filter_by_genre(genre_list:list, options:list)->bool:
        """
        Filtre les films par genre.

        Args:
            genre_list (list): Liste des genres d'un film.
            options (list): Liste des genres sélectionnés.

        Returns:
            bool: True si le film contient au moins un des genres sélectionnés, sinon False.
        """
        return any(genres in options for genres in genre_list)


    if options_genre_film != []:
        df_film = df_film[df_film['genres'].apply(lambda x: filter_by_genre(x, options_genre_film))]

    return df_film, options_genre_film




def menu_select_paysProd(df_film:pd.DataFrame)->tuple[pd.DataFrame, list]:
    """
    Permet de filtrer les données des films en fonction des pays de production sélectionnés.

    Args:
        df_film (pd.DataFrame): Le DataFrame contenant les données des films.

    Returns:
        tuple[pd.DataFrame, list]: Un tuple contenant le DataFrame filtré et la liste des pays de production sélectionnés.
    """
    #extraction des différents genres
    pays_prod = df_film['production_countries'].explode().unique()

    # Affichage d'une boîte de sélection multiple pour les genres dans la barre latérale
    options_pays_prod = st.sidebar.multiselect(
        "Selection des pays de production",
        pays_prod, 
        [])

    def filter_by_pays_prod(pays_prod_list:list, options:list)->bool:
        """
        Fonction de filtre pour vérifier si un film appartient à l'un des pays sélectionnés.

        Args:
            pays_prod_list (list): Liste des pays de production du film.
            options (list): Liste des pays de production sélectionnés.

        Returns:
            bool: True si le film appartient à l'un des pays sélectionnés, False sinon.
        """
        return any(pays_prod in options for pays_prod in pays_prod_list)


    if options_pays_prod != []:
        df_film = df_film[df_film['production_countries'].apply(lambda x: filter_by_pays_prod(x, options_pays_prod))]

    return df_film, options_pays_prod



def menu_select_real(df_film:pd.DataFrame, df_name:pd.DataFrame):

    # Filtrer les valeurs indésirables
    filtered_realisateur = df_film['directors'].dropna().explode()
    # Obtenir les 20 valeurs les plus fréquentes
    top_realisateur = filtered_realisateur.value_counts().head(20)
    # Extraire les valeurs uniques de 'nconst' et 'primaryName' de BDD_clean_avant_ML_name
    nconst_primaryName_mapping = df_name[['nconst', 'primaryName']].set_index('nconst')['primaryName'].to_dict()
    # Remplacer les 'nconst' par 'primaryName'
    top_realisateur_names = top_realisateur.rename(index=nconst_primaryName_mapping).reset_index()

    # inversion des clé, valeur du dictionnaire
    new_dic_real = {}
    for k, v in nconst_primaryName_mapping.items():
        new_dic_real[v] = k

    option_realisateur = st.sidebar.selectbox(
        "Sélection d'un réalisateur",
        top_realisateur_names, 
        index=None)

    def filter_by_director(director_list, options):
        return any(director in options for director in director_list)

    if option_realisateur != None:
        nconst_select = new_dic_real[str(option_realisateur)]
        df_film = df_film[df_film['directors'].apply(lambda x: filter_by_director(x, nconst_select))]

    return df_film, option_realisateur



def menu_select_date(df_film:pd.DataFrame)->tuple[pd.DataFrame, int, int]:
    """
    Affiche un sélecteur de plage de dates dans la barre latérale de l'application Streamlit
    et filtre les films en fonction des dates sélectionnées.

    Args:
        df_film (pd.DataFrame): DataFrame contenant les informations sur les films.

    Returns:
        tuple: Un tuple contenant le DataFrame filtré et les années de début et de fin sélectionnées.
    """

    #Faire une sélection des date avec un slider
    start_year, end_year = st.sidebar.select_slider(
            'Selection une étendue d\'année',
            options= sorted(df_film['year_release_date'].unique()),
            value=(df_film['year_release_date'].unique().min(), df_film['year_release_date'].unique().max()))
    
    # Filtrer les films en fonction de la plage d'années sélectionnée
    df_film = df_film[(df_film['year_release_date']>= start_year) & (df_film ['year_release_date']<= end_year)]

    return df_film, start_year, end_year



def diplay_title()->None:
    """
    Affiche une image de titre centrée dans l'application Streamlit.
    """

    # Chemin de l'image de titre
    chemin_titre = "https://dim2960.github.io/Flixoucreuse.png"

    # HTML pour afficher l'image centrée
    html_titre = f"""
            <div style='display: flex; justify-content: center;'>
                <img src="{chemin_titre}" width=50%>  
            </div>
    """

    # Affichage de l'image de titre en utilisant st.markdown pour interpréter le HTML
    st.markdown(html_titre, unsafe_allow_html=True)



def display_reco(list_film2:list, df_film:pd.DataFrame)->None:
    """
    Affiche les recommandations de films sous forme de posters cliquables dans l'application Streamlit.

    Args:
        list_film2 (list): Liste des identifiants de films recommandés.
        df_film (pd.DataFrame): DataFrame contenant les informations sur les films.
    """

    st.write('Vos 5 recommandations')

    # Affichage des posters des films recommandés sur des colonnes
    cols = st.columns(5)

    for i, element in enumerate(list_film2[1:6]):

        # Filtrer le DataFrame pour obtenir les informations du film recommandé
        chemin_poster = df_film[df_film['tconst'] == element].reset_index()

        with cols[i]:
            # Créer le HTML pour afficher le poster du film avec un lien cliquable
            html2 = f"""
                <div style='display: flex; justify-content: center;'>
                    <a href="nouvelle_page?tconst={chemin_poster['tconst'][0]}" target= "_self" >
                        <img src="https://image.tmdb.org/t/p/w220_and_h330_face{chemin_poster["poster_path"][0]}" class="hover-image1">  
                    </a>
                </div>
            """

            # Afficher le poster du film 
            st.markdown(html2, unsafe_allow_html=True)
            st.write(' ')



def display_selection(result_film:pd.DataFrame)->None:
    """
    Affiche une sélection de film sous forme de poster cliquable dans l'application Streamlit.

    Args:
        result_film (pd.DataFrame): DataFrame contenant les informations sur le film sélectionné.
    """

     # Création du HTML pour afficher le poster du film avec un lien cliquable
    html = f"""
        <div style='display: flex; justify-content: center;'>
            <a href="nouvelle_page?tconst={result_film['tconst'][0]}" target= "_self" >
                <img src="https://image.tmdb.org/t/p/w220_and_h330_face{str(result_film['poster_path'][0])}" class="hover-image">  
            </a>
        </div>
    """
    
    # Affichage du poster du film en utilisant st.markdown pour interpréter le HTML
    st.markdown(html, unsafe_allow_html=True)



def aff_etoile_rate(rating:float)->str:
    """
    Convertit le rating en une représentation graphique sous forme d'étoiles.

    Args:
        rating (float): Le rating du film.

    Returns:
        str: Une représentation graphique du rating en étoiles.
    """

    # Convertir le rating en nombre d'étoiles pleines et demi-étoiles
    full_stars = int(rating/2)
    remaining_rating = rating/2 - full_stars
    
    # Générer le texte pour les étoiles
    star_text = '\u2B50' * full_stars  # Étoiles pleines
    if remaining_rating >= 0.75:
        star_text += '\u2B50'  # Demi-étoile pleine
    elif remaining_rating >= 0.5:
        star_text += '\u2B50'  # Demi-étoile avec quart
    elif remaining_rating >= 0.25:
        star_text += '\u2606'  # Demi-étoile avec quart
    remaining_stars = 5 - len(star_text)
    star_text += '\u2606' * remaining_stars  # Étoiles vides
    
    return star_text



def aff_casting(df: pd.DataFrame) -> None:
    """
    Affiche le casting d'un film à partir des données du DataFrame.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les informations du film.
    """
    
    # Liste des catégories de personnes à ajouter
    list_cat_people = ['actor', 'actress', 'directors', 'producer']
    chemins = {}
    names = {}

    col20, col21, col22, col23 = st.columns(4)
    gens0, gens1, gens2, gens3, gens4, gens5, gens6 = 0,0,0,0,0,0,0
    bbb = 0

    for id in range(len(list_cat_people)):  
        col2 = locals()['col2' + str(id)]
        
        if len(df[list_cat_people[id]]) != 0:
            with col2:
                CTN3 = st.container(border=True)
                with CTN3:
                    chemins[list_cat_people[id]] = []
                    names[list_cat_people[id]] = []

                    # Affichage du titre en fonction de la catégorie de personnes en français
                    if list_cat_people[id].capitalize() == 'Actor':
                        categ='Acteur(s)'
                    elif list_cat_people[id].capitalize() == 'Actress':
                        categ='Actrice(s)'
                    elif list_cat_people[id].capitalize() == 'Directors':
                        categ='Réalisateur(s)'
                    elif list_cat_people[id].capitalize() == 'Producer':
                        categ='Producteur(s)'

                    cat = df[list_cat_people[id]][0]

                    if len(cat) != 0:
                        
                        for person in cat:

                            imdb_id = person
                            chemin, name = display_people_image(imdb_id)

                            if chemin != 'https://image.tmdb.org/t/p/w220_and_h330_face':
                                chemins[list_cat_people[id]].append(chemin) 
                                names[list_cat_people[id]].append(name) 

                        aaa = locals()['gens' + str(id)] 

                    
                        nb_gens = len(chemins[list_cat_people[id]])

                        if nb_gens ==1:
                            slid_haut = 1
                        elif nb_gens == 0:
                            slid_haut = 1
                        elif nb_gens % 2 == 0:
                            slid_haut = nb_gens -2
                        else : 
                            slid_haut = nb_gens -2



                        if nb_gens >2:
                            aaa = st.slider(categ, 0, slid_haut, 0)
                            html = f"""
                                <div style='display: flex; justify-content: center;'>
                                    <img src="{str(chemins[list_cat_people[id]][0+aaa])}" width=50% style="margin-left: 10px;margin-bottom: 10px;">
                                    <img src="{str(chemins[list_cat_people[id]][1+aaa])}" width=50% style="margin-left: 10px;margin-right: 10px;margin-bottom:10px;">
                                </div>
                            """
                        elif nb_gens == 2:
                            aaa = st.slider(categ, 0, 1, 0)
                            aaa = 0
                            html = f"""
                                <div style='display: flex; justify-content: center;'>
                                    <img src="{str(chemins[list_cat_people[id]][0+aaa])}" width=50% style="margin-left: 10px;margin-bottom: 10px;">
                                    <img src="{str(chemins[list_cat_people[id]][1+aaa])}" width=50% style="margin-left: 10px;margin-right: 10px;margin-bottom:10px;">
                                </div>
                            """
                        elif nb_gens == 1:
                            aaa = st.slider(categ, 0, 1, 0)
                            aaa = 0
                            html = f"""
                                <div style='display: flex; justify-content: center;'>
                                    <img src="{str(chemins[list_cat_people[id]][0+aaa])}" width=50% style="margin-left: 10px;margin-bottom: 10px;">
                                </div>
                            """
                        else:
                            aaa = st.slider(categ, 0, 1, 0)
                            aaa = 0
                            html = f"""
                                <div style='display: flex; justify-content: center;'>
                                    Pas d'inforamation disponible
                                </div>
                            """

                        # Affichage du poster du film en utilisant st.markdown pour interpréter le HTML
                        st.markdown(html, unsafe_allow_html=True)


    return None
