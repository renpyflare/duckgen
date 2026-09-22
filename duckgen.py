import subprocess
import sys
import urllib.request
from pathlib import Path

RAW_URL = "https://raw.githubusercontent.com/renpyflare/duckgen/refs/heads/main/duckgen_colab.py"

TARGET = Path("/content/duckgen_colab.py")

PACKAGES = [
    "fastapi",
    "uvicorn",
    "pyngrok",
    "nest-asyncio",
    "diffusers",
    "transformers",
    "accelerate"
]


def install_dependencies():
    print("📦 Instalando dependências...")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "-U",
            *PACKAGES
        ],
        check=True
    )

    print("✅ Dependências instaladas.")
    print()


def download_server():
    print("🌐 Baixando servidor DuckGen...")

    urllib.request.urlretrieve(
        RAW_URL,
        TARGET
    )

    print("✅ Servidor baixado.")
    print()


def start_server():
    print("🚀 Iniciando DuckGen...")
    print()

    subprocess.run(
        [sys.executable, str(TARGET)],
        check=False
    )


def main():
    install_dependencies()
    download_server()
    start_server()


if __name__ == "__main__":
    main()
