import sys
import subprocess
import urllib.request
from pathlib import Path

RAW_URL = "https://raw.githubusercontent.com/renpyflare/duckgen/refs/heads/main/duckgen_colab.py"

BASE_DIR = Path(__file__).resolve().parent
TARGET = BASE_DIR / "duckgen_colab.py"


def download():
    print("🦆 DuckGen")
    print("⏳ Baixando servidor principal...")

    try:
        urllib.request.urlretrieve(
            RAW_URL,
            TARGET
        )
    except Exception as e:
        print()
        print("❌ Falha ao baixar o servidor.")
        print(e)
        sys.exit(1)

    print("✅ Servidor baixado.")
    print()


def run():
    print("🚀 Iniciando DuckGen...")
    print()

    subprocess.run(
        [sys.executable, str(TARGET)],
        check=False
    )


if __name__ == "__main__":
    download()
    run()
