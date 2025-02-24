from .check_dependencies import install_requirements
install_requirements()

from aqt import mw
from aqt.qt import QAction, qconnect
from .anki_sync import create_card
from .server import run_server

def test_add_card() -> None:
    fields = {
        "Front": "What is the capital of France?",
        "Back": "Paris"
    }
    
    create_card("basic", fields)

def init_addon():
    # Adicionar ação ao menu principal (thread-safe)
    action = QAction("Test AI Sync", mw)
    qconnect(action.triggered, test_add_card)
    mw.form.menuTools.addAction(action)
    
    # Iniciar servidor em thread daemon
    from threading import Thread
    server_thread = Thread(target=run_server, daemon=True, name="AnkiAddonServer")
    server_thread.start()

# Inicializar quando o Anki carregar
mw.app.aboutToQuit.connect(lambda: None)  # Previne crash ao fechar
init_addon()