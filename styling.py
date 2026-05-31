# styling.py
from PyQt5.QtGui import QFont

def app_stylesheet():
    return """
    /* Main Window Background */
    #SearchApp, QDialog, QMainWindow {
        background-color: #f4f5f7;
    }
    
    /* Reset background for standard widgets so they do not inherit the window background */
    QLabel {
        background-color: transparent;
        color: #334155;
        font-family: "Poppins", "Arial", sans-serif;
        font-size: 13px;
    }
    
    QRadioButton {
        background-color: transparent;
        color: #475569;
        font-family: "Poppins", "Arial", sans-serif;
        font-weight: 500;
        padding: 4px;
        spacing: 6px;
    }
    
    QRadioButton::indicator {
        width: 14px;
        height: 14px;
        border-radius: 7px;
        border: 2px solid #cbd5e1;
        background-color: #ffffff;
    }
    
    QRadioButton::indicator:checked {
        background-color: #0b5ed7;
        border: 2px solid #0056b3;
    }
    
    /* Headers */
    QLabel#header_title {
        color: #1e3a8a;
        font-size: 18px;
        font-weight: bold;
    }
    
    QLabel#sidebar_title {
        font-size: 16px;
        font-weight: 700;
        color: #0b5ed7;
        padding: 10px 5px;
        background-color: transparent;
    }
    
    /* Sidebar Frame */
    QFrame#sidebar_frame {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    QPushButton#sidebar_btn {
        background-color: transparent;
        color: #64748b;
        border: none;
        border-radius: 6px;
        padding: 10px 15px;
        text-align: left;
        font-weight: 500;
        font-family: "Poppins", "Arial", sans-serif;
    }
    
    QPushButton#sidebar_btn:hover {
        background-color: #f1f5f9;
        color: #0b5ed7;
    }
    
    QPushButton#sidebar_btn:pressed {
        background-color: #e2e8f0;
    }
    
    /* Stats Card Styling */
    QFrame#stats_card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px;
    }
    
    QFrame#stats_card QLabel {
        background-color: transparent;
    }
    
    QLabel#stats_value {
        font-size: 20px;
        font-weight: bold;
        color: #1e293b;
    }
    
    QLabel#stats_label {
        font-size: 11px;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    /* White Card GroupBox Styles */
    QGroupBox {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        margin-top: 14px;
        padding-top: 10px;
        padding-left: 0px;
        padding-right: 0px;
        padding-bottom: 0px;
        background-color: #ffffff;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        margin-top: -7px;
        padding: 0 6px;
        color: #0b5ed7;
        font-weight: bold;
        font-size: 13px;
        background-color: #ffffff;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #0b5ed7;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 8px 14px;
        font-weight: 600;
        font-family: "Poppins", "Arial", sans-serif;
    }
    
    QPushButton:hover {
        background-color: #0056b3;
    }
    
    QPushButton:pressed {
        background-color: #004085;
    }
    
    QPushButton#btn_secondary {
        background-color: #ffffff;
        color: #475569;
        border: 1px solid #cbd5e1;
    }
    
    QPushButton#btn_secondary:hover {
        background-color: #f1f5f9;
        color: #1e293b;
    }
    
    /* Inputs */
    QLineEdit, QComboBox, QSpinBox {
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 7px;
        background-color: #ffffff;
        color: #1e293b;
        font-family: "Poppins", "Arial", sans-serif;
    }
    
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
        border: 2px solid #0b5ed7;
    }
    
    /* Tables */
    QTableWidget {
        background-color: #ffffff;
        gridline-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        color: #334155;
        font-family: "Poppins", "Arial", sans-serif;
    }
    
    QHeaderView::section {
        background-color: #f8fafc;
        color: #475569;
        padding: 8px;
        border: none;
        font-weight: 600;
        border-bottom: 2px solid #e2e8f0;
        font-family: "Poppins", "Arial", sans-serif;
    }
    
    QTableWidget::item:selected {
        background-color: #eff6ff;
        color: #0b5ed7;
    }
    
    /* Text Edits */
    QTextEdit {
        background-color: #ffffff;
        color: #1e293b;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px;
        font-family: "Poppins", "Arial", sans-serif;
    }
    
    /* Splitter handle — the draggable divider between panels */
    QSplitter::handle {
        background-color: #e2e8f0;
        border-radius: 2px;
        margin: 4px 1px;
    }
    
    QSplitter::handle:hover {
        background-color: #0b5ed7;
    }
    
    QSplitter::handle:pressed {
        background-color: #0056b3;
    }
    """

def title_font():
    f = QFont("Poppins", 14, QFont.Bold)
    if not f.exactMatch():
        f = QFont("Arial", 14, QFont.Bold)
    return f

def subtitle_font():
    f = QFont("Poppins", 10, QFont.Bold)
    if not f.exactMatch():
        f = QFont("Arial", 10, QFont.Bold)
    return f
