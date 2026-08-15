# track_metadata.py - Rich Track Metadata & Classification Pipeline

from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class TrackMetadata:
    path: str
    title: str
    artist: str
    duration: float = 0.0
    bpm: float = 120.0
    key: str = "1A"
    energy: float = 0.5
    culture: str = "global"
    language: str = "en"
    genre: str = "Pop"
    decade: str = "Modern"
    confidence: float = 1.0
    source: str = "manual"

def classify_track(file_path: str) -> TrackMetadata:
    """Classifies a local audio file or stream stub and extracts rich metadata."""
    import os
    filename = os.path.basename(file_path)
    title = os.path.splitext(filename)[0]
    
    # Basic heuristic classification fallback
    culture = "greek_traditional" if "συρτός" in title.lower() or "κρητικ" in title.lower() else "global"
    genre = "Traditional" if culture == "greek_traditional" else "Pop"
    
    return TrackMetadata(
        path=file_path,
        title=title,
        artist="Unknown Artist",
        culture=culture,
        genre=genre,
        source="heuristic"
    )
  
