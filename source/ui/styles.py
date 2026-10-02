"""Styles CSS pour l'application CoursIA."""

STYLE = """
QWidget{
    background:#0b1220;
    color:#e6edf7;
    font-family:Inter,Segoe UI,sans-serif;
    font-size:14px
}

#side{
    background:#111a2b;
    border-right:1px solid #26344d
}

#brand{
    font-size:28px;
    font-weight:700;
    color:#62d0ff;
    margin:20px 8px 2px
}

#side QPushButton{
    padding:14px;
    text-align:left;
    border:0;
    border-radius:9px;
    margin:3px;
    background:transparent
}

#side QPushButton:hover{
    background:#1a2942
}

#side QPushButton:checked{
    background:#1677ff;
    color:white
}

QLabel#title{
    font-size:26px;
    font-weight:700;
    color:white;
    margin-top:12px
}

QGroupBox{
    border:1px solid #26344d;
    border-radius:12px;
    margin-top:16px;
    padding:16px;
    background:#101a2a;
    font-weight:600
}

QGroupBox::title{
    subcontrol-origin:margin;
    left:14px;
    padding:0 6px;
    color:#8bdcff
}

QPushButton{
    background:#1677ff;
    border:0;
    border-radius:8px;
    padding:9px 14px;
    font-weight:600
}

QPushButton:hover{
    background:#4096ff
}

QLineEdit, QComboBox, QListWidget, QPlainTextEdit{
    background:#0b1424;
    border:1px solid #31415f;
    border-radius:8px;
    padding:8px;
    selection-background-color:#1677ff
}

QStatusBar{
    background:#101a2a;
    color:#9fb3cc
}
"""
