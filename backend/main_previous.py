# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import requests
# from datetime import datetime, timezone
# from fastapi import FastAPI
# from sqlmodel import text
# # from api.cat import router as cat_router
# # from database import engine, SessionDep, create_db_and_tables
# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select

# # Route grab the router from cat
# app = FastAPI()
# # app.include_router(cat_router, prefix="/api")

# # Set up OAuth, Spotify also uses OAuth
# scope = "user-read-private playlist-modify-private user-modify-playback-state user-read-recently-played user-read-currently-playing user-top-read"
# oauth = SpotifyOAuth(
#     client_id="2b6316217836453ab2c4b124287ee025",
#     client_secret="e4340cf6cb7e44fab462ba9c6f8e674b",
#     redirect_uri="http://127.0.0.1:8000/callback",
#     scope=scope
# )

# # Authenticate (prompts user login in browser)
# sp = spotipy.Spotify(auth_manager=oauth)

# class CurrentTrack:
#     def __init__(self, sp):
#         self.sp = sp
#         self.data = sp.current_user_playing_track()
    
#     def refresh(self):
#         self.data = self.sp.current_user_playing_track()

#     def is_active(self):
#         if self.data is None:
#             return False
#         else:
#             return True
    
#     def title(self):
#         return self.data["item"]["name"]
    
#     def artists(self):
#         artist_array = []
#         for artist in self.data["item"]["artists"]:
#             artist_array.append(artist["name"])
#         return artist_array
    
#     def image_url(self):
#         return self.data["item"]["album"]["images"][0]["url"]

#     def remaining_duration(self):
#         return (self.data["item"]["duration_ms"] - self.data["progress_ms"])//1000


# class LastPlayedTrack:
#     def __init__(self, sp):
#         self.sp = sp
#         self.data = sp.current_user_recently_played(1)
    
#     def refresh(self):
#         self.data = self.sp.current_user_recently_played(1)
    
#     def title(self):
#         return self.data["items"][0]["track"]["name"]
    
#     def artists(self):
#         artist_array = []
#         for artist in self.data["items"][0]["track"]["artists"]:
#             artist_array.append(artist["name"])
#         return artist_array
    
#     def image_url(self):
#         return self.data["items"][0]["track"]["album"]["images"][0]["url"]

#     def time_since_last_played(self):
#         played_at = datetime.fromisoformat((self.data["items"][0]["played_at"]).replace("Z", "+00:00"))
#         now = datetime.now(timezone.utc)
#         elapsed = now - played_at
#         return int(elapsed.total_seconds())
        

# def download_image_from_url(file_name: str, image_url: str):
#     img_data = requests.get(image_url).content
#     extension = file_name + '.jpg'
#     with open(extension, 'wb') as handler:
#         handler.write(img_data)


# current_track = CurrentTrack(sp)
# last_played_track = LastPlayedTrack(sp)

# # Current Track
# if current_track.is_active() is False:
#     print("No track is currently playing")
# else:
#     print(current_track.title())
#     print(current_track.artists())
#     print(current_track.remaining_duration())
#     download_image_from_url("current_album", current_track.image_url())


# # Previous Track
# print(last_played_track.title())
# print(last_played_track.artists())
# print(last_played_track.time_since_last_played())
# print(last_played_track.image_url())
# download_image_from_url("previous_album", last_played_track.image_url())

# # Maybe the top 20 tracks short term and get the artist and the genre from that?

# # def get_tags(artist_name):
# #     artist = network.get_artist(artist_name)
# #     top_tags = artist.get_top_tags()
# #     tag_100 = []

# #     for tag in top_tags:
# #         if int(tag.weight) > 50:
# #             tag_100.append(tag)
# #     return tag_100

# from test_stuff import get_similar_artists, get_tag_names_and_weights, get_tags, get_artist_score, get_scores

# N = 10
# rank_weights = 1/(N*2)

# top_artists = sp.current_user_top_artists(N, 0, "short_term") # do long_term vs short_term

# # for artist in top_artists["items"]:
# #     name = artist["name"]
# #     tags = get_tag_names_and_weights(get_tags(name, 5))
# #     similar_artists = get_similar_artists(name)

# #     print(f"Artist: {name}")
# #     print(f"Tags: {tags}")
    
# #     print("Similar Artists:")
# #     for similar in similar_artists:
# #         similar_name = similar.item.get_name()
# #         similarity_percentage = similar.match  # similarity
# #         similar_tags = get_tag_names_and_weights(get_tags(similar_name, 5))
# #         print(f"  - {similar_name} ({similarity_percentage:.2f})")
# #         print(f"    Tags: {similar_tags}")
    
# #     print("\n" + "-"*50 + "\n")
    
# for artist in top_artists["items"]:
#     name = artist["name"]
#     print(f"Artist: {name}")
#     artist_scores = get_artist_score(name)
#     for key, value in sorted(artist_scores.items(), key=lambda item: item[1], reverse=True):
#         print(key, value)
    
#     print("\n" + "-"*50 + "\n")


# score_dict = dict()
# count = 0
# for artist in top_artists["items"]:
#     current_weight = 1 - (rank_weights * count)
#     name = artist["name"]
#     get_scores(name, score_dict, current_weight)
#     count += 1

# return_arr = []
# for key, value in sorted(score_dict.items(), key=lambda item: item[1], reverse=True):
#     arr = [key, value]
#     return_arr.append(arr)

# max_val = return_arr[0][1]
# for val in return_arr:
#     replacement_val = val[1]/max_val
#     val[1] = replacement_val

# for i in range(5):
#     print(return_arr[i])





# # top_songs = sp.current_user_top_tracks(50, 0, "short_term")
# # for song in top_songs["items"]:
# #     for artist in song["artists"]:
# #         artist_id = artist["id"]
# #         name = artist["name"]
# #         print(artist["name"] , " : ",  sp.artist(artist_id)["genres"])
# #         get_tags(name)
        


# # @app.get("/")
# # async def root():
# #     return {"message": "Hello World"}

# # Refresh after waiting remaining_ms

# # If not currently playing, poll every 30 seconds to see 

# # To reduce the number of requests sent to the server, this application grabs how many seconds are left in a track and then waits until that amount of time + 3 seconds to poll the server again

# # Implement a surprise me feature that plays a random song from a predefined list

# # Play current track on partner's Spotify account

# # Add current track to shared playlist

# # create_db_and_tables()

# # @app.get("/db-test")
# # def test_db():
# #     with engine.connect() as connection:
# #         result = connection.execute(text("SELECT 1"))
# #         return {"db_connection": "successful", "result": result.scalar()}
    
# # class Hero(SQLModel, table=True):
# #     id: int | None = Field(default=None, primary_key=True)
# #     name: str = Field(index=True)
# #     age: int | None = Field(default=None, index=True)
# #     secret_name: str

# # @app.post("/heroes/")
# # def create_hero(hero: Hero, session: SessionDep) -> Hero:
# #     session.add(hero)
# #     session.commit()
# #     session.refresh(hero)
# #     return hero


