import streamlit as st
import requests
import pandas as pd

# recuperation de la clé API tmdb
def get_api_key(
        path: str = r"data/API_tmdb.txt"
) -> tuple[str]:
    with open(path, 'r') as api_file:
        first_line = api_file.readline()

        return first_line.split(":")[1].strip()

    
@st.cache_data
def fetch_people_imagePath(tmdb_id: int = 31, api_key: str = get_api_key() )-> str:

    url = f'https://api.themoviedb.org/3/person/{tmdb_id}/images?api_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['profiles'])

        if len(df) != 0:
            path = df['file_path'][0] 
            return path
        else :
            return ""

    else:
        print("Erreur fetching data")
        return None


@st.cache_data 
def fetch_tmdbId_from_imdbId(my_imdb_id: str, api_key: str = get_api_key())->tuple[int,str]:

    url = f'https://api.themoviedb.org/3/find/{my_imdb_id}?external_source=imdb_id&api_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['person_results'])

        if len(df) != 0:
            tmdb_id = int(df['id'][0])
            tmdb_name = df['original_name'][0]
            return tmdb_id, tmdb_name
        else:
            return 0, ""

    else:
        print("Erreur fetching data")
        return None


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

    


def display_people_image(imdb_id: str)-> tuple[str, str]:

    tmdb_id, name = fetch_tmdbId_from_imdbId(imdb_id)
    image_name = fetch_people_imagePath(tmdb_id)

    chemin = f"https://image.tmdb.org/t/p/w220_and_h330_face{image_name}" 

    return chemin, name


