# import firebase_admin
# from firebase_admin import credentials, firestore, firestore_async
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate('./config/esp32-docking-system-firebase-adminsdk-fbsvc-77256d16e6.json')
# firebase_admin.initialize_app(cred)

# # Initialize Firestore Async Client
# db = firestore_async.client()

# # FastAPI instance
# app = FastAPI()

# # Pydantic model for request validation
# class User(BaseModel):
#     first: str
#     last: str
#     born: int

# # Endpoint to add a user to Firestore
# @app.post("/users/{user_id}")
# async def add_user(user_id: str, user: User):
#     try:
#         # Reference to the Firestore document
#         doc_ref = db.collection("users").document(user_id)
#         # Set the document data (asynchronously)
#         await doc_ref.set(user.dict())
#         return {"message": f"User {user_id} added successfully", "data": user.dict()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")

# # Example endpoint for testing
# @app.get("/")
# async def root():
#     return {"message": "FastAPI with Firestore is running!"}

# sessions = dict()

# @app.get("/login")
# async def login():
#     return {"message": "Login endpoint"}

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# Get user's currently playing track
# current_track = sp.current_user_playing_track()
# if current_track is None:
#     print("No track is currently playing.")
# else:
#     print(current_track["item"]["name"])
#     print(current_track["item"]["artists"][0]["name"])
#     image_url = current_track["item"]["album"]["images"][0]["url"]
#     print(current_track["progress_ms"])
#     print(current_track["item"]["duration_ms"])
#     remaining_ms = current_track["item"]["duration_ms"] - current_track["progress_ms"]
#     print((remaining_ms))



# last_played = sp.current_user_recently_played(1)
# print(last_played["items"][0]["track"]["name"])
# image_url = last_played["items"][0]["track"]["album"]["images"][0]["url"]

# # Grabbing all the artists for the song
# for artist in last_played["items"][0]["track"]["artists"]:
#     print(artist["name"])

# print(last_played["items"][0]["played_at"])

# # Downloading the album art
# img_data = requests.get(image_url).content
# with open('current_album.jpg', 'wb') as handler:
#     handler.write(img_data)

# Get user's last played track
# def get_last_played_track():
#     return sp.current_user_recently_played(1)

# def get_last_played_track_song_title(last_played):
#     return last_played["items"][0]["track"]["name"]

# def get_last_played_track_artists(last_played):
#     artist_array = []
#     for artist in last_played["items"][0]["track"]["artists"]:
#         artist_array.append(artist["name"])
#     return artist_array

# def get_last_played_track_image_url(last_played):
#     return last_played["items"][0]["track"]["album"]["images"][0]["url"]

# def get_last_played_track_time(last_played):
#     return last_played["items"][0]["played_at"]