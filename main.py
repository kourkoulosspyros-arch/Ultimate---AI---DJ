# main.py - Ultimate AI DJ Master GUI & Execution Entry Point

import sys
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from music_policy import parse_natural_language_prompt
from library_scanner import scan_library
from set_planner import plan_set
from audio_engine import AudioEngine

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class UltimateAIDJApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Ultimate AI DJ - Autonomous Curator & Engine")
        self.geometry("950x650")
        
        self.audio_engine = AudioEngine()
        self.current_playlist = []
        
        # Layout Setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar Controls
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Ultimate AI DJ", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.prompt_label = ctk.CTkLabel(self.sidebar_frame, text="AI Prompt / Vibe:", anchor="w")
        self.prompt_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.prompt_entry = ctk.CTkEntry(self.sidebar_frame, width=240, placeholder_text="e.g. Κρητικό Γλέντι / Ibiza Lounge")
        self.prompt_entry.grid(row=2, column=0, padx=20, pady=(5, 10))
        self.prompt_entry.insert(0, "Κρητικό Γλέντι / Traditional")
        
        self.generate_btn = ctk.CTkButton(self.sidebar_frame, text="Generate Set & Policy", command=self.generate_set)
        self.generate_btn.grid(row=3, column=0, padx=20, pady=10)
        
        self.stem_btn = ctk.CTkButton(self.sidebar_frame, text="Isolate Stems (AI)", fg_color="green", command=self.run_stem_separation)
        self.stem_btn.grid(row=4, column=0, padx=20, pady=10)
        
        # Main Dashboard Panel
        self.main_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.main_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_panel.grid_rowconfigure(1, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)
        
        self.header_title = ctk.CTkLabel(self.main_panel, text="Active Playlist & Policy Dashboard", font=ctk.CTkFont(size=16, weight="bold"))
        self.header_title.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Playlist Box / Listframe
        self.playlist_box = ctk.CTkTextbox(self.main_panel, width=600, height=450)
        self.playlist_box.grid(row=1, column=0, sticky="nsew")
        self.playlist_box.insert("0.0", "Welcome to Ultimate AI DJ!\nEnter your prompt on the left and click 'Generate Set & Policy' to build your smart set.\n")

    def generate_set(self):
        prompt_text = self.prompt_entry.get()
        policy = parse_natural_language_prompt(prompt_text)
        
        # Scan mock or local library
        library = scan_library("./music_library")
        playlist = plan_set(prompt_text, policy, library, target_duration_minutes=30)
        self.current_playlist = playlist
        
        # Display results in GUI
        self.playlist_box.delete("0.0", "end")
        self.playlist_box.insert("end", f"=== ACTIVE POLICY: {policy.display_name} ===\n")
        self.playlist_box.insert("end", f"Mode ID: {policy.mode_id} | Exclusive Filter: {policy.exclusive}\n\n")
        self.playlist_box.insert("end", "Generated Playlist Sequence:\n" + "-"*40 + "\n")
        
        for i, track in enumerate(playlist, 1):
            line = f"{i}. {track.get('artist', 'Unknown')} - {track.get('title')} [{track.get('genre')}, Energy: {track.get('energy')}]\n"
            self.playlist_box.insert("end", line)

    def run_stem_separation(self):
        if not self.current_playlist:
            messagebox.showwarning("Warning", "Please generate a set first!")
            return
        track = self.current_playlist[0]
        stems = self.audio_engine.separate_stems(track.get("path", "sample.mp3"))
        messagebox.showinfo("AI Stems", f"Stems isolated successfully:\n- Vocals: {stems['vocals']}\n- Drums: {stems['drums']}")

if __name__ == "__main__":
    app = UltimateAIDJApp()
    app.mainloop()
  
