# Start the local llama-server in router mode: all models in tools\models.ini are selectable and load on demand.
# One shared llama.cpp build for the whole project.
#   playground: port 8081, web UI at http://127.0.0.1:8081 (model picker), 1 model resident at a time
#   real:       port 8082, for sprint runs, 2 models resident (agents + replacement); refuses to start before 2026-10-23
# usage: .\tools\serve.ps1 [-Mode playground|real]
#   -Lan: playground only, listen on all network interfaces (no login!) instead of this PC only; for brief demos
param([ValidateSet('playground', 'real')][string]$Mode = 'playground', [switch]$Lan)
if ($Lan -and $Mode -eq 'real') { throw '-Lan is for the playground only.' }
$bindHost = if ($Lan) { '0.0.0.0' } else { '127.0.0.1' }
$bin = 'D:\llm\llama.cpp\b11798\llama-server.exe'
if ($Mode -eq 'real' -and (Get-Date) -lt [datetime]'2026-10-23') {
    throw 'real mode is locked until 2026-10-23 (no sprint runs before the start). Use -Mode playground.'
}
$port = if ($Mode -eq 'real') { 8082 } else { 8081 }   # 8080 is taken by another local service
$max = if ($Mode -eq 'real') { 2 } else { 1 }   # ponytail: check VRAM before raising; 16 GB fits e.g. 8B + 12B, not gpt-oss-20b + anything
$slots = if ($Mode -eq 'real') { '--parallel', '4', '--ctx-size', '32768' } else { @() }   # real: 4 agent slots x 8k each; playground uses models.ini (1 slot)
$logs = "D:\llm\logs\$Mode"
New-Item -ItemType Directory -Force $logs | Out-Null
# playground UI is a locally renamed copy of the built-in web UI (see D:\llm\playground-ui); falls back to the built-in one
$ui = @(); if ($Mode -eq 'playground' -and (Test-Path 'D:\llm\playground-ui\index.html')) {
    Copy-Item "$PSScriptRoot\playground\shortcuts.js" 'D:\llm\playground-ui\shortcuts.js' -Force   # keyboard shortcuts, source of truth is in the repo
    $ui = '--path', 'D:\llm\playground-ui'
}
& $bin --models-preset "$PSScriptRoot\models.ini" --models-max $max --host $bindHost --port $port @ui @slots `
    --log-file "$logs\router-$(Get-Date -Format yyyyMMdd_HHmm).log"
