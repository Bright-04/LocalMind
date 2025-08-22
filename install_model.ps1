# Pull the phi3:mini model using the ollama CLI (PowerShell)
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Error "`ollama` CLI not found on PATH. Install Ollama from https://ollama.ai and re-run this script."
    exit 1
}

Write-Host "Pulling phi3:mini via ollama..."
$proc = Start-Process -FilePath "ollama" -ArgumentList "pull", "phi3:mini" -NoNewWindow -Wait -PassThru
if ($proc.ExitCode -ne 0) {
    Write-Error "Failed to pull phi3:mini (exit code $($proc.ExitCode)). Check your Ollama installation and network connectivity."
    exit $proc.ExitCode
}

Write-Host "phi3:mini pulled successfully."
