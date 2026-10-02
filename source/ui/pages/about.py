from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout
from PySide6.QtCore import Qt
from pathlib import Path
import webbrowser

from utils.helpers import open_file


class AboutPage(QWidget):
    """Page "À propos"."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        l = QVBoxLayout(self)
        l.setContentsMargins(70, 35, 70, 35)
        l.addStretch()
        
        # Logo
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        from utils.helpers import open_file
        from pathlib import Path
        
        def asset(name):
            return Path(__file__).parent.parent.parent / 'assets' / name
        
        from PySide6.QtGui import QPixmap
        pix = QPixmap(str(asset('logo.png')))
        if not pix.isNull():
            logo.setPixmap(pix.scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        l.addWidget(logo)
        
        # Titre
        brand = QLabel('CoursIA')
        brand.setAlignment(Qt.AlignCenter)
        brand.setStyleSheet('font-size:34px;font-weight:800;color:#62d0ff;')
        l.addWidget(brand)
        
        # Version
        version = QLabel('Version 0.6')
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet('font-size:18px;color:#9fb3cc;margin-bottom:18px;')
        l.addWidget(version)
        
        # Description
        tag = QLabel('Enregistrement, transcription et révision universitaire assistés par Mistral AI')
        tag.setWordWrap(True)
        tag.setAlignment(Qt.AlignCenter)
        l.addWidget(tag)
        
        # Licence
        card = QGroupBox('Licence')
        cl = QVBoxLayout(card)
        lic = QLabel('<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr" style="color:#62d0ff;">Creative Commons Attribution - Pas d’Utilisation Commerciale - Partage dans les Mêmes Conditions 4.0 International</a>')
        lic.setTextFormat(Qt.RichText)
        lic.setTextInteractionFlags(Qt.TextBrowserInteraction)
        lic.setOpenExternalLinks(True)
        lic.setWordWrap(True)
        lic.setAlignment(Qt.AlignCenter)
        cl.addWidget(lic)
        note = QLabel('CC BY-NC-SA 4.0')
        note.setAlignment(Qt.AlignCenter)
        cl.addWidget(note)
        l.addWidget(card)
        
        # Crédits
        credit = QLabel('Developed by Dofyx AI Corp')
        credit.setAlignment(Qt.AlignCenter)
        credit.setStyleSheet('font-size:20px;font-weight:700;color:white;margin-top:22px;')
        l.addWidget(credit)
        
        # Lien GitHub
        github = QLabel('<a href="https://github.com/Dofyx/CoursAI" style="color:#62d0ff;">GitHub - Dofyx/CoursAI</a>')
        github.setTextFormat(Qt.RichText)
        github.setTextInteractionFlags(Qt.TextBrowserInteraction)
        github.setOpenExternalLinks(True)
        github.setAlignment(Qt.AlignCenter)
        github.setStyleSheet('font-size:15px;margin-top:10px;')
        l.addWidget(github)
        
        l.addStretch()
