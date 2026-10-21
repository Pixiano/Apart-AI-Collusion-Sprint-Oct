# Start the local llama-server in router mode: all models in tools\models.ini are selectable and load on demand.
# One shared llama.cpp build for the whole project.
#   playground: port 8081, web UI at http://127.0.0.1:8081 (model picker), 1 model resident at a time
#   real:       port 8080, for sprint runs, 2 models resident (agents + replacement); refuses to start before 2026-10-23
# usage: .\tools\serve.ps1 [-Mode playground|real]
param([ValidateSet('playground', 'real')][string]$Mode = 'playground')
$bin = 'D:\llm\llama.cpp\b11798\llama-server.exe'
if ($Mode -eq 'real' -and (Get-Date) -lt [datetime]'2026-10-23') {
    throw 'real mode is locked until 2026-10-23 (no sprint runs before the start). Use -Mode playground.'
}
$port = if ($Mode -eq 'real') { 8080 } else { 8081 }
$max = if ($Mode -eq 'real') { 2 } else { 1 }   # ponytail: check VRAM before raising; 16 GB fits e.g. 8B + 12B, not gpt-oss-20b + anything
$logs = "D:\llm\logs\$Mode"
New-Item -ItemType Directory -Force $logs | Out-Null
# playground UI is a locally renamed copy of the built-in web UI (see D:\llm\playground-ui); falls back to the built-in one
$ui = @(); if ($Mode -eq 'playground' -and (Test-Path 'D:\llm\playground-ui\index.html')) { $ui = '--path', 'D:\llm\playground-ui' }
& $bin --models-preset "$PSScriptRoot\models.ini" --models-max $max --host 127.0.0.1 --port $port @ui `
    --log-file "$logs\router-$(Get-Date -Format yyyyMMdd_HHmm).log"
