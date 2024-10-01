import json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from random import sample, shuffle
from components.button import CustomButton

class WordMatchApp(App):
    def build(self):
        self.words = self.load_dictionary('dictionaries/dictionary_q_to_u.json')

        self.selected_button = None

        # Main layout with background
        root = FloatLayout()
        background = Image(source='images/background.jpg', fit_mode="cover")
        root.add_widget(background)

        # Creating a GridLayout
        self.main_layout = GridLayout(cols=2, row_force_default=True, row_default_height=80, padding=10, spacing=10)
        root.add_widget(self.main_layout)

        # Splitting words into columns
        self.left_words = sample(list(self.words.keys()), len(self.words))
        self.right_words = sample(list(self.words.values()), len(self.words))

        # Shuffling each column separately
        shuffle(self.left_words)
        shuffle(self.right_words)

        # Adding buttons to the GridLayout
        self.left_buttons = []
        self.right_buttons = []
        for left_word, right_word in zip(self.left_words, self.right_words):
            left_button = CustomButton(text=left_word)
            left_button.bind(on_press=self.on_word_press)
            self.left_buttons.append(left_button)
            self.main_layout.add_widget(left_button)

            right_button = CustomButton(text=right_word)
            right_button.bind(on_press=self.on_word_press)
            self.right_buttons.append(right_button)
            self.main_layout.add_widget(right_button)

        return root

    @staticmethod
    def load_dictionary(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def on_word_press(self, instance):
        if self.selected_button:
            if (self.selected_button in self.left_buttons and instance in self.left_buttons) or \
               (self.selected_button in self.right_buttons and instance in self.right_buttons):
                self.reset_pair(self.selected_button)
                self.select_button(instance)
            else:
                if (self.selected_button.text in self.words and self.words[self.selected_button.text] == instance.text) or \
                   (instance.text in self.words and self.words[instance.text] == self.selected_button.text):
                    self.correct_pair(self.selected_button, instance)
                else:
                    self.incorrect_pair(self.selected_button, instance)
                self.selected_button = None
        else:
            self.select_button(instance)

    def select_button(self, instance):
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 0.6)  # White with transparency for reset
        instance.background_color = (0, 1, 1, 1)  # Cyan for the selected button
        self.selected_button = instance

    def correct_pair(self, first, second):
        first.background_color = (0, 1, 0, 1)  # Green for correct pair
        second.background_color = (0, 1, 0, 1)  # Green for correct pair
        Clock.schedule_once(lambda dt: self.remove_correct_pair(first, second), 0.5)

    def remove_correct_pair(self, first, second):
        self.remove_button(first)
        self.remove_button(second)
        self.reorganize_buttons()

    def incorrect_pair(self, first, second):
        first.background_color = (1, 0, 0, 1)  # Red for incorrect pair
        second.background_color = (1, 0, 0, 1)  # Red for incorrect pair
        Clock.schedule_once(lambda dt: self.reset_pair(first, second), 0.5)

    def reset_pair(self, first, second=None):
        first.background_color = (1, 1, 1, 0.6)  # White with transparency for reset
        if second:
            second.background_color = (1, 1, 1, 0.6)  # White with transparency for reset

    def remove_button(self, button):
        if button in self.left_buttons:
            index = self.left_buttons.index(button)
            self.left_buttons.pop(index)
            self.left_words.pop(index)
        elif button in self.right_buttons:
            index = self.right_buttons.index(button)
            self.right_buttons.pop(index)
            self.right_words.pop(index)
        self.main_layout.remove_widget(button)

    def reorganize_buttons(self):
        self.main_layout.clear_widgets()
        self.left_buttons.clear()
        self.right_buttons.clear()
        for left_word, right_word in zip(self.left_words, self.right_words):
            left_button = CustomButton(text=left_word)
            left_button.bind(on_press=self.on_word_press)
            self.left_buttons.append(left_button)
            self.main_layout.add_widget(left_button)

            right_button = CustomButton(text=right_word)
            right_button.bind(on_press=self.on_word_press)
            self.right_buttons.append(right_button)
            self.main_layout.add_widget(right_button)
