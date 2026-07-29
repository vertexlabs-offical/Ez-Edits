"""
🤖 AI Features Module
Handles AI-powered editing features: captions, smart cuts, transitions
"""

import random
from typing import List, Dict


class AICaptionGenerator:
    """
    Generate styled captions from video transcription
    Uses Whisper for transcription (can be simulated)
    """
    
    CAPTION_STYLES = {
        'modern': {
            'name': 'Modern Glow',
            'font_size': 32,
            'color': '#FFFFFF',
            'background': 'rgba(102, 126, 234, 0.8)',
            'position': 'bottom',
            'animation': 'pop',
            'stroke': '#000000'
        },
        'classic': {
            'name': 'Classic Yellow',
            'font_size': 28,
            'color': '#FFFF00',
            'background': 'rgba(0, 0, 0, 0.6)',
            'position': 'bottom',
            'animation': 'fade',
            'stroke': '#000000'
        },
        'bold': {
            'name': 'Bold Center',
            'font_size': 38,
            'color': '#FFFFFF',
            'background': 'rgba(255, 0, 0, 0.8)',
            'position': 'center',
            'animation': 'typewriter',
            'stroke': '#000000'
        },
        'subtle': {
            'name': 'Subtle Bottom',
            'font_size': 24,
            'color': '#CCCCCC',
            'background': 'none',
            'position': 'bottom',
            'animation': 'fade',
            'stroke': '#333333'
        },
        'glow': {
            'name': 'Neon Glow',
            'font_size': 34,
            'color': '#00FFFF',
            'background': 'rgba(0, 100, 100, 0.6)',
            'position': 'bottom',
            'animation': 'glow',
            'stroke': '#00FFFF'
        },
        'neon': {
            'name': 'Cyber Neon',
            'font_size': 32,
            'color': '#FF00FF',
            'background': 'rgba(50, 0, 50, 0.8)',
            'position': 'center',
            'animation': 'neon',
            'stroke': '#FF00FF'
        },
        'minimal': {
            'name': 'Minimal White',
            'font_size': 26,
            'color': '#FFFFFF',
            'background': 'none',
            'position': 'bottom',
            'animation': 'fade',
            'stroke': 'none'
        },
        'retro': {
            'name': 'Retro VHS',
            'font_size': 28,
            'color': '#FFFFFF',
            'background': 'rgba(255, 165, 0, 0.7)',
            'position': 'bottom',
            'animation': 'glitch',
            'stroke': '#000000'
        }
    }
    
    def __init__(self, style='modern'):
        self.style_config = self.CAPTION_STYLES.get(style, self.CAPTION_STYLES['modern'])
        
    def get_available_styles(self):
        """Return list of available caption styles"""
        return [(k, v['name']) for k, v in self.CAPTION_STYLES.items()]
    
    def highlight_keywords(self, text: str) -> str:
        """Highlight emphasis words in caption text"""
        emphasis_words = [
            'amazing', 'incredible', 'wow', 'fantastic', 'key', 
            'important', 'remember', 'forever', 'mind-blowing', 
            'unbelievable', 'wow', 'boom', 'shocking', 'essential'
        ]
        
        words = text.split()
        highlighted = []
        
        for word in words:
            clean_word = word.lower().strip('.,!?')
            if clean_word in emphasis_words:
                highlighted.append(f"**{word}**")
            else:
                highlighted.append(word)
        
        return ' '.join(highlighted)
    
    def generate_mock_transcription(self, duration: float) -> List[Dict]:
        """Generate realistic mock transcription for demo"""
        sample_phrases = [
            "Welcome back to the channel",
            "Today we're going to talk about",
            "This is something you need to know",
            "Let me show you exactly how",
            "The key insight here is",
            "Here's what happens next",
            "This is absolutely amazing",
            "You won't believe what",
            "The most important part is",
            "Now let's get into it",
            "Thanks for watching",
            "Don't forget to subscribe",
            "Leave a comment below",
            "Share this with your friends",
            "This changes everything"
        ]
        
        transcription = []
        current_time = random.uniform(0.5, 2.0)
        
        while current_time < duration:
            phrase = random.choice(sample_phrases)
            duration_sec = len(phrase.split()) * 0.3 + random.uniform(0.5, 1.5)
            
            transcription.append({
                'start': current_time,
                'end': current_time + duration_sec,
                'text': phrase,
                'confidence': random.uniform(0.85, 0.99)
            })
            
            current_time += duration_sec + random.uniform(0.3, 1.0)
        
        return transcription


