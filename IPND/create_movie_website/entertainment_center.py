# Project: Make Your Own Movie Website

# import media.py file
import media
#import fresh_tomatoes.py file
import fresh_tomatoes

# Define instances of class Movie in media.py
the_matrix = media.Movie("The Matrix", "Part-time hacker discovers the world is not what it seems", "https://upload.wikimedia.org/wikipedia/en/thumb/c/c1/The_Matrix_Poster.jpg/220px-The_Matrix_Poster.jpg", "https://youtu.be/m8e-FF8MsqU?t=38")
few_good_men = media.Movie("A Few Good Men", "Military legal drama", "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/A_Few_Good_Men_poster.jpg/220px-A_Few_Good_Men_poster.jpg", "https://youtu.be/sCrR9uQrPKA")
apollo_13 = media.Movie("Apollo 13", "True story of flight of Apollo 13", "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/Apollo_thirteen_movie.jpg/220px-Apollo_thirteen_movie.jpg", "https://youtu.be/nEl0NsYn1fU?t=9")
doctor_strange = media.Movie("Doctor Strange", "One of the best comic book superhero movies of all time", "https://upload.wikimedia.org/wikipedia/en/thumb/c/c7/Doctor_Strange_poster.jpg/220px-Doctor_Strange_poster.jpg", "https://youtu.be/MWRUNTLisPo")
princess_bride = media.Movie("The Princess Bride", "Whimsical romantic adventure", "https://upload.wikimedia.org/wikipedia/en/d/db/Princess_bride.jpg", "https://youtu.be/YU_-MUJRgyQ?t=8")
the_saint = media.Movie("The Saint", "Nuclear scientist caught in a world of espionage", "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/The_Saint_1997_poster.jpg/220px-The_Saint_1997_poster.jpg", "https://youtu.be/e-DyI420gQA?t=5")

movies = [the_matrix, few_good_men, apollo_13, doctor_strange, princess_bride, the_saint]
fresh_tomatoes.open_movies_page(movies)
