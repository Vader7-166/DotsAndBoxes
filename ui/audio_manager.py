import pygame
import os
from constants import DEFAULT_VOLUME, MUTE_DEFAULT

class AudioManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        self.bgm_volume = DEFAULT_VOLUME
        self.sfx_volume = DEFAULT_VOLUME
        self.is_muted = MUTE_DEFAULT
        
        self.sfx = {}
        self.bgm_path = None
        
        self._load_assets()
        self._update_volume()

    def _load_assets(self):
        audio_dir = os.path.join('ui', 'assets', 'audio')
        
        # Load SFX
        sfx_files = {
            'move': 'move.wav',
            'score': 'score.wav',
            'gameover': 'gameover.wav'
        }
        
        for name, filename in sfx_files.items():
            path = os.path.join(audio_dir, filename)
            if os.path.exists(path):
                try:
                    self.sfx[name] = pygame.mixer.Sound(path)
                except pygame.error as e:
                    print(f"Warning: Could not load SFX {filename}: {e}")
            else:
                print(f"Warning: SFX file not found: {path}")

        # BGM path
        path = os.path.join(audio_dir, 'bgm.mp3')
        if os.path.exists(path):
            self.bgm_path = path
        else:
            print(f"Warning: BGM file not found: {path}")

    def play_bgm(self):
        if self.bgm_path:
            try:
                pygame.mixer.music.load(self.bgm_path)
                pygame.mixer.music.play(-1) # Loop indefinitely
                self._update_volume()
            except pygame.error as e:
                print(f"Warning: Could not play BGM: {e}")

    def play_sfx(self, name):
        if not self.is_muted and name in self.sfx:
            sound = self.sfx[name]
            sound.set_volume(self.sfx_volume)
            sound.play()

    def set_bgm_volume(self, volume):
        self.bgm_volume = max(0.0, min(1.0, volume))
        self._update_volume()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self._update_volume()

    def _update_volume(self):
        actual_volume = 0.0 if self.is_muted else self.bgm_volume
        pygame.mixer.music.set_volume(actual_volume)
        # SFX volume is set individually when played in play_sfx
