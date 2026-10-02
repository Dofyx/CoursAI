from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QScrollArea, QLabel, QMessageBox
from PySide6.QtCore import Qt
from pathlib import Path
import webbrowser


class CfgPage(QWidget):
    """Page de configuration."""
    
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config
        self._init_ui()

    def _init_ui(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        body = QWidget()
        l = QVBoxLayout(body)
        
        # En-tête
        title = QLabel('Paramètres')
        title.setObjectName('title')
        l.addWidget(title)
        l.addWidget(QLabel('Matières et accès Mistral Pay As You Go.'))
        
        # Groupe "Matières"
        g = QGroupBox('Matières, une par ligne')
        gl = QVBoxLayout(g)
        self.subjects = QPlainTextEdit('\n'.join(self.config.get('subjects', [])))
        self.subjects.setMinimumHeight(150)
        gl.addWidget(self.subjects)
        l.addWidget(g)
        
        # Groupe "Mistral AI"
        g = QGroupBox('Mistral AI')
        f = QFormLayout(g)
        self.mistral_key = QLineEdit('')
        self.mistral_key.setEchoMode(QLineEdit.Password)
        f.addRow('Clé API', self.mistral_key)
        
        b = QPushButton('Ouvrir la console Mistral')
        b.clicked.connect(lambda: webbrowser.open('https://console.mistral.ai/'))
        f.addRow('', b)
        l.addWidget(g)
        
        # Groupe "Modèles Mistral"
        g = QGroupBox('Modèles Mistral')
        f = QFormLayout(g)
        self.mtm = QLineEdit(self.config.get('mistral_transcription_model', 'voxtral-mini-latest'))
        f.addRow('Modèle de transcription', self.mtm)
        self.mxm = QLineEdit(self.config.get('mistral_text_model', 'mistral-small-latest'))
        f.addRow('Modèle de résumé', self.mxm)
        l.addWidget(g)
        
        # Bouton de sauvegarde
        b = QPushButton('Enregistrer les paramètres')
        b.clicked.connect(self._save)
        l.addWidget(b)
        
        l.addStretch()
        scroll.setWidget(body)
        outer.addWidget(scroll)
        
        # Charger la clé API
        from config.settings import get_secret
        self.mistral_key.setText(get_secret('mistral_api_key', self.config))
        
        # Ajouter à la layout principale
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(page)

    def _save(self):
        """Sauvegarde la configuration."""
        subjects = []
        for x in self.subjects.toPlainText().splitlines():
            x = x.strip()
            if x and x not in subjects:
                subjects.append(x)
        if not subjects:
            self.parent().err('Ajoutez au moins une matière.')
            return
        
        self.config.update({
            'subjects': subjects,
            'mistral_transcription_model': self.mtm.text().strip() or 'voxtral-mini-latest',
            'mistral_text_model': self.mxm.text().strip() or 'mistral-small-latest'
        })
        
        from config.settings import set_secret, save_config
        set_secret('mistral_api_key', self.mistral_key.text().strip(), self.config)
        save_config(self.config)
        
        # Rafraîchir les matières dans la page d'enregistrement
        if hasattr(self.parent(), 'rec_page'):
            self.parent().rec_page._load_subjects()
        
        self.parent().statusBar().showMessage('Paramètres enregistrés')
