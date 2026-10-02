from pathlib import Path

try:
    import sounddevice as sd
    import soundfile as sf
    SOUND_AVAILABLE = True
except (OSError, ImportError):
    SOUND_AVAILABLE = False


class Recorder:
    """Gère l'enregistrement audio."""
    
    def __init__(self):
        self.stream = None
        self.file = None
        self.paused = False

    def start(self, path: Path, device: int) -> None:
        """Démarre l'enregistrement."""
        if not SOUND_AVAILABLE:
            raise OSError("La bibliothèque PortAudio n'est pas disponible. Impossible d'enregistrer.")
        
        self.file = sf.SoundFile(
            path, 'w', 
            samplerate=48000, 
            channels=1, 
            subtype='PCM_16'
        )
        
        def callback(indata, frames, time, status):
            if not self.paused:
                self.file.write(indata.copy())
        
        self.stream = sd.InputStream(
            device=device,
            channels=1,
            samplerate=48000,
            callback=callback
        )
        self.stream.start()

    def pause(self) -> None:
        """Met l'enregistrement en pause."""
        self.paused = True

    def resume(self) -> None:
        """Reprend l'enregistrement."""
        self.paused = False

    def stop(self) -> None:
        """Arrête l'enregistrement."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if self.file:
            self.file.close()
            self.file = None
