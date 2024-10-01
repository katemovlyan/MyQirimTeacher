from kivy.uix.button import Button
from kivy.graphics import Color, Line, RoundedRectangle


class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.color = (0, 0, 0, 1)  # Black text color
        with self.canvas.before:
            Color(1, 1, 1, 0.6)  # White color with transparency for the background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
            Color(0.5, 0.5, 0.5, 1)  # Gray color for the borders
            self.line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 20), width=1)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.line.rounded_rectangle = (self.x, self.y, self.width, self.height, 20)

