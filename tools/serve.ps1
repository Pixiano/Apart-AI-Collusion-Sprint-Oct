# Start a local llama-server. One shared llama.cpp build for the whole project.
#   playground: port 8081, web UI at http://127.0.0.1:8081 , for internal testing only
#   real:       port 8080, for sprint runs; refuses to start before the sprint (2026-10-23)
# usage: .\tools\serve.ps1 [-Mode playground|real] [-Model qwen3-8b|qwen3-14b|gemma4-12b|gpt-oss-20b] [-Parallel 4]
param(
    [ValidateSet('playground', 'real')][string]$Mode = 'playground',
    [ValidateSet('qwen3-8b', 'qwen3-14b', 'gemma4-12b', 'gpt-oss-20b')][string]$Model = 'qwen3-8b',
    [int]$Parallel = 4,
    [int]$CtxPerSlot = 4096
)
$bin = 'D:\llm\llama.cpp\b11798\llama-server.exe'
$lm = 'C:\Users\Dhiraj Vatsal\.lmstudio\models\lmstudio-community'
$gguf = @{
    'qwen3-8b'    = "$lm\Qwen3-8B-GGUF\Qwen3-8B-Q4_K_M.gguf"
    'qwen3-14b'   = "$lm\Qwen3-14B-GGUF\Qwen3-14B-Q4_K_M.gguf"
    'gemma4-12b'  = "$lm\gemma-4-12B-it-QAT-GGUF\gemma-4-12B-it-QAT-Q4_0.gguf"
    'gpt-oss-20b' = "$lm\gpt-oss-20b-GGUF\gpt-oss-20b.gguf"
}
if ($Mode -eq 'real' -and (Get-Date) -lt [datetime]'2026-10-23') {
    throw 'real mode is locked until 2026-10-23 (no sprint runs before the start). Use -Mode playground.'
}
$port = if ($Mode -eq 'real') { 8080 } else { 8081 }
$logs = "D:\llm\logs\$Mode"
New-Item -ItemType Directory -Force $logs | Out-Null
# -c is split across slots; -ngl 99 = full GPU offload
& $bin -m $gguf[$Model] --alias $Model --host 127.0.0.1 --port $port `
    -ngl 99 --parallel $Parallel -c ($Parallel * $CtxPerSlot) `
    --log-file "$logs\$Model-$(Get-Date -Format yyyyMMdd_HHmm).log"
