import random
import bot
import json
import requests
from requests import get
import discord
import time
import asyncio
import re

#################### SEARCH ####################

def search_spotify(token, search_type, search_query):
    """
    Search Spotify for a specific type (artist, album, playlist, track) with a query.
    :params token: Spotify API token
    :params search_type: Type of search (artist, album, playlist, track)
    :params search_query: Query to search for
    :return: JSON result of the search
    """
    url = f"https://api.spotify.com/v1/search?q={search_query}&type={search_type}"
    headers = bot.get_auth_header(token)
    try:
        response = get(url, headers=headers)
        response.raise_for_status() 
        json_result = response.json()[f"{search_type}s"]["items"]
        for item in json_result:
            if item["name"].lower() == search_query.lower():
                return item
        return json_result[0] if json_result else None
    except requests.RequestException as e:
        print(f"Error during Spotify search: {e}")
        return None

#################### ARTIST ####################

async def get_artist_info(ctx, token, artist_name, is_private):
    """ 
    Get information about an artist.
    :params ctx: Discord context
    :params token: Spotify API token
    :params artist_name: Name of the artist
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        artist_info = search_spotify(token, "artist", artist_name)
        if artist_info == 0:
            await send(ctx, "Error", "Artist not found or invalid artist name.", "", "", is_private)
            return
        
        genres = ""
        for genre in artist_info["genres"]:
            genres += genre + ", "

        response = "`Name: " + artist_info["name"] + "\n" \
            "Genres: " + genres[:len(genres)-2] + "\n" \
            "Popularity: " + str(artist_info["popularity"]) + "\n" \
            "Followers: " + str(artist_info["followers"]["total"]) + "`"
        
        artist_name = artist_info['name']
        await send(ctx, f"{artist_name} Info", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_artist_info: {e}")
        await send(ctx, "Error", "An error occurred while fetching artist information.", "", "", is_private)
    
async def get_albums_by_artist(ctx, token, artist_name, is_private):
    """
    Get all albums by an artist.
    :params ctx: Discord context
    :params token: Spotify API token
    :params artist_name: Name of the artist
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        artist_info = search_spotify(token, "artist", artist_name)
        if artist_info == 0:
            await send(ctx, "Error", "Artist not found or invalid artist name.", "", "", is_private)
            return
        
        artist_name = artist_info['name']
        artist_id = artist_info['id']
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        querry_url =  url + "?include_groups=album"
        headers = bot.get_auth_header(token)
        api_response = get(querry_url, headers=headers)
        artist_albums = json.loads(api_response.content)['items']

        i = 0
        response = ""
        response += f"`Albums by {artist_name}:\n"
        for album in artist_albums:
            if i == len(artist_albums)-1:
                response += "\t" + album['name'] + "`"
            else:
                response += "\t" + album['name'] + "\n"
            i += 1

        await send(ctx, f"Albums By {artist_name}", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_albums_by_artist: {e}")
        await send(ctx, "Error", "An error occurred while fetching artist albums.", "", "", is_private)
        
async def get_top_tracks_by_artist(ctx, token, artist_name, is_private):
    """
    Get top trending tracks by an artist.
    :params ctx: Discord context
    :params token: Spotify API token
    :params artist_name: Name of the artist
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        artist_info = search_spotify(token, "artist", artist_name)
        if artist_info == 0:
            await send(ctx, "Error", "Artist not found or invalid artist name.", "", "", is_private)
            return   

        artist_name = artist_info['name']
        artist_id = artist_info['id']
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=PT"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        top_tracks = json.loads(api_response.content)["tracks"]

        i = 0
        response = ""
        response += f"`Top trending tracks by {artist_name}:\n"
        for idx,track in enumerate(top_tracks):
            if i == len(top_tracks)-1:
                response += f"{idx+1}. {track['name']}`"
            else:
                response += f"{idx+1}. {track['name']}\n"
            
            i += 1

        await send(ctx, f"Top Tracks By {artist_name}", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_top_tracks_by_artist: {e}")
        await send(ctx, "Error", "An error occurred while fetching artist top tracks.", "", "", is_private)

async def get_artist_related_artists(ctx, token, artist_name, is_private):
    """
    Get related artists to an artist.
    :params ctx: Discord context
    :params token: Spotify API token
    :params artist_name: Name of the artist
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        artist_info = search_spotify(token, "artist", artist_name)
        if artist_info == 0:
            await send(ctx, "Error", "Artist not found or invalid artist name.", "", "", is_private)
            return

        artist_id = artist_info['id']
        artist_name = artist_info['name']
        url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        related_artists = json.loads(api_response.content)["artists"]

        i = 0
        response = ""
        response += f"`Related artists to {artist_name}:\n"
        for idx,artist in enumerate(related_artists):
            if i == len(related_artists)-1:
                response += f"{idx+1}. {artist['name']}`"
            else:
                response += f"{idx+1}. {artist['name']}\n"
            
            i += 1

        await send(ctx, f"Related Artists To {artist_name}", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_artist_related_artists: {e}")
        await send(ctx, "Error", "An error occurred while fetching artist related artists.", "", "", is_private)

#################### ALBUM #################### 

async def get_album_info(ctx, token, album_name, is_private):
    """
    Get information about an album.
    :params ctx: Discord context
    :params token: Spotify API token
    :params album_name: Name of the album
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        album_info = search_spotify(token, "album", album_name)
        if album_info == 0:
            await send(ctx, "Error", "Album not found or invalid album name.", "", "", is_private)
            return
        
        url = f"https://api.spotify.com/v1/albums/{album_info['id']}"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        album_info= json.loads(api_response.content)

        artists = ""
        for artist in album_info["artists"]:
            artists += artist["name"] + ", "
        tracks = ""
        for track in album_info["tracks"]["items"]:
            tracks += "\t" + str(track["track_number"]) + ": " + track["name"] + "\n"

        response = "`Name: " + album_info["name"] + "\n" \
            "Artists: " + artists[:len(artists)-2] + "\n" \
            "Release Date: " + album_info["release_date"] + "\n" \
            "Tracks:\n" + tracks[:len(tracks)-1] + "\n" \
            "Popularity: " + str(album_info["popularity"]) + "\n" \
            "Label: " + album_info["label"] + "`"
        
        await send(ctx, album_info["name"]+" Info", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_album_info: {e}")
        await send(ctx, "Error", "An error occurred while fetching album information.", "", "", is_private)

async def get_new_album_releases(ctx, token, country, is_private): ### A BIT BROKEN WORKS BEST FOR country=US
    """
    Get new album releases.
    :params ctx: Discord context
    :params token: Spotify API token
    :params country: Country code
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        url = "https://api.spotify.com/v1/browse/new-releases"
        if country != "":
            url += f"?country={country}"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)

        if api_response.status_code != 200:
            return "Please provide a valide country. For more informations type '!help'."
        
        new_album_releases = json.loads(api_response.content)

        limit = 0
        for item in new_album_releases["albums"]["items"]:
            if item["album_type"] == "album":
                limit += 1

        i = 0
        response = ""
        for name in new_album_releases["albums"]["items"]:
            if name["album_type"] == "album":
                if i == 0:
                    response += "`New Albums:\n"
                elif i == limit-1:
                    response += "\t" + name["name"] + " - " + name["artists"][0]["name"] + " - " + name["release_date"] + "`"
                else:
                    response += "\t" + name["name"] + " - " + name["artists"][0]["name"] + " - " + name["release_date"] + "\n"
            
                i += 1

        await send(ctx, "New Album Releases "+country, response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_new_album_releases: {e}")
        await send(ctx, "Error", "An error occurred while fetching new album releases.", "", "", is_private)

#################### CATEGORIES ####################   

def get_categories(token):
    """
    Get all categories.
    :params token: Spotify API token
    :return: List of categories
    """
    try: 
        url = "https://api.spotify.com/v1/browse/categories"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)

        category_data = json.loads(api_response.content)

        categories_names = []
        for category in category_data["categories"]["items"]:
            categories_names.append([category["id"], category["name"]])

        return categories_names
    except Exception as e:
        print(f"Error in get_categories: {e}")
        return None

async def show_categories(ctx, token, is_private):
    """
    Show all categories.
    :params ctx: Discord context
    :params token: Spotify API token
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try: 
        categories_list = get_categories(token)

        i = 0
        response = ""
        for category in categories_list:
            if i == 0:
                response += "`Categories:\n"
            elif i == len(categories_list)-1:
                response += "\t" + category[1] + "`"
            else:
                response += "\t" + category[1] + "\n"

            i += 1
        
        await send(ctx, "Spotify Categories", response, "", "", is_private)
    except Exception as e:
        print(f"Error in show_categories: {e}")
        await send(ctx, "Error", "An error occurred while fetching spotify categories.", "", "", is_private)

#################### GENRES ####################

async def get_genres(ctx, token, is_private):
    """
    Get all genres.
    :params ctx: Discord context
    :params token: Spotify API token
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        genre_data = json.loads(api_response.content)

        i = 0
        response = ""
        for genre in genre_data["genres"]:
            if i == 0:
                response += "`Genres:\n"
            elif i == len(genre_data["genres"])-1:
                response += "\t" + genre + "`"
            else:
                response += "\t" + genre + "\n"
            
            i += 1

        await send(ctx, "Spotify Genres", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_genres: {e}")
        await send(ctx, "Error", "An error occurred while fetching spotify genres.", "", "", is_private)

#################### PLAYLIST ####################

async def get_playlist_info(ctx, token, playlist_name, is_private):
    """
    Get information about a playlist.
    :params ctx: Discord context
    :params token: Spotify API token
    :params playlist_name: Name of the playlist
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        playlist_info = search_spotify(token, "playlist", playlist_name)
        if playlist_info == 0:
            await send(ctx, "Error", "Playlist not found or invalid playlist name.", "", "", is_private)
            return

        url = f"https://api.spotify.com/v1/playlists/{playlist_info['id']}"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        playlist_info = json.loads(api_response.content)

        response = "`Name: " + playlist_info["name"] + "\n" \
            "Owner: " + playlist_info["owner"]["display_name"] + "\n" \
            "Description: " + playlist_info["description"] + "\n" \
            "Followers: " + str(playlist_info["followers"]["total"]) + "\n" \
            "Tracks: " + str(playlist_info["tracks"]["total"]) + "\n" \
            "Link: `" + playlist_info["external_urls"]["spotify"] 
        
        await send(ctx, playlist_info["name"]+" Info", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_playlist_info: {e}")
        await send(ctx, "Error", "An error occurred while fetching playlist information.", "", "", is_private)

async def get_spotify_featured_playlists(ctx, token, is_private):
    """
    Get all featured playlists.
    :params ctx: Discord context
    :params token: Spotify API token
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        url = "https://api.spotify.com/v1/browse/featured-playlists"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        featuredPlaylists = json.loads(api_response.content)

        i = 0
        response = "`Playlists: " + "\n"
        for playlist in featuredPlaylists["playlists"]["items"]:
            if i == len(featuredPlaylists["playlists"]["items"]) - 1:
                response += "\t" + playlist["name"] + " - " + playlist["owner"]["display_name"] + "`"
            else:
                response += "\t" + playlist["name"] + " - " + playlist["owner"]["display_name"] + "\n"

            i += 1

        await send(ctx, "Spotify Featured Playlists", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_spotify_featured_playlists: {e}")
        await send(ctx, "Error", "An error occurred while fetching spotify featured playlists.", "", "", is_private)


async def get_spotify_categories_playlists(ctx, token, category_id, is_private):
    """
    Get all playlists from a specific category. If the category is not given, a random category will be selected.
    :params ctx: Discord context
    :params token: Spotify API token
    :params category_id: Category ID
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        categories_list = get_categories(token)
        if category_id == "":
            random_number = random.randint(0, len(categories_list)-1)
            category_id = categories_list[random_number][0]
        else:
            for categories in categories_list:
                if categories[1].lower() == category_id:
                    category_id = categories[0]
        url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit=50"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        if api_response.status_code != 200:
            return "Please provide a valid category name."
        
        playlists = json.loads(api_response.content)

        random_number = random.randint(0, len(playlists["playlists"]["items"])-1)

        await get_playlist_info(ctx, token, playlists["playlists"]["items"][random_number]["name"], is_private)
    except Exception as e:
        print(f"Error in get_spotify_categories_playlists: {e}")
        await send(ctx, "Error", "An error occurred while fetching spotify categories playlists.", "", "", is_private)

#################### TRACKS ####################

async def get_track_info(ctx, token, track_name, is_private):
    """
    Get information about a track.
    :params ctx: Discord context
    :params token: Spotify API token
    :params track_name: Name of the track
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try: 
        track_info = search_spotify(token, "track", track_name)
        if track_info == 0:
            await send(ctx, "Error", "Track not found or invalid track name.", "", "", is_private)
            return

        url = f"https://api.spotify.com/v1/tracks/{track_info['id']}"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        track_info = json.loads(api_response.content)

        artists = ""
        for artist in track_info["artists"]:
            artists += artist["name"] + ", "

        response = "`Name: " + track_info["name"] + "\n" \
            "Artists: " + artists[:len(artists)-2] + "\n" \
            "Album: " + track_info["album"]["name"] + "\n" \
            "Release Date: " + track_info["album"]["release_date"] + "\n" \
            "Popularity: " + str(track_info["popularity"]) + "\n" \
            "Link: `" + track_info["external_urls"]["spotify"]
        
        await send(ctx, track_info["name"]+" Info", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_track_info: {e}")
        await send(ctx, "Error", "An error occurred while fetching track information.", "", "", is_private)

async def get_track_features(ctx, token, track_name, is_private):
    """ 
    Get features about a track.
    :params ctx: Discord context
    :params token: Spotify API token
    :params track_name: Name of the track
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        track_info = search_spotify(token, "track", track_name)
        if track_info == 0:
            await send(ctx, "Error", "Track not found or invalid track name.", "", "", is_private)
            return
        
        track_name = track_info['name']
        url = f"https://api.spotify.com/v1/audio-features?ids={track_info['id']}"
        headers = bot.get_auth_header(token)
        api_response = get(url, headers=headers)
        track_info = json.loads(api_response.content)

        keysList = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb","G", "G#/Ab", "A", "A#/Bb", "B"]

        response = "`Key: " + keysList[track_info["audio_features"][0]["key"]] + "\n" 
        if (track_info["audio_features"][0]["mode"] == 0):
            response += "Mode: Minor\n"
        else:
            response += "Mode: Major\n"
        response += "Time Signature: " + str(track_info["audio_features"][0]["time_signature"]) + "/4\n" \
            "Tempo (BPM): " + str(track_info["audio_features"][0]["tempo"]) + "\n" \
            "Danceability (Range: 0-1): " + str(track_info["audio_features"][0]["danceability"]) + "\n" \
            "Instrumentalness (Range: 0-1): " + str(track_info["audio_features"][0]["instrumentalness"]) + "\n" \
            "Acousticness (Range: 0-1): " + str(track_info["audio_features"][0]["acousticness"]) + "\n" \
            "Energy (Range: 0-1): " + str(track_info["audio_features"][0]["energy"]) + "\n" \
            "Loudness (Range: -60-0 db): " + str(track_info["audio_features"][0]["loudness"]) + "\n" \
            "Speechiness (Range: 0-1): " + str(track_info["audio_features"][0]["speechiness"]) + "\n" \
            "Valence (Range: 0-1): " + str(track_info["audio_features"][0]["valence"]) + "`" 
        
        await send(ctx, track_name+" Features", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_track_features: {e}")
        await send(ctx, "Error", "An error occurred while fetching track features.", "", "", is_private)
        
async def get_track_features_help(ctx, features_list, is_private):
    """
    Get help about track features.
    :params ctx: Discord context
    :params features_list: List of features
    :params is_private: Boolean to check if the message should be sent via DM
    """
    response = ""
    if ("acousticness" in features_list or features_list == ""):
        response += "⇨ Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.\n"
    if ("danceability" in features_list or features_list == ""):
        response += "⇨ Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm" \
        "stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.\n"
    if ("energy" in features_list or features_list == ""):
        response += "⇨ Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel" \
        "fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing" \
        "to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.\n"
    if ("instrumentalness" in features_list or features_list == ""):
        response += "⇨ Instrumentalness: Predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are treated as instrumental in this context. Rap or" \
        "spoken word tracks are clearly 'vocal'. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal" \
        "content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.\n"
    if ("liveness" in features_list or features_list == ""):
        response += "⇨ Liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track\n"
        "was performed live. A value above 0.8 provides strong likelihood that the track is live.\n"
    if ("loudness" in features_list or features_list == ""):    
        response += "⇨ Loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing" \
        "relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude)." \
        "Values typically range between -60 and 0 db.\n"
    if ("speechiness" in features_list or features_list == ""):
        response += "⇨ Speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show," \
        "audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words." \
        "Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as" \
        "rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.\n"
    if ("tempo" in features_list or features_list == ""):
        response += "⇨ Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece" \
        "and derives directly from the average beat duration.\n"
    if ("valence" in features_list or features_list == ""):
        response += "⇨ Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive" \
        "(e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."

    if response == "":
        response = "Please provide a valid feature name. For more informations type '!help'."

    await send(ctx, "Track Features Help", response, "", "", is_private)

async def get_recomendations(ctx, token, message, is_private):
    """
    Get tracks recommendations based on artists, genres, and tracks.
    :params ctx: Discord context
    :params token: Spotify API token
    :params message: Message with the command
    :params is_private: Boolean to check if the message should be sent via DM
    """
    try:
        parts = [part.strip() for part in message.split('|')]

        number_of_results = int(parts[0]) if parts[0].isdigit() else 0
        if number_of_results <= 0 or number_of_results > 100:
            await send(ctx, "Error", "The number of results must be greater than 0 and less than 100", "", "", is_private)
            return
        
        artists_names = [name.strip() for name in parts[1].split(',')] if len(parts) > 1 else []
        genres_names = [name.strip() for name in parts[2].split(',')] if len(parts) > 2 else []
        tracks_names = [name.strip() for name in parts[3].split(',')] if len(parts) > 3 else []

        if len(artists_names) + len(genres_names) + len(tracks_names) > 5:
            await send(ctx, "Error", "The sum of artists, genres, and tracks must not be greater than 5", "", "", is_private)
            return 

        artistsID = ','.join([search_spotify(token, "artist", artist)['id'] for artist in artists_names if artist])
        genresID = ','.join(genres_names)
        tracksID = ','.join([search_spotify(token, "track", track)['id'] for track in tracks_names if track])

        url = f"https://api.spotify.com/v1/recommendations?limit={number_of_results}&seed_artists={artistsID}&seed_genres={genresID}&seed_tracks={tracksID}"
        headers = bot.get_auth_header(token)
        api_response = requests.get(url, headers=headers)
        api_response.raise_for_status()
        song_recommendations = api_response.json()

        response = "`Song recommendations:\n"
        for idx, recommendation in enumerate(song_recommendations["tracks"]):
            response += f"{idx + 1}. {recommendation['name']} - {recommendation['artists'][0]['name']}\n"
        response += "`"

        await send(ctx, "Recommended Tracks", response, "", "", is_private)
    except Exception as e:
        print(f"Error in get_recomendations: {e}")
        await send(ctx, "Error", "An error occurred while fetching recommendations.", "", "", is_private)

#################### OTHER ####################

async def help(ctx, is_private):
    """
    Show all commands.
    :params ctx: Discord context
    :params is_private: Boolean to check if the message should be sent via DM
    """
    response = "`"
    response += "# Commands Help:\n"
    response += "\t" + "#artist " + "artist_name" + "\n"
    response += "\t" + "#albums " + "artist_name" + "\n"
    response += "\t" + "#toptracks " + "artist_name" + "\n"
    response += "\t" + "#relatedartists " + "artist_name" + "\n"
    response += "\t" + "#album " + "album_name" + "\n"
    response += "\t" + "#newreleases " + "country (e.g. PT, US - works best for US)" + "\n"
    response += "\t" + "#categories" + "\n"
    response += "\t" + "#genres" + "\n"
    response += "\t" + "#playlist " + "playlist_name" + "\n"
    response += "\t" + "#featuredplaylists" + "\n"
    response += "\t" + "#categoryplaylist " + "[category_name] (optional - if not given will be randomly selected)" + "\n"
    response += "\t" + "#track " + "track_name" + "\n"
    response += "\t" + "#featurestrack " + "track_name" + "\n"
    response += "\t" + "#infotrackfeatures " + "[feature_name] (optional)" + "\n"
    response += "\t- #recommendations number_of_results | artists | genres | tracks\n"
    response += "\t\tExample: #recommendations 10 | Taylor Sift | pop, rock | Bad Blood, Shape of You\n"
    response += "\t\tNote: At least one of 'artists', 'genres', or 'tracks' is required. The sum of them can't be more than 5.\n"
    response += "\t" + "#game " + "playlist_name/playlis_url " + "mode=songs/artists" + "\n"
    response += "\t" + "#usertop " + "mode=songs/artists " + "limit=(1-50) " + "time=short/medium/long" + "\n"
    response += "\t" + "Note: If before every command you insert '?' the information will be sent to you via DM" + "`"
    
    await send(ctx, "Help:", response, "", "", is_private)

async def send(ctx, title, description, field, value, is_private):
    """
    Create the message embed and send it.
    :params ctx: Discord context
    :params title: Title of the embed
    :params description: Description of the embed
    :params field: Field of the embed
    :params value: Value of the embed
    :params is_private: Boolean to check if the message should be sent via DM
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.green()  
    )
    
    if field != "" or value != "":
        field = "⇨ " +field
        embed.add_field(name=field, value=value, inline=True)

    if is_private:
        message = await ctx.author.send(embed=embed)
    else:
        message = await ctx.send(embed=embed)

    return message

#################### GAME ####################

async def get_artist_info_for_game(token, artist_name):
    """
    Get artist info.
    :params token: Spotify API token
    :params artist_name: Name of the artist
    """
    info = search_spotify(token, "artist", artist_name)
    if info == 0:
      return "Please provide a valid artist name."
    
    return info

async def get_playlist_info_for_game(ctx, token, playlist_name, url, mode):
    """
    Get playlist info.
    :params ctx: Discord context
    :params token: Spotify API token
    :params playlist_name: Name of the playlist
    :params url: Boolean to check if the playlist name is a url
    :params mode: Mode of the game. Can be "songs" or "artists"    
    """
    if not url:
        info = search_spotify(token, "playlist", playlist_name)
        if info == None:
            await send(ctx, "Something went wrong", "Check the playlist url or the name you have provided.", "", "", False)
            return
        url = f"https://api.spotify.com/v1/playlists/{info['id']}"
    else: 
        playlist_id = playlist_name.split('/')[-1]
        playlist_id = playlist_id.split('?')[0]
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    headers = bot.get_auth_header(token)
    api_response = get(url, headers=headers)
    if api_response == None:
        await send(ctx, "Something went wrong", "Check the playlist url or the name you have provided.", "", "", False)
        return
    playlistInfo = json.loads(api_response.content)

    if mode == "songs":
        track_names_and_popularity = []

        for track_item in playlistInfo.get("tracks", {}).get("items", []):
            track = track_item.get("track")
            if track:
                track_name = track.get("name")
                track_popularity = track.get("popularity")
                if track_name is not None and track_popularity is not None:
                    track_names_and_popularity.append({"name": track_name, "popularity": track_popularity})

        return track_names_and_popularity, playlistInfo["name"]
    elif mode == "artists":
        await send(ctx, "Please standby.", "The game will start in a few seconds.", "", "", False)
        artist_names = set()
        for track_item in playlistInfo.get("tracks", {}).get("items", []):
            track = track_item.get("track")
            if track:
                track_artist = track.get("artists")
                if track_artist is not None:
                    artist_name = track_artist[0].get("name")
                    artist_names.add(artist_name)
        
        artist_info_list = []
        for artist_name in artist_names:
            artist_info = await get_artist_info_for_game(token, artist_name)
            if artist_info:
                if artist_info.get("name") is not None and artist_info.get("popularity") is not None:
                    artist_info_list.append({"name": artist_name, "popularity": artist_info["popularity"]})

        return artist_info_list, playlistInfo["name"]
    else:
        return None, playlistInfo["name"]

def load_high_scores():
    """
    Load high scores from a text file
    :return: List of high scores
    """
    high_scores = []
    try:
        with open("high_scores.txt", "r") as file:
            for line in file:
                player, score, playlist, mode = line.strip().split(":")
                high_scores.append({"player": player, "score": int(score), "playlist": playlist, "mode": mode})
    except FileNotFoundError:
        pass
    return high_scores

def save_high_scores(high_scores):
    """
    Save high scores to a text file
    """
    with open("high_scores.txt", "w") as file:
        for score_data in high_scores:
            file.write(f"{score_data['player']}:{score_data['score']}:{score_data['playlist']}:{score_data['mode']}\n")

def print_highest_scores(highest_scores):
    """
    Print highest scores.
    :params highest_scores: List of highest scores
    :return: String with the highest scores
    """
    highest_scores_message = "Top 10 High Scores:\n"
    for idx, score_data in enumerate(sorted(highest_scores, key=lambda x: x["score"], reverse=True)[:10]):
        highest_scores_message += f"{idx + 1}. {score_data['player']}: {score_data['score']} (Playlist: {score_data['playlist']}) (Mode: {score_data['mode']})\n"
    return highest_scores_message

def print_player_lost(players_to_remove):
    """
    Print players who have lost.    
    :params players_to_remove: List of players to remove
    :return: String with the players who have lost
    """
    message = ""
    for player in players_to_remove:
        message += f"{player} has been eliminated!\n"
    return message

def print_all_points(players_scores):
    """
    Print all points.
    :params players_scores: Dictionary of players and their scores
    :return: String with all points
    """
    players_scores = dict(sorted(players_scores.items(), key=lambda item: item[1], reverse=True))
    points_msg = ""
    for idx, player in enumerate(players_scores):
        points_msg += f"{idx}. {player}: {players_scores[player]}\n"
    return points_msg

async def game(ctx, tokenSpotify, playlist_name):
    """
    Represents a higher or lower game.
    :params ctx: Discord context
    :params tokenSpotify: Spotify API token
    :params playlist_name: Name of the playlist
    """
    pattern = r"(.*?)(?: mode=(\w+))?$"
    match = re.search(pattern, playlist_name)
    if match:
        playlist_name = match.group(1).strip()
        mode = match.group(2) if match.group(2) else None
    else:
        await send(ctx, "Something went wrong", "Check the playlist url or the name you have provided. Make sure you also specify a mode.", "", "", False)
        return    

    if mode == None:
        await send(ctx, "Something went wrong", "Check the playlist url or the name you have provided. Make sure you also specify a mode.", "", "", False)
        return

    url_mode = False
    if playlist_name.startswith("https://"):
        url_mode = True

    if url_mode:
        info, actual_playlist_name = await get_playlist_info_for_game(ctx, tokenSpotify, playlist_name, True, mode)
    else:
        playlist_name = playlist_name.lower()
        info, actual_playlist_name = await get_playlist_info_for_game(ctx, tokenSpotify, playlist_name, False, mode)

    if info == [] or info == None:
        await send(ctx, "Something went wrong", "Check the playlist url or the name you have provided.", "", "", False)
        return

    highest_scores = load_high_scores()
    players_scores = {}
    num_rounds = len(info)
    songs_chosen = []
    current_index = random.randint(0, len(info) - 1)
    songs_chosen.append(current_index)
    next_index = 0
    participants = []
    first_round = True

    while (num_rounds > 0):
        players_to_remove = []

        if len(info) < 2:
            await send(ctx, "Invalid playlist size.", "Please make sure your playlist has more tan 1 song.", "", "", False)
            break

        current_item = info[current_index]
        next_index = random.randint(0, len(info) - 1)
        while next_index in songs_chosen:
            next_index = random.randint(0, len(info) - 1)
        songs_chosen.append(next_index)

        next_item = info[next_index]
        current_index = next_index

        game_message = f"Is the popularity of '{current_item['name']}' higher or lower than '{next_item['name']}'?"
        message = await send(ctx, game_message, "", "", "", False)

        await message.add_reaction('⬆️')
        await message.add_reaction('⬇️')

        is_higher = current_item['popularity'] > next_item['popularity']

        round_participants_reactions = {}

        while True:
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=5.0)
                if user.name not in participants and first_round:
                    participants.append(user.name)
                    players_scores[user.name] = 0
                if user.name not in round_participants_reactions and reaction.emoji in ['⬆️', '⬇️']:
                    round_participants_reactions[user.name] = reaction.emoji
            except asyncio.TimeoutError:
                break
            
        for participant in participants:
            if (participant not in round_participants_reactions):
                players_to_remove.append(participant)
            elif (is_higher and '⬆️' == round_participants_reactions[participant]) or \
               (not is_higher and '⬇️' == round_participants_reactions[participant]):
                players_scores[participant] += 1
            else:
                players_to_remove.append(participant)

        for player in players_to_remove:
            participants.remove(player)        

        await send(ctx, "Round Over!", print_player_lost(players_to_remove), "Points table", print_all_points(players_scores), False)

        if participants == []:
            break

        first_round = False
        num_rounds -= 1

        time.sleep(1)
    
    for participant, score in players_scores.items():
        if len(highest_scores) < 10 or score > min(highest_scores, key=lambda x: x["score"])["score"]:
            new_high_score = {"player": participant, "score": score, "playlist": actual_playlist_name, "mode": mode}
            highest_scores.append(new_high_score)
            if len(highest_scores) > 10:
                highest_scores.remove(min(highest_scores, key=lambda x: x["score"]))

    save_high_scores(highest_scores)

    await send(ctx, "Game over! Thanks for playing.", "", "Highest Scores", print_highest_scores(highest_scores), False)


#################### HANDLE RESPONSES ####################

async def handle_responses(ctx, tokenSpotify, message, sp, is_private):
    """
    Handle all responses.
    :params ctx: Discord context
    :params tokenSpotify: Spotify API token
    :params message: Message with the command
    :params sp: Spotify API object
    :params is_private: Boolean to check if the message should be sent via DM
    """
    p_message = message.lower()

    if p_message.startswith('#artist'):
        await get_artist_info(ctx, tokenSpotify, p_message[8:], is_private)
    
    elif p_message.startswith('#albums'):
        await get_albums_by_artist(ctx, tokenSpotify, p_message[8:], is_private)
    
    elif p_message.startswith('#toptracks'):
        await get_top_tracks_by_artist(ctx, tokenSpotify, p_message[11:], is_private)
    
    elif p_message.startswith('#relatedartists'):
        await get_artist_related_artists(ctx, tokenSpotify, p_message[15:], is_private)

    elif p_message.startswith('#album'):
        await get_album_info(ctx, tokenSpotify, p_message[7:], is_private)
    
    elif p_message.startswith('#newreleases'):
        await get_new_album_releases(ctx, tokenSpotify, p_message[13:].upper(), is_private)
    
    elif p_message.startswith('#categories'):
        await show_categories(ctx, tokenSpotify, is_private)
    
    elif p_message.startswith('#genres'):
        await get_genres(ctx, tokenSpotify, is_private)
    
    elif p_message.startswith('#playlist'):
        await get_playlist_info(ctx, tokenSpotify, p_message[10:], is_private)
    
    elif p_message.startswith('#featuredplaylists'):
        await get_spotify_featured_playlists(ctx, tokenSpotify, is_private)
    
    elif p_message.startswith('#categoryplaylist'):  
        await get_spotify_categories_playlists(ctx, tokenSpotify, p_message[18:], is_private)
    
    elif p_message.startswith('#track'):
        await get_track_info(ctx, tokenSpotify, p_message[7:], is_private)
    
    elif p_message.startswith('#featurestrack'):
        await get_track_features(ctx, tokenSpotify, p_message[15:], is_private)
    
    elif p_message.startswith('#infotrackfeatures'):
        await get_track_features_help(ctx, p_message[18:], is_private)

    elif p_message.startswith('#recomendations'):  
        await get_recomendations(ctx, tokenSpotify, p_message[15:], is_private)

    elif p_message == '#help':
        await help(ctx, is_private)

    elif p_message.startswith('#game'):
        await game(ctx, tokenSpotify, p_message[6:])
    

