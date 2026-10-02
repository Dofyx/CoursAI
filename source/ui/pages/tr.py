from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QComboBox, QPushButton, QLabel
from PySide6.QtCore import Qt
from pathlib import Path

from config.paths import TR
from audio.manager import Manager


class TrPage(QWidget):
    """Page de gestion des retranscriptions."""
    
    def __init__(self, parent, bus, config):
        super().__init__(parent)
        self.bus = bus
        self.config = config
        self._init_ui()

    def _init_ui(self):
        l = QVBoxLayout(self)
        
        # En-tête
        title = QLabel('Gestion des retranscriptions')
        title.setObjectName('title')
        l.addWidget(title)
        l.addWidget(QLabel('Transcription directe avec Mistral Voxtral.'))
        
        # Groupe "Retranscrire"
        g = QGroupBox('Retranscrire')
        f = QFormLayout(g)
        f.addRow('IA', QLabel('Mistral Voxtral'))
        
        # Liste des enregistrements
        self.trrec = QComboBox()
        f.addRow('Enregistrement', self.trrec)
        
        # Bouton de transcription
        b = QPushButton('Retranscrire')
        b.clicked.connect(self._transcribe)
        f.addRow('', b)
        
        l.addWidget(g)
        
        # Gestionnaire de fichiers
        self.fmtr = Manager('Retranscriptions', TR, ['*.txt'])
        l.addWidget(self.fmtr, 1)

    def _transcribe(self):
        """Démarre la transcription."""
        self._refresh()
        n = self.trrec.currentText()
        if not n:
            self.parent().err('Aucun enregistrement sélectionné.')
            return
        
        from config.settings import get_secret
        k = get_secret('mistral_api_key', self.config)
        if not k:
            self.parent().err('Renseignez la clé Mistral dans Paramètres.')
            return
        
        source = TR / n
        out = TR / (source.stem + '.txt')
        if not self._confirm_overwrite(out, 'La retranscription'):
            return
        
        self.parent().bg(self.parent()._do_transcribe, source, k)

    def _confirm_overwrite(self, path: Path, label: str) -> bool:
        """Demande confirmation avant écrasement."""
        if not path.exists():
            return True
        from PySide6.QtWidgets import QMessageBox
        return QMessageBox.warning(
            self.parent(), 'Fichier existant',
            f'{label} existe déjà :\n\n{path.name}\n\nVoulez-vous l’écraser ? Cette action est irréversible.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        ) == QMessageBox.Yes

    def _refresh(self):
        """Rafraîchit la liste des enregistrements."""
        from config.paths import REC
        from audio.manager import Manager
        temp_manager = Manager('Temp', REC, ['*.wav', '*.mp3', '*.m4a', '*.flac', '*.ogg', '*.opus'])
        self.trrec.clear()
        self.trrec.addItems([p.name for p in temp_manager.paths()])
