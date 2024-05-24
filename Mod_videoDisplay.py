import streamlit as st
import requests
import pandas as pd
from tmdb_API import *



def aff_video(df: pd.DataFrame)->None:
    """
    Affiche la vidéo du trailer d'un film à partir du DataFrame contenant les données du film.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données du film.
                       Doit inclure la colonne 'tconst'.

    Returns:
    None
    """

    url = fetch_video_link(fetch_idMovie_fromImdbtconst(df['tconst'][0]))

    if url != '':
        st.video(url)
