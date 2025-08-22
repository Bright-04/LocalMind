# LocalMind

A self-hosted LAN AI Assistant powered by Ollama and Open WebIO.

## Quick start

1.  Install Ollama from https://ollama.ai and ensure the `ollama` CLI is on your PATH.
    Optionally, pull the phi3:mini model locally (see `install_model.ps1`):

        .\install_model.ps1

2.  Create a Python virtual environment and install dependencies:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

3.  Start the backend (PowerShell):

    .\run.ps1

4.  Open http://<your-lan-ip>:8000/static/ in a browser on the same LAN and try a prompt.

## Notes

-   This project uses the `ollama run phi3:mini` command under the hood. Replace `phi3:mini` with another local model name if desired.
-   The backend expects the `ollama` CLI to be installed locally and accessible from the server environment.

## Install model helper

There's a small PowerShell helper `install_model.ps1` that attempts to pull `phi3:mini` using the `ollama` CLI. Run it after installing Ollama to download the model.

