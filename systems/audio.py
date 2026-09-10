"""Sound and music system"""
import pygame
import random

class SoundManager:
    """Manages sound effects"""
    
    def __init__(self):
        self.sounds = {}
        self.volume = 0.7
        self.enabled = True
    
    def load_sound(self, name, filepath):
        """Load a sound effect"""
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
        except:
            print(f"Failed to load sound: {filepath}")
    
    def play(self, sound_name):
        """Play a sound effect"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        self.sounds[sound_name].play()
    
    def stop(self, sound_name):
        """Stop a sound"""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
    
    def set_volume(self, volume):
        """Set master volume"""
        self.volume = max(0, min(1, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def toggle(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled

class MusicManager:
    """Manages background music"""
    
    def __init__(self):
        self.current_track = None
        self.volume = 0.5
        self.enabled = True
    
    def load_music(self, filepath):
        """Load music track"""
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.volume)
        except:
            print(f"Failed to load music: {filepath}")
    
    def play(self, filepath, loops=-1):
        """Play music"""
        if not self.enabled:
            return
        
        try:
            self.load_music(filepath)
            pygame.mixer.music.play(loops)
            self.current_track = filepath
        except:
            pass
    
    def stop(self):
        """Stop music"""
        pygame.mixer.music.stop()
        self.current_track = None
    
    def set_volume(self, volume):
        """Set music volume"""
        self.volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def toggle(self):
        """Toggle music on/off"""
        self.enabled = not self.enabled
        if self.enabled and self.current_track:
            self.play(self.current_track)
        else:
            self.stop()
