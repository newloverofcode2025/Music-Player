import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x400")

        pygame.mixer.init()

        self.playlist = []
        self.current_song = None

        self.song_label = tk.Label(self.root, text="No song playing", font=("Arial", 14))
        self.song_label.pack(pady=20)

        self.load_button = tk.Button(self.root, text="Load Song", command=self.load_song)
        self.load_button.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_song, width=10)
        self.play_button.pack(side='left', padx=20)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_song, width=10)
        self.pause_button.pack(side='left', padx=20)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_song, width=10)
        self.stop_button.pack(side='left', padx=20)

    def load_song(self):
        song_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if song_path:
            self.playlist.append(song_path)
            self.current_song = song_path
            self.song_label.config(text=os.path.basename(song_path))

    def play_song(self):
        if self.current_song:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.song_label.config(text="No song playing")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()