# Swap study (main sweep): per seed one base run (rounds 1-30, checkpoint) then four hidden, one-firm branches from that checkpoint: none (control), clone, family, undercutter (positive control).
# Set EASY=profit in the environment for models run on the easy prompt. Needs the real-mode server. Main data is kept apart from pilot data (new seeds).
# usage: .\tools\swapstudy.ps1 [-Model gemma4-12b] [-Seeds 11..20] [-Out data/main]
param([string]$Model = 'gemma4-12b', [int[]]$Seeds = (11..20), [string]$Out = 'data/main')
Set-Location (Split-Path $PSScriptRoot)
$py = '.\.venv\Scripts\python.exe'
foreach ($s in $Seeds) {
    & $py -m harness.run base --model $Model --comm on --seed $s --out $Out
    foreach ($w in 'none', 'clone', 'family', 'undercutter') { & $py -m harness.run branch --run "$Out/${Model}_common_s$s" --swap $w --k 1 }
}
