import sqlite3
from faker import Faker
import random

# Connect to your database
conn = sqlite3.connect('songs.db')
fake = Faker()

# Helper: commit after each section
def commit():
    conn.commit()

# 1. Insert multiple Artists
artist_ids = []
for _ in range(10):  # 10 artists
    name = fake.name()
    conn.execute("INSERT INTO artists (name) VALUES (?)", (name,))
    artist_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    artist_ids.append(artist_id)
commit()

# 2. Insert Albums
album_ids = []
for artist_id in artist_ids:
    for _ in range(random.randint(1, 3)):  # 1–3 albums per artist
        title = fake.sentence(nb_words=3).replace('.', '')
        release_year = random.randint(2000, 2024)
        conn.execute("INSERT INTO albums (title, release_year, artist_id) VALUES (?, ?, ?)", (title, release_year, artist_id))
        album_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        album_ids.append(album_id)
commit()

# 3. Insert Songs
song_ids = []
for album_id in album_ids:
    for _ in range(random.randint(4, 7)):  # 4–7 songs per album
        title = fake.sentence(nb_words=2).replace('.', '')
        duration = random.randint(120, 300)  # 2 to 5 min
        conn.execute("INSERT INTO songs (title, duration_seconds, album_id) VALUES (?, ?, ?)", (title, duration, album_id))
        song_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        song_ids.append(song_id)
commit()

# 4. Insert Users
user_ids = []
for _ in range(10):  # 10 users
    username = fake.user_name()
    password = "password"  # simple password for testing
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=40).strftime("%Y-%m-%d")
    gender = random.choice(['Male', 'Female', 'Other'])
    
    conn.execute("""
        INSERT INTO users (username, password, email, first_name, last_name, dob, gender)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, password, email, first_name, last_name, dob, gender))
    user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    user_ids.append(user_id)
commit()

# 5. Insert Playlists
playlist_ids = []
for user_id in user_ids:
    for _ in range(2):  # 2 playlists per user
        name = fake.sentence(nb_words=2).replace('.', '')
        conn.execute("INSERT INTO playlists (name) VALUES (?)", (name,))
        playlist_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Link playlist to user
        conn.execute("INSERT INTO user_playlists (user_id, playlist_id) VALUES (?, ?)", (user_id, playlist_id))
        playlist_ids.append(playlist_id)
commit()

# 6. Fill Playlists with Songs
for playlist_id in playlist_ids:
    songs_to_add = random.sample(song_ids, random.randint(5, 10))  # 5-10 songs in a playlist
    for song_id in songs_to_add:
        conn.execute("INSERT OR IGNORE INTO playlist_song (playlist_id, song_id) VALUES (?, ?)", (playlist_id, song_id))
commit()

# 7. Liked Songs by Users
for user_id in user_ids:
    liked = random.sample(song_ids, random.randint(5, 15))  # 5-15 liked songs
    for song_id in liked:
        conn.execute("INSERT OR IGNORE INTO liked_songs (user_id, song_id) VALUES (?, ?)", (user_id, song_id))
commit()

# 8. Following Artists
for user_id in user_ids:
    followed_artists = random.sample(artist_ids, random.randint(2, 5))  # Follow 2-5 artists
    for artist_id in followed_artists:
        conn.execute("INSERT OR IGNORE INTO following_artists (user_id, artist_id) VALUES (?, ?)", (user_id, artist_id))
commit()

conn.close()
print("Database successfully filled with demo data!")
