import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
import os
import json
import time
import random

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Music Player")
        self.root.geometry("800x600")
        self.root.configure(bg="#282828")

        pygame.mixer.init()

        self.playlist = []
        self.current_song_index = 0
        self.is_shuffle = False
        self.is_repeat = False
        self.is_paused = False

        self.create_widgets()

    def create_widgets(self):
        # Song Label
        self.song_label = tk.Label(self.root, text="No song playing", font=("Arial", 14), fg="white", bg="#282828")
        self.song_label.pack(pady=20)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg="#282828")
        buttons_frame.pack(pady=20)

        # Load Button
        self.load_button = tk.Button(buttons_frame, text="Load Song", command=self.load_song, width=15, bg="#4CAF50", fg="white")
        self.load_button.grid(row=0, column=0, padx=10)

        # Play Button
        self.play_button = tk.Button(buttons_frame, text="Play", command=self.play_song, width=15, bg="#2196F3", fg="white")
        self.play_button.grid(row=0, column=1, padx=10)

        # Pause Button
        self.pause_button = tk.Button(buttons_frame, text="Pause", command=self.pause_song, width=15, bg="#FFC107", fg="white")
        self.pause_button.grid(row=0, column=2, padx=10)

        # Stop Button
        self.stop_button = tk.Button(buttons_frame, text="Stop", command=self.stop_song, width=15, bg="#F44336", fg="white")
        self.stop_button.grid(row=0, column=3, padx=10)

        # Next Button
        self.next_button = tk.Button(buttons_frame, text="Next", command=self.next_song, width=15, bg="#9E9E9E", fg="white")
        self.next_button.grid(row=0, column=4, padx=10)

        # Previous Button
        self.previous_button = tk.Button(buttons_frame, text="Previous", command=self.previous_song, width=15, bg="#9E9E9E", fg="white")
        self.previous_button.grid(row=0, column=5, padx=10)

        # Shuffle Button
        self.shuffle_button = tk.Button(buttons_frame, text="Shuffle", command=self.toggle_shuffle, width=15, bg="#9E9E9E", fg="white")
        self.shuffle_button.grid(row=0, column=6, padx=10)

        # Repeat Button
        self.repeat_button = tk.Button(buttons_frame, text="Repeat", command=self.toggle_repeat, width=15, bg="#9E9E9E", fg="white")
        self.repeat_button.grid(row=0, column=7, padx=10)

        # Volume Slider
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient='horizontal', command=self.adjust_volume, bg="#282828", fg="white", troughcolor="#4CAF50")
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=20)

        # Playlist Box
        self.playlist_box = tk.Listbox(self.root, width=50, height=15, bg="#333333", fg="white", selectbackground="#4CAF50")
        self.playlist_box.pack(pady=20)

        # Save Playlist Button
        self.save_playlist_button = tk.Button(self.root, text="Save Playlist", command=self.save_playlist, width=15, bg="#2196F3", fg="white")
        self.save_playlist_button.pack(side='left', padx=10, pady=20)

        # Load Playlist Button
        self.load_playlist_button = tk.Button(self.root, text="Load Playlist", command=self.load_playlist, width=15, bg="#2196F3", fg="white")
        self.load_playlist_button.pack(side='left', padx=10, pady=20)

        # Duration and Elapsed Labels
        self.duration_label = tk.Label(self.root, text="Duration: 00:00", font=("Arial", 12), fg="white", bg="#282828")
        self.duration_label.pack(pady=10)

        self.elapsed_label = tk.Label(self.root, text="Elapsed: 00:00", font=("Arial", 12), fg="white", bg="#282828")
        self.elapsed_label.pack(pady=10)

    def load_song(self):
        song_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if song_path:
            self.playlist.append(song_path)
            self.playlist_box.insert(tk.END, os.path.basename(song_path))
            if not self.current_song_index:
                self.current_song_index = 0
                self.current_song = song_path
                self.song_label.config(text=os.path.basename(song_path))

    def play_song(self):
        if self.playlist:
            self.current_song = self.playlist[self.current_song_index]
            self.song_label.config(text=os.path.basename(self.current_song))
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.is_paused = False
            self.update_duration()

    def pause_song(self):
        if not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
        else:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop_song(self):
        pygame.mixer.music.stop()
        self.song_label.config(text="No song playing")
        self.duration_label.config(text="Duration: 00:00")
        self.elapsed_label.config(text="Elapsed: 00:00")

    def next_song(self):
        if self.playlist:
            if self.is_shuffle:
                self.current_song_index = random.randint(0, len(self.playlist) - 1)
            else:
                self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.play_song()

    def previous_song(self):
        if self.playlist:
            if self.is_shuffle:
                self.current_song_index = random.randint(0, len(self.playlist) - 1)
            else:
                self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.play_song()

    def toggle_shuffle(self):
        self.is_shuffle = not self.is_shuffle
        if self.is_shuffle:
            self.shuffle_button.config(relief='sunken')
        else:
            self.shuffle_button.config(relief='raised')

    def toggle_repeat(self):
        self.is_repeat = not self.is_repeat
        if self.is_repeat:
            self.repeat_button.config(relief='sunken')
        else:
            self.repeat_button.config(relief='raised')

    def adjust_volume(self, value):
        volume = float(value)
        pygame.mixer.music.set_volume(volume)

    def save_playlist(self):
        playlist_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if playlist_path:
            with open(playlist_path, "w") as file:
                json.dump(self.playlist, file)
            messagebox.showinfo("Success", "Playlist saved successfully!")

    def load_playlist(self):
        playlist_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if playlist_path:
            with open(playlist_path, "r") as file:
                self.playlist = json.load(file)
            self.playlist_box.delete(0, tk.END)
            for song in self.playlist:
                self.playlist_box.insert(tk.END, os.path.basename(song))
            self.current_song_index = 0
            self.current_song = self.playlist[self.current_song_index]
            self.song_label.config(text=os.path.basename(self.current_song))

    def update_duration(self):
        if self.playlist:
            song_length = pygame.mixer.Sound(self.current_song).get_length()
            minutes, seconds = divmod(song_length, 60)
            self.duration_label.config(text=f"Duration: {int(minutes):02d}:{int(seconds):02d}")
            self.update_elapsed()

    def update_elapsed(self):
        if pygame.mixer.music.get_busy():
            elapsed_time = pygame.mixer.music.get_pos() / 1000
            minutes, seconds = divmod(elapsed_time, 60)
            self.elapsed_label.config(text=f"Elapsed: {int(minutes):02d}:{int(seconds):02d}")
            self.root.after(1000, self.update_elapsed)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()