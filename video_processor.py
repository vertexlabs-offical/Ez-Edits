"""
🎬 Video Processor Module
Handles video analysis, scene detection, and frame extraction
"""

import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from PIL import Image
import os


class VideoProcessor:
    """
    Core video processing class
    Handles video loading, frame extraction, and analysis
    """
    
    def __init__(self, video_path):
        """Initialize with video file path"""
        self.video_path = video_path
        self.clip = VideoFileClip(video_path)
        self.duration = self.clip.duration
        self.fps = self.clip.fps
        self.width = self.clip.size[0]
        self.height = self.clip.size[1]
        self.scenes = []
        self.silence_segments = []
        self.keyframes = []
        
    def extract_frames(self, num_frames=30):
        """Extract evenly spaced frames from video"""
        frame_indices = np.linspace(0, self.duration - 0.01, num_frames, dtype=int)
        frames = []
        
        for idx in frame_indices:
            frame = self.clip.get_frame(idx)
            frames.append({
                'timestamp': idx / self.fps,
                'frame': frame
            })
        
        return frames
    
    def detect_scenes(self, threshold=30):
        """
        Detect scene changes using frame difference analysis
        Returns list of timestamps where scenes change
        """
        cap = cv2.VideoCapture(self.video_path)
        
        ret, prev_frame = cap.read()
        if not ret:
            return []
            
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
        
        scenes = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # Calculate difference between frames
            diff = cv2.absdiff(prev_gray, gray)
            diff_score = np.mean(diff)
            
            # If difference is significant, it's a scene change
            if diff_score > threshold:
                timestamp = frame_count / self.fps
                scenes.append({
                    'timestamp': timestamp,
                    'confidence': min(diff_score / 50, 1.0),
                    'frame': frame
                })
            
            prev_gray = gray
            frame_count += 1
            
        cap.release()
        self.scenes = scenes
        return scenes
    
    def detect_silence(self, silence_threshold=0.01, min_silence_len=0.5):
        """
        Detect silent segments in video audio
        Returns list of silent segments with start/end times
        """
        if self.clip.audio is None:
            return []
        
        # Get audio as numpy array at 44100 Hz
        audio_data = self.clip.audio.to_soundarray(fps=44100)
        
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Calculate RMS energy in windows
        hop_size = int(44100 * 0.1)  # 100ms windows
        energies = []
        
        for i in range(0, len(audio_data) - hop_size, hop_size):
            window = audio_data[i:i + hop_size]
            rms = np.sqrt(np.mean(window ** 2))
            energies.append(rms)
        
        # Find silent segments
        silent_segments = []
        in_silence = False
        silence_start = 0
        
        for i, energy in enumerate(energies):
            timestamp = i * 0.1  # Each window is 0.1 seconds
            if energy < silence_threshold and not in_silence:
                in_silence = True
                silence_start = timestamp
            elif energy >= silence_threshold and in_silence:
                duration = timestamp - silence_start
                if duration >= min_silence_len:
                    silent_segments.append({
                        'start': silence_start,
                        'end': timestamp,
                        'duration': duration
                    })
                in_silence = False
        
        self.silence_segments = silent_segments
        return silent_segments
    
    def extract_keyframes(self, num_frames=5):
        """
        Extract the most visually interesting frames
        Uses contrast, edge density, and color variance scoring
        """
        cap = cv2.VideoCapture(self.video_path)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Sample more frames than we need, then select best
        sample_positions = np.linspace(0, total_frames - 1, num_frames * 3, dtype=int)
        
        frame_scores = []
        
        for pos in sample_positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            ret, frame = cap.read()
            
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Score based on multiple factors:
                
                # 1. Contrast (sharpness)
                contrast = np.std(gray)
                
                # 2. Edge density (interesting visual elements)
                edges = cv2.Canny(gray, 100, 200)
                edge_density = np.mean(edges) / 255
                
                # 3. Color variance (vibrant visuals)
                color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                color_var = np.std(color_frame.reshape(-1, 3), axis=0).mean()
                
                # Calculate overall score
                score = (contrast / 50) * 0.4 + edge_density * 0.3 + (color_var / 50) * 0.3
                
                frame_scores.append({
                    'position': pos,
                    'timestamp': pos / self.fps,
                    'score': score,
                    'frame': frame,
                    'contrast': contrast,
                    'edge_density': edge_density,
                    'color_variance': color_var
                })
        
        cap.release()
        
        # Sort by score and get top frames
        frame_scores.sort(key=lambda x: x['score'], reverse=True)
        self.keyframes = frame_scores[:num_frames]
        
        return self.keyframes
    
    def get_frame_at(self, timestamp):
        """Get a specific frame at given timestamp"""
        return self.clip.get_frame(timestamp)
    
    def frame_to_image(self, frame):
        """Convert numpy array frame to PIL Image"""
        return Image.fromarray(frame.astype('uint8'))
    
    def get_video_info(self):
        """Get comprehensive video information"""
        return {
            'path': self.video_path,
            'duration': self.duration,
            'fps': self.fps,
            'width': self.width,
            'height': self.height,
            'resolution': f"{self.width}x{self.height}",
            'aspect_ratio': round(self.width / self.height, 2),
            'total_frames': int(self.duration * self.fps),
            'has_audio': self.clip.audio is not None
        }
    
    def close(self):
        """Clean up resources"""
        self.clip.close()
        self.clip.reader.close()
        if hasattr(self.clip, 'audio') and self.clip.audio:
            self.clip.audio.close()


# Helper function for quick analysis
def analyze_video(video_path):
    """Quick helper to analyze a video file"""
    processor = VideoProcessor(video_path)
    
    results = {
        'info': processor.get_video_info(),
        'scenes': processor.detect_scenes(),
        'silence': processor.detect_silence(),
        'keyframes': processor.extract_keyframes(5)
    }
    
    processor.close()
    return results
