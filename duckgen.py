import subprocess
import sys
import urllib.request
from pathlib import Path

RAW_URL = "https://raw.githubusercontent.com/renpyflare/duckgen/refs/heads/main/duckgen_colab.py"
TARGET = Path("/content/duckgen_colab.py")


def main():
    print("🦆 DuckGen")
    print("📦 Instalando dependências...")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "-U",
            "fastapi",
            "uvicorn",
            "pyngrok",
            "nest-asyncio",
            "diffusers",
            "transformers",
            "accelerate"
        ],
        check=True
    )

    print("✅ Dependências instaladas.")
    print("🌐 Baixando servidor DuckGen...")

    urllib.request.urlretrieve(
        RAW_URL,
        TARGET
    )

    print("✅ Servidor baixado.")
    print("🚀 Iniciando DuckGen...")
    print()

    subprocess.run(
        [sys.executable, str(TARGET)],
        check=False
    )


if __name__ == "__main__":
    main()
