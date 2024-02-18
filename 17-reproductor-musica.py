import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import pygame

class MusicPlayer(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pygame.mixer.init()

    def build(self):
        self.title = "Reproductor de Música"
        self.song_list = self.find_mp3_files()
        self.current_song = None
        self.playing = False

        # Imprimir la lista de canciones y sus rutas
        print("Lista de canciones disponibles:")
        for song_path in self.song_list:
            print(song_path)

        layout = BoxLayout(orientation="vertical")

        self.song_label = Label(text="Selecciona una Canción")
        layout.add_widget(self.song_label)

        for song_path in self.song_list:
            song_name = os.path.basename(song_path)
            button = Button(text=song_name, size_hint_y=None, height=40)
            button.bind(on_press=self.play_song)
            layout.add_widget(button)

        self.play_button = Button(text="Play", size_hint_y=None, height=40)
        self.play_button.bind(on_press=self.toggle_play)
        layout.add_widget(self.play_button)

        return layout
    
    def find_mp3_files(self):
        music_dir = os.path.expanduser("~/Escritorio/Música")  # Directorio de música del usuario
        songs = []
        for root, dirs, files in os.walk(music_dir):
            for file in files:
                if file.endswith(".mp3"):
                    songs.append(os.path.join(root, file))
        return songs
    
    def play_song(self, instance):
        song_name = instance.text
        song_path = self.get_song_path(song_name)
        if not song_path:
            print(f"Archivo de música '{song_name}' no encontrado.")
            return
        if self.current_song:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.current_song = song_path
        self.song_label.text = f"Reproduciendo: {song_name}"
        self.playing = True
        self.play_button.text = "Pause"

    def get_song_path(self, song_name):
        for song_path in self.song_list:
            if song_name == os.path.basename(song_path):
                return song_path
        return None

    def toggle_play(self, instance):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            self.play_button.text = "Play"
        else:
            pygame.mixer.music.unpause()
            self.playing = True
            self.play_button.text = "Pause"

if __name__ == "__main__":
    MusicPlayer().run()
