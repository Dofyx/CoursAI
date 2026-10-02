from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QComboBox, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from pathlib import Path

from config.paths import DOC, TR
from audio.manager import Manager


class DocPage(QWidget):
    """Page de génération des résumés et fiches de révision."""
    
    def __init__(self, parent, bus, config):
        super().__init__(parent)
        self.bus = bus
        self.config = config
        self._init_ui()

    def _init_ui(self):
        l = QVBoxLayout(self)
        
        # En-tête
        title = QLabel('Résumés et fiches de révision')
        title.setObjectName('title')
        l.addWidget(title)
        l.addWidget(QLabel('Deux productions pédagogiques distinctes avec Mistral.'))
        
        # Groupe "Générer"
        g = QGroupBox('Générer')
        f = QFormLayout(g)
        f.addRow('IA', QLabel('Mistral'))
        
        # Liste des transcriptions
        self.doctr = QComboBox()
        f.addRow('Retranscription', self.doctr)
        
        # Boutons de génération
        h = QHBoxLayout()
        for text, kind in [('Créer le résumé', 'resume'), ('Créer la fiche de révision', 'fiche')]:
            b = QPushButton(text)
            b.clicked.connect(lambda _, x=kind: self._document(x))
            h.addWidget(b)
        f.addRow(h)
        
        l.addWidget(g)
        
        # Gestionnaire de fichiers
        self.fmdoc = Manager('Documents Word', DOC, ['*.docx'])
        l.addWidget(self.fmdoc, 1)

    def _document(self, kind: str):
        """Génère un document (résumé ou fiche)."""
        self._refresh()
        n = self.doctr.currentText()
        if not n:
            self.parent().err('Aucune retranscription sélectionnée.')
            return
        
        from config.settings import get_secret
        k = get_secret('mistral_api_key', self.config)
        if not k:
            self.parent().err('Renseignez la clé Mistral dans Paramètres.')
            return
        
        source = TR / n
        suffix = '_resume.docx' if kind == 'resume' else '_fiche_revision.docx'
        out = DOC / (source.stem + suffix)
        if not self._confirm_overwrite(out, 'Le document Word'):
            return
        
        self.parent().bg(self.parent()._do_document, source, kind, k)

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
        """Rafraîchit la liste des transcriptions."""
        from config.paths import TR
        from audio.manager import Manager
        temp_manager = Manager('Temp', TR, ['*.txt'])
        self.doctr.clear()
        self.doctr.addItems([p.name for p in temp_manager.paths()])
