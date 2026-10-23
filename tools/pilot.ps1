# Pilot: base runs (rounds 1-30) for 3 seeds x 2 models with communication on, then the gate table. Run after the sanity checks pass
# and with the real-mode server up (.\tools\serve.ps1 -Mode real). Pilot data stays in data\pilot and is never pooled with main data.
# usage: .\tools\pilot.ps1 [-Seeds 1,2,3] [-Models qwen3-14b,gemma4-12b]
param([int[]]$Seeds = @(1, 2, 3), [string[]]$Models = @('qwen3-14b', 'gemma4-12b'), [string]$Out = 'data/pilot')
Set-Location (Split-Path $PSScriptRoot)
$py = '.\.venv\Scripts\python.exe'
foreach ($m in $Models) { foreach ($s in $Seeds) { & $py -m harness.run base --model $m --comm on --seed $s --out $Out } }
& $py -m harness.analyze gate $Out
