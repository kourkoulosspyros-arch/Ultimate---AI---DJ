# music_policy.py - Central Music Policy & Hard/Soft Filtering Engine

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class MusicPolicy:
    mode_id: str
    display_name: str
    allowed_cultures: List[str] = field(default_factory=list)
    allowed_languages: List[str] = field(default_factory=list)
    allowed_genres: List[str] = field(default_factory=list)
    allowed_decades: List[str] = field(default_factory=list)
    min_energy: float = 0.0
    max_energy: float = 1.0
    exclusive: bool = False # If True, Hard Filter rejects anything outside allowed lists

POLICIES = {
    "cretan_traditional": MusicPolicy(
        mode_id="cretan_traditional",
        display_name="Κρητικό Γλέντι / Traditional",
        allowed_cultures=["greek_cretan", "greek_traditional"],
        allowed_languages=["el"],
        allowed_genres=["Traditional", "Folk"],
        exclusive=True
    ),
    "ibiza_lounge": MusicPolicy(
        mode_id="ibiza_lounge",
        display_name="Ibiza Lounge Curator",
        allowed_cultures=["global", "ambient"],
        allowed_genres=["Lounge", "Ambient", "Chillout", "Deep House"],
        max_energy=0.5,
        exclusive=True
    ),
    "festival_headliner": MusicPolicy(
        mode_id="festival_headliner",
        display_name="Festival Headliner (EDM/Club)",
        allowed_genres=["EDM", "House", "Club", "Mainstream", "Dance"],
        min_energy=0.6,
        exclusive=False
    ),
    "retro_80s_90s": MusicPolicy(
        mode_id="retro_80s_90s",
        display_name="Retro 80s/90s & Disco King",
        allowed_decades=["80s", "90s"],
        allowed_genres=["Disco", "Pop", "Synth-Pop", "Dance"],
        exclusive=True
    )
}

def parse_natural_language_prompt(prompt: str) -> MusicPolicy:
    text = prompt.lower()
    if "κρητικ" in text or "cretan" in text:
        return POLICIES["cretan_traditional"]
    elif "lounge" in text or "cocktail" in text or "χαλάρωση" in text:
        return POLICIES["ibiza_lounge"]
    elif "80s" in text or "90s" in text or "disco" in text:
        return POLICIES["retro_80s_90s"]
    elif "festival" in text or "club" in text or "edm" in text:
        return POLICIES["festival_headliner"]
    
    return POLICIES["festival_headliner"]

def validate_track_against_policy(track: Dict[str, Any], policy: MusicPolicy) -> tuple[bool, str]:
    """Stage A: Hard Filter. Returns (is_valid, reason_if_invalid)."""
    if policy.exclusive:
        if policy.allowed_genres and track.get("genre") not in policy.allowed_genres:
            return False, f"Genre '{track.get('genre')}' not allowed in policy {policy.mode_id}"
        if policy.allowed_decades and track.get("decade") not in policy.allowed_decades:
            return False, f"Decade '{track.get('decade')}' not allowed in policy {policy.mode_id}"
            
    energy = track.get("energy", 0.5)
    if energy < policy.min_energy or energy > policy.max_energy:
        return False, f"Energy {energy} out of policy bounds [{policy.min_energy}, {policy.max_energy}]"
        
    return True, "OK"
          
