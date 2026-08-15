# set_planner.py - AI Set Planner with Music Policy Hard & Soft Filtering

from typing import List, Dict, Any
from music_policy import MusicPolicy, validate_track_against_policy

def plan_set(prompt: str, policy: MusicPolicy, library: List[Dict[str, Any]], target_duration_minutes: int = 60) -> List[Dict[str, Any]]:
    """Plans a dynamic DJ set using the active Music Policy."""
    selected_tracks = []
    
    # Stage A: Hard Filter available tracks
    valid_pool = []
    for track in library:
        valid, reason = validate_track_against_policy(track, policy)
        if valid:
            valid_pool.append(track)
            
    # If library is empty or all filtered out, use a safe fallback from library if any, or empty
    if not valid_pool:
        valid_pool = library # Fallback safety if strict filter leaves 0 tracks
        
    # Build sequence up to target duration
    current_duration = 0.0
    target_seconds = target_duration_minutes * 60
    
    index = 0
    while current_duration < target_seconds and valid_pool:
        track = valid_pool[index % len(valid_pool)]
        selected_tracks.append(track)
        current_duration += track.get("duration", 180.0)
        index += 1
        
    return selected_tracks
  
