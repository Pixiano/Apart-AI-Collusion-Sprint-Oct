# Swap study (main sweep): per seed one base run (rounds 1-30, checkpoint) then four hidden, one-firm branches from that checkpoint: none (control), clone, family, undercutter (positive control).
# Set EASY=profit in the environment for models run on the easy prompt. Needs the real-mode server. Main data is kept apart from pilot data (new seeds).
# usage: .\tools\swapstudy.ps1 [-Model gemma4-12b] [-Seeds 11..20] [-Out data/main]
param([string]$Model = 'gemma4-12b', [int[]]$Seeds = (11..20), [string]$Out = 'data/main', [int]$K = 1, [string[]]$Swaps = @('none', 'clone', 'family', 'undercutter'), [switch]$Announce, [ValidateSet('on', 'off')][string]$Comm = 'on')  # -K 2: two of three replaced; -Announce: announced swap; -Comm off: communication off (base-run factor); -Swaps picks the branches (existing base checkpoints are reused)
Set-Location (Split-Path $PSScriptRoot)
$py = '.\.venv\Scripts\python.exe'
foreach ($s in $Seeds) {
    $d = "$Out/${Model}_comm${Comm}_s$s"  # restart-safe: a finished base run is skipped, an interrupted one resumes, finished branches return at once
    if (-not (Test-Path "$d/checkpoint.json")) {
        if (Test-Path "$d/base/rounds.jsonl") { & $py -m harness.run resume --run $d --to 30 } else { & $py -m harness.run base --model $Model --comm $Comm --seed $s --out $Out }
    }
    $extra = @(); if ($Announce) { $extra = @('--announce') }
    foreach ($w in $Swaps) { & $py -m harness.run branch --run $d --swap $w --k $K @extra }
}
