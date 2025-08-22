from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import subprocess
import shutil


class ChatRequest(BaseModel):
    prompt: str


app = FastAPI(title="LocalMind - Ollama bridge")

# Allow LAN devices to access the API/UI. Adjust origins for stricter security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve the `static/` directory at /static
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def site_root():
    """Return the main UI index page so visiting `/` shows the web UI."""
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    """Lightweight health check. Returns 200 when server is healthy and 503 when Ollama is missing."""
    status = {"status": "ok"}
    if not shutil.which("ollama"):
        status.update({"ollama": False, "detail": "Ollama CLI not found on PATH"})
        return JSONResponse(status_code=503, content=status)
    status.update({"ollama": True})
    return status


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """Forward a chat prompt to the local `ollama` CLI running phi3:mini and return the result.

    This uses the `ollama` binary on PATH. If you don't have Ollama installed, the endpoint
    will return a helpful 500 error with instructions.
    """
    if not shutil.which("ollama"):
        raise HTTPException(status_code=500, detail="Ollama CLI not found. Install Ollama from https://ollama.ai and ensure `ollama` is on PATH.")
    try:
        # Use the ollama CLI to run phi3:mini. This avoids assuming Ollama HTTP API details.
        proc = subprocess.run([
            "ollama",
            "run",
            "phi3:mini",
            "--prompt",
            req.prompt
        ], capture_output=True, text=True, timeout=120)

        if proc.returncode != 0:
            raise HTTPException(status_code=500, detail=(proc.stderr or "Unknown Ollama error").strip())

        return {"response": proc.stdout.strip()}

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Ollama request timed out")
