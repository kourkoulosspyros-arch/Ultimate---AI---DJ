# library_scanner.py - Dynamic Local Library Scanner & Classifier

import os
from typing import List, Dict, Any
from track_metadata import classify_track, TrackMetadata

def scan_library(folder_path: str) -> List[Dict[str, Any]]:
    """Scans a folder for audio files and returns classified metadata records."""
    supported_extensions = (".mp3", ".wav", ".flac", ".m4a")
    tracks = []
    
    if not os.path.exists(folder_path):
        # Fallback default catalog if folder doesn't exist yet
        return [
            {"path": "dummy_1.mp3", "title": "Σιγανός Συρτός", "artist": "Κρητικός", "bpm": 105, "key": "3A", "energy": 0.6, "culture": "greek_cretan", "genre": "Traditional", "decade": "Modern"},
            {"path": "dummy_2.mp3", "title": "Rasputin", "artist": "Boney M", "bpm": 128, "key": "3A", "energy": 0.8, "culture": "global", "genre": "Disco", "decade": "80s"},
            {"path": "dummy_3.mp3", "title": "Ibiza Chill Sunset", "artist": "Lounge Artist", "bpm": 95, "key": "1A", "energy": 0.3, "culture": "global", "genre": "Lounge", "decade": "Modern"},
        ]
        
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(supported_extensions):
                full_path = os.path.join(root, file)
                meta: TrackMetadata = classify_track(full_path)
                tracks.append({
                    "path": meta.path,
                    "title": meta.title,
                    "artist": meta.artist,
                    "duration": meta.duration,
                    "bpm": meta.bpm,
                    "key": meta.key,
                    "energy": meta.energy,
                    "culture": meta.culture,
                    "language": meta.language,
                    "genre": meta.genre,
                    "decade": meta.decade
                })
                
    return tracks
  