class SmartCutAnalyzer:
    """
    AI-powered cut suggestions and auto-editing
    """
    
    def __init__(self):
        self.cut_types = [
            'jump_cut',
            'fade_transition',
            'cut_away',
            'B-roll_insert',
            'zoom_cut',
            'speed_ramp'
        ]
    
    def suggest_cuts(self, video_duration: float, scenes: List[Dict], 
                    silence_segments: List[Dict] = None) -> List[Dict]:
        """Analyze video and suggest intelligent cuts"""
        cuts = []
        
        # Add cuts at scene changes
        for i, scene in enumerate(scenes):
            cut = {
                'timestamp': scene['timestamp'],
                'type': 'scene_change',
                'confidence': scene.get('confidence', 0.5),
                'action': 'cut',
                'transition': 'fade'
            }
            cuts.append(cut)
        
        # Suggest jump cuts for long segments
        if scenes:
            last_scene = 0
            for scene in scenes:
                if scene['timestamp'] - last_scene > 10:
                    # Long segment - suggest jump cut in the middle
                    cuts.append({
                        'timestamp': last_scene + (scene['timestamp'] - last_scene) / 2,
                        'type': 'jump_cut',
                        'confidence': 0.7,
                        'action': 'jump_cut'
                    })
                last_scene = scene['timestamp']
        
        # Mark silence segments for removal
        if silence_segments:
            for silence in silence_segments:
                if silence['duration'] > 0.5:
                    cuts.append({
                        'timestamp': silence['start'],
                        'type': 'silence_removal',
                        'confidence': 0.95,
                        'action': 'remove',
                        'start': silence['start'],
                        'end': silence['end'],
                        'duration': silence['duration']
                    })
        
        return sorted(cuts, key=lambda x: x['timestamp'])
    
    def find_jump_cut_moments(self, scenes: List[Dict], video_duration: float) -> List[Dict]:
        """Find optimal locations for jump cuts"""
        jump_moments = []
        
        # Find long talking segments
        last_scene = 0
        for scene in scenes:
            segment_duration = scene['timestamp'] - last_scene
            if segment_duration > 8:  # More than 8 seconds talking
                # Suggest jump cuts at regular intervals
                num_jumps = int(segment_duration / 4)  # Every 4 seconds
                for i in range(num_jumps):
                    jump_time = last_scene + (i + 1) * 4
                    if jump_time < scene['timestamp'] - 2:  # Leave 2s buffer before scene change
                        jump_moments.append({
                            'timestamp': jump_time,
                            'confidence': 0.8,
                            'reason': 'Long talking segment'
                        })
            last_scene = scene['timestamp']
        
        return jump_moments


class TransitionEffects:
    """
    Video transition effects library
    """
    
    TRANSITIONS = {
        'none': {'name': 'None (Hard Cut)', 'duration': 0, 'difficulty': 'Easy'},
        'fade': {'name': 'Fade', 'duration': 0.5, 'difficulty': 'Easy'},
        'dissolve': {'name': 'Dissolve', 'duration': 0.5, 'difficulty': 'Easy'},
        'wipe_left': {'name': 'Wipe Left', 'duration': 0.4, 'difficulty': 'Medium'},
        'wipe_right': {'name': 'Wipe Right', 'duration': 0.4, 'difficulty': 'Medium'},
        'wipe_up': {'name': 'Wipe Up', 'duration': 0.4, 'difficulty': 'Medium'},
        'wipe_down': {'name': 'Wipe Down', 'duration': 0.4, 'difficulty': 'Medium'},
        'zoom_in': {'name': 'Zoom In', 'duration': 0.3, 'difficulty': 'Easy'},
        'zoom_out': {'name': 'Zoom Out', 'duration': 0.3, 'difficulty': 'Easy'},
        'slide': {'name': 'Slide', 'duration': 0.4, 'difficulty': 'Medium'},
        'blur': {'name': 'Blur', 'duration': 0.5, 'difficulty': 'Hard'},
        'crosszoom': {'name': 'Cross Zoom', 'duration': 0.6, 'difficulty': 'Hard'},
        'glitch': {'name': 'Glitch', 'duration': 0.3, 'difficulty': 'Hard'},
        'rgb_split': {'name': 'RGB Split', 'duration': 0.4, 'difficulty': 'Hard'},
        'circle_wipe': {'name': 'Circle Wipe', 'duration': 0.5, 'difficulty': 'Medium'}
    }
    
    def get_all_transitions(self):
        """Get all available transitions"""
        return self.TRANSITIONS
    
    def get_transition(self, name: str) -> Dict:
        """Get transition parameters by name"""
        return self.TRANSITIONS.get(name, self.TRANSITIONS['none'])


