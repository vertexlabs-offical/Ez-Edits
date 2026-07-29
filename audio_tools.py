"""
🔊 Audio Tools Module
Handles audio manipulation, sound effects, and background music
"""

from typing import List, Dict
from pydub import AudioSegment


class AudioTools:
    """
    Audio processing and manipulation tools
    """
    
    def __init__(self):
        self.effects_library = {
            'sfx': [
                {'id': 'whoosh', 'name': 'Whoosh', 'category': 'Transitions', 'duration': 0.5},
                {'id': 'impact', 'name': 'Impact Hit', 'category': 'Effects', 'duration': 0.3},
                {'id': 'ding', 'name': 'Notification Ding', 'category': 'Notifications', 'duration': 0.4},
                {'id': 'whoop', 'name': 'Whoop Up', 'category': 'Transitions', 'duration': 0.6},
                {'id': 'pop', 'name': 'Pop', 'category': 'Effects', 'duration': 0.2},
                {'id': 'swoosh', 'name': 'Swoosh', 'category': 'Transitions', 'duration': 0.8},
                {'id': 'laugh', 'name': 'Laughter', 'category': 'Reactions', 'duration': 1.5},
                {'id': 'applause', 'name': 'Applause', 'category': 'Reactions', 'duration': 2.0},
                {'id': 'transition', 'name': 'Transition Whoosh', 'category': 'Transitions', 'duration': 1.0},
                {'id': 'reveal', 'name': 'Reveal', 'category': 'Effects', 'duration': 0.7},
                {'id': 'blip', 'name': 'Blip', 'category': 'UI', 'duration': 0.1},
                {'id': 'click', 'name': 'Click', 'category': 'UI', 'duration': 0.1},
                {'id': 'success', 'name': 'Success Chime', 'category': 'Notifications', 'duration': 0.5},
                {'id': 'error', 'name': 'Error Sound', 'category': 'Notifications', 'duration': 0.3},
                {'id': 'drum_roll', 'name': 'Drum Roll', 'category': 'Effects', 'duration': 2.0},
                {'id': 'cymbal', 'name': 'Cymbal Crash', 'category': 'Effects', 'duration': 1.5}
            ],
            'music': [
                {'id': 'uplifting', 'name': 'Uplifting Pop', 'bpm': 120, 'mood': 'Positive', 'duration': 60},
                {'id': 'chill', 'name': 'Chill Beats', 'bpm': 85, 'mood': 'Relaxed', 'duration': 60},
                {'id': 'epic', 'name': 'Epic Orchestra', 'bpm': 100, 'mood': 'Dramatic', 'duration': 60},
                {'id': 'corporate', 'name': 'Corporate Positive', 'bpm': 110, 'mood': 'Professional', 'duration': 60},
                {'id': 'energetic', 'name': 'Energetic EDM', 'bpm': 140, 'mood': 'Exciting', 'duration': 60},
                {'id': 'ambient', 'name': 'Ambient Background', 'bpm': 60, 'mood': 'Calm', 'duration': 60},
                {'id': 'acoustic', 'name': 'Acoustic Guitar', 'bpm': 95, 'mood': 'Warm', 'duration': 60},
                {'id': 'cinematic', 'name': 'Cinematic Tension', 'bpm': 80, 'mood': 'Tense', 'duration': 60},
                {'id': 'happy', 'name': 'Happy Ukulele', 'bpm': 115, 'mood': 'Cheerful', 'duration': 60},
                {'id': 'inspiring', 'name': 'Inspiring Piano', 'bpm': 100, 'mood': 'Motivating', 'duration': 60}
            ]
        }
    
    def get_sfx_categories(self) -> Dict:
        """Get all SFX organized by category"""
        categories = {}
        for sfx in self.effects_library['sfx']:
            cat = sfx['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(sfx)
        return categories
    
    def get_music_by_mood(self, mood: str = None) -> List[Dict]:
        """Get music tracks, optionally filtered by mood"""
        tracks = self.effects_library['music']
        if mood:
            tracks = [t for t in tracks if t['mood'].lower() == mood.lower()]
        return tracks
    
    def get_all_sfx(self) -> List[Dict]:
        """Get all sound effects"""
        return self.effects_library['sfx']
    
    def get_all_music(self) -> List[Dict]:
        """Get all music tracks"""
        return self.effects_library['music']


class SoundEffect:
    """Individual sound effect with parameters"""
    
    def __init__(self, name: str, duration: float, volume: float = 0):
        self.name = name
        self.duration = duration
        self.volume = volume
        self.start_time = 0
        self.fade_in = 0.05
        self.fade_out = 0.05
        
    def set_position(self, timestamp: float):
        """Set when this effect plays in the timeline"""
        self.start_time = timestamp
        return self
    
    def set_fades(self, fade_in: float, fade_out: float):
        """Set fade in/out times"""
        self.fade_in = fade_in
        self.fade_out = fade_out
        return self


class AudioTrack:
    """Audio track containing multiple sound effects and music"""
    
    def __init__(self, name: str = "Main Track"):
        self.name = name
        self.effects: List[SoundEffect] = []
        self.music = None
        self.voice_audio = None
        
    def add_effect(self, effect: SoundEffect):
        """Add a sound effect to this track"""
        self.effects.append(effect)
        return self
        
    def set_music(self, music_track: Dict, volume: float = -20, loop: bool = True):
        """Set background music for this track"""
        self.music = {
            'track': music_track,
            'volume': volume,
            'loop': loop
        }
        return self
    
    def get_total_duration(self) -> float:
        """Calculate total duration of the track"""
        if self.effects:
            max_time = max(e.start_time + e.duration for e in self.effects)
        else:
            max_time = 0
            
        if self.music:
            max_time = max(max_time, self.music['track']['duration'])
            
        return max_time


class AudioMixer:
    """
    Mix multiple audio tracks with ducking
    """
    
    def __init__(self):
        self.tracks = []
        
    def add_track(self, track: AudioTrack):
        """Add an audio track"""
        self.tracks.append(track)
        
    def mix_with_ducking(self, speech_level: float = 0, music_level: float = -20):
        """
        Mix audio with automatic ducking
        Reduces music volume when speech is detected
        """
        # This is a simplified version - real implementation would use pydub
        return {
            'speech_level': speech_level,
            'music_level': music_level,
            'ducking_threshold': -30,
            'ducking_ratio': 0.3
        }
    
    def get_mix_settings(self) -> Dict:
        """Get recommended mix settings"""
        return {
            'speech': 0,  # 0dB (full volume)
            'music': -18,  # -18dB (background)
            'sfx': -6,  # -6dB (prominent)
            'master': -3  # Slight limiting
        }
