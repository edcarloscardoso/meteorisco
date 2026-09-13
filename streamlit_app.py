"""
MeteoRisco — Entrypoint Raiz para Deploy no Streamlit Community Cloud.

Redireciona a execução diretamente para o módulo app/streamlit_app.py,
garantindo compatibilidade imediata com a detecção automática do Streamlit Cloud.
"""
import sys
from pathlib import Path
import runpy

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

target_app = ROOT_DIR / "app" / "streamlit_app.py"
runpy.run_path(str(target_app), run_name="__main__")