class AudioEnhancer:
    """
    AI audio enhancement features
    """
    
    def __init__(self):
        self.sound_effects = {
            'whoosh': {'name': 'Whoosh', 'duration': 0.5, 'category': 'Transitions', 'volume': 0.6},
            'impact': {'name': 'Impact Hit', 'duration': 0.3, 'category': 'Effects', 'volume': 0.8},
            'ding': {'name': 'Notification Ding', 'duration': 0.4, 'category': 'Notifications', 'volume': 0.7},
            'whoop': {'name': 'Whoop Up', 'duration': 0.6, 'category': 'Transitions', 'volume': 0.6},
            'pop': {'name': 'Pop', 'duration': 0.2, 'category': 'Effects', 'volume': 0.5},
            'swoosh': {'name': 'Swoosh', 'duration': 0.8, 'category': 'Transitions', 'volume': 0.5},
            'laugh': {'name': 'Laughter', 'duration': 1.5, 'category': 'Reactions', 'volume': 0.7},
            'applause': {'name': 'Applause', 'duration': 2.0, 'category': 'Reactions', 'volume': 0.6},
            'transition': {'name': 'Transition Whoosh', 'duration': 1.0, 'category': 'Transitions', 'volume': 0.5},
            'reveal': {'name': 'Reveal', 'duration': 0.7, 'category': 'Effects', 'volume': 0.6},
            'blip': {'name': 'Blip', 'duration': 0.1, 'category': 'UI', 'volume': 0.4},
            'click': {'name': 'Click', 'duration': 0.1, 'category': 'UI', 'volume': 0.4},
            'success': {'name': 'Success Chime', 'duration': 0.5, 'category': 'Notifications', 'volume': 0.7},
            'error': {'name': 'Error Sound', 'duration': 0.3, 'category': 'Notifications', 'volume': 0.6},
            'drum_roll': {'name': 'Drum Roll', 'duration': 2.0, 'category': 'Effects', 'volume': 0.5},
            'cymbal': {'name': 'Cymbal Crash', 'duration': 1.5, 'category': 'Effects', 'volume': 0.7}
        }
        
        self.background_music = {
            'uplifting': {'name': 'Uplifting Pop', 'bpm': 120, 'mood': 'Positive', 'duration': 60},
            'chill': {'name': 'Chill Beats', 'bpm': 85, 'mood': 'Relaxed', 'duration': 60},
            'epic': {'name': 'Epic Orchestra', 'bpm': 100, 'mood': 'Dramatic', 'duration': 60},
            'corporate': {'name': 'Corporate Positive', 'bpm': 110, 'mood': 'Professional', 'duration': 60},
            'energetic': {'name': 'Energetic EDM', 'bpm': 140, 'mood': 'Exciting', 'duration': 60},
            'ambient': {'name': 'Ambient Background', 'bpm': 60, 'mood': 'Calm', 'duration': 60},
            'acoustic': {'name': 'Acoustic Guitar', 'bpm': 95, 'mood': 'Warm', 'duration': 60},
            'cinematic': {'name': 'Cinematic Tension', 'bpm': 80, 'mood': 'Tense', 'duration': 60},
            'happy': {'name': 'Happy Ukulele', 'bpm': 115, 'mood': 'Cheerful', 'duration': 60},
            'inspiring': {'name': 'Inspiring Piano', 'bpm': 100, 'mood': 'Motivating', 'duration': 60}
        }
    
    def get_sfx_by_category(self, category: str = None):
        """Get sound effects, optionally filtered by category"""
        if category:
            return [sfx for sfx in self.sound_effects.values() if sfx['category'] == category]
        return list(self.sound_effects.values())
    
    def get_music_by_mood(self, mood: str = None):
        """Get music tracks, optionally filtered by mood"""
        if mood:
            return [track for track in self.background_music.values() 
                   if track['mood'].lower() == mood.lower()]
        return list(self.background_music.values())
    
    def suggest_sfx_for_cuts(self, cuts: List[Dict]) -> List[Dict]:
        """Suggest sound effects for each cut type"""
        suggestions = []
        
        for cut in cuts:
            if cut['type'] == 'scene_change':
                suggestions.append({
                    'timestamp': cut['timestamp'],
                    'sfx': 'whoosh',
                    'volume': 0.6,
                    'offset': 0
                })
            elif cut['type'] == 'jump_cut':
                suggestions.append({
                    'timestamp': cut['timestamp'],
                    'sfx': 'pop',
                    'volume': 0.4,
                    'offset': 0
                })
            elif cut['type'] == 'silence_removal':
                suggestions.append({
                    'timestamp': cut['timestamp'],
                    'sfx': 'transition',
                    'volume': 0.5,
                    'offset': 0
                })
        
        return suggestions


