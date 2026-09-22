!pip install -q -U fastapi uvicorn pyngrok nest-asyncio diffusers transformers accelerate

import io
import base64
import torch
import nest_asyncio
import uvicorn

from fastapi import FastAPI, WebSocket
from pyngrok import ngrok
from PIL import Image
from diffusers import AutoPipelineForImage2Image

nest_asyncio.apply()

NGROK_TOKEN = ""

if not NGROK_TOKEN:
    raise ValueError("Coloque seu token do ngrok em NGROK_TOKEN.")

ngrok.set_auth_token(NGROK_TOKEN)

device = "cuda" if torch.cuda.is_available() else "cpu"

print("🦆 DuckGen")
print("⏳ Carregando SDXL-Turbo...")

pipe = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
)

if device == "cuda":
    pipe.enable_model_cpu_offload()

    try:
        pipe.enable_xformers_memory_efficient_attention()
        print("⚡ Memória eficiente ativada")
    except Exception:
        pass

print("✅ Modelo pronto")

app = FastAPI()


@app.get("/")
async def home():
    return {
        "status": "DuckGen Online",
        "device": device
    }


@app.websocket("/duckgen/v1/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()

    print("🟢 Cliente DuckGen conectado")

    prompt = (
        "high quality game scene, realistic lighting, "
        "sharp details, detailed textures, clean image"
    )

    try:
        while True:
            data = await websocket.receive_text()

            image = Image.open(
                io.BytesIO(
                    base64.b64decode(data)
                )
            ).convert("RGB")

            image = image.resize(
                (512, 512),
                Image.Resampling.LANCZOS
            )

            with torch.inference_mode():
                result = pipe(
                    prompt=prompt,
                    image=image,
                    num_inference_steps=1,
                    strength=0.35,
                    guidance_scale=0.0
                ).images[0]

            buffer = io.BytesIO()

            result.save(
                buffer,
                format="JPEG",
                quality=80,
                optimize=True
            )

            await websocket.send_text(
                base64.b64encode(
                    buffer.getvalue()
                ).decode("utf-8")
            )

    except Exception as e:
        print(f"🔴 Cliente desconectado: {e}")

    finally:
        try:
            await websocket.close()
        except:
            pass


public_url = ngrok.connect(8000)

domain = (
    public_url.public_url
    .replace("https://", "")
    .replace("http://", "")
    .strip("/")
)

print()
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🦆 DUCKGEN ONLINE")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()
print("COPIE ESTE DOMÍNIO NO DUCKGEN:")
print()
print(domain)
print()
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"WebSocket: wss://{domain}/duckgen/v1/stream")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

config = uvicorn.Config(
    app,
    host="127.0.0.1",
    port=8000,
    log_level="warning"
)

server = uvicorn.Server(config)

await server.serve()
