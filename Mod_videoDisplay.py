import streamlit as st
import requests
import pandas as pd
from tmdb_API import *


def aff_video(df: pd.DataFrame)->None:
    url = fetch_video_link(fetch_idMovie_fromImdbtconst(df['tconst'][0]))

    if url != '':
        st.video(url)


def fetch_video_link(movie_id: int, api_key: str = get_api_key())->str:

    url = f"https://api.themoviedb.org/3/movie/{str(movie_id)}/videos?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        df = pd.DataFrame(data['results'])
        if len(df) != 0:
            df = df[df['type'] == 'Trailer'].reset_index()
            
            if len(df) != 0:
                youtube_key = df['key'][0]
                
                return f'https://www.youtube.com/watch?v={youtube_key}'
            else:
                return f''

    else:
        st.write("Erreur fetching data", response.status_code)
        return ''
    

def fetch_idMovie_fromImdbtconst(my_imdb_id: str, api_key: str = get_api_key())->tuple[int,str]:
        # les trois freres: tt0114732 - 37653

    url = f'https://api.themoviedb.org/3/find/{my_imdb_id}?external_source=imdb_id&api_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['movie_results'])

        if len(df) != 0:
            tmdb_id = int(df['id'][0])
            return tmdb_id
        
        else:
            return 0

    else:
        print("Erreur fetching data")
        return None