class ThumbnailGenerator:
    """
    AI thumbnail generation and selection
    """
    
    def __init__(self):
        self.title_templates = [
            "Must Watch Moment",
            "The Key Insight",
            "Here's What Happened",
            "Watch This Part",
            "The Big Reveal",
            "Don't Miss This",
            "Game Changer",
            "Essential Viewing",
            "This Changed Everything",
            "You Need to See This",
            "The Truth About...",
            "Why Everyone's Talking About"
        ]
    
    def generate_thumbnails(self, keyframes: List[Dict], num_thumbnails: int = 5) -> List[Dict]:
        """Generate thumbnail options from keyframes"""
        thumbnails = []
        
        for i, kf in enumerate(keyframes[:num_thumbnails]):
            thumbnail = {
                'frame': kf['frame'],
                'timestamp': kf['timestamp'],
                'score': kf.get('score', 0.5),
                'title_suggestion': random.choice(self.title_templates),
                'rating': self._rate_thumbnail(kf),
                'contrast': kf.get('contrast', 0.5),
                'brightness': self._estimate_brightness(kf['frame'])
            }
            thumbnails.append(thumbnail)
        
        return sorted(thumbnails, key=lambda x: x['score'], reverse=True)
    
    def _rate_thumbnail(self, frame_data: Dict) -> str:
        """Rate thumbnail quality based on score"""
        score = frame_data.get('score', 0.5)
        
        if score > 0.75:
            return "⭐⭐⭐ Excellent"
        elif score > 0.55:
            return "⭐⭐ Good"
        elif score > 0.35:
            return "⭐ Average"
        else:
            return "Below Average"
    
    def _estimate_brightness(self, frame) -> str:
        """Estimate frame brightness"""
        if frame is None:
            return "Unknown"
        
        # Calculate average brightness
        import numpy as np
        brightness = np.mean(frame)
        
        if brightness > 200:
            return "Very Bright"
        elif brightness > 150:
            return "Bright"
        elif brightness > 100:
            return "Normal"
        elif brightness > 50:
            return "Dark"
        else:
            return "Very Dark"


class ColorGrader:
    """
    Color grading presets for cinematic look
    """
    
    PRESETS = {
        'cinematic': {
            'name': 'Cinematic Look',
            'contrast': 1.2,
            'saturation': 0.9,
            'temperature': -10,  # Cooler
            'vignette': True,
            'grain': 0.02
        },
        'vintage': {
            'name': 'Vintage Film',
            'contrast': 1.1,
            'saturation': 0.8,
            'temperature': 15,  # Warmer
            'vignette': True,
            'grain': 0.05
        },
        'vibrant': {
            'name': 'Vibrant Colors',
            'contrast': 1.3,
            'saturation': 1.3,
            'temperature': 0,
            'vignette': False,
            'grain': 0
        },
        'muted': {
            'name': 'Muted Tones',
            'contrast': 1.0,
            'saturation': 0.7,
            'temperature': -5,
            'vignette': False,
            'grain': 0.01
        },
        'teal_orange': {
            'name': 'Teal & Orange',
            'contrast': 1.2,
            'saturation': 1.1,
            'temperature': -15,
            'vignette': True,
            'grain': 0.02
        }
    }
    
    def get_presets(self):
        """Get all available color presets"""
        return self.PRESETS
