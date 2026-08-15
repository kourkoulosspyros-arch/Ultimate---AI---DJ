# set_planner.py - AI Set Planner with Music Policy Hard & Soft Filtering & Harmonic Mixing

from typing import List, Dict, Any
from music_policy import MusicPolicy, validate_track_against_policy

def get_harmonic_neighbor(current_key: str) -> str:
    """Returns a harmonically compatible key (Camelot Wheel system)."""
    try:
        number = int(current_key[:-1])
        letter = current_key[-1]
        next_number = (number % 12) + 1
        return f"{next_number}{letter}"
    except Exception:
        return "1A"

def sort_by_harmonic_mix(playlist: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Reorders playlist to ensure smooth transitions (Harmonic Mixing)."""
    if not playlist: return []
    ordered = [playlist[0]]
    remaining = playlist[1:]
    
    while remaining:
        last_key = ordered[-1].get("key", "1A")
        target = get_harmonic_neighbor(last_key)
        
        # Find best match
        match = next((t for t in remaining if t.get("key") == target), remaining[0])
        ordered.append(match)
        remaining.remove(match)
        
    return ordered

def plan_set(prompt: str, policy: MusicPolicy, library: List[Dict[str, Any]], target_duration_minutes: int = 60) -> List[Dict[str, Any]]:
    """Plans a dynamic DJ set using the active Music Policy and Harmonic Mixing."""
    selected_tracks = []
    
    # Stage A: Hard Filter available tracks
    valid_pool = []
    for track in library:
        valid, reason = validate_track_against_policy(track, policy)
        if valid:
            valid_pool.append(track)
            
    # If library is empty or all filtered out, use a safe fallback
    if not valid_pool:
        valid_pool = library 
        
    # Build sequence up to target duration
    current_duration = 0.0
    target_seconds = target_duration_minutes * 60
    
    index = 0
    while current_duration < target_seconds and valid_pool:
        track = valid_pool[index % len(valid_pool)]
        selected_tracks.append(track)
        current_duration += track.get("duration", 180.0)
        index += 1
        
    # Apply Professional Harmonic Mixing
    final_set = sort_by_harmonic_mix(selected_tracks)
    return final_set
  
