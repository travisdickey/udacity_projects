# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id SERIAL PRIMARY KEY,
        start_time bigint NOT NULL,
        user_id integer NOT NULL,
        level text,
        song_id text,
        artist_id text,
        session_id integer,
        location text,
        user_agent text
    ) """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (userId text, firstName text, lastName text, \
                        gender char, level text) """)

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id text, title text, artist_id text, year int, duration double precision)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id text, artist_name text, artist_location text, \
                        artist_latitude numeric, artist_longitude numeric) """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (time time, hour int, day int, weekofyear int,	month int, \
                        year int, weekday int) """)

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""INSERT INTO users (userId, firstName, lastName, gender, level) VALUES \
                        (%s, %s, %s, %s, %s) """)

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES \
                        (%s, %s, %s, %s, %s) """)

artist_table_insert = ("""INSERT INTO artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) VALUES \
                        (%s, %s, %s, %s, %s) """)

time_table_insert = ("""INSERT INTO time (time, hour, day, weekofyear, month, year, weekday) VALUES \
                         (%s, %s, %s, %s, %s, %s, %s) """)

# FIND SONGS

song_select = ("""SELECT song_id, artists.artist_id FROM songs, artists WHERE \
                  title = %s AND artist_name = %s AND duration = %s  """)

# song_select = ("""
# SELECT songs.song_id, artists.artist_id
#    FROM songs JOIN artists ON (songs.artist_id = artists.artist_id)
#    WHERE songs.title ILIKE (%s)
#    AND artists.artist_name ILIKE (%s)
#    AND songs.duration = (%s)
# """)

# QUERY LISTS

# create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
# drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

create_table_queries = [song_table_create, artist_table_create, time_table_create, user_table_create, songplay_table_create]
drop_table_queries = [song_table_drop, artist_table_drop, time_table_drop, user_table_drop, songplay_table_drop]