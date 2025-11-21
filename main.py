# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.ventana_principal import VentanaPrincipal

def main():
    app = QApplication(sys.argv)
    # Cargar estilo global si existe
    try:
        import os
        style_path = os.path.join(os.path.dirname(__file__), "recursos", "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
    except Exception:
        pass

    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
