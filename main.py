from kivy.config import Config
from wordMatchApp import WordMatchApp

# Set the initial window size (width, height)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')


if __name__ == "__main__":
    WordMatchApp().run()
