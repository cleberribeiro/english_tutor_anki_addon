import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias para o addon"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        return True
    except subprocess.CalledProcessError:
        return False

# Verifica se o requests está instalado, se não, tenta instalar
try:
    import requests
except ImportError:
    if not install_requirements():
        from aqt.utils import showWarning
        showWarning("Não foi possível instalar as dependências necessárias. Por favor, instale o módulo 'requests' manualmente.")