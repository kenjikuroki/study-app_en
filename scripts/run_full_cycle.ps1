$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$runnerScript = Join-Path $scriptDir "studyapp_full_cycle_runner.py"

$pythonExe = "C:\Users\kurok\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path $pythonExe)) {
  throw "Bundled Python runtime not found: $pythonExe"
}

Push-Location $repoRoot
try {
  & $pythonExe $runnerScript @args
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
