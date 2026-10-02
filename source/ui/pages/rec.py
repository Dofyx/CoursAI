from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QComboBox, QLineEdit, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from pathlib import Path

from config.paths import REC
from config.settings import load_config
from audio.manager import Manager
from audio.recorder import Recorder
from utils.helpers import stem, clean


class RecPage(QWidget):
    """Page d'enregistrement et de gestion des fichiers audio."""
    
    def __init__(self, parent, bus, config, recorder):
        super().__init__(parent)
        self.bus = bus
        self.config = config
        self.recorder = recorder
        self._init_ui()

    def _init_ui(self):
        l = QVBoxLayout(self)
        
        # En-tête
        title = QLabel('Gestion de l\'enregistrement')
        title.setObjectName('title')
        l.addWidget(title)
        l.addWidget(QLabel('Nommage automatique : matière, titre, date et heure.'))
        
        # Groupe "Nouveau cours"
        g = QGroupBox('Nouveau cours')
        f = QFormLayout(g)
        
        # Matière
        self.subject = QComboBox()
        f.addRow('Matière', self.subject)
        
        # Titre du cours
        self.course = QLineEdit()
        self.course.setPlaceholderText('Ex. Introduction au droit constitutionnel')
        self.course.textChanged.connect(self._preview)
        self.subject.currentTextChanged.connect(self._preview)
        f.addRow('Titre du cours', self.course)
        
        # Aperçu du nom
        self.name_preview = QLabel()
        self.name_preview.setWordWrap(True)
        f.addRow('Nom produit', self.name_preview)
        
        # Microphone
        self.mic = QComboBox()
        import sounddevice as sd
        for i, d in enumerate(sd.query_devices()):
            if d['max_input_channels'] > 0:
                self.mic.addItem(f"{d['name']} ({i})", i)
        f.addRow('Microphone', self.mic)
        
        # Boutons d'action
        h = QHBoxLayout()
        for text, func in [
            ('● Commencer', self._start),
            ('Pause', lambda: (self.recorder.pause(), self.parent().statusBar().showMessage('En pause'))),
            ('Reprendre', lambda: (self.recorder.resume(), self.parent().statusBar().showMessage('Repris'))),
            ('Fin', self._stop),
            ('Ajouter un fichier audio', self._import_audio)
        ]:
            b = QPushButton(text)
            b.clicked.connect(func)
            h.addWidget(b)
        f.addRow(h)
        
        l.addWidget(g)
        
        # Gestionnaire de fichiers
        self.fmrec = Manager('Enregistrements', REC, ['*.wav', '*.mp3', '*.m4a', '*.flac', '*.ogg', '*.opus'])
        l.addWidget(self.fmrec, 1)
        
        # Charger les matières
        self._load_subjects()

    def _load_subjects(self):
        """Charge la liste des matières depuis la config."""
        cur = self.subject.currentText() if hasattr(self, 'subject') else ''
        self.subject.clear()
        self.subject.addItems(self.config.get('subjects', []))
        i = self.subject.findText(cur)
        self.subject.setCurrentIndex(max(0, i))
        self._preview()

    def _preview(self):
        """Met à jour l'aperçu du nom de fichier."""
        if hasattr(self, 'name_preview'):
            self.name_preview.setText(
                stem(
                    self.subject.currentText() or 'Sans matière',
                    self.course.text() or 'Titre du cours'
                ) + '.wav'
            )

    def _checked_identity(self):
        """Vérifie que matière et titre sont renseignés."""
        if not self.subject.currentText():
            raise ValueError('Ajoutez et sélectionnez une matière dans Paramètres.')
        if not self.course.text().strip():
            raise ValueError('Renseignez le titre du cours.')
        return (
            self.subject.currentText(),
            self.course.text().strip(),
            stem(self.subject.currentText(), self.course.text())
        )

    def _start(self):
        """Démarre l'enregistrement."""
        try:
            s, t, st = self._checked_identity()
            self.recorder.start(REC / (st + '.wav'), self.mic.currentData())
            from utils.meta import write_meta
            write_meta(st, s, t, 'enregistrement')
            self.parent().statusBar().showMessage('Enregistrement en cours…')
        except Exception as e:
            self.parent().err(str(e))

    def _stop(self):
        """Arrête l'enregistrement."""
        self.recorder.stop()
        self.fmrec.refresh()
        self._refresh()
        self.parent().statusBar().showMessage('Enregistrement terminé')

    def _import_audio(self):
        """Importe un fichier audio."""
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        from utils.helpers import clean
        from utils.meta import write_meta
        import shutil
        
        try:
            s, t, st = self._checked_identity()
            src, _ = QFileDialog.getOpenFileName(
                self, 'Ajouter un fichier audio', '',
                'Audio (*.wav *.mp3 *.m4a *.flac *.ogg *.opus);;Tous les fichiers (*)'
            )
            if not src:
                return
            ext = Path(src).suffix.lower()
            dst = REC / (st + ext)
            if not self._confirm_overwrite(dst, 'Le fichier audio'):
                return
            shutil.copy2(src, dst)
            write_meta(st, s, t, 'fichier importé')
            self.fmrec.refresh()
            self._refresh()
            QMessageBox.information(
                self, 'Fichier ajouté',
                f'Le fichier a été copié et renommé :\n{dst.name}'
            )
        except Exception as e:
            self.parent().err(str(e))

    def _confirm_overwrite(self, path: Path, label: str) -> bool:
        """Demande confirmation avant écrasement."""
        if not path.exists():
            return True
        return QMessageBox.warning(
            self.parent(), 'Fichier existant',
            f'{label} existe déjà :\n\n{path.name}\n\nVoulez-vous l’écraser ? Cette action est irréversible.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        ) == QMessageBox.Yes

    def _refresh(self):
        """Rafraîchit les listes de fichiers."""
        if hasattr(self.parent(), 'trrec'):
            self.parent().trrec.clear()
            self.parent().trrec.addItems([p.name for p in self.fmrec.paths()])
        if hasattr(self.parent(), 'doctr'):
            self.parent().doctr.clear()
            self.parent().doctr.addItems([p.name for p in self.parent().fmtr.paths()])
