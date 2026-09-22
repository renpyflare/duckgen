import sys
import subprocess
import urllib.request
from pathlib import Path

RAW_URL = "https://raw.githubusercontent.com/renpyflare/duckgen/refs/heads/main/duckgen_colab.py"
TARGET = Path("/content/duckgen_colab.py")

print("🦆 DuckGen")
print("⏳ Baixando servidor principal...")

urllib.request.urlretrieve(
    RAW_URL,
    TARGET
)

print("✅ Servidor baixado.")
print("🚀 Iniciando DuckGen...")
print()

subprocess.run(
    [
        sys.executable,
        str(TARGET)
    ],
    check=False
)
