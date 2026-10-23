# Round-1 spread test: how much does the sampling seed alone change the opening prices? Plays only round 1, N seeds, then prints a price histogram.
# Set EASY/VARIANT in the environment first to test a non-base prompt. Needs the real-mode server (use when no other run is active).
# usage: .\tools\round1_spread.ps1 [-Model phi4-14b] [-N 50] [-Out data/round1]
param([string]$Model = 'phi4-14b', [int]$N = 50, [string]$Out = 'data/round1')
Set-Location (Split-Path $PSScriptRoot)
$py = '.\.venv\Scripts\python.exe'
$env:ROUNDS = '1'
foreach ($s in 1..$N) { & $py -m harness.run base --model $Model --comm on --seed $s --out $Out *> $null }
& $py -I -c "
import collections, glob, json, sys
c = collections.Counter(p for f in glob.glob('$Out/${Model}_common_s*/base/rounds.jsonl') for p in json.loads(open(f).readline())['prices'])
n = sum(c.values()); print('round-1 prices over', n, 'replies:'); [print(f'{p:3d} {\"#\" * round(40 * k / n)} {k}') for p, k in sorted(c.items())]"
