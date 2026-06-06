param(
  [Parameter(Mandatory = $true)]
  [string]$AppId,
  [string]$Date = "2026-06-06"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$runnerScript = Join-Path $scriptDir "studyapp_app_runner.py"

$pythonExe = "C:\Users\kurok\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path $pythonExe)) {
  throw "Bundled Python runtime not found: $pythonExe"
}

Push-Location $repoRoot
try {
  & $pythonExe $runnerScript --app-id $AppId --date $Date
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
