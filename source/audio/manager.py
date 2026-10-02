from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QInputDialog, QMessageBox
from PySide6.QtCore import Qt
from pathlib import Path
from typing import List, Optional

from utils.helpers import open_file, clean


class Manager(QGroupBox):
    """Gestionnaire de fichiers (liste, ouverture, renommage, suppression)."""
    
    def __init__(self, title: str, folder: Path, patterns: List[str]):
        super().__init__(title)
        self.folder = folder
        self.patterns = patterns
        
        # Layout
        l = QVBoxLayout(self)
        self.list = QListWidget()
        l.addWidget(self.list)
        
        # Boutons
        h = QHBoxLayout()
        for text, func in [
            ('Ouvrir', self.open),
            ('Renommer', self.rename),
            ('Supprimer', self.delete)
        ]:
            b = QPushButton(text)
            b.clicked.connect(func)
            h.addWidget(b)
        l.addLayout(h)
        
        self.refresh()

    def paths(self) -> List[Path]:
        """Retourne la liste des fichiers correspondant aux patterns."""
        a = []
        for pattern in self.patterns:
            a += list(self.folder.glob(pattern))
        return sorted(set(a), key=lambda p: p.stat().st_mtime, reverse=True)

    def refresh(self) -> None:
        """Rafraîchit la liste des fichiers."""
        self.list.clear()
        self.list.addItems([p.name for p in self.paths()])

    def selected(self) -> Optional[Path]:
        """Retourne le fichier sélectionné, ou None."""
        if self.list.currentItem():
            return self.folder / self.list.currentItem().text()
        return None

    def open(self) -> None:
        """Ouvre le fichier sélectionné."""
        selected = self.selected()
        if selected:
            open_file(selected)

    def rename(self) -> None:
        """Renomme le fichier sélectionné."""
        p = self.selected()
        if not p:
            return
        
        n, ok = QInputDialog.getText(
            self, 'Renommer', 'Nouveau nom', text=p.stem
        )
        if ok and n:
            from utils.helpers import clean
            old_stem = p.stem
            p.rename(p.with_name(clean(n) + p.suffix))
            
            # Renommer aussi les métadonnées
            from utils.meta import meta_path
            m = meta_path(old_stem)
            if m.exists():
                m.rename(meta_path(clean(n)))
            
            self.refresh()

    def delete(self) -> None:
        """Supprime le fichier sélectionné."""
        p = self.selected()
        if p and QMessageBox.question(
            self, 'Suppression', f'Supprimer {p.name} ?'
        ) == QMessageBox.Yes:
            from utils.meta import meta_path
            m = meta_path(p.stem)
            p.unlink()
            m.unlink(missing_ok=True)
            self.refresh()
