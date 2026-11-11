# Genera el .zip de entrega sin la contraseña ni el entorno virtual.
# Uso:  powershell -ExecutionPolicy Bypass -File empaquetar.ps1

$ErrorActionPreference = "Stop"

$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
$nombreZip = "facturacion_streamlit.zip"
$destino = Join-Path $raiz $nombreZip
$temporal = Join-Path $env:TEMP ("facturacion_" + [guid]::NewGuid().ToString("N"))

Write-Host "Copiando archivos a una carpeta temporal..."
New-Item -ItemType Directory -Path $temporal | Out-Null

$excluir = @(".venv", "venv", "__pycache__", ".git", ".pytest_cache")

Get-ChildItem -LiteralPath $raiz -Force | Where-Object {
    $_.Name -notin $excluir -and
    $_.Name -ne $nombreZip
} | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $temporal -Recurse -Force
}

Write-Host "Quitando secrets.toml y archivos temporales de la copia..."
Get-ChildItem -Path $temporal -Recurse -Force -File |
    Where-Object { $_.Name -eq "secrets.toml" -or $_.Extension -eq ".pyc" } |
    Remove-Item -Force

Get-ChildItem -Path $temporal -Recurse -Force -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force

if (Test-Path -LiteralPath $destino) {
    Remove-Item -LiteralPath $destino -Force
}

Write-Host "Comprimiendo..."
Compress-Archive -Path (Join-Path $temporal "*") -DestinationPath $destino -Force
Remove-Item -LiteralPath $temporal -Recurse -Force

Write-Host ""
Write-Host "Listo: $destino"
Write-Host "Recuerda revisar que NO esté .streamlit/secrets.toml."
