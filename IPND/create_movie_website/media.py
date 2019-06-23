# Project: Create Your Own Movie Website

# imports webbrowser module
import webbrowser

# Class provides a way to store movie related information
class Movie():
    def __init__(self, movie_title, movie_storyline, poster_image, trailer_youtube):
        ''' initialize instance of class movie '''
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        ''' opens youtube movie trailer '''
        webbrowser.open(self.trailer_youtube_url)
