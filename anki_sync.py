from typing import Dict, Optional
import json
import requests
from aqt.utils import showWarning, showInfo
from aqt.qt import QApplication
from PyQt6.QtCore import QThread
from PyQt6.QtCore import QTimer

ANKI_CONNECT_URL = "http://localhost:8766"
DECK_NAME = "English"

CARD_MODELS = {
    "basic": "Basic",
    "basic_reversed": "Basic (and reversed card)",
    "cloze": "Cloze",
    "basic_typing": "Basic (type in the answer)"
}


def show_message_safe(message: str, is_error: bool = False) -> None:
    """Mostra mensagens de forma segura na thread principal"""
    def _show():
        if is_error:
            showWarning(message)
        else:
            showInfo(message)
    
    QTimer.singleShot(0, _show)  # Garante que será executado na thread principal do Qt


def create_card(model: str, fields: Dict[str, str]) -> Optional[int]:
    """
    Cria um card no Anki através do AnkiConnect.
    """
    if model not in CARD_MODELS:
        show_message_safe(f"Erro: Modelo '{model}' não suportado.", True)
        return None
    
    data = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": CARD_MODELS[model],
                "fields": fields,
                "tags": ["AI_generated"]
            }
        }
    }
    
    try:
        response = requests.post(ANKI_CONNECT_URL, json=data, timeout=3)
        response.raise_for_status()
        result = response.json()

        
        if result.get("error"):
            show_message_safe(f"Erro do AnkiConnect: {result['error']}", True)
            return None
            
        show_message_safe("Card criado com sucesso!")
        return result.get("result")
    except requests.exceptions.RequestException as e:
        show_message_safe(f"Erro de conexão com AnkiConnect: {e}", True)
        return None
    except json.JSONDecodeError:
        show_message_safe("Erro ao decodificar resposta do AnkiConnect", True)
        return